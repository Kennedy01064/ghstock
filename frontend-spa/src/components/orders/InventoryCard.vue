<template>
  <article
    class="card !p-0 overflow-hidden border-white/[0.07] hover:border-amber/30 transition-all group/card shadow-2xl shadow-black/40"
    :class="inventory.quantity === 0 ? 'opacity-40 grayscale pointer-events-none' : ''"
  >
    <div class="relative h-44 bg-white/[0.06] p-6 flex items-center justify-center border-b border-white/[0.07] overflow-hidden">
      <img
        :src="inventory.product.imageUrl"
        :alt="inventory.product.name"
        class="max-h-full object-contain drop-shadow-2xl transition-transform duration-500 group-hover/card:scale-110"
      >

      <div class="absolute top-4 left-4">
        <div class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-navy-deep/80 backdrop-blur-md border border-white/[0.12] shadow-lg">
          <svg class="w-3.5 h-3.5 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <span class="text-[10px] font-black text-white uppercase tracking-widest truncate max-w-[100px]">
            {{ inventory.building?.name || "Sede" }}
          </span>
        </div>
      </div>

      <div class="absolute top-4 right-4">
        <div class="flex items-center gap-2 px-4 py-1.5 rounded-xl bg-amber text-navy-deep font-black shadow-xl shadow-amber/20 border border-amber/40">
          <span class="text-[9px] uppercase tracking-tighter">Disponible</span>
          <span class="text-base leading-none">{{ inventory.quantity }}</span>
        </div>
      </div>

      <div class="absolute inset-0 bg-gradient-to-t from-navy-deep/40 to-transparent" />
    </div>

    <div class="p-6 flex flex-col flex-grow bg-white/[0.01]">
      <div class="flex-grow space-y-1">
        <h3 class="text-sm font-black text-white uppercase tracking-tight leading-tight line-clamp-2 min-h-[2.5rem] group-hover/card:text-amber transition-colors">
          {{ inventory.product.name }}
        </h3>
        <p v-if="inventory.product.sku" class="text-[10px] font-black text-text-muted tracking-[0.2em] uppercase">
          {{ inventory.product.sku }}
        </p>
      </div>

      <div class="mt-6 pt-5 border-t border-white/[0.07] space-y-4">
        <div class="flex items-center gap-2">
          <input
            v-model.number="consumeQuantity"
            type="number"
            min="1"
            :max="inventory.quantity"
            :disabled="isConsuming || isAdjusting"
            class="w-16 h-10 px-2 bg-white/[0.04] border border-white/[0.12] rounded-xl text-center font-black text-amber outline-none focus:border-amber/40 focus:bg-white/[0.06] transition-all shadow-inner disabled:opacity-50"
          >
          <button
            type="button"
            class="flex-1 h-10 flex items-center justify-center gap-2 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all border bg-red-500/5 text-red-400 border-red-500/20 hover:bg-red-500 hover:text-white hover:border-red-500 shadow-xl shadow-red-500/5 disabled:opacity-50"
            :disabled="inventory.quantity === 0 || isConsuming || isAdjusting"
            @click="emit('consume', { id: inventory.id, quantity: safeConsumeQuantity })"
          >
            <svg v-if="!isConsuming" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M20 12H4" />
            </svg>
            <svg v-else class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ isConsuming ? "PROCESANDO..." : "Registrar consumo" }}
          </button>
        </div>

        <div class="pt-2 border-t border-white/[0.03]">
          <div class="flex items-center gap-2">
            <input
              v-model.number="adjustQuantity"
              type="number"
              min="1"
              :disabled="isConsuming || isAdjusting"
              class="w-16 h-8 px-2 bg-white/[0.04] border border-white/[0.07] rounded-lg text-center font-black text-emerald-400/60 outline-none focus:border-emerald-500/40 focus:bg-white/[0.06] transition-all shadow-inner text-[11px] disabled:opacity-50"
            >
            <button
              type="button"
              class="flex-1 h-8 flex items-center justify-center gap-2 rounded-lg font-black text-[9px] uppercase tracking-widest transition-all border bg-emerald-500/5 text-emerald-400 border-emerald-500/10 hover:bg-emerald-500 hover:text-white hover:border-emerald-500 disabled:opacity-50"
              :disabled="isConsuming || isAdjusting"
              @click="emit('adjust', { id: inventory.id, quantity: safeAdjustedQuantity })"
            >
              <svg v-if="!isAdjusting" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
              </svg>
              <svg v-else class="w-3.5 h-3.5 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              {{ isAdjusting ? "SINCRONIZANDO..." : "Reposicion directa" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed, ref, watch } from "vue"

const props = defineProps({
  inventory: { type: Object, required: true },
  isConsuming: { type: Boolean, default: false },
  isAdjusting: { type: Boolean, default: false },
})

const emit = defineEmits(["consume", "adjust"])

const consumeQuantity = ref(props.inventory.quantity > 0 ? 1 : 0)
const adjustQuantity = ref(1)

const safeConsumeQuantity = computed(() => {
  const value = Number(consumeQuantity.value) || 1
  return Math.max(1, Math.min(value, props.inventory.quantity || 1))
})

const safeAdjustedQuantity = computed(() => {
  const delta = Number(adjustQuantity.value) || 1
  return Math.max(0, (props.inventory.quantity || 0) + Math.max(1, delta))
})

watch(
  () => props.inventory.quantity,
  (quantity) => {
    consumeQuantity.value = quantity > 0 ? 1 : 0
    adjustQuantity.value = 1
  },
)
</script>
