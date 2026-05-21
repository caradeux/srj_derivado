from datetime import date

from derivacion_drm.domain.models import (
    Adolescente, AdultoResponsable, CasoDerivacion, Causa, CentroAsignado,
    Genero, Medida,
)
from derivacion_drm.domain.word_content import componer_documento_estandar


def _caso_base(genero: Genero = Genero.MASCULINO, adulto=None, art_37=False) -> CasoDerivacion:
    return CasoDerivacion(
        adolescente=Adolescente(
            nombre="Juan Manuel Pérez García", run="22.846.782-0",
            genero=genero, domicilio="Calle Falsa 123 Dpto 4",
            comuna="Lo Espejo",
        ),
        causa=Causa(
            tribunal="Unidad Especializada RPA", tipo_resolucion="oficio",
            ruc="2600664806-0", rit="2903-2026",
            delito="robo con violencia",
            fecha_resolucion=date(2026, 5, 10),
            art_37_bis=art_37,
        ),
        medida=Medida.MCA,
        adulto=adulto,
        centro=CentroAsignado(
            nombre="MCA Centro Sur",
            director="Pedro Soto", mail="pedro@x.cl", telefono="22222",
            direccion="Av. Sur 100",
        ),
    )


def _texto_doc(spec) -> str:
    """Concatena todo el texto del WordDocumentSpec para asserts simples."""
    from derivacion_drm.domain.word_spec import ParagraphSpec
    return " ".join(
        r.text for p in spec.paragraphs if isinstance(p, ParagraphSpec)
        for r in p.runs
    )


def test_estandar_genero_masculino_usa_don_domiciliado():
    spec = componer_documento_estandar(_caso_base(Genero.MASCULINO), "Juan Olivares", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "don " in t.lower() and "domiciliado" in t.lower()
    assert "doña " not in t.lower()


def test_estandar_genero_femenino_usa_dona_domiciliada():
    spec = componer_documento_estandar(_caso_base(Genero.FEMENINO), "Juan Olivares", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "doña " in t.lower() and "domiciliada" in t.lower()
    assert " don " not in t.lower()


def test_estandar_sin_adulto_no_emite_parentesis_vacio():
    spec = componer_documento_estandar(_caso_base(adulto=None), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "()" not in t
    assert "adulto responsable" not in t.lower()


def test_estandar_con_adulto_completo():
    a = AdultoResponsable(nombre="Carmen Soto", telefono="+56999999999")
    spec = componer_documento_estandar(_caso_base(adulto=a), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "Carmen Soto" in t
    assert "+56999999999" in t
    assert "adulto responsable" in t.lower()


def test_estandar_con_adulto_solo_nombre():
    a = AdultoResponsable(nombre="Carmen Soto", telefono=None)
    spec = componer_documento_estandar(_caso_base(adulto=a), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "Carmen Soto" in t
    assert "()" not in t


def test_estandar_con_37_bis_incluye_cita_literal():
    spec = componer_documento_estandar(_caso_base(art_37=True), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "Evacúese informe Técnico conforme al artículo 37 bis" in t


def test_estandar_sin_37_bis_no_incluye_cita():
    spec = componer_documento_estandar(_caso_base(art_37=False), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "37 bis" not in t


def test_estandar_nombre_imputado_en_mayusculas():
    spec = componer_documento_estandar(_caso_base(), "X", date(2026, 5, 20))
    # Algún run del párrafo principal debe llevar uppercase=True para el nombre
    from derivacion_drm.domain.word_spec import ParagraphSpec, RunSpec
    runs_upper = [r for p in spec.paragraphs if isinstance(p, ParagraphSpec)
                  for r in p.runs if isinstance(r, RunSpec) and r.uppercase]
    assert any("Juan Manuel Pérez García" in r.text for r in runs_upper)


def test_estandar_filename_compuesto():
    spec = componer_documento_estandar(_caso_base(), "X", date(2026, 5, 20))
    assert spec.filename.endswith(".docx")
    assert "Juan_Manuel_Perez_Garcia_MCA" in spec.filename
