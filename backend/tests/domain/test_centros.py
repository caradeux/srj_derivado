from derivacion_drm.domain.centros import (
    CENTROS_IP_IRC, CatalogoOferta, EntradaOferta, centro_ip_irc,
    resolver_centro_estandar,
)
from derivacion_drm.domain.models import CentroIPIRC, Medida


def _entrada(programa: str, medida: Medida, priorizadas: str = "", no_prior: str = "") -> EntradaOferta:
    return EntradaOferta(
        programa=programa, medida=medida,
        comunas_priorizadas=[c.strip() for c in priorizadas.split(",") if c.strip()],
        comunas_no_priorizadas=[c.strip() for c in no_prior.split(",") if c.strip()],
        direccion="dir", director="dr", mail="m@x", telefono="111",
    )


def test_resolver_un_centro_por_comuna_priorizada():
    cat = CatalogoOferta(entradas=[
        _entrada("MCA Centro Sur", Medida.MCA, priorizadas="Lo Espejo, La Cisterna"),
    ])
    centros = resolver_centro_estandar(Medida.MCA, "Lo Espejo", cat)
    assert len(centros) == 1
    assert centros[0].nombre == "MCA Centro Sur"
    assert centros[0].tipo == "Priorizada"


def test_resolver_normaliza_tildes_y_caso():
    cat = CatalogoOferta(entradas=[
        _entrada("LAE Peñalolén", Medida.LAE, priorizadas="Peñalolén"),
    ])
    centros = resolver_centro_estandar(Medida.LAE, "PEÑALOLEN", cat)
    assert len(centros) == 1


def test_resolver_dos_centros_si_priorizada_y_no_priorizada():
    cat = CatalogoOferta(entradas=[
        _entrada("Centro A", Medida.LAE, priorizadas="Santiago"),
        _entrada("Centro B", Medida.LAE, no_prior="Santiago"),
    ])
    centros = resolver_centro_estandar(Medida.LAE, "Santiago", cat)
    assert len(centros) == 2


def test_resolver_sin_match_devuelve_lista_vacia():
    cat = CatalogoOferta(entradas=[
        _entrada("Centro X", Medida.MCA, priorizadas="Otra Comuna"),
    ])
    centros = resolver_centro_estandar(Medida.MCA, "Lo Espejo", cat)
    assert centros == []


def test_centros_ip_irc_contiene_4_centros():
    assert set(CENTROS_IP_IRC) == set(CentroIPIRC)


def test_centro_ip_irc_devuelve_san_joaquin():
    c = centro_ip_irc(CentroIPIRC.SAN_JOAQUIN)
    assert "San Joaquín" in c.nombre
    assert c.director == "Virna Salazar"
    assert c.mail == "ingresos.ipircsnjqn@reinsercionjuvenil.cl"
