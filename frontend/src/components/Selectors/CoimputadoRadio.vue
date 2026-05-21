<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import Icon from '../Icon.vue'
const s = useCasoStore()
</script>

<template>
  <fieldset v-if="s.candidatos.length > 1" class="aviso">
    <legend>
      <Icon name="alert-circle" :size="18" />
      <span>Se detectaron {{ s.candidatos.length }} personas. Seleccione el imputado:</span>
    </legend>
    <label v-for="(c, i) in s.candidatos" :key="c.run + i" class="opt">
      <input
        type="radio" name="coimputado"
        :value="i"
        :checked="s.adolescente.run === c.run && s.adolescente.nombre === c.nombre"
        @change="s.seleccionarCoimputado(i)"
      />
      <span>{{ i + 1 }}. {{ c.nombre }} ({{ c.run }})</span>
    </label>
  </fieldset>
</template>

<style scoped>
.aviso {
  background: var(--color-warning-bg);
  border: 1px solid #FBBF24;
  border-left: 4px solid var(--color-warning);
  border-radius: var(--radius-md);
  padding: var(--sp-4) var(--sp-5);
  box-shadow: var(--shadow-sm);
}
legend {
  font-family: var(--font-heading);
  font-weight: var(--fw-semibold);
  font-size: var(--fs-md);
  color: var(--color-warning);
  padding: 0 var(--sp-2);
}
.opt {
  display: flex; align-items: center; gap: var(--sp-2);
  font-size: var(--fs-sm); color: var(--color-fg);
  padding: var(--sp-1) 0; cursor: pointer;
}
.opt input[type="radio"] {
  width: 18px; height: 18px; min-height: 0; padding: 0;
  accent-color: var(--color-primary);
}
</style>
