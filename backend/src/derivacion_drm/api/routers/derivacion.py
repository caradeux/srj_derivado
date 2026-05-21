from fastapi import APIRouter, Depends
from fastapi.responses import Response

from derivacion_drm.adapters.word_writer import escribir_word
from derivacion_drm.api.deps import get_settings
from derivacion_drm.api.config import Settings
from derivacion_drm.api.schemas import GenerarDerivacionRequest
from derivacion_drm.domain.word_content import componer_documento_estandar

router = APIRouter(prefix="/api/derivacion", tags=["derivacion"])

_DOCX_MIME = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


@router.post("/generar")
def generar(
    req: GenerarDerivacionRequest,
    settings: Settings = Depends(get_settings),
) -> Response:
    spec = componer_documento_estandar(req.caso, req.profesional, req.fecha_emision)
    logo = settings.logo_path if settings.logo_path.exists() else None
    data = escribir_word(spec, logo_path=logo)
    return Response(
        content=data,
        media_type=_DOCX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{spec.filename}"'},
    )
