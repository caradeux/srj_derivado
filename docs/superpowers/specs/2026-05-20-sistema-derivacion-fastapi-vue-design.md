# Sistema de Derivación Virtual — Reimplementación FastAPI + Vue 3

**Fecha:** 2026-05-20
**Autor del spec:** Brainstorming session
**Reemplaza:** `app_derivacion_v15.py` (Streamlit, single-file ~1500 LOC)
**BRD de referencia:** `docs/BRD_Sistema_Derivacion_Virtual.md`

---

## 1. Objetivo y no-objetivos

### Objetivo
Reimplementar el Sistema de Derivación Virtual con una arquitectura por capas, framework moderno (FastAPI + Vue 3), y suite de tests pragmática — manteniendo todas las reglas de negocio, formato institucional y restricciones operacionales documentadas en el BRD v1.0.

### No-objetivos (no cambian respecto del BRD)
- Multiusuario, servidor compartido, autenticación.
- Persistencia de derivaciones históricas (no hay BD).
- Llamadas de red fuera de `localhost` (NFR-05).
- OCR de PDFs escaneados, firma electrónica, integración SITPJ.
- Implementación de PSA o combinaciones mixtas (BRD §17.2 las deja pendientes).

---

## 2. Decisiones de arquitectura (fijadas en brainstorming)

| Decisión | Elegido | Alternativas descartadas |
|---|---|---|
| Backend | **FastAPI** (Python 3.10+) | Django, Flask |
| Frontend | **Vue 3 + Vite + Pinia + TypeScript** | React, Svelte |
| Despliegue | **Local-only, mismo modelo que hoy** | Servidor institucional |
| Empaquetado | **Frontend pre-build + .bat launcher** | Tauri, PyInstaller |
| Organización backend | **Capas pragmáticas: `domain` / `adapters` / `api`** | Hexagonal formal, feature folders |
| Tests | **Pragmáticos con pytest** (sin e2e) | Comprehensive con Playwright |
| Linting | **Ruff** (sin pre-commit, sin CI) | mypy estricto + pre-commit + GH Actions |
| Tipos compartidos | **OpenAPI → TypeScript generado** | DTOs escritos a mano |
| UI library | **CSS plano** | Vuetify, PrimeVue |
| Scope MVP-1 | **Sólo MCA end-to-end** | Paridad v15 total en un solo release |

Cualquier desviación de estas decisiones requiere revisar este spec.

---

## 3. Arquitectura y modelo de proceso

Un solo proceso `uvicorn` sirve la API REST y el bundle estático de Vue. El `.bat` arranca uvicorn en `127.0.0.1:8000` y abre el navegador.

```
┌──────────────────── PC del Profesional de Línea ─────────────────────┐
│                                                                       │
│   iniciar_app.bat                                                     │
│       │                                                               │
│       ▼                                                               │
│   uvicorn (un solo proceso)                                           │
│       ├── FastAPI                                                     │
│       │     ├── /api/*    → endpoints REST                            │
│       │     └── /         → mount frontend/dist como StaticFiles      │
│       │                                                               │
│       └── abre el navegador → http://127.0.0.1:8000                   │
│                                                                       │
│   Archivos locales (lectura en runtime):                              │
│       data/CONSOLIDADO_OFERTA_DRM_V2.xlsx                             │
│       data/logo_snrsj.png (opcional)                                  │
└───────────────────────────────────────────────────────────────────────┘
```

Restricciones del BRD preservadas:
- Sin red fuera de localhost (NFR-05).
- Lanzador `python -m uvicorn …` para evitar conflictos de PATH (R-07, análogo al `python -m streamlit` actual).
- `logo_snrsj.png` y la planilla Excel viven junto al proyecto, no se modifican en runtime.

---

## 4. Backend — capas

Regla de dependencias: `domain` no importa de `adapters` ni de `api`. `adapters` puede importar de `domain`. `api` importa de ambos. Esta regla se verifica con un test (`tests/test_layering.py`) que escanea imports.

### 4.1 `domain/` — lógica pura, sin I/O

#### `domain/models.py` — entidades Pydantic v2

```python
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
    nombre: str                       # Title Case, conectores en minúscula
    run: str                          # canonical XX.XXX.XXX-X
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
    tipo: Literal["Priorizada", "No priorizada"] | None = None   # None para IP/IRC

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

#### `domain/extractors/` — un módulo por campo

Cada extractor es función pura `(texto, tablas) → ExtractedField[T]`. `ExtractedField` lleva `value`, `confidence: Literal["high","low"]` y `source: str` (ej. `"tabla acta"`, `"regex fallback"`) para que la UI pueda señalar al profesional cuándo verificar.

- `run.py` — FR-04, RN-03: formato canónico `XX.XXX.XXX-X`, descarta ceros iniciales, distingue de RUC.
- `ruc.py` — FR-02: prioriza coincidencias precedidas por "RUC".
- `rit.py` — FR-03: prioriza coincidencias precedidas por "RIT".
- `nombre.py` — FR-05: lee columna "NOMBRE IMPUTADO", limpia paréntesis/comas trailing, Title Case con conectores en minúscula, descarta tablas con encabezado `VICTIMA`/`VÍCTIMA`/`ADULTO RESPONSABLE` (RN-01). Devuelve `list[Adolescente]` para coimputados (FR-08).
- `domicilio.py` — FR-07: lee celda contigua al RUN, maneja caso "RUN+dirección+comuna en una sola celda", normaliza comuna con `normalizar_comuna()`.
- `genero.py` — FR-06: tabla de ~60 nombres femeninos chilenos, retorna `None` para nombres no identificados (el usuario corrige manualmente, RN-09).
- `medida.py` — detecta mediante `SINONIMOS_MEDIDA` (BRD §13.3).
- `adulto.py` — FR-11: tabla con encabezado "ADULTO RESPONSABLE".
- `art_37_bis.py` — FR-10: detección literal de "37 bis", retorna `bool`.

#### `domain/pipeline.py` — orquestador

```python
class Tabla(BaseModel):
    """Representación neutral de una tabla; los adaptadores convierten desde
    pdfplumber.Table o docx.table.Table a esto antes de pasarlo al pipeline."""
    encabezados: list[str]
    filas: list[list[str]]

class DocumentoCargado(BaseModel):
    nombre_archivo: str
    texto: str
    tablas: list[Tabla]

class ExtractionResult(BaseModel):
    candidatos: list[Adolescente]     # 1..N (coimputados)
    causa: Causa
    adulto: AdultoResponsable
    medida_sugerida: Medida | None
    warnings: list[str]               # ej. "RUN detectado por regex, verificar"

def ejecutar_pipeline(docs: list[DocumentoCargado]) -> ExtractionResult: ...
```

#### `domain/centros.py` — resolución

```python
SINONIMOS_MEDIDA: dict[Medida, list[str]] = { ... }    # BRD §13.3

CENTROS_IP_IRC: dict[CentroIPIRC, CentroAsignado] = { ... }    # BRD §13.2 hardcoded

def normalizar_comuna(s: str) -> str:
    """Strip accents, lowercase, strip whitespace. Peñalolén ≡ peñalolen ≡ Penalolen."""

def resolver_centro_estandar(
    medida: Medida,
    comuna: str,
    catalogo: CatalogoOferta,           # inyectado por FastAPI
) -> list[CentroAsignado]:
    """0 / 1 / muchos. El router decide qué hacer en cada caso."""

def centro_ip_irc(opcion: CentroIPIRC) -> CentroAsignado:
    return CENTROS_IP_IRC[opcion]
```

#### `domain/word_content.py` — composición pura del documento

Separar **qué dice** de **cómo se renderiza**. Esta capa devuelve un `WordDocumentSpec` (Pydantic, data-only) y contiene toda la lógica del BRD:

- Concordancia de género (RN-06: don/doña, domiciliado/a, derivado/a, etc.).
- Elisión de paréntesis del adulto responsable cuando está vacío o parcial (RN-07).
- Cita literal de art. 37 bis (FR-10).
- Párrafo condicional de audiencia PII (FR-16).

#### `domain/filename.py` — composición del nombre de archivo

Función pura `componer_nombre_archivo(caso: CasoDerivacion) -> str` que implementa BR-04, FR-19, RN-09:
- Estándar: `{Nombre}_{Medida}_{Tribunal}_{RIT}_{RUC}.docx`
- IP/IRC: `{Nombre}_{Medida}_{Sigla_Centro}_{Tribunal}_{RIT}_{RUC}.docx`

Separada de `word_content.py` porque el filename viaja en el header HTTP (`Content-Disposition`) antes de que se renderice el `.docx` — son dos productos distintos derivados del mismo `CasoDerivacion`.

```python
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
    rows: list[tuple[str, str]]        # 2-col: etiqueta, valor
    style: str = "Table Grid"

class WordDocumentSpec(BaseModel):
    paragraphs: list[ParagraphSpec | TableSpec]
    incluir_logo: bool
    footer_text: str = "Av. Pedro De Valdivia N° 4070, Ñuñoa.  Fono: 22.3980.04.00"
    filename: str

def componer_documento_estandar(
    caso: CasoDerivacion, profesional: str, fecha_emision: date,
) -> WordDocumentSpec: ...

def componer_documento_ipirc(
    caso: CasoDerivacion, profesional: str, fecha_emision: date,
) -> WordDocumentSpec: ...
```

### 4.2 `adapters/` — I/O

- `pdf_reader.py` — `pdfplumber` primario, `PyPDF2` fallback (NFR-06). Devuelve `DocumentoCargado` con texto y tablas neutralizadas.
- `word_reader.py` — `python-docx` para `.docx`. Devuelve `DocumentoCargado`.
- `excel_catalog.py` — `pandas` + `openpyxl` lee `CONSOLIDADO_OFERTA_DRM_V2.xlsx` hoja `Desacumulado`, devuelve `CatalogoOferta` indexado por medida.
- `word_writer.py` — toma un `WordDocumentSpec` y produce `bytes` `.docx` aplicando: Bookman Old Style 12pt, márgenes 2.5cm, interlineado 1.15, sangría 1.25cm, hyperlink azul+negrita+subrayado, logo si el PNG existe, pie de página fijo (RN-10, RN-11).

### 4.3 `api/` — superficie HTTP

Cinco routers, todos bajo `/api`:

| Método | Path | Body | Respuesta |
|---|---|---|---|
| `POST` | `/api/extract` | `multipart/form-data` con 1..N archivos PDF/.docx | `ExtractionResult` |
| `POST` | `/api/centros/resolver` | `{ medida, comuna }` | `list[CentroAsignado]` |
| `GET`  | `/api/centros/ip-irc` | — | `dict[CentroIPIRC, CentroAsignado]` |
| `POST` | `/api/derivacion/generar` | `{ caso: CasoDerivacion, profesional, fecha_emision }` | `.docx` stream, `Content-Disposition: attachment; filename=…` |
| `GET`  | `/api/catalogo/medidas` | — | lista de medidas con estado activa/pendiente y base legal |
| `GET`  | `/api/catalogo/delitos` | — | `list[str]` (~50 delitos comunes RPA) |

Stateless. El `CasoDerivacion` completo viaja en el body de `/generar`. No hay base de datos. No hay CORS (same-origin).

Validación: Pydantic v2 valida en el server. Errores 422 con detalle por campo. El frontend valida lo mismo en cliente para feedback inmediato; el 422 sólo aparece si el cliente está fuera de sincro.

`adapters/excel_catalog.py` se carga **una vez al startup** con `@lru_cache` y se inyecta a `resolver` vía `Depends`. Recargar requiere reiniciar el proceso (matches el modelo actual donde el .xlsx se lee al arrancar).

---

## 5. Frontend — Vue 3 + Vite + Pinia + TypeScript

### 5.1 Contrato de tipos

```
FastAPI (Pydantic v2) ── /openapi.json ──► openapi-typescript ──► src/api/types.ts
```

`npm run gen` regenera `types.ts`. Si el backend cambia el contrato, el frontend deja de compilar. Single source of truth.

### 5.2 Estructura

```
frontend/src/
  App.vue
  main.ts
  api/
    client.ts                    fetch wrapper con normalización de errores
    types.ts                     ← generado por openapi-typescript
  stores/
    caso.ts                      Pinia: el CasoDerivacion en edición
    catalogos.ts                 medidas, delitos, centros IP/IRC (carga única)
  components/
    Upload/
      DropZone.vue               FR-01 drag-and-drop multi-archivo
      FileCard.vue               una tarjeta por archivo
    Form/
      DatosAdolescente.vue       nombre, RUN, género, domicilio, comuna
      DatosCausa.vue             tribunal, RUC, RIT, delito, fecha, 37 bis
      AdultoResponsable.vue      nombre + teléfono opcional (RN-07)
      AudienciaPII.vue           checkbox + 5 campos (FR-16)
    Selectors/
      CoimputadoRadio.vue        si candidatos.length > 1 (FR-08)
      MedidaBotonera.vue         8 botones + Mixtas, pendientes disabled (FR-12)
      CentroSelector.vue         radio para estándar, dropdown para IP/IRC
    Actions/
      GenerarButton.vue          valida y llama /generar
      LimpiarButton.vue          FR-20: reset preservando fecha + profesional
  composables/
    useDownload.ts               dispara descarga del .docx
```

### 5.3 Flujo de estado (Pinia única fuente de verdad)

```
1. usuario suelta archivos      → POST /api/extract
                                  → store.setExtraction(result)
                                  → si candidatos.length > 1: pedir coimputado
                                  → sino: store.selectAdolescente(candidatos[0])

2. usuario edita medida/comuna  → (debounced) POST /api/centros/resolver
                                  → store.setCentrosDisponibles([...])
                                  → 0 → mostrar error
                                  → 1 → auto-asignar
                                  → >1 → mostrar radio

3. usuario elige IP o IRC       → CentroSelector cambia a modo IP/IRC
                                  → lee de catalogos.centrosIpIrc

4. click Generar                → store.validate() → si OK:
                                  → POST /api/derivacion/generar
                                  → useDownload.triggerSave(blob, filenameDeHeader)

5. click Limpiar                → store.reset({ keep: ['profesional', 'fechaEmision'] })
```

### 5.4 Validación cliente

El store expone `validationErrors: ComputedRef<string[]>`. El botón Generar lee `validationErrors.value.length === 0` para habilitarse. Reglas (FR-22):
- Siempre: `nombre`, `genero`, `medida`.
- Medidas estándar: además `comuna`.
- IP/IRC: además `centro`.

### 5.5 CSS

CSS plano por componente (Vue SFC `<style scoped>`). Sin Vuetify/PrimeVue: los botones de medida (FR-12) requieren estados visuales muy específicos (activo/disabled/tooltip explicativo) que son más fáciles en CSS directo que peleando con un framework.

---

## 6. Scope MVP y plan de iteraciones

Cada iteración termina con una app que un profesional podría usar para ese subconjunto. Las medidas no implementadas viven en la UI como botones **disabled con tooltip** (FR-12) — nunca medidas a medio terminar.

### MVP-1: MCA end-to-end (primer release)
- Upload + extracción de PDF/.docx.
- Coimputado selector.
- Resolución de centro desde Excel por comuna × MCA.
- Generación Word formato estándar con formato institucional completo.
- Filename per FR-19 patrón estándar.
- Limpiar.

### MVP-2: SBC, LAS, LAE, LAEIP
- Agrega secciones de UI: duración, abonos, audiencia PII.
- Mismo formato Word base, mismas reglas de género.

### MVP-3: IP e IRC
- Nuevo generador `componer_documento_ipirc` (formato de tabla, BRD FR-18, §14.2).
- Selector de centro IP/IRC desde catálogo hardcoded.
- Filename con sigla de centro.

### MVP-4: Salidas Alternativas
- Reusa formato estándar.

### Fuera de este build
PSA (BRD §17.2 pendiente), combinaciones mixtas (§17.2 pendiente), OCR, validación de dígito verificador, historial de derivaciones, multi-usuario.

---

## 7. Estrategia de tests

```
backend/tests/
  domain/
    test_run_format.py             FR-04, RN-03 — table-driven, 20+ casos
                                     "0022846782-0" → "22.846.782-0"
                                     "8765432-9"    → "8.765.432-9"
    test_comuna_normalize.py       Peñalolén ≡ Peñalolen ≡ peñalolen
    test_centros_resolver.py       0 / 1 / muchos resultados, sinónimos
    test_genero_inferir.py         catálogo de ~60 nombres, unisex → None
    test_adulto_eliding.py         RN-07 — paréntesis vacíos nunca emitidos
    test_word_content_estandar.py  snapshot WordDocumentSpec MCA:
                                     masculino vs femenino
                                     con/sin 37 bis
                                     con/sin adulto responsable
                                     con/sin audiencia PII (MVP-2+)
    test_word_content_ipirc.py     snapshot WordDocumentSpec IP/IRC (MVP-3)
    test_extractors_run.py         (uno por extractor)
    test_extractors_nombre.py      incluye RN-01: filtra VICTIMA/ADULTO
    test_pipeline.py               integration: doc → ExtractionResult
  adapters/
    test_pdf_reader.py             PDFs fixture anonimizados
    test_word_writer.py            renderiza spec, reabre con python-docx,
                                     assert Bookman, 2.5cm márgenes, 1.15
    test_excel_catalog.py          carga .xlsx fixture
  api/
    test_extract_endpoint.py       multipart → ExtractionResult
    test_resolver_endpoint.py      múltiples centros → list
    test_generar_endpoint.py       happy path + 422
  test_layering.py                 AST scan: domain/ no importa adapters/ ni api/

backend/tests/fixtures/
  pdfs/
    acta_audiencia_anon_01.pdf
    oficio_mca_anon_01.pdf
    sentencia_irc_anon_01.pdf      (para MVP-3)
  excel/
    catalogo_test.xlsx             trimmed, no datos productivos
```

Dos niveles para el Word:
1. **Content snapshots** del `WordDocumentSpec` como JSON — rápido, cubre toda la lógica condicional y de género.
2. **Una prueba de renderizado** que abre el `.docx` con python-docx y verifica font, márgenes, interlineado — lenta, un solo canario.

Sin tests e2e. Si en el futuro hace falta, agregar Playwright contra `npm run dev` + `uvicorn --reload`.

---

## 8. Layout del repositorio

```
JM/
├── backend/
│   ├── pyproject.toml             ruff config, deps, metadata
│   ├── src/derivacion_drm/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── extractors/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── run.py
│   │   │   │   ├── ruc.py
│   │   │   │   ├── rit.py
│   │   │   │   ├── nombre.py
│   │   │   │   ├── domicilio.py
│   │   │   │   ├── genero.py
│   │   │   │   ├── medida.py
│   │   │   │   ├── adulto.py
│   │   │   │   └── art_37_bis.py
│   │   │   ├── pipeline.py
│   │   │   ├── centros.py
│   │   │   ├── word_content.py
│   │   │   └── filename.py
│   │   ├── adapters/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_reader.py
│   │   │   ├── word_reader.py
│   │   │   ├── excel_catalog.py
│   │   │   └── word_writer.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   ├── schemas.py
│   │   │   └── routers/
│   │   │       ├── extract.py
│   │   │       ├── centros.py
│   │   │       ├── derivacion.py
│   │   │       └── catalogo.py
│   │   └── main.py                app factory + StaticFiles mount
│   └── tests/                     ver §7
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json              strict
│   ├── src/                       ver §5.2
│   └── dist/                      ← artefacto, committed
├── data/
│   ├── CONSOLIDADO_OFERTA_DRM_V2.xlsx
│   └── logo_snrsj.png             opcional
├── scripts/
│   ├── build.ps1                  npm ci + npm run build + pip install -e
│   ├── iniciar_app.bat            lanzador final
│   └── dev.ps1                    uvicorn --reload + vite dev simultáneo
├── docs/
│   ├── BRD_Sistema_Derivacion_Virtual.md
│   └── superpowers/specs/
│       └── 2026-05-20-sistema-derivacion-fastapi-vue-design.md   ← este archivo
├── CLAUDE.md
└── README.md
```

---

## 9. Empaquetado y lanzamiento

### Build (máquina del desarrollador)
```powershell
# scripts/build.ps1
Set-Location frontend
npm ci
npm run build
Set-Location ../backend
python -m pip install -e .
pytest tests
```

`frontend/dist/` queda comprometido al repo. La máquina del usuario final **nunca necesita Node.js**.

### Instalación end-user (una vez)
```
python -m pip install fastapi uvicorn[standard] pandas python-docx PyPDF2 pdfplumber openpyxl
```

### Lanzador (`scripts/iniciar_app.bat`)
```bat
@echo off
cd /d "%~dp0..\backend"
start "" http://127.0.0.1:8000
python -m uvicorn derivacion_drm.main:app --host 127.0.0.1 --port 8000
```

Doble-clic → uvicorn arranca → navegador abre → Vue carga → trabajo.

---

## 10. Tooling

- **Ruff** en `pyproject.toml` (format + lint). Se corre on-demand: `ruff format .`, `ruff check .`. Sin pre-commit.
- **TypeScript strict** en frontend, ESLint con config default del scaffold Vue.
- **Sin CI**. Sin GitHub Actions. Un solo desarrollador, repo local.

---

## 11. Riesgos y decisiones de mitigación

| Riesgo | Mitigación heredada del BRD | Mitigación adicional de este diseño |
|---|---|---|
| Cambio de formato de actas judiciales (BRD R-01) | Fallback manual, regex configurables | Extractores aislados como funciones puras, fáciles de ajustar sin tocar el resto |
| Planilla Excel desactualizada (R-02) | Mantenedor designado | Catálogo cargado en startup; reinicio del proceso recarga |
| Cambio en directiva IP/IRC (R-03) | Catálogo editable en código | `CENTROS_IP_IRC` en `domain/centros.py` como constante con un solo punto de edición |
| PDF escaneado no procesa (R-05) | Aviso al usuario | El extractor retorna `ExtractedField.value=None`, la UI lo señala |
| Múltiples Pythons en PATH (R-07) | Documentación | Mantiene `python -m uvicorn …` en el .bat |
| Drift del frontend respecto del backend | — | OpenAPI → TypeScript: drift causa fallo de compilación |
| Tests de Word frágiles (binarios) | — | Split content/render: snapshots de `WordDocumentSpec` (JSON), no de .docx |

---

## 12. Cambios respecto del BRD

Este diseño preserva el 100% de los requerimientos funcionales y no funcionales del BRD v1.0. Los únicos cambios son **internos**:

| Aspecto | BRD v1.0 (v15) | Este diseño |
|---|---|---|
| Framework UI | Streamlit | Vue 3 + Vite |
| Backend | Streamlit en un solo archivo ~1500 LOC | FastAPI por capas |
| Estado | `st.session_state` con sufijos `_{ck}` | Pinia store, reset explícito |
| Tipos compartidos | — (todo en runtime) | OpenAPI → TypeScript generado |
| Tests | — (sin suite) | pytest con fixtures anonimizadas |
| Versionado | Un archivo nuevo por versión (`app_derivacion_v15.py`) | Git + semver en `pyproject.toml` |
| Comentarios `# 🆕 V15: ...` | Marcadores en código | Reemplazados por git blame |

El usuario final no percibe diferencias funcionales en MVP-1 más allá de un look-and-feel distinto: las mismas medidas, los mismos extractores, el mismo Word de salida.

---

**Fin del spec — listo para writing-plans**
