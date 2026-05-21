# Arranca backend (con autoreload) y frontend (vite dev) en paralelo.
# Usar con: powershell -ExecutionPolicy Bypass -File scripts/dev.ps1
$repo = Split-Path -Parent $PSScriptRoot

$backend = Start-Process powershell -ArgumentList @(
  "-NoExit", "-Command",
  "Set-Location '$repo\backend'; python -m uvicorn derivacion_drm.main:app --reload --host 127.0.0.1 --port 8000"
) -PassThru

$frontend = Start-Process powershell -ArgumentList @(
  "-NoExit", "-Command",
  "Set-Location '$repo\frontend'; npm run dev"
) -PassThru

Write-Host "Backend PID=$($backend.Id), Frontend PID=$($frontend.Id)"
Write-Host "Abrir http://127.0.0.1:5173 (con proxy a 8000)."
Write-Host "Cerrar ambas ventanas para detener."
