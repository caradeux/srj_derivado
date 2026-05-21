<script setup lang="ts">
import { computed } from 'vue'
import { useCasoStore } from '../../stores/caso'

const s = useCasoStore()

const adolescenteLineas = computed(() => {
  const a = s.adolescente
  if (!a.nombre && !a.run) return null
  const detalles: string[] = []
  if (a.run) detalles.push(a.run)
  if (a.genero) detalles.push(a.genero)
  return {
    titulo: a.nombre || '— Sin nombre',
    detalle: detalles.join(' · '),
  }
})

const causaLineas = computed(() => {
  const c = s.causa
  if (!c.ruc && !c.rit && !c.tribunal) return null
  const items: { label: string; value: string }[] = []
  if (c.ruc) items.push({ label: 'RUC', value: c.ruc })
  if (c.rit) items.push({ label: 'RIT', value: c.rit })
  return items
})

const centroLineas = computed(() => {
  const c = s.centroSeleccionado
  if (!c) return null
  return { nombre: c.nombre, tipo: c.tipo }
})

const estado = computed(() => {
  const errs = s.validationErrors
  if (errs.length === 0) {
    return { tipo: 'listo' as const, texto: 'Listo para generar' }
  }
  return {
    tipo: 'pendiente' as const,
    texto: errs.length === 1
      ? 'Falta 1 campo requerido'
      : `Faltan ${errs.length} campos requeridos`,
  }
})
</script>

<template>
  <section class="resumen-caso">
    <h2 class="resumen-titulo">Resumen del caso</h2>

    <div class="bloque">
      <span class="bloque-label">Adolescente</span>
      <p v-if="adolescenteLineas" class="bloque-valor">
        <strong>{{ adolescenteLineas.titulo }}</strong>
        <span v-if="adolescenteLineas.detalle" class="bloque-sub">
          {{ adolescenteLineas.detalle }}
        </span>
      </p>
      <p v-else class="bloque-vacio">— Sin datos</p>
    </div>

    <div class="bloque">
      <span class="bloque-label">Causa</span>
      <ul v-if="causaLineas" class="kv">
        <li v-for="i in causaLineas" :key="i.label">
          <span class="kv-label">{{ i.label }}</span>
          <span class="kv-value">{{ i.value }}</span>
        </li>
      </ul>
      <p v-else class="bloque-vacio">— Sin datos</p>
    </div>

    <div class="bloque">
      <span class="bloque-label">Medida</span>
      <p v-if="s.medida" class="bloque-valor">
        <span class="medida-dot" aria-hidden="true"></span>
        <strong>{{ s.medida }}</strong>
      </p>
      <p v-else class="bloque-vacio">— Sin medida</p>
    </div>

    <div class="bloque">
      <span class="bloque-label">Centro</span>
      <p v-if="centroLineas" class="bloque-valor">
        <strong>{{ centroLineas.nombre }}</strong>
        <span class="bloque-sub">({{ centroLineas.tipo }})</span>
      </p>
      <p v-else class="bloque-vacio">— Sin centro asignado</p>
    </div>

    <div :class="['estado', `estado-${estado.tipo}`]">
      <svg v-if="estado.tipo === 'listo'" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round"
           stroke-linejoin="round" aria-hidden="true">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
      <svg v-else viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
           stroke-linejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <span>{{ estado.texto }}</span>
    </div>
  </section>
</template>

<style scoped>
.resumen-caso {
  display: flex; flex-direction: column;
  gap: var(--sp-3);
}
.resumen-titulo {
  margin: 0;
  font-size: var(--fs-xs);
  font-weight: var(--fw-semibold);
  color: var(--color-fg-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding-bottom: var(--sp-2);
  border-bottom: 1px solid var(--color-border);
}
.bloque {
  display: flex; flex-direction: column;
  gap: 2px;
}
.bloque-label {
  font-size: var(--fs-xs);
  color: var(--color-fg-subtle);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-weight: var(--fw-medium);
}
.bloque-valor {
  margin: 0;
  font-size: var(--fs-sm);
  color: var(--color-fg);
  line-height: var(--lh-tight);
  display: flex; flex-direction: column;
  gap: 2px;
}
.bloque-valor strong {
  font-weight: var(--fw-semibold);
}
.bloque-sub {
  font-size: var(--fs-xs);
  color: var(--color-fg-muted);
}
.bloque-vacio {
  margin: 0;
  font-size: var(--fs-sm);
  color: var(--color-fg-subtle);
  font-style: italic;
}

.kv {
  list-style: none;
  margin: 0; padding: 0;
  display: flex; flex-direction: column; gap: 2px;
}
.kv li {
  display: flex; align-items: baseline;
  gap: var(--sp-2);
  font-size: var(--fs-sm);
}
.kv-label {
  font-family: var(--font-mono);
  font-size: var(--fs-xs);
  color: var(--color-fg-subtle);
  min-width: 32px;
}
.kv-value {
  color: var(--color-fg);
  font-variant-numeric: tabular-nums;
}

.medida-dot {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--color-primary);
  margin-right: var(--sp-1);
  vertical-align: middle;
}
.bloque-valor:has(.medida-dot) {
  flex-direction: row; align-items: center;
}

.estado {
  display: flex; align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-2) var(--sp-3);
  border-radius: var(--radius);
  font-size: var(--fs-sm);
  font-weight: var(--fw-medium);
  border-left-width: 3px;
  border-left-style: solid;
  margin-top: var(--sp-1);
}
.estado svg {
  width: 16px; height: 16px;
  flex-shrink: 0;
}
.estado-listo {
  background: var(--color-surface-muted);
  color: var(--color-primary);
  border-left-color: var(--color-primary);
}
.estado-pendiente {
  background: var(--color-warning-bg);
  color: var(--color-warning);
  border-left-color: var(--color-warning);
}
</style>
