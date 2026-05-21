import { defineStore } from 'pinia'
import { api, type CentroAsignado, type CentroIPIRC, type MedidaCatalogoItem } from '../api/client'

export const useCatalogosStore = defineStore('catalogos', {
  state: () => ({
    medidas: [] as MedidaCatalogoItem[],
    centrosIpIrc: {} as Record<CentroIPIRC, CentroAsignado>,
    delitos: [] as string[],
    cargado: false,
  }),
  actions: {
    async load() {
      if (this.cargado) return
      const [m, c, d] = await Promise.all([
        api.medidas(), api.centrosIpIrc(), api.delitos(),
      ])
      this.medidas = m
      this.centrosIpIrc = c
      this.delitos = d
      this.cargado = true
    },
  },
})
