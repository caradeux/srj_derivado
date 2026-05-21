from pathlib import Path

import pandas as pd

from derivacion_drm.domain.centros import CatalogoOferta, EntradaOferta
from derivacion_drm.domain.models import Medida
from derivacion_drm.domain.sinonimos import SINONIMOS_MEDIDA
from derivacion_drm.domain.text_normalize import strip_acentos


def _identificar_medida(texto: str) -> Medida | None:
    norm = strip_acentos(texto).lower().strip()
    for medida, sinonimos in SINONIMOS_MEDIDA.items():
        for s in sinonimos:
            if strip_acentos(s).lower() == norm:
                return medida
    # fallback: si el texto contiene la sigla exacta
    for medida in Medida:
        if medida.value.lower() == norm:
            return medida
    return None


def _split_comunas(s: str | float | None) -> list[str]:
    if not s or (isinstance(s, float) and pd.isna(s)):
        return []
    return [c.strip() for c in str(s).split(",") if c.strip()]


def cargar_catalogo(path: Path, hoja: str = "Desacumulado") -> CatalogoOferta:
    """Carga CONSOLIDADO_OFERTA_DRM_V2.xlsx hoja Desacumulado (BRD §13.1)."""
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_excel(path, sheet_name=hoja, dtype=str).fillna("")
    entradas: list[EntradaOferta] = []
    for _, fila in df.iterrows():
        medida = _identificar_medida(fila["Tipo de medida o sanción"])
        if medida is None:
            continue
        entradas.append(EntradaOferta(
            programa=str(fila["PROGRAMA"]).strip(),
            medida=medida,
            comunas_priorizadas=_split_comunas(fila["COMUNAS PRIORIZADAS"]),
            comunas_no_priorizadas=_split_comunas(fila["COMUNAS NO PRIORIZADAS"]),
            direccion=str(fila["DIRECCION"]).strip(),
            director=str(fila["DIRECTOR"]).strip(),
            mail=str(fila["CONTACTO MAIL"]).strip(),
            telefono=str(fila["TELEFONO"]).strip(),
        ))
    return CatalogoOferta(entradas=entradas)
