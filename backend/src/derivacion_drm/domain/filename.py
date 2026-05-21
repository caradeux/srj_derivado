import re

from derivacion_drm.domain.models import CasoDerivacion, Medida
from derivacion_drm.domain.text_normalize import strip_acentos

# BRD §14.3 — sigla del centro por nombre canónico
_SIGLA_POR_NOMBRE_CENTRO: dict[str, str] = {
    "san joaquin": "San_Joaquin",
    "san bernardo": "San_Bernardo",
    "til til": "Til_Til",
    "santiago": "Santiago",
}

_MEDIDAS_CON_SIGLA_CENTRO = {Medida.IP, Medida.IRC}


def _ascii_safe(s: str) -> str:
    """Reemplaza no-letras (excepto guion y guion bajo) por guion bajo."""
    s = strip_acentos(s)
    s = re.sub(r"[^A-Za-z0-9_-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def _sigla_centro_ipirc(nombre_centro: str) -> str:
    n = strip_acentos(nombre_centro).lower()
    for clave, sigla in _SIGLA_POR_NOMBRE_CENTRO.items():
        if clave in n:
            return sigla
    return _ascii_safe(nombre_centro)


def _title_case_archivo(s: str) -> str:
    """Capitaliza cada palabra para el nombre de archivo (BRD §14.3)."""
    return " ".join(w.capitalize() for w in s.split())


def componer_nombre_archivo(caso: CasoDerivacion) -> str:
    """BR-04, FR-19, RN-09.

    Estándar: {Nombre}_{Medida}_{Tribunal}_{RIT}_{RUC}.docx
    IP/IRC:   {Nombre}_{Medida}_{Sigla_Centro}_{Tribunal}_{RIT}_{RUC}.docx
    """
    nombre = _ascii_safe(_title_case_archivo(caso.adolescente.nombre))
    medida = caso.medida.value
    tribunal = _ascii_safe(_title_case_archivo(caso.causa.tribunal or "Sin_Tribunal"))
    rit = caso.causa.rit or "Sin_RIT"
    ruc = caso.causa.ruc or "Sin_RUC"

    if caso.medida in _MEDIDAS_CON_SIGLA_CENTRO:
        sigla = _sigla_centro_ipirc(caso.centro.nombre)
        return f"{nombre}_{medida}_{sigla}_{tribunal}_{rit}_{ruc}.docx"
    return f"{nombre}_{medida}_{tribunal}_{rit}_{ruc}.docx"
