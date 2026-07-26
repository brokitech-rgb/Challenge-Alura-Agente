"""Interfaz web del agente de soporte de Brokitech Turnos.

Ejecutar con:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from src.agent import AgenteSoporte
from src.config import CONFIG
from src.ingest import cargar_corpus, resumen_corpus
from src.retriever import Buscador

st.set_page_config(
    page_title="Agente de Soporte — Brokitech Turnos",
    page_icon="📅",
    layout="centered",
)

PREGUNTAS_SUGERIDAS = [
    "¿Brokitech se queda con una parte de la seña?",
    "Somos 8 profesionales y hacemos 1200 turnos por mes, ¿cuánto me sale?",
    "¿Puedo usar mi número actual de WhatsApp Business?",
    "Si cancelo, ¿cuánto tiempo tengo para exportar mis datos?",
    "¿Qué diferencia hay entre el plan Profesional y el Negocio?",
    "¿Usan mis conversaciones para entrenar modelos de IA?",
    "El bot dejó de responderle a mis clientes, ¿qué reviso?",
    "¿Emiten factura A? ¿Hay descuento por pago anual?",
]


@st.cache_resource(show_spinner="Leyendo los PDF e indexando la documentación…")
def preparar_agente() -> tuple[AgenteSoporte, list]:
    corpus = cargar_corpus()
    return AgenteSoporte(buscador=Buscador(corpus)), corpus


def encolar(pregunta: str) -> None:
    st.session_state.pendiente = pregunta


# ---------------------------------------------------------------- estado
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "pendiente" not in st.session_state:
    st.session_state.pendiente = None

try:
    agente, corpus = preparar_agente()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.code("python scripts/build_pdfs.py", language="bash")
    st.stop()

# ---------------------------------------------------------------- barra lateral
with st.sidebar:
    st.subheader("Brokitech Turnos")
    st.caption("Agente de soporte sobre documentación oficial")

    if agente.modo_demo:
        st.warning(
            "**Modo demo** — no hay clave de API cargada. El agente devuelve "
            "extractos textuales de los PDF, sin redacción del modelo.",
            icon="⚠️",
        )
    else:
        st.success(f"Modelo activo: `{CONFIG.descripcion}`", icon="✅")

    st.divider()
    st.markdown("**Base de conocimiento indexada**")
    st.dataframe(
        resumen_corpus(corpus),
        hide_index=True,
        width="stretch",
    )
    st.caption(f"{len(corpus)} fragmentos · 5 PDF + 1 CSV")

    st.divider()
    st.markdown("**Herramientas del agente**")
    st.markdown(
        "- `buscar_en_documentacion` — RAG sobre los PDF\n"
        "- `consultar_planes` — lectura del CSV\n"
        "- `calcular_presupuesto` — cálculo determinístico\n"
        "- `escalar_a_humano` — deriva a soporte"
    )

    st.divider()
    if st.button("Limpiar conversación", width="stretch"):
        st.session_state.mensajes = []
        st.rerun()


def escapar_dolares(texto: str) -> str:
    """Escapa los `$` para que Streamlit no los tome como delimitadores LaTeX.

    Toda la documentación cotiza en pesos, así que una respuesta típica trae
    varios `$`. Streamlit los interpreta de a pares y renderiza lo que queda en
    el medio como fórmula matemática: "$39.900 base y $14.700 extra" se
    convertía en una cursiva serif sin espacios. Acá no hay LaTeX legítimo que
    preservar, así que se escapan todos.
    """
    return texto.replace("$", r"\$")


def render_trazas(trazas: list[dict]) -> None:
    if not trazas:
        return
    with st.expander(f"Razonamiento — {len(trazas)} llamada(s) a herramientas"):
        for i, traza in enumerate(trazas, start=1):
            st.markdown(f"**{i}. `{traza['herramienta']}`**")
            st.json(traza["argumentos"], expanded=False)
            st.code(traza["resumen"], language="json")


# ---------------------------------------------------------------- cabecera
st.title("📅 Agente de Soporte")
st.caption(
    "Respondo sobre la documentación oficial de Brokitech Turnos: base de "
    "conocimiento, FAQ, política de privacidad, planes y precios, y términos de uso."
)

# La entrada se resuelve antes de dibujar nada: así las sugerencias no quedan
# visibles junto a la primera respuesta. `st.chat_input` se ancla al pie de la
# página sin importar en qué orden se lo invoque.
entrada = st.chat_input("Escribí tu consulta…")
pregunta = entrada or st.session_state.pendiente
st.session_state.pendiente = None

if not st.session_state.mensajes and not pregunta:
    st.markdown("**Probá con alguna de estas:**")
    columnas = st.columns(2)
    for i, sugerencia in enumerate(PREGUNTAS_SUGERIDAS):
        columnas[i % 2].button(
            sugerencia,
            key=f"sug_{i}",
            width="stretch",
            on_click=encolar,
            args=(sugerencia,),
        )

# ---------------------------------------------------------------- historial
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(escapar_dolares(mensaje["content"]))
        render_trazas(mensaje.get("trazas") or [])

# ---------------------------------------------------------------- turno nuevo
# El turno en curso se dibuja acá mismo y NO se hace rerun: el bucle de arriba
# ya se encarga de re-dibujarlo en la proxima interaccion. Renderizar y ademas
# rerunear duplicaba cada mensaje en el arbol de la pagina.
if pregunta:
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(escapar_dolares(pregunta))

    with st.chat_message("assistant"):
        with st.spinner("Consultando la documentación…"):
            historial = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.mensajes[:-1]
            ]
            respuesta = agente.responder(pregunta, historial)

        st.markdown(escapar_dolares(respuesta.texto))
        if respuesta.error:
            st.warning(respuesta.error, icon="⚠️")

        trazas = [
            {"herramienta": t.herramienta, "argumentos": t.argumentos, "resumen": t.resumen}
            for t in respuesta.trazas
        ]
        render_trazas(trazas)

    st.session_state.mensajes.append(
        {"role": "assistant", "content": respuesta.texto, "trazas": trazas}
    )
