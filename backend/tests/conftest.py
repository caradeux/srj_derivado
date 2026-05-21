from pathlib import Path
import pytest

FIXTURES = Path(__file__).parent / "fixtures"

@pytest.fixture
def fixtures_path() -> Path:
    return FIXTURES


@pytest.fixture
def sample_pdf_path(tmp_path: Path) -> Path:
    """Genera un PDF mínimo con texto reconocible para los extractors."""
    try:
        from reportlab.pdfgen import canvas
    except ImportError:
        pytest.skip("reportlab no instalado; skipping PDF fixture test")
    p = tmp_path / "sample.pdf"
    c = canvas.Canvas(str(p))
    c.drawString(100, 750, "RUC 2600664806-0 RIT 2903-2026")
    c.drawString(100, 730, "Juan Perez 22.846.782-0 Lo Espejo")
    c.save()
    return p
