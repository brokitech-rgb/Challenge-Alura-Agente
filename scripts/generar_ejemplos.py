"""Corre una batería de preguntas contra el agente y guarda las respuestas.

Sirve para dos cosas: dejar en el repo evidencia reproducible de lo que el
agente contesta, y detectar regresiones cuando se toca el prompt o el corpus.

    python scripts/generar_ejemplos.py

Escribe docs/EJEMPLOS.md con la salida textual, sin editar.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import AgenteSoporte  # noqa: E402
from src.config import CONFIG, RAIZ  # noqa: E402
from src.ingest import cargar_corpus  # noqa: E402
from src.retriever import Buscador  # noqa: E402

PREGUNTAS = [
    # Respuesta directa de un solo documento
    "¿Brokitech se queda con una parte de la seña que cobro?",
    # Obliga a cruzar CSV + PDF y a hacer una recomendación
    "Somos 8 profesionales y hacemos unos 1200 turnos por mes. ¿Qué plan me conviene y cuánto pagaría?",
    # Matiz importante: la respuesta correcta es "no directamente"
    "¿Puedo usar mi número actual de WhatsApp Business?",
    # Dato puntual de la política de privacidad
    "Si cancelo la suscripción, ¿cuánto tiempo tengo para exportar mis datos?",
    # Comparación entre planes
    "¿Qué diferencia hay entre el plan Profesional y el Negocio?",
    # Pregunta sensible sobre IA y datos
    "¿Usan las conversaciones de mis clientes para entrenar modelos de IA?",
    # Troubleshooting con pasos
    "El bot dejó de responderle a mis clientes, ¿qué reviso?",
    # Funcionalidad que NO existe: el agente no debe inventarla
    "¿Se integra con AFIP para emitir factura electrónica automática?",
    # Fuera de dominio: debe reconocer que no sabe
    "¿Cuál es la mejor receta de milanesas a la napolitana?",
    # Debe derivar a soporte humano
    "Me cobraron dos veces el mes pasado y necesito que alguien lo revise.",
]


def main() -> int:
    try:
        corpus = cargar_corpus()
    except FileNotFoundError as exc:
        print(exc)
        return 1

    agente = AgenteSoporte(buscador=Buscador(corpus))
    modo = "MODO DEMO (sin clave de API)" if agente.modo_demo else f"modelo `{CONFIG.modelo}`"
    print(f"Generando ejemplos con {modo}…\n")

    lineas = [
        "# Ejemplos de preguntas y respuestas",
        "",
        "> Archivo generado por `python scripts/generar_ejemplos.py`. ",
        "> Las respuestas son la salida textual del agente, sin editar.",
        "",
        f"- **Generado:** {dt.datetime.now():%d/%m/%Y %H:%M}",
        f"- **Motor:** {modo}",
        f"- **Fragmentos indexados:** {len(corpus)}",
        "",
        "---",
        "",
    ]

    for i, pregunta in enumerate(PREGUNTAS, start=1):
        print(f"[{i}/{len(PREGUNTAS)}] {pregunta}")
        respuesta = agente.responder(pregunta)

        lineas += [f"## {i}. {pregunta}", "", respuesta.texto, ""]

        if respuesta.trazas:
            lineas += ["**Herramientas invocadas:**", ""]
            lineas += [
                f"{n}. `{t.herramienta}({t.argumentos})`"
                for n, t in enumerate(respuesta.trazas, start=1)
            ]
            lineas.append("")
        if respuesta.error:
            lineas += [f"> Aviso: {respuesta.error}", ""]
        lineas += ["---", ""]

    destino = RAIZ / "docs" / "EJEMPLOS.md"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    print(f"\nEscrito: {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
