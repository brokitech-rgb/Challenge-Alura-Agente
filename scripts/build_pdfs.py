"""Convierte los documentos Markdown de docs/ en los PDF de docs/pdf/.

Los PDF son la fuente de verdad que consume el agente: el challenge pide que
el agente responda a partir de un documento PDF o CSV, así que el Markdown es
solo el formato editable y el PDF es el artefacto que se indexa.

Uso:
    python scripts/build_pdfs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DIR_DOCS, DIR_PDF  # noqa: E402

# Glifos que no existen en la codificación WinAnsi de las fuentes base de
# ReportLab. Se reemplazan por equivalentes ASCII para que el PDF sea legible
# tanto en Windows como en la VM Linux de OCI.
REEMPLAZOS = {
    "✓": "Si",
    "✔": "Si",
    "✗": "No",
    "✘": "No",
    "≥": ">=",
    "≤": "<=",
    "→": "->",
    " ": " ",
}

def _registrar_fuentes() -> tuple[str, str]:
    """Registra una TrueType embebida en lugar de las fuentes base del PDF.

    Las fuentes base (Helvetica) se escriben sin tabla ToUnicode, así que al
    extraer el texto con pypdf las vocales acentuadas vuelven como U+FFFD. Una
    TrueType embebida sí lleva ToUnicode y el texto se recupera intacto, que es
    justo lo que necesita el indexador.

    Vera viene incluida en el paquete reportlab, así que funciona igual en
    Windows y en la VM Linux de OCI sin depender de fuentes del sistema.
    """
    import reportlab

    dir_fuentes = Path(reportlab.__file__).parent / "fonts"
    regular = dir_fuentes / "Vera.ttf"
    negrita = dir_fuentes / "VeraBd.ttf"
    if regular.exists() and negrita.exists():
        pdfmetrics.registerFont(TTFont("Vera", str(regular)))
        pdfmetrics.registerFont(TTFont("Vera-Bold", str(negrita)))
        return "Vera", "Vera-Bold"
    return "Helvetica", "Helvetica-Bold"


FUENTE, FUENTE_NEGRITA = _registrar_fuentes()


def _escapar(texto: str) -> str:
    """Escapa XML y traduce el mini-Markdown inline a etiquetas de ReportLab."""
    for origen, destino in REEMPLAZOS.items():
        texto = texto.replace(origen, destino)
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", texto)
    texto = re.sub(r"`([^`]+?)`", r'<font face="Courier">\1</font>', texto)
    return texto


def _construir_estilos():
    base = getSampleStyleSheet()
    return {
        "titulo": ParagraphStyle(
            "TituloDoc", parent=base["Title"], fontName=FUENTE_NEGRITA,
            fontSize=20, leading=25, spaceAfter=14, textColor=colors.HexColor("#0f2b46"),
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading1"], fontName=FUENTE_NEGRITA,
            fontSize=14, leading=18, spaceBefore=16, spaceAfter=7,
            textColor=colors.HexColor("#12507e"),
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading2"], fontName=FUENTE_NEGRITA,
            fontSize=11.5, leading=15, spaceBefore=11, spaceAfter=5,
            textColor=colors.HexColor("#1f6fb0"),
        ),
        "h4": ParagraphStyle(
            "H4", parent=base["Heading3"], fontName=FUENTE_NEGRITA,
            fontSize=10.5, leading=14, spaceBefore=9, spaceAfter=4,
            textColor=colors.HexColor("#3a3a3a"),
        ),
        "cuerpo": ParagraphStyle(
            "Cuerpo", parent=base["BodyText"], fontName=FUENTE,
            fontSize=9.5, leading=14, alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "cita": ParagraphStyle(
            "Cita", parent=base["BodyText"], fontName=FUENTE,
            fontSize=9.5, leading=14, leftIndent=14, spaceAfter=6,
            borderPadding=(4, 4, 4, 4), backColor=colors.HexColor("#f2f6fa"),
        ),
        "celda": ParagraphStyle(
            "Celda", fontName=FUENTE, fontSize=8, leading=10.5,
        ),
        "celda_encabezado": ParagraphStyle(
            "CeldaEnc", fontName=FUENTE_NEGRITA, fontSize=8, leading=10.5,
            textColor=colors.white,
        ),
    }


def _es_separador_de_tabla(linea: str) -> bool:
    return bool(re.fullmatch(r"\|[\s:\-|]+\|", linea.strip()))


def _celdas(linea: str) -> list[str]:
    return [c.strip() for c in linea.strip().strip("|").split("|")]


def _tabla(filas: list[list[str]], estilos) -> Table:
    encabezado = [Paragraph(_escapar(c), estilos["celda_encabezado"]) for c in filas[0]]
    cuerpo = [[Paragraph(_escapar(c), estilos["celda"]) for c in fila] for fila in filas[1:]]
    ancho_util = A4[0] - 4 * cm
    n = max(len(f) for f in filas)
    tabla = Table([encabezado] + cuerpo, colWidths=[ancho_util / n] * n, repeatRows=1)
    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12507e")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9d4de")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f7fa")]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return tabla


def markdown_a_flowables(markdown: str, estilos) -> list:
    """Traduce el subconjunto de Markdown que usan los documentos."""
    flowables: list = []
    lineas = markdown.splitlines()
    i = 0
    vinetas: list[str] = []

    def volcar_vinetas() -> None:
        nonlocal vinetas
        if vinetas:
            flowables.append(
                ListFlowable(
                    [ListItem(Paragraph(_escapar(v), estilos["cuerpo"])) for v in vinetas],
                    bulletType="bullet",
                    bulletFontName=FUENTE,
                    leftIndent=16,
                )
            )
            flowables.append(Spacer(1, 4))
            vinetas = []

    while i < len(lineas):
        linea = lineas[i].rstrip()
        despojada = linea.strip()

        if not despojada:
            volcar_vinetas()
            i += 1
            continue

        # Tabla: fila de encabezado seguida de la línea separadora |---|---|
        if despojada.startswith("|") and i + 1 < len(lineas) and _es_separador_de_tabla(lineas[i + 1]):
            volcar_vinetas()
            filas = [_celdas(despojada)]
            i += 2
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                filas.append(_celdas(lineas[i]))
                i += 1
            flowables.append(Spacer(1, 4))
            flowables.append(_tabla(filas, estilos))
            flowables.append(Spacer(1, 8))
            continue

        if despojada.startswith("#### "):
            volcar_vinetas()
            flowables.append(Paragraph(_escapar(despojada[5:]), estilos["h4"]))
        elif despojada.startswith("### "):
            volcar_vinetas()
            flowables.append(Paragraph(_escapar(despojada[4:]), estilos["h3"]))
        elif despojada.startswith("## "):
            volcar_vinetas()
            flowables.append(Paragraph(_escapar(despojada[3:]), estilos["h2"]))
        elif despojada.startswith("# "):
            volcar_vinetas()
            flowables.append(Paragraph(_escapar(despojada[2:]), estilos["titulo"]))
        elif despojada.startswith("> "):
            volcar_vinetas()
            flowables.append(Paragraph(_escapar(despojada[2:]), estilos["cita"]))
        elif despojada in {"---", "***", "___"}:
            volcar_vinetas()
            flowables.append(Spacer(1, 5))
            flowables.append(HRFlowable(width="100%", color=colors.HexColor("#c9d4de")))
            flowables.append(Spacer(1, 5))
        elif re.match(r"^[-*]\s+", despojada):
            vinetas.append(re.sub(r"^[-*]\s+", "", despojada))
        elif re.match(r"^\d+\.\s+", despojada):
            volcar_vinetas()
            flowables.append(Paragraph(_escapar(despojada), estilos["cuerpo"]))
        else:
            volcar_vinetas()
            flowables.append(Paragraph(_escapar(despojada), estilos["cuerpo"]))
        i += 1

    volcar_vinetas()
    return flowables


def _pie_de_pagina(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont(FUENTE, 7.5)
    canvas.setFillColor(colors.HexColor("#7a8894"))
    canvas.drawString(2 * cm, 1.2 * cm, "Brokitech Turnos - Documentacion oficial")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def construir_pdf(ruta_md: Path, ruta_pdf: Path) -> None:
    estilos = _construir_estilos()
    doc = SimpleDocTemplate(
        str(ruta_pdf),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=ruta_md.stem,
        author="Brokitech S.A.S.",
    )
    doc.build(
        markdown_a_flowables(ruta_md.read_text(encoding="utf-8"), estilos),
        onFirstPage=_pie_de_pagina,
        onLaterPages=_pie_de_pagina,
    )


def main() -> int:
    DIR_PDF.mkdir(parents=True, exist_ok=True)
    fuentes = sorted(DIR_DOCS.glob("*.md"))
    if not fuentes:
        print(f"No se encontraron .md en {DIR_DOCS}")
        return 1
    for ruta_md in fuentes:
        destino = DIR_PDF / f"{ruta_md.stem}.pdf"
        construir_pdf(ruta_md, destino)
        print(f"  OK  {ruta_md.name}  ->  {destino.relative_to(DIR_PDF.parent.parent)}")
    print(f"\n{len(fuentes)} PDF generados en {DIR_PDF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
