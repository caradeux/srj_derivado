---
documento: Plan de rediseño de interfaz
proyecto: Sistema de Derivación Virtual D.R.M. — S.N.R.S.J.
version: v1
fecha: 2026-05-21
autor: jcaradeux@inovabiz.com (con asistencia Claude Code)
estado: PENDIENTE DE APROBACIÓN
alcance: solo frontend Vue 3 (src/) — backend y BRD intactos
---

# Plan de rediseño de interfaz — v1

> **Objetivo:** transformar el formulario actual (1.700+ px de scroll, 5 cards anidadas, acento verde tipo SaaS) en una superficie densa, monocromática y profesional acorde a un acto administrativo del S.N.R.S.J. bajo Ley 20.084.

---

## 0. Decisiones tomadas (resumen ejecutivo)

| Eje | Decisión |
|---|---|
| Enfoque | **A — Densificación monocromática** (pantalla única, sin cards, sidebar derecho sticky con resumen + CTA) |
| Paleta | Azul marino S.N.R.S.J. (`#1E3A5F`) + grises carbono (`#475569`, `#64748B`, `#E5E7EB`). **Cero verde en UI funcional.** |
| Tipografía | Sin cambio: EB Garamond (heading) + Lato (body) se mantienen |
| Adulto responsable | Colapsado por defecto. Si el extractor lo detecta, se renderiza ya expandido |
| Tipo de resolución | `<select>` cerrado con `[oficio, sentencia, sentencia ejecutoriada]` (3 únicos valores que el backend extrae) |
| Lógica / store / API | **NO se tocan.** Solo CSS + reestructura de templates Vue |
| Mockup | Ver §5 |

---

## 1. Diagnóstico — causas raíz

Lo observado en `srj-form-filled.png` no es una falla única, son 5 decisiones acumuladas:

| # | Causa | Dónde vive | Síntoma |
|---|---|---|---|
| 1 | **5 `<fieldset>` independientes** con `border + box-shadow + padding sp-4/sp-5` cada uno | `DatosAdolescente.vue`, `DatosCausa.vue`, `AdultoResponsable.vue`, `MedidaBotonera.vue`, `CentroSelector.vue` — CSS idéntico copiado 5 veces | ~250-280 px verticales por sección × 5 = 1.300+ px solo de "marcos" |
| 2 | **Verde mint en iconos de cada legend** + CTA | `tokens.css` define `--color-accent: #059669`; cada componente repite `legend :deep(.icon) { color: var(--color-accent); }`; `GenerarButton.vue` usa `background: var(--color-accent)` | Look "saas-friendly" disonante con contexto judicial |
| 3 | **Layout 2-col fijo** con sidebar izquierda permanente | `App.vue:179-185`, `grid-template-columns: minmax(320px, 1fr) minmax(420px, 2fr)` | Izq queda en blanco tras procesar; der hace todo el scroll |
| 4 | **Tres `<h2>` numerados** + cinco `<legend>` de fieldset | `App.vue:58-82` | Doble jerarquía: 8 títulos visibles para 14 campos |
| 5 | `SALIDAS_ALTERNATIVAS` (enum crudo) + `Tipo de resolución` como input libre | `MedidaBotonera.vue:38`; `DatosCausa.vue:19-21` | Texto técnico filtrado al usuario final + inconsistencia en Word generado |

---

## 2. Tokens — cambios en `src/styles/tokens.css`

### 2.1 Reemplazos directos

| Token actual | Valor actual | Valor nuevo | Justificación |
|---|---|---|---|
| `--color-accent` | `#059669` verde | `#1E3A5F` (= primary) | Iconos de legend pasan a navy. Concepto "accent" deja de existir. |
| `--color-accent-hover` | `#047857` | (eliminar) | Sin accent que hover-ear. |
| `--color-secondary` | `#2563EB` azul brillante | `#475569` (gris carbono) | Links sobrios; azul brillante se reserva solo para `:focus-visible`. |
| `--color-success` | `#059669` | `#1E3A5F` | Panel "Centro asignado" deja de ser verde. |
| `--color-success-bg` | `#ECFDF5` mint | `#F1F5F9` (= surface-muted) | |

### 2.2 Tokens nuevos a agregar

```css
--color-rule:           #E5E7EB;   /* línea fina entre secciones (más sutil que --color-border) */
--color-aside-bg:       #F8FAFC;   /* fondo aside resumen (= bg, para que se "funda") */
--color-fg-on-aside:    #475569;   /* texto del aside */
--control-h-compact:    36px;      /* alternativa a --control-h: 40px */
--sp-section:           20px;      /* separación vertical entre secciones del form */
```

### 2.3 Tipografía

Sin cambio. EB Garamond (heading) + Lato (body) se mantienen tal como están en `tokens.css:5`.

---

## 3. Layout nuevo — cambios en `App.vue`

### 3.1 Estructura del DOM

**Antes** (`App.vue:56-92`):

```
<main>
  <section.col-izq>                              ← 1/3 ancho, fija
    <h2>1. Cargar documentos</h2>
    <DropZone/>
    <CoimputadoRadio/>
  </section>
  <section.col-der>                              ← 2/3 ancho, hace TODO el scroll
    <h2>2. Revisar y completar datos</h2>
    <DatosAdolescente/>                          ← fieldset con border+shadow
    <DatosCausa/>                                ← fieldset con border+shadow
    <AdultoResponsable/>                         ← fieldset con border+shadow
    <MedidaBotonera/>                            ← fieldset con border+shadow
    <CentroSelector/>                            ← fieldset con border+shadow
    <div.generar-wrap>
      <h2>3. Generar certificado</h2>
      <GenerarButton/>
    </div>
    <ul.warns/>
  </section>
</main>
```

**Después**:

```
<main class="workspace">
  <CoimputadoRadio/>                             ← sticky top banner si aplica
  <article class="form">                         ← col 1, max ~720 px
    <section data-step="documentos">             ← sin <h2>, separador fino
      <DropZone/>                                ← compacto post-carga
    </section>
    <section data-step="datos">
      <DatosAdolescente/>                        ← SIN fieldset border, heading inline
      <DatosCausa/>                              ← idem
      <AdultoResponsable/>                       ← colapsado por defecto
    </section>
    <section data-step="medida">
      <MedidaBotonera/>                          ← horizontal compacto
      <CentroSelector/>                          ← inline, no card
    </section>
  </article>
  <aside class="resumen" aria-label="Resumen y acciones">  ← STICKY, top:24px
    <ResumenCaso/>                               ← NUEVO componente
    <GenerarButton/>                             ← CTA primario navy
    <warnings/>                                  ← acá viven warnings + errores
  </aside>
</main>
```

### 3.2 CSS clave del nuevo `main`

```css
main.workspace {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: var(--sp-8);
  padding: var(--sp-6);
  max-width: 1200px;
  margin: 0 auto;
}

aside.resumen {
  position: sticky;
  top: var(--sp-6);
  align-self: start;            /* clave: no estirar al alto del form */
  height: fit-content;
}

@media (max-width: 980px) {
  main.workspace { grid-template-columns: 1fr; }
  aside.resumen { position: static; }
}
```

---

## 4. Cambios por archivo

| Archivo | Acción | Resumen del cambio |
|---|---|---|
| `src/styles/tokens.css` | **MODIFICAR** | Purgar verde (`--color-accent`, `--color-success` → navy); agregar `--color-rule`, `--color-aside-bg`, `--control-h-compact`, `--sp-section`. |
| `src/App.vue` | **MODIFICAR** | Quitar las dos `<section.col-*>`, los tres `<h2>` numerados y el `.generar-wrap`. Nuevo layout `main.workspace` con `<article.form>` + `<aside.resumen>` sticky. Mover `GenerarButton` y warnings al aside. |
| `src/components/Form/DatosAdolescente.vue` | **MODIFICAR** | Reemplazar `<fieldset>` con border+shadow por `<section class="form-section">` con `border-top: 1px solid var(--color-rule)` + heading inline. Quitar icono. Grid 12-col: Nombre 5 / RUN 4 / Género 3 / Domicilio 9 / Comuna 3. |
| `src/components/Form/DatosCausa.vue` | **MODIFICAR** | Mismo patrón. Grid: Tribunal full, Tipo 4 / Fecha 4 / RUC 4, RIT 4 / Delito 8, checkbox Art.37 bis inline. **Convertir `Tipo de resolución` de input libre a `<select>` con valores `oficio`, `sentencia`, `sentencia ejecutoriada`** (extraídos del backend, ver §7). |
| `src/components/Form/AdultoResponsable.vue` | **MODIFICAR** | Mismo patrón. **Collapsible**: por default colapsado mostrando solo `▸ Adulto responsable (opcional) · Agregar`. Expande al click. Si el extractor PDF lo detecta, se renderiza ya expandido y prellenado. |
| `src/components/Selectors/MedidaBotonera.vue` | **MODIFICAR** | Quitar fieldset. Heading "Medida" inline. **Mapear `SALIDAS_ALTERNATIVAS` → `Sal. Alternativas`** en el render (no en el enum). Botones h: 36px, pills sin shadow. |
| `src/components/Selectors/CentroSelector.vue` | **MODIFICAR** | Quitar fieldset. Panel "Centro asignado: X (Priorizada)" pasa de verde a gris claro con `border-left: 3px solid var(--color-primary)`. Inline con MedidaBotonera. |
| `src/components/Selectors/CoimputadoRadio.vue` | **MODIFICAR** | Pasa de card amarilla a banner sticky en la parte superior del `<article.form>`. Decisión bloqueante: visible siempre que haya múltiples candidatos. |
| `src/components/Upload/DropZone.vue` | **MODIFICAR** | Modo compacto post-carga: pasa de `padding: var(--sp-8) var(--sp-4)` (80px tall) a horizontal slim (40px tall) mostrando `Archivos cargados ✓ — [Reemplazar]`. |
| `src/components/Actions/GenerarButton.vue` | **MODIFICAR** | `background: var(--color-accent)` → `var(--color-primary)`. Mismo navy del header. Spinner y disabled-state intactos. Ahora vive dentro del aside. |
| `src/components/Actions/LimpiarButton.vue` | **NO CAMBIAR** | Ya está bien (outline en header). |
| `src/components/Login.vue` | **REVISAR** | No leído aún. Si usa `--color-accent` para CTA → aplicar mismo cambio (navy). Si no, no tocar. |
| `src/components/Icon.vue` | **NO CAMBIAR** | Agnóstico al color (hereda via `currentColor`). |
| **NUEVO** `src/components/Resumen/ResumenCaso.vue` | **CREAR** | Componente ~80 líneas que lee `useCasoStore()` y muestra: adolescente (nombre + RUN), causa (RUC/RIT), medida (sigla), centro, % completitud. |
| `src/stores/caso.ts` | **OPCIONAL** | Agregar getter `progresoPct` (campos requeridos llenados / total) si se quiere mostrar en `ResumenCaso`. Lógica de validación intacta. |

---

## 5. Mockup ASCII del resultado final

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ ▌DRM  Sistema de Derivación Virtual          21-05-2026  Juan M. Olivares  [Limpiar] [↪Salir]│
│ COORDINACIÓN JUDICIAL D.R.M. · S.N.R.S.J.                                            │
└──────────────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┬──────────────────────────────┐
│  Documentos judiciales                              │  ─── RESUMEN ──────────────  │
│  ✓ Acta_Audiencia.pdf · resolucion.docx [Reemplazar]│                              │
│  ─────────────────────────────────────────────────  │  Adolescente                 │
│                                                     │  Cristóbal García Pérez      │
│  Adolescente                                        │  22.846.782-0 · Masculino    │
│  Nombre              RUN              Género        │                              │
│  [Cristóbal García_] [22.846.782-0_]  [Masculino ▾] │  Causa                       │
│  Domicilio                            Comuna        │  RUC 2600664806-0            │
│  [Calle Falsa 123 Dpto 4__________]   [Lo Espejo_]  │  RIT 2903-2026               │
│                                                     │                              │
│  Causa                                              │  Medida                      │
│  Tribunal                                           │  ● MCA                       │
│  [Unidad Especializada RPA______________________]   │                              │
│  Tipo res.   Fecha res.   RUC          RIT          │  Centro                      │
│  [oficio ▾] [10-05-2026] [2600664806-0] [2903-2026] │  MCA Centro Sur              │
│  Delito                                             │  (Priorizada)                │
│  [robo con violencia____________________________]   │                              │
│  ☑ Informe Técnico Art. 37 bis                      │  Completitud  14/14 ✓        │
│                                                     │  ───────────────────────     │
│  ▸ Adulto responsable (opcional)                    │                              │
│                                                     │  ┌──────────────────────┐    │
│  Medida                                             │  │ ↓ Generar y          │    │
│  [MCA] [SBC] [LAS] [LAE] [LAEIP] [IP] [IRC]         │  │   descargar          │    │
│  [PSA ⓘ] [Sal. Alternativas ⓘ]                      │  │   certificado        │    │
│                                                     │  └──────────────────────┘    │
│  Centro                                             │                              │
│  │ MCA Centro Sur · Priorizada                      │  (sticky en scroll)          │
│                                                     │                              │
└─────────────────────────────────────────────────────┴──────────────────────────────┘
   Av. Pedro De Valdivia N° 4070, Ñuñoa · Fono: 22.3980.04.00
```

### 5.1 Métricas estimadas del cambio

| Medida | Antes | Después | Δ |
|---|---|---|---|
| Altura total scrolleable del viewport | ~1.700 px | ~720-820 px | **−52 %** |
| Cards con border + shadow | 5 fieldsets + 1 wrap | 0 | **−100 %** |
| Verde en la UI | Iconos legend × 5 + CTA + panel "Centro asignado" | 0 | **−100 %** |
| Títulos jerárquicos visibles | 3 H2 + 5 legends = 8 | 4 headings inline | **−50 %** |
| CTA visible sin scroll | No (vive al final) | Sí (sticky en aside) | ✓ |
| Anchura útil del form en desktop | 60 % (2fr de minmax 420/1280) | 100 % menos aside (320 px) | ~ +15 % |

---

## 6. Orden de implementación recomendado

Si se aprueba este plan, ejecutar en **6 commits incrementales** para validar visualmente en cada paso:

| # | Commit | Riesgo | Validación visual |
|---|---|---|---|
| 1 | `refactor(tokens): purgar verde de la paleta` | Bajo | Iconos de legend y CTA quedan navy. Inmediato. |
| 2 | `refactor(form): quitar fieldset+shadow de DatosAdolescente/Causa/Adulto` | Bajo | Scroll baja ~30 %. Estructura visible. |
| 3 | `refactor(selectors): unificar MedidaBotonera+CentroSelector` | Bajo | Densidad medida+centro. Fix de `SALIDAS_ALTERNATIVAS`. |
| 4 | `feat(layout): nuevo grid form+aside sticky en App.vue` | Medio | Cambio más visible. Mover GenerarButton + warnings a aside. |
| 5 | `feat(resumen): componente ResumenCaso con % completitud` | Bajo | Nuevo componente en aside. |
| 6 | `refactor(upload): DropZone compacto post-carga` | Bajo | Opcional, mejora pero no crítico. |

Cada paso es un commit aislado. Si algo no convence visualmente, se revierte sin afectar el resto.

---

## 7. Tipo de resolución — valores oficiales

El extractor del backend (`backend/src/derivacion_drm/domain/extractors/causa.py:36-43`) reconoce **exactamente 3 valores** desde el texto del PDF:

```python
def _extraer_tipo_resolucion(texto: str) -> str | None:
    t = texto.lower()
    if "sentencia ejecutoriada" in t:
        return "sentencia ejecutoriada"
    if "sentencia" in t:
        return "sentencia"
    if "oficio" in t:
        return "oficio"
    return None
```

Por consistencia entre lo que extrae el backend y lo que el usuario puede seleccionar manualmente, el `<select>` del frontend debe ofrecer estos 3 valores y solo estos:

```html
<select v-model="s.causa.tipo_resolucion">
  <option :value="null">— Seleccionar —</option>
  <option value="oficio">Oficio</option>
  <option value="sentencia">Sentencia</option>
  <option value="sentencia ejecutoriada">Sentencia ejecutoriada</option>
</select>
```

> **Nota:** los valores `value=""` que se envían al backend van en minúsculas (para coincidir con lo que el extractor produce). El label visible al usuario sí va capitalizado.

> **Pregunta abierta:** si la abogada/profesional encuentra un caso atípico (ej. "auto", "decreto"), ¿cómo lo manejamos? Opciones: (a) agregar opción "Otro" con input libre adicional; (b) mantener input libre y solo dar el `<datalist>` como sugerencias. **Decisión diferida — confirmar con usuario antes de implementar paso 2.**

---

## 8. Lo que NO cambia

- **Lógica del store** (`caso.ts`, `auth.ts`, `catalogos.ts`): intacta.
- **API contract**: cero cambios en `/extract`, `/resolver-centro`, `/generar`.
- **Validaciones del BRD** (RN-01 a RN-12): los `validationErrors` del store siguen exactamente igual; solo cambia *dónde* se renderizan (aside, no abajo).
- **Documento Word de salida**: cero cambios. Reglas RN-10 / RN-11 (Bookman Old Style 12 pt, márgenes 2.5 cm, etc.) viven en el backend.
- **Nombre de archivo de salida** (`{Nombre}_{Medida}[_{Centro}]_{Tribunal}_{RIT}_{RUC}.docx`): igual.
- **Comportamiento del botón Limpiar**: igual.
- **Login**: misma estructura, solo se aplican los nuevos colores si usa `--color-accent`.
- **Tipografía** (EB Garamond + Lato): se mantiene.

---

## 9. Riesgos identificados

| Riesgo | Mitigación |
|---|---|
| Cambio de paleta puede romper contraste en algún estado no detectado | Verificar contraste navy-sobre-blanco y blanco-sobre-navy con devtools (ratio ≥ 4.5:1). Ya cumplen por diseño. |
| `position: sticky` del aside puede no funcionar en algún viewport raro | Fallback con `@media (max-width: 980px)`: aside pasa a estático abajo. |
| Sin verde, el feedback positivo del "Centro asignado" pierde fuerza visual | Sustituir verde por borde-izq navy 3px + icono check sutil. La info sigue siendo escaneable. |
| Cambiar `tipo_resolucion` a select cerrado puede rechazar valores válidos atípicos | Ver §7 pregunta abierta — decidir antes del commit 2. |
| Collapse de Adulto responsable puede ocultar info ya extraída | Por defecto, si el extractor encontró datos, viene expandido. Solo colapsa cuando está vacío. |

---

## 10. Aprobación

- [ ] Diagnóstico (§1) entendido y validado
- [ ] Paleta y tokens (§2) aprobados
- [ ] Layout y mockup (§3, §5) aprobados
- [ ] Cambios por archivo (§4) revisados
- [ ] Orden de implementación (§6) consensuado
- [ ] Decisión sobre "tipo de resolución" en caso atípico (§7) tomada

Una vez marcados los 6 puntos: proceder con commit 1 (`refactor(tokens): purgar verde`).
