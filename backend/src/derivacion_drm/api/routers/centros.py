from fastapi import APIRouter, Depends

from derivacion_drm.api.deps import get_catalogo
from derivacion_drm.api.schemas import ResolverCentroRequest
from derivacion_drm.domain.centros import (
    CENTROS_IP_IRC, CatalogoOferta, resolver_centro_estandar,
)
from derivacion_drm.domain.models import CentroAsignado, CentroIPIRC

router = APIRouter(prefix="/api/centros", tags=["centros"])


@router.post("/resolver", response_model=list[CentroAsignado])
def resolver(
    req: ResolverCentroRequest,
    catalogo: CatalogoOferta = Depends(get_catalogo),
) -> list[CentroAsignado]:
    return resolver_centro_estandar(req.medida, req.comuna, catalogo)


@router.get("/ip-irc", response_model=dict[CentroIPIRC, CentroAsignado])
def ip_irc() -> dict[CentroIPIRC, CentroAsignado]:
    return CENTROS_IP_IRC
