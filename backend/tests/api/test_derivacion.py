from fastapi.testclient import TestClient

from derivacion_drm.api.app import create_app


def _payload_mca() -> dict:
    return {
        "caso": {
            "adolescente": {
                "nombre": "Juan Pérez García", "run": "22.846.782-0",
                "genero": "Masculino", "domicilio": "Calle 1", "comuna": "Lo Espejo",
            },
            "causa": {
                "tribunal": "Unidad Especializada RPA", "tipo_resolucion": "oficio",
                "ruc": "2600664806-0", "rit": "2903-2026",
                "delito": "robo con violencia",
                "fecha_resolucion": "2026-05-10", "art_37_bis": False,
            },
            "medida": "MCA",
            "centro": {
                "nombre": "MCA Centro Sur", "director": "Pedro Soto",
                "mail": "pedro@x.cl", "telefono": "22",
                "direccion": "Av Sur", "tipo": "Priorizada",
            },
        },
        "profesional": "Juan Manuel Olivares Oyarzún",
        "fecha_emision": "2026-05-20",
    }


def test_generar_devuelve_docx_y_filename_correcto():
    c = TestClient(create_app())
    r = c.post("/api/derivacion/generar", json=_payload_mca())
    assert r.status_code == 200
    assert r.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    cd = r.headers["content-disposition"]
    assert "Juan_Perez_Garcia_MCA_Unidad_Especializada_Rpa_2903-2026_2600664806-0.docx" in cd
    assert len(r.content) > 1000


def test_generar_request_invalido_devuelve_422():
    c = TestClient(create_app())
    payload = _payload_mca()
    del payload["caso"]["adolescente"]["nombre"]
    r = c.post("/api/derivacion/generar", json=payload)
    assert r.status_code == 422
