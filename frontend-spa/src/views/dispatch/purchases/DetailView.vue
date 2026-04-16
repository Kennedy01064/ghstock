<template>
  <div v-if="dispatchStore.error && !purchase" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
    {{ dispatchStore.error }}
  </div>

  <div v-else-if="dispatchStore.isLoading && !purchase" class="card text-text-secondary">
    Cargando compra...
  </div>

  <div v-else-if="purchase" class="max-w-6xl mx-auto space-y-10 pb-32">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 px-2">
      <div class="space-y-2">
        <div class="flex items-center gap-3">
          <RouterLink :to="{ name: 'dispatchPurchases' }" class="w-10 h-10 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-center text-text-muted hover:text-amber hover:bg-slate-50 transition-all group">
            <svg class="w-5 h-5 transition-transform group-hover:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M15 19l-7-7 7-7" />
            </svg>
          </RouterLink>
          <span class="eyebrow tracking-[0.4em] !text-amber">Registro de Suministros</span>
        </div>
        <h1 class="h2 italic !tracking-tighter">Adquisicion #{{ purchase.id }}</h1>
        <p class="text-text-muted font-medium text-sm">Detalle exhaustivo de la operacion mercantil y carga recibida.</p>
      </div>

      <div class="flex flex-col items-end gap-2 px-6 py-4 bg-emerald-500/10 border border-emerald-500/20 rounded-3xl shadow-2xl shadow-emerald-500/5">
        <span class="text-[9px] font-black text-emerald-400 uppercase tracking-[0.3em]">Inversion Total</span>
        <span class="text-3xl font-black text-slate-900 tabular-nums">{{ formatCurrency(purchase.total || 0) }}</span>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="card bg-slate-50 border-slate-200 relative overflow-hidden group">
        <div class="absolute top-0 left-0 w-1 h-full bg-amber/40 shadow-[0_0_15px_rgba(242,173,61,0.2)]" />
        <div class="space-y-6">
          <h3 class="text-[10px] font-black text-text-muted uppercase tracking-[0.3em]">Datos del Comprobante</h3>
          <div class="space-y-5">
            <div>
              <p class="text-[9px] font-black text-text-muted uppercase tracking-widest mb-1 opacity-60">Fecha de Operacion</p>
              <p class="text-base font-black text-slate-900 uppercase tracking-tight">{{ purchase.purchaseDate }}</p>
            </div>
            <div>
              <p class="text-[9px] font-black text-text-muted uppercase tracking-widest mb-1 opacity-60">Proveedor Emitente</p>
              <p class="text-sm font-black text-slate-900 uppercase tracking-tight">{{ purchase.supplier || "PROVEEDOR NO REGISTRADO" }}</p>
            </div>
            <div>
              <p class="text-[9px] font-black text-text-muted uppercase tracking-widest mb-1 opacity-60">N° de Documento</p>
              <p class="text-sm font-black text-amber uppercase tracking-[0.2em]">{{ purchase.invoice_number || "SIN COMPROBANTE" }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card bg-slate-50 border-slate-200">
        <div class="space-y-6">
          <h3 class="text-[10px] font-black text-text-muted uppercase tracking-[0.3em]">Validacion de Registro</h3>
          <div class="flex items-center gap-5 p-4 bg-slate-200/60 rounded-2xl border border-slate-200">
            <div class="w-14 h-14 rounded-2xl bg-amber/10 border border-amber/20 flex items-center justify-center text-xl font-black text-amber shadow-2xl shadow-amber/5">
              {{ (purchase.created_by?.name || purchase.created_by?.username || "?").slice(0, 1).toUpperCase() }}
            </div>
            <div class="space-y-1">
              <p class="text-sm font-black text-slate-900 uppercase tracking-tight">{{ purchase.created_by?.name || purchase.created_by?.username }}</p>
              <p class="text-[10px] font-black text-amber uppercase tracking-[0.2em]">{{ purchase.created_by?.role }}</p>
            </div>
          </div>
          <div class="pt-4 border-t border-slate-200">
            <p class="text-[9px] font-black text-text-muted uppercase tracking-widest mb-1 opacity-60">Timestamp de Sistema</p>
            <p class="text-xs font-black text-slate-900/60 tracking-widest">{{ formatDate(purchase.createdAt) }}</p>
          </div>
        </div>
      </div>

      <div class="card bg-slate-50 border-slate-200 flex flex-col justify-between">
        <h3 class="text-[10px] font-black text-text-muted uppercase tracking-[0.3em] mb-6">Resumen Operativo</h3>
        <div class="space-y-4">
          <div class="flex justify-between items-center px-4 py-3 bg-slate-50 rounded-xl border border-slate-200">
            <span class="text-[10px] font-black text-text-muted uppercase tracking-widest">Variedad SKUs</span>
            <span class="text-lg font-black text-slate-900 tabular-nums">{{ purchase.items.length }}</span>
          </div>
          <div class="flex justify-between items-center px-4 py-3 bg-slate-50 rounded-xl border border-slate-200">
            <span class="text-[10px] font-black text-text-muted uppercase tracking-widest">Unidades Fisicas</span>
            <span class="text-lg font-black text-slate-900 tabular-nums">{{ totalUnits }}</span>
          </div>
          <div v-if="purchase.notes" class="p-4 bg-amber/5 border border-amber/10 rounded-xl">
            <p class="text-[10px] font-black text-amber/60 uppercase tracking-widest mb-2">Observaciones</p>
            <p class="text-[11px] font-medium text-amber/80 leading-relaxed italic line-clamp-3">"{{ purchase.notes }}"</p>
          </div>
        </div>
      </div>
    </div>

    <div class="card !p-0 border-slate-200 bg-slate-50 overflow-hidden shadow-[0_40px_100px_-20px_rgba(0,0,0,0.6)]">
      <div class="px-8 py-5 border-b border-slate-200 bg-slate-50">
        <h2 class="text-sm font-black text-slate-900 uppercase tracking-[0.2em]">Desglose de Mercancia Recibida</h2>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-[9px] uppercase tracking-[0.3em] font-black text-text-muted">
              <th class="px-8 py-5">Articulo & Categoria</th>
              <th class="px-8 py-5 text-center">Volumen</th>
              <th class="px-8 py-5 text-right">Precio Un.</th>
              <th class="px-8 py-5 text-right">Inversion Bruta</th>
              <th class="px-8 py-5 text-center">Estado Actual Nucleo</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="item in purchase.items" :key="item.id" class="hover:bg-slate-50 transition-all group">
              <td class="px-8 py-6">
                <div class="flex flex-col gap-1">
                  <p class="text-[13px] font-black text-slate-900 uppercase tracking-tight group-hover:text-amber transition-colors">{{ item.name }}</p>
                  <p class="text-[10px] font-black text-text-muted uppercase tracking-widest">{{ item.product?.categoria }}</p>
                </div>
              </td>
              <td class="px-8 py-6 text-center">
                <span class="text-base font-black text-slate-900 tabular-nums">{{ item.quantity }}</span>
              </td>
              <td class="px-8 py-6 text-right font-black text-text-muted tabular-nums">
                {{ formatCurrency(item.price || 0) }}
              </td>
              <td class="px-8 py-6 text-right font-black text-emerald-400 tabular-nums text-base">
                {{ formatCurrency((item.quantity || 0) * (item.price || 0)) }}
              </td>
              <td class="px-8 py-6 text-center">
                <div class="inline-flex items-center gap-3 px-3 py-1.5 rounded-xl border" :class="(item.product?.stock_actual || 0) <= (item.product?.stock_minimo || 0) ? 'bg-red-500/10 border-red-500/20 text-red-400' : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'">
                  <span class="w-1.5 h-1.5 rounded-full" :class="(item.product?.stock_actual || 0) <= (item.product?.stock_minimo || 0) ? 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.4)]' : 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]'" />
                  <span class="text-[10px] font-black uppercase tracking-widest">{{ item.product?.stock_actual || 0 }} EN STOCK</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="flex justify-center pt-10">
      <RouterLink :to="{ name: 'dispatchPurchases' }" class="btn btn-secondary !py-4 px-10 !rounded-2xl border-slate-200 text-text-muted hover:text-slate-900 hover:border-slate-300 uppercase tracking-widest text-[10px]">
        REGRESAR AL LISTADO DE COMPRAS
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"
import { useRoute } from "vue-router"

import { useDispatchStore } from "@/stores/dispatchStore"
import { formatCurrency, formatDate } from "@/utils/formatters"
import { normalizePurchase } from "@/utils/normalizers"

const route = useRoute()
const dispatchStore = useDispatchStore()

const purchase = computed(() => (dispatchStore.currentPurchase ? normalizePurchase(dispatchStore.currentPurchase) : null))
const totalUnits = computed(() => (purchase.value?.items || []).reduce((sum, item) => sum + (item.quantity || 0), 0))

onMounted(() => {
  dispatchStore.fetchPurchase(route.params.purchaseId)
})
</script>
