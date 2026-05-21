<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'
import DelitoCombobox from './DelitoCombobox.vue'
const s = useCasoStore()
const cat = useCatalogosStore()
</script>

<template>
  <section class="form-section">
    <h3>Datos de la causa</h3>
    <div class="form-grid">
      <label class="col-12">Tribunal
        <input v-model="s.causa.tribunal" type="text" />
      </label>
      <label class="col-4">Tipo de resolución
        <input v-model="s.causa.tipo_resolucion" type="text" />
      </label>
      <label class="col-4">Fecha de resolución
        <input v-model="s.causa.fecha_resolucion" type="date" />
      </label>
      <label class="col-4">RUC
        <input v-model="s.causa.ruc" type="text" />
      </label>
      <label class="col-4">RIT
        <input v-model="s.causa.rit" type="text" />
      </label>
      <label class="col-8">Delito
        <DelitoCombobox v-model="s.causa.delito" :opciones="cat.delitos" />
      </label>
      <label class="col-12 checkbox-inline">
        <input v-model="s.causa.art_37_bis" type="checkbox" />
        Informe Técnico Art. 37 bis
      </label>
    </div>
  </section>
</template>
