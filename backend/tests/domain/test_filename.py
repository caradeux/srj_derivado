from derivacion_drm.domain.filename import componer_nombre_archivo
from derivacion_drm.domain.models import (
    Adolescente, CasoDerivacion, Causa, CentroAsignado, Medida,
)


def _caso(medida: Medida, centro_nombre: str = "Centro X") -> CasoDerivacion:
    return CasoDerivacion(
        adolescente=Adolescente(nombre="Juan Manuel Pérez García", run="22.846.782-0"),
        causa=Causa(
            tribunal="Unidad Especializada RPA",
            ruc="2600664806-0", rit="2903-2026",
        ),
        medida=medida,
        centro=CentroAsignado(
            nombre=centro_nombre, director="d", mail="m", telefono="t",
        ),
    )


def test_filename_estandar_mca():
    n = componer_nombre_archivo(_caso(Medida.MCA))
    assert n == "Juan_Manuel_Perez_Garcia_MCA_Unidad_Especializada_Rpa_2903-2026_2600664806-0.docx"


def test_filename_irc_incluye_sigla_centro():
    caso = _caso(Medida.IRC, centro_nombre="Centro IP - IRC San Joaquín")
    n = componer_nombre_archivo(caso)
    assert "_IRC_San_Joaquin_" in n


def test_filename_ip_til_til():
    caso = _caso(Medida.IP, centro_nombre="C.M.N. Til Til")
    n = componer_nombre_archivo(caso)
    assert "_IP_Til_Til_" in n


def test_filename_sin_tildes():
    caso = _caso(Medida.MCA)
    caso.adolescente.nombre = "Cristóbal Ñañez"
    n = componer_nombre_archivo(caso)
    assert "Cristobal_Nanez" in n
