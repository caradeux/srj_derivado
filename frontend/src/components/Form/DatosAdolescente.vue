<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import Icon from '../Icon.vue'
const s = useCasoStore()
</script>

<template>
  <fieldset>
    <legend>
      <Icon name="user" :size="18" />
      <span>Datos del adolescente</span>
    </legend>
    <div class="grid">
      <label>Nombre
        <input v-model="s.adolescente.nombre" type="text" />
      </label>
      <label>RUN
        <input v-model="s.adolescente.run" type="text" placeholder="XX.XXX.XXX-X" />
      </label>
      <label>Género
        <select v-model="s.adolescente.genero">
          <option :value="null">— Seleccionar —</option>
          <option value="Masculino">Masculino</option>
          <option value="Femenino">Femenino</option>
        </select>
      </label>
      <label class="full">Domicilio
        <input v-model="s.adolescente.domicilio" type="text" />
      </label>
      <label>Comuna
        <input v-model="s.adolescente.comuna" type="text" @change="s.resolverCentros()" />
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
  display: inline-flex; align-items: center; gap: var(--sp-2);
  font-family: var(--font-heading);
  font-weight: var(--fw-semibold);
  font-size: var(--fs-md);
  color: var(--color-primary);
  padding: 0 var(--sp-2);
}
legend :deep(.icon) { color: var(--color-accent); }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-3) var(--sp-4); margin-top: var(--sp-2); }
.full { grid-column: 1 / -1; }
label {
  display: flex; flex-direction: column; gap: var(--sp-1);
  font-size: var(--fs-sm); font-weight: var(--fw-medium); color: var(--color-fg-muted);
}
</style>
