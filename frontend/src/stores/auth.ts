import { defineStore } from 'pinia'

/**
 * Auth store — gate cliente-side para uso en estación de trabajo.
 *
 * Nota: La aplicación es local-only (BRD NFR-05). Este gate evita que un
 * tercero use la estación mientras el profesional está ausente; no es una
 * autenticación de servidor. Las credenciales se verifican contra una
 * constante en bundle, configurable vía variable de build.
 *
 * Para producción más estricta:
 *  - Mover la verificación a un endpoint /api/auth/login en el backend
 *  - Hashear la contraseña en config
 *  - Emitir un token con expiración corta
 */

// Credenciales por defecto — cambiar en producción vía VITE_AUTH_USER / VITE_AUTH_PASS
const USER_VALIDO = import.meta.env.VITE_AUTH_USER ?? 'drm'
const PASS_VALIDA = import.meta.env.VITE_AUTH_PASS ?? 'drm2026'

const STORAGE_KEY = 'derivacion_drm_auth'

interface State {
  usuario: string | null
  autenticado: boolean
}

function _cargarSesion(): State {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return { usuario: null, autenticado: false }
    const parsed = JSON.parse(raw)
    return {
      usuario: typeof parsed.usuario === 'string' ? parsed.usuario : null,
      autenticado: parsed.autenticado === true,
    }
  } catch {
    return { usuario: null, autenticado: false }
  }
}

export const useAuthStore = defineStore('auth', {
  state: (): State => _cargarSesion(),
  actions: {
    iniciarSesion(usuario: string, password: string): { ok: boolean; mensaje?: string } {
      const u = usuario.trim()
      if (!u || !password) {
        return { ok: false, mensaje: 'Ingrese usuario y contraseña.' }
      }
      if (u !== USER_VALIDO || password !== PASS_VALIDA) {
        return { ok: false, mensaje: 'Usuario o contraseña incorrectos.' }
      }
      this.usuario = u
      this.autenticado = true
      sessionStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ usuario: u, autenticado: true }),
      )
      return { ok: true }
    },

    cerrarSesion() {
      this.usuario = null
      this.autenticado = false
      sessionStorage.removeItem(STORAGE_KEY)
    },
  },
})
