<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <fieldset>
    <legend>Adulto responsable (opcional)</legend>
    <div class="grid">
      <label>Nombre
        <input v-model="s.adulto.nombre" type="text" />
      </label>
      <label>Teléfono
        <input v-model="s.adulto.telefono" type="text" />
      </label>
    </div>
  </fieldset>
</template>

<style scoped>
fieldset {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  padding: var(--sp-4) var(--sp-5);
}
legend {
  font-family: var(--font-heading);
  font-weight: var(--fw-semibold);
  font-size: var(--fs-md);
  color: var(--color-primary);
  padding: 0 var(--sp-2);
}
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-3) var(--sp-4); margin-top: var(--sp-2); }
label {
  display: flex; flex-direction: column; gap: var(--sp-1);
  font-size: var(--fs-sm); font-weight: var(--fw-medium); color: var(--color-fg-muted);
}
</style>
