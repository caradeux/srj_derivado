<script setup lang="ts">
import { ref, computed, nextTick, useTemplateRef, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const usuario = ref('')
const password = ref('')
const error = ref<string | null>(null)
const verPassword = ref(false)
const enviando = ref(false)

const userRef = useTemplateRef<HTMLInputElement>('userInput')
onMounted(() => { userRef.value?.focus() })

const formularioListo = computed(() => usuario.value.trim() && password.value)

async function submit() {
  error.value = null
  enviando.value = true
  try {
    // Pequeño delay para feedback visual (no real network — pero da sensación de envío)
    await new Promise(r => setTimeout(r, 250))
    const r = auth.iniciarSesion(usuario.value, password.value)
    if (!r.ok) {
      error.value = r.mensaje ?? 'No se pudo iniciar sesión.'
      password.value = ''
      await nextTick()
    }
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <main class="login-page">
    <section class="login-card" aria-labelledby="login-title">
      <header class="login-head">
        <div class="brand-mark" aria-hidden="true">DRM</div>
        <h1 id="login-title">Sistema de Derivación Virtual</h1>
        <p class="subtitle">Coordinación Judicial D.R.M. · S.N.R.S.J.</p>
      </header>

      <form class="login-form" @submit.prevent="submit" novalidate>
        <label class="field">
          <span class="field-label">Usuario</span>
          <input
            ref="userInput"
            v-model="usuario"
            type="text"
            autocomplete="username"
            spellcheck="false"
            autocapitalize="none"
            aria-required="true"
          />
        </label>

        <label class="field">
          <span class="field-label">Contraseña</span>
          <div class="pw-wrap">
            <input
              v-model="password"
              :type="verPassword ? 'text' : 'password'"
              autocomplete="current-password"
              aria-required="true"
              @keyup.enter="submit"
            />
            <button
              type="button"
              class="pw-toggle"
              :aria-label="verPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
              :aria-pressed="verPassword"
              @click="verPassword = !verPassword"
            >
              <svg v-if="!verPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                   stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor"
                   stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            </button>
          </div>
        </label>

        <p v-if="error" class="error" role="alert">{{ error }}</p>

        <button type="submit" class="submit"
                :disabled="!formularioListo || enviando">
          <svg v-if="!enviando" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
            <polyline points="10 17 15 12 10 7"/>
            <line x1="15" y1="12" x2="3" y2="12"/>
          </svg>
          <svg v-else class="spin" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
          <span>{{ enviando ? 'Verificando…' : 'Iniciar sesión' }}</span>
        </button>

        <p class="hint">
          Uso interno · Coordinación Judicial D.R.M.<br />
          Para soporte contacte al administrador del sistema.
        </p>
      </form>
    </section>

    <footer class="login-foot">
      Av. Pedro De Valdivia N° 4070, Ñuñoa · Fono: 22.3980.04.00
    </footer>
  </main>
</template>

<style scoped>
.login-page {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--sp-6);
  background:
    linear-gradient(180deg, rgba(30,58,95,0.05) 0%, rgba(30,58,95,0) 60%),
    var(--color-bg);
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-top: 4px solid var(--color-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: var(--sp-8) var(--sp-8) var(--sp-6);
}

.login-head {
  text-align: center;
  display: flex; flex-direction: column; align-items: center;
  gap: var(--sp-2);
  margin-bottom: var(--sp-6);
  padding-bottom: var(--sp-4);
  border-bottom: 1px solid var(--color-border);
}
.brand-mark {
  width: 56px; height: 56px;
  display: grid; place-items: center;
  background: var(--color-primary);
  color: var(--color-on-primary);
  border-radius: var(--radius-md);
  font-family: var(--font-heading);
  font-weight: var(--fw-bold);
  font-size: var(--fs-lg);
  letter-spacing: 0.06em;
  box-shadow: var(--shadow-md);
}
.login-head h1 {
  font-size: var(--fs-lg);
  color: var(--color-primary);
  line-height: 1.2;
}
.subtitle {
  margin: 0;
  font-size: var(--fs-xs);
  color: var(--color-fg-subtle);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.login-form { display: flex; flex-direction: column; gap: var(--sp-4); }

.field {
  display: flex; flex-direction: column; gap: var(--sp-1);
}
.field-label {
  font-size: var(--fs-sm);
  font-weight: var(--fw-medium);
  color: var(--color-fg-muted);
}

.pw-wrap { position: relative; }
.pw-wrap input { padding-right: 44px; }
.pw-toggle {
  position: absolute;
  top: 50%;
  right: var(--sp-1);
  transform: translateY(-50%);
  width: 36px; height: 36px;
  display: grid; place-items: center;
  background: transparent;
  border: none;
  color: var(--color-fg-subtle);
  border-radius: var(--radius-sm);
  padding: 0;
}
.pw-toggle:hover { color: var(--color-primary); background: var(--color-surface-muted); }
.pw-toggle svg { width: 18px; height: 18px; }

.submit {
  display: inline-flex; align-items: center; justify-content: center;
  gap: var(--sp-2);
  min-height: 48px;
  margin-top: var(--sp-1);
  background: var(--color-accent);
  color: var(--color-on-primary);
  border: 1px solid var(--color-accent);
  font-size: var(--fs-base);
  font-weight: var(--fw-semibold);
  letter-spacing: 0.01em;
  box-shadow: var(--shadow-sm);
}
.submit:hover:not(:disabled) {
  background: var(--color-accent-hover);
  border-color: var(--color-accent-hover);
}
.submit:disabled {
  background: var(--color-fg-subtle);
  border-color: var(--color-fg-subtle);
  opacity: 0.7;
}
.submit svg { width: 20px; height: 20px; }
.spin { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .spin { animation: none; } }

.error {
  color: var(--color-danger);
  background: var(--color-danger-bg);
  border: 1px solid #FECACA;
  border-left: 4px solid var(--color-danger);
  border-radius: var(--radius);
  padding: var(--sp-2) var(--sp-3);
  font-size: var(--fs-sm);
  margin: 0;
}

.hint {
  margin: var(--sp-2) 0 0;
  font-size: var(--fs-xs);
  color: var(--color-fg-subtle);
  text-align: center;
  line-height: var(--lh-base);
}

.login-foot {
  margin-top: var(--sp-6);
  font-size: var(--fs-xs);
  color: var(--color-fg-subtle);
  text-align: center;
}
</style>
