import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, model_validator

# Raíz del repo (subiendo desde backend/src/derivacion_drm/api/config.py).
# Independiente del CWD desde donde se arranque uvicorn.
_REPO_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseModel):
    """Configuración leída de variables de entorno con defaults locales.

    BRD: la planilla y el logo viven junto al proyecto. data_dir resuelve a
    la carpeta `data/` del repo (no del CWD).
    """
    data_dir: Optional[Path] = None
    profesional_default: Optional[str] = None

    @model_validator(mode="after")
    def _set_defaults_from_env(self) -> "Settings":
        if self.data_dir is None:
            env_path = os.getenv("DERIVACION_DATA_DIR")
            self.data_dir = (
                Path(env_path).resolve() if env_path else (_REPO_ROOT / "data").resolve()
            )
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
