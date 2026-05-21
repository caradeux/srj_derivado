<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'
import type { Medida } from '../../api/client'

const s = useCasoStore()
const cat = useCatalogosStore()

async function elegir(sigla: string, estado: string) {
  if (estado === 'pendiente') return
  s.medida = sigla as Medida
  await s.resolverCentros()
}
</script>

<template>
  <fieldset>
    <legend>Medida</legend>
    <div class="botonera">
      <button
        v-for="m in cat.medidas"
        :key="m.sigla"
        type="button"
        :class="['btn-medida', {
          activa: s.medida === m.sigla,
          pendiente: m.estado === 'pendiente',
        }]"
        :disabled="m.estado === 'pendiente'"
        :title="m.estado === 'pendiente'
          ? 'Pendiente de formato — disponible en próxima versión'
          : m.nombre + ' (' + m.base_legal + ')'"
        @click="elegir(m.sigla, m.estado)"
      >
        {{ m.sigla }}
      </button>
    </div>
  </fieldset>
</template>

<style scoped>
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
.botonera { display: flex; flex-wrap: wrap; gap: 6px; }
.btn-medida {
  border: 1px solid #d0d7de; background: #f6f8fa; color: #24292f;
  padding: 6px 14px; border-radius: 6px; cursor: pointer;
  font-weight: 600; font-size: 0.9rem; min-width: 64px;
}
.btn-medida.activa { background: #0969da; color: #fff; border-color: #0969da; }
.btn-medida.pendiente { opacity: 0.45; cursor: not-allowed; }
.btn-medida:hover:not(.pendiente):not(.activa) { background: #e6e8ea; }
</style>
