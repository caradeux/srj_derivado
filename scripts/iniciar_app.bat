@echo off
REM Lanzador para usuario final.
cd /d "%~dp0..\backend"
start "" http://127.0.0.1:8000
python -m uvicorn derivacion_drm.main:app --host 127.0.0.1 --port 8000
