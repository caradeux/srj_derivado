<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <button type="button" class="limpiar" @click="s.reset()" aria-label="Limpiar formulario">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <polyline points="3 6 5 6 21 6"/>
      <path d="M19 6l-2 14a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2L5 6"/>
      <path d="M10 11v6"/>
      <path d="M14 11v6"/>
      <path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/>
    </svg>
    <span>Limpiar</span>
  </button>
</template>

<style scoped>
.limpiar {
  display: inline-flex; align-items: center; gap: var(--sp-2);
  min-height: 36px;
  background: rgba(255,255,255,0.10);
  color: var(--color-on-primary);
  border: 1px solid rgba(255,255,255,0.30);
  border-radius: var(--radius);
  padding: 0 var(--sp-3);
  font-size: var(--fs-sm);
  font-weight: var(--fw-medium);
}
.limpiar:hover { background: rgba(255,255,255,0.18); border-color: rgba(255,255,255,0.50); }
.limpiar svg { width: 16px; height: 16px; }
</style>
