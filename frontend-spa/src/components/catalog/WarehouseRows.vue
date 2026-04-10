<template>
  <div class="selection:bg-amber selection:text-navy-deep">
    <table class="w-full text-left border-collapse table-fixed">
      <colgroup>
        <col class="w-[40%]" />
        <col class="w-[8%]" />
        <col class="w-[12%]" />
        <col class="w-[14%]" />
        <col class="w-[10%]" />
        <col class="w-[16%]" />
      </colgroup>
      <thead>
        <tr class="bg-white/[0.03] border-b border-white/5">
          <th class="px-4 py-4 text-[10px] font-black uppercase tracking-[0.3em] text-text-muted">Producto / SKU</th>
          <th class="px-3 py-4 text-[10px] font-black uppercase tracking-[0.3em] text-text-muted text-center">Unidad</th>
          <th class="px-3 py-4 text-[10px] font-black uppercase tracking-[0.3em] text-text-muted text-center">Stock</th>
          <th class="px-3 py-4 text-[10px] font-black uppercase tracking-[0.3em] text-text-muted text-right">Valuacion</th>
          <th class="px-3 py-4 text-[10px] font-black uppercase tracking-[0.3em] text-text-muted text-center">Estatus</th>
          <th class="px-4 py-4 text-[10px] font-black uppercase tracking-[0.3em] text-text-muted text-right">Acciones</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-white/5">
        <tr
          v-for="product in products"
          :key="product.id"
          class="group hover:bg-white/[0.03] transition-all duration-300"
          :class="product.active ? '' : 'opacity-30 grayscale blur-[0.5px] bg-navy-deep/50'"
        >
          <td class="px-4 py-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl border border-white/10 bg-navy-accent overflow-hidden shrink-0 shadow-lg group-hover:border-amber/40 group-hover:shadow-amber/10 transition-all duration-500">
                <img :src="product.imageUrl" :alt="product.name" class="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-110" loading="lazy" />
              </div>
              <div class="min-w-0 space-y-0.5">
                <p class="text-sm font-black text-white tracking-tight truncate leading-tight uppercase group-hover:text-amber transition-colors">{{ product.name }}</p>
                <div class="flex items-center gap-1.5">
                  <span class="text-[9px] font-black text-amber uppercase tracking-widest px-1.5 py-0.5 rounded bg-amber/10 border border-amber/20">SKU</span>
                  <span class="text-[10px] font-bold text-text-muted tracking-wider truncate">{{ product.sku || "SIN-SKU" }}</span>
                </div>
              </div>
            </div>
          </td>
          <td class="px-3 py-4 text-center">
            <span class="text-[11px] font-black text-text-muted tracking-widest uppercase">{{ product.unit || "GL" }}</span>
          </td>
          <td class="px-3 py-4 text-center">
            <div class="inline-flex flex-col items-center">
              <span class="text-base font-black tracking-tight leading-none" :class="product.stockActual <= product.stockMinimo ? 'text-rose-500' : 'text-emerald-400'">
                {{ product.stockActual }}
              </span>
              <span class="text-[9px] font-black uppercase tracking-[0.2em] text-text-muted/60 mt-0.5">Existencias</span>
            </div>
          </td>
          <td class="px-3 py-4 text-right">
            <div class="inline-flex flex-col items-end">
              <span class="text-base font-black text-white leading-none"><span class="text-amber">S/</span> {{ formatNumber(product.precio) }}</span>
              <span class="text-[9px] font-black uppercase tracking-[0.2em] text-text-muted/60 mt-0.5">P. Unitario</span>
            </div>
          </td>
          <td class="px-3 py-4 text-center">
            <div v-if="product.active" class="inline-flex items-center gap-1.5 px-2 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
              <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.5)]"></div>
              <span class="text-[9px] font-black text-emerald-400 uppercase tracking-widest">Activo</span>
            </div>
            <div v-else class="inline-flex items-center gap-1.5 px-2 py-1 rounded-full bg-white/5 border border-white/10">
              <div class="w-1.5 h-1.5 rounded-full bg-white/20"></div>
              <span class="text-[9px] font-black text-text-muted uppercase tracking-widest">Inactivo</span>
            </div>
          </td>
          <td class="px-4 py-4 text-right">
            <div class="flex items-center justify-end gap-2">
              <button
                v-if="product.is_dynamic && product.source_url"
                type="button"
                class="w-8 h-8 flex items-center justify-center rounded-xl border border-amber/20 bg-amber/5 text-amber hover:bg-amber hover:text-navy-deep transition-all duration-300"
                title="Sincronizar Precio/Datos"
                @click="$emit('sync', product.id)"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
              <RouterLink
                :to="{ name: 'catalogProductEdit', params: { productId: product.id } }"
                class="w-8 h-8 flex items-center justify-center rounded-xl border border-white/5 bg-white/5 text-text-muted hover:text-white hover:border-white/20 hover:bg-white/10 transition-all duration-300"
                title="Editar Activo"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </RouterLink>
              <button
                type="button"
                class="w-8 h-8 flex items-center justify-center rounded-xl border border-white/5 bg-white/5 text-text-muted transition-all duration-300"
                :class="product.active ? 'hover:text-rose-500 hover:border-rose-500/30 hover:bg-rose-500/10' : 'hover:text-emerald-400 hover:border-emerald-400/30 hover:bg-emerald-400/10'"
                :title="product.active ? 'Desactivar Item' : 'Reactivar Item'"
                @click="$emit('toggle', product.id)"
              >
                <svg v-if="product.active" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728L5.636 5.636" />
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </button>
            </div>
          </td>
        </tr>
        <tr v-if="!products.length">
          <td colspan="6" class="px-8 py-20">
            <EmptyState 
              title="Sin Productos" 
              description="No se encontraron artículos en el almacén con los criterios de búsqueda actuales."
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import EmptyState from "@/components/ui/EmptyState.vue"

defineProps({
  products: { type: Array, default: () => [] },
})

defineEmits(["sync", "toggle"])

function formatNumber(value) {
  return Number(value ?? 0).toFixed(2)
}
</script>
