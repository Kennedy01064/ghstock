<template>
  <div class="flex flex-col items-center justify-center p-12 text-center bg-white/[0.02] border border-white/[0.05] rounded-[3rem] animate-in fade-in zoom-in duration-700">
    <!-- Icon Container -->
    <div class="relative mb-6">
      <div class="absolute inset-0 bg-amber-500/20 blur-3xl rounded-full scale-150 opacity-50"></div>
      <div class="relative w-20 h-20 flex items-center justify-center rounded-3xl bg-gradient-to-br from-white/[0.08] to-transparent border border-white/[0.1] shadow-2xl">
        <slot name="icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-amber-500">
            <path d="m7.5 4.27 9 5.15"/>
            <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>
            <path d="m3.3 7 8.7 5 8.7-5"/>
            <path d="M12 22V12"/>
          </svg>
        </slot>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-sm space-y-3">
      <h3 class="text-xl font-black text-slate-900 uppercase tracking-tight">{{ title }}</h3>
      <p class="text-sm font-medium text-text-muted leading-relaxed opacity-60">
        {{ description }}
      </p>
    </div>

    <!-- Action Slot -->
    <div v-if="$slots.action" class="mt-8">
      <slot name="action"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'Sin resultados'
  },
  description: {
    type: String,
    default: 'No se encontraron elementos para mostrar en este momento.'
  }
})
</script>

<style scoped>
.animate-in {
  animation: enter 0.6s ease-out;
}

@keyframes enter {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
