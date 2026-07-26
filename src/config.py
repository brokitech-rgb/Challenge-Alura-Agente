"""Configuración central del agente, leída de variables de entorno.

El agente habla con el modelo a través del SDK de OpenAI, así que sirve
cualquier proveedor con API compatible. Cambiar de uno a otro es cuestión de
variables de entorno: no hay nada específico de un proveedor en el resto del
código.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

RAIZ = Path(__file__).resolve().parent.parent
DIR_DOCS = RAIZ / "docs"
DIR_PDF = DIR_DOCS / "pdf"
DIR_DATA = RAIZ / "data"
CSV_PLANES = DIR_DATA / "planes.csv"


@dataclass(frozen=True)
class Proveedor:
    nombre: str
    variable_clave: str
    base_url: str
    modelo: str


# El orden importa: sin LLM_PROVIDER explícito se toma el primero que tenga
# clave cargada.
PROVEEDORES = (
    Proveedor("groq", "GROQ_API_KEY", "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile"),
    Proveedor("deepseek", "DEEPSEEK_API_KEY", "https://api.deepseek.com", "deepseek-chat"),
    Proveedor("openai", "OPENAI_API_KEY", "https://api.openai.com/v1", "gpt-4o-mini"),
)


def _int_env(clave: str, por_defecto: int) -> int:
    try:
        return int(os.getenv(clave, por_defecto))
    except (TypeError, ValueError):
        return por_defecto


def _float_env(clave: str, por_defecto: float) -> float:
    try:
        return float(os.getenv(clave, por_defecto))
    except (TypeError, ValueError):
        return por_defecto


def _detectar_proveedor() -> tuple[Proveedor | None, str]:
    """Elige el proveedor según LLM_PROVIDER, o el primero con clave cargada."""
    elegido = os.getenv("LLM_PROVIDER", "").strip().lower()
    if elegido:
        for proveedor in PROVEEDORES:
            if proveedor.nombre == elegido:
                return proveedor, os.getenv(proveedor.variable_clave, "").strip()
    for proveedor in PROVEEDORES:
        clave = os.getenv(proveedor.variable_clave, "").strip()
        if clave:
            return proveedor, clave
    return None, ""


@dataclass(frozen=True)
class Config:
    proveedor: Proveedor | None = field(default=None)
    api_key: str = field(default="")
    base_url: str = field(default="")
    modelo: str = field(default="")

    top_k: int = field(default_factory=lambda: _int_env("AGENTE_TOP_K", 5))
    temperatura: float = field(default_factory=lambda: _float_env("AGENTE_TEMPERATURA", 0.2))
    max_iteraciones: int = field(default_factory=lambda: _int_env("AGENTE_MAX_ITERACIONES", 6))

    @classmethod
    def desde_entorno(cls) -> "Config":
        proveedor, clave = _detectar_proveedor()
        if proveedor is None:
            return cls()
        # LLM_BASE_URL y LLM_MODEL permiten pisar los valores por defecto sin
        # tocar el código (por ejemplo, para apuntar a un modelo distinto del
        # mismo proveedor).
        return cls(
            proveedor=proveedor,
            api_key=clave,
            base_url=os.getenv("LLM_BASE_URL", "").strip() or proveedor.base_url,
            modelo=os.getenv("LLM_MODEL", "").strip() or proveedor.modelo,
        )

    @property
    def modo_demo(self) -> bool:
        """Sin clave de API el agente responde solo con extractos recuperados."""
        return not self.api_key

    @property
    def descripcion(self) -> str:
        if self.modo_demo:
            return "modo demo (sin clave de API)"
        return f"{self.proveedor.nombre} · {self.modelo}"


CONFIG = Config.desde_entorno()

# Nombre legible de cada documento, para citar la fuente en las respuestas.
NOMBRES_DOCUMENTOS = {
    "01-base-conocimiento": "Base de Conocimiento del Producto",
    "02-faq-soporte": "FAQ de Soporte",
    "03-politica-privacidad": "Política de Privacidad",
    "04-planes-precios": "Planes y Precios",
    "05-terminos-uso": "Términos y Condiciones de Uso",
}


def nombre_legible(slug: str) -> str:
    return NOMBRES_DOCUMENTOS.get(slug, slug.replace("-", " ").title())
