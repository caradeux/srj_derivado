import re

from derivacion_drm.domain.extractors.base import ExtractedField

_RIT_CON_ETIQUETA = re.compile(r"RIT[\s:]*?(\d{1,6}-\d{4})", re.IGNORECASE)


def extraer_rit(texto: str) -> ExtractedField[str]:
    m = _RIT_CON_ETIQUETA.search(texto)
    if m:
        return ExtractedField[str](value=m.group(1), confidence="high", source="etiqueta RIT")
    return ExtractedField[str](value=None, confidence="low", source="no encontrado")
