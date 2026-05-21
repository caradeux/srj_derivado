import re
from datetime import date

from derivacion_drm.domain.delitos import DELITOS_COMUNES
from derivacion_drm.domain.extractors.art_37_bis import detectar_art_37_bis
from derivacion_drm.domain.extractors.ruc import extraer_ruc
from derivacion_drm.domain.extractors.rit import extraer_rit
from derivacion_drm.domain.models import Causa

_MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11,
    "diciembre": 12,
}
_FECHA_LARGA = re.compile(
    r"\b(\d{1,2})\s+de\s+(" + "|".join(_MESES) + r")\s+de\s+(\d{4})\b",
    re.IGNORECASE,
)
_FECHA_CORTA = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")

_TRIBUNALES = [
    re.compile(r"Unidad Especializada\s*R\.?P\.?A\.?", re.IGNORECASE),
    re.compile(r"(\d+°?\s*)?Juzgado de Garantía[^.\n]*", re.IGNORECASE),
    re.compile(r"Tribunal de Juicio Oral en lo Penal[^.\n]*", re.IGNORECASE),
]


def _extraer_tribunal(texto: str) -> str | None:
    for pat in _TRIBUNALES:
        m = pat.search(texto)
        if m:
            return re.sub(r"\s+", " ", m.group(0)).strip().rstrip(",.")
    return None


def _extraer_tipo_resolucion(texto: str) -> str | None:
    t = texto.lower()
    if "sentencia ejecutoriada" in t:
        return "sentencia ejecutoriada"
    if "sentencia" in t:
        return "sentencia"
    if "oficio" in t:
        return "oficio"
    if "resolución" in t or "resolucion" in t:
        return "resolución"
    return None


def _extraer_fecha(texto: str) -> date | None:
    m = _FECHA_LARGA.search(texto)
    if m:
        d, mes_nombre, a = m.groups()
        return date(int(a), _MESES[mes_nombre.lower()], int(d))
    m = _FECHA_CORTA.search(texto)
    if m:
        d, mm, a = m.groups()
        return date(int(a), int(mm), int(d))
    return None


def _extraer_delito(texto: str) -> str | None:
    t = texto.lower()
    for d in DELITOS_COMUNES:
        if d in t:
            return d
    return None


def extraer_causa(texto: str) -> Causa:
    return Causa(
        tribunal=_extraer_tribunal(texto),
        tipo_resolucion=_extraer_tipo_resolucion(texto),
        ruc=extraer_ruc(texto).value,
        rit=extraer_rit(texto).value,
        delito=_extraer_delito(texto),
        fecha_resolucion=_extraer_fecha(texto),
        art_37_bis=detectar_art_37_bis(texto),
    )
