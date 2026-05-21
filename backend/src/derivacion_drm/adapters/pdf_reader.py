from pathlib import Path

import pdfplumber
from PyPDF2 import PdfReader

from derivacion_drm.domain.models import DocumentoCargado, Tabla


def _tablas_neutralizadas(page_tables: list[list[list[str | None]]]) -> list[Tabla]:
    """Convierte la matriz cruda de pdfplumber a list[Tabla]."""
    out: list[Tabla] = []
    for raw in page_tables:
        if not raw or not raw[0]:
            continue
        encab = [str(c or "").strip() for c in raw[0]]
        filas = [[str(c or "").strip() for c in fila] for fila in raw[1:]]
        out.append(Tabla(encabezados=encab, filas=filas))
    return out


def leer_pdf(path: Path) -> DocumentoCargado:
    """BRD §10.2: pdfplumber primario para preservar tablas, PyPDF2 fallback."""
    if not path.exists():
        raise FileNotFoundError(path)
    texto_partes: list[str] = []
    tablas: list[Tabla] = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                texto_partes.append(t)
                tablas.extend(_tablas_neutralizadas(page.extract_tables() or []))
    except Exception:
        # Fallback PyPDF2
        reader = PdfReader(str(path))
        for page in reader.pages:
            texto_partes.append(page.extract_text() or "")
    return DocumentoCargado(
        nombre_archivo=path.name,
        texto="\n".join(texto_partes),
        tablas=tablas,
    )
