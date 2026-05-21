"""Punto de entrada para uvicorn.

Ejecutar con: python -m uvicorn derivacion_drm.main:app --host 127.0.0.1 --port 8000
"""
from pathlib import Path

from fastapi.staticfiles import StaticFiles

from derivacion_drm.api.app import create_app

app = create_app()

# Sirve el bundle Vue construido bajo /  (frontend/dist está committed)
_REPO_ROOT = Path(__file__).resolve().parents[3]
_FRONTEND_DIST = _REPO_ROOT / "frontend" / "dist"
if _FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=_FRONTEND_DIST, html=True), name="frontend")
