import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, model_validator


class Settings(BaseModel):
    """Configuración leída de variables de entorno con defaults locales.

    BRD: la planilla y el logo viven junto al proyecto. data_dir resuelve a
    la carpeta `data/` del repo en producción.
    """
    data_dir: Optional[Path] = None
    profesional_default: Optional[str] = None

    @model_validator(mode="after")
    def _set_defaults_from_env(self) -> "Settings":
        if self.data_dir is None:
            self.data_dir = Path(os.getenv("DERIVACION_DATA_DIR", "data")).resolve()
        if self.profesional_default is None:
            self.profesional_default = os.getenv(
                "DERIVACION_PROFESIONAL_DEFAULT",
                "Juan Manuel Olivares Oyarzún",
            )
        return self

    @property
    def excel_path(self) -> Path:
        return self.data_dir / "CONSOLIDADO_OFERTA_DRM_V2.xlsx"

    @property
    def logo_path(self) -> Path:
        return self.data_dir / "logo_snrsj.png"
