# Multi-stage build: frontend Vue + backend FastAPI en un único contenedor.
# El backend monta el dist del frontend en / (ver backend/src/derivacion_drm/main.py).

# ========================================================================
# Stage 1 — Build del frontend
# ========================================================================
FROM node:20-alpine AS frontend-builder

WORKDIR /build
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY frontend/ ./
RUN npm run build

# ========================================================================
# Stage 2 — Runtime: Python + uvicorn + dist del frontend
# ========================================================================
FROM python:3.11-slim AS runtime

# pdfplumber/PyPDF2 son puro Python; openpyxl también. No requiere build deps.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Backend: instalar dependencias antes del código para aprovechar cache
COPY backend/pyproject.toml backend/
RUN cd backend && pip install --no-cache-dir -e .

# Código + datos + frontend buildeado
COPY backend/src backend/src
COPY data data
COPY --from=frontend-builder /build/dist frontend/dist

# uvicorn debe correr con cwd=/app/backend para que el editable install resuelva
WORKDIR /app/backend
ENV PYTHONPATH=/app/backend/src

# Healthcheck — uvicorn debe responder en /api/catalogo/medidas (catálogo simple)
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/catalogo/medidas').read()" || exit 1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "derivacion_drm.main:app", "--host", "0.0.0.0", "--port", "8000"]
