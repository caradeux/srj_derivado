from datetime import date

from derivacion_drm.domain.extractors.causa import extraer_causa


def test_extrae_tribunal_unidad_especializada():
    c = extraer_causa("Causa ante la Unidad Especializada RPA, Santiago")
    assert c.tribunal is not None and "Unidad Especializada" in c.tribunal


def test_extrae_tribunal_juzgado_garantia():
    c = extraer_causa("4° Juzgado de Garantía de Santiago")
    assert "Juzgado de Garantía" in (c.tribunal or "")


def test_extrae_ruc_rit_via_causa():
    c = extraer_causa("RUC 2600664806-0 RIT 2903-2026 ordena...")
    assert c.ruc == "2600664806-0"
    assert c.rit == "2903-2026"


def test_extrae_tipo_resolucion_oficio():
    c = extraer_causa("Mediante el presente oficio se ordena...")
    assert c.tipo_resolucion is not None and "oficio" in c.tipo_resolucion.lower()


def test_extrae_tipo_resolucion_sentencia():
    c = extraer_causa("se dicta sentencia ejecutoriada en autos")
    assert "sentencia" in (c.tipo_resolucion or "").lower()


def test_extrae_fecha_formato_largo():
    c = extraer_causa("De fecha 10 de mayo de 2026, se ordena...")
    assert c.fecha_resolucion == date(2026, 5, 10)


def test_extrae_fecha_formato_corto():
    c = extraer_causa("Fecha: 10/05/2026")
    assert c.fecha_resolucion == date(2026, 5, 10)


def test_detecta_delito_de_catalogo():
    c = extraer_causa("por el delito de robo con violencia")
    assert c.delito is not None and "robo" in c.delito.lower()


def test_art_37_bis_marcado():
    c = extraer_causa("Evacúese informe Técnico conforme al artículo 37 bis")
    assert c.art_37_bis is True
