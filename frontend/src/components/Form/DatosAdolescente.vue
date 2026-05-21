<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <fieldset>
    <legend>Datos del adolescente</legend>
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
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.full { grid-column: 1 / -1; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 4px; }
input, select { padding: 6px 8px; border: 1px solid #d0d7de; border-radius: 4px; font-size: 0.95rem; }
</style>
