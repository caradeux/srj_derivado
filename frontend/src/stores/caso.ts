import { defineStore } from 'pinia'
import {
  api, type Adolescente, type AdultoResponsable, type CasoDerivacion,
  type Causa, type CentroAsignado, type ExtractionResult, type Medida,
} from '../api/client'

interface State {
  fechaEmision: string
  profesional: string
  candidatos: Adolescente[]
  adolescente: Adolescente
  causa: Causa
  adulto: AdultoResponsable
  medida: Medida | null
  centrosDisponibles: CentroAsignado[]
  centroSeleccionado: CentroAsignado | null
  warnings: string[]
  generando: boolean
}

const _hoyIso = () => new Date().toISOString().slice(0, 10)

const _adolescenteVacio = (): Adolescente => ({
  nombre: '', run: '', genero: null, domicilio: null, comuna: null,
})

const _causaVacia = (): Causa => ({
  tribunal: null, tipo_resolucion: null, ruc: null, rit: null,
  delito: null, fecha_resolucion: null, art_37_bis: false,
})

export const useCasoStore = defineStore('caso', {
  state: (): State => ({
    fechaEmision: _hoyIso(),
    profesional: 'Juan Manuel Olivares Oyarzún',
    candidatos: [],
    adolescente: _adolescenteVacio(),
    causa: _causaVacia(),
    adulto: { nombre: null, telefono: null },
    medida: null,
    centrosDisponibles: [],
    centroSeleccionado: null,
    warnings: [],
    generando: false,
  }),

  getters: {
    validationErrors(state): string[] {
      const errs: string[] = []
      if (!state.adolescente.nombre) errs.push('Falta nombre del adolescente.')
      if (!state.adolescente.genero) errs.push('Falta género.')
      if (!state.medida) errs.push('Falta medida.')
      const esIpIrc = state.medida === 'IP' || state.medida === 'IRC'
      if (!esIpIrc && !state.adolescente.comuna) errs.push('Falta comuna.')
      if (!state.centroSeleccionado) errs.push('Falta centro.')
      return errs
    },
    listo(): boolean { return this.validationErrors.length === 0 },
  },

  actions: {
    aplicarExtraccion(r: ExtractionResult) {
      this.candidatos = r.candidatos
      this.causa = r.causa
      this.adulto = r.adulto
      this.medida = r.medida_sugerida
      this.warnings = r.warnings ?? []
      if (r.candidatos.length === 1) this.adolescente = r.candidatos[0]
    },

    seleccionarCoimputado(idx: number) {
      const c = this.candidatos[idx]
      if (c) this.adolescente = c
    },

    async resolverCentros() {
      if (!this.medida || !this.adolescente.comuna) {
        this.centrosDisponibles = []
        this.centroSeleccionado = null
        return
      }
      const ipIrc = this.medida === 'IP' || this.medida === 'IRC'
      if (ipIrc) return  // IP/IRC se selecciona via dropdown, no por resolver
      const lista = await api.resolverCentro(this.medida, this.adolescente.comuna)
      this.centrosDisponibles = lista
      this.centroSeleccionado = lista.length === 1 ? lista[0] : null
    },

    reset() {
      const fecha = this.fechaEmision
      const prof = this.profesional
      this.$reset()
      this.fechaEmision = fecha
      this.profesional = prof
    },

    async generar(): Promise<{ blob: Blob; filename: string } | null> {
      if (!this.listo) return null
      this.generando = true
      try {
        const payload = {
          caso: {
            adolescente: this.adolescente,
            causa: this.causa,
            medida: this.medida!,
            adulto: this.adulto,
            centro: this.centroSeleccionado!,
          } as CasoDerivacion,
          profesional: this.profesional,
          fecha_emision: this.fechaEmision,
        }
        return await api.generar(payload)
      } finally {
        this.generando = false
      }
    },
  },
})
