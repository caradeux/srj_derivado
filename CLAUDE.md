# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository status

This repo currently contains **only the BRD** (`docs/BRD_Sistema_Derivacion_Virtual.md`). The application code described by the BRD (`app_derivacion_v15.py`, `CONSOLIDADO_OFERTA_DRM_V2.xlsx`, `iniciar_app.bat`, `logo_snrsj.png`) is not yet present in this directory. When asked to "implement", "continue", or "fix" something, first verify whether the source file exists — if not, the task is greenfield implementation against the BRD, not an edit.

The BRD is the source of truth for requirements, business rules, and target architecture. Read it before making design decisions; it documents what was already tried and discarded (e.g., the v8 attempt at the Anthropic API was rejected for cost/privacy).

## Domain context (read this — code makes no sense without it)

This is a **Spanish-language internal tool** for the Chilean **Servicio Nacional de Reinserción Social Juvenil (S.N.R.S.J.)**, Coordinación Judicial D.R.M. It automates the generation of *certificados de derivación virtual* — Word documents that route juvenile offenders to the appropriate program under **Ley N° 20.084** (Responsabilidad Penal Adolescente).

The user is a non-technical *Profesional de Línea*. UI, error messages, comments, and commit messages should be in **Spanish**. The output Word document is a legal artifact — formatting is not cosmetic, it is required (see "Non-negotiable formatting rules" below).

### Legal/business vocabulary you must not confuse
- **RUN** ≠ **RUC** ≠ **RIT**. RUN identifies the *person* (`XX.XXX.XXX-X`, 7–9 digits + DV). RUC identifies the *case* (10–12 digits + DV, e.g. `2600664806-0`). RIT is the tribunal's internal case number (`NNNN-AAAA`). Confusing them silently corrupts a legal document.
- **Imputado** (the adolescent being derived) vs. **víctima** vs. **adulto responsable**. The extractor must discard anything from tables headed `VICTIMA`/`VÍCTIMA`/`ADULTO RESPONSABLE` when identifying the *imputado*. See RN-01.
- Measure siglas — **MCA, SBC, LAS, LAE, LAEIP, IP, IRC, PSA, SALIDAS ALTERNATIVAS** — are not interchangeable. Each maps to a different legal article, a different output format, and (for IP/IRC) a different center catalog. See §12 of the BRD.

### Two output formats — different code paths
1. **Standard derivation** (MCA, SBC, LAS, LAE, LAEIP, Salidas Alternativas): paragraph-based Word, centro selected by **comuna × medida** from `CONSOLIDADO_OFERTA_DRM_V2.xlsx`. See FR-17.
2. **IP / IRC**: **table-based** Word (11 rows: TRIBUNAL, NOMBRE, R.U.N, RUC, RIT, DELITO, RESOLUCIÓN, AUDIENCIA PII, FECHA DE RESOLUCIÓN, OBSERVACIONES, and for IRC also DURACIÓN Y ABONOS). Centro chosen by the user from a **hardcoded catalog of 4 centers** (San Joaquín, San Bernardo, C.M.N. Til Til, Santiago) — NOT from the Excel. See FR-18, RN-05.

PSA and the five mixed combinations (IRC+LAEIP, IRC+LAE, IRC+LAS, LAEIP+LAE, LAEIP+LAS) are **pending** — their buttons render disabled with a tooltip. No other mixed combinations are valid. See §12.2, RN-12.

## Target architecture

Single-file Streamlit app (`app_derivacion_v15.py`, ~1500 lines) running locally at `http://localhost:8501`. No database, no server, no network calls, no auth. All state lives in `st.session_state` with keys suffixed `_{ck}` where `ck` is a counter — incrementing `ck` is how the "Limpiar" button resets the form without enumerating each key (see §10.4).

Dependencies (NFR-02, Anexo B):
```
python -m pip install streamlit pandas python-docx PyPDF2 pdfplumber openpyxl
```

Pipeline:
- **PDF reading**: `pdfplumber` (primary, preserves tables) → `PyPDF2` (fallback). v9 switched to pdfplumber specifically because table structure matters for extracting names from the *Acta de Audiencia*.
- **Word reading**: `python-docx`.
- **Centro lookup** (standard medidas): `pandas` + `openpyxl` reads `CONSOLIDADO_OFERTA_DRM_V2.xlsx`, sheet `Desacumulado`. Match by **medida synonym** (see `SINONIMOS_MEDIDA` in BRD §13.3) and **normalized comuna** (tilde- and case-insensitive — Peñalolén/Peñalolen must match).
- **Word generation**: `python-docx`.

Run the app:
```
iniciar_app.bat
```
or
```
python -m streamlit run app_derivacion_v15.py
```
Always use `python -m streamlit ...`, not `streamlit ...` directly, to avoid PATH issues with multiple Python installs (R-07).

## Extraction rules that are easy to get wrong

- **RUN formatting** (FR-04, RN-03): strip leading zeros, output `XX.XXX.XXX-X`. `0022846782-0` → `22.846.782-0`. `8765432-9` → `8.765.432-9`.
- **Name cleanup** (FR-05): strip trailing parentheses and commas — `"Juan Pérez (ip San Bernardo)"` → `"Juan Pérez"`. Title Case, but connectors (`de`, `del`, `la`, `los`, etc.) stay lowercase.
- **Coimputados** (FR-08): when multiple valid imputados are detected, show a radio selector; do not silently pick one.
- **Art. 37 bis** (FR-10): detection auto-checks the checkbox AND inserts the exact quoted phrase `"Evacúese informe Técnico conforme al artículo 37 bis"` in the Word.
- **Multiple centers for one comuna** (FR-13): if both PRIORIZADAS and NO PRIORIZADAS list the comuna, show a radio — do not auto-pick.

## Non-negotiable formatting rules for the output Word

These come from RN-10, RN-11, BR-03. The document is institutional output; deviations are defects.

- Font: **Bookman Old Style 12 pt**
- Margins: **2.5 cm all four sides**
- Page size: **Carta (8.5" × 11")**
- Line spacing: **1.15** (every paragraph)
- Body paragraph first-line indent: **1.25 cm**
- Fixed footer on every page: `Av. Pedro De Valdivia N° 4070, Ñuñoa.  Fono: 22.3980.04.00`
- Logo `logo_snrsj.png` inserted if file present; if absent, generate without it (do not error)
- Center email rendered as hyperlink (blue + bold + underline)
- Gendered text agreement (RN-06): Masculino → `don/domiciliado/derivado/al adolescente individualizado/adulto responsable`; Femenino → `doña/domiciliada/derivada/a la adolescente individualizada/adulta responsable`
- Adulto responsable parenthetical (RN-07): if empty, **do not emit empty parentheses**; if partial, emit only the filled fields
- Duration field for LAS/LAE/LAEIP (RN-08): no default like `"6 meses"` — empty with placeholder hint

## Output filename convention (BR-04, FR-19, RN-09)

```
{Nombre_Adolescente}_{Sigla_Medida}[_{Sigla_Centro}]_{Tribunal}_{RIT}_{RUC}.docx
```
The center sigla segment is present **only** for IP/IRC, using: `San_Joaquin`, `San_Bernardo`, `Til_Til`, `Santiago`. This filename is the trazabilidad mechanism — there is no DB.

## Versioning convention

Files are versioned in the filename (`app_derivacion_v15.py`). New versions are not rebases of the previous file but separate files; v15 was specifically "back to v10 clean + reapply everything" (see §17.1). Each non-trivial block carries a comment like `# 🆕 V15: ...` indicating which version introduced it (NFR-07) — preserve this convention when adding code.

## What is out of scope (do not propose unless asked)

Per §4.2: OCR for scanned PDFs, persistent storage of past derivations, automatic email sending to centers, integration with SITPJ or internal S.N.R.S.J. systems, multi-user operation, electronic signature, and any paid API (Anthropic/OpenAI was explicitly rejected in v8 for cost and privacy — local-only is a hard requirement, NFR-05).
