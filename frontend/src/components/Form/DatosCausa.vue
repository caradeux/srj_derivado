<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'
const s = useCasoStore()
const cat = useCatalogosStore()
</script>

<template>
  <fieldset>
    <legend>Datos de la causa</legend>
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
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.full { grid-column: 1 / -1; }
.checkbox { flex-direction: row; align-items: center; gap: 8px; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 4px; }
input { padding: 6px 8px; border: 1px solid #d0d7de; border-radius: 4px; font-size: 0.95rem; }
</style>
