<script setup lang="ts">
import { useCasoStore } from '../../stores/caso'
const s = useCasoStore()
</script>

<template>
  <button type="button" class="limpiar" @click="s.reset()">🧹 Limpiar</button>
</template>

<style scoped>
.limpiar {
  background: #f6f8fa; color: #57606a; border: 1px solid #d0d7de;
  border-radius: 6px; padding: 6px 10px; font-size: 0.85rem; cursor: pointer;
}
.limpiar:hover { background: #eaeef2; }
</style>
