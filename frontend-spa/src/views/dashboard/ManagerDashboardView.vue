<template>
  <div v-if="dashboardStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
    {{ dashboardStore.error }}
  </div>

  <DashboardSkeleton v-else-if="dashboardStore.isLoading && !dashboard" />

  <div v-else-if="dashboard" class="max-w-[1320px] mx-auto px-4 sm:px-8 xl:px-10 py-8 space-y-10">
    <div class="relative bg-gradient-to-br from-[#041120] via-[#05142b] to-black rounded-[2rem] p-7 md:p-12 text-white shadow-2xl overflow-hidden border border-white/5">
      <div class="absolute -top-20 -right-20 w-80 h-80 bg-amber/10 rounded-full blur-[100px]"></div>
      <div class="relative z-10 flex flex-col xl:flex-row xl:items-center justify-between gap-8">
        <div class="space-y-4">
          <div class="inline-flex items-center gap-3 px-4 py-2 rounded-xl bg-white/[0.03] border border-white/10">
            <span class="w-2 h-2 bg-amber rounded-full animate-pulse shadow-[0_0_12px_rgba(242,173,61,0.8)]"></span>
            <span class="text-[10px] font-black uppercase tracking-[0.3em] text-amber-soft">Operaciones de Almacen</span>
          </div>
          <h1 class="text-3xl md:text-5xl font-black tracking-tight leading-tight">
            <span class="text-white/40 block text-2xl font-bold mb-1">Bienvenido,</span>
            <span class="text-white">{{ displayName }}</span>
          </h1>
          <p class="text-text-secondary text-base opacity-80 max-w-lg">Panel de gestion de despacho y logistica del almacen central.</p>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 w-full xl:w-auto shrink-0">
          <article v-for="metric in metrics" :key="metric.label" class="card !p-5 md:!p-7 !bg-white/[0.02] border-white/5" :class="metric.cardClass">
            <div class="flex items-center justify-between mb-1">
              <p class="text-3xl md:text-4xl font-black mb-1" :class="metric.valueClass">{{ metric.value }}</p>
              <span v-if="metric.pulse" class="flex h-3 w-3 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
              </span>
            </div>
            <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em]">{{ metric.label }}</p>
          </article>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <RouterLink :to="{ name: 'dispatchPending' }" class="card flex items-center gap-5 hover:border-amber/40 hover:-translate-y-1 transition-all group">
        <div class="w-12 h-12 shrink-0 rounded-2xl bg-amber/10 border border-amber/20 flex items-center justify-center text-amber group-hover:bg-amber group-hover:text-navy-deep transition-all">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <div>
          <p class="text-sm font-black text-white uppercase tracking-tight group-hover:text-amber transition-colors">Consolidar Pedidos</p>
          <p class="text-[10px] text-text-muted font-bold">{{ dashboard.pedidos_submitted }} solicitudes listas</p>
        </div>
      </RouterLink>
      <RouterLink :to="{ name: 'dispatchHistory' }" class="card flex items-center gap-5 hover:border-white/20 hover:-translate-y-1 transition-all group">
        <div class="w-12 h-12 shrink-0 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-text-muted group-hover:border-white/20 transition-all">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <p class="text-sm font-black text-white uppercase tracking-tight">Historial Despachos</p>
          <p class="text-[10px] text-text-muted font-bold">Lotes procesados</p>
        </div>
      </RouterLink>
      <RouterLink :to="{ name: 'dispatchPurchaseCreate' }" class="card flex items-center gap-5 hover:border-emerald-500/30 hover:-translate-y-1 transition-all group">
        <div class="w-12 h-12 shrink-0 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 transition-all">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
          </svg>
        </div>
        <div>
          <p class="text-sm font-black text-white uppercase tracking-tight group-hover:text-emerald-400 transition-colors">Nueva Compra</p>
          <p class="text-[10px] text-text-muted font-bold">Ingresar stock al almacen</p>
        </div>
      </RouterLink>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="card !p-0 overflow-hidden border-white/5">
        <div class="px-7 py-5 border-b border-white/5 flex items-center justify-between bg-white/[0.01]">
          <h3 class="text-sm font-black text-white uppercase tracking-widest">Lotes en Proceso</h3>
          <span v-if="dashboard.lotes_pendientes?.length" class="px-3 py-1 bg-amber/10 text-amber text-[10px] font-black rounded-lg border border-amber/20 uppercase tracking-widest">{{ dashboard.lotes_pendientes.length }} activos</span>
        </div>
        <div v-if="dashboard.lotes_pendientes?.length" class="divide-y divide-white/[0.04]">
          <RouterLink v-for="batch in dashboard.lotes_pendientes" :key="batch.id" :to="{ name: 'dispatchBatchDetail', params: { batchId: batch.id } }" class="flex items-center justify-between px-7 py-5 hover:bg-white/[0.02] transition-colors group">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-xl bg-amber/10 border border-amber/20 flex items-center justify-center text-amber text-xs font-black">#{{ batch.id }}</div>
              <div>
                <p class="text-sm font-black text-white group-hover:text-amber transition-colors">Lote #{{ batch.id }}</p>
                <p class="text-[10px] text-text-muted font-bold">{{ batch.orders?.length ?? 0 }} sedes / {{ batch.items?.length ?? 0 }} SKUs</p>
              </div>
            </div>
            <div class="text-right">
              <span class="text-[9px] font-black text-amber uppercase tracking-widest bg-amber/5 px-3 py-1.5 rounded-lg border border-amber/10">Pendiente</span>
              <p class="text-[10px] text-text-muted mt-1">{{ formatDate(batch.created_at) }}</p>
            </div>
          </RouterLink>
        </div>
        <div v-else class="px-7 py-10 text-center">
          <div class="w-14 h-14 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg class="w-7 h-7 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-sm font-black text-white mb-1">Sin lotes pendientes</p>
          <p class="text-[12px] text-text-muted">Todos los despachos estan al dia.</p>
        </div>
      </div>

      <div class="card !p-0 overflow-hidden border-white/5">
        <div class="px-7 py-5 border-b border-white/5 flex items-center justify-between bg-white/[0.01]">
          <h3 class="text-sm font-black text-white uppercase tracking-widest">Alertas de Stock</h3>
          <span v-if="dashboard.alertas_stock?.length" class="px-3 py-1 bg-rose-500/10 text-rose-400 text-[10px] font-black rounded-lg border border-rose-500/20 uppercase tracking-widest flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 bg-rose-400 rounded-full animate-pulse"></span>
            {{ dashboard.alertas_stock.length }} criticos
          </span>
        </div>
        <div v-if="dashboard.alertas_stock?.length" class="divide-y divide-white/[0.04]">
          <div v-for="product in dashboard.alertas_stock" :key="product.id" class="flex items-center gap-4 px-7 py-4 hover:bg-white/[0.02] transition-colors group">
            <img :src="product.imagen_url || defaultProductUrl" :alt="product.name" class="w-10 h-10 rounded-xl object-contain bg-white/5 p-1.5 border border-white/10 shrink-0" />
            <div class="flex-1 min-w-0">
              <p class="text-[13px] font-black text-white truncate group-hover:text-amber transition-colors">{{ product.name }}</p>
              <p class="text-[10px] text-text-muted font-bold">Min: {{ product.stock_minimo }} {{ product.unit }}</p>
            </div>
            <div class="shrink-0 text-right">
              <span class="text-sm font-black" :class="product.stock_actual === 0 ? 'text-red-400' : 'text-amber'">{{ product.stock_actual }}</span>
              <p class="text-[9px] text-text-muted uppercase tracking-widest">{{ product.unit }}</p>
            </div>
          </div>
        </div>
        <div v-else class="px-7 py-10 text-center">
          <p class="text-sm font-black text-white mb-1">Stock en niveles normales</p>
          <p class="text-[12px] text-text-muted">No hay productos bajo el minimo.</p>
        </div>
      </div>
    </div>

    <div v-if="dashboard.compras_recientes?.length" class="card !p-0 overflow-hidden border-white/5">
      <div class="px-7 py-5 border-b border-white/5 flex items-center justify-between bg-white/[0.01]">
        <h3 class="text-sm font-black text-white uppercase tracking-widest">Compras Recientes</h3>
        <RouterLink :to="{ name: 'dispatchPurchases' }" class="text-[10px] font-black text-amber hover:text-amber/80 uppercase tracking-widest transition-colors">Ver todas -></RouterLink>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="bg-white/[0.02] border-b border-white/5">
            <tr>
              <th class="px-7 py-4 text-[10px] font-black text-amber uppercase tracking-[0.3em]">ID</th>
              <th class="px-7 py-4 text-[10px] font-black text-white/60 uppercase tracking-[0.3em]">Proveedor</th>
              <th class="px-7 py-4 text-[10px] font-black text-white/60 uppercase tracking-[0.3em] hidden sm:table-cell">Fecha</th>
              <th class="px-7 py-4 text-[10px] font-black text-white/60 uppercase tracking-[0.3em] text-right">Total</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/[0.04]">
            <tr v-for="purchase in dashboard.compras_recientes" :key="purchase.id" class="hover:bg-white/[0.02] transition-colors group">
              <td class="px-7 py-4 text-sm font-black text-amber">#{{ purchase.id }}</td>
              <td class="px-7 py-4 text-[13px] font-bold text-white group-hover:text-amber transition-colors">{{ purchase.supplier || "—" }}</td>
              <td class="px-7 py-4 text-[12px] text-text-muted hidden sm:table-cell">{{ formatDate(purchase.purchase_date) }}</td>
              <td class="px-7 py-4 text-right text-sm font-black text-emerald-400">S/ {{ Number(purchase.total_amount || 0).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"

import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import { useAuthStore } from "@/stores/authStore"
import { useDashboardStore } from "@/stores/dashboardStore"
import { defaultProductUrl, formatDate, titleCase } from "@/utils/formatters"

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()

const dashboard = computed(() => dashboardStore.managerDashboard)
const displayName = computed(() => titleCase(authStore.user?.name || authStore.user?.username || "Usuario"))
const metrics = computed(() => [
  { label: "Pendientes", value: dashboard.value?.pedidos_submitted ?? 0, valueClass: "text-amber", cardClass: "hover:border-amber/20" },
  { label: "Lotes Activos", value: dashboard.value?.lotes_pendientes?.length ?? 0, valueClass: "text-white", cardClass: "" },
  {
    label: "Stock Bajo",
    value: dashboard.value?.alertas_stock?.length ?? 0,
    valueClass: "text-rose-400",
    cardClass: "hover:border-rose-500/20 col-span-2 sm:col-span-1",
    pulse: (dashboard.value?.alertas_stock?.length ?? 0) > 0,
  },
])

onMounted(() => {
  dashboardStore.fetchManagerDashboard()
})
</script>
