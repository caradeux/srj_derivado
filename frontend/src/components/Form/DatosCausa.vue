<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'
import Icon from '../Icon.vue'
const s = useCasoStore()
const cat = useCatalogosStore()
</script>

<template>
  <fieldset>
    <legend>
      <Icon name="file-text" :size="18" />
      <span>Datos de la causa</span>
    </legend>
    <div class="grid">
      <label class="full">Tribunal
        <input v-model="s.causa.tribunal" type="text" />
      </label>
      <label>Tipo de resolución
        <input v-model="s.causa.tipo_resolucion" type="text" />
      </label>
      <label>Fecha de resolución
        <input v-model="s.causa.fecha_resolucion" type="date" />
      </label>
      <label>RUC
        <input v-model="s.causa.ruc" type="text" />
      </label>
      <label>RIT
        <input v-model="s.causa.rit" type="text" />
      </label>
      <label class="full">Delito
        <input v-model="s.causa.delito" type="text" list="delitos-list" />
        <datalist id="delitos-list">
          <option v-for="d in cat.delitos" :key="d" :value="d" />
        </datalist>
      </label>
      <label class="checkbox">
        <input v-model="s.causa.art_37_bis" type="checkbox" />
        Informe Técnico Art. 37 bis
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
.checkbox {
  flex-direction: row; align-items: center; gap: var(--sp-2);
  padding: var(--sp-2) 0; color: var(--color-fg);
}
.checkbox input[type="checkbox"] {
  width: 18px; height: 18px; min-height: 0; padding: 0;
  accent-color: var(--color-primary);
}
label {
  display: flex; flex-direction: column; gap: var(--sp-1);
  font-size: var(--fs-sm); font-weight: var(--fw-medium); color: var(--color-fg-muted);
}
</style>
