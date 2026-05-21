<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <section class="form-section">
    <h3>Datos del adolescente</h3>
    <div class="form-grid">
      <label class="col-5">Nombre
        <input v-model="s.adolescente.nombre" type="text" />
      </label>
      <label class="col-4">RUN
        <input v-model="s.adolescente.run" type="text" placeholder="XX.XXX.XXX-X" />
      </label>
      <label class="col-3">Género
        <select v-model="s.adolescente.genero">
          <option :value="null">— Seleccionar —</option>
          <option value="Masculino">Masculino</option>
          <option value="Femenino">Femenino</option>
        </select>
      </label>
      <label class="col-9">Domicilio
        <input v-model="s.adolescente.domicilio" type="text" />
      </label>
      <label class="col-3">Comuna
        <input v-model="s.adolescente.comuna" type="text" @change="s.resolverCentros()" />
      </label>
    </div>
  </section>
</template>
