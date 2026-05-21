<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <section class="form-section">
    <h3>Adulto responsable <em>(opcional)</em></h3>
    <div class="form-grid">
      <label class="col-6">Nombre
        <input v-model="s.adulto.nombre" type="text" />
      </label>
      <label class="col-6">Teléfono
        <input v-model="s.adulto.telefono" type="text" />
      </label>
    </div>
  </section>
</template>
