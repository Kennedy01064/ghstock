<template>
  <div data-testid="manager-dashboard-root" class="space-y-10 pb-24">
    <header class="flex flex-col xl:flex-row xl:items-end justify-between gap-10 border-b border-slate-200 pb-10">
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-6 bg-amber rounded-full shadow-[0_0_12px_rgba(242,173,61,0.4)]"></div>
          <span class="eyebrow tracking-[0.4em] !text-amber text-[10px]">Operación Manager</span>
        </div>
        <h1
          data-testid="manager-dashboard-title"
          class="text-5xl font-black tracking-tighter italic leading-none text-slate-900"
        >
          Tablero <span class="text-amber">Logístico</span>
        </h1>
        <p class="text-text-muted font-medium text-sm md:text-base max-w-xl">
          Vista operativa para <span class="text-slate-900 font-bold capitalize">{{ displayName }}</span>, con foco en cobertura de edificios, pedidos y rotación de catálogo.
        </p>
      </div>

      <div class="flex items-center gap-5 bg-slate-50 border border-slate-200 backdrop-blur-3xl rounded-[2rem] px-8 py-5 shadow-2xl self-start xl:self-auto">
        <div class="text-right">
          <p class="label-premium !mb-0">Fecha Operativa</p>
          <p class="text-slate-900 font-black text-sm tracking-widest tabular-nums uppercase">{{ formatDate(new Date()) }}</p>
        </div>
        <div class="w-[1px] h-10 bg-slate-200"></div>
        <div class="w-10 h-10 bg-amber/10 rounded-xl flex items-center justify-center border border-amber/20 shadow-lg shadow-amber/10">
          <svg class="w-5 h-5 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
      </div>
    </header>

    <div v-if="dashboardStore.error" class="card border border-rose-500/20 bg-rose-50 text-rose-700">
      {{ dashboardStore.error }}
    </div>

    <DashboardSkeleton v-else-if="dashboardStore.isLoading && !dashboard" />

    <div v-else-if="dashboard" class="space-y-12">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <article
        v-for="metric in metrics"
        :key="metric.label"
        class="card group hover:translate-y-[-4px] duration-500 overflow-hidden"
        :class="metric.cardClass"
      >
        <div class="absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.08] transition-opacity duration-700 -rotate-12 pointer-events-none">
          <img :src="logoUrl" alt="" class="w-32 h-auto" />
        </div>
        <div class="relative z-10">
          <div class="flex justify-between items-start mb-6">
            <div class="w-14 h-14 rounded-2xl flex items-center justify-center border transition-all duration-500 shadow-inner" :class="metric.iconWrapClass">
              <svg class="w-7 h-7" :class="metric.iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" :d="metric.iconPath" />
              </svg>
            </div>
          </div>
          <div class="space-y-1">
            <div v-if="metric.prefix" class="flex items-baseline gap-1">
              <span class="text-xl font-bold text-amber/70 tabular-nums">{{ metric.prefix }}</span>
              <p class="text-5xl font-black text-slate-900 tracking-tighter">{{ metric.value }}</p>
            </div>
            <p v-else class="text-5xl font-black text-slate-900 tracking-tighter">{{ metric.value }}</p>
            <div class="flex items-center gap-2" :class="metric.dot ? '' : 'pt-1'">
              <span v-if="metric.dot" class="w-1.5 h-1.5 rounded-full bg-amber animate-pulse"></span>
              <span class="eyebrow !text-slate-500">{{ metric.label }}</span>
            </div>
          </div>
        </div>
      </article>
    </div>


    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <article class="card !p-0 overflow-hidden group">
        <div class="px-8 py-6 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-amber/10 rounded-xl flex items-center justify-center border border-amber/20 shadow-lg shadow-amber/5">
              <svg class="w-5 h-5 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <h3 class="text-base font-bold text-slate-900">Pedidos por Edificio</h3>
              <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-0.5">Distribución de Solicitudes</p>
            </div>
          </div>
        </div>
        <div class="p-8">
          <div class="h-[300px] relative">
            <canvas ref="barChartRef"></canvas>
          </div>
        </div>
      </article>

      <article class="card !p-0 overflow-hidden group">
        <div class="px-8 py-6 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-indigo-500/10 rounded-xl flex items-center justify-center border border-indigo-500/20 shadow-lg shadow-indigo-500/5">
              <svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
              </svg>
            </div>
            <div>
              <h3 class="text-base font-bold text-slate-900">Top 5 Movimientos</h3>
              <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-0.5">Acumulado Total de Pedidos</p>
            </div>
          </div>
        </div>
        <div class="p-8">
          <div class="h-[300px] relative">
            <canvas ref="doughnutChartRef"></canvas>
          </div>
        </div>
      </article>
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
      <article class="card !p-0 overflow-hidden border-slate-200">
        <div class="px-7 py-5 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <h3 class="text-sm font-black text-slate-900 uppercase tracking-widest">Lotes en Proceso</h3>
          <span v-if="dashboard.lotes_pendientes?.length" class="px-3 py-1 bg-amber/10 text-amber text-[10px] font-black rounded-lg border border-amber/20 uppercase tracking-widest">{{ dashboard.lotes_pendientes.length }} activos</span>
        </div>
        <div v-if="dashboard.lotes_pendientes?.length" class="divide-y divide-slate-100">
          <RouterLink v-for="batch in dashboard.lotes_pendientes" :key="batch.id" :to="{ name: 'dispatchBatchDetail', params: { batchId: batch.id } }" class="flex items-center justify-between px-7 py-5 hover:bg-slate-50 transition-colors group">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-xl bg-amber/10 border border-amber/20 flex items-center justify-center text-amber text-xs font-black">#{{ batch.id }}</div>
              <div>
                <p class="text-sm font-black text-slate-900 group-hover:text-amber transition-colors">Lote #{{ batch.id }}</p>
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
          <p class="text-sm font-black text-slate-900 mb-1">Sin lotes pendientes</p>
          <p class="text-[12px] text-text-muted">Todos los despachos están al día.</p>
        </div>
      </article>

      <article class="card !p-0 overflow-hidden border-rose-500/10">
        <div class="px-7 py-5 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <h3 class="text-sm font-black text-slate-900 uppercase tracking-widest">Alertas de Stock</h3>
          <span v-if="dashboard.alertas_stock?.length" class="px-3 py-1 bg-rose-500/10 text-rose-400 text-[10px] font-black rounded-lg border border-rose-500/20 uppercase tracking-widest flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 bg-rose-400 rounded-full animate-pulse"></span>
            {{ dashboard.alertas_stock.length }} críticos
          </span>
        </div>
        <div v-if="dashboard.alertas_stock?.length" class="divide-y divide-slate-100">
          <div v-for="product in dashboard.alertas_stock" :key="product.id" class="flex items-center gap-4 px-7 py-4 hover:bg-slate-50 transition-colors group">
            <img :src="product.imagen_url || defaultProductUrl" :alt="product.name" class="w-10 h-10 rounded-xl object-contain bg-slate-50 p-1.5 border border-slate-200 shrink-0" />
            <div class="flex-1 min-w-0">
              <p class="text-[13px] font-black text-slate-900 truncate group-hover:text-amber transition-colors">{{ product.name }}</p>
              <p class="text-[10px] text-text-muted font-bold">Min: {{ product.stock_minimo }} {{ product.unit }}</p>
            </div>
            <div class="shrink-0 text-right">
              <span class="text-sm font-black" :class="product.stock_actual === 0 ? 'text-red-400' : 'text-amber'">{{ product.stock_actual }}</span>
              <p class="text-[9px] text-text-muted uppercase tracking-widest">{{ product.unit }}</p>
            </div>
          </div>
        </div>
        <div v-else class="px-7 py-10 text-center">
          <p class="text-sm font-black text-slate-900 mb-1">Stock en niveles normales</p>
          <p class="text-[12px] text-text-muted">No hay productos bajo el mínimo.</p>
        </div>
      </article>

      <article class="card !p-0 overflow-hidden border-slate-200">
        <div class="px-7 py-5 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <h3 class="text-sm font-black text-slate-900 uppercase tracking-widest">Compras Recientes</h3>
          <RouterLink :to="{ name: 'dispatchPurchases' }" class="text-[10px] font-black text-amber hover:text-amber/80 uppercase tracking-widest transition-colors">Ver todas</RouterLink>
        </div>
        <div v-if="dashboard.compras_recientes?.length" class="divide-y divide-slate-100">
          <div v-for="purchase in dashboard.compras_recientes" :key="purchase.id" class="px-7 py-4 hover:bg-slate-50 transition-colors group">
            <div class="flex items-start justify-between gap-4">
              <div class="min-w-0">
                <p class="text-sm font-black text-slate-900 group-hover:text-amber transition-colors">#{{ purchase.id }} {{ purchase.supplier || "Proveedor no definido" }}</p>
                <p class="text-[10px] text-text-muted font-bold uppercase tracking-widest mt-1">{{ formatDate(purchase.purchase_date) }}</p>
              </div>
              <div class="text-right shrink-0">
                <p class="text-sm font-black text-emerald-400">S/ {{ formatDecimal(purchase.total_amount || 0) }}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="px-7 py-10 text-center">
          <p class="text-sm font-black text-slate-900 mb-1">Sin compras registradas</p>
          <p class="text-[12px] text-text-muted">Todavía no hay movimientos de abastecimiento recientes.</p>
        </div>
      </article>
    </div>

    <article class="card !p-0 border-slate-200 mb-24 relative z-[60]">
      <div class="px-8 py-6 border-b border-slate-200 flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-slate-50 rounded-t-[20px]">
        <div class="flex items-center gap-4">
          <div class="w-11 h-11 rounded-2xl bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center shadow-lg shadow-cyan-400/5">
            <svg class="w-5 h-5 text-cyan-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <h3 class="text-base font-black text-slate-900 italic uppercase tracking-tighter leading-none">Ventana de envio <span class="text-amber">Operativa</span></h3>
            <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-0.5">Fecha limite para listas y pedidos de administradores</p>
          </div>
        </div>

        <span class="inline-flex items-center rounded-full border px-4 py-2 text-[10px] font-black uppercase tracking-[0.2em]" :class="submissionDeadline ? deadlineStateClass(submissionDeadline.state) : 'border-slate-200 bg-slate-50 text-text-muted'">
          {{ submissionDeadline ? deadlineStateLabel(submissionDeadline.state) : "Sin fecha activa" }}
        </span>
      </div>

      <div class="grid gap-6 xl:grid-cols-[minmax(0,1.1fr)_360px] p-8">
        <form class="space-y-5" @submit.prevent="saveDeadline">
          <div class="grid gap-5 md:grid-cols-2">
            <div class="space-y-2">
              <label class="label-premium">Fecha y hora limite</label>
                <PremiumDateTimePicker
                  v-model="deadlineForm.order_submission_deadline_at"
                />
            </div>

            <div class="space-y-2">
              <label class="label-premium">Nota operativa</label>
              <input
                v-model="deadlineForm.order_submission_deadline_note"
                type="text"
                maxlength="180"
                class="input-field"
                placeholder="Ej. Enviar listas completas antes del corte"
              />
            </div>
          </div>

          <div class="rounded-[28px] border border-slate-200 bg-slate-50 px-5 py-4 text-sm leading-7 text-text-secondary">
            La alerta se mostrara en el dashboard admin. Si la fecha vence y aun existen borradores, el aviso cambiara a estado critico.
          </div>

          <div class="flex flex-col sm:flex-row gap-4">
            <button type="submit" class="btn btn-primary flex-1" :disabled="isSavingDeadline">
              {{ isSavingDeadline ? "Guardando..." : "Guardar fecha limite" }}
            </button>
            <button type="button" class="btn btn-secondary flex-1" :disabled="isSavingDeadline" @click="clearDeadline">
              Limpiar fecha
            </button>
          </div>
        </form>

        <aside class="rounded-[32px] border p-6 space-y-4 shadow-2xl" :class="submissionDeadline ? deadlineStatePanelClass(submissionDeadline.state) : 'border-slate-200 bg-slate-50'">
          <p class="text-[10px] font-black uppercase tracking-[0.24em]" :class="submissionDeadline ? (submissionDeadline.state === 'overdue' ? 'text-rose-200' : 'text-cyan-200') : 'text-text-muted'">
            Estado actual
          </p>

          <template v-if="submissionDeadline">
            <div class="space-y-2">
              <p class="text-2xl font-black text-slate-900 leading-tight uppercase tracking-tighter tabular-nums">{{ formatDateTime(submissionDeadline.deadline_at) }}</p>
              <p class="text-sm font-bold" :class="submissionDeadline.state === 'overdue' ? 'text-rose-200' : 'text-cyan-100'">
                {{ relativeDeadlineCopy(submissionDeadline.deadline_at, submissionDeadline.state) }}
              </p>
            </div>

            <div class="rounded-2xl border border-slate-200 bg-slate-100 px-4 py-4 space-y-2">
              <p class="text-[10px] font-black uppercase tracking-[0.2em] text-text-muted">Listas pendientes</p>
              <p class="text-3xl font-black text-slate-900">{{ submissionDeadline.pending_orders_count }}</p>
              <p class="text-xs leading-6 text-text-secondary font-bold">
                {{ submissionDeadline.pending_orders_count === 1 ? "Hay 1 borrador activo sin enviar." : `Hay ${submissionDeadline.pending_orders_count} borradores activos sin enviar.` }}
              </p>
            </div>

            <p v-if="submissionDeadline.note" class="text-sm leading-7 text-text-secondary italic">
              "{{ submissionDeadline.note }}"
            </p>
          </template>

          <template v-else>
            <p class="text-xl font-black text-slate-900 italic">Sin fecha limite configurada</p>
            <p class="text-sm leading-7 text-text-secondary font-medium">
              Define una ventana de envio para que los administradores reciban la alerta desde su panel principal.
            </p>
          </template>
        </aside>
      </div>
    </article>

    <div class="mt-12 space-y-6">
      <div class="flex items-center gap-4">
        <h3 class="label-premium !mb-0 whitespace-nowrap">Acceso Rápido</h3>
        <div class="h-px bg-slate-50 flex-grow"></div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <RouterLink
          v-for="item in navItems"
          :key="item.label"
          :to="item.to"
          class="card !p-6 flex flex-col items-center justify-center gap-3 group hover:border-amber/40 hover:bg-amber/5 transition-all duration-300"
        >
          <div class="relative">
            <div class="w-12 h-12 bg-slate-50 rounded-2xl flex items-center justify-center group-hover:scale-110 group-hover:bg-amber group-hover:text-navy transition-all duration-500 shadow-lg">
              <svg class="w-6 h-6 text-slate-900 group-hover:text-navy" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" :d="item.iconPath" />
              </svg>
            </div>
            <span v-if="item.count" class="absolute -top-1 -right-1 w-5 h-5 bg-rose-500 text-slate-900 text-[10px] font-black rounded-full flex items-center justify-center border-2 border-navy-deep shadow-lg">
              {{ item.count }}
            </span>
          </div>
          <p class="text-[11px] font-black text-text-muted uppercase tracking-[0.2em] group-hover:text-slate-900 transition-colors text-center">{{ item.label }}</p>
        </RouterLink>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { Chart } from "chart.js/auto"
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue"

import operationsApi from "@/api/operations.api"
import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import PremiumDateTimePicker from "@/components/ui/PremiumDateTimePicker.vue"
import { useAuthStore } from "@/stores/authStore"
import { useDashboardStore } from "@/stores/dashboardStore"
import { useUiStore } from "@/stores/uiStore"
import { defaultProductUrl, formatDate, logoUrl } from "@/utils/formatters"

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()
const uiStore = useUiStore()
const barChartRef = ref(null)
const doughnutChartRef = ref(null)
const isSavingDeadline = ref(false)
const deadlineForm = reactive({
  order_submission_deadline_at: "",
  order_submission_deadline_note: "",
})
let barChart = null
let doughnutChart = null

const dashboard = computed(() => dashboardStore.managerDashboard)
const submissionDeadline = computed(() => dashboard.value?.submission_deadline ?? null)
const displayName = computed(() => authStore.user?.name || authStore.user?.username || "Usuario")
const metrics = computed(() => [
  {
    label: "Pedidos en Espera",
    value: dashboard.value?.pedidos_submitted ?? 0,
    iconWrapClass: "bg-amber/15 group-hover:bg-amber/20 border-amber/25 group-hover:border-amber/40",
    iconClass: "text-amber",
    iconPath: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2",
    dot: true,
    cardClass: "hover:shadow-[0_30px_60px_-15px_rgba(242,173,61,0.1)]",
  },
  {
    label: "Edificios Operativos",
    value: dashboard.value?.total_edificios_activos ?? 0,
    iconWrapClass: "bg-slate-50 group-hover:bg-slate-50 border-slate-200 group-hover:border-slate-300",
    iconClass: "text-slate-500 group-hover:text-slate-700 transition-colors",
    iconPath: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4",
    cardClass: "hover:shadow-[0_30px_60px_-15px_rgba(255,255,255,0.05)]",
  },
  {
    label: "Flujo Mensual",
    value: formatDecimal(dashboard.value?.costo_despachado_mes ?? 0),
    prefix: "S/",
    iconWrapClass: "bg-emerald-500/15 group-hover:bg-emerald-500/20 border-emerald-500/25 group-hover:border-emerald-500/40",
    iconClass: "text-emerald-600",
    iconPath: "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
    cardClass: "border-emerald-500/10 hover:shadow-[0_30px_60px_-15px_rgba(16,185,129,0.08)]",
  },
  {
    label: "Catálogo Activo",
    value: dashboard.value?.total_productos ?? 0,
    iconWrapClass: "bg-slate-50 group-hover:bg-slate-50 border-slate-200 group-hover:border-slate-300",
    iconClass: "text-slate-500 group-hover:text-slate-700 transition-colors",
    iconPath: "M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4",
    cardClass: "hover:shadow-[0_30px_60px_-15px_rgba(255,255,255,0.05)]",
  },
])

const navItems = computed(() => [
  { to: { name: "dispatchPending" }, iconPath: "M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4", label: "Despacho", count: dashboard.value?.pedidos_submitted ?? 0 },
  { to: { name: "catalogBuildings" }, iconPath: "M3 21h18M5 21V5a2 2 0 012-2h10a2 2 0 012 2v16m-14 0h14", label: "Edificios" },
  { to: { name: "catalogAssignBuilding" }, iconPath: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4", label: "Asignar" },
  { to: { name: "catalogAdminCreate" }, iconPath: "M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0z", label: "Nuevo Admin" },
  { to: { name: "dispatchPurchases" }, iconPath: "M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z", label: "Compras" },
])

onMounted(async () => {
  await dashboardStore.fetchManagerDashboard()
})

watch(
  dashboard,
  async (value) => {
    if (!value) {
      destroyCharts()
      return
    }

    await nextTick()
    renderCharts()
  },
  { deep: true },
)

watch(
  submissionDeadline,
  () => {
    syncDeadlineForm()
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  destroyCharts()
})

function formatDecimal(value) {
  return Number(value ?? 0).toFixed(2)
}

function formatDateTime(value) {
  if (!value) {
    return "-"
  }

  return new Intl.DateTimeFormat("es-PE", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value))
}

function syncDeadlineForm() {
  deadlineForm.order_submission_deadline_at = submissionDeadline.value?.deadline_at ?? ""
  deadlineForm.order_submission_deadline_note = submissionDeadline.value?.note ?? ""
}

function deadlineStateLabel(state) {
  return state === "overdue" ? "Vencida" : "Programada"
}

function deadlineStateClass(state) {
  return state === "overdue"
    ? "border-rose-400/30 bg-rose-500/10 text-rose-200"
    : "border-cyan-400/30 bg-cyan-400/10 text-cyan-100"
}

function deadlineStatePanelClass(state) {
  return state === "overdue"
    ? "border-rose-500/20 bg-rose-500/10"
    : "border-cyan-400/20 bg-cyan-400/5"
}

function relativeDeadlineCopy(value, state) {
  if (!value) {
    return ""
  }

  const diffMs = new Date(value).getTime() - Date.now()
  const diffHours = Math.round(Math.abs(diffMs) / 36e5)

  if (state === "overdue") {
    if (diffHours < 1) {
      return "La fecha limite ya expiro."
    }
    return `La ventana ya vencio hace ${diffHours} hora${diffHours === 1 ? "" : "s"}.`
  }

  if (diffHours < 1) {
    return "El cierre ocurre en menos de una hora."
  }

  return `El cierre esta previsto en ${diffHours} hora${diffHours === 1 ? "" : "s"}.`
}

async function saveDeadline() {
  if (!deadlineForm.order_submission_deadline_at) {
    uiStore.error("Selecciona una fecha limite para guardar la alerta.", "Falta la fecha")
    return
  }

  isSavingDeadline.value = true

  try {
    await operationsApi.updateOrderDeadline({
      order_submission_deadline_at: deadlineForm.order_submission_deadline_at,
      order_submission_deadline_note: deadlineForm.order_submission_deadline_note.trim() || null,
    })
    await dashboardStore.fetchManagerDashboard()
    uiStore.success("La alerta para administradores fue actualizada.", "Fecha limite guardada")
  } catch (error) {
    uiStore.error(error.message, "No se pudo guardar la fecha limite")
  } finally {
    isSavingDeadline.value = false
  }
}

async function clearDeadline() {
  isSavingDeadline.value = true

  try {
    await operationsApi.updateOrderDeadline({
      order_submission_deadline_at: null,
      order_submission_deadline_note: null,
    })
    await dashboardStore.fetchManagerDashboard()
    uiStore.warning("La fecha limite operativa fue retirada.", "Fecha eliminada")
  } catch (error) {
    uiStore.error(error.message, "No se pudo limpiar la fecha limite")
  } finally {
    isSavingDeadline.value = false
  }
}

function destroyCharts() {
  if (barChart) {
    barChart.destroy()
    barChart = null
  }

  if (doughnutChart) {
    doughnutChart.destroy()
    doughnutChart = null
  }
}

function renderCharts() {
  if (!barChartRef.value || !doughnutChartRef.value || !dashboard.value) {
    return
  }

  destroyCharts()

  const barCtx = barChartRef.value.getContext("2d")
  const doughnutCtx = doughnutChartRef.value.getContext("2d")
  const gradient = barCtx.createLinearGradient(0, 0, 0, 300)
  gradient.addColorStop(0, "#F2AD3D")
  gradient.addColorStop(0.5, "rgba(242, 173, 61, 0.80)")
  gradient.addColorStop(1, "rgba(242, 173, 61, 0.60)")

  barChart = new Chart(barCtx, {
    type: "bar",
    data: {
      labels: dashboard.value.chart_edificios_labels ?? [],
      datasets: [
        {
          data: dashboard.value.chart_edificios_data ?? [],
          backgroundColor: gradient,
          borderRadius: 12,
          borderSkipped: false,
          barThickness: 32,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#0f172a",
          titleColor: "#F2AD3D",
          bodyColor: "#ffffff",
          borderColor: "#334155",
          borderWidth: 1,
          padding: 16,
          cornerRadius: 16,
          displayColors: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1, color: "#64748b" },
          grid: { color: "#e2e8f0", drawBorder: false },
        },
        x: {
          ticks: { color: "#334155" },
          grid: { display: false },
        },
      },
    },
  })

  doughnutChart = new Chart(doughnutCtx, {
    type: "doughnut",
    data: {
      labels: dashboard.value.chart_productos_labels ?? [],
      datasets: [
        {
          data: dashboard.value.chart_productos_data ?? [],
          backgroundColor: ["#F2AD3D", "#4F46E5", "#10B981", "#6B7280", "#F43F5E"],
          borderColor: "#ffffff",
          borderWidth: 4,
          hoverOffset: 20,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "72%",
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            padding: 24,
            color: "#334155",
            usePointStyle: true,
            pointStyle: "circle",
            boxWidth: 10,
            font: {
              size: 11,
              weight: 700,
            },
          },
        },
        tooltip: {
          backgroundColor: "#0f172a",
          titleColor: "#F2AD3D",
          bodyColor: "#ffffff",
          borderColor: "#334155",
          borderWidth: 1,
          padding: 16,
          cornerRadius: 16,
        },
      },
    },
  })
}
</script>
