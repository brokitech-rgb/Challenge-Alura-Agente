"""El agente: decide qué herramientas usar y redacta la respuesta final.

El ciclo es el clásico de un agente con herramientas:

    pregunta -> el modelo elige herramienta(s) -> se ejecutan localmente
             -> los resultados vuelven al modelo -> repetir hasta que responda

La documentación nunca entra entera en el prompt. El modelo pide sólo los
fragmentos que necesita a través de `buscar_en_documentacion`, lo que mantiene
el consumo de tokens bajo y acotado sin importar cuánto crezca el corpus.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from .config import CONFIG, Config
from .retriever import Buscador
from .tools import ESQUEMAS_HERRAMIENTAS, Herramientas

INSTRUCCIONES = """\
Sos el asistente de soporte oficial de Brokitech Turnos, un SaaS argentino de \
gestión de turnos con cobro de seña por WhatsApp.

Reglas que no podés romper:

1. Respondé ÚNICAMENTE con información obtenida de las herramientas. No completes \
   con conocimiento general ni supongas datos que no viste.
2. Antes de responder cualquier consulta de contenido, llamá a una herramienta. \
   Si la pregunta menciona precios, planes o cupos, usá `consultar_planes` \
   (los datos del CSV son la fuente exacta) además de `buscar_en_documentacion`.
3. Citá la fuente al final, con este formato exacto:
   Fuente: <documento>, pág. <n>
   Si usaste varias, listalas todas.
4. Si las herramientas no traen la información, decilo con claridad: "Eso no está \
   cubierto en la documentación que tengo". No inventes. Ofrecé escalar a soporte \
   humano y, si el usuario acepta o el caso lo amerita, llamá a `escalar_a_humano`.
5. Nunca prometas funcionalidades que figuren como "en roadmap", "en beta" o \
   "no planificado" como si estuvieran disponibles. Aclará su estado real.
6. Los precios se citan siempre en pesos argentinos con IVA incluido, tal como \
   figuran en la fuente. No conviertas monedas ni estimes valores.

Estilo: español rioplatense, tuteo con "vos", tono profesional pero cercano. \
Andá al grano: primero la respuesta concreta, después el detalle. Usá listas o \
tablas cuando ayuden. No abras con saludos largos ni cierres con relleno.
"""


@dataclass
class Traza:
    """Registro de una llamada a herramienta, para mostrar el razonamiento."""

    herramienta: str
    argumentos: dict[str, Any]
    resultado: str

    @property
    def resumen(self) -> str:
        return self.resultado[:400] + ("…" if len(self.resultado) > 400 else "")


@dataclass
class Respuesta:
    texto: str
    trazas: list[Traza] = field(default_factory=list)
    fuentes: list[str] = field(default_factory=list)
    modo_demo: bool = False
    error: str | None = None


class AgenteSoporte:
    def __init__(self, config: Config | None = None, buscador: Buscador | None = None) -> None:
        self.config = config or CONFIG
        self.buscador = buscador or Buscador()
        self.herramientas = Herramientas(self.buscador)
        self._cliente = None

        if not self.config.modo_demo:
            from openai import OpenAI

            self._cliente = OpenAI(
                api_key=self.config.api_key, base_url=self.config.base_url
            )

    @property
    def modo_demo(self) -> bool:
        return self._cliente is None

    # ------------------------------------------------------------------
    def responder(
        self, pregunta: str, historial: list[dict[str, str]] | None = None
    ) -> Respuesta:
        pregunta = (pregunta or "").strip()
        if not pregunta:
            return Respuesta(texto="Contame qué necesitás saber sobre Brokitech Turnos.")

        if self.modo_demo:
            return self._responder_demo(pregunta)

        mensajes: list[dict[str, Any]] = [{"role": "system", "content": INSTRUCCIONES}]
        # Se conservan los últimos turnos para que el agente entienda repreguntas.
        for turno in (historial or [])[-6:]:
            mensajes.append({"role": turno["role"], "content": turno["content"]})
        mensajes.append({"role": "user", "content": pregunta})

        trazas: list[Traza] = []

        for _ in range(self.config.max_iteraciones):
            try:
                completion = self._cliente.chat.completions.create(
                    model=self.config.modelo,
                    messages=mensajes,
                    tools=ESQUEMAS_HERRAMIENTAS,
                    tool_choice="auto",
                    temperature=self.config.temperatura,
                )
            except Exception as exc:  # noqa: BLE001 - se degrada a modo demo
                degradada = self._responder_demo(pregunta)
                degradada.error = f"Falló la llamada al modelo ({exc}). Se respondió con extractos."
                degradada.trazas = trazas + degradada.trazas
                return degradada

            mensaje = completion.choices[0].message
            llamadas = mensaje.tool_calls or []

            if not llamadas:
                texto = (mensaje.content or "").strip()
                return Respuesta(
                    texto=texto or "No pude generar una respuesta. Probá reformular la pregunta.",
                    trazas=trazas,
                    fuentes=self._extraer_fuentes(texto, trazas),
                )

            mensajes.append(
                {
                    "role": "assistant",
                    "content": mensaje.content or "",
                    "tool_calls": [
                        {
                            "id": ll.id,
                            "type": "function",
                            "function": {
                                "name": ll.function.name,
                                "arguments": ll.function.arguments,
                            },
                        }
                        for ll in llamadas
                    ],
                }
            )

            for llamada in llamadas:
                try:
                    argumentos = json.loads(llamada.function.arguments or "{}")
                except json.JSONDecodeError:
                    argumentos = {}
                resultado = self.herramientas.ejecutar(llamada.function.name, argumentos)
                trazas.append(Traza(llamada.function.name, argumentos, resultado))
                mensajes.append(
                    {
                        "role": "tool",
                        "tool_call_id": llamada.id,
                        "content": resultado,
                    }
                )

        return Respuesta(
            texto=(
                "Consulté la documentación varias veces y no llegué a una respuesta "
                "concluyente. Te conviene escribirle a soporte@brokitech.com."
            ),
            trazas=trazas,
            error="Se alcanzó el máximo de iteraciones.",
        )

    # ------------------------------------------------------------------
    def _responder_demo(self, pregunta: str) -> Respuesta:
        """Sin clave de API: se devuelven los extractos recuperados, sin redacción."""
        resultados = self.buscador.buscar(pregunta, top_k=3)
        traza = Traza(
            "buscar_en_documentacion",
            {"consulta": pregunta, "top_k": 3},
            self.herramientas.buscar_en_documentacion(pregunta, 3),
        )
        if not resultados:
            return Respuesta(
                texto=(
                    "**Modo demo (sin clave de API).**\n\n"
                    "No encontré nada sobre eso en la documentación. Probá con otras "
                    "palabras o escribí a soporte@brokitech.com."
                ),
                trazas=[traza],
                modo_demo=True,
            )

        bloques = [
            "**Modo demo (sin clave de API).** Extractos textuales de la documentación, "
            "sin redacción del modelo:\n"
        ]
        for i, r in enumerate(resultados, start=1):
            bloques.append(f"**{i}. {r.fragmento.cita}**\n\n> {r.fragmento.texto}\n")
        return Respuesta(
            texto="\n".join(bloques),
            trazas=[traza],
            fuentes=[r.fragmento.cita for r in resultados],
            modo_demo=True,
        )

    # ------------------------------------------------------------------
    @staticmethod
    def _extraer_fuentes(texto: str, trazas: list[Traza]) -> list[str]:
        """Fuentes citadas en la respuesta; si no hay, las que devolvieron las herramientas."""
        citadas = re.findall(r"Fuente[s]?:\s*(.+)", texto)
        if citadas:
            partes = [p.strip(" .;") for linea in citadas for p in linea.split(";")]
            return [p for p in dict.fromkeys(partes) if p]

        vistas: list[str] = []
        for traza in trazas:
            try:
                datos = json.loads(traza.resultado)
            except json.JSONDecodeError:
                continue
            for fragmento in datos.get("fragmentos", []):
                fuente = fragmento.get("fuente")
                if fuente and fuente not in vistas:
                    vistas.append(fuente)
        return vistas
