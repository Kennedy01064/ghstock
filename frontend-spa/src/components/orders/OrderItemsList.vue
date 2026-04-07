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
        class="w-9 h-9 flex items-center justify-center text-white/20 hover:text-red-500 hover:bg-red-500/10 rounded-xl transition-all shrink-0 border border-transparent hover:border-red-500/30 disabled:opacity-50"
        :disabled="loading"
        @click="$emit('remove', item.id)"
      >
        <svg v-if="!loading" class="w-4 h-4 transition-transform group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
        <svg v-else class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </li>

    <li v-if="!items.length">
      <EmptyState
        title="Pedido vacio"
        description="Agrega productos del catalogo para completar la solicitud."
        class="py-16 bg-transparent border-none shadow-none"
      />
    </li>
  </ul>
</template>

<script setup>
import EmptyState from "@/components/ui/EmptyState.vue"
import { formatCurrency } from "@/utils/formatters"

defineProps({
  items: { type: Array, default: () => [] },
  editable: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
})

defineEmits(["remove"])
</script>
