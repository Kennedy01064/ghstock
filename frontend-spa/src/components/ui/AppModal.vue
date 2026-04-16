<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="open" class="fixed inset-0 z-[70] flex items-center justify-center px-4 py-8">
        <div class="absolute inset-0 bg-slate-100/70 backdrop-blur-sm" @click="$emit('close')"></div>

        <Transition name="modal-scale">
          <div
            v-if="open"
            class="relative z-10 w-full max-w-lg overflow-hidden rounded-[32px] border border-white/[0.12] bg-white/95 shadow-2xl"
          >
            <div class="border-b border-white/[0.12] px-7 py-6">
              <p class="text-[11px] font-black uppercase tracking-[0.2em] text-amber">{{ eyebrow }}</p>
              <h3 class="mt-3 text-2xl font-black tracking-tight text-slate-900">{{ title }}</h3>
              <p v-if="description" class="mt-3 text-sm leading-7 text-text-secondary">{{ description }}</p>
            </div>

            <div class="flex flex-col gap-3 px-7 py-6 sm:flex-row">
              <button type="button" class="btn btn-secondary flex-1" :disabled="loading" @click="$emit('close')">
                {{ cancelLabel }}
              </button>
              <button
                type="button"
                class="btn flex-1"
                :class="confirmVariant === 'danger' ? 'bg-rose-500 text-slate-900 hover:bg-rose-400' : 'btn-primary'"
                :disabled="loading"
                @click="$emit('confirm')"
              >
                {{ loading ? loadingLabel : confirmLabel }}
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  open: { type: Boolean, default: false },
  eyebrow: { type: String, default: "Confirmacion" },
  title: { type: String, default: "" },
  description: { type: String, default: "" },
  confirmLabel: { type: String, default: "Confirmar" },
  cancelLabel: { type: String, default: "Cancelar" },
  loadingLabel: { type: String, default: "Procesando..." },
  loading: { type: Boolean, default: false },
  confirmVariant: { type: String, default: "primary" },
})

defineEmits(["close", "confirm"])
</script>

<style>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-scale-enter-active,
.modal-scale-leave-active {
  transition:
    opacity 0.22s ease,
    transform 0.22s ease,
    filter 0.22s ease;
}

.modal-scale-enter-from,
.modal-scale-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.97);
  filter: blur(6px);
}
</style>
