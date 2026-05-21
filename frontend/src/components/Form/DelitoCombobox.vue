<script setup lang="ts">
import { ref, computed, nextTick, useTemplateRef } from 'vue'

const props = defineProps<{
  modelValue: string | null | undefined
  opciones: string[]
  placeholder?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: string): void
}>()

const MAX_VISIBLES = 8

const abierto = ref(false)
const indiceActivo = ref(-1)
const inputEl = useTemplateRef<HTMLInputElement>('inputEl')
const listaEl = useTemplateRef<HTMLUListElement>('listaEl')

const valor = computed({
  get: () => props.modelValue ?? '',
  set: (v: string) => emit('update:modelValue', v),
})

function _normalizar(s: string): string {
  return s.toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
}

const resultados = computed(() => {
  const q = _normalizar(valor.value.trim())
  if (!q) return props.opciones.slice(0, MAX_VISIBLES)
  return props.opciones.filter(o => _normalizar(o).includes(q)).slice(0, MAX_VISIBLES)
})

const restantes = computed(() => {
  const q = _normalizar(valor.value.trim())
  const total = q
    ? props.opciones.filter(o => _normalizar(o).includes(q)).length
    : props.opciones.length
  return Math.max(0, total - resultados.value.length)
})

function abrir() {
  abierto.value = true
  indiceActivo.value = resultados.value.length > 0 ? 0 : -1
}

function cerrar() {
  abierto.value = false
  indiceActivo.value = -1
}

function seleccionar(opcion: string) {
  emit('update:modelValue', opcion)
  cerrar()
  inputEl.value?.blur()
}

function onInput(e: Event) {
  const v = (e.target as HTMLInputElement).value
  emit('update:modelValue', v)
  abierto.value = true
  indiceActivo.value = 0
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'ArrowDown') {
    e.preventDefault()
    if (!abierto.value) { abrir(); return }
    indiceActivo.value = Math.min(indiceActivo.value + 1, resultados.value.length - 1)
    _scrollVisible()
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    if (!abierto.value) return
    indiceActivo.value = Math.max(indiceActivo.value - 1, 0)
    _scrollVisible()
  } else if (e.key === 'Enter') {
    if (abierto.value && indiceActivo.value >= 0) {
      e.preventDefault()
      seleccionar(resultados.value[indiceActivo.value])
    }
  } else if (e.key === 'Escape') {
    if (abierto.value) {
      e.preventDefault()
      cerrar()
    }
  } else if (e.key === 'Tab') {
    cerrar()
  }
}

function _scrollVisible() {
  nextTick(() => {
    const item = listaEl.value?.querySelector<HTMLElement>(`[data-idx="${indiceActivo.value}"]`)
    item?.scrollIntoView({ block: 'nearest' })
  })
}

function onBlur() {
  // Pequeño delay para permitir click en opción antes de cerrar
  setTimeout(() => { abierto.value = false }, 120)
}
</script>

<template>
  <div class="dc">
    <input
      ref="inputEl"
      type="text"
      :value="valor"
      :placeholder="placeholder ?? 'Escriba para buscar o seleccione…'"
      role="combobox"
      :aria-expanded="abierto"
      aria-autocomplete="list"
      aria-controls="dc-listbox"
      :aria-activedescendant="abierto && indiceActivo >= 0 ? `dc-opt-${indiceActivo}` : undefined"
      autocomplete="off"
      @input="onInput"
      @focus="abrir"
      @blur="onBlur"
      @keydown="onKeydown"
    />
    <button
      type="button"
      class="caret"
      :aria-label="abierto ? 'Cerrar lista' : 'Abrir lista'"
      tabindex="-1"
      @mousedown.prevent="abierto ? cerrar() : (inputEl?.focus(), abrir())"
    >
      <svg viewBox="0 0 12 8" fill="none" stroke="currentColor"
           stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"
           :class="{ rotado: abierto }" aria-hidden="true">
        <polyline points="1 1 6 6 11 1"/>
      </svg>
    </button>

    <ul
      v-if="abierto"
      id="dc-listbox"
      ref="listaEl"
      class="dc-lista"
      role="listbox"
    >
      <li
        v-for="(opcion, i) in resultados"
        :id="`dc-opt-${i}`"
        :key="opcion"
        :data-idx="i"
        role="option"
        :aria-selected="indiceActivo === i"
        :class="['dc-opt', { activa: indiceActivo === i }]"
        @mousedown.prevent="seleccionar(opcion)"
        @mousemove="indiceActivo = i"
      >
        {{ opcion }}
      </li>
      <li v-if="resultados.length === 0" class="dc-vacio">
        Sin resultados para «{{ valor }}»
      </li>
      <li v-else-if="restantes > 0" class="dc-mas">
        + {{ restantes }} resultado{{ restantes === 1 ? '' : 's' }} más — afine la búsqueda
      </li>
    </ul>
  </div>
</template>

<style scoped>
.dc {
  position: relative;
  width: 100%;
}

.dc input {
  padding-right: var(--sp-8);
}

.caret {
  position: absolute;
  top: 50%;
  right: var(--sp-2);
  transform: translateY(-50%);
  width: 28px; height: 28px;
  display: grid; place-items: center;
  background: transparent;
  border: none;
  color: var(--color-fg-subtle);
  border-radius: var(--radius-sm);
  padding: 0;
  cursor: pointer;
}
.caret:hover { color: var(--color-primary); }
.caret svg {
  width: 12px; height: 8px;
  transition: transform var(--t-fast);
}
.caret svg.rotado { transform: rotate(180deg); }

.dc-lista {
  position: absolute;
  top: calc(100% + 4px);
  left: 0; right: 0;
  list-style: none;
  margin: 0; padding: var(--sp-1);
  background: var(--color-surface);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius);
  box-shadow: var(--shadow-md);
  max-height: 280px;
  overflow-y: auto;
  z-index: 100;
  font-size: var(--fs-sm);
  color: var(--color-fg);
}

.dc-opt {
  padding: var(--sp-2) var(--sp-3);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-weight: var(--fw-regular);
  line-height: 1.3;
}
.dc-opt.activa {
  background: var(--color-primary);
  color: var(--color-on-primary);
}

.dc-vacio {
  padding: var(--sp-3);
  color: var(--color-fg-subtle);
  font-style: italic;
  text-align: center;
}

.dc-mas {
  padding: var(--sp-2) var(--sp-3);
  margin-top: var(--sp-1);
  border-top: 1px solid var(--color-border);
  color: var(--color-fg-subtle);
  font-size: var(--fs-xs);
  text-align: center;
  font-style: italic;
}
</style>
