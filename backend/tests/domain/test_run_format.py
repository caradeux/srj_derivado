import pytest
from derivacion_drm.domain.run_format import formatear_run


@pytest.mark.parametrize("entrada,esperado", [
    ("0022846782-0", "22.846.782-0"),
    ("22846782-0", "22.846.782-0"),
    ("22.846.782-0", "22.846.782-0"),
    ("8765432-9", "8.765.432-9"),
    ("8.765.432-9", "8.765.432-9"),
    ("12345678K", "12.345.678-K"),
    ("12345678-k", "12.345.678-K"),
])
def test_formatear_run_canonical(entrada, esperado):
    assert formatear_run(entrada) == esperado


def test_formatear_run_invalido_devuelve_none():
    assert formatear_run("abc") is None
    assert formatear_run("") is None
