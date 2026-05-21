<script setup lang="ts">
import DropZone from './components/Upload/DropZone.vue'
import DatosAdolescente from './components/Form/DatosAdolescente.vue'
import DatosCausa from './components/Form/DatosCausa.vue'
import AdultoResponsable from './components/Form/AdultoResponsable.vue'
import CoimputadoRadio from './components/Selectors/CoimputadoRadio.vue'
import MedidaBotonera from './components/Selectors/MedidaBotonera.vue'
import CentroSelector from './components/Selectors/CentroSelector.vue'
import GenerarButton from './components/Actions/GenerarButton.vue'
import LimpiarButton from './components/Actions/LimpiarButton.vue'
import { useCasoStore } from './stores/caso'
const s = useCasoStore()
</script>

<template>
  <header>
    <h1>Sistema de Derivación Virtual — D.R.M.</h1>
    <div class="meta">
      <label>Fecha emisión <input v-model="s.fechaEmision" type="date" /></label>
      <label>Profesional <input v-model="s.profesional" type="text" /></label>
      <LimpiarButton />
    </div>
  </header>

  <main>
    <div class="col-izq">
      <DropZone />
      <CoimputadoRadio />
    </div>

    <div class="col-der">
      <DatosAdolescente />
      <DatosCausa />
      <AdultoResponsable />
      <MedidaBotonera />
      <CentroSelector />
      <GenerarButton />

      <ul v-if="s.warnings.length > 0" class="warns">
        <li v-for="w in s.warnings" :key="w">⚠️ {{ w }}</li>
      </ul>
    </div>
  </main>
</template>

<style>
* { box-sizing: border-box; }
body { margin: 0; font-family: Segoe UI, Roboto, sans-serif; color: #24292f; background: #fff; }
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 24px; border-bottom: 1px solid #d0d7de; background: #f6f8fa;
}
header h1 { font-size: 1.1rem; margin: 0; }
.meta { display: flex; align-items: center; gap: 12px; font-size: 0.85rem; }
.meta input { padding: 4px 6px; border: 1px solid #d0d7de; border-radius: 4px; }
main {
  display: grid; grid-template-columns: 1fr 2fr; gap: 16px;
  padding: 16px 24px; max-width: 1280px; margin: 0 auto;
}
.col-izq, .col-der { display: flex; flex-direction: column; gap: 12px; }
.warns { color: #9a6700; font-size: 0.85rem; margin: 4px 0; padding-left: 20px; }
</style>
