# Build de release: instala deps, compila frontend, corre tests.
$repo = Split-Path -Parent $PSScriptRoot

Set-Location "$repo\frontend"
if (-not (Test-Path node_modules)) { npm ci }
npm run build
if ($LASTEXITCODE -ne 0) { throw "Build de frontend falló." }

Set-Location "$repo\backend"
python -m pip install -e ".[dev]"
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "Tests del backend fallaron." }

Write-Host "Build OK. frontend/dist actualizado, tests del backend en verde."
