"""Verifica que domain/ no importe de adapters/ ni de api/.

BRD spec §4 — regla de dependencias por capas.
"""
import ast
from pathlib import Path

import pytest

DOMAIN = Path(__file__).resolve().parents[1] / "src" / "derivacion_drm" / "domain"

PROHIBIDOS = ("derivacion_drm.adapters", "derivacion_drm.api")


def _imports_de(archivo: Path) -> list[str]:
    arbol = ast.parse(archivo.read_text(encoding="utf-8"))
    nombres: list[str] = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            nombres.extend(a.name for a in nodo.names)
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            nombres.append(nodo.module)
    return nombres


@pytest.mark.parametrize(
    "py_file",
    [p for p in DOMAIN.rglob("*.py") if p.name != "__init__.py"],
    ids=lambda p: str(p.relative_to(DOMAIN)),
)
def test_domain_no_importa_capas_superiores(py_file: Path):
    for nombre in _imports_de(py_file):
        for prohibido in PROHIBIDOS:
            assert not nombre.startswith(prohibido), (
                f"{py_file.relative_to(DOMAIN)} importa de capa superior: {nombre}"
            )
