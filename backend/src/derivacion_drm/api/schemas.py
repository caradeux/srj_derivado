from datetime import date

from pydantic import BaseModel

from derivacion_drm.domain.models import (
    Adolescente, AdultoResponsable, CasoDerivacion, CentroAsignado,
    CentroIPIRC, Medida,
)
from derivacion_drm.domain.pipeline import ExtractionResult


# Re-exportes (Pydantic los serializa para OpenAPI automáticamente).
__all__ = [
    "Adolescente", "AdultoResponsable", "CasoDerivacion", "CentroAsignado",
    "CentroIPIRC", "ExtractionResult", "Medida",
    "ResolverCentroRequest", "GenerarDerivacionRequest",
    "MedidaCatalogoItem",
]


class ResolverCentroRequest(BaseModel):
    medida: Medida
    comuna: str


class GenerarDerivacionRequest(BaseModel):
    caso: CasoDerivacion
    profesional: str
    fecha_emision: date


class MedidaCatalogoItem(BaseModel):
    sigla: Medida
    nombre: str
    base_legal: str
    estado: str  # "activa" | "pendiente"
