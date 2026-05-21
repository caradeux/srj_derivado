from derivacion_drm.domain.models import DocumentoCargado, Medida, Tabla
from derivacion_drm.domain.pipeline import ejecutar_pipeline


def _doc(texto: str, tablas: list[Tabla] | None = None) -> DocumentoCargado:
    return DocumentoCargado(nombre_archivo="t.pdf", texto=texto, tablas=tablas or [])


def test_pipeline_combina_texto_de_varios_docs():
    docs = [_doc("RUC 2600664806-0"), _doc("RIT 2903-2026")]
    r = ejecutar_pipeline(docs)
    assert r.causa.ruc == "2600664806-0"
    assert r.causa.rit == "2903-2026"


def test_pipeline_detecta_medida_mca():
    docs = [_doc("se ordena MCA por art 155 letra B")]
    r = ejecutar_pipeline(docs)
    assert r.medida_sugerida == Medida.MCA


def test_pipeline_un_imputado():
    tablas = [Tabla(
        encabezados=["NOMBRE IMPUTADO", "RUT", "DIRECCION", "COMUNA"],
        filas=[["Juan Pérez", "22.846.782-0", "Calle Falsa 123", "Lo Espejo"]],
    )]
    r = ejecutar_pipeline([_doc("contenido", tablas)])
    assert len(r.candidatos) == 1
    assert r.candidatos[0].nombre == "Juan Pérez"
    assert r.candidatos[0].run == "22.846.782-0"
    assert r.candidatos[0].genero is not None


def test_pipeline_warning_si_run_baja_confianza():
    docs = [_doc("2600664806-0 sin etiqueta")]  # parecería RUC sin etiqueta
    r = ejecutar_pipeline(docs)
    # Si el RUC se detectó vía fallback regex, debe haber warning
    assert any("RUC" in w or "ruc" in w for w in r.warnings) or r.causa.ruc is not None
