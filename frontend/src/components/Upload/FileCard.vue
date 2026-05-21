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
    <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14 2 14 8 20 8"/>
    </svg>
    <span class="name">{{ filename }}</span>
    <span class="size">{{ fmt(sizeBytes) }}</span>
    <button type="button" class="remove" @click="emit('remove')" aria-label="Quitar archivo">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </button>
  </div>
</template>

<style scoped>
.file-card {
  display: flex; align-items: center; gap: var(--sp-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: var(--sp-2) var(--sp-3);
  background: var(--color-surface);
  font-size: var(--fs-sm);
  color: var(--color-fg);
}
.file-icon {
  width: 18px; height: 18px;
  color: var(--color-primary);
  flex-shrink: 0;
}
.name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.size {
  color: var(--color-fg-subtle);
  font-size: var(--fs-xs);
  font-variant-numeric: tabular-nums;
}
.remove {
  display: grid; place-items: center;
  width: 28px; height: 28px;
  background: transparent;
  border: none;
  color: var(--color-fg-subtle);
  border-radius: var(--radius-sm);
  padding: 0;
}
.remove:hover { background: var(--color-danger-bg); color: var(--color-danger); }
.remove svg { width: 16px; height: 16px; }
</style>
