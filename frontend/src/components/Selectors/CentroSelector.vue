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
fieldset {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  padding: var(--sp-4) var(--sp-5);
}
legend {
  font-family: var(--font-heading);
  font-weight: var(--fw-semibold);
  font-size: var(--fs-md);
  color: var(--color-primary);
  padding: 0 var(--sp-2);
}
label {
  display: flex; flex-direction: column; gap: var(--sp-1);
  font-size: var(--fs-sm); font-weight: var(--fw-medium);
  color: var(--color-fg-muted);
  margin-top: var(--sp-2);
}
.opt {
  display: flex; flex-direction: row; align-items: center; gap: var(--sp-2);
  padding: var(--sp-1) 0; font-size: var(--fs-sm);
  color: var(--color-fg); cursor: pointer;
  margin-top: 0;
}
.opt input[type="radio"] {
  width: 18px; height: 18px; min-height: 0; padding: 0;
  accent-color: var(--color-primary);
}
.error {
  color: var(--color-danger);
  background: var(--color-danger-bg);
  border: 1px solid #FECACA;
  border-radius: var(--radius);
  padding: var(--sp-2) var(--sp-3);
  font-size: var(--fs-sm);
  margin: var(--sp-2) 0 0;
}
.info {
  color: var(--color-success);
  background: var(--color-success-bg);
  border: 1px solid #A7F3D0;
  border-radius: var(--radius);
  padding: var(--sp-2) var(--sp-3);
  font-size: var(--fs-sm);
  margin: var(--sp-2) 0 0;
}
</style>
