<template>
  <div v-if="dispatchStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
    {{ dispatchStore.error }}
  </div>

  <div v-else class="max-w-6xl mx-auto space-y-10 pb-32">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 px-2">
      <div class="space-y-2">
        <span class="eyebrow tracking-[0.4em] !text-amber">Archivo Logistico</span>
        <h1 class="text-5xl font-black tracking-tighter italic text-white">Historial de Despachos</h1>
        <p class="text-text-muted font-medium text-sm">Registro historico de lotes operativos consolidados y procesados con exito.</p>
      </div>

      <div class="flex items-center gap-6 bg-white/[0.06] border border-white/[0.07] backdrop-blur-xl rounded-2xl px-6 py-3 shadow-2xl shadow-black/20">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-amber/10 border border-amber/20 flex items-center justify-center text-amber">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
          <div class="flex flex-col">
            <span class="text-[9px] font-black text-text-muted uppercase tracking-widest">Lotes</span>
            <span class="text-lg font-black text-white leading-none">{{ history.batches.length }}</span>
          </div>
        </div>
        <div class="w-px h-8 bg-white/[0.06]"></div>
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-white/[0.04] border border-white/[0.12] flex items-center justify-center text-white/40">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <div class="flex flex-col">
            <span class="text-[9px] font-black text-text-muted uppercase tracking-widest">Pedidos</span>
            <span class="text-lg font-black text-white leading-none">{{ history.orders.length }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="space-y-4">
      <div class="flex items-center gap-3 px-2">
        <div class="w-1.5 h-6 bg-amber rounded-full"></div>
        <h3 class="text-sm font-black text-white uppercase tracking-tight">Lotes de Despacho</h3>
      </div>
      <div class="card !p-0 border-white/[0.07] bg-white/[0.02] overflow-hidden shadow-[0_40px_100px_-20px_rgba(0,0,0,0.6)]">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm whitespace-nowrap border-collapse">
            <thead>
              <tr class="bg-white/[0.02] border-b border-white/[0.03] text-[10px] uppercase tracking-[0.3em] font-black text-text-muted">
                <th class="px-8 py-5">Identificador</th>
                <th class="px-8 py-5">Cronologia</th>
                <th class="px-8 py-5">Responsable</th>
                <th class="px-8 py-5 text-center">Consolidado</th>
                <th class="px-8 py-5 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/[0.03]">
              <tr v-for="batch in history.batches" :key="batch.id" class="hover:bg-white/[0.01] transition-all group">
                <td class="px-8 py-6">
                  <div class="inline-flex items-center gap-3 px-4 py-1.5 bg-amber/5 border border-amber/10 rounded-xl group-hover:border-amber/40 transition-all">
                    <span class="w-1.5 h-1.5 rounded-full bg-amber shadow-[0_0_8px_rgba(242,173,61,0.4)]"></span>
                    <span class="text-xs font-black text-white tracking-widest">#{{ batch.id }}</span>
                  </div>
                </td>
                <td class="px-8 py-6">
                  <div class="flex flex-col gap-0.5">
                    <p class="font-black text-white text-[13px] uppercase tracking-tight">{{ formatDate(batch.created_at) }}</p>
                    <p class="text-[10px] font-black text-text-muted uppercase tracking-widest">{{ formatTime(batch.created_at) }} HRS</p>
                  </div>
                </td>
                <td class="px-8 py-6">
                  <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-2xl bg-white/[0.04] border border-white/[0.12] flex items-center justify-center text-xs font-black text-amber shadow-inner group-hover:border-amber/30 transition-all">
                      {{ creatorInitial(batch.created_by) }}
                    </div>
                    <div class="flex flex-col">
                      <span class="text-[11px] font-black text-white uppercase tracking-widest">{{ batch.created_by?.name || batch.created_by?.username }}</span>
                      <span class="text-[9px] font-black text-text-muted uppercase tracking-widest mt-0.5 opacity-60">{{ batch.created_by?.role }}</span>
                    </div>
                  </div>
                </td>
                <td class="px-8 py-6 text-center">
                  <div class="flex flex-col items-center gap-1">
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-black text-white tabular-nums">{{ batch.orders?.length ?? 0 }}</span>
                      <span class="text-[9px] font-black text-text-muted uppercase tracking-widest">Sedes</span>
                    </div>
                  </div>
                </td>
                <td class="px-8 py-6 text-right">
                  <RouterLink :to="{ name: 'dispatchBatchDetail', params: { batchId: batch.id } }" class="btn btn-secondary !py-2.5 !px-5 !rounded-xl !text-[10px] border-white/[0.07] hover:border-amber/30 hover:text-amber shadow-none group/link">
                    <span>VER DETALLES</span>
                    <svg class="w-4 h-4 transition-transform group-hover/link:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7" />
                    </svg>
                  </RouterLink>
                </td>
              </tr>
              <tr v-if="!dispatchStore.isLoading && !history.batches.length">
                <td colspan="5">
                  <EmptyState
                    title="Sin lotes"
                    description="Aun no hay lotes despachados en el archivo logistico."
                    class="py-16 bg-transparent border-none shadow-none"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="space-y-4">
      <div class="flex items-center gap-3 px-2">
        <div class="w-1.5 h-6 bg-white/20 rounded-full"></div>
        <h3 class="text-sm font-black text-white uppercase tracking-tight">Historial de Pedidos</h3>
        <span class="text-[10px] font-black text-text-muted bg-white/[0.04] border border-white/[0.07] rounded-lg px-2 py-1 uppercase">{{ history.orders.length }} total</span>
      </div>
      <div class="card !p-0 border-white/[0.07] bg-white/[0.02] overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm whitespace-nowrap border-collapse">
            <thead>
              <tr class="bg-white/[0.02] border-b border-white/[0.03] text-[10px] uppercase tracking-[0.3em] font-black text-text-muted">
                <th class="px-6 py-4">Pedido</th>
                <th class="px-6 py-4">Sede</th>
                <th class="px-6 py-4">Admin</th>
                <th class="px-6 py-4">Fecha</th>
                <th class="px-6 py-4 text-center">Estado</th>
                <th class="px-6 py-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/[0.03]">
              <tr v-for="order in history.orders" :key="order.id" class="hover:bg-white/[0.01] transition-all group">
                <td class="px-6 py-4">
                  <span class="text-[12px] font-black text-white/60 group-hover:text-amber transition-colors">#{{ order.id }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-[12px] font-black text-white uppercase tracking-tight">{{ order.building?.name }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-[11px] font-bold text-text-muted">{{ order.created_by?.name || order.created_by?.username }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-[11px] font-bold text-text-muted">{{ formatDate(order.created_at) }}</span>
                </td>
                <td class="px-6 py-4 text-center">
                  <span class="inline-flex items-center px-3 py-1 rounded-xl text-[9px] font-black uppercase tracking-widest border" :class="statusClass(order.status)">
                    {{ statusLabel(order.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <RouterLink :to="{ name: 'ordersOrderDetail', params: { orderId: order.id } }" class="w-8 h-8 rounded-xl bg-white/[0.05] border border-white/[0.12] text-white hover:bg-amber hover:text-navy-deep hover:border-amber transition-all inline-flex items-center justify-center">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </RouterLink>
                </td>
              </tr>
              <tr v-if="!dispatchStore.isLoading && !history.orders.length">
                <td colspan="6">
                  <EmptyState
                    title="Sin pedidos"
                    description="No hay pedidos registrados aun en el historial."
                    class="py-16 bg-transparent border-none shadow-none"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"

import EmptyState from "@/components/ui/EmptyState.vue"
import { useDispatchStore } from "@/stores/dispatchStore"
import { formatDate, statusClass } from "@/utils/formatters"

const dispatchStore = useDispatchStore()
const history = computed(() => dispatchStore.history ?? { batches: [], orders: [] })

onMounted(() => {
  dispatchStore.fetchHistory()
})

function creatorInitial(user) {
  return String(user?.name || user?.username || "U").trim().charAt(0).toUpperCase()
}

function formatTime(value) {
  return new Intl.DateTimeFormat("es-PE", {
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value))
}

function statusLabel(status) {
  const labels = {
    submitted: "Enviado",
    processing: "En proceso",
    dispatched: "Despachado",
    partially_dispatched: "Parcia. Despachado",
    delivered: "Entregado",
    cancelled: "Cancelado",
    rejected: "Rechazado",
  }

  return labels[status] ?? status
}
</script>
