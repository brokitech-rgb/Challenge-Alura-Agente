"""Pruebas de la interfaz, ejecutando app.py con el runner de Streamlit.

Corren en modo demo (sin clave de API) a propósito: lo que se verifica acá es
el cableado de la UI, no la calidad de la redacción del modelo. El agente con
LLM se prueba por separado.

    python -m pytest tests/test_app.py -q
"""

from __future__ import annotations

import pytest

from src.config import DIR_PDF

streamlit_testing = pytest.importorskip("streamlit.testing.v1")
AppTest = streamlit_testing.AppTest


@pytest.fixture
def app(monkeypatch):
    """Levanta app.py forzando el modo demo (sin clave de API)."""
    if not any(DIR_PDF.glob("*.pdf")):
        pytest.skip("Faltan los PDF. Ejecutá: python scripts/build_pdfs.py")

    import dataclasses

    import streamlit as st

    import src.agent as agent
    import src.config as config
    import src.tools as tools

    # load_dotenv() ya corrió al importar src.config, así que limpiar el entorno
    # no alcanza. Config es un dataclass congelado: se reemplaza el objeto, y en
    # cada módulo que lo importó por nombre.
    demo = dataclasses.replace(config.CONFIG, api_key="", proveedor=None)
    for modulo in (config, agent, tools):
        monkeypatch.setattr(modulo, "CONFIG", demo)

    # El agente se construye con @st.cache_resource: sin limpiar el caché, la
    # instancia de un test anterior sobreviviría con la config vieja.
    st.cache_resource.clear()

    at = AppTest.from_file("app.py", default_timeout=120)
    at.run()
    assert not at.exception, at.exception
    assert at.session_state is not None
    return at


def test_la_app_arranca_sin_excepciones(app):
    assert app.title[0].value.endswith("Agente de Soporte")


def test_muestra_las_sugerencias_al_inicio(app):
    etiquetas = [b.label for b in app.button if b.label]
    assert any("seña" in (e or "") for e in etiquetas)
    assert len([e for e in etiquetas if e != "Limpiar conversación"]) == 8


def test_la_barra_lateral_reporta_el_corpus(app):
    assert app.dataframe, "falta la tabla de documentos indexados"
    filas = app.dataframe[0].value
    assert len(filas) == 6  # 5 PDF + el CSV


def test_una_pregunta_produce_exactamente_un_par_de_mensajes(app):
    """Regresión: renderizar imperativamente y ademas hacer st.rerun()
    duplicaba cada mensaje en el arbol de la pagina."""
    app.chat_input[0].set_value("¿Brokitech cobra comisión sobre las señas?").run()

    assert not app.exception, app.exception
    roles = [m.name for m in app.chat_message]
    assert roles == ["user", "assistant"], f"mensajes duplicados o faltantes: {roles}"


def test_el_click_en_una_sugerencia_dispara_la_consulta(app):
    objetivo = [b for b in app.button if b.label and "WhatsApp Business" in b.label]
    assert objetivo, "no se encontró el botón de sugerencia"

    objetivo[0].click().run()

    assert not app.exception, app.exception
    roles = [m.name for m in app.chat_message]
    assert roles == ["user", "assistant"], f"mensajes duplicados o faltantes: {roles}"

    respuesta = " ".join(str(e.value) for e in app.chat_message[1].markdown)
    assert "WhatsApp Business" in respuesta


def test_las_sugerencias_desaparecen_tras_la_primera_consulta(app):
    app.chat_input[0].set_value("¿Hay descuento por pago anual?").run()

    etiquetas = [b.label for b in app.button if b.label]
    assert etiquetas == ["Limpiar conversación"]


def test_una_consulta_fuera_de_dominio_no_rompe_la_ui(app):
    app.chat_input[0].set_value("receta de milanesas a la napolitana").run()

    assert not app.exception, app.exception
    respuesta = " ".join(str(e.value) for e in app.chat_message[1].markdown)
    assert "No encontré" in respuesta or "no está" in respuesta.lower()
