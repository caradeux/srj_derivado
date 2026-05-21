import tempfile
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from derivacion_drm.adapters.pdf_reader import leer_pdf
from derivacion_drm.adapters.word_reader import leer_docx
from derivacion_drm.domain.models import DocumentoCargado
from derivacion_drm.domain.pipeline import ExtractionResult, ejecutar_pipeline

router = APIRouter(prefix="/api", tags=["extract"])


@router.post("/extract", response_model=ExtractionResult)
async def extract(files: list[UploadFile]) -> ExtractionResult:
    if not files:
        raise HTTPException(400, "Debe enviar al menos un archivo.")
    docs: list[DocumentoCargado] = []
    for f in files:
        name = (f.filename or "").lower()
        if not (name.endswith(".pdf") or name.endswith(".docx")):
            raise HTTPException(400, f"Formato no soportado: {f.filename}")
        contenido = await f.read()
        with tempfile.NamedTemporaryFile(suffix=Path(name).suffix, delete=False) as tmp:
            tmp.write(contenido)
            tmp_path = Path(tmp.name)
        try:
            if name.endswith(".pdf"):
                docs.append(leer_pdf(tmp_path))
            else:
                docs.append(leer_docx(tmp_path))
        finally:
            tmp_path.unlink(missing_ok=True)
    return ejecutar_pipeline(docs)
