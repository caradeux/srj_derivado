from derivacion_drm.domain.extractors.rit import extraer_rit


def test_rit_con_etiqueta():
    r = extraer_rit("RUC 2600664806-0 RIT 2903-2026")
    assert r.value == "2903-2026"
    assert r.confidence == "high"


def test_rit_descarta_fechas():
    # "10-2026" tiene formato de RIT pero no está precedido por RIT — NO debe matchear
    # sin etiqueta. La etiqueta es lo que distingue de "DD-AAAA" en fechas truncadas.
    r = extraer_rit("Documento fechado 10-2026 sin más contexto")
    assert r.value is None or r.confidence == "low"


def test_rit_no_encontrado():
    assert extraer_rit("texto vacío").value is None
