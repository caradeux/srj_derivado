import pytest
from pydantic import ValidationError

from derivacion_drm.domain.models import (
    Adolescente, Causa, CasoDerivacion, CentroAsignado,
    Genero, Medida, CentroIPIRC,
)


def test_medida_enum_has_all_siglas():
    assert {m.value for m in Medida} >= {
        "MCA", "SBC", "LAS", "LAE", "LAEIP", "IP", "IRC", "PSA",
        "SALIDAS_ALTERNATIVAS",
    }


def test_centro_ip_irc_enum_has_four():
    assert {c.value for c in CentroIPIRC} == {
        "San_Joaquin", "San_Bernardo", "Til_Til", "Santiago",
    }


def test_adolescente_minimal_valid():
    a = Adolescente(nombre="Juan Pérez", run="12.345.678-9")
    assert a.genero is None and a.comuna is None


def test_causa_default_art_37_bis_false():
    c = Causa()
    assert c.art_37_bis is False


def test_caso_derivacion_requires_centro():
    with pytest.raises(ValidationError):
        CasoDerivacion(
            adolescente=Adolescente(nombre="X", run="1-9"),
            causa=Causa(), medida=Medida.MCA,
        )
