from fastapi.testclient import TestClient

from derivacion_drm.api.app import create_app


def test_catalogo_medidas_incluye_mca_y_pendientes():
    c = TestClient(create_app())
    r = c.get("/api/catalogo/medidas")
    assert r.status_code == 200
    data = r.json()
    siglas = {m["sigla"] for m in data}
    assert "MCA" in siglas and "PSA" in siglas
    psa = next(m for m in data if m["sigla"] == "PSA")
    assert psa["estado"] == "pendiente"
    mca = next(m for m in data if m["sigla"] == "MCA")
    assert mca["estado"] == "activa"


def test_catalogo_delitos_no_vacio():
    c = TestClient(create_app())
    r = c.get("/api/catalogo/delitos")
    assert r.status_code == 200
    delitos = r.json()
    assert len(delitos) >= 30
    assert any("robo" in d for d in delitos)
