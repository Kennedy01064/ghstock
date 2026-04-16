<template>
  <div class="max-w-7xl mx-auto space-y-10 pb-32">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 px-2">
      <div class="space-y-2">
        <span class="eyebrow tracking-[0.4em] !text-amber">Gestion de Suministros</span>
        <h1 class="h2 italic !tracking-tighter">Compras Directas</h1>
        <p class="text-text-muted font-medium text-sm">
          Registro y control de adquisiciones realizadas para el reabastecimiento del nucleo logistico.
        </p>
      </div>

      <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4">
        <div class="flex items-center gap-4 bg-slate-50 border border-slate-200 backdrop-blur-xl rounded-2xl px-6 py-3 shadow-2xl shadow-black/20">
          <span class="text-[9px] font-black text-text-muted uppercase tracking-widest text-center">Operaciones<br>Registradas</span>
          <span class="text-2xl font-black text-slate-900 leading-none border-l border-slate-200 pl-4">{{ purchases.length }}</span>
        </div>

        <RouterLink :to="{ name: 'dispatchPurchaseCreate' }" class="btn btn-primary shadow-2xl shadow-amber/10 group h-14 px-8">
          <svg class="w-5 h-5 transition-transform group-hover:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
          </svg>
          REGISTRAR ADQUISICION
        </RouterLink>
      </div>
    </div>

    <div v-if="dispatchStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ dispatchStore.error }}
    </div>

    <div class="card !p-0 border-slate-200 bg-slate-50 overflow-hidden shadow-[0_40px_100px_-20px_rgba(0,0,0,0.6)]">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm whitespace-nowrap border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-[10px] uppercase tracking-[0.3em] font-black text-text-muted">
              <th class="px-8 py-5">Control</th>
              <th class="px-8 py-5">Cronologia</th>
              <th class="px-8 py-5">Proveedor & Comprobante</th>
              <th class="px-8 py-5 text-center">Carga</th>
              <th class="px-8 py-5 text-right">Inversion</th>
              <th class="px-8 py-5 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="purchase in purchases" :key="purchase.id" class="hover:bg-slate-50 transition-all group">
              <td class="px-8 py-6">
                <div class="inline-flex items-center gap-3 px-4 py-1.5 bg-emerald-500/5 border border-emerald-500/10 rounded-xl group-hover:border-emerald-500/40 transition-all">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]" />
                  <span class="text-xs font-black text-slate-900 tracking-widest">#{{ purchase.id }}</span>
                </div>
              </td>
              <td class="px-8 py-6">
                <div class="flex flex-col gap-0.5">
                  <p class="font-black text-slate-900 text-[13px] uppercase tracking-tight">{{ formatDate(purchase.purchase_date) }}</p>
                  <p class="text-[10px] font-black text-text-muted uppercase tracking-widest">REGISTRO GH</p>
                </div>
              </td>
              <td class="px-8 py-6">
                <div class="flex flex-col gap-1">
                  <p class="text-[13px] font-black text-slate-900 uppercase tracking-tight truncate max-w-[200px]">
                    {{ purchase.supplier || "PROVEEDOR NO ESPECIFICADO" }}
                  </p>
                  <div class="flex items-center gap-2">
                    <svg class="w-3 h-3 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em]">{{ purchase.invoice_number || "SIN FACTURA" }}</span>
                  </div>
                </div>
              </td>
              <td class="px-8 py-6 text-center">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-lg bg-slate-100/60 border border-slate-200">
                  <span class="text-sm font-black text-slate-900 tabular-nums">{{ purchase.items?.length || 0 }}</span>
                  <span class="text-[9px] font-black text-text-muted uppercase tracking-widest">SKUs</span>
                </div>
              </td>
              <td class="px-8 py-6 text-right">
                <p class="text-base font-black text-emerald-400 tabular-nums tracking-tight">
                  {{ formatCurrency(purchase.total_amount || 0) }}
                </p>
              </td>
              <td class="px-8 py-6 text-right">
                <RouterLink :to="{ name: 'dispatchPurchaseDetail', params: { purchaseId: purchase.id } }" class="btn btn-secondary !py-2.5 !px-5 !rounded-xl !text-[10px] border-slate-200 hover:border-amber/30 hover:text-amber shadow-none group/link">
                  <span>VER DETALLE</span>
                  <svg class="w-4 h-4 transition-transform group-hover/link:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7" />
                  </svg>
                </RouterLink>
              </td>
            </tr>

            <tr v-if="!purchases.length">
              <td colspan="6" class="px-8 py-20">
                <EmptyState
                  title="Sin Adquisiciones"
                  description="Aun no se han registrado compras directas en el sistema logistico."
                  class="bg-transparent border-none shadow-none"
                >
                  <template #action>
                    <RouterLink :to="{ name: 'dispatchPurchaseCreate' }" class="btn btn-primary !py-3 !px-8 text-[11px]">
                      REGISTRAR PRIMERA COMPRA
                    </RouterLink>
                  </template>
                </EmptyState>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"

import EmptyState from "@/components/ui/EmptyState.vue"
import { useDispatchStore } from "@/stores/dispatchStore"
import { formatCurrency, formatDate } from "@/utils/formatters"
import { normalizePurchase } from "@/utils/normalizers"

const dispatchStore = useDispatchStore()
const purchases = computed(() => dispatchStore.purchases.map(normalizePurchase))

onMounted(() => {
  dispatchStore.fetchPurchases()
})
</script>
