from derivacion_drm.domain.extractors.ruc import extraer_ruc


def test_ruc_con_etiqueta_alta_confianza():
    texto = "RUC 2600664806-0 RIT 2903-2026"
    r = extraer_ruc(texto)
    assert r.value == "2600664806-0"
    assert r.confidence == "high"


def test_ruc_sin_etiqueta_baja_confianza():
    texto = "Aparece el número 2600664806-0 en algún lado"
    r = extraer_ruc(texto)
    assert r.value == "2600664806-0"
    assert r.confidence == "low"


def test_ruc_no_encontrado():
    r = extraer_ruc("texto sin números válidos")
    assert r.value is None
