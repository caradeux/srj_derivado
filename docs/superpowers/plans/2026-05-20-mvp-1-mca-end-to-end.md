# MVP-1 — MCA End-to-End Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first working release of the Sistema de Derivación Virtual reimplementation — FastAPI backend + Vue 3 frontend, supporting the MCA medida end-to-end with full institutional Word output.

**Architecture:** Layered Python backend (`domain` / `adapters` / `api`) served by uvicorn alongside a pre-built Vue 3 SPA. Stateless REST API. Test-driven from the pure-domain layer outward. Reference: `docs/superpowers/specs/2026-05-20-sistema-derivacion-fastapi-vue-design.md`.

**Tech Stack:** Python 3.10+, FastAPI, Pydantic v2, pdfplumber, PyPDF2, python-docx, openpyxl, pandas, pytest, ruff. Frontend: Vue 3, Vite, Pinia, TypeScript, openapi-typescript.

**Scope of MVP-1:** Only MCA (Medida Cautelar Ambulatoria). Other medidas appear in the UI as **disabled** buttons with tooltips. IP/IRC table format, audiencia PII, duración/abonos UI sections are deferred to MVP-2/3.

---

## Phase 1 — Project setup

### Task 1: Initialize repo + .gitignore

**Files:**
- Create: `.gitignore`
- Create: `README.md`

- [ ] **Step 1: Initialize git**

Run: `git init`

- [ ] **Step 2: Write .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
.pytest_cache/
.ruff_cache/
.mypy_cache/

# Node
node_modules/
.npm

# Build artefacts (frontend/dist IS committed; nothing else)
backend/dist/
backend/build/
*.egg

# IDE
.vscode/
.idea/

# OS
Thumbs.db
.DS_Store

# Local data sensitive
data/*.local.*
```

- [ ] **Step 3: Write minimal README**

```markdown
# Sistema de Derivación Virtual — D.R.M.

Reimplementación FastAPI + Vue 3 del Sistema de Derivación Virtual del S.N.R.S.J.

Ver `docs/BRD_Sistema_Derivacion_Virtual.md` para requerimientos y
`docs/superpowers/specs/2026-05-20-sistema-derivacion-fastapi-vue-design.md` para diseño.

## Quick start

Ver `scripts/iniciar_app.bat` (usuario final) y `scripts/dev.ps1` (desarrollo).
```

- [ ] **Step 4: First commit**

```bash
git add .gitignore README.md docs/ CLAUDE.md
git commit -m "chore: initialize repo with BRD, spec, and CLAUDE.md"
```

---

### Task 2: Backend project scaffolding

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/src/derivacion_drm/__init__.py`
- Create: `backend/src/derivacion_drm/domain/__init__.py`
- Create: `backend/src/derivacion_drm/adapters/__init__.py`
- Create: `backend/src/derivacion_drm/api/__init__.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`

- [ ] **Step 1: Write pyproject.toml**

```toml
[project]
name = "derivacion-drm"
version = "0.1.0"
description = "Sistema de Derivación Virtual - D.R.M."
requires-python = ">=3.10"
dependencies = [
  "fastapi>=0.110",
  "uvicorn[standard]>=0.27",
  "pydantic>=2.6",
  "pdfplumber>=0.10",
  "PyPDF2>=3.0",
  "python-docx>=1.1",
  "openpyxl>=3.1",
  "pandas>=2.2",
  "python-multipart>=0.0.9",
]

[project.optional-dependencies]
dev = ["pytest>=8", "httpx>=0.27", "ruff>=0.4"]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "RUF"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

- [ ] **Step 2: Create empty package `__init__.py` files**

All five `__init__.py` files (root + domain + adapters + api + tests) are empty.

- [ ] **Step 3: Write conftest.py**

```python
from pathlib import Path
import pytest

FIXTURES = Path(__file__).parent / "fixtures"

@pytest.fixture
def fixtures_path() -> Path:
    return FIXTURES
```

- [ ] **Step 4: Install in editable mode**

Run: `python -m pip install -e backend[dev]`
Expected: successful install of fastapi, pydantic, pdfplumber, etc.

- [ ] **Step 5: Verify pytest can discover (empty)**

Run: `cd backend && python -m pytest -q`
Expected: `no tests ran` (no error).

- [ ] **Step 6: Commit**

```bash
git add backend/
git commit -m "chore: scaffold backend project structure"
```

---

### Task 3: Frontend project scaffolding

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tsconfig.json`
- Create: `frontend/tsconfig.node.json`
- Create: `frontend/index.html`
- Create: `frontend/src/main.ts`
- Create: `frontend/src/App.vue`

- [ ] **Step 1: Write package.json**

```json
{
  "name": "derivacion-drm-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc --noEmit && vite build",
    "gen": "openapi-typescript http://127.0.0.1:8000/openapi.json -o src/api/types.ts",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "pinia": "^2.1.7"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.3.0",
    "vite": "^5.1.0",
    "vue-tsc": "^2.0.0",
    "openapi-typescript": "^6.7.0"
  }
}
```

- [ ] **Step 2: Write vite.config.ts**

```ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: { '/api': 'http://127.0.0.1:8000' },
  },
  build: { outDir: 'dist', emptyOutDir: true },
})
```

- [ ] **Step 3: Write tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "jsx": "preserve",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

- [ ] **Step 4: Write tsconfig.node.json**

```json
{
  "compilerOptions": {
    "composite": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

- [ ] **Step 5: Write index.html**

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Derivación Virtual — D.R.M.</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

- [ ] **Step 6: Write main.ts + App.vue stub**

`frontend/src/main.ts`:
```ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

createApp(App).use(createPinia()).mount('#app')
```

`frontend/src/App.vue`:
```vue
<template>
  <main><h1>Derivación Virtual</h1></main>
</template>
```

- [ ] **Step 7: Install + verify dev server starts**

```bash
cd frontend
npm install
npm run dev
```
Expected: Vite reports `Local: http://localhost:5173/`. Stop with Ctrl+C.

- [ ] **Step 8: Commit**

```bash
git add frontend/
git commit -m "chore: scaffold Vue 3 + Vite + Pinia frontend"
```

---

## Phase 2 — Domain layer (pure logic, TDD)

### Task 4: Domain models (enums + entities)

**Files:**
- Create: `backend/src/derivacion_drm/domain/models.py`
- Test: `backend/tests/domain/__init__.py` (empty)
- Test: `backend/tests/domain/test_models.py`

- [ ] **Step 1: Write failing test**

`backend/tests/domain/test_models.py`:
```python
import pytest
from pydantic import ValidationError

from derivacion_drm.domain.models import (
    Adolescente, Causa, CasoDerivacion, CentroAsignado,
    Genero, Medida, CentroIPIRC,
)


def test_medida_enum_has_all_siglas():
    assert {m.value for m in Medida} >= {
        "MCA", "SBC", "LAS", "LAE", "LAEIP", "IP", "IRC", "PSA",
        "SALIDAS_ALTERNATIVAS",
    }


def test_centro_ip_irc_enum_has_four():
    assert {c.value for c in CentroIPIRC} == {
        "San_Joaquin", "San_Bernardo", "Til_Til", "Santiago",
    }


def test_adolescente_minimal_valid():
    a = Adolescente(nombre="Juan Pérez", run="12.345.678-9")
    assert a.genero is None and a.comuna is None


def test_causa_default_art_37_bis_false():
    c = Causa()
    assert c.art_37_bis is False


def test_caso_derivacion_requires_centro():
    with pytest.raises(ValidationError):
        CasoDerivacion(
            adolescente=Adolescente(nombre="X", run="1-9"),
            causa=Causa(), medida=Medida.MCA,
        )
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_models.py -v`
Expected: ImportError (module does not exist).

- [ ] **Step 3: Implement models**

`backend/src/derivacion_drm/domain/models.py`:
```python
from datetime import date, time
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


class Medida(StrEnum):
    MCA = "MCA"
    SBC = "SBC"
    LAS = "LAS"
    LAE = "LAE"
    LAEIP = "LAEIP"
    IP = "IP"
    IRC = "IRC"
    PSA = "PSA"
    SALIDAS_ALTERNATIVAS = "SALIDAS_ALTERNATIVAS"


class Genero(StrEnum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


class CentroIPIRC(StrEnum):
    SAN_JOAQUIN = "San_Joaquin"
    SAN_BERNARDO = "San_Bernardo"
    TIL_TIL = "Til_Til"
    SANTIAGO = "Santiago"


class Adolescente(BaseModel):
    nombre: str
    run: str
    genero: Genero | None = None
    domicilio: str | None = None
    comuna: str | None = None


class Causa(BaseModel):
    tribunal: str | None = None
    tipo_resolucion: str | None = None
    ruc: str | None = None
    rit: str | None = None
    delito: str | None = None
    fecha_resolucion: date | None = None
    art_37_bis: bool = False


class AdultoResponsable(BaseModel):
    nombre: str | None = None
    telefono: str | None = None


class AudienciaPII(BaseModel):
    fecha: date
    hora: time = time(11, 0)
    sala: str = "802"
    piso: str = "8°"
    edificio: str = "E"


class CentroAsignado(BaseModel):
    nombre: str
    director: str
    mail: str
    telefono: str
    direccion: str | None = None
    tipo: Literal["Priorizada", "No priorizada"] | None = None


class CasoDerivacion(BaseModel):
    adolescente: Adolescente
    causa: Causa
    medida: Medida
    adulto: AdultoResponsable | None = None
    duracion: str | None = None
    abonos: str | None = None
    audiencia_pii: AudienciaPII | None = None
    observaciones: str | None = None
    centro: CentroAsignado
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_models.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/models.py backend/tests/domain/
git commit -m "feat(domain): add Pydantic v2 entities and enums"
```

---
