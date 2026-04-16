<template>
  <Teleport to="body">
    <div class="pointer-events-none fixed right-4 top-4 z-[80] flex w-[min(92vw,380px)] flex-col gap-3">
      <TransitionGroup name="toast-stack">
        <article
          v-for="toast in uiStore.toasts"
          :key="toast.id"
          class="pointer-events-auto overflow-hidden rounded-[24px] border shadow-2xl backdrop-blur-xl"
          :class="toastClass(toast.type)"
        >
          <div class="flex items-start gap-4 px-5 py-4">
            <div class="mt-0.5 h-2.5 w-2.5 shrink-0 rounded-full" :class="dotClass(toast.type)"></div>
            <div class="min-w-0 flex-1">
              <p class="text-[11px] font-black uppercase tracking-[0.18em]">{{ toast.title }}</p>
              <p class="mt-2 text-sm leading-6">{{ toast.message }}</p>
            </div>
            <button
              type="button"
              class="rounded-full border border-slate-300 px-2 py-1 text-[10px] font-black uppercase tracking-[0.18em] text-slate-500 transition hover:text-slate-700 hover:border-slate-400"
              @click="uiStore.removeToast(toast.id)"
            >
              cerrar
            </button>
          </div>
        </article>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useUiStore } from "@/stores/uiStore"

const uiStore = useUiStore()

function toastClass(type) {
  if (type === "success") {
    return "border-emerald-200 bg-emerald-50 text-emerald-800"
  }

  if (type === "error") {
    return "border-rose-200 bg-rose-50 text-rose-800"
  }

  return "border-amber/30 bg-amber/10 text-amber-900"
}

function dotClass(type) {
  if (type === "success") {
    return "bg-emerald-400"
  }

  if (type === "error") {
    return "bg-rose-400"
  }

  return "bg-amber"
}
</script>

<style>
.toast-stack-enter-active,
.toast-stack-leave-active {
  transition:
    opacity 0.24s ease,
    transform 0.24s ease,
    filter 0.24s ease;
}

.toast-stack-enter-from,
.toast-stack-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
  filter: blur(4px);
}
</style>
