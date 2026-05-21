from fastapi import FastAPI

from derivacion_drm.api.routers import centros, extract


def create_app() -> FastAPI:
    app = FastAPI(title="Sistema de Derivación Virtual", version="0.1.0")
    app.include_router(extract.router)
    app.include_router(centros.router)
    return app
