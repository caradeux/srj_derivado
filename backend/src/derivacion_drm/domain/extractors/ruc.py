import re

from derivacion_drm.domain.extractors.base import ExtractedField

_RUC_CON_ETIQUETA = re.compile(r"RUC[\s:]*?(\d{10,12}-[0-9kK])", re.IGNORECASE)
_RUC_SIN_ETIQUETA = re.compile(r"\b(\d{10,12}-[0-9kK])\b")


def extraer_ruc(texto: str) -> ExtractedField[str]:
    m = _RUC_CON_ETIQUETA.search(texto)
    if m:
        return ExtractedField[str](value=m.group(1), confidence="high", source="etiqueta RUC")
    m = _RUC_SIN_ETIQUETA.search(texto)
    if m:
        return ExtractedField[str](value=m.group(1), confidence="low", source="regex fallback")
    return ExtractedField[str](value=None, confidence="low", source="no encontrado")
