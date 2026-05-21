from pathlib import Path

from derivacion_drm.api.config import Settings


def test_settings_default_data_dir(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("DERIVACION_DATA_DIR", str(tmp_path))
    s = Settings()
    assert s.data_dir == tmp_path
    assert s.excel_path == tmp_path / "CONSOLIDADO_OFERTA_DRM_V2.xlsx"
    assert s.logo_path == tmp_path / "logo_snrsj.png"


def test_settings_default_profesional():
    s = Settings()
    # No exigimos un nombre por defecto, pero el campo existe
    assert hasattr(s, "profesional_default")
