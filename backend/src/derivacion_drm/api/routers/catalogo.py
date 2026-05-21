from fastapi import APIRouter

from derivacion_drm.api.schemas import MedidaCatalogoItem
from derivacion_drm.domain.delitos import DELITOS_COMUNES
from derivacion_drm.domain.models import Medida

router = APIRouter(prefix="/api/catalogo", tags=["catalogo"])


# BRD §12.1 — estado por medida en MVP-1
_ESTADO: dict[Medida, str] = {
    Medida.MCA: "activa",
    Medida.SBC: "pendiente",
    Medida.LAS: "pendiente",
    Medida.LAE: "pendiente",
    Medida.LAEIP: "pendiente",
    Medida.IP: "pendiente",
    Medida.IRC: "pendiente",
    Medida.PSA: "pendiente",
    Medida.SALIDAS_ALTERNATIVAS: "pendiente",
}

_NOMBRE: dict[Medida, str] = {
    Medida.MCA: "Medida Cautelar Ambulatoria",
    Medida.SBC: "Prestación de Servicios en Beneficio de la Comunidad",
    Medida.LAS: "Libertad Asistida Simple",
    Medida.LAE: "Libertad Asistida Especial",
    Medida.LAEIP: "Libertad Asistida Especial con Internación Parcial",
    Medida.IP: "Internación Provisoria",
    Medida.IRC: "Internación en Régimen Cerrado",
    Medida.PSA: "Programa de Salidas Alternativas",
    Medida.SALIDAS_ALTERNATIVAS: "Salidas Alternativas",
}

_BASE_LEGAL: dict[Medida, str] = {
    Medida.MCA: "Art. 155 letra B C.P.P.",
    Medida.SBC: "Ley N° 20.084",
    Medida.LAS: "Art. 13 Ley N° 20.084",
    Medida.LAE: "Art. 14 Ley N° 20.084",
    Medida.LAEIP: "Ley N° 20.084",
    Medida.IP: "Art. 32 Ley N° 20.084",
    Medida.IRC: "Art. 17 Ley N° 20.084",
    Medida.PSA: "Ley N° 20.084",
    Medida.SALIDAS_ALTERNATIVAS: "Art. 237 C.P.P.",
}


@router.get("/medidas", response_model=list[MedidaCatalogoItem])
def medidas() -> list[MedidaCatalogoItem]:
    return [
        MedidaCatalogoItem(
            sigla=m, nombre=_NOMBRE[m],
            base_legal=_BASE_LEGAL[m], estado=_ESTADO[m],
        )
        for m in Medida
    ]


@router.get("/delitos", response_model=list[str])
def delitos() -> list[str]:
    return DELITOS_COMUNES
