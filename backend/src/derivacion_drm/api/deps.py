from functools import lru_cache

from fastapi import Depends

from derivacion_drm.adapters.excel_catalog import cargar_catalogo
from derivacion_drm.api.config import Settings
from derivacion_drm.domain.centros import CatalogoOferta


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def _catalogo_cache(excel_path_str: str) -> CatalogoOferta:
    from pathlib import Path
    return cargar_catalogo(Path(excel_path_str))


def get_catalogo(
    settings: Settings = Depends(get_settings),
) -> CatalogoOferta:
    """Cargado una vez por ejecución (BRD §10.2). Reiniciar el proceso recarga."""
    return _catalogo_cache(str(settings.excel_path))
