"""Pruebas del pipeline de lectura, indexado y herramientas.

    python -m pytest -q
"""

from __future__ import annotations

import json

import pytest

from src.config import CSV_PLANES, DIR_PDF
from src.ingest import cargar_corpus, leer_pdf
from src.retriever import Buscador, normalizar
from src.tools import Herramientas


@pytest.fixture(scope="module")
def corpus():
    if not any(DIR_PDF.glob("*.pdf")):
        pytest.skip("Faltan los PDF. Ejecutá: python scripts/build_pdfs.py")
    return cargar_corpus()


@pytest.fixture(scope="module")
def buscador(corpus):
    return Buscador(corpus)


@pytest.fixture(scope="module")
def herramientas(buscador):
    return Herramientas(buscador)


# --- lectura de documentos ------------------------------------------------


def test_se_generaron_los_cinco_pdf():
    assert len(list(DIR_PDF.glob("*.pdf"))) == 5


def test_el_csv_de_planes_existe():
    assert CSV_PLANES.exists()


def test_el_corpus_cubre_todos_los_documentos(corpus):
    documentos = {f.documento for f in corpus}
    assert len(documentos) == 6  # 5 PDF + el CSV
    assert "FAQ de Soporte" in documentos
    assert "Tabla comparativa de planes (CSV)" in documentos


def test_la_extraccion_conserva_los_acentos(corpus):
    """Regresión: con fuentes base del PDF las tildes volvían como U+FFFD."""
    texto = " ".join(f.texto for f in corpus)
    assert "�" not in texto
    assert "seña" in texto
    assert "Política" in texto or "política" in texto


def test_cada_fragmento_tiene_procedencia(corpus):
    for fragmento in corpus:
        assert fragmento.documento
        assert fragmento.pagina >= 1
        assert fragmento.texto.strip()
        assert "pág." in fragmento.cita


def test_se_detectan_las_secciones(corpus):
    con_seccion = [f for f in corpus if f.seccion]
    assert len(con_seccion) / len(corpus) > 0.8


def test_se_descartan_encabezado_y_pie(corpus):
    assert not any("Documentacion oficial" in f.texto for f in corpus)


def test_leer_pdf_devuelve_fragmentos():
    fragmentos = leer_pdf(DIR_PDF / "02-faq-soporte.pdf")
    assert fragmentos
    assert all(f.documento == "FAQ de Soporte" for f in fragmentos)


# --- buscador -------------------------------------------------------------


def test_normalizar_saca_acentos():
    assert normalizar("Política de Señas") == "politica de senas"


@pytest.mark.parametrize(
    "consulta, esperado",
    [
        ("comisión sobre las señas", "no cobra comisión"),
        ("número de whatsapp business", "WhatsApp Business"),
        ("exportar datos después de cancelar", "60 días"),
        ("entrenan modelos con mis conversaciones", "entrenar"),
    ],
)
def test_la_busqueda_encuentra_lo_relevante(buscador, consulta, esperado):
    resultados = buscador.buscar(consulta, top_k=5)
    assert resultados, f"sin resultados para: {consulta}"
    assert any(esperado.lower() in r.fragmento.texto.lower() for r in resultados)


def test_la_busqueda_tolera_falta_de_acentos(buscador):
    con = buscador.buscar("política de privacidad", top_k=3)
    sin = buscador.buscar("politica de privacidad", top_k=3)
    assert [r.fragmento.cita for r in con] == [r.fragmento.cita for r in sin]


def test_consulta_vacia_no_devuelve_nada(buscador):
    assert buscador.buscar("") == []
    assert buscador.buscar("   ") == []


def test_los_puntajes_vienen_ordenados(buscador):
    puntajes = [r.score for r in buscador.buscar("planes y precios", top_k=5)]
    assert puntajes == sorted(puntajes, reverse=True)


@pytest.mark.parametrize(
    "consulta",
    [
        "receta de milanesas a la napolitana",
        "quien gano el mundial de 1986",
        "como cambio el aceite del auto",
    ],
)
def test_consulta_sin_relacion_no_trae_ruido(buscador, consulta):
    """Fuera de dominio no se devuelve nada, aunque los n-gramas de caracteres
    den una similitud residual: el agente prefiere decir que no sabe."""
    assert buscador.buscar(consulta, top_k=5) == []


@pytest.mark.parametrize(
    "consulta",
    ["wathsapp bussines numero", "cuanto sale el plan profesionl", "politca de privacidad"],
)
def test_la_busqueda_tolera_errores_de_tipeo(buscador, consulta):
    assert buscador.buscar(consulta, top_k=3), f"sin resultados para: {consulta}"


# --- herramientas ---------------------------------------------------------


def test_consultar_planes_trae_los_cuatro(herramientas):
    datos = json.loads(herramientas.consultar_planes())
    assert [p["plan"] for p in datos["planes"]] == [
        "Inicial",
        "Profesional",
        "Negocio",
        "Enterprise",
    ]


def test_consultar_planes_por_nombre(herramientas):
    datos = json.loads(herramientas.consultar_planes("profesional"))
    assert datos["plan"]["precio_mensual_ars"] == "39900"


def test_consultar_plan_inexistente(herramientas):
    assert "error" in json.loads(herramientas.consultar_planes("Platino"))


def test_presupuesto_simple(herramientas):
    datos = json.loads(herramientas.calcular_presupuesto("Inicial"))
    assert datos["total_mensual"] == "$19.900"
    assert datos["turnos_excedentes"] == 0


def test_presupuesto_anual_aplica_descuento(herramientas):
    datos = json.loads(herramientas.calcular_presupuesto("Negocio", ciclo="anual", meses=12))
    assert datos["abono_base_mensual"] == "$63.920"
    assert datos["total_periodo"] == "$767.040"


def test_presupuesto_suma_excedentes(herramientas):
    datos = json.loads(
        herramientas.calcular_presupuesto(
            "Profesional", ciclo="mensual", meses=1, profesionales=8, turnos_por_mes=1200
        )
    )
    # 39.900 base + 3 profesionales x 4.900 + 400 turnos x 95
    assert datos["profesionales_adicionales"] == 3
    assert datos["turnos_excedentes"] == 400
    assert datos["total_mensual"] == "$92.600"


def test_plan_negocio_no_tiene_excedente_de_turnos(herramientas):
    datos = json.loads(herramientas.calcular_presupuesto("Negocio", turnos_por_mes=99999))
    assert datos["turnos_excedentes"] == 0
    assert datos["total_mensual"] == "$79.900"


def test_plan_inicial_rechaza_profesionales_adicionales(herramientas):
    """El CSV marca el costo como 'no disponible': debe avisar, no romper."""
    datos = json.loads(herramientas.calcular_presupuesto("Inicial", profesionales=4))
    assert "error" in datos
    assert "no admite adicionales" in datos["error"]


def test_enterprise_se_deriva_a_ventas(herramientas):
    datos = json.loads(herramientas.calcular_presupuesto("Enterprise"))
    assert "a medida" in datos["error"]


def test_escalar_genera_ticket(herramientas):
    datos = json.loads(herramientas.escalar_a_humano("facturación", "Cobro duplicado"))
    assert datos["ticket"].startswith("BTK-")
    assert datos["estado"] == "registrado"


def test_herramienta_desconocida_no_rompe(herramientas):
    assert "error" in json.loads(herramientas.ejecutar("volar", {}))


def test_argumentos_invalidos_no_rompen(herramientas):
    assert "error" in json.loads(herramientas.ejecutar("consultar_planes", {"x": 1}))
