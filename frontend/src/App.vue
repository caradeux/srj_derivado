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
import ResumenCaso from './components/Resumen/ResumenCaso.vue'
import Login from './components/Login.vue'
import Icon from './components/Icon.vue'
import { useCasoStore } from './stores/caso'
import { useAuthStore } from './stores/auth'
const s = useCasoStore()
const auth = useAuthStore()
</script>

<template>
  <Login v-if="!auth.autenticado" />

  <template v-else>
  <a class="skip-link" href="#contenido">Saltar al contenido</a>

  <header class="appbar">
    <div class="brand">
      <div class="brand-mark" aria-hidden="true">DRM</div>
      <div class="brand-text">
        <h1>Sistema de Derivación Virtual</h1>
        <p class="subtitle">Coordinación Judicial D.R.M. · S.N.R.S.J.</p>
      </div>
    </div>
    <div class="meta">
      <label class="meta-field">
        <span>Fecha emisión</span>
        <input v-model="s.fechaEmision" type="date" />
      </label>
      <label class="meta-field meta-field--prof">
        <span>Profesional firmante</span>
        <input v-model="s.profesional" type="text" />
      </label>
      <LimpiarButton />
      <button type="button" class="logout-btn" @click="auth.cerrarSesion()"
              aria-label="Cerrar sesión">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/>
          <line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
        <span>Cerrar sesión</span>
      </button>
    </div>
  </header>

  <main id="contenido" class="workspace">
    <article class="form">
      <CoimputadoRadio />

      <section class="form-section">
        <h3>Documentos judiciales</h3>
        <DropZone />
      </section>

      <DatosAdolescente />
      <DatosCausa />
      <AdultoResponsable />
      <MedidaBotonera />
      <CentroSelector />
    </article>

    <aside class="resumen" aria-label="Resumen y acciones">
      <ResumenCaso />
      <GenerarButton />
      <ul v-if="s.warnings.length > 0" class="warns" role="status" aria-live="polite">
        <li v-for="w in s.warnings" :key="w">
          <Icon name="alert-triangle" :size="18" />
          <span>{{ w }}</span>
        </li>
      </ul>
    </aside>
  </main>

  <footer class="appfoot">
    Av. Pedro De Valdivia N° 4070, Ñuñoa · Fono: 22.3980.04.00
  </footer>
  </template>
</template>

<style>
.skip-link {
  position: absolute;
  left: -10000px;
  top: var(--sp-2);
  background: var(--color-primary);
  color: var(--color-on-primary);
  padding: var(--sp-2) var(--sp-3);
  border-radius: var(--radius);
  font-weight: var(--fw-semibold);
  z-index: 1000;
}
.skip-link:focus { left: var(--sp-4); }

.appbar {
  display: flex; align-items: center; justify-content: space-between;
  gap: var(--sp-6);
  padding: var(--sp-4) var(--sp-6);
  background: var(--color-primary);
  color: var(--color-on-primary);
  border-bottom: 1px solid var(--color-primary-hover);
}

.brand { display: flex; align-items: center; gap: var(--sp-3); }
.brand-mark {
  width: 44px; height: 44px;
  display: grid; place-items: center;
  background: rgba(255,255,255,0.10);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: var(--radius-md);
  font-family: var(--font-heading);
  font-weight: var(--fw-bold);
  font-size: var(--fs-md);
  letter-spacing: 0.04em;
}
.brand-text h1 {
  font-size: var(--fs-lg);
  color: var(--color-on-primary);
  line-height: 1.2;
}
.subtitle {
  margin: 2px 0 0;
  font-size: var(--fs-xs);
  color: rgba(255,255,255,0.78);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.meta { display: flex; align-items: flex-end; gap: var(--sp-3); }
.meta-field { display: flex; flex-direction: column; gap: 4px; }
.meta-field span {
  font-size: var(--fs-xs);
  color: rgba(255,255,255,0.78);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}
.meta-field input {
  min-height: 36px;
  background: rgba(255,255,255,0.92);
  border: 1px solid rgba(255,255,255,0.35);
  font-size: var(--fs-sm);
}
.meta-field--prof input { min-width: 240px; }

.logout-btn {
  display: inline-flex; align-items: center; gap: var(--sp-2);
  min-height: 36px;
  background: transparent;
  color: var(--color-on-primary);
  border: 1px solid rgba(255,255,255,0.30);
  border-radius: var(--radius);
  padding: 0 var(--sp-3);
  font-size: var(--fs-sm);
  font-weight: var(--fw-medium);
}
.logout-btn:hover { background: rgba(255,255,255,0.10); border-color: rgba(255,255,255,0.50); }
.logout-btn svg { width: 16px; height: 16px; }

/* Workspace: form a la izquierda, resumen sticky a la derecha */
main.workspace {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: var(--sp-8);
  padding: var(--sp-6);
  max-width: 1200px;
  margin: 0 auto;
}

.form { min-width: 0; }
.form > .form-section:first-child,
.form > .form-section:first-of-type {
  padding-top: 0;
}

aside.resumen {
  position: sticky;
  top: var(--sp-6);
  align-self: start;
  height: fit-content;
  background: var(--color-aside-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--sp-4);
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}
.warns {
  background: var(--color-warning-bg);
  color: var(--color-warning);
  border: 1px solid #fcd34d;
  border-radius: var(--radius);
  padding: var(--sp-2) var(--sp-3);
  margin: 0;
  font-size: var(--fs-sm);
  list-style: none;
}
.warns li {
  display: flex; align-items: flex-start; gap: var(--sp-2);
  padding: var(--sp-1) 0;
}
.warns li svg { width: 16px; height: 16px; flex-shrink: 0; margin-top: 2px; }

.appfoot {
  text-align: center;
  padding: var(--sp-4);
  font-size: var(--fs-xs);
  color: var(--color-fg-subtle);
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
}

@media (max-width: 980px) {
  .appbar { flex-direction: column; align-items: stretch; gap: var(--sp-3); }
  main.workspace { grid-template-columns: 1fr; padding: var(--sp-4); gap: var(--sp-6); }
  aside.resumen { position: static; }
  .meta { flex-wrap: wrap; }
}
</style>
