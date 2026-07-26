"""Configuración central del agente, leída de variables de entorno."""

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


@dataclass(frozen=True)
class Config:
    api_key: str = field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY", "").strip())
    base_url: str = field(
        default_factory=lambda: os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip()
    )
    modelo: str = field(default_factory=lambda: os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip())

    top_k: int = field(default_factory=lambda: _int_env("AGENTE_TOP_K", 5))
    temperatura: float = field(default_factory=lambda: _float_env("AGENTE_TEMPERATURA", 0.2))
    max_iteraciones: int = field(default_factory=lambda: _int_env("AGENTE_MAX_ITERACIONES", 6))

    @property
    def modo_demo(self) -> bool:
        """Sin clave de API el agente responde solo con extractos recuperados."""
        return not self.api_key


CONFIG = Config()

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
