import pytest
from derivacion_drm.domain.text_normalize import normalizar_comuna, strip_acentos


@pytest.mark.parametrize("entrada,esperado", [
    ("Peñalolén", "penalolen"),
    ("Peñalolen", "penalolen"),
    ("PEÑALOLÉN", "penalolen"),
    ("  Ñuñoa  ", "nunoa"),
    ("La Florida", "la florida"),
    ("San José de Maipo", "san jose de maipo"),
])
def test_normalizar_comuna(entrada, esperado):
    assert normalizar_comuna(entrada) == esperado


def test_strip_acentos_preserva_no_letras():
    assert strip_acentos("María del Carmen") == "Maria del Carmen"
