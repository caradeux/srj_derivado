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
