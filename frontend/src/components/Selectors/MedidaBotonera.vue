<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'
import type { Medida } from '../../api/client'

const s = useCasoStore()
const cat = useCatalogosStore()

const LABELS_MEDIDA: Record<string, string> = {
  SALIDAS_ALTERNATIVAS: 'Sal. Alternativas',
}
const label = (sigla: string) => LABELS_MEDIDA[sigla] ?? sigla

async function elegir(sigla: string, estado: string) {
  if (estado === 'pendiente') return
  s.medida = sigla as Medida
  await s.resolverCentros()
}
</script>

<template>
  <section class="form-section">
    <h3>Medida</h3>
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
        {{ label(m.sigla) }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.botonera {
  display: flex; flex-wrap: wrap; gap: var(--sp-2);
}
.btn-medida {
  min-height: 36px;
  min-width: 64px;
  padding: 0 var(--sp-3);
  border: 1px solid var(--color-border-strong);
  background: var(--color-surface);
  color: var(--color-fg);
  border-radius: var(--radius);
  font-family: var(--font-body);
  font-weight: var(--fw-semibold);
  font-size: var(--fs-sm);
  letter-spacing: 0.02em;
  transition: background var(--t-fast), border-color var(--t-fast),
              color var(--t-fast);
}
.btn-medida:hover:not(.pendiente):not(.activa) {
  background: var(--color-surface-muted);
  border-color: var(--color-primary);
}
.btn-medida.activa {
  background: var(--color-primary);
  color: var(--color-on-primary);
  border-color: var(--color-primary);
}
.btn-medida.pendiente {
  opacity: 0.40;
  background: var(--color-surface-muted);
}
</style>
