from pathlib import Path

from derivacion_drm.adapters.excel_catalog import cargar_catalogo
from derivacion_drm.domain.models import Medida


def test_cargar_catalogo_lee_dos_filas(sample_excel_path: Path):
    cat = cargar_catalogo(sample_excel_path)
    assert len(cat.entradas) == 2


def test_cargar_catalogo_parsea_comunas_separadas_por_coma(sample_excel_path: Path):
    cat = cargar_catalogo(sample_excel_path)
    mca = next(e for e in cat.entradas if e.medida == Medida.MCA)
    assert mca.comunas_priorizadas == ["Lo Espejo", "La Cisterna"]
    assert mca.comunas_no_priorizadas == []


def test_cargar_catalogo_normaliza_medida_via_sinonimos(sample_excel_path: Path):
    cat = cargar_catalogo(sample_excel_path)
    medidas = {e.medida for e in cat.entradas}
    assert Medida.MCA in medidas and Medida.LAE in medidas
