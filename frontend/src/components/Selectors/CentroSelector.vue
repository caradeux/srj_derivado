<script setup lang="ts">
import { computed } from 'vue'
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'

const s = useCasoStore()
const cat = useCatalogosStore()

const esIpIrc = computed(() => s.medida === 'IP' || s.medida === 'IRC')
const opcionesIpIrc = computed(() =>
  Object.entries(cat.centrosIpIrc).map(([sigla, c]) => ({ sigla, c })),
)
</script>

<template>
  <fieldset v-if="s.medida">
    <legend>Centro de cumplimiento</legend>

    <!-- IP/IRC: dropdown desde catálogo hardcoded -->
    <div v-if="esIpIrc">
      <label>Centro IP/IRC de ingreso
        <select
          :value="s.centroSeleccionado ? s.centroSeleccionado.nombre : ''"
          @change="(e) => {
            const t = (e.target as HTMLSelectElement).value
            s.centroSeleccionado = opcionesIpIrc.find(o => o.c.nombre === t)?.c ?? null
          }"
        >
          <option value="">— Seleccionar —</option>
          <option v-for="o in opcionesIpIrc" :key="o.sigla" :value="o.c.nombre">
            {{ o.c.nombre }}
          </option>
        </select>
      </label>
    </div>

    <!-- Estándar: radio si >1, info si =1, error si =0 -->
    <div v-else>
      <p v-if="s.centrosDisponibles.length === 0" class="error">
        Sin centros para la combinación medida × comuna.
      </p>
      <p v-else-if="s.centrosDisponibles.length === 1" class="info">
        Centro asignado: <strong>{{ s.centrosDisponibles[0].nombre }}</strong>
        ({{ s.centrosDisponibles[0].tipo }})
      </p>
      <div v-else>
        <p>Hay {{ s.centrosDisponibles.length }} centros para esta combinación. Elija uno:</p>
        <label v-for="(c, i) in s.centrosDisponibles" :key="i" class="opt">
          <input
            type="radio" name="centro"
            :value="i"
            :checked="s.centroSeleccionado?.nombre === c.nombre"
            @change="s.centroSeleccionado = c"
          />
          <span>{{ i + 1 }}. {{ c.nombre }} ({{ c.tipo }})</span>
        </label>
      </div>
    </div>
  </fieldset>
</template>

<style scoped>
fieldset { border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; }
legend { font-weight: 600; padding: 0 6px; }
label { font-size: 0.9rem; }
select { padding: 6px 8px; border: 1px solid #d0d7de; border-radius: 4px; }
.opt { display: flex; align-items: center; gap: 8px; padding: 2px 0; }
.error { color: #cf222e; font-size: 0.9rem; }
.info { color: #1a7f37; font-size: 0.9rem; }
</style>
