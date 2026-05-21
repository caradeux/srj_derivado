import type { components } from './types'

type Schemas = components['schemas']
export type Adolescente = Schemas['Adolescente']
export type Causa = Schemas['Causa']
export type AdultoResponsable = Schemas['AdultoResponsable']
export type CasoDerivacion = Schemas['CasoDerivacion']
export type CentroAsignado = Schemas['CentroAsignado']
export type ExtractionResult = Schemas['ExtractionResult']
export type Medida = Schemas['Medida']
export type CentroIPIRC = Schemas['CentroIPIRC']
export type MedidaCatalogoItem = Schemas['MedidaCatalogoItem']

class ApiError extends Error {
  constructor(public status: number, message: string, public detail?: unknown) {
    super(message)
  }
}

async function unwrap<T>(r: Response): Promise<T> {
  if (!r.ok) {
    let detail: unknown
    try { detail = await r.json() } catch { /* ignore */ }
    throw new ApiError(r.status, `HTTP ${r.status}`, detail)
  }
  return r.json() as Promise<T>
}

export const api = {
  async extract(files: File[]): Promise<ExtractionResult> {
    const fd = new FormData()
    files.forEach(f => fd.append('files', f))
    return unwrap(await fetch('/api/extract', { method: 'POST', body: fd }))
  },

  async resolverCentro(medida: Medida, comuna: string): Promise<CentroAsignado[]> {
    return unwrap(await fetch('/api/centros/resolver', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ medida, comuna }),
    }))
  },

  async centrosIpIrc(): Promise<Record<CentroIPIRC, CentroAsignado>> {
    return unwrap(await fetch('/api/centros/ip-irc'))
  },

  async medidas(): Promise<MedidaCatalogoItem[]> {
    return unwrap(await fetch('/api/catalogo/medidas'))
  },

  async delitos(): Promise<string[]> {
    return unwrap(await fetch('/api/catalogo/delitos'))
  },

  async generar(payload: {
    caso: CasoDerivacion
    profesional: string
    fecha_emision: string
  }): Promise<{ blob: Blob; filename: string }> {
    const r = await fetch('/api/derivacion/generar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    if (!r.ok) {
      let detail: unknown
      try { detail = await r.json() } catch { /* ignore */ }
      throw new ApiError(r.status, `HTTP ${r.status}`, detail)
    }
    const cd = r.headers.get('content-disposition') ?? ''
    const match = cd.match(/filename="([^"]+)"/)
    const filename = match?.[1] ?? 'derivacion.docx'
    return { blob: await r.blob(), filename }
  },
}

export { ApiError }
