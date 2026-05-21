from derivacion_drm.domain.extractors.base import ExtractedField


def test_extracted_field_holds_value_confidence_source():
    f = ExtractedField[str](value="X", confidence="high", source="tabla acta")
    assert f.value == "X" and f.confidence == "high" and f.source == "tabla acta"


def test_extracted_field_none_value_low_confidence():
    f = ExtractedField[str](value=None, confidence="low", source="no encontrado")
    assert f.value is None
