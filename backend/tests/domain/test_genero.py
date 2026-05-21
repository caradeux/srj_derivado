import pytest
from derivacion_drm.domain.models import Genero
from derivacion_drm.domain.genero import inferir_genero


@pytest.mark.parametrize("primer_nombre,esperado", [
    ("María", Genero.FEMENINO),
    ("MARIA", Genero.FEMENINO),
    ("Catalina", Genero.FEMENINO),
    ("Javiera", Genero.FEMENINO),
    ("Juan", Genero.MASCULINO),
    ("Cristóbal", Genero.MASCULINO),
    ("Jeyson", Genero.MASCULINO),
])
def test_inferir_genero(primer_nombre, esperado):
    assert inferir_genero(primer_nombre) == esperado


def test_inferir_genero_desconocido_devuelve_none():
    assert inferir_genero("Xyz123") is None


def test_inferir_genero_compuesto_usa_primer_token():
    # "María José" → primer token "María" → FEMENINO
    assert inferir_genero("María José") == Genero.FEMENINO
