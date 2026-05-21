from pathlib import Path

from derivacion_drm.adapters.word_reader import leer_docx


def test_leer_docx_devuelve_texto_y_tablas(sample_docx_path: Path):
    doc = leer_docx(sample_docx_path)
    assert doc.nombre_archivo == sample_docx_path.name
    assert "RUC" in doc.texto
    assert len(doc.tablas) == 1
    assert doc.tablas[0].encabezados == ["NOMBRE IMPUTADO", "RUT"]
    assert doc.tablas[0].filas == [["Juan Pérez", "22.846.782-0"]]
