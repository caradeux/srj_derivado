<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
import { useCatalogosStore } from '../../stores/catalogos'
import type { Medida } from '../../api/client'
import Icon from '../Icon.vue'

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
    <legend>
      <Icon name="scale" :size="18" />
      <span>Medida</span>
    </legend>
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
fieldset {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  padding: var(--sp-4) var(--sp-5);
}
legend {
  display: inline-flex; align-items: center; gap: var(--sp-2);
  font-family: var(--font-heading);
  font-weight: var(--fw-semibold);
  font-size: var(--fs-md);
  color: var(--color-primary);
  padding: 0 var(--sp-2);
}
legend :deep(.icon) { color: var(--color-accent); }
.botonera {
  display: flex; flex-wrap: wrap; gap: var(--sp-2);
  margin-top: var(--sp-2);
}
.btn-medida {
  min-height: var(--control-h-lg);
  min-width: 72px;
  padding: 0 var(--sp-4);
  border: 1px solid var(--color-border-strong);
  background: var(--color-surface);
  color: var(--color-fg);
  border-radius: var(--radius);
  font-family: var(--font-body);
  font-weight: var(--fw-semibold);
  font-size: var(--fs-sm);
  letter-spacing: 0.02em;
  transition: background var(--t-fast), border-color var(--t-fast),
              color var(--t-fast), transform var(--t-fast);
}
.btn-medida:hover:not(.pendiente):not(.activa) {
  background: var(--color-surface-muted);
  border-color: var(--color-primary);
}
.btn-medida.activa {
  background: var(--color-primary);
  color: var(--color-on-primary);
  border-color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}
.btn-medida.pendiente {
  opacity: 0.40;
  background: var(--color-surface-muted);
}
.btn-medida:active:not(.pendiente) { transform: translateY(1px); }
</style>
