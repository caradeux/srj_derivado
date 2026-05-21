from pydantic import BaseModel

from derivacion_drm.domain.extractors.adulto import extraer_adulto
from derivacion_drm.domain.extractors.causa import extraer_causa
from derivacion_drm.domain.extractors.medida import extraer_medida
from derivacion_drm.domain.extractors.nombre import extraer_imputados_de_tabla
from derivacion_drm.domain.extractors.ruc import extraer_ruc
from derivacion_drm.domain.genero import inferir_genero
from derivacion_drm.domain.models import (
    Adolescente, AdultoResponsable, Causa, DocumentoCargado, Medida,
)


class ExtractionResult(BaseModel):
    candidatos: list[Adolescente]
    causa: Causa
    adulto: AdultoResponsable
    medida_sugerida: Medida | None
    warnings: list[str] = []


def ejecutar_pipeline(docs: list[DocumentoCargado]) -> ExtractionResult:
    texto_combinado = "\n".join(d.texto for d in docs)
    tablas_combinadas = [t for d in docs for t in d.tablas]
    warnings: list[str] = []

    causa = extraer_causa(texto_combinado)
    medida_sug = extraer_medida(texto_combinado).value
    adulto = extraer_adulto(tablas_combinadas)
    candidatos = extraer_imputados_de_tabla(tablas_combinadas)

    # Inferir género de cada candidato
    candidatos = [
        c.model_copy(update={"genero": inferir_genero(c.nombre.split()[0])
                             if c.nombre else None})
        for c in candidatos
    ]

    # Warnings
    if not candidatos:
        warnings.append("No se detectaron imputados en las tablas; complete manualmente.")
    ruc_field = extraer_ruc(texto_combinado)
    if ruc_field.value and ruc_field.confidence == "low":
        warnings.append("RUC detectado por regex sin etiqueta; verifique antes de generar.")

    return ExtractionResult(
        candidatos=candidatos,
        causa=causa,
        adulto=adulto,
        medida_sugerida=medida_sug,
        warnings=warnings,
    )
