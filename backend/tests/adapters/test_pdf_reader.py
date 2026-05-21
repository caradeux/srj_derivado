from pathlib import Path

from derivacion_drm.adapters.pdf_reader import leer_pdf


def test_leer_pdf_devuelve_documento_cargado(sample_pdf_path: Path):
    doc = leer_pdf(sample_pdf_path)
    assert doc.nombre_archivo == sample_pdf_path.name
    assert "RUC" in doc.texto
    assert "2600664806-0" in doc.texto


def test_leer_pdf_inexistente_lanza(tmp_path: Path):
    import pytest
    with pytest.raises(FileNotFoundError):
        leer_pdf(tmp_path / "no_existe.pdf")
