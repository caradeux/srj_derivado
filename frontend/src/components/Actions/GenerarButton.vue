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
