from derivacion_drm.domain.extractors.adulto import extraer_adulto
from derivacion_drm.domain.models import Tabla


def test_extrae_adulto_con_nombre_y_telefono():
    tablas = [
        Tabla(encabezados=["NOMBRE IMPUTADO", "RUT"],
              filas=[["Juan Pérez", "22.846.782-0"]]),
        Tabla(encabezados=["ADULTO RESPONSABLE", "TELÉFONO"],
              filas=[["Carmen Soto", "+56 9 1234 5678"]]),
    ]
    a = extraer_adulto(tablas)
    assert a.nombre == "Carmen Soto"
    assert a.telefono == "+56 9 1234 5678"


def test_sin_tabla_de_adulto_devuelve_vacio():
    tablas = [Tabla(encabezados=["NOMBRE IMPUTADO"], filas=[["Juan"]])]
    a = extraer_adulto(tablas)
    assert a.nombre is None and a.telefono is None


def test_adulto_sin_telefono():
    tablas = [
        Tabla(encabezados=["ADULTO RESPONSABLE"], filas=[["Carmen Soto"]]),
    ]
    a = extraer_adulto(tablas)
    assert a.nombre == "Carmen Soto" and a.telefono is None
