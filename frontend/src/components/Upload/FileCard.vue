<script setup lang="ts">
defineProps<{ filename: string; sizeBytes: number }>()
const emit = defineEmits<{ (e: 'remove'): void }>()

function fmt(n: number): string {
  if (n < 1024) return `${n} B`
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(0)} KB`
  return `${(n / 1024 / 1024).toFixed(1)} MB`
}
</script>

<template>
  <div class="file-card">
    <span class="name">{{ filename }}</span>
    <span class="size">{{ fmt(sizeBytes) }}</span>
    <button type="button" @click="emit('remove')" aria-label="Quitar">×</button>
  </div>
</template>

<style scoped>
.file-card {
  display: flex; align-items: center; gap: 8px;
  border: 1px solid #d0d7de; border-radius: 6px;
  padding: 6px 10px; background: #f6f8fa;
  font-size: 0.9rem;
}
.name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.size { color: #57606a; }
button {
  background: none; border: none; cursor: pointer; font-size: 1.2rem; color: #57606a;
}
</style>
