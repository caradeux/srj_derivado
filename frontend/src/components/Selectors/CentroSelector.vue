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
  <section v-if="s.medida" class="form-section">
    <h3>Centro de cumplimiento</h3>

    <div v-if="esIpIrc" class="form-grid">
      <label class="col-12">Centro IP/IRC de ingreso
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

    <div v-else>
      <p v-if="s.centrosDisponibles.length === 0" class="banner banner-error">
        Sin centros para la combinación medida × comuna.
      </p>
      <p v-else-if="s.centrosDisponibles.length === 1" class="banner banner-info">
        Centro asignado: <strong>{{ s.centrosDisponibles[0].nombre }}</strong>
        <span class="tipo">({{ s.centrosDisponibles[0].tipo }})</span>
      </p>
      <div v-else class="opciones">
        <p class="opciones-titulo">
          Hay {{ s.centrosDisponibles.length }} centros para esta combinación. Elija uno:
        </p>
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
  </section>
</template>

<style scoped>
.banner {
  border-radius: var(--radius);
  padding: var(--sp-2) var(--sp-3);
  font-size: var(--fs-sm);
  margin: 0;
}
.banner-info {
  background: var(--color-surface-muted);
  color: var(--color-fg);
  border-left: 3px solid var(--color-primary);
}
.banner-info .tipo {
  color: var(--color-fg-subtle);
  margin-left: var(--sp-1);
}
.banner-error {
  background: var(--color-danger-bg);
  color: var(--color-danger);
  border-left: 3px solid var(--color-danger);
}

.opciones { display: flex; flex-direction: column; gap: var(--sp-1); }
.opciones-titulo {
  font-size: var(--fs-sm);
  color: var(--color-fg-muted);
  margin: 0 0 var(--sp-1);
}
.opt {
  display: flex; align-items: center; gap: var(--sp-2);
  padding: var(--sp-1) 0;
  font-size: var(--fs-sm); color: var(--color-fg);
  cursor: pointer;
}
.opt input[type="radio"] {
  width: 18px; height: 18px; min-height: 0; padding: 0;
  accent-color: var(--color-primary);
}
</style>
