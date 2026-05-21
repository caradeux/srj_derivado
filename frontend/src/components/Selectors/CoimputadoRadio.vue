<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <fieldset v-if="s.candidatos.length > 1" class="aviso">
    <legend>Se detectaron {{ s.candidatos.length }} personas. Seleccione el imputado:</legend>
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
.aviso { border: 1px solid #f6c244; background: #fff8c5; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.opt { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; padding: 2px 0; }
</style>
