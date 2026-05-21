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
      <svg v-if="!s.generando" class="icon" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
           stroke-linejoin="round" aria-hidden="true">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7 10 12 15 17 10"/>
        <line x1="12" y1="15" x2="12" y2="3"/>
      </svg>
      <svg v-else class="icon spin" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
        <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
      </svg>
      <span>{{ s.generando ? 'Generando…' : 'Generar y descargar certificado' }}</span>
    </button>
    <ul v-if="s.validationErrors.length > 0" class="errs">
      <li v-for="e in s.validationErrors" :key="e">{{ e }}</li>
    </ul>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
  </div>
</template>

<style scoped>
.generar { display: flex; flex-direction: column; gap: var(--sp-2); }
.primary {
  display: inline-flex; align-items: center; justify-content: center;
  gap: var(--sp-2);
  min-height: 48px;
  background: var(--color-accent);
  color: var(--color-on-primary);
  border: 1px solid var(--color-accent);
  padding: 0 var(--sp-5);
  font-size: var(--fs-base);
  font-weight: var(--fw-semibold);
  letter-spacing: 0.01em;
  box-shadow: var(--shadow-sm);
}
.primary:hover:not(:disabled) {
  background: var(--color-accent-hover);
  border-color: var(--color-accent-hover);
}
.primary:disabled {
  background: var(--color-fg-subtle);
  border-color: var(--color-fg-subtle);
  opacity: 0.7;
}
.icon { width: 20px; height: 20px; }
.spin { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .spin { animation: none; } }

.errs {
  background: var(--color-warning-bg);
  color: var(--color-warning);
  border: 1px solid #FCD34D;
  border-radius: var(--radius);
  padding: var(--sp-2) var(--sp-3);
  margin: 0;
  font-size: var(--fs-sm);
  list-style: none;
}
.errs li { padding: 2px 0; }
.errs li::before { content: "•  "; font-weight: var(--fw-bold); }

.error {
  color: var(--color-danger);
  background: var(--color-danger-bg);
  border: 1px solid #FECACA;
  border-radius: var(--radius);
  padding: var(--sp-2) var(--sp-3);
  font-size: var(--fs-sm);
  margin: 0;
}
</style>
