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

### Task 5: RUN formatting (pure function)

**Files:**
- Create: `backend/src/derivacion_drm/domain/run_format.py`
- Test: `backend/tests/domain/test_run_format.py`

- [ ] **Step 1: Write failing test**

```python
import pytest
from derivacion_drm.domain.run_format import formatear_run


@pytest.mark.parametrize("entrada,esperado", [
    ("0022846782-0", "22.846.782-0"),
    ("22846782-0", "22.846.782-0"),
    ("22.846.782-0", "22.846.782-0"),
    ("8765432-9", "8.765.432-9"),
    ("8.765.432-9", "8.765.432-9"),
    ("12345678K", "12.345.678-K"),
    ("12345678-k", "12.345.678-K"),
])
def test_formatear_run_canonical(entrada, esperado):
    assert formatear_run(entrada) == esperado


def test_formatear_run_invalido_devuelve_none():
    assert formatear_run("abc") is None
    assert formatear_run("") is None
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_run_format.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
import re

_RUN_RE = re.compile(r"^(\d{1,9})-?([0-9kK])$")


def formatear_run(raw: str | None) -> str | None:
    """Devuelve el RUN en formato XX.XXX.XXX-X, sin ceros iniciales.

    BRD FR-04, RN-03. Acepta entradas con o sin puntos, con o sin guion.
    """
    if not raw:
        return None
    s = raw.strip().replace(".", "").replace(" ", "")
    if "-" not in s and len(s) >= 2:
        s = f"{s[:-1]}-{s[-1]}"
    m = _RUN_RE.match(s)
    if not m:
        return None
    cuerpo, dv = m.group(1), m.group(2).upper()
    cuerpo = cuerpo.lstrip("0") or "0"
    rev = cuerpo[::-1]
    grupos = [rev[i:i+3][::-1] for i in range(0, len(rev), 3)][::-1]
    return f"{'.'.join(grupos)}-{dv}"
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_run_format.py -v`
Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/run_format.py backend/tests/domain/test_run_format.py
git commit -m "feat(domain): RUN canonical formatting (FR-04, RN-03)"
```

---

### Task 6: Comuna normalization

**Files:**
- Create: `backend/src/derivacion_drm/domain/text_normalize.py`
- Test: `backend/tests/domain/test_text_normalize.py`

- [ ] **Step 1: Write failing test**

```python
import pytest
from derivacion_drm.domain.text_normalize import normalizar_comuna, strip_acentos


@pytest.mark.parametrize("entrada,esperado", [
    ("Peñalolén", "penalolen"),
    ("Peñalolen", "penalolen"),
    ("PEÑALOLÉN", "penalolen"),
    ("  Ñuñoa  ", "nunoa"),
    ("La Florida", "la florida"),
    ("San José de Maipo", "san jose de maipo"),
])
def test_normalizar_comuna(entrada, esperado):
    assert normalizar_comuna(entrada) == esperado


def test_strip_acentos_preserva_no_letras():
    assert strip_acentos("María del Carmen") == "Maria del Carmen"
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_text_normalize.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
import unicodedata


def strip_acentos(s: str) -> str:
    """Quita tildes y diéresis; preserva ñ→n."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalizar_comuna(s: str) -> str:
    """Normaliza una comuna para comparación: sin tildes, lowercase, sin espacios extra.

    BRD FR-07: 'Peñalolén' ≡ 'Peñalolen' ≡ 'penalolen'.
    """
    return strip_acentos(s).strip().lower()
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_text_normalize.py -v`
Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/text_normalize.py backend/tests/domain/test_text_normalize.py
git commit -m "feat(domain): text normalization helpers (strip acentos, normalizar comuna)"
```

---

### Task 7: Género inference + nombres femeninos catalog

**Files:**
- Create: `backend/src/derivacion_drm/domain/genero.py`
- Test: `backend/tests/domain/test_genero.py`

- [ ] **Step 1: Write failing test**

```python
import pytest
from derivacion_drm.domain.models import Genero
from derivacion_drm.domain.genero import inferir_genero


@pytest.mark.parametrize("primer_nombre,esperado", [
    ("María", Genero.FEMENINO),
    ("MARIA", Genero.FEMENINO),
    ("Catalina", Genero.FEMENINO),
    ("Javiera", Genero.FEMENINO),
    ("Juan", Genero.MASCULINO),
    ("Cristóbal", Genero.MASCULINO),
    ("Jeyson", Genero.MASCULINO),
])
def test_inferir_genero(primer_nombre, esperado):
    assert inferir_genero(primer_nombre) == esperado


def test_inferir_genero_desconocido_devuelve_none():
    assert inferir_genero("Xyz123") is None


def test_inferir_genero_compuesto_usa_primer_token():
    # "María José" → primer token "María" → FEMENINO
    assert inferir_genero("María José") == Genero.FEMENINO
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_genero.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
from derivacion_drm.domain.models import Genero
from derivacion_drm.domain.text_normalize import strip_acentos

# ~60 nombres femeninos comunes en Chile (BRD FR-06, §13.4)
NOMBRES_FEMENINOS: frozenset[str] = frozenset(strip_acentos(n).lower() for n in {
    "maria", "ana", "catalina", "javiera", "francisca", "constanza", "valentina",
    "camila", "fernanda", "antonia", "florencia", "isidora", "amanda", "agustina",
    "martina", "emilia", "sofia", "trinidad", "rosario", "paz", "monserrat",
    "ignacia", "magdalena", "anais", "anais", "belen", "renata", "alondra",
    "krishna", "scarlett", "scarlet", "millaray", "rayen", "kiara", "kiara",
    "carla", "carolina", "patricia", "paola", "andrea", "claudia", "veronica",
    "marcela", "lorena", "natalia", "yasna", "ximena", "soledad", "macarena",
    "barbara", "daniela", "alejandra", "pamela", "tamara", "gabriela", "valeria",
    "denisse", "yemina", "virna", "paula", "yohana", "ivonne", "evelyn",
    "jessica", "jocelyn", "katherine", "michelle", "nicole", "stephanie",
})


def inferir_genero(primer_nombre: str) -> Genero | None:
    """Infiere el género desde el primer nombre.

    BRD FR-06, RN-09. Si el nombre no aparece en el catálogo femenino,
    asume masculino (caso mayoritario); devuelve None solo si la entrada
    está vacía o es claramente no-nombre.
    """
    if not primer_nombre or not primer_nombre.strip():
        return None
    primer_token = primer_nombre.strip().split()[0]
    clave = strip_acentos(primer_token).lower()
    if not clave.isalpha():
        return None
    if clave in NOMBRES_FEMENINOS:
        return Genero.FEMENINO
    return Genero.MASCULINO
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_genero.py -v`
Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/genero.py backend/tests/domain/test_genero.py
git commit -m "feat(domain): género inference with chilean female-names catalog (FR-06)"
```

---

### Task 8: ExtractedField generic + extractors package

**Files:**
- Create: `backend/src/derivacion_drm/domain/extractors/__init__.py`
- Create: `backend/src/derivacion_drm/domain/extractors/base.py`
- Test: `backend/tests/domain/extractors/__init__.py` (empty)
- Test: `backend/tests/domain/extractors/test_base.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.extractors.base import ExtractedField


def test_extracted_field_holds_value_confidence_source():
    f = ExtractedField[str](value="X", confidence="high", source="tabla acta")
    assert f.value == "X" and f.confidence == "high" and f.source == "tabla acta"


def test_extracted_field_none_value_low_confidence():
    f = ExtractedField[str](value=None, confidence="low", source="no encontrado")
    assert f.value is None
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/extractors/test_base.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

`backend/src/derivacion_drm/domain/extractors/__init__.py`: empty.

`backend/src/derivacion_drm/domain/extractors/base.py`:
```python
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ExtractedField(BaseModel, Generic[T]):
    """Resultado de un extractor: valor + confianza + procedencia.

    `source` permite que la UI señale al profesional cuando un campo viene
    del fallback regex en lugar de la lectura por tablas (BRD NFR-06).
    """
    value: T | None
    confidence: Literal["high", "low"]
    source: str
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/extractors/test_base.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/extractors/ backend/tests/domain/extractors/
git commit -m "feat(domain): ExtractedField generic for extractor results"
```

---

### Task 9: Tabla model + DocumentoCargado

**Files:**
- Modify: `backend/src/derivacion_drm/domain/models.py` (add Tabla, DocumentoCargado)
- Test: `backend/tests/domain/test_models.py` (add 2 tests)

- [ ] **Step 1: Append failing test to test_models.py**

```python
def test_tabla_has_encabezados_and_filas():
    from derivacion_drm.domain.models import Tabla
    t = Tabla(encabezados=["A", "B"], filas=[["1", "2"], ["3", "4"]])
    assert t.encabezados == ["A", "B"]
    assert t.filas[1][0] == "3"


def test_documento_cargado_carries_text_and_tablas():
    from derivacion_drm.domain.models import DocumentoCargado, Tabla
    d = DocumentoCargado(
        nombre_archivo="acta.pdf",
        texto="contenido",
        tablas=[Tabla(encabezados=["X"], filas=[["y"]])],
    )
    assert d.nombre_archivo == "acta.pdf"
    assert len(d.tablas) == 1
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_models.py -v`
Expected: ImportError on Tabla / DocumentoCargado.

- [ ] **Step 3: Append to models.py**

```python
class Tabla(BaseModel):
    """Representación neutral de una tabla extraída de PDF o DOCX.

    Los adaptadores convierten desde pdfplumber.Table / docx.table.Table a esto.
    """
    encabezados: list[str]
    filas: list[list[str]]


class DocumentoCargado(BaseModel):
    """Documento ya parseado por un adaptador, listo para el pipeline domain."""
    nombre_archivo: str
    texto: str
    tablas: list[Tabla] = []
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_models.py -v`
Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/models.py backend/tests/domain/test_models.py
git commit -m "feat(domain): add Tabla and DocumentoCargado models"
```

---

### Task 10: Extractor — RUC

**Files:**
- Create: `backend/src/derivacion_drm/domain/extractors/ruc.py`
- Test: `backend/tests/domain/extractors/test_ruc.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.extractors.ruc import extraer_ruc


def test_ruc_con_etiqueta_alta_confianza():
    texto = "RUC 2600664806-0 RIT 2903-2026"
    r = extraer_ruc(texto)
    assert r.value == "2600664806-0"
    assert r.confidence == "high"


def test_ruc_sin_etiqueta_baja_confianza():
    texto = "Aparece el número 2600664806-0 en algún lado"
    r = extraer_ruc(texto)
    assert r.value == "2600664806-0"
    assert r.confidence == "low"


def test_ruc_no_encontrado():
    r = extraer_ruc("texto sin números válidos")
    assert r.value is None
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/extractors/test_ruc.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
import re

from derivacion_drm.domain.extractors.base import ExtractedField

# BRD FR-02: 10-12 dígitos + DV, idealmente precedido por "RUC"
_RUC_CON_ETIQUETA = re.compile(r"RUC[\s:]*?(\d{10,12}-[0-9kK])", re.IGNORECASE)
_RUC_SIN_ETIQUETA = re.compile(r"\b(\d{10,12}-[0-9kK])\b")


def extraer_ruc(texto: str) -> ExtractedField[str]:
    m = _RUC_CON_ETIQUETA.search(texto)
    if m:
        return ExtractedField[str](value=m.group(1), confidence="high", source="etiqueta RUC")
    m = _RUC_SIN_ETIQUETA.search(texto)
    if m:
        return ExtractedField[str](value=m.group(1), confidence="low", source="regex fallback")
    return ExtractedField[str](value=None, confidence="low", source="no encontrado")
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/extractors/test_ruc.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/extractors/ruc.py backend/tests/domain/extractors/test_ruc.py
git commit -m "feat(extractors): RUC detection with label priority (FR-02)"
```

---

### Task 11: Extractor — RIT

**Files:**
- Create: `backend/src/derivacion_drm/domain/extractors/rit.py`
- Test: `backend/tests/domain/extractors/test_rit.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.extractors.rit import extraer_rit


def test_rit_con_etiqueta():
    r = extraer_rit("RUC 2600664806-0 RIT 2903-2026")
    assert r.value == "2903-2026"
    assert r.confidence == "high"


def test_rit_descarta_fechas():
    # "10-2026" tiene formato de RIT pero no está precedido por RIT — NO debe matchear
    # sin etiqueta. La etiqueta es lo que distingue de "DD-AAAA" en fechas truncadas.
    r = extraer_rit("Documento fechado 10-2026 sin más contexto")
    assert r.value is None or r.confidence == "low"


def test_rit_no_encontrado():
    assert extraer_rit("texto vacío").value is None
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/extractors/test_rit.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
import re

from derivacion_drm.domain.extractors.base import ExtractedField

# BRD FR-03: número-año, idealmente precedido por "RIT" para evitar confusión con fechas
_RIT_CON_ETIQUETA = re.compile(r"RIT[\s:]*?(\d{1,6}-\d{4})", re.IGNORECASE)


def extraer_rit(texto: str) -> ExtractedField[str]:
    m = _RIT_CON_ETIQUETA.search(texto)
    if m:
        return ExtractedField[str](value=m.group(1), confidence="high", source="etiqueta RIT")
    return ExtractedField[str](value=None, confidence="low", source="no encontrado")
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/extractors/test_rit.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/extractors/rit.py backend/tests/domain/extractors/test_rit.py
git commit -m "feat(extractors): RIT detection requires label to avoid date confusion (FR-03)"
```

---

### Task 12: Extractor — art 37 bis

**Files:**
- Create: `backend/src/derivacion_drm/domain/extractors/art_37_bis.py`
- Test: `backend/tests/domain/extractors/test_art_37_bis.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.extractors.art_37_bis import detectar_art_37_bis


def test_detecta_mencion_directa():
    assert detectar_art_37_bis("conforme al artículo 37 bis se solicita...") is True


def test_detecta_variantes():
    assert detectar_art_37_bis("Art. 37 Bis Ley N° 20.084") is True
    assert detectar_art_37_bis("artículo 37bis") is True


def test_no_detecta_si_ausente():
    assert detectar_art_37_bis("texto sin mención del artículo") is False
    assert detectar_art_37_bis("artículo 37") is False
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/extractors/test_art_37_bis.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
import re

# BRD FR-10: detecta "37 bis" en cualquier variante
_ART_37_BIS = re.compile(r"\b37\s*bis\b", re.IGNORECASE)


def detectar_art_37_bis(texto: str) -> bool:
    return bool(_ART_37_BIS.search(texto))
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/extractors/test_art_37_bis.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/extractors/art_37_bis.py backend/tests/domain/extractors/test_art_37_bis.py
git commit -m "feat(extractors): detect article 37 bis mentions (FR-10)"
```

---

### Task 13: Extractor — Medida via sinónimos

**Files:**
- Create: `backend/src/derivacion_drm/domain/sinonimos.py`
- Create: `backend/src/derivacion_drm/domain/extractors/medida.py`
- Test: `backend/tests/domain/extractors/test_medida.py`

- [ ] **Step 1: Write failing test**

```python
import pytest
from derivacion_drm.domain.models import Medida
from derivacion_drm.domain.extractors.medida import extraer_medida


@pytest.mark.parametrize("texto,esperada", [
    ("se ordena MCA conforme al 155 letra B", Medida.MCA),
    ("la medida cautelar ambulatoria ordenada", Medida.MCA),
    ("dicta sentencia a Libertad Asistida Simple", Medida.LAS),
    ("libertad asistida especial con internación parcial", Medida.LAEIP),
    ("internación provisoria del adolescente", Medida.IP),
    ("régimen cerrado por 3 años", Medida.IRC),
    ("suspensión condicional del procedimiento", Medida.SALIDAS_ALTERNATIVAS),
])
def test_extraer_medida_por_sinonimos(texto, esperada):
    r = extraer_medida(texto)
    assert r.value == esperada


def test_extraer_medida_no_detectada():
    assert extraer_medida("texto sin medidas").value is None


def test_laeip_no_confunde_con_lae():
    # "LAEIP" debe ganar a "LAE" — orden de búsqueda por especificidad
    r = extraer_medida("se ordena LAEIP por 2 años")
    assert r.value == Medida.LAEIP
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/extractors/test_medida.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement sinonimos.py**

```python
from derivacion_drm.domain.models import Medida

# BRD §13.3. Orden de listas: el primero (sigla) suele ser el match más específico,
# pero el orden de iteración por medida importa: LAEIP antes que LAE para evitar
# que el regex de LAE consuma "LAE" dentro de "LAEIP".
SINONIMOS_MEDIDA: dict[Medida, list[str]] = {
    Medida.LAEIP: ["laeip", "lae-ip", "libertad asistida especial con internación parcial",
                   "libertad asistida especial con internacion parcial"],
    Medida.LAE:   ["lae", "libertad asistida especial"],
    Medida.LAS:   ["las", "libertad asistida simple", "l.a.s"],
    Medida.MCA:   ["mca", "medida cautelar ambulatoria", "sujeción a la vigilancia",
                   "sujecion a la vigilancia", "155 letra b"],
    Medida.SBC:   ["sbc", "servicios en beneficio", "prestación de servicios",
                   "prestacion de servicios"],
    Medida.IP:    ["internación provisoria", "internacion provisoria", " ip "],
    Medida.IRC:   ["irc", "crc", "régimen cerrado", "regimen cerrado", "centro cerrado"],
    Medida.SALIDAS_ALTERNATIVAS: ["salidas alternativas", "suspensión condicional",
                                  "suspension condicional", "art. 237", "artículo 237"],
    Medida.PSA:   ["psa", "programa de salidas alternativas"],
}


# Orden de evaluación: más específico primero
ORDEN_MEDIDAS: list[Medida] = [
    Medida.LAEIP, Medida.LAE, Medida.LAS,
    Medida.MCA, Medida.SBC,
    Medida.IRC, Medida.IP,
    Medida.SALIDAS_ALTERNATIVAS, Medida.PSA,
]
```

- [ ] **Step 4: Implement extractors/medida.py**

```python
from derivacion_drm.domain.extractors.base import ExtractedField
from derivacion_drm.domain.models import Medida
from derivacion_drm.domain.sinonimos import ORDEN_MEDIDAS, SINONIMOS_MEDIDA
from derivacion_drm.domain.text_normalize import strip_acentos


def extraer_medida(texto: str) -> ExtractedField[Medida]:
    norm = strip_acentos(texto).lower()
    for medida in ORDEN_MEDIDAS:
        for syn in SINONIMOS_MEDIDA[medida]:
            if strip_acentos(syn).lower() in norm:
                return ExtractedField[Medida](
                    value=medida, confidence="high", source=f"sinónimo: '{syn}'",
                )
    return ExtractedField[Medida](value=None, confidence="low", source="no encontrada")
```

- [ ] **Step 5: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/extractors/test_medida.py -v`
Expected: 9 passed.

- [ ] **Step 6: Commit**

```bash
git add backend/src/derivacion_drm/domain/sinonimos.py backend/src/derivacion_drm/domain/extractors/medida.py backend/tests/domain/extractors/test_medida.py
git commit -m "feat(extractors): medida detection via synonyms catalog (BRD §13.3)"
```

---

### Task 14: Extractor — Nombre + coimputados + filtro VICTIMA/ADULTO

**Files:**
- Create: `backend/src/derivacion_drm/domain/extractors/nombre.py`
- Test: `backend/tests/domain/extractors/test_nombre.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.extractors.nombre import (
    normalizar_nombre, extraer_imputados_de_tabla,
)
from derivacion_drm.domain.models import Tabla


def test_normalizar_nombre_title_case_conectores_minuscula():
    assert normalizar_nombre("JUAN DE LA CRUZ PÉREZ") == "Juan de la Cruz Pérez"


def test_normalizar_nombre_strip_parentesis_trailing():
    assert normalizar_nombre("Juan Pérez (ip San Bernardo)") == "Juan Pérez"


def test_normalizar_nombre_strip_coma_trailing():
    assert normalizar_nombre("María González, ") == "María González"


def test_normalizar_nombre_colapsa_espacios_y_saltos():
    assert normalizar_nombre("Juan\nManuel  Pérez") == "Juan Manuel Pérez"


def test_extraer_imputados_filtra_victima():
    tablas = [
        Tabla(encabezados=["NOMBRE IMPUTADO", "RUT", "DIRECCION"],
              filas=[["Juan Pérez", "22.846.782-0", "Calle 1"]]),
        Tabla(encabezados=["VICTIMA", "RUT"],
              filas=[["María González", "8.765.432-9"]]),
    ]
    imputados = extraer_imputados_de_tabla(tablas)
    assert len(imputados) == 1
    assert imputados[0].nombre == "Juan Pérez"


def test_extraer_imputados_filtra_adulto_responsable():
    tablas = [
        Tabla(encabezados=["NOMBRE IMPUTADO", "RUT"],
              filas=[["Cristóbal Soto", "20.111.222-3"]]),
        Tabla(encabezados=["ADULTO RESPONSABLE", "TELÉFONO"],
              filas=[["Carmen Soto", "+56999999999"]]),
    ]
    imputados = extraer_imputados_de_tabla(tablas)
    assert len(imputados) == 1
    assert imputados[0].nombre == "Cristóbal Soto"


def test_extraer_coimputados_devuelve_multiples():
    tablas = [
        Tabla(encabezados=["NOMBRE IMPUTADO", "RUT"],
              filas=[
                  ["Juan Pérez", "22.846.782-0"],
                  ["Jeyson Castro", "22.857.912-2"],
                  ["Cristóbal Soto", "20.111.222-3"],
              ]),
    ]
    imputados = extraer_imputados_de_tabla(tablas)
    assert len(imputados) == 3
    assert {i.nombre for i in imputados} == {"Juan Pérez", "Jeyson Castro", "Cristóbal Soto"}
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/extractors/test_nombre.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
import re

from derivacion_drm.domain.models import Adolescente, Tabla
from derivacion_drm.domain.run_format import formatear_run
from derivacion_drm.domain.text_normalize import strip_acentos

CONECTORES = {"de", "del", "la", "las", "los", "y", "da", "el"}

# BRD RN-01: tablas con estos encabezados NO contienen al imputado
_ENCABEZADOS_NO_IMPUTADO = {"VICTIMA", "ADULTO RESPONSABLE"}


def normalizar_nombre(raw: str) -> str:
    """Title Case con conectores en minúscula; quita paréntesis y comas trailing.

    BRD FR-05: 'Juan Pérez (ip San Bernardo)' → 'Juan Pérez'.
    """
    s = re.sub(r"\s*\([^)]*\)\s*$", "", raw)        # quita paréntesis trailing
    s = re.sub(r",\s*$", "", s).strip()              # quita coma trailing
    s = re.sub(r"\s+", " ", s)                       # colapsa whitespace
    tokens = []
    for i, tok in enumerate(s.split()):
        low = tok.lower()
        if i > 0 and low in CONECTORES:
            tokens.append(low)
        else:
            tokens.append(tok.capitalize())
    return " ".join(tokens)


def _es_tabla_de_imputados(tabla: Tabla) -> bool:
    enc_norm = {strip_acentos(e).upper().strip() for e in tabla.encabezados}
    if any(e in enc_norm for e in _ENCABEZADOS_NO_IMPUTADO):
        return False
    # Acepta encabezados típicos del Acta de Audiencia
    return any("IMPUTADO" in e or "NOMBRE" in e for e in enc_norm)


def _indices(tabla: Tabla) -> dict[str, int]:
    out = {}
    for i, enc in enumerate(tabla.encabezados):
        e = strip_acentos(enc).upper().strip()
        if "NOMBRE" in e or "IMPUTADO" in e:
            out.setdefault("nombre", i)
        if "RUT" in e or "R.U.N" in e or "RUN" in e:
            out.setdefault("run", i)
        if "DIRECC" in e or "DOMICILIO" in e:
            out.setdefault("domicilio", i)
        if "COMUNA" in e:
            out.setdefault("comuna", i)
    return out


def extraer_imputados_de_tabla(tablas: list[Tabla]) -> list[Adolescente]:
    """Devuelve la lista de adolescentes detectados en las tablas de imputados.

    BRD FR-08 (coimputados), RN-01 (filtra víctima y adulto responsable).
    """
    encontrados: list[Adolescente] = []
    for t in tablas:
        if not _es_tabla_de_imputados(t):
            continue
        idx = _indices(t)
        if "nombre" not in idx:
            continue
        for fila in t.filas:
            if idx["nombre"] >= len(fila):
                continue
            nombre_raw = fila[idx["nombre"]]
            if not nombre_raw or not nombre_raw.strip():
                continue
            nombre = normalizar_nombre(nombre_raw)
            run = formatear_run(fila[idx["run"]]) if "run" in idx and idx["run"] < len(fila) else None
            domicilio = fila[idx["domicilio"]].strip() if "domicilio" in idx and idx["domicilio"] < len(fila) else None
            comuna = fila[idx["comuna"]].strip() if "comuna" in idx and idx["comuna"] < len(fila) else None
            encontrados.append(Adolescente(
                nombre=nombre, run=run or "", domicilio=domicilio, comuna=comuna,
            ))
    return encontrados
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/extractors/test_nombre.py -v`
Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/extractors/nombre.py backend/tests/domain/extractors/test_nombre.py
git commit -m "feat(extractors): nombre normalization + imputados from tables, filters víctima/adulto (FR-05, FR-08, RN-01)"
```

---

### Task 15: Extractor — Adulto responsable

**Files:**
- Create: `backend/src/derivacion_drm/domain/extractors/adulto.py`
- Test: `backend/tests/domain/extractors/test_adulto.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.extractors.adulto import extraer_adulto
from derivacion_drm.domain.models import Tabla


def test_extrae_adulto_con_nombre_y_telefono():
    tablas = [
        Tabla(encabezados=["NOMBRE IMPUTADO", "RUT"],
              filas=[["Juan Pérez", "22.846.782-0"]]),
        Tabla(encabezados=["ADULTO RESPONSABLE", "TELÉFONO"],
              filas=[["Carmen Soto", "+56 9 1234 5678"]]),
    ]
    a = extraer_adulto(tablas)
    assert a.nombre == "Carmen Soto"
    assert a.telefono == "+56 9 1234 5678"


def test_sin_tabla_de_adulto_devuelve_vacio():
    tablas = [Tabla(encabezados=["NOMBRE IMPUTADO"], filas=[["Juan"]])]
    a = extraer_adulto(tablas)
    assert a.nombre is None and a.telefono is None


def test_adulto_sin_telefono():
    tablas = [
        Tabla(encabezados=["ADULTO RESPONSABLE"], filas=[["Carmen Soto"]]),
    ]
    a = extraer_adulto(tablas)
    assert a.nombre == "Carmen Soto" and a.telefono is None
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/extractors/test_adulto.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
from derivacion_drm.domain.extractors.nombre import normalizar_nombre
from derivacion_drm.domain.models import AdultoResponsable, Tabla
from derivacion_drm.domain.text_normalize import strip_acentos


def _es_tabla_de_adulto(tabla: Tabla) -> bool:
    enc_norm = {strip_acentos(e).upper().strip() for e in tabla.encabezados}
    return any("ADULTO RESPONSABLE" in e for e in enc_norm)


def _indices(tabla: Tabla) -> dict[str, int]:
    out: dict[str, int] = {}
    for i, enc in enumerate(tabla.encabezados):
        e = strip_acentos(enc).upper().strip()
        if "ADULTO" in e or "NOMBRE" in e:
            out.setdefault("nombre", i)
        if "TELEFONO" in e or "TELÉFONO" in e or "FONO" in e:
            out.setdefault("telefono", i)
    return out


def extraer_adulto(tablas: list[Tabla]) -> AdultoResponsable:
    """Lee la tabla con encabezado 'ADULTO RESPONSABLE' (BRD FR-11)."""
    for t in tablas:
        if not _es_tabla_de_adulto(t):
            continue
        idx = _indices(t)
        if not t.filas:
            continue
        fila = t.filas[0]
        nombre = None
        if "nombre" in idx and idx["nombre"] < len(fila):
            raw = fila[idx["nombre"]]
            nombre = normalizar_nombre(raw) if raw and raw.strip() else None
        telefono = None
        if "telefono" in idx and idx["telefono"] < len(fila):
            t_raw = fila[idx["telefono"]].strip()
            telefono = t_raw or None
        return AdultoResponsable(nombre=nombre, telefono=telefono)
    return AdultoResponsable()
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/extractors/test_adulto.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/extractors/adulto.py backend/tests/domain/extractors/test_adulto.py
git commit -m "feat(extractors): adulto responsable from labeled table (FR-11)"
```

---

### Task 16: Extractor — Causa metadata (tribunal, RUC/RIT, tipo resolución, delito, fecha)

**Files:**
- Create: `backend/src/derivacion_drm/domain/extractors/causa.py`
- Create: `backend/src/derivacion_drm/domain/delitos.py`
- Test: `backend/tests/domain/extractors/test_causa.py`

- [ ] **Step 1: Write failing test**

```python
from datetime import date

from derivacion_drm.domain.extractors.causa import extraer_causa


def test_extrae_tribunal_unidad_especializada():
    c = extraer_causa("Causa ante la Unidad Especializada RPA, Santiago")
    assert c.tribunal is not None and "Unidad Especializada" in c.tribunal


def test_extrae_tribunal_juzgado_garantia():
    c = extraer_causa("4° Juzgado de Garantía de Santiago")
    assert "Juzgado de Garantía" in (c.tribunal or "")


def test_extrae_ruc_rit_via_causa():
    c = extraer_causa("RUC 2600664806-0 RIT 2903-2026 ordena...")
    assert c.ruc == "2600664806-0"
    assert c.rit == "2903-2026"


def test_extrae_tipo_resolucion_oficio():
    c = extraer_causa("Mediante el presente oficio se ordena...")
    assert c.tipo_resolucion is not None and "oficio" in c.tipo_resolucion.lower()


def test_extrae_tipo_resolucion_sentencia():
    c = extraer_causa("se dicta sentencia ejecutoriada en autos")
    assert "sentencia" in (c.tipo_resolucion or "").lower()


def test_extrae_fecha_formato_largo():
    c = extraer_causa("De fecha 10 de mayo de 2026, se ordena...")
    assert c.fecha_resolucion == date(2026, 5, 10)


def test_extrae_fecha_formato_corto():
    c = extraer_causa("Fecha: 10/05/2026")
    assert c.fecha_resolucion == date(2026, 5, 10)


def test_detecta_delito_de_catalogo():
    c = extraer_causa("por el delito de robo con violencia")
    assert c.delito is not None and "robo" in c.delito.lower()


def test_art_37_bis_marcado():
    c = extraer_causa("Evacúese informe Técnico conforme al artículo 37 bis")
    assert c.art_37_bis is True
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/extractors/test_causa.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement delitos.py**

```python
# BRD §13.5: ~50 delitos comunes en causas RPA
DELITOS_COMUNES: list[str] = [
    "robo con violencia", "robo con intimidación", "robo en lugar habitado",
    "robo en lugar no habitado", "robo por sorpresa", "robo con fuerza",
    "hurto", "hurto simple", "hurto agravado",
    "tráfico ilícito de estupefacientes", "microtráfico",
    "porte ilegal de arma", "porte de munición",
    "lesiones graves", "lesiones menos graves", "lesiones leves",
    "abuso sexual", "violación", "estupro",
    "homicidio", "homicidio simple", "homicidio calificado", "femicidio",
    "receptación", "daños", "amenazas",
    "manejo en estado de ebriedad", "conducción en estado de ebriedad",
    "infracción a la ley de drogas",
    "asociación ilícita", "extorsión",
    "violencia intrafamiliar", "desórdenes públicos",
    "incendio", "estafa", "apropiación indebida",
    "encubrimiento", "obstrucción a la justicia",
    "secuestro", "trata de personas",
    "abigeato", "infracción a la ley de armas",
    "infracción a la ley 20.000",
]
```

- [ ] **Step 4: Implement extractors/causa.py**

```python
import re
from datetime import date

from derivacion_drm.domain.delitos import DELITOS_COMUNES
from derivacion_drm.domain.extractors.art_37_bis import detectar_art_37_bis
from derivacion_drm.domain.extractors.ruc import extraer_ruc
from derivacion_drm.domain.extractors.rit import extraer_rit
from derivacion_drm.domain.models import Causa

_MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11,
    "diciembre": 12,
}
_FECHA_LARGA = re.compile(
    r"\b(\d{1,2})\s+de\s+(" + "|".join(_MESES) + r")\s+de\s+(\d{4})\b",
    re.IGNORECASE,
)
_FECHA_CORTA = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")

_TRIBUNALES = [
    re.compile(r"Unidad Especializada\s*R\.?P\.?A\.?", re.IGNORECASE),
    re.compile(r"(\d+°?\s*)?Juzgado de Garantía[^.\n]*", re.IGNORECASE),
    re.compile(r"Tribunal de Juicio Oral en lo Penal[^.\n]*", re.IGNORECASE),
]


def _extraer_tribunal(texto: str) -> str | None:
    for pat in _TRIBUNALES:
        m = pat.search(texto)
        if m:
            return re.sub(r"\s+", " ", m.group(0)).strip().rstrip(",.")
    return None


def _extraer_tipo_resolucion(texto: str) -> str | None:
    t = texto.lower()
    if "sentencia ejecutoriada" in t:
        return "sentencia ejecutoriada"
    if "sentencia" in t:
        return "sentencia"
    if "oficio" in t:
        return "oficio"
    if "resolución" in t or "resolucion" in t:
        return "resolución"
    return None


def _extraer_fecha(texto: str) -> date | None:
    m = _FECHA_LARGA.search(texto)
    if m:
        d, mes_nombre, a = m.groups()
        return date(int(a), _MESES[mes_nombre.lower()], int(d))
    m = _FECHA_CORTA.search(texto)
    if m:
        d, mm, a = m.groups()
        return date(int(a), int(mm), int(d))
    return None


def _extraer_delito(texto: str) -> str | None:
    t = texto.lower()
    for d in DELITOS_COMUNES:
        if d in t:
            return d
    return None


def extraer_causa(texto: str) -> Causa:
    return Causa(
        tribunal=_extraer_tribunal(texto),
        tipo_resolucion=_extraer_tipo_resolucion(texto),
        ruc=extraer_ruc(texto).value,
        rit=extraer_rit(texto).value,
        delito=_extraer_delito(texto),
        fecha_resolucion=_extraer_fecha(texto),
        art_37_bis=detectar_art_37_bis(texto),
    )
```

- [ ] **Step 5: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/extractors/test_causa.py -v`
Expected: 9 passed.

- [ ] **Step 6: Commit**

```bash
git add backend/src/derivacion_drm/domain/delitos.py backend/src/derivacion_drm/domain/extractors/causa.py backend/tests/domain/extractors/test_causa.py
git commit -m "feat(extractors): causa metadata (tribunal, tipo, RUC, RIT, fecha, delito, 37 bis)"
```

---

### Task 17: Pipeline orchestrator + ExtractionResult

**Files:**
- Create: `backend/src/derivacion_drm/domain/pipeline.py`
- Test: `backend/tests/domain/test_pipeline.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.models import DocumentoCargado, Medida, Tabla
from derivacion_drm.domain.pipeline import ejecutar_pipeline


def _doc(texto: str, tablas: list[Tabla] | None = None) -> DocumentoCargado:
    return DocumentoCargado(nombre_archivo="t.pdf", texto=texto, tablas=tablas or [])


def test_pipeline_combina_texto_de_varios_docs():
    docs = [_doc("RUC 2600664806-0"), _doc("RIT 2903-2026")]
    r = ejecutar_pipeline(docs)
    assert r.causa.ruc == "2600664806-0"
    assert r.causa.rit == "2903-2026"


def test_pipeline_detecta_medida_mca():
    docs = [_doc("se ordena MCA por art 155 letra B")]
    r = ejecutar_pipeline(docs)
    assert r.medida_sugerida == Medida.MCA


def test_pipeline_un_imputado():
    tablas = [Tabla(
        encabezados=["NOMBRE IMPUTADO", "RUT", "DIRECCION", "COMUNA"],
        filas=[["Juan Pérez", "22.846.782-0", "Calle Falsa 123", "Lo Espejo"]],
    )]
    r = ejecutar_pipeline([_doc("contenido", tablas)])
    assert len(r.candidatos) == 1
    assert r.candidatos[0].nombre == "Juan Pérez"
    assert r.candidatos[0].run == "22.846.782-0"
    assert r.candidatos[0].genero is not None


def test_pipeline_warning_si_run_baja_confianza():
    docs = [_doc("2600664806-0 sin etiqueta")]  # parecería RUC sin etiqueta
    r = ejecutar_pipeline(docs)
    # Si el RUC se detectó vía fallback regex, debe haber warning
    assert any("RUC" in w or "ruc" in w for w in r.warnings) or r.causa.ruc is not None
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_pipeline.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
from pydantic import BaseModel

from derivacion_drm.domain.extractors.adulto import extraer_adulto
from derivacion_drm.domain.extractors.causa import extraer_causa
from derivacion_drm.domain.extractors.medida import extraer_medida
from derivacion_drm.domain.extractors.nombre import extraer_imputados_de_tabla
from derivacion_drm.domain.extractors.ruc import extraer_ruc
from derivacion_drm.domain.genero import inferir_genero
from derivacion_drm.domain.models import (
    Adolescente, AdultoResponsable, Causa, DocumentoCargado, Medida,
)


class ExtractionResult(BaseModel):
    candidatos: list[Adolescente]
    causa: Causa
    adulto: AdultoResponsable
    medida_sugerida: Medida | None
    warnings: list[str] = []


def ejecutar_pipeline(docs: list[DocumentoCargado]) -> ExtractionResult:
    texto_combinado = "\n".join(d.texto for d in docs)
    tablas_combinadas = [t for d in docs for t in d.tablas]
    warnings: list[str] = []

    causa = extraer_causa(texto_combinado)
    medida_sug = extraer_medida(texto_combinado).value
    adulto = extraer_adulto(tablas_combinadas)
    candidatos = extraer_imputados_de_tabla(tablas_combinadas)

    # Inferir género de cada candidato
    candidatos = [
        c.model_copy(update={"genero": inferir_genero(c.nombre.split()[0])
                             if c.nombre else None})
        for c in candidatos
    ]

    # Warnings
    if not candidatos:
        warnings.append("No se detectaron imputados en las tablas; complete manualmente.")
    ruc_field = extraer_ruc(texto_combinado)
    if ruc_field.value and ruc_field.confidence == "low":
        warnings.append("RUC detectado por regex sin etiqueta; verifique antes de generar.")

    return ExtractionResult(
        candidatos=candidatos,
        causa=causa,
        adulto=adulto,
        medida_sugerida=medida_sug,
        warnings=warnings,
    )
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_pipeline.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/pipeline.py backend/tests/domain/test_pipeline.py
git commit -m "feat(domain): pipeline orchestrator combines extractors into ExtractionResult"
```

---

### Task 18: Centros — CatalogoOferta + resolver + IP/IRC constants

**Files:**
- Create: `backend/src/derivacion_drm/domain/centros.py`
- Test: `backend/tests/domain/test_centros.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.centros import (
    CENTROS_IP_IRC, CatalogoOferta, EntradaOferta, centro_ip_irc,
    resolver_centro_estandar,
)
from derivacion_drm.domain.models import CentroIPIRC, Medida


def _entrada(programa: str, medida: Medida, priorizadas: str = "", no_prior: str = "") -> EntradaOferta:
    return EntradaOferta(
        programa=programa, medida=medida,
        comunas_priorizadas=[c.strip() for c in priorizadas.split(",") if c.strip()],
        comunas_no_priorizadas=[c.strip() for c in no_prior.split(",") if c.strip()],
        direccion="dir", director="dr", mail="m@x", telefono="111",
    )


def test_resolver_un_centro_por_comuna_priorizada():
    cat = CatalogoOferta(entradas=[
        _entrada("MCA Centro Sur", Medida.MCA, priorizadas="Lo Espejo, La Cisterna"),
    ])
    centros = resolver_centro_estandar(Medida.MCA, "Lo Espejo", cat)
    assert len(centros) == 1
    assert centros[0].nombre == "MCA Centro Sur"
    assert centros[0].tipo == "Priorizada"


def test_resolver_normaliza_tildes_y_caso():
    cat = CatalogoOferta(entradas=[
        _entrada("LAE Peñalolén", Medida.LAE, priorizadas="Peñalolén"),
    ])
    centros = resolver_centro_estandar(Medida.LAE, "PEÑALOLEN", cat)
    assert len(centros) == 1


def test_resolver_dos_centros_si_priorizada_y_no_priorizada():
    cat = CatalogoOferta(entradas=[
        _entrada("Centro A", Medida.LAE, priorizadas="Santiago"),
        _entrada("Centro B", Medida.LAE, no_prior="Santiago"),
    ])
    centros = resolver_centro_estandar(Medida.LAE, "Santiago", cat)
    assert len(centros) == 2


def test_resolver_sin_match_devuelve_lista_vacia():
    cat = CatalogoOferta(entradas=[
        _entrada("Centro X", Medida.MCA, priorizadas="Otra Comuna"),
    ])
    centros = resolver_centro_estandar(Medida.MCA, "Lo Espejo", cat)
    assert centros == []


def test_centros_ip_irc_contiene_4_centros():
    assert set(CENTROS_IP_IRC) == set(CentroIPIRC)


def test_centro_ip_irc_devuelve_san_joaquin():
    c = centro_ip_irc(CentroIPIRC.SAN_JOAQUIN)
    assert "San Joaquín" in c.nombre
    assert c.director == "Virna Salazar"
    assert c.mail == "ingresos.ipircsnjqn@reinsercionjuvenil.cl"
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_centros.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
from pydantic import BaseModel

from derivacion_drm.domain.models import CentroAsignado, CentroIPIRC, Medida
from derivacion_drm.domain.text_normalize import normalizar_comuna


class EntradaOferta(BaseModel):
    """Una fila de CONSOLIDADO_OFERTA_DRM_V2.xlsx hoja 'Desacumulado'."""
    programa: str
    medida: Medida
    comunas_priorizadas: list[str] = []
    comunas_no_priorizadas: list[str] = []
    direccion: str
    director: str
    mail: str
    telefono: str


class CatalogoOferta(BaseModel):
    entradas: list[EntradaOferta]


def resolver_centro_estandar(
    medida: Medida, comuna: str, catalogo: CatalogoOferta,
) -> list[CentroAsignado]:
    """BRD FR-13, RN-04. Devuelve 0, 1 o N centros."""
    c_norm = normalizar_comuna(comuna)
    out: list[CentroAsignado] = []
    for e in catalogo.entradas:
        if e.medida != medida:
            continue
        if any(normalizar_comuna(x) == c_norm for x in e.comunas_priorizadas):
            tipo = "Priorizada"
        elif any(normalizar_comuna(x) == c_norm for x in e.comunas_no_priorizadas):
            tipo = "No priorizada"
        else:
            continue
        out.append(CentroAsignado(
            nombre=e.programa, director=e.director, mail=e.mail,
            telefono=e.telefono, direccion=e.direccion, tipo=tipo,
        ))
    return out


# BRD §13.2 — hardcoded por decisión de mantención (RN-05)
CENTROS_IP_IRC: dict[CentroIPIRC, CentroAsignado] = {
    CentroIPIRC.SAN_JOAQUIN: CentroAsignado(
        nombre="Centro IP - IRC San Joaquín",
        director="Virna Salazar",
        mail="ingresos.ipircsnjqn@reinsercionjuvenil.cl",
        telefono="+56 9 7835 9080",
        direccion="Comuna de San Joaquín, Región Metropolitana",
    ),
    CentroIPIRC.SAN_BERNARDO: CentroAsignado(
        nombre="Centro IP - IRC San Bernardo",
        director="Miguel González Rubio",
        mail="estadisticas.sanbdo@reinsercionjuvenil.cl",
        telefono="22 592 3302",
        direccion="Comuna de San Bernardo, Región Metropolitana",
    ),
    CentroIPIRC.TIL_TIL: CentroAsignado(
        nombre="C.M.N. Til Til",
        director="Eduardo Quevedo",
        mail="estadisticas.tiltil@reinsercionjuvenil.cl",
        telefono="+56 9 5202 9630",
        direccion="Comuna de Til Til, Región Metropolitana",
    ),
    CentroIPIRC.SANTIAGO: CentroAsignado(
        nombre="Centro IP - IRC Santiago",
        director="Paula Alcayaga T.",
        mail="yemina.vargas@reinsercionjuvenil.cl",
        telefono="",
        direccion="Comuna de Santiago, Región Metropolitana",
    ),
}


def centro_ip_irc(opcion: CentroIPIRC) -> CentroAsignado:
    return CENTROS_IP_IRC[opcion]
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_centros.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/centros.py backend/tests/domain/test_centros.py
git commit -m "feat(domain): centro resolver + hardcoded IP/IRC catalog (FR-13, FR-14, RN-04, RN-05)"
```

---

### Task 19: Filename composer

**Files:**
- Create: `backend/src/derivacion_drm/domain/filename.py`
- Test: `backend/tests/domain/test_filename.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.filename import componer_nombre_archivo
from derivacion_drm.domain.models import (
    Adolescente, CasoDerivacion, Causa, CentroAsignado, Medida,
)


def _caso(medida: Medida, centro_nombre: str = "Centro X") -> CasoDerivacion:
    return CasoDerivacion(
        adolescente=Adolescente(nombre="Juan Manuel Pérez García", run="22.846.782-0"),
        causa=Causa(
            tribunal="Unidad Especializada RPA",
            ruc="2600664806-0", rit="2903-2026",
        ),
        medida=medida,
        centro=CentroAsignado(
            nombre=centro_nombre, director="d", mail="m", telefono="t",
        ),
    )


def test_filename_estandar_mca():
    n = componer_nombre_archivo(_caso(Medida.MCA))
    assert n == "Juan_Manuel_Perez_Garcia_MCA_Unidad_Especializada_Rpa_2903-2026_2600664806-0.docx"


def test_filename_irc_incluye_sigla_centro():
    caso = _caso(Medida.IRC, centro_nombre="Centro IP - IRC San Joaquín")
    n = componer_nombre_archivo(caso)
    assert "_IRC_San_Joaquin_" in n


def test_filename_ip_til_til():
    caso = _caso(Medida.IP, centro_nombre="C.M.N. Til Til")
    n = componer_nombre_archivo(caso)
    assert "_IP_Til_Til_" in n


def test_filename_sin_tildes():
    caso = _caso(Medida.MCA)
    caso.adolescente.nombre = "Cristóbal Ñañez"
    n = componer_nombre_archivo(caso)
    assert "Cristobal_Nanez" in n
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_filename.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
import re

from derivacion_drm.domain.models import CasoDerivacion, Medida
from derivacion_drm.domain.text_normalize import strip_acentos

# BRD §14.3 — sigla del centro por nombre canónico
_SIGLA_POR_NOMBRE_CENTRO: dict[str, str] = {
    "san joaquin": "San_Joaquin",
    "san bernardo": "San_Bernardo",
    "til til": "Til_Til",
    "santiago": "Santiago",
}

_MEDIDAS_CON_SIGLA_CENTRO = {Medida.IP, Medida.IRC}


def _ascii_safe(s: str) -> str:
    """Reemplaza no-letras (excepto guion y guion bajo) por guion bajo."""
    s = strip_acentos(s)
    s = re.sub(r"[^A-Za-z0-9_-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def _sigla_centro_ipirc(nombre_centro: str) -> str:
    n = strip_acentos(nombre_centro).lower()
    for clave, sigla in _SIGLA_POR_NOMBRE_CENTRO.items():
        if clave in n:
            return sigla
    return _ascii_safe(nombre_centro)


def _title_case_archivo(s: str) -> str:
    """Capitaliza cada palabra para el nombre de archivo (BRD §14.3)."""
    return " ".join(w.capitalize() for w in s.split())


def componer_nombre_archivo(caso: CasoDerivacion) -> str:
    """BR-04, FR-19, RN-09.

    Estándar: {Nombre}_{Medida}_{Tribunal}_{RIT}_{RUC}.docx
    IP/IRC:   {Nombre}_{Medida}_{Sigla_Centro}_{Tribunal}_{RIT}_{RUC}.docx
    """
    nombre = _ascii_safe(_title_case_archivo(caso.adolescente.nombre))
    medida = caso.medida.value
    tribunal = _ascii_safe(_title_case_archivo(caso.causa.tribunal or "Sin_Tribunal"))
    rit = caso.causa.rit or "Sin_RIT"
    ruc = caso.causa.ruc or "Sin_RUC"

    if caso.medida in _MEDIDAS_CON_SIGLA_CENTRO:
        sigla = _sigla_centro_ipirc(caso.centro.nombre)
        return f"{nombre}_{medida}_{sigla}_{tribunal}_{rit}_{ruc}.docx"
    return f"{nombre}_{medida}_{tribunal}_{rit}_{ruc}.docx"
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_filename.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/filename.py backend/tests/domain/test_filename.py
git commit -m "feat(domain): filename composer with center sigla for IP/IRC (FR-19, RN-09)"
```

---

### Task 20: Word document spec types (data-only IR)

**Files:**
- Create: `backend/src/derivacion_drm/domain/word_spec.py`
- Test: `backend/tests/domain/test_word_spec.py`

- [ ] **Step 1: Write failing test**

```python
from derivacion_drm.domain.word_spec import (
    ParagraphSpec, RunSpec, TableSpec, WordDocumentSpec,
)


def test_run_spec_defaults_plain():
    r = RunSpec(text="hola")
    assert r.bold is False and r.underline is False and r.uppercase is False
    assert r.hyperlink is None


def test_paragraph_spec_default_line_spacing_115():
    p = ParagraphSpec(runs=[RunSpec(text="x")])
    assert p.line_spacing == 1.15
    assert p.alignment == "left"
    assert p.indent_first_line_cm is None


def test_word_document_spec_defaults():
    s = WordDocumentSpec(paragraphs=[], filename="x.docx", incluir_logo=False)
    assert "Pedro De Valdivia" in s.footer_text


def test_table_spec_default_style():
    t = TableSpec(rows=[("A", "1"), ("B", "2")])
    assert t.style == "Table Grid"
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_word_spec.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
from typing import Literal

from pydantic import BaseModel


class RunSpec(BaseModel):
    text: str
    bold: bool = False
    underline: bool = False
    uppercase: bool = False
    hyperlink: str | None = None


class ParagraphSpec(BaseModel):
    runs: list[RunSpec]
    alignment: Literal["left", "center", "right", "justify"] = "left"
    indent_first_line_cm: float | None = None
    line_spacing: float = 1.15


class TableSpec(BaseModel):
    rows: list[tuple[str, str]]
    style: str = "Table Grid"


class WordDocumentSpec(BaseModel):
    paragraphs: list[ParagraphSpec | TableSpec]
    incluir_logo: bool = True
    footer_text: str = "Av. Pedro De Valdivia N° 4070, Ñuñoa.  Fono: 22.3980.04.00"
    filename: str
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_word_spec.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/word_spec.py backend/tests/domain/test_word_spec.py
git commit -m "feat(domain): Pydantic IR for Word document (paragraphs, runs, table, footer)"
```

---

### Task 21: Word content composer — formato estándar

**Files:**
- Create: `backend/src/derivacion_drm/domain/word_content.py`
- Test: `backend/tests/domain/test_word_content.py`

- [ ] **Step 1: Write failing test**

```python
from datetime import date

from derivacion_drm.domain.models import (
    Adolescente, AdultoResponsable, CasoDerivacion, Causa, CentroAsignado,
    Genero, Medida,
)
from derivacion_drm.domain.word_content import componer_documento_estandar


def _caso_base(genero: Genero = Genero.MASCULINO, adulto=None, art_37=False) -> CasoDerivacion:
    return CasoDerivacion(
        adolescente=Adolescente(
            nombre="Juan Manuel Pérez García", run="22.846.782-0",
            genero=genero, domicilio="Calle Falsa 123 Dpto 4",
            comuna="Lo Espejo",
        ),
        causa=Causa(
            tribunal="Unidad Especializada RPA", tipo_resolucion="oficio",
            ruc="2600664806-0", rit="2903-2026",
            delito="robo con violencia",
            fecha_resolucion=date(2026, 5, 10),
            art_37_bis=art_37,
        ),
        medida=Medida.MCA,
        adulto=adulto,
        centro=CentroAsignado(
            nombre="MCA Centro Sur",
            director="Pedro Soto", mail="pedro@x.cl", telefono="22222",
            direccion="Av. Sur 100",
        ),
    )


def _texto_doc(spec) -> str:
    """Concatena todo el texto del WordDocumentSpec para asserts simples."""
    from derivacion_drm.domain.word_spec import ParagraphSpec
    return " ".join(
        r.text for p in spec.paragraphs if isinstance(p, ParagraphSpec)
        for r in p.runs
    )


def test_estandar_genero_masculino_usa_don_domiciliado():
    spec = componer_documento_estandar(_caso_base(Genero.MASCULINO), "Juan Olivares", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "don " in t.lower() and "domiciliado" in t.lower()
    assert "doña " not in t.lower()


def test_estandar_genero_femenino_usa_dona_domiciliada():
    spec = componer_documento_estandar(_caso_base(Genero.FEMENINO), "Juan Olivares", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "doña " in t.lower() and "domiciliada" in t.lower()
    assert " don " not in t.lower()


def test_estandar_sin_adulto_no_emite_parentesis_vacio():
    spec = componer_documento_estandar(_caso_base(adulto=None), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "()" not in t
    assert "adulto responsable" not in t.lower()


def test_estandar_con_adulto_completo():
    a = AdultoResponsable(nombre="Carmen Soto", telefono="+56999999999")
    spec = componer_documento_estandar(_caso_base(adulto=a), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "Carmen Soto" in t
    assert "+56999999999" in t
    assert "adulto responsable" in t.lower()


def test_estandar_con_adulto_solo_nombre():
    a = AdultoResponsable(nombre="Carmen Soto", telefono=None)
    spec = componer_documento_estandar(_caso_base(adulto=a), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "Carmen Soto" in t
    assert "()" not in t


def test_estandar_con_37_bis_incluye_cita_literal():
    spec = componer_documento_estandar(_caso_base(art_37=True), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "Evacúese informe Técnico conforme al artículo 37 bis" in t


def test_estandar_sin_37_bis_no_incluye_cita():
    spec = componer_documento_estandar(_caso_base(art_37=False), "X", date(2026, 5, 20))
    t = _texto_doc(spec)
    assert "37 bis" not in t


def test_estandar_nombre_imputado_en_mayusculas():
    spec = componer_documento_estandar(_caso_base(), "X", date(2026, 5, 20))
    # Algún run del párrafo principal debe llevar uppercase=True para el nombre
    from derivacion_drm.domain.word_spec import ParagraphSpec, RunSpec
    runs_upper = [r for p in spec.paragraphs if isinstance(p, ParagraphSpec)
                  for r in p.runs if isinstance(r, RunSpec) and r.uppercase]
    assert any("Juan Manuel Pérez García" in r.text for r in runs_upper)


def test_estandar_filename_compuesto():
    spec = componer_documento_estandar(_caso_base(), "X", date(2026, 5, 20))
    assert spec.filename.endswith(".docx")
    assert "Juan_Manuel_Perez_Garcia_MCA" in spec.filename
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/domain/test_word_content.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
from datetime import date

from derivacion_drm.domain.filename import componer_nombre_archivo
from derivacion_drm.domain.models import CasoDerivacion, Genero
from derivacion_drm.domain.word_spec import (
    ParagraphSpec, RunSpec, WordDocumentSpec,
)

_MESES_ES = [
    "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def _fecha_larga(d: date) -> str:
    return f"{d.day} de {_MESES_ES[d.month]} de {d.year}"


def _concordancia(g: Genero | None) -> dict[str, str]:
    """BRD RN-06."""
    if g == Genero.FEMENINO:
        return {
            "tratamiento": "doña", "domiciliado": "domiciliada",
            "derivado": "derivada", "individualizado": "individualizada",
            "adulto_responsable": "adulta responsable",
            "el_la_adolescente": "la adolescente",
        }
    return {
        "tratamiento": "don", "domiciliado": "domiciliado",
        "derivado": "derivado", "individualizado": "individualizado",
        "adulto_responsable": "adulto responsable",
        "el_la_adolescente": "el adolescente",
    }


def _parentesis_adulto(caso: CasoDerivacion, c: dict[str, str]) -> str:
    """RN-07: nunca emite paréntesis vacíos."""
    a = caso.adulto
    if not a or (not a.nombre and not a.telefono):
        return ""
    partes = []
    if a.nombre:
        partes.append(f"{c['adulto_responsable']}: {a.nombre}")
    if a.telefono:
        partes.append(f"teléfono {a.telefono}")
    return " (" + ", ".join(partes) + ")"


def _p(*runs: RunSpec,
       alignment: str = "justify",
       indent: float | None = 1.25) -> ParagraphSpec:
    return ParagraphSpec(
        runs=list(runs), alignment=alignment, indent_first_line_cm=indent,
    )


def _r(text: str, **kw) -> RunSpec:
    return RunSpec(text=text, **kw)


def componer_documento_estandar(
    caso: CasoDerivacion, profesional: str, fecha_emision: date,
) -> WordDocumentSpec:
    """BRD FR-17, §14.1. Formato de párrafos para MCA, SBC, LAS, LAE, LAEIP,
    Salidas Alternativas."""
    c = _concordancia(caso.adolescente.genero)
    paragraphs: list[ParagraphSpec] = []

    # Fecha alineada a la derecha
    paragraphs.append(_p(
        _r(f"Santiago, {_fecha_larga(fecha_emision)}"),
        alignment="right", indent=None,
    ))

    # Título centrado, negrita, subrayado
    paragraphs.append(_p(
        _r("CERTIFICA DERIVACIÓN VIRTUAL", bold=True, underline=True),
        alignment="center", indent=None,
    ))
    paragraphs.append(_p(
        _r("SERVICIO NACIONAL DE REINSERCIÓN SOCIAL JUVENIL (S.N.R.S.J.)",
           bold=True, underline=True),
        alignment="center", indent=None,
    ))

    # Párrafo 1 — presentación del imputado
    parents = _parentesis_adulto(caso, c)
    domicilio_txt = (
        f", domiciliad{'a' if c['domiciliado'] == 'domiciliada' else 'o'} en "
        f"{caso.adolescente.domicilio}, comuna de {caso.adolescente.comuna}"
        if caso.adolescente.domicilio else ""
    )
    paragraphs.append(_p(
        _r(f"Por medio del presente certifico que con esta fecha envío los antecedentes de "
           f"{c['tratamiento']} "),
        _r(caso.adolescente.nombre, bold=True, uppercase=True),
        _r(f", run {caso.adolescente.run}{domicilio_txt}{parents}, siendo "
           f"{c['derivado']} en forma no presencial a la Red del S.N.R.S.J. en los "
           f"siguientes términos:"),
    ))

    # Párrafo 2 — solicitud al director
    paragraphs.append(_p(
        _r(f"Señor(a) director(a) Centro "),
        _r(caso.centro.nombre, bold=True),
        _r(f", solicito a usted ingresar a{' la' if c['el_la_adolescente'] == 'la adolescente' else 'l'} "
           f"{c['individualizado']} a vuestro programa para el fin de implementar la medida "
           f"ordenada en {caso.causa.tipo_resolucion or 'resolución'} de fecha "
           f"{_fecha_larga(caso.causa.fecha_resolucion) if caso.causa.fecha_resolucion else 'S/F'} "
           f"por la {caso.causa.tribunal or 'S/T'}, en causa RUC {caso.causa.ruc or 'S/RUC'}, "
           f"RIT {caso.causa.rit or 'S/RIT'}, por el delito de "
           f"{caso.causa.delito or 'S/delito'}."),
    ))

    # Cita 37 bis — FR-10
    if caso.causa.art_37_bis:
        paragraphs.append(_p(
            _r("Cabe señalar que el tribunal solicita expresamente: \""),
            _r("Evacúese informe Técnico conforme al artículo 37 bis", bold=True),
            _r("\", el cual será elaborado por el equipo regional."),
        ))

    # Datos del centro + email hipervinculado
    paragraphs.append(_p(
        _r(f"Se solicita gestionar el ingreso e informar los resultados. Habilitar la casilla "),
        _r(caso.centro.mail, bold=True, underline=True, hyperlink=f"mailto:{caso.centro.mail}"),
        _r(f" para recibir las actas y resoluciones de la causa. El centro tiene su ubicación en "
           f"{caso.centro.direccion or 'S/dirección'}, fono {caso.centro.telefono}."),
    ))

    # Firma centrada (líneas en blanco + nombre + cargo)
    paragraphs.append(_p(_r(""), alignment="center", indent=None))
    paragraphs.append(_p(_r(""), alignment="center", indent=None))
    paragraphs.append(_p(_r(profesional, bold=True), alignment="center", indent=None))
    paragraphs.append(_p(_r("Profesional de Línea"), alignment="center", indent=None))
    paragraphs.append(_p(
        _r("Coordinación Judicial D.R.M. - S.N.R.S.J."),
        alignment="center", indent=None,
    ))

    return WordDocumentSpec(
        paragraphs=paragraphs,
        incluir_logo=True,
        filename=componer_nombre_archivo(caso),
    )
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/domain/test_word_content.py -v`
Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/domain/word_content.py backend/tests/domain/test_word_content.py
git commit -m "feat(domain): word_content composer for standard format (FR-17, RN-06, RN-07, FR-10)"
```

---

## Phase 3 — Adapters (I/O)

### Task 22: Adapter — PDF reader

**Files:**
- Create: `backend/src/derivacion_drm/adapters/__init__.py` (empty)
- Create: `backend/src/derivacion_drm/adapters/pdf_reader.py`
- Test: `backend/tests/adapters/__init__.py` (empty)
- Test: `backend/tests/adapters/test_pdf_reader.py`
- Test fixture: `backend/tests/fixtures/pdfs/sample.pdf` (generated programmatically in conftest)

- [ ] **Step 1: Add fixture generator to conftest**

Append to `backend/tests/conftest.py`:
```python
import io
from pathlib import Path

import pytest


@pytest.fixture
def sample_pdf_path(tmp_path: Path) -> Path:
    """Genera un PDF mínimo con texto reconocible para los extractors."""
    try:
        from reportlab.pdfgen import canvas
    except ImportError:
        pytest.skip("reportlab no instalado; skipping PDF fixture test")
    p = tmp_path / "sample.pdf"
    c = canvas.Canvas(str(p))
    c.drawString(100, 750, "RUC 2600664806-0 RIT 2903-2026")
    c.drawString(100, 730, "Juan Perez 22.846.782-0 Lo Espejo")
    c.save()
    return p
```

- [ ] **Step 2: Write failing test**

```python
from pathlib import Path

from derivacion_drm.adapters.pdf_reader import leer_pdf


def test_leer_pdf_devuelve_documento_cargado(sample_pdf_path: Path):
    doc = leer_pdf(sample_pdf_path)
    assert doc.nombre_archivo == sample_pdf_path.name
    assert "RUC" in doc.texto
    assert "2600664806-0" in doc.texto


def test_leer_pdf_inexistente_lanza(tmp_path: Path):
    import pytest
    with pytest.raises(FileNotFoundError):
        leer_pdf(tmp_path / "no_existe.pdf")
```

- [ ] **Step 3: Run test, expect failure**

Run: `cd backend && python -m pytest tests/adapters/test_pdf_reader.py -v`
Expected: ImportError.

- [ ] **Step 4: Add reportlab to dev deps + install**

Modify `backend/pyproject.toml` `[project.optional-dependencies]`:
```toml
dev = ["pytest>=8", "httpx>=0.27", "ruff>=0.4", "reportlab>=4"]
```

Run: `python -m pip install -e backend[dev]`

- [ ] **Step 5: Implement**

```python
from pathlib import Path

import pdfplumber
from PyPDF2 import PdfReader

from derivacion_drm.domain.models import DocumentoCargado, Tabla


def _tablas_neutralizadas(page_tables: list[list[list[str | None]]]) -> list[Tabla]:
    """Convierte la matriz cruda de pdfplumber a list[Tabla]."""
    out: list[Tabla] = []
    for raw in page_tables:
        if not raw or not raw[0]:
            continue
        encab = [str(c or "").strip() for c in raw[0]]
        filas = [[str(c or "").strip() for c in fila] for fila in raw[1:]]
        out.append(Tabla(encabezados=encab, filas=filas))
    return out


def leer_pdf(path: Path) -> DocumentoCargado:
    """BRD §10.2: pdfplumber primario para preservar tablas, PyPDF2 fallback."""
    if not path.exists():
        raise FileNotFoundError(path)
    texto_partes: list[str] = []
    tablas: list[Tabla] = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                texto_partes.append(t)
                tablas.extend(_tablas_neutralizadas(page.extract_tables() or []))
    except Exception:
        # Fallback PyPDF2
        reader = PdfReader(str(path))
        for page in reader.pages:
            texto_partes.append(page.extract_text() or "")
    return DocumentoCargado(
        nombre_archivo=path.name,
        texto="\n".join(texto_partes),
        tablas=tablas,
    )
```

- [ ] **Step 6: Run test, expect pass**

Run: `cd backend && python -m pytest tests/adapters/test_pdf_reader.py -v`
Expected: 2 passed.

- [ ] **Step 7: Commit**

```bash
git add backend/pyproject.toml backend/src/derivacion_drm/adapters/ backend/tests/adapters/ backend/tests/conftest.py
git commit -m "feat(adapters): PDF reader with pdfplumber primary + PyPDF2 fallback"
```

---

### Task 23: Adapter — DOCX reader

**Files:**
- Create: `backend/src/derivacion_drm/adapters/word_reader.py`
- Test: `backend/tests/adapters/test_word_reader.py`

- [ ] **Step 1: Add docx fixture to conftest**

Append to `backend/tests/conftest.py`:
```python
@pytest.fixture
def sample_docx_path(tmp_path: Path) -> Path:
    from docx import Document
    p = tmp_path / "sample.docx"
    d = Document()
    d.add_paragraph("RUC 2600664806-0 RIT 2903-2026")
    tabla = d.add_table(rows=2, cols=2)
    tabla.cell(0, 0).text = "NOMBRE IMPUTADO"
    tabla.cell(0, 1).text = "RUT"
    tabla.cell(1, 0).text = "Juan Pérez"
    tabla.cell(1, 1).text = "22.846.782-0"
    d.save(str(p))
    return p
```

- [ ] **Step 2: Write failing test**

```python
from pathlib import Path

from derivacion_drm.adapters.word_reader import leer_docx


def test_leer_docx_devuelve_texto_y_tablas(sample_docx_path: Path):
    doc = leer_docx(sample_docx_path)
    assert doc.nombre_archivo == sample_docx_path.name
    assert "RUC" in doc.texto
    assert len(doc.tablas) == 1
    assert doc.tablas[0].encabezados == ["NOMBRE IMPUTADO", "RUT"]
    assert doc.tablas[0].filas == [["Juan Pérez", "22.846.782-0"]]
```

- [ ] **Step 3: Run test, expect failure**

Run: `cd backend && python -m pytest tests/adapters/test_word_reader.py -v`
Expected: ImportError.

- [ ] **Step 4: Implement**

```python
from pathlib import Path

from docx import Document

from derivacion_drm.domain.models import DocumentoCargado, Tabla


def leer_docx(path: Path) -> DocumentoCargado:
    if not path.exists():
        raise FileNotFoundError(path)
    d = Document(str(path))
    texto = "\n".join(p.text for p in d.paragraphs)
    tablas: list[Tabla] = []
    for t in d.tables:
        if not t.rows:
            continue
        encab = [c.text.strip() for c in t.rows[0].cells]
        filas = [[c.text.strip() for c in fila.cells] for fila in t.rows[1:]]
        tablas.append(Tabla(encabezados=encab, filas=filas))
    return DocumentoCargado(nombre_archivo=path.name, texto=texto, tablas=tablas)
```

- [ ] **Step 5: Run test, expect pass**

Run: `cd backend && python -m pytest tests/adapters/test_word_reader.py -v`
Expected: 1 passed.

- [ ] **Step 6: Commit**

```bash
git add backend/src/derivacion_drm/adapters/word_reader.py backend/tests/adapters/test_word_reader.py backend/tests/conftest.py
git commit -m "feat(adapters): DOCX reader via python-docx"
```

---

### Task 24: Adapter — Excel catalog loader

**Files:**
- Create: `backend/src/derivacion_drm/adapters/excel_catalog.py`
- Test: `backend/tests/adapters/test_excel_catalog.py`

- [ ] **Step 1: Add Excel fixture to conftest**

Append to `backend/tests/conftest.py`:
```python
@pytest.fixture
def sample_excel_path(tmp_path: Path) -> Path:
    import pandas as pd
    p = tmp_path / "catalogo.xlsx"
    df = pd.DataFrame({
        "PROGRAMA": ["MCA Centro Sur", "LAE Oriente"],
        "Tipo de medida o sanción": ["MCA", "LAE"],
        "COMUNAS PRIORIZADAS": ["Lo Espejo, La Cisterna", "Peñalolén"],
        "COMUNAS NO PRIORIZADAS": ["", "La Reina, Las Condes"],
        "DIRECCION": ["Av Sur 100", "Av Oriente 200"],
        "DIRECTOR": ["Pedro Soto", "Ana Vidal"],
        "CONTACTO MAIL": ["pedro@x.cl", "ana@y.cl"],
        "TELEFONO": ["22 111", "22 222"],
    })
    with pd.ExcelWriter(p) as w:
        df.to_excel(w, sheet_name="Desacumulado", index=False)
    return p
```

- [ ] **Step 2: Write failing test**

```python
from pathlib import Path

from derivacion_drm.adapters.excel_catalog import cargar_catalogo
from derivacion_drm.domain.models import Medida


def test_cargar_catalogo_lee_dos_filas(sample_excel_path: Path):
    cat = cargar_catalogo(sample_excel_path)
    assert len(cat.entradas) == 2


def test_cargar_catalogo_parsea_comunas_separadas_por_coma(sample_excel_path: Path):
    cat = cargar_catalogo(sample_excel_path)
    mca = next(e for e in cat.entradas if e.medida == Medida.MCA)
    assert mca.comunas_priorizadas == ["Lo Espejo", "La Cisterna"]
    assert mca.comunas_no_priorizadas == []


def test_cargar_catalogo_normaliza_medida_via_sinonimos(sample_excel_path: Path):
    cat = cargar_catalogo(sample_excel_path)
    medidas = {e.medida for e in cat.entradas}
    assert Medida.MCA in medidas and Medida.LAE in medidas
```

- [ ] **Step 3: Run test, expect failure**

Run: `cd backend && python -m pytest tests/adapters/test_excel_catalog.py -v`
Expected: ImportError.

- [ ] **Step 4: Implement**

```python
from pathlib import Path

import pandas as pd

from derivacion_drm.domain.centros import CatalogoOferta, EntradaOferta
from derivacion_drm.domain.models import Medida
from derivacion_drm.domain.sinonimos import SINONIMOS_MEDIDA
from derivacion_drm.domain.text_normalize import strip_acentos


def _identificar_medida(texto: str) -> Medida | None:
    norm = strip_acentos(texto).lower().strip()
    for medida, sinonimos in SINONIMOS_MEDIDA.items():
        for s in sinonimos:
            if strip_acentos(s).lower() == norm:
                return medida
    # fallback: si el texto contiene la sigla exacta
    for medida in Medida:
        if medida.value.lower() == norm:
            return medida
    return None


def _split_comunas(s: str | float | None) -> list[str]:
    if not s or (isinstance(s, float) and pd.isna(s)):
        return []
    return [c.strip() for c in str(s).split(",") if c.strip()]


def cargar_catalogo(path: Path, hoja: str = "Desacumulado") -> CatalogoOferta:
    """Carga CONSOLIDADO_OFERTA_DRM_V2.xlsx hoja Desacumulado (BRD §13.1)."""
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_excel(path, sheet_name=hoja, dtype=str).fillna("")
    entradas: list[EntradaOferta] = []
    for _, fila in df.iterrows():
        medida = _identificar_medida(fila["Tipo de medida o sanción"])
        if medida is None:
            continue
        entradas.append(EntradaOferta(
            programa=str(fila["PROGRAMA"]).strip(),
            medida=medida,
            comunas_priorizadas=_split_comunas(fila["COMUNAS PRIORIZADAS"]),
            comunas_no_priorizadas=_split_comunas(fila["COMUNAS NO PRIORIZADAS"]),
            direccion=str(fila["DIRECCION"]).strip(),
            director=str(fila["DIRECTOR"]).strip(),
            mail=str(fila["CONTACTO MAIL"]).strip(),
            telefono=str(fila["TELEFONO"]).strip(),
        ))
    return CatalogoOferta(entradas=entradas)
```

- [ ] **Step 5: Run test, expect pass**

Run: `cd backend && python -m pytest tests/adapters/test_excel_catalog.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add backend/src/derivacion_drm/adapters/excel_catalog.py backend/tests/adapters/test_excel_catalog.py backend/tests/conftest.py
git commit -m "feat(adapters): Excel catalog loader for CONSOLIDADO_OFERTA_DRM_V2"
```

---

### Task 25: Adapter — Word writer (applies python-docx formatting)

**Files:**
- Create: `backend/src/derivacion_drm/adapters/word_writer.py`
- Test: `backend/tests/adapters/test_word_writer.py`

- [ ] **Step 1: Write failing test**

```python
import io
from pathlib import Path

from docx import Document
from docx.shared import Cm, Pt

from derivacion_drm.adapters.word_writer import escribir_word
from derivacion_drm.domain.word_spec import (
    ParagraphSpec, RunSpec, WordDocumentSpec,
)


def _spec_minimo() -> WordDocumentSpec:
    return WordDocumentSpec(
        paragraphs=[
            ParagraphSpec(
                runs=[RunSpec(text="Hola "), RunSpec(text="MUNDO", bold=True, uppercase=True)],
                alignment="center", indent_first_line_cm=1.25,
            ),
        ],
        incluir_logo=False,
        filename="x.docx",
    )


def test_escribir_word_devuelve_bytes_no_vacios():
    data = escribir_word(_spec_minimo(), logo_path=None)
    assert isinstance(data, bytes) and len(data) > 1000


def test_word_aplica_font_bookman_y_margenes(tmp_path: Path):
    data = escribir_word(_spec_minimo(), logo_path=None)
    out = tmp_path / "out.docx"
    out.write_bytes(data)
    d = Document(str(out))
    # Márgenes 2.5 cm en todos los bordes
    sec = d.sections[0]
    assert abs(sec.top_margin.cm - 2.5) < 0.05
    assert abs(sec.left_margin.cm - 2.5) < 0.05
    assert abs(sec.right_margin.cm - 2.5) < 0.05
    assert abs(sec.bottom_margin.cm - 2.5) < 0.05
    # Font Bookman Old Style 12pt en al menos un run
    fonts = {r.font.name for p in d.paragraphs for r in p.runs if r.font.name}
    assert "Bookman Old Style" in fonts


def test_word_pie_de_pagina_contiene_direccion(tmp_path: Path):
    data = escribir_word(_spec_minimo(), logo_path=None)
    out = tmp_path / "out.docx"
    out.write_bytes(data)
    d = Document(str(out))
    footer_texts = [
        p.text for sec in d.sections for p in sec.footer.paragraphs
    ]
    assert any("Pedro De Valdivia" in t for t in footer_texts)


def test_word_aplica_uppercase_a_runs_marcados(tmp_path: Path):
    data = escribir_word(_spec_minimo(), logo_path=None)
    out = tmp_path / "out.docx"
    out.write_bytes(data)
    d = Document(str(out))
    todos = "".join(p.text for p in d.paragraphs)
    assert "MUNDO" in todos
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/adapters/test_word_writer.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement**

```python
import io
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt, RGBColor

from derivacion_drm.domain.word_spec import (
    ParagraphSpec, RunSpec, TableSpec, WordDocumentSpec,
)

FONT_NAME = "Bookman Old Style"
FONT_SIZE_PT = 12

_ALIGN = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
}


def _aplicar_font(run, *, bold: bool, underline: bool):
    run.font.name = FONT_NAME
    # Asegurar font para Asia / complex scripts también
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts")) or OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT_NAME)
    if rFonts.getparent() is None:
        rPr.append(rFonts)
    run.font.size = Pt(FONT_SIZE_PT)
    run.bold = bold
    run.underline = underline


def _add_hyperlink(paragraph, url: str, run_spec: RunSpec):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    # Estilo: azul + negrita + subrayado
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0000EE")
    rPr.append(color)
    b = OxmlElement("w:b"); rPr.append(b)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    rFonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi"):
        rFonts.set(qn(attr), FONT_NAME)
    rPr.append(rFonts)
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(FONT_SIZE_PT * 2)); rPr.append(sz)
    new_run.append(rPr)
    text = OxmlElement("w:t")
    text.text = run_spec.text.upper() if run_spec.uppercase else run_spec.text
    text.set(qn("xml:space"), "preserve")
    new_run.append(text)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def _aplicar_parrafo(doc, spec: ParagraphSpec):
    p = doc.add_paragraph()
    p.alignment = _ALIGN[spec.alignment]
    pf = p.paragraph_format
    pf.line_spacing = spec.line_spacing
    if spec.indent_first_line_cm is not None:
        pf.first_line_indent = Cm(spec.indent_first_line_cm)
    for r in spec.runs:
        if r.hyperlink:
            _add_hyperlink(p, r.hyperlink, r)
            continue
        texto = r.text.upper() if r.uppercase else r.text
        run = p.add_run(texto)
        _aplicar_font(run, bold=r.bold, underline=r.underline)


def _aplicar_tabla(doc, spec: TableSpec):
    table = doc.add_table(rows=len(spec.rows), cols=2)
    table.style = spec.style
    for i, (etiqueta, valor) in enumerate(spec.rows):
        for j, txt in enumerate((etiqueta, valor)):
            cell = table.rows[i].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(txt)
            _aplicar_font(run, bold=(j == 0), underline=False)


def _setup_documento(doc):
    """Márgenes 2.5cm, default font Bookman 12pt, pie de página."""
    for sec in doc.sections:
        sec.top_margin = Cm(2.5)
        sec.bottom_margin = Cm(2.5)
        sec.left_margin = Cm(2.5)
        sec.right_margin = Cm(2.5)
    style = doc.styles["Normal"]
    style.font.name = FONT_NAME
    style.font.size = Pt(FONT_SIZE_PT)


def _agregar_footer(doc, texto: str):
    for sec in doc.sections:
        footer = sec.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(texto)
        _aplicar_font(run, bold=False, underline=False)


def _agregar_logo(doc, logo_path: Path | None):
    if logo_path is None or not logo_path.exists():
        return
    sec = doc.sections[0]
    header = sec.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(str(logo_path), width=Cm(4))


def escribir_word(spec: WordDocumentSpec, logo_path: Path | None) -> bytes:
    """Aplica formato institucional al WordDocumentSpec y devuelve bytes .docx."""
    doc = Document()
    _setup_documento(doc)
    if spec.incluir_logo:
        _agregar_logo(doc, logo_path)
    for item in spec.paragraphs:
        if isinstance(item, ParagraphSpec):
            _aplicar_parrafo(doc, item)
        elif isinstance(item, TableSpec):
            _aplicar_tabla(doc, item)
    _agregar_footer(doc, spec.footer_text)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()
```

- [ ] **Step 4: Run test, expect pass**

Run: `cd backend && python -m pytest tests/adapters/test_word_writer.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/src/derivacion_drm/adapters/word_writer.py backend/tests/adapters/test_word_writer.py
git commit -m "feat(adapters): word writer with institutional formatting (RN-10, RN-11)"
```

---

## Phase 4 — API layer (FastAPI)

### Task 26: API — schemas + dependencies

**Files:**
- Create: `backend/src/derivacion_drm/api/__init__.py` (empty)
- Create: `backend/src/derivacion_drm/api/schemas.py`
- Create: `backend/src/derivacion_drm/api/deps.py`
- Create: `backend/src/derivacion_drm/api/config.py`
- Test: `backend/tests/api/__init__.py` (empty)
- Test: `backend/tests/api/test_deps.py`

- [ ] **Step 1: Write failing test**

```python
from pathlib import Path

from derivacion_drm.api.config import Settings


def test_settings_default_data_dir(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("DERIVACION_DATA_DIR", str(tmp_path))
    s = Settings()
    assert s.data_dir == tmp_path
    assert s.excel_path == tmp_path / "CONSOLIDADO_OFERTA_DRM_V2.xlsx"
    assert s.logo_path == tmp_path / "logo_snrsj.png"


def test_settings_default_profesional():
    s = Settings()
    # No exigimos un nombre por defecto, pero el campo existe
    assert hasattr(s, "profesional_default")
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/api/test_deps.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement config.py**

```python
import os
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    """Configuración leída de variables de entorno con defaults locales.

    BRD: la planilla y el logo viven junto al proyecto. data_dir resuelve a
    la carpeta `data/` del repo en producción.
    """
    data_dir: Path = Path(os.getenv("DERIVACION_DATA_DIR", "data")).resolve()
    profesional_default: str = os.getenv(
        "DERIVACION_PROFESIONAL_DEFAULT",
        "Juan Manuel Olivares Oyarzún",
    )

    @property
    def excel_path(self) -> Path:
        return self.data_dir / "CONSOLIDADO_OFERTA_DRM_V2.xlsx"

    @property
    def logo_path(self) -> Path:
        return self.data_dir / "logo_snrsj.png"
```

- [ ] **Step 4: Implement deps.py**

```python
from functools import lru_cache

from fastapi import Depends

from derivacion_drm.adapters.excel_catalog import cargar_catalogo
from derivacion_drm.api.config import Settings
from derivacion_drm.domain.centros import CatalogoOferta


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def _catalogo_cache(excel_path_str: str) -> CatalogoOferta:
    from pathlib import Path
    return cargar_catalogo(Path(excel_path_str))


def get_catalogo(
    settings: Settings = Depends(get_settings),
) -> CatalogoOferta:
    """Cargado una vez por ejecución (BRD §10.2). Reiniciar el proceso recarga."""
    return _catalogo_cache(str(settings.excel_path))
```

- [ ] **Step 5: Implement schemas.py**

```python
from datetime import date

from pydantic import BaseModel

from derivacion_drm.domain.models import (
    Adolescente, AdultoResponsable, CasoDerivacion, CentroAsignado,
    CentroIPIRC, Medida,
)
from derivacion_drm.domain.pipeline import ExtractionResult


# Re-exportes (Pydantic los serializa para OpenAPI automáticamente).
__all__ = [
    "Adolescente", "AdultoResponsable", "CasoDerivacion", "CentroAsignado",
    "CentroIPIRC", "ExtractionResult", "Medida",
    "ResolverCentroRequest", "GenerarDerivacionRequest",
    "MedidaCatalogoItem",
]


class ResolverCentroRequest(BaseModel):
    medida: Medida
    comuna: str


class GenerarDerivacionRequest(BaseModel):
    caso: CasoDerivacion
    profesional: str
    fecha_emision: date


class MedidaCatalogoItem(BaseModel):
    sigla: Medida
    nombre: str
    base_legal: str
    estado: str  # "activa" | "pendiente"
```

- [ ] **Step 6: Run test, expect pass**

Run: `cd backend && python -m pytest tests/api/test_deps.py -v`
Expected: 2 passed.

- [ ] **Step 7: Commit**

```bash
git add backend/src/derivacion_drm/api/ backend/tests/api/
git commit -m "feat(api): config settings, DI dependencies, request schemas"
```

---

### Task 27: API router — /api/extract

**Files:**
- Create: `backend/src/derivacion_drm/api/routers/__init__.py` (empty)
- Create: `backend/src/derivacion_drm/api/routers/extract.py`
- Test: `backend/tests/api/test_extract.py`
- Stub for now: `backend/src/derivacion_drm/api/app.py`

- [ ] **Step 1: Write failing test**

```python
import io

from fastapi.testclient import TestClient

from derivacion_drm.api.app import create_app


def _docx_minimo_bytes() -> bytes:
    from docx import Document
    d = Document()
    d.add_paragraph("RUC 2600664806-0 RIT 2903-2026")
    tabla = d.add_table(rows=2, cols=2)
    tabla.cell(0, 0).text = "NOMBRE IMPUTADO"
    tabla.cell(0, 1).text = "RUT"
    tabla.cell(1, 0).text = "Juan Pérez"
    tabla.cell(1, 1).text = "22.846.782-0"
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


def test_extract_docx_devuelve_extraction_result():
    client = TestClient(create_app())
    resp = client.post(
        "/api/extract",
        files=[("files", ("acta.docx", _docx_minimo_bytes(),
                          "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))],
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["causa"]["ruc"] == "2600664806-0"
    assert data["causa"]["rit"] == "2903-2026"
    assert len(data["candidatos"]) == 1
    assert data["candidatos"][0]["nombre"] == "Juan Pérez"


def test_extract_sin_archivos_400():
    client = TestClient(create_app())
    resp = client.post("/api/extract", files=[])
    assert resp.status_code in (400, 422)


def test_extract_archivo_no_soportado():
    client = TestClient(create_app())
    resp = client.post(
        "/api/extract",
        files=[("files", ("nota.txt", b"x", "text/plain"))],
    )
    assert resp.status_code == 400
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/api/test_extract.py -v`
Expected: ImportError on app.

- [ ] **Step 3: Implement extract router**

```python
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
```

- [ ] **Step 4: Implement app.py stub**

```python
from fastapi import FastAPI

from derivacion_drm.api.routers import extract


def create_app() -> FastAPI:
    app = FastAPI(title="Sistema de Derivación Virtual", version="0.1.0")
    app.include_router(extract.router)
    return app
```

- [ ] **Step 5: Run test, expect pass**

Run: `cd backend && python -m pytest tests/api/test_extract.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add backend/src/derivacion_drm/api/routers/ backend/src/derivacion_drm/api/app.py backend/tests/api/test_extract.py
git commit -m "feat(api): /api/extract uploads PDFs and DOCXs, returns ExtractionResult"
```

---

### Task 28: API router — /api/centros (resolver + ip-irc)

**Files:**
- Create: `backend/src/derivacion_drm/api/routers/centros.py`
- Test: `backend/tests/api/test_centros.py`
- Modify: `backend/src/derivacion_drm/api/app.py`

- [ ] **Step 1: Write failing test**

```python
from fastapi.testclient import TestClient

from derivacion_drm.api.app import create_app
from derivacion_drm.api.deps import get_catalogo
from derivacion_drm.domain.centros import CatalogoOferta, EntradaOferta
from derivacion_drm.domain.models import Medida


def _catalogo_test() -> CatalogoOferta:
    return CatalogoOferta(entradas=[
        EntradaOferta(
            programa="MCA Centro Sur", medida=Medida.MCA,
            comunas_priorizadas=["Lo Espejo"], comunas_no_priorizadas=[],
            direccion="Av Sur", director="P", mail="p@x", telefono="1",
        ),
    ])


def _client_con_catalogo() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_catalogo] = _catalogo_test
    return TestClient(app)


def test_resolver_devuelve_un_centro():
    c = _client_con_catalogo()
    r = c.post("/api/centros/resolver", json={"medida": "MCA", "comuna": "Lo Espejo"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "MCA Centro Sur"


def test_resolver_sin_match_devuelve_lista_vacia():
    c = _client_con_catalogo()
    r = c.post("/api/centros/resolver", json={"medida": "MCA", "comuna": "Otra"})
    assert r.status_code == 200
    assert r.json() == []


def test_ip_irc_devuelve_4_centros():
    c = TestClient(create_app())
    r = c.get("/api/centros/ip-irc")
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"San_Joaquin", "San_Bernardo", "Til_Til", "Santiago"}
    assert data["San_Joaquin"]["director"] == "Virna Salazar"
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/api/test_centros.py -v`
Expected: 404 / ImportError.

- [ ] **Step 3: Implement centros router**

```python
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
```

- [ ] **Step 4: Register router in app.py**

Modify `backend/src/derivacion_drm/api/app.py`:
```python
from fastapi import FastAPI

from derivacion_drm.api.routers import centros, extract


def create_app() -> FastAPI:
    app = FastAPI(title="Sistema de Derivación Virtual", version="0.1.0")
    app.include_router(extract.router)
    app.include_router(centros.router)
    return app
```

- [ ] **Step 5: Run test, expect pass**

Run: `cd backend && python -m pytest tests/api/test_centros.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add backend/src/derivacion_drm/api/routers/centros.py backend/src/derivacion_drm/api/app.py backend/tests/api/test_centros.py
git commit -m "feat(api): /api/centros resolver + IP/IRC catalog"
```

---

### Task 29: API router — /api/derivacion/generar

**Files:**
- Create: `backend/src/derivacion_drm/api/routers/derivacion.py`
- Test: `backend/tests/api/test_derivacion.py`
- Modify: `backend/src/derivacion_drm/api/app.py`

- [ ] **Step 1: Write failing test**

```python
from fastapi.testclient import TestClient

from derivacion_drm.api.app import create_app


def _payload_mca() -> dict:
    return {
        "caso": {
            "adolescente": {
                "nombre": "Juan Pérez García", "run": "22.846.782-0",
                "genero": "Masculino", "domicilio": "Calle 1", "comuna": "Lo Espejo",
            },
            "causa": {
                "tribunal": "Unidad Especializada RPA", "tipo_resolucion": "oficio",
                "ruc": "2600664806-0", "rit": "2903-2026",
                "delito": "robo con violencia",
                "fecha_resolucion": "2026-05-10", "art_37_bis": False,
            },
            "medida": "MCA",
            "centro": {
                "nombre": "MCA Centro Sur", "director": "Pedro Soto",
                "mail": "pedro@x.cl", "telefono": "22",
                "direccion": "Av Sur", "tipo": "Priorizada",
            },
        },
        "profesional": "Juan Manuel Olivares Oyarzún",
        "fecha_emision": "2026-05-20",
    }


def test_generar_devuelve_docx_y_filename_correcto():
    c = TestClient(create_app())
    r = c.post("/api/derivacion/generar", json=_payload_mca())
    assert r.status_code == 200
    assert r.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    cd = r.headers["content-disposition"]
    assert "Juan_Perez_Garcia_MCA_Unidad_Especializada_Rpa_2903-2026_2600664806-0.docx" in cd
    assert len(r.content) > 1000


def test_generar_request_invalido_devuelve_422():
    c = TestClient(create_app())
    payload = _payload_mca()
    del payload["caso"]["adolescente"]["nombre"]
    r = c.post("/api/derivacion/generar", json=payload)
    assert r.status_code == 422
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/api/test_derivacion.py -v`
Expected: 404.

- [ ] **Step 3: Implement derivacion router**

```python
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
```

- [ ] **Step 4: Register router**

Modify `backend/src/derivacion_drm/api/app.py`:
```python
from fastapi import FastAPI

from derivacion_drm.api.routers import centros, derivacion, extract


def create_app() -> FastAPI:
    app = FastAPI(title="Sistema de Derivación Virtual", version="0.1.0")
    app.include_router(extract.router)
    app.include_router(centros.router)
    app.include_router(derivacion.router)
    return app
```

- [ ] **Step 5: Run test, expect pass**

Run: `cd backend && python -m pytest tests/api/test_derivacion.py -v`
Expected: 2 passed.

- [ ] **Step 6: Commit**

```bash
git add backend/src/derivacion_drm/api/routers/derivacion.py backend/src/derivacion_drm/api/app.py backend/tests/api/test_derivacion.py
git commit -m "feat(api): /api/derivacion/generar renders Word with filename header (FR-19)"
```

---

### Task 30: API router — /api/catalogo

**Files:**
- Create: `backend/src/derivacion_drm/api/routers/catalogo.py`
- Test: `backend/tests/api/test_catalogo.py`
- Modify: `backend/src/derivacion_drm/api/app.py`

- [ ] **Step 1: Write failing test**

```python
from fastapi.testclient import TestClient

from derivacion_drm.api.app import create_app


def test_catalogo_medidas_incluye_mca_y_pendientes():
    c = TestClient(create_app())
    r = c.get("/api/catalogo/medidas")
    assert r.status_code == 200
    data = r.json()
    siglas = {m["sigla"] for m in data}
    assert "MCA" in siglas and "PSA" in siglas
    psa = next(m for m in data if m["sigla"] == "PSA")
    assert psa["estado"] == "pendiente"
    mca = next(m for m in data if m["sigla"] == "MCA")
    assert mca["estado"] == "activa"


def test_catalogo_delitos_no_vacio():
    c = TestClient(create_app())
    r = c.get("/api/catalogo/delitos")
    assert r.status_code == 200
    delitos = r.json()
    assert len(delitos) >= 30
    assert any("robo" in d for d in delitos)
```

- [ ] **Step 2: Run test, expect failure**

Run: `cd backend && python -m pytest tests/api/test_catalogo.py -v`
Expected: 404.

- [ ] **Step 3: Implement catalogo router**

```python
from fastapi import APIRouter

from derivacion_drm.api.schemas import MedidaCatalogoItem
from derivacion_drm.domain.delitos import DELITOS_COMUNES
from derivacion_drm.domain.models import Medida

router = APIRouter(prefix="/api/catalogo", tags=["catalogo"])


# BRD §12.1 — estado por medida en MVP-1
_ESTADO: dict[Medida, str] = {
    Medida.MCA: "activa",
    Medida.SBC: "pendiente",
    Medida.LAS: "pendiente",
    Medida.LAE: "pendiente",
    Medida.LAEIP: "pendiente",
    Medida.IP: "pendiente",
    Medida.IRC: "pendiente",
    Medida.PSA: "pendiente",
    Medida.SALIDAS_ALTERNATIVAS: "pendiente",
}

_NOMBRE: dict[Medida, str] = {
    Medida.MCA: "Medida Cautelar Ambulatoria",
    Medida.SBC: "Prestación de Servicios en Beneficio de la Comunidad",
    Medida.LAS: "Libertad Asistida Simple",
    Medida.LAE: "Libertad Asistida Especial",
    Medida.LAEIP: "Libertad Asistida Especial con Internación Parcial",
    Medida.IP: "Internación Provisoria",
    Medida.IRC: "Internación en Régimen Cerrado",
    Medida.PSA: "Programa de Salidas Alternativas",
    Medida.SALIDAS_ALTERNATIVAS: "Salidas Alternativas",
}

_BASE_LEGAL: dict[Medida, str] = {
    Medida.MCA: "Art. 155 letra B C.P.P.",
    Medida.SBC: "Ley N° 20.084",
    Medida.LAS: "Art. 13 Ley N° 20.084",
    Medida.LAE: "Art. 14 Ley N° 20.084",
    Medida.LAEIP: "Ley N° 20.084",
    Medida.IP: "Art. 32 Ley N° 20.084",
    Medida.IRC: "Art. 17 Ley N° 20.084",
    Medida.PSA: "Ley N° 20.084",
    Medida.SALIDAS_ALTERNATIVAS: "Art. 237 C.P.P.",
}


@router.get("/medidas", response_model=list[MedidaCatalogoItem])
def medidas() -> list[MedidaCatalogoItem]:
    return [
        MedidaCatalogoItem(
            sigla=m, nombre=_NOMBRE[m],
            base_legal=_BASE_LEGAL[m], estado=_ESTADO[m],
        )
        for m in Medida
    ]


@router.get("/delitos", response_model=list[str])
def delitos() -> list[str]:
    return DELITOS_COMUNES
```

- [ ] **Step 4: Register router**

Modify `backend/src/derivacion_drm/api/app.py`:
```python
from fastapi import FastAPI

from derivacion_drm.api.routers import catalogo, centros, derivacion, extract


def create_app() -> FastAPI:
    app = FastAPI(title="Sistema de Derivación Virtual", version="0.1.0")
    app.include_router(extract.router)
    app.include_router(centros.router)
    app.include_router(derivacion.router)
    app.include_router(catalogo.router)
    return app
```

- [ ] **Step 5: Run test, expect pass**

Run: `cd backend && python -m pytest tests/api/test_catalogo.py -v`
Expected: 2 passed.

- [ ] **Step 6: Commit**

```bash
git add backend/src/derivacion_drm/api/routers/catalogo.py backend/src/derivacion_drm/api/app.py backend/tests/api/test_catalogo.py
git commit -m "feat(api): /api/catalogo for medidas (with estado) and delitos"
```

---

### Task 31: main.py — uvicorn entry + StaticFiles mount

**Files:**
- Create: `backend/src/derivacion_drm/main.py`

- [ ] **Step 1: Implement main.py**

```python
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
```

- [ ] **Step 2: Smoke-test uvicorn startup**

Run (Windows): `cd backend && python -m uvicorn derivacion_drm.main:app --host 127.0.0.1 --port 8765 --no-server-header` then in another terminal `curl http://127.0.0.1:8765/api/catalogo/delitos` and Ctrl-C uvicorn.
Expected: 200 OK with JSON list of delitos.

- [ ] **Step 3: Commit**

```bash
git add backend/src/derivacion_drm/main.py
git commit -m "feat(api): main.py entrypoint with StaticFiles mount for Vue bundle"
```

---

### Task 32: Layering test (enforce domain isolation)

**Files:**
- Test: `backend/tests/test_layering.py`

- [ ] **Step 1: Write the test**

```python
"""Verifica que domain/ no importe de adapters/ ni de api/.

BRD spec §4 — regla de dependencias por capas.
"""
import ast
from pathlib import Path

import pytest

DOMAIN = Path(__file__).resolve().parents[1] / "src" / "derivacion_drm" / "domain"

PROHIBIDOS = ("derivacion_drm.adapters", "derivacion_drm.api")


def _imports_de(archivo: Path) -> list[str]:
    arbol = ast.parse(archivo.read_text(encoding="utf-8"))
    nombres: list[str] = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            nombres.extend(a.name for a in nodo.names)
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            nombres.append(nodo.module)
    return nombres


@pytest.mark.parametrize(
    "py_file",
    [p for p in DOMAIN.rglob("*.py") if p.name != "__init__.py"],
    ids=lambda p: str(p.relative_to(DOMAIN)),
)
def test_domain_no_importa_capas_superiores(py_file: Path):
    for nombre in _imports_de(py_file):
        for prohibido in PROHIBIDOS:
            assert not nombre.startswith(prohibido), (
                f"{py_file.relative_to(DOMAIN)} importa de capa superior: {nombre}"
            )
```

- [ ] **Step 2: Run test, expect pass (capa correcta)**

Run: `cd backend && python -m pytest tests/test_layering.py -v`
Expected: all parametrized cases passed.

- [ ] **Step 3: Run full suite to ensure nothing broke**

Run: `cd backend && python -m pytest -q`
Expected: all tests pass.

- [ ] **Step 4: Commit**

```bash
git add backend/tests/test_layering.py
git commit -m "test: enforce domain/ does not import from adapters/ or api/"
```

---

## Phase 5 — Frontend (Vue 3 + Pinia)

### Task 33: Generate TypeScript types from OpenAPI

**Files:**
- Create: `frontend/src/api/types.ts` (generated)
- Create: `frontend/scripts/generate-types.ps1`

- [ ] **Step 1: Start backend in background and capture OpenAPI**

Run in one terminal:
```powershell
cd backend
python -m uvicorn derivacion_drm.main:app --host 127.0.0.1 --port 8000
```

Run in another:
```powershell
cd frontend
npm run gen
```

Expected: `frontend/src/api/types.ts` is created with types for `Adolescente`, `Causa`, `CasoDerivacion`, `CentroAsignado`, `ExtractionResult`, etc.

Stop uvicorn (Ctrl-C).

- [ ] **Step 2: Write helper script for future regenerations**

`frontend/scripts/generate-types.ps1`:
```powershell
# Regenera src/api/types.ts contra el backend en 127.0.0.1:8000.
# Requiere que el backend esté corriendo en otra ventana.
param([string]$Url = "http://127.0.0.1:8000/openapi.json")
npx openapi-typescript $Url -o src/api/types.ts
```

- [ ] **Step 3: Sanity check the generated file**

Open `frontend/src/api/types.ts` and confirm it exports `components["schemas"]["CasoDerivacion"]` and the endpoint paths.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/api/types.ts frontend/scripts/generate-types.ps1
git commit -m "feat(frontend): generate TS types from FastAPI OpenAPI"
```

---

### Task 34: API client + Pinia stores

**Files:**
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/stores/caso.ts`
- Create: `frontend/src/stores/catalogos.ts`

- [ ] **Step 1: Implement api/client.ts**

```ts
import type { components } from './types'

type Schemas = components['schemas']
export type Adolescente = Schemas['Adolescente']
export type Causa = Schemas['Causa']
export type AdultoResponsable = Schemas['AdultoResponsable']
export type CasoDerivacion = Schemas['CasoDerivacion']
export type CentroAsignado = Schemas['CentroAsignado']
export type ExtractionResult = Schemas['ExtractionResult']
export type Medida = Schemas['Medida']
export type CentroIPIRC = Schemas['CentroIPIRC']
export type MedidaCatalogoItem = Schemas['MedidaCatalogoItem']

class ApiError extends Error {
  constructor(public status: number, message: string, public detail?: unknown) {
    super(message)
  }
}

async function unwrap<T>(r: Response): Promise<T> {
  if (!r.ok) {
    let detail: unknown
    try { detail = await r.json() } catch { /* ignore */ }
    throw new ApiError(r.status, `HTTP ${r.status}`, detail)
  }
  return r.json() as Promise<T>
}

export const api = {
  async extract(files: File[]): Promise<ExtractionResult> {
    const fd = new FormData()
    files.forEach(f => fd.append('files', f))
    return unwrap(await fetch('/api/extract', { method: 'POST', body: fd }))
  },

  async resolverCentro(medida: Medida, comuna: string): Promise<CentroAsignado[]> {
    return unwrap(await fetch('/api/centros/resolver', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ medida, comuna }),
    }))
  },

  async centrosIpIrc(): Promise<Record<CentroIPIRC, CentroAsignado>> {
    return unwrap(await fetch('/api/centros/ip-irc'))
  },

  async medidas(): Promise<MedidaCatalogoItem[]> {
    return unwrap(await fetch('/api/catalogo/medidas'))
  },

  async delitos(): Promise<string[]> {
    return unwrap(await fetch('/api/catalogo/delitos'))
  },

  async generar(payload: {
    caso: CasoDerivacion
    profesional: string
    fecha_emision: string
  }): Promise<{ blob: Blob; filename: string }> {
    const r = await fetch('/api/derivacion/generar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    if (!r.ok) {
      let detail: unknown
      try { detail = await r.json() } catch { /* ignore */ }
      throw new ApiError(r.status, `HTTP ${r.status}`, detail)
    }
    const cd = r.headers.get('content-disposition') ?? ''
    const match = cd.match(/filename="([^"]+)"/)
    const filename = match?.[1] ?? 'derivacion.docx'
    return { blob: await r.blob(), filename }
  },
}

export { ApiError }
```

- [ ] **Step 2: Implement stores/catalogos.ts**

```ts
import { defineStore } from 'pinia'
import { api, type CentroAsignado, type CentroIPIRC, type MedidaCatalogoItem } from '../api/client'

export const useCatalogosStore = defineStore('catalogos', {
  state: () => ({
    medidas: [] as MedidaCatalogoItem[],
    centrosIpIrc: {} as Record<CentroIPIRC, CentroAsignado>,
    delitos: [] as string[],
    cargado: false,
  }),
  actions: {
    async load() {
      if (this.cargado) return
      const [m, c, d] = await Promise.all([
        api.medidas(), api.centrosIpIrc(), api.delitos(),
      ])
      this.medidas = m
      this.centrosIpIrc = c
      this.delitos = d
      this.cargado = true
    },
  },
})
```

- [ ] **Step 3: Implement stores/caso.ts**

```ts
import { defineStore } from 'pinia'
import {
  api, type Adolescente, type AdultoResponsable, type CasoDerivacion,
  type Causa, type CentroAsignado, type ExtractionResult, type Medida,
} from '../api/client'

interface State {
  fechaEmision: string
  profesional: string
  candidatos: Adolescente[]
  adolescente: Adolescente
  causa: Causa
  adulto: AdultoResponsable
  medida: Medida | null
  centrosDisponibles: CentroAsignado[]
  centroSeleccionado: CentroAsignado | null
  warnings: string[]
  generando: boolean
}

const _hoyIso = () => new Date().toISOString().slice(0, 10)

const _adolescenteVacio = (): Adolescente => ({
  nombre: '', run: '', genero: null, domicilio: null, comuna: null,
})

const _causaVacia = (): Causa => ({
  tribunal: null, tipo_resolucion: null, ruc: null, rit: null,
  delito: null, fecha_resolucion: null, art_37_bis: false,
})

export const useCasoStore = defineStore('caso', {
  state: (): State => ({
    fechaEmision: _hoyIso(),
    profesional: 'Juan Manuel Olivares Oyarzún',
    candidatos: [],
    adolescente: _adolescenteVacio(),
    causa: _causaVacia(),
    adulto: { nombre: null, telefono: null },
    medida: null,
    centrosDisponibles: [],
    centroSeleccionado: null,
    warnings: [],
    generando: false,
  }),

  getters: {
    validationErrors(state): string[] {
      const errs: string[] = []
      if (!state.adolescente.nombre) errs.push('Falta nombre del adolescente.')
      if (!state.adolescente.genero) errs.push('Falta género.')
      if (!state.medida) errs.push('Falta medida.')
      const esIpIrc = state.medida === 'IP' || state.medida === 'IRC'
      if (!esIpIrc && !state.adolescente.comuna) errs.push('Falta comuna.')
      if (!state.centroSeleccionado) errs.push('Falta centro.')
      return errs
    },
    listo(): boolean { return this.validationErrors.length === 0 },
  },

  actions: {
    aplicarExtraccion(r: ExtractionResult) {
      this.candidatos = r.candidatos
      this.causa = r.causa
      this.adulto = r.adulto
      this.medida = r.medida_sugerida
      this.warnings = r.warnings
      if (r.candidatos.length === 1) this.adolescente = r.candidatos[0]
    },

    seleccionarCoimputado(idx: number) {
      const c = this.candidatos[idx]
      if (c) this.adolescente = c
    },

    async resolverCentros() {
      if (!this.medida || !this.adolescente.comuna) {
        this.centrosDisponibles = []
        this.centroSeleccionado = null
        return
      }
      const ipIrc = this.medida === 'IP' || this.medida === 'IRC'
      if (ipIrc) return  // IP/IRC se selecciona via dropdown, no por resolver
      const lista = await api.resolverCentro(this.medida, this.adolescente.comuna)
      this.centrosDisponibles = lista
      this.centroSeleccionado = lista.length === 1 ? lista[0] : null
    },

    reset() {
      const fecha = this.fechaEmision
      const prof = this.profesional
      this.$reset()
      this.fechaEmision = fecha
      this.profesional = prof
    },

    async generar(): Promise<{ blob: Blob; filename: string } | null> {
      if (!this.listo) return null
      this.generando = true
      try {
        const payload = {
          caso: {
            adolescente: this.adolescente,
            causa: this.causa,
            medida: this.medida!,
            adulto: this.adulto,
            centro: this.centroSeleccionado!,
          } as CasoDerivacion,
          profesional: this.profesional,
          fecha_emision: this.fechaEmision,
        }
        return await api.generar(payload)
      } finally {
        this.generando = false
      }
    },
  },
})
```

- [ ] **Step 4: Type-check**

Run: `cd frontend && npx vue-tsc --noEmit`
Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/api/client.ts frontend/src/stores/
git commit -m "feat(frontend): API client + Pinia stores (caso, catalogos)"
```

---

### Task 35: Upload components (DropZone + FileCard)

**Files:**
- Create: `frontend/src/components/Upload/DropZone.vue`
- Create: `frontend/src/components/Upload/FileCard.vue`

- [ ] **Step 1: Implement FileCard.vue**

```vue
<script setup lang="ts">
defineProps<{ filename: string; sizeBytes: number }>()
const emit = defineEmits<{ (e: 'remove'): void }>()

function fmt(n: number): string {
  if (n < 1024) return `${n} B`
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(0)} KB`
  return `${(n / 1024 / 1024).toFixed(1)} MB`
}
</script>

<template>
  <div class="file-card">
    <span class="name">{{ filename }}</span>
    <span class="size">{{ fmt(sizeBytes) }}</span>
    <button type="button" @click="emit('remove')" aria-label="Quitar">×</button>
  </div>
</template>

<style scoped>
.file-card {
  display: flex; align-items: center; gap: 8px;
  border: 1px solid #d0d7de; border-radius: 6px;
  padding: 6px 10px; background: #f6f8fa;
  font-size: 0.9rem;
}
.name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.size { color: #57606a; }
button {
  background: none; border: none; cursor: pointer; font-size: 1.2rem; color: #57606a;
}
</style>
```

- [ ] **Step 2: Implement DropZone.vue**

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../../api/client'
import { useCasoStore } from '../../stores/caso'
import FileCard from './FileCard.vue'

const store = useCasoStore()
const archivos = ref<File[]>([])
const procesando = ref(false)
const error = ref<string | null>(null)
const dragOver = ref(false)

const ACEPTADOS = ['.pdf', '.docx']

function _validos(lista: File[]): File[] {
  return lista.filter(f =>
    ACEPTADOS.some(ext => f.name.toLowerCase().endsWith(ext)),
  )
}

function onDrop(e: DragEvent) {
  e.preventDefault()
  dragOver.value = false
  if (!e.dataTransfer) return
  archivos.value = [..._validos(Array.from(e.dataTransfer.files))]
}

function onChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files) return
  archivos.value = [..._validos(Array.from(input.files))]
}

function remove(idx: number) {
  archivos.value.splice(idx, 1)
}

async function procesar() {
  if (archivos.value.length === 0) return
  procesando.value = true
  error.value = null
  try {
    const r = await api.extract(archivos.value)
    store.aplicarExtraccion(r)
    await store.resolverCentros()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al procesar.'
  } finally {
    procesando.value = false
  }
}
</script>

<template>
  <section class="drop-zone-wrap">
    <div
      class="drop-zone"
      :class="{ over: dragOver }"
      @dragover.prevent="dragOver = true"
      @dragleave="dragOver = false"
      @drop="onDrop"
    >
      <p>Arrastre aquí los documentos (PDF o DOCX) o</p>
      <label class="select">
        <input type="file" multiple accept=".pdf,.docx" @change="onChange" />
        seleccionar archivos
      </label>
    </div>

    <div v-if="archivos.length > 0" class="lista">
      <FileCard
        v-for="(f, i) in archivos" :key="f.name + i"
        :filename="f.name" :size-bytes="f.size"
        @remove="remove(i)"
      />
    </div>

    <button
      type="button"
      class="primary"
      :disabled="archivos.length === 0 || procesando"
      @click="procesar"
    >
      {{ procesando ? 'Procesando…' : 'Procesar documentos' }}
    </button>

    <p v-if="error" class="error">{{ error }}</p>
  </section>
</template>

<style scoped>
.drop-zone-wrap { display: flex; flex-direction: column; gap: 12px; }
.drop-zone {
  border: 2px dashed #d0d7de; border-radius: 8px; padding: 24px;
  text-align: center; background: #f6f8fa; transition: background 0.15s;
}
.drop-zone.over { background: #ddf4ff; border-color: #0969da; }
.select { display: inline-block; color: #0969da; cursor: pointer; text-decoration: underline; }
.select input { display: none; }
.lista { display: flex; flex-direction: column; gap: 6px; }
.primary {
  background: #0969da; color: #fff; border: none; border-radius: 6px;
  padding: 10px 16px; font-size: 0.95rem; cursor: pointer;
}
.primary:disabled { opacity: 0.5; cursor: not-allowed; }
.error { color: #cf222e; font-size: 0.9rem; }
</style>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/Upload/
git commit -m "feat(frontend): DropZone + FileCard for document upload (FR-01)"
```

---

### Task 36: Form components (DatosAdolescente, DatosCausa, AdultoResponsable)

**Files:**
- Create: `frontend/src/components/Form/DatosAdolescente.vue`
- Create: `frontend/src/components/Form/DatosCausa.vue`
- Create: `frontend/src/components/Form/AdultoResponsable.vue`

- [ ] **Step 1: Implement DatosAdolescente.vue**

```vue
<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <fieldset>
    <legend>Datos del adolescente</legend>
    <div class="grid">
      <label>Nombre
        <input v-model="s.adolescente.nombre" type="text" />
      </label>
      <label>RUN
        <input v-model="s.adolescente.run" type="text" placeholder="XX.XXX.XXX-X" />
      </label>
      <label>Género
        <select v-model="s.adolescente.genero">
          <option :value="null">— Seleccionar —</option>
          <option value="Masculino">Masculino</option>
          <option value="Femenino">Femenino</option>
        </select>
      </label>
      <label class="full">Domicilio
        <input v-model="s.adolescente.domicilio" type="text" />
      </label>
      <label>Comuna
        <input v-model="s.adolescente.comuna" type="text" @change="s.resolverCentros()" />
      </label>
    </div>
  </fieldset>
</template>

<style scoped>
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.full { grid-column: 1 / -1; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 4px; }
input, select { padding: 6px 8px; border: 1px solid #d0d7de; border-radius: 4px; font-size: 0.95rem; }
</style>
```

- [ ] **Step 2: Implement DatosCausa.vue**

```vue
<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'
const s = useCasoStore()
const cat = useCatalogosStore()
</script>

<template>
  <fieldset>
    <legend>Datos de la causa</legend>
    <div class="grid">
      <label class="full">Tribunal
        <input v-model="s.causa.tribunal" type="text" />
      </label>
      <label>Tipo de resolución
        <input v-model="s.causa.tipo_resolucion" type="text" />
      </label>
      <label>Fecha de resolución
        <input v-model="s.causa.fecha_resolucion" type="date" />
      </label>
      <label>RUC
        <input v-model="s.causa.ruc" type="text" />
      </label>
      <label>RIT
        <input v-model="s.causa.rit" type="text" />
      </label>
      <label class="full">Delito
        <input v-model="s.causa.delito" type="text" list="delitos-list" />
        <datalist id="delitos-list">
          <option v-for="d in cat.delitos" :key="d" :value="d" />
        </datalist>
      </label>
      <label class="checkbox">
        <input v-model="s.causa.art_37_bis" type="checkbox" />
        Informe Técnico Art. 37 bis
      </label>
    </div>
  </fieldset>
</template>

<style scoped>
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.full { grid-column: 1 / -1; }
.checkbox { flex-direction: row; align-items: center; gap: 8px; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 4px; }
input { padding: 6px 8px; border: 1px solid #d0d7de; border-radius: 4px; font-size: 0.95rem; }
</style>
```

- [ ] **Step 3: Implement AdultoResponsable.vue**

```vue
<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <fieldset>
    <legend>Adulto responsable (opcional)</legend>
    <div class="grid">
      <label>Nombre
        <input v-model="s.adulto.nombre" type="text" />
      </label>
      <label>Teléfono
        <input v-model="s.adulto.telefono" type="text" />
      </label>
    </div>
  </fieldset>
</template>

<style scoped>
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 4px; }
input { padding: 6px 8px; border: 1px solid #d0d7de; border-radius: 4px; font-size: 0.95rem; }
</style>
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/Form/
git commit -m "feat(frontend): form components for adolescente, causa, adulto"
```

---

### Task 37: Selectors (CoimputadoRadio, MedidaBotonera, CentroSelector)

**Files:**
- Create: `frontend/src/components/Selectors/CoimputadoRadio.vue`
- Create: `frontend/src/components/Selectors/MedidaBotonera.vue`
- Create: `frontend/src/components/Selectors/CentroSelector.vue`

- [ ] **Step 1: Implement CoimputadoRadio.vue**

```vue
<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <fieldset v-if="s.candidatos.length > 1" class="aviso">
    <legend>Se detectaron {{ s.candidatos.length }} personas. Seleccione el imputado:</legend>
    <label v-for="(c, i) in s.candidatos" :key="c.run + i" class="opt">
      <input
        type="radio" name="coimputado"
        :value="i"
        :checked="s.adolescente.run === c.run && s.adolescente.nombre === c.nombre"
        @change="s.seleccionarCoimputado(i)"
      />
      <span>{{ i + 1 }}. {{ c.nombre }} ({{ c.run }})</span>
    </label>
  </fieldset>
</template>

<style scoped>
.aviso { border: 1px solid #f6c244; background: #fff8c5; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.opt { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; padding: 2px 0; }
</style>
```

- [ ] **Step 2: Implement MedidaBotonera.vue**

```vue
<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'

const s = useCasoStore()
const cat = useCatalogosStore()

async function elegir(sigla: string, estado: string) {
  if (estado === 'pendiente') return
  s.medida = sigla as never
  await s.resolverCentros()
}
</script>

<template>
  <fieldset>
    <legend>Medida</legend>
    <div class="botonera">
      <button
        v-for="m in cat.medidas"
        :key="m.sigla"
        type="button"
        :class="['btn-medida', {
          activa: s.medida === m.sigla,
          pendiente: m.estado === 'pendiente',
        }]"
        :disabled="m.estado === 'pendiente'"
        :title="m.estado === 'pendiente'
          ? 'Pendiente de formato — disponible en próxima versión'
          : m.nombre + ' (' + m.base_legal + ')'"
        @click="elegir(m.sigla, m.estado)"
      >
        {{ m.sigla }}
      </button>
    </div>
  </fieldset>
</template>

<style scoped>
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.botonera { display: flex; flex-wrap: wrap; gap: 6px; }
.btn-medida {
  border: 1px solid #d0d7de; background: #f6f8fa; color: #24292f;
  padding: 6px 14px; border-radius: 6px; cursor: pointer;
  font-weight: 600; font-size: 0.9rem; min-width: 64px;
}
.btn-medida.activa { background: #0969da; color: #fff; border-color: #0969da; }
.btn-medida.pendiente { opacity: 0.45; cursor: not-allowed; }
.btn-medida:hover:not(.pendiente):not(.activa) { background: #e6e8ea; }
</style>
```

- [ ] **Step 3: Implement CentroSelector.vue**

```vue
<script setup lang="ts">
import { computed } from 'vue'
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'

const s = useCasoStore()
const cat = useCatalogosStore()

const esIpIrc = computed(() => s.medida === 'IP' || s.medida === 'IRC')
const opcionesIpIrc = computed(() =>
  Object.entries(cat.centrosIpIrc).map(([sigla, c]) => ({ sigla, c })),
)
</script>

<template>
  <fieldset v-if="s.medida">
    <legend>Centro de cumplimiento</legend>

    <!-- IP/IRC: dropdown desde catálogo hardcoded -->
    <div v-if="esIpIrc">
      <label>Centro IP/IRC de ingreso
        <select
          :value="s.centroSeleccionado ? s.centroSeleccionado.nombre : ''"
          @change="(e) => {
            const t = (e.target as HTMLSelectElement).value
            s.centroSeleccionado = opcionesIpIrc.find(o => o.c.nombre === t)?.c ?? null
          }"
        >
          <option value="">— Seleccionar —</option>
          <option v-for="o in opcionesIpIrc" :key="o.sigla" :value="o.c.nombre">
            {{ o.c.nombre }}
          </option>
        </select>
      </label>
    </div>

    <!-- Estándar: radio si >1, info si =1, error si =0 -->
    <div v-else>
      <p v-if="s.centrosDisponibles.length === 0" class="error">
        Sin centros para la combinación medida × comuna.
      </p>
      <p v-else-if="s.centrosDisponibles.length === 1" class="info">
        Centro asignado: <strong>{{ s.centrosDisponibles[0].nombre }}</strong>
        ({{ s.centrosDisponibles[0].tipo }})
      </p>
      <div v-else>
        <p>Hay {{ s.centrosDisponibles.length }} centros para esta combinación. Elija uno:</p>
        <label v-for="(c, i) in s.centrosDisponibles" :key="i" class="opt">
          <input
            type="radio" name="centro"
            :value="i"
            :checked="s.centroSeleccionado?.nombre === c.nombre"
            @change="s.centroSeleccionado = c"
          />
          <span>{{ i + 1 }}. {{ c.nombre }} ({{ c.tipo }})</span>
        </label>
      </div>
    </div>
  </fieldset>
</template>

<style scoped>
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
label { font-size: 0.9rem; }
select { padding: 6px 8px; border: 1px solid #d0d7de; border-radius: 4px; }
.opt { display: flex; align-items: center; gap: 8px; padding: 2px 0; }
.error { color: #cf222e; font-size: 0.9rem; }
.info { color: #1a7f37; font-size: 0.9rem; }
</style>
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/Selectors/
git commit -m "feat(frontend): coimputado / medida / centro selectors (FR-08, FR-12, FR-13, FR-14)"
```

---

### Task 38: Action buttons + App.vue final layout

**Files:**
- Create: `frontend/src/components/Actions/GenerarButton.vue`
- Create: `frontend/src/components/Actions/LimpiarButton.vue`
- Create: `frontend/src/composables/useDownload.ts`
- Modify: `frontend/src/App.vue`
- Modify: `frontend/src/main.ts` (load catalogos)

- [ ] **Step 1: Implement useDownload.ts**

```ts
export function descargarBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}
```

- [ ] **Step 2: Implement GenerarButton.vue**

```vue
<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import { descargarBlob } from '../../composables/useDownload'
import { ref } from 'vue'

const s = useCasoStore()
const error = ref<string | null>(null)

async function generar() {
  error.value = null
  try {
    const r = await s.generar()
    if (r) descargarBlob(r.blob, r.filename)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al generar.'
  }
}
</script>

<template>
  <div class="generar">
    <button
      type="button" class="primary"
      :disabled="!s.listo || s.generando"
      @click="generar"
    >
      📥 {{ s.generando ? 'Generando…' : 'Procesar caso y descargar Word' }}
    </button>
    <ul v-if="s.validationErrors.length > 0" class="errs">
      <li v-for="e in s.validationErrors" :key="e">{{ e }}</li>
    </ul>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<style scoped>
.generar { display: flex; flex-direction: column; gap: 8px; }
.primary {
  background: #1f883d; color: #fff; border: none; border-radius: 6px;
  padding: 12px 16px; font-size: 1rem; cursor: pointer; font-weight: 600;
}
.primary:disabled { background: #6e7781; cursor: not-allowed; }
.errs { color: #bf8700; font-size: 0.85rem; margin: 0; padding-left: 18px; }
.error { color: #cf222e; font-size: 0.9rem; }
</style>
```

- [ ] **Step 3: Implement LimpiarButton.vue**

```vue
<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <button type="button" class="limpiar" @click="s.reset()">🧹 Limpiar</button>
</template>

<style scoped>
.limpiar {
  background: #f6f8fa; color: #57606a; border: 1px solid #d0d7de;
  border-radius: 6px; padding: 6px 10px; font-size: 0.85rem; cursor: pointer;
}
.limpiar:hover { background: #eaeef2; }
</style>
```

- [ ] **Step 4: Update main.ts to load catálogos**

```ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { useCatalogosStore } from './stores/catalogos'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')

// Cargar catálogos en background
useCatalogosStore().load().catch(err => {
  console.error('No se pudo cargar catálogos iniciales:', err)
})
```

- [ ] **Step 5: Update App.vue**

```vue
<script setup lang="ts">
import DropZone from './components/Upload/DropZone.vue'
import DatosAdolescente from './components/Form/DatosAdolescente.vue'
import DatosCausa from './components/Form/DatosCausa.vue'
import AdultoResponsable from './components/Form/AdultoResponsable.vue'
import CoimputadoRadio from './components/Selectors/CoimputadoRadio.vue'
import MedidaBotonera from './components/Selectors/MedidaBotonera.vue'
import CentroSelector from './components/Selectors/CentroSelector.vue'
import GenerarButton from './components/Actions/GenerarButton.vue'
import LimpiarButton from './components/Actions/LimpiarButton.vue'
import { useCasoStore } from './stores/caso'
const s = useCasoStore()
</script>

<template>
  <header>
    <h1>Sistema de Derivación Virtual — D.R.M.</h1>
    <div class="meta">
      <label>Fecha emisión <input v-model="s.fechaEmision" type="date" /></label>
      <label>Profesional <input v-model="s.profesional" type="text" /></label>
      <LimpiarButton />
    </div>
  </header>

  <main>
    <div class="col-izq">
      <DropZone />
      <CoimputadoRadio />
    </div>

    <div class="col-der">
      <DatosAdolescente />
      <DatosCausa />
      <AdultoResponsable />
      <MedidaBotonera />
      <CentroSelector />
      <GenerarButton />

      <ul v-if="s.warnings.length > 0" class="warns">
        <li v-for="w in s.warnings" :key="w">⚠️ {{ w }}</li>
      </ul>
    </div>
  </main>
</template>

<style>
* { box-sizing: border-box; }
body { margin: 0; font-family: Segoe UI, Roboto, sans-serif; color: #24292f; background: #fff; }
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 24px; border-bottom: 1px solid #d0d7de; background: #f6f8fa;
}
header h1 { font-size: 1.1rem; margin: 0; }
.meta { display: flex; align-items: center; gap: 12px; font-size: 0.85rem; }
.meta input { padding: 4px 6px; border: 1px solid #d0d7de; border-radius: 4px; }
main {
  display: grid; grid-template-columns: 1fr 2fr; gap: 16px;
  padding: 16px 24px; max-width: 1280px; margin: 0 auto;
}
.col-izq, .col-der { display: flex; flex-direction: column; gap: 12px; }
.warns { color: #9a6700; font-size: 0.85rem; margin: 4px 0; padding-left: 20px; }
</style>
```

- [ ] **Step 6: Build the frontend and verify**

Run: `cd frontend && npm run build`
Expected: `frontend/dist/` created with `index.html` and `assets/`.

- [ ] **Step 7: Commit**

```bash
git add frontend/src/ frontend/dist/
git commit -m "feat(frontend): actions, useDownload, App.vue layout, initial dist build"
```

---

## Phase 6 — Packaging & smoke test

### Task 39: Scripts (dev, build, iniciar)

**Files:**
- Create: `scripts/dev.ps1`
- Create: `scripts/build.ps1`
- Create: `scripts/iniciar_app.bat`
- Create: `data/.gitkeep`

- [ ] **Step 1: Create data/ placeholder**

`data/.gitkeep`: empty file. Reminds users to copy the real `CONSOLIDADO_OFERTA_DRM_V2.xlsx` here.

- [ ] **Step 2: Write scripts/dev.ps1**

```powershell
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
```

- [ ] **Step 3: Write scripts/build.ps1**

```powershell
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
```

- [ ] **Step 4: Write scripts/iniciar_app.bat**

```bat
@echo off
REM Lanzador para usuario final.
cd /d "%~dp0..\backend"
start "" http://127.0.0.1:8000
python -m uvicorn derivacion_drm.main:app --host 127.0.0.1 --port 8000
```

- [ ] **Step 5: Smoke test the launcher locally**

Run from a terminal (after `scripts/build.ps1` succeeded):
```
.\scripts\iniciar_app.bat
```
Expected: browser opens to `http://127.0.0.1:8000`, page loads the Vue UI (header "Sistema de Derivación Virtual"). Stop with Ctrl+C in the terminal.

- [ ] **Step 6: Commit**

```bash
git add scripts/ data/.gitkeep
git commit -m "chore(scripts): dev/build/iniciar PowerShell + BAT launchers"
```

---

### Task 40: End-to-end manual smoke test

**Files:**
- None (validation pass).

- [ ] **Step 1: Place the production Excel and logo into data/**

Manually copy `CONSOLIDADO_OFERTA_DRM_V2.xlsx` and optionally `logo_snrsj.png` into `data/`.

- [ ] **Step 2: Run build and launch**

```
.\scripts\build.ps1
.\scripts\iniciar_app.bat
```

- [ ] **Step 3: Execute MCA end-to-end scenario**

1. Browser opens at `http://127.0.0.1:8000`.
2. Drag a real (anonymized) Acta de Audiencia PDF + Oficio PDF for an MCA case to the DropZone.
3. Click "Procesar documentos". Verify:
   - Datos del adolescente autocompleted (nombre, RUN, género, domicilio, comuna).
   - Datos de la causa autocompleted (tribunal, RUC, RIT, delito, fecha).
   - If coimputados present, radio selector shows.
   - MCA button is highlighted (or user clicks it).
   - CentroSelector shows the resolved center for the comuna.
4. Click "🧹 Limpiar" to test reset preserves fecha emisión + profesional only.
5. Re-process and click "Procesar caso y descargar Word".
6. Open the downloaded `.docx`. Verify visually:
   - Font Bookman Old Style 12 pt.
   - Margins 2.5 cm everywhere.
   - Title centered, bold, underlined.
   - Adolescente nombre in MAYÚSCULAS, bold.
   - If art 37 bis was checked, the literal quote appears.
   - If adulto responsable is empty, NO empty parentheses.
   - Footer present on all pages.
   - Filename matches `{Nombre}_MCA_{Tribunal}_{RIT}_{RUC}.docx`.

- [ ] **Step 4: If issues found, file them as follow-up tasks (no fixes in this task)**

Track regressions in `docs/superpowers/plans/2026-05-20-mvp-1-mca-end-to-end.md` as a checklist below "Open issues from smoke test". If clean, mark MVP-1 done.

- [ ] **Step 5: Final tag (only if smoke test is clean)**

```bash
git tag -a mvp-1 -m "MVP-1: MCA end-to-end working"
```

(No `git push --tags` without explicit user authorization.)

---

## Self-review checklist (for the plan author)

- [ ] All 22 BRD FRs touched by MVP-1 (FR-01, 02, 03, 04, 05, 06, 07, 08, 10, 11, 13, 17, 19, 20, 22) have at least one task.
- [ ] FR-12 (botonera with disabled tooltips for pending medidas) covered by Task 37.
- [ ] FR-14 (IP/IRC selector) covered by Task 28 + 37 (visible but only relevant from MVP-3).
- [ ] FR-15, FR-16 (abonos, audiencia PII) deferred to MVP-2/3 by design — UI sections not added in MVP-1.
- [ ] FR-18 (IP/IRC table format) deferred to MVP-3 — `componer_documento_ipirc` is not implemented in this plan.
- [ ] FR-21 (interlineado 1.15) covered by ParagraphSpec default + Task 25 writer.
- [ ] RN-01 (filter víctima/adulto) — Task 14.
- [ ] RN-03 (RUN format) — Task 5.
- [ ] RN-06 (gendered agreement) — Task 21.
- [ ] RN-07 (no empty parentheses) — Task 21 (test included).
- [ ] RN-10 (footer) — Task 25.
- [ ] RN-11 (Bookman 12pt, margins 2.5cm, spacing 1.15, indent 1.25cm) — Task 25 (tests verify font + margins).
- [ ] Layering rule (domain ↛ adapters/api) — Task 32.

---

**Plan complete.**

