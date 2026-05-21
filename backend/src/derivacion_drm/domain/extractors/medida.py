from derivacion_drm.domain.extractors.base import ExtractedField
from derivacion_drm.domain.models import Medida
from derivacion_drm.domain.sinonimos import ORDEN_MEDIDAS, SINONIMOS_MEDIDA
from derivacion_drm.domain.text_normalize import strip_acentos


def extraer_medida(texto: str) -> ExtractedField[Medida]:
    norm = strip_acentos(texto).lower()
    for medida in ORDEN_MEDIDAS:
        for syn in SINONIMOS_MEDIDA[medida]:
            if strip_acentos(syn).lower() in norm:
                return ExtractedField[Medida](
                    value=medida, confidence="high", source=f"sinónimo: '{syn}'",
                )
    return ExtractedField[Medida](value=None, confidence="low", source="no encontrada")
