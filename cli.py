"""Versión de terminal del agente, útil para probar sin levantar Streamlit.

    python cli.py                       # modo conversacional
    python cli.py "¿hay descuento anual?"   # una sola pregunta
"""

from __future__ import annotations

import sys

from src.agent import AgenteSoporte
from src.ingest import cargar_corpus
from src.retriever import Buscador


def imprimir(respuesta) -> None:
    print()
    print(respuesta.texto)
    if respuesta.trazas:
        print("\n" + "-" * 60)
        print("Herramientas usadas:")
        for traza in respuesta.trazas:
            print(f"  · {traza.herramienta}({traza.argumentos})")
    if respuesta.error:
        print(f"\n[aviso] {respuesta.error}")
    print()


def main() -> int:
    try:
        corpus = cargar_corpus()
    except FileNotFoundError as exc:
        print(exc)
        return 1

    agente = AgenteSoporte(buscador=Buscador(corpus))
    print(f"Agente de Soporte — Brokitech Turnos  ({len(corpus)} fragmentos indexados)")
    if agente.modo_demo:
        print("MODO DEMO: sin clave de API, se devuelven extractos sin redactar.")

    if len(sys.argv) > 1:
        imprimir(agente.responder(" ".join(sys.argv[1:])))
        return 0

    print("Escribí tu consulta. 'salir' para terminar.\n")
    historial: list[dict[str, str]] = []
    while True:
        try:
            pregunta = input("vos> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if pregunta.lower() in {"salir", "exit", "quit"}:
            return 0
        if not pregunta:
            continue
        respuesta = agente.responder(pregunta, historial)
        imprimir(respuesta)
        historial += [
            {"role": "user", "content": pregunta},
            {"role": "assistant", "content": respuesta.texto},
        ]


if __name__ == "__main__":
    raise SystemExit(main())
