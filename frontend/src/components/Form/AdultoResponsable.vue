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
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 4px; }
input { padding: 6px 8px; border: 1px solid #d0d7de; border-radius: 4px; font-size: 0.95rem; }
</style>
