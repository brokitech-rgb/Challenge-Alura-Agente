"""Lectura y troceado de los documentos fuente (PDF y CSV).

Este módulo es el que cumple el requisito del challenge de "leer y procesar el
documento utilizado como fuente de información": extrae el texto de cada PDF
página por página, reconstruye a qué sección pertenece cada línea y lo parte en
fragmentos indexables que conservan la referencia a documento, sección y página.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import pandas as pd
from pypdf import PdfReader

from .config import CSV_PLANES, DIR_PDF, nombre_legible

# Tamaño objetivo de cada fragmento. Suficiente para que una respuesta quepa
# entera, chico como para que el TF-IDF no se diluya.
TAM_FRAGMENTO = 1000
SOLAPE = 150

# Encabezado y pie que build_pdfs.py estampa en cada página: son ruido.
LINEAS_RUIDO = re.compile(r"^(Brokitech Turnos - Documentacion oficial|Pagina \d+)\s*$")

# Encabezados de sección tal como quedan tras extraer el texto del PDF:
#   "3. Cobro de señas"        "4.2 Ventana de 24 horas"       "B3. El bot no responde..."
PATRONES_SECCION = (
    re.compile(r"^\d+(?:\.\d+)*\.?\s+\S.{1,90}$"),
    re.compile(r"^[A-H]\d{1,2}\.\s+\S.{1,90}$"),
    re.compile(r"^[A-H]\.\s+\S.{1,60}$"),
)


@dataclass(frozen=True)
class Fragmento:
    """Una porción de documento con su procedencia, para poder citarla."""

    texto: str
    documento: str
    seccion: str
    pagina: int

    @property
    def cita(self) -> str:
        base = f"{self.documento}, pág. {self.pagina}"
        return f"{base}, sección «{self.seccion}»" if self.seccion else base

    def to_dict(self) -> dict:
        return asdict(self) | {"cita": self.cita}


def _es_encabezado(linea: str) -> bool:
    if len(linea) > 95 or linea.endswith((".", ",", ";", ":")) and not linea[0].isdigit():
        return False
    return any(p.match(linea) for p in PATRONES_SECCION)


def _limpiar(texto: str) -> str:
    """Normaliza espacios y quita guiones de corte de línea."""
    texto = texto.replace("­", "")
    texto = re.sub(r"(\w)-\n(\w)", r"\1\2", texto)
    texto = re.sub(r"[ \t]+", " ", texto)
    return texto.strip()


def _trocear(texto: str) -> list[str]:
    """Parte un bloque largo en fragmentos con solape, cortando en oraciones."""
    texto = texto.strip()
    if len(texto) <= TAM_FRAGMENTO:
        return [texto] if texto else []

    piezas: list[str] = []
    inicio = 0
    while inicio < len(texto):
        fin = min(inicio + TAM_FRAGMENTO, len(texto))
        if fin < len(texto):
            # Preferimos cortar en un final de oración cercano al límite.
            corte = max(texto.rfind(". ", inicio + TAM_FRAGMENTO // 2, fin),
                        texto.rfind("\n", inicio + TAM_FRAGMENTO // 2, fin))
            if corte > inicio:
                fin = corte + 1
        pieza = texto[inicio:fin].strip()
        if pieza:
            piezas.append(pieza)
        if fin >= len(texto):
            break
        inicio = max(fin - SOLAPE, inicio + 1)
    return piezas


def leer_pdf(ruta: Path) -> list[Fragmento]:
    """Extrae fragmentos de un PDF conservando sección y número de página."""
    documento = nombre_legible(ruta.stem)
    lector = PdfReader(str(ruta))

    fragmentos: list[Fragmento] = []
    seccion_actual = ""
    buffer: list[str] = []
    pagina_buffer = 1

    def volcar() -> None:
        nonlocal buffer
        if not buffer:
            return
        cuerpo = _limpiar("\n".join(buffer))
        for pieza in _trocear(cuerpo):
            # El encabezado se repite dentro del texto del fragmento para que el
            # buscador lo tenga en cuenta al calcular la similitud.
            contenido = f"{seccion_actual}\n{pieza}" if seccion_actual else pieza
            fragmentos.append(
                Fragmento(contenido, documento, seccion_actual, pagina_buffer)
            )
        buffer = []

    for numero_pagina, pagina in enumerate(lector.pages, start=1):
        for linea_cruda in (pagina.extract_text() or "").splitlines():
            linea = linea_cruda.strip()
            if not linea or LINEAS_RUIDO.match(linea):
                continue
            if _es_encabezado(linea):
                volcar()
                seccion_actual = linea
                pagina_buffer = numero_pagina
                continue
            if not buffer:
                pagina_buffer = numero_pagina
            buffer.append(linea)

    volcar()
    return fragmentos


def leer_csv(ruta: Path, nombre: str) -> list[Fragmento]:
    """Convierte cada fila del CSV en un fragmento legible por el modelo."""
    df = pd.read_csv(ruta)
    fragmentos = []
    for _, fila in df.iterrows():
        campos = "; ".join(
            f"{col.replace('_', ' ')}: {valor}" for col, valor in fila.items()
        )
        etiqueta = str(fila.iloc[0])
        fragmentos.append(
            Fragmento(f"Plan {etiqueta}\n{campos}", nombre, f"Plan {etiqueta}", 1)
        )
    return fragmentos


def asegurar_pdfs(dir_pdf: Path) -> None:
    """Genera los PDF a partir del Markdown si todavía no existen.

    Permite que la app arranque en cualquier plataforma (Streamlit Cloud,
    Hugging Face, un contenedor recién construido) sin un paso manual previo:
    lo único que hace falta versionar es el Markdown.
    """
    if dir_pdf.exists() and any(dir_pdf.glob("*.pdf")):
        return
    from scripts.build_pdfs import main as construir_pdfs

    construir_pdfs()


def cargar_corpus(
    dir_pdf: Path | None = None, csv: Path | None = None
) -> list[Fragmento]:
    """Carga todos los PDF de docs/pdf/ más el CSV de planes."""
    dir_pdf = dir_pdf or DIR_PDF
    csv = csv if csv is not None else CSV_PLANES

    asegurar_pdfs(dir_pdf)

    if not dir_pdf.exists() or not any(dir_pdf.glob("*.pdf")):
        raise FileNotFoundError(
            f"No hay PDF en {dir_pdf}. Generalos con:  python scripts/build_pdfs.py"
        )

    corpus: list[Fragmento] = []
    for ruta in sorted(dir_pdf.glob("*.pdf")):
        corpus.extend(leer_pdf(ruta))
    if csv and csv.exists():
        corpus.extend(leer_csv(csv, "Tabla comparativa de planes (CSV)"))
    return corpus


def resumen_corpus(corpus: Iterable[Fragmento]) -> pd.DataFrame:
    """Tabla de control: cuántos fragmentos aportó cada documento."""
    df = pd.DataFrame([f.to_dict() for f in corpus])
    if df.empty:
        return df
    return (
        df.groupby("documento")
        .agg(fragmentos=("texto", "size"), caracteres=("texto", lambda s: int(s.str.len().sum())))
        .reset_index()
        .sort_values("documento")
    )
