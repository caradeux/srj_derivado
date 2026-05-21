import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { useCatalogosStore } from './stores/catalogos'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')

// Cargar catálogos en background
useCatalogosStore().load().catch(err => {
  console.error('No se pudo cargar catálogos iniciales:', err)
})
