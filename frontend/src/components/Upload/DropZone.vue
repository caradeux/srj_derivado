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
      <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="17 8 12 3 7 8"/>
        <line x1="12" y1="3" x2="12" y2="15"/>
      </svg>
      <p class="dz-title">Arrastre aquí los documentos</p>
      <p class="dz-hint">Formatos aceptados: PDF · DOCX</p>
      <label class="select">
        <input type="file" multiple accept=".pdf,.docx" @change="onChange" />
        Seleccionar archivos
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

    <p v-if="error" class="error" role="alert">{{ error }}</p>
  </section>
</template>

<style scoped>
.drop-zone-wrap { display: flex; flex-direction: column; gap: var(--sp-3); }

.drop-zone {
  display: flex; flex-direction: column; align-items: center; gap: var(--sp-2);
  border: 2px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  padding: var(--sp-8) var(--sp-4);
  text-align: center;
  background: var(--color-surface);
  color: var(--color-fg-muted);
  transition: background var(--t-base), border-color var(--t-base);
}
.drop-zone.over {
  background: rgba(30, 58, 95, 0.04);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.upload-icon {
  width: 40px; height: 40px;
  color: var(--color-primary);
  opacity: 0.7;
}

.dz-title {
  margin: 0; font-size: var(--fs-base); font-weight: var(--fw-semibold);
  color: var(--color-fg);
}
.dz-hint {
  margin: 0; font-size: var(--fs-xs);
  color: var(--color-fg-subtle); letter-spacing: 0.02em;
  text-transform: uppercase;
}

.select {
  display: inline-flex; align-items: center;
  margin-top: var(--sp-2);
  padding: var(--sp-2) var(--sp-4);
  background: var(--color-surface-muted);
  color: var(--color-primary);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius);
  font-size: var(--fs-sm);
  font-weight: var(--fw-semibold);
  cursor: pointer;
  transition: background var(--t-fast), border-color var(--t-fast);
}
.select:hover { background: var(--color-surface); border-color: var(--color-primary); }
.select input { display: none; }

.lista { display: flex; flex-direction: column; gap: var(--sp-1); }

.primary {
  min-height: var(--control-h-lg);
  background: var(--color-primary);
  color: var(--color-on-primary);
  border: 1px solid var(--color-primary);
  padding: 0 var(--sp-4);
  font-size: var(--fs-sm);
  font-weight: var(--fw-semibold);
}
.primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
}
.primary:disabled {
  opacity: 0.45;
  background: var(--color-fg-subtle);
  border-color: var(--color-fg-subtle);
}

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
