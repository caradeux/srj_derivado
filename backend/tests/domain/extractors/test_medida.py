import pytest
from derivacion_drm.domain.models import Medida
from derivacion_drm.domain.extractors.medida import extraer_medida


@pytest.mark.parametrize("texto,esperada", [
    ("se ordena MCA conforme al 155 letra B", Medida.MCA),
    ("la medida cautelar ambulatoria ordenada", Medida.MCA),
    ("dicta sentencia a Libertad Asistida Simple", Medida.LAS),
    ("libertad asistida especial con internación parcial", Medida.LAEIP),
    ("internación provisoria del adolescente", Medida.IP),
    ("régimen cerrado por 3 años", Medida.IRC),
    ("suspensión condicional del procedimiento", Medida.SALIDAS_ALTERNATIVAS),
])
def test_extraer_medida_por_sinonimos(texto, esperada):
    r = extraer_medida(texto)
    assert r.value == esperada


def test_extraer_medida_no_detectada():
    assert extraer_medida("texto sin medidas").value is None


def test_laeip_no_confunde_con_lae():
    # "LAEIP" debe ganar a "LAE" — orden de búsqueda por especificidad
    r = extraer_medida("se ordena LAEIP por 2 años")
    assert r.value == Medida.LAEIP
