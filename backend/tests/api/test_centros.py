from fastapi.testclient import TestClient

from derivacion_drm.api.app import create_app
from derivacion_drm.api.deps import get_catalogo
from derivacion_drm.domain.centros import CatalogoOferta, EntradaOferta
from derivacion_drm.domain.models import Medida


def _catalogo_test() -> CatalogoOferta:
    return CatalogoOferta(entradas=[
        EntradaOferta(
            programa="MCA Centro Sur", medida=Medida.MCA,
            comunas_priorizadas=["Lo Espejo"], comunas_no_priorizadas=[],
            direccion="Av Sur", director="P", mail="p@x", telefono="1",
        ),
    ])


def _client_con_catalogo() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_catalogo] = _catalogo_test
    return TestClient(app)


def test_resolver_devuelve_un_centro():
    c = _client_con_catalogo()
    r = c.post("/api/centros/resolver", json={"medida": "MCA", "comuna": "Lo Espejo"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "MCA Centro Sur"


def test_resolver_sin_match_devuelve_lista_vacia():
    c = _client_con_catalogo()
    r = c.post("/api/centros/resolver", json={"medida": "MCA", "comuna": "Otra"})
    assert r.status_code == 200
    assert r.json() == []


def test_ip_irc_devuelve_4_centros():
    c = TestClient(create_app())
    r = c.get("/api/centros/ip-irc")
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"San_Joaquin", "San_Bernardo", "Til_Til", "Santiago"}
    assert data["San_Joaquin"]["director"] == "Virna Salazar"
