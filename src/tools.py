"""Herramientas que el agente puede invocar.

El agente no se limita a recuperar texto: decide cuál de estas funciones llamar
según lo que le preguntan. Las tres primeras leen datos reales (PDF y CSV) y la
última cierra el circuito cuando la documentación no alcanza.

Cada herramienta expone su esquema JSON en ESQUEMAS_HERRAMIENTAS, que es lo que
se le manda al modelo en el parámetro `tools` de la API.
"""

from __future__ import annotations

import json
from typing import Any, Callable

import pandas as pd

from .config import CSV_PLANES
from .retriever import Buscador

# Planes cuyos valores no son numéricos y por lo tanto no se pueden presupuestar.
PLANES_A_MEDIDA = {"enterprise"}


def _cargar_planes() -> pd.DataFrame:
    df = pd.read_csv(CSV_PLANES)
    df["_clave"] = df["plan"].str.strip().str.lower()
    return df


def _fila_plan(nombre: str) -> pd.Series | None:
    df = _cargar_planes()
    clave = (nombre or "").strip().lower()
    coincidencias = df[df["_clave"] == clave]
    if coincidencias.empty:
        # Coincidencia parcial: "plan negocio" -> "negocio"
        coincidencias = df[df["_clave"].apply(lambda c: c in clave or clave in c)]
    return None if coincidencias.empty else coincidencias.iloc[0]


def _a_numero(valor: Any) -> float | None:
    """Convierte una celda del CSV a número; None si es texto ('a medida')."""
    try:
        return float(str(valor).strip())
    except (TypeError, ValueError):
        return None


def _pesos(monto: float) -> str:
    return f"${monto:,.0f}".replace(",", ".")


class Herramientas:
    """Implementación de las herramientas, ligada a un índice ya construido."""

    def __init__(self, buscador: Buscador) -> None:
        self.buscador = buscador
        self.escalamientos: list[dict[str, str]] = []

    # --- 1. Búsqueda en los PDF -------------------------------------------
    def buscar_en_documentacion(self, consulta: str, top_k: int = 5) -> str:
        resultados = self.buscador.buscar(consulta, top_k=max(1, min(int(top_k), 10)))
        if not resultados:
            return json.dumps(
                {
                    "encontrado": False,
                    "mensaje": "No hay información sobre eso en la documentación.",
                },
                ensure_ascii=False,
            )
        return json.dumps(
            {
                "encontrado": True,
                "fragmentos": [
                    {
                        "fuente": r.fragmento.cita,
                        "texto": r.fragmento.texto,
                        "relevancia": round(r.score, 3),
                    }
                    for r in resultados
                ],
            },
            ensure_ascii=False,
        )

    # --- 2. Consulta estructurada al CSV ----------------------------------
    def consultar_planes(self, plan: str | None = None) -> str:
        df = _cargar_planes().drop(columns=["_clave"])
        if plan:
            fila = _fila_plan(plan)
            if fila is None:
                return json.dumps(
                    {
                        "error": f"No existe el plan '{plan}'.",
                        "planes_disponibles": df["plan"].tolist(),
                    },
                    ensure_ascii=False,
                )
            datos = fila.drop(labels=["_clave"]).to_dict()
            return json.dumps({"plan": datos}, ensure_ascii=False)
        return json.dumps({"planes": df.to_dict(orient="records")}, ensure_ascii=False)

    # --- 3. Presupuesto determinístico ------------------------------------
    def calcular_presupuesto(
        self,
        plan: str,
        ciclo: str = "mensual",
        meses: int = 1,
        profesionales: int = 1,
        turnos_por_mes: int = 0,
    ) -> str:
        fila = _fila_plan(plan)
        if fila is None:
            return json.dumps({"error": f"No existe el plan '{plan}'."}, ensure_ascii=False)

        if fila["_clave"] in PLANES_A_MEDIDA:
            return json.dumps(
                {
                    "error": "El plan Enterprise se cotiza a medida.",
                    "accion_sugerida": "Derivar a ventas@brokitech.com",
                },
                ensure_ascii=False,
            )

        ciclo = (ciclo or "mensual").strip().lower()
        if ciclo not in {"mensual", "anual"}:
            ciclo = "mensual"
        meses = max(1, int(meses))
        profesionales = max(1, int(profesionales))
        turnos_por_mes = max(0, int(turnos_por_mes))

        columna = "precio_anual_por_mes_ars" if ciclo == "anual" else "precio_mensual_ars"
        base = float(fila[columna])

        # Profesionales por encima de los incluidos en el plan.
        incluidos = int(fila["profesionales_incluidos"])
        extra_profesionales = max(0, profesionales - incluidos)
        costo_prof = _a_numero(fila["costo_profesional_adicional_ars"])
        if extra_profesionales and costo_prof is None:
            return json.dumps(
                {
                    "error": (
                        f"El plan {fila['plan']} incluye {incluidos} profesional(es) y no "
                        f"admite adicionales, pero se pidieron {profesionales}."
                    ),
                    "accion_sugerida": (
                        "Recalcular con el plan inmediatamente superior que cubra esa "
                        "cantidad de profesionales."
                    ),
                },
                ensure_ascii=False,
            )
        cargo_profesionales = extra_profesionales * (costo_prof or 0.0)

        # Turnos por encima del cupo. El plan Negocio no tiene tope.
        cupo_turnos = str(fila["turnos_por_mes"]).strip().lower()
        if cupo_turnos.isdigit():
            extra_turnos = max(0, turnos_por_mes - int(cupo_turnos))
            cargo_turnos = extra_turnos * (_a_numero(fila["costo_turno_excedente_ars"]) or 0.0)
        else:
            extra_turnos, cargo_turnos = 0, 0.0

        mensual = base + cargo_profesionales + cargo_turnos
        total = mensual * meses

        detalle = {
            "plan": fila["plan"],
            "ciclo": ciclo,
            "meses": meses,
            "abono_base_mensual": _pesos(base),
            "profesionales_solicitados": profesionales,
            "profesionales_incluidos": incluidos,
            "profesionales_adicionales": extra_profesionales,
            "cargo_profesionales_adicionales": _pesos(cargo_profesionales),
            "turnos_declarados_por_mes": turnos_por_mes,
            "cupo_turnos_del_plan": fila["turnos_por_mes"],
            "turnos_excedentes": extra_turnos,
            "cargo_turnos_excedentes": _pesos(cargo_turnos),
            "total_mensual": _pesos(mensual),
            "total_periodo": _pesos(total),
            "nota": (
                "Precios en ARS con IVA incluido. Brokitech no cobra comisión sobre "
                "las señas; la comisión de Mercado Pago corre por fuera."
            ),
        }
        if ciclo == "anual":
            detalle["aclaracion_ciclo"] = (
                "El ciclo anual aplica 20% de descuento y se abona en un único pago "
                "por adelantado."
            )
        return json.dumps(detalle, ensure_ascii=False)

    # --- 4. Escalamiento a soporte humano ---------------------------------
    def escalar_a_humano(self, motivo: str, resumen: str) -> str:
        ticket = {
            "ticket": f"BTK-{len(self.escalamientos) + 1:04d}",
            "motivo": motivo,
            "resumen": resumen,
            "canal": "soporte@brokitech.com / WhatsApp +54 9 11 5555-0143",
            "estado": "registrado",
        }
        self.escalamientos.append(ticket)
        return json.dumps(ticket, ensure_ascii=False)

    # --- Despacho ----------------------------------------------------------
    @property
    def registro(self) -> dict[str, Callable[..., str]]:
        return {
            "buscar_en_documentacion": self.buscar_en_documentacion,
            "consultar_planes": self.consultar_planes,
            "calcular_presupuesto": self.calcular_presupuesto,
            "escalar_a_humano": self.escalar_a_humano,
        }

    def ejecutar(self, nombre: str, argumentos: dict[str, Any]) -> str:
        funcion = self.registro.get(nombre)
        if funcion is None:
            return json.dumps({"error": f"Herramienta desconocida: {nombre}"}, ensure_ascii=False)
        try:
            return funcion(**argumentos)
        except TypeError as exc:
            return json.dumps({"error": f"Argumentos inválidos: {exc}"}, ensure_ascii=False)
        except Exception as exc:  # noqa: BLE001 - el error vuelve al modelo, no rompe el chat
            return json.dumps({"error": f"Fallo al ejecutar {nombre}: {exc}"}, ensure_ascii=False)


ESQUEMAS_HERRAMIENTAS = [
    {
        "type": "function",
        "function": {
            "name": "buscar_en_documentacion",
            "description": (
                "Busca en los documentos oficiales de Brokitech Turnos (base de "
                "conocimiento, FAQ, política de privacidad, planes y precios, términos "
                "de uso). Es la herramienta principal: usala para cualquier pregunta "
                "sobre funcionamiento, políticas, límites, integraciones o soporte."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "consulta": {
                        "type": "string",
                        "description": "Términos de búsqueda en español. Sé específico.",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Cantidad de fragmentos a traer (1 a 10). Por defecto 5.",
                    },
                },
                "required": ["consulta"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_planes",
            "description": (
                "Devuelve los datos exactos de los planes desde la tabla CSV: precios, "
                "cupos, funcionalidades incluidas y costos de excedente. Usala siempre "
                "que la pregunta involucre comparar planes o citar un precio, en vez de "
                "confiar en el texto del PDF."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "plan": {
                        "type": "string",
                        "description": (
                            "Nombre del plan: Inicial, Profesional, Negocio o Enterprise. "
                            "Omitir para traer los cuatro."
                        ),
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_presupuesto",
            "description": (
                "Calcula el costo total de una suscripción incluyendo profesionales "
                "adicionales y turnos excedentes. Usala cuando el usuario describe su "
                "caso concreto ('somos 8 personas y hacemos 1200 turnos por mes')."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "plan": {"type": "string", "description": "Inicial, Profesional o Negocio."},
                    "ciclo": {
                        "type": "string",
                        "enum": ["mensual", "anual"],
                        "description": "Ciclo de facturación. Por defecto mensual.",
                    },
                    "meses": {"type": "integer", "description": "Cantidad de meses a proyectar."},
                    "profesionales": {
                        "type": "integer",
                        "description": "Cuántos profesionales usarán el sistema.",
                    },
                    "turnos_por_mes": {
                        "type": "integer",
                        "description": "Turnos mensuales estimados.",
                    },
                },
                "required": ["plan"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalar_a_humano",
            "description": (
                "Registra un ticket para soporte humano. Usala cuando la documentación "
                "no cubre la consulta, cuando el usuario pide hablar con una persona, o "
                "ante un reclamo de facturación o un incidente que requiere revisar la "
                "cuenta concreta."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "motivo": {
                        "type": "string",
                        "description": "Categoría breve: facturación, incidente técnico, comercial, otro.",
                    },
                    "resumen": {
                        "type": "string",
                        "description": "Resumen de lo que necesita el usuario, para el equipo de soporte.",
                    },
                },
                "required": ["motivo", "resumen"],
            },
        },
    },
]
