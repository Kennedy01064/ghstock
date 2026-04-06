<template>
  <ul class="divide-y divide-white/5">
    <li
      v-for="item in items"
      :key="item.id"
      class="px-5 py-4 flex items-center gap-4 hover:bg-white/[0.03] transition-colors group"
    >
      <div class="w-14 h-14 rounded-2xl bg-navy-accent border border-white/5 flex items-center justify-center p-2 shrink-0 shadow-inner overflow-hidden">
        <img
          :src="item.imageUrl"
          :alt="item.nombreProductoSnapshot"
          class="max-h-full object-contain transition-transform group-hover:scale-110"
        >
      </div>

      <div class="w-9 h-9 bg-amber text-navy-deep font-black text-xs rounded-xl flex items-center justify-center shrink-0 shadow-lg shadow-amber/10">
        {{ item.quantity }}
      </div>

      <div class="flex-grow min-w-0">
        <p class="text-[11px] font-black text-white uppercase tracking-wider truncate group-hover:text-amber transition-colors">
          {{ item.nombreProductoSnapshot }}
        </p>
        <div class="flex items-center gap-2 mt-1">
          <span class="text-[9px] font-bold text-text-muted bg-white/5 px-1.5 py-0.5 rounded uppercase">{{ item.unit }}</span>
          <span v-if="item.precioUnitario" class="text-xs font-black text-amber">
            {{ formatCurrency(item.precioUnitario * item.quantity) }}
          </span>
        </div>
      </div>

      <button
        v-if="editable"
        type="button"
        class="w-9 h-9 flex items-center justify-center text-white/20 hover:text-red-500 hover:bg-red-500/10 rounded-xl transition-all shrink-0 border border-transparent hover:border-red-500/30"
        @click="$emit('remove', item.id)"
      >
        <svg class="w-4 h-4 transition-transform group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </li>

    <li v-if="!items.length" class="px-5 py-16 text-center">
      <div class="w-16 h-16 bg-white/5 border border-white/10 rounded-[2rem] flex items-center justify-center mx-auto mb-4 text-white/10 shadow-inner">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4" />
        </svg>
      </div>
      <p class="text-xs font-black text-white uppercase tracking-[0.2em]">Pedido vacio</p>
      <p class="text-[10px] text-text-muted mt-1 uppercase font-bold">Agrega productos del catalogo</p>
    </li>
  </ul>
</template>

<script setup>
import { formatCurrency } from "@/utils/formatters"

defineProps({
  items: { type: Array, default: () => [] },
  editable: { type: Boolean, default: false },
})

defineEmits(["remove"])
</script>
