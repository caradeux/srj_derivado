from derivacion_drm.domain.extractors.nombre import (
    normalizar_nombre, extraer_imputados_de_tabla,
)
from derivacion_drm.domain.models import Tabla


def test_normalizar_nombre_title_case_conectores_minuscula():
    assert normalizar_nombre("JUAN DE LA CRUZ PÉREZ") == "Juan de la Cruz Pérez"


def test_normalizar_nombre_strip_parentesis_trailing():
    assert normalizar_nombre("Juan Pérez (ip San Bernardo)") == "Juan Pérez"


def test_normalizar_nombre_strip_coma_trailing():
    assert normalizar_nombre("María González, ") == "María González"


def test_normalizar_nombre_colapsa_espacios_y_saltos():
    assert normalizar_nombre("Juan\nManuel  Pérez") == "Juan Manuel Pérez"


def test_extraer_imputados_filtra_victima():
    tablas = [
        Tabla(encabezados=["NOMBRE IMPUTADO", "RUT", "DIRECCION"],
              filas=[["Juan Pérez", "22.846.782-0", "Calle 1"]]),
        Tabla(encabezados=["VICTIMA", "RUT"],
              filas=[["María González", "8.765.432-9"]]),
    ]
    imputados = extraer_imputados_de_tabla(tablas)
    assert len(imputados) == 1
    assert imputados[0].nombre == "Juan Pérez"


def test_extraer_imputados_filtra_adulto_responsable():
    tablas = [
        Tabla(encabezados=["NOMBRE IMPUTADO", "RUT"],
              filas=[["Cristóbal Soto", "20.111.222-3"]]),
        Tabla(encabezados=["ADULTO RESPONSABLE", "TELÉFONO"],
              filas=[["Carmen Soto", "+56999999999"]]),
    ]
    imputados = extraer_imputados_de_tabla(tablas)
    assert len(imputados) == 1
    assert imputados[0].nombre == "Cristóbal Soto"


def test_extraer_coimputados_devuelve_multiples():
    tablas = [
        Tabla(encabezados=["NOMBRE IMPUTADO", "RUT"],
              filas=[
                  ["Juan Pérez", "22.846.782-0"],
                  ["Jeyson Castro", "22.857.912-2"],
                  ["Cristóbal Soto", "20.111.222-3"],
              ]),
    ]
    imputados = extraer_imputados_de_tabla(tablas)
    assert len(imputados) == 3
    assert {i.nombre for i in imputados} == {"Juan Pérez", "Jeyson Castro", "Cristóbal Soto"}
