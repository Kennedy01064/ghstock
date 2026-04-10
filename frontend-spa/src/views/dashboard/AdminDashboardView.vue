<template>
  <div v-if="dashboardStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
    {{ dashboardStore.error }}
  </div>

  <DashboardSkeleton v-else-if="dashboardStore.isLoading && !dashboard" />

  <div v-else-if="dashboard" class="max-w-[1320px] mx-auto px-5 py-8 md:px-8 xl:px-10 space-y-10">
    <div class="relative bg-gradient-to-br from-[#041120] via-[#05142b] to-black rounded-[2.5rem] p-8 md:p-14 text-white shadow-2xl overflow-hidden border border-white/5 group">
      <div class="absolute -top-24 -right-24 w-96 h-96 bg-amber/10 rounded-full blur-[120px] group-hover:bg-amber/20 transition-all duration-1000"></div>
      <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-navy-accent/20 rounded-full blur-[100px]"></div>

      <div class="relative z-10">
        <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-12">
          <div class="flex-1 space-y-6">
            <div class="inline-flex items-center gap-3 px-4 py-2 rounded-xl bg-white/[0.03] border border-white/10 backdrop-blur-2xl">
              <span class="w-2 h-2 bg-amber rounded-full animate-pulse shadow-[0_0_12px_rgba(242,173,61,0.8)]"></span>
              <span class="text-[10px] font-black uppercase tracking-[0.3em] text-amber-soft">Centro de Operaciones</span>
            </div>

            <h1 class="text-4xl md:text-5xl lg:text-6xl font-black tracking-tight leading-[0.95]">
              <span class="text-white/40 block mb-2 text-3xl font-bold">Resumen Operativo,</span>
              <span class="text-white drop-shadow-2xl">{{ displayName }}</span>
            </h1>

            <p class="text-text-secondary text-lg md:max-w-xl leading-relaxed font-medium opacity-80">
              Estado logistico en tiempo real para su gestion administrativa.
            </p>

            <div class="inline-flex items-center gap-4 bg-white/[0.03] border border-white/5 backdrop-blur-3xl rounded-2xl px-6 py-3 shadow-2xl">
              <div class="text-right">
                <p class="text-[10px] font-black text-amber uppercase tracking-widest leading-none mb-1">Fecha Operativa</p>
                <p class="text-white font-black text-sm tracking-widest tabular-nums uppercase whitespace-nowrap">{{ formatDate(new Date()) }}</p>
              </div>
              <div class="w-[1px] h-8 bg-white/10"></div>
              <div class="w-8 h-8 bg-amber/10 rounded-lg flex items-center justify-center border border-amber/20 shadow-lg shadow-amber/10">
                <svg class="w-4 h-4 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 lg:grid-cols-4 gap-5 w-full xl:w-auto shrink-0">
            <article v-for="metric in metrics" :key="metric.label" class="card !p-6 md:!p-8 group/stat !bg-white/[0.02] hover:!bg-white/[0.05] transition-all border-white/5" :class="metric.cardClass">
              <div class="flex items-center justify-between mb-2">
                <p class="text-4xl md:text-5xl font-black mb-2 group-hover/stat:scale-110 transition-transform origin-left" :class="metric.valueClass">{{ metric.value }}</p>
                <span v-if="metric.pulse" class="flex h-3 w-3 relative">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" :class="metric.pulseClass"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3" :class="metric.dotClass"></span>
                </span>
              </div>
              <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em]">{{ metric.label }}</p>
            </article>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="submissionDeadline"
      class="rounded-[2rem] border p-6 md:p-8 shadow-[0_0_40px_rgba(4,17,32,0.18)]"
      :class="submissionDeadline.state === 'overdue' ? 'border-rose-500/30 bg-rose-500/10' : 'border-cyan-400/20 bg-cyan-400/5'"
    >
      <div class="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
        <div class="flex items-start gap-4">
          <div
            class="w-11 h-11 rounded-2xl border flex items-center justify-center shrink-0"
            :class="submissionDeadline.state === 'overdue' ? 'border-rose-400/30 bg-rose-500/15 text-rose-200' : 'border-cyan-400/30 bg-cyan-400/10 text-cyan-100'"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>

          <div class="space-y-2">
            <div class="flex flex-wrap items-center gap-3">
              <h3 class="text-lg font-black text-white uppercase tracking-[0.12em]">Alerta de cierre operativo</h3>
              <span class="inline-flex items-center rounded-full border px-3 py-1 text-[10px] font-black uppercase tracking-[0.2em]" :class="submissionDeadline.state === 'overdue' ? 'border-rose-400/30 bg-rose-500/10 text-rose-100' : 'border-cyan-400/30 bg-cyan-400/10 text-cyan-100'">
                {{ submissionDeadline.state === "overdue" ? "Vencida" : "Programada" }}
              </span>
            </div>

            <p class="text-sm leading-7 text-text-secondary">
              {{ submissionDeadline.state === "overdue" ? "La fecha limite para enviar listas ya vencio." : "Existe una fecha limite activa para el envio de listas." }}
            </p>

            <div class="flex flex-wrap items-center gap-4 text-sm font-bold">
              <span class="text-white">{{ formatDateTime(submissionDeadline.deadline_at) }}</span>
              <span :class="submissionDeadline.state === 'overdue' ? 'text-rose-200' : 'text-cyan-100'">
                {{ deadlineRelativeCopy(submissionDeadline.deadline_at, submissionDeadline.state) }}
              </span>
            </div>

            <p v-if="submissionDeadline.note" class="text-sm leading-7 text-text-secondary">
              {{ submissionDeadline.note }}
            </p>
          </div>
        </div>

        <div class="w-full max-w-[280px] rounded-[28px] border border-white/10 bg-black/10 px-5 py-5 space-y-3 shrink-0">
          <p class="text-[10px] font-black uppercase tracking-[0.24em] text-text-muted">Listas pendientes</p>
          <p class="text-4xl font-black text-white">{{ submissionDeadline.pending_orders_count }}</p>
          <p class="text-xs leading-6 text-text-secondary">
            {{ submissionDeadline.pending_orders_count === 0 ? "No tienes borradores pendientes por enviar." : submissionDeadline.pending_orders_count === 1 ? "Mantienes 1 lista en borrador pendiente de envio." : `Mantienes ${submissionDeadline.pending_orders_count} listas en borrador pendientes de envio.` }}
          </p>
          <RouterLink :to="{ name: 'ordersMyOrders' }" class="btn btn-secondary w-full !py-3 !text-[10px]">
            Revisar mis pedidos
          </RouterLink>
        </div>
      </div>
    </div>

    <div v-if="dashboard.pedidos_despachados?.length" class="rounded-[2rem] border border-blue-500/30 bg-blue-500/5 p-6 md:p-8 shadow-[0_0_40px_rgba(59,130,246,0.05)]">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded-2xl bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-black text-white uppercase tracking-widest">Pedidos en Transito</h3>
            <p class="text-[10px] text-blue-400 font-bold uppercase tracking-widest">{{ dashboard.pedidos_despachados.length }} listo<span v-if="dashboard.pedidos_despachados.length !== 1">s</span> para recibir</p>
          </div>
        </div>
        <span class="flex h-3 w-3 relative shrink-0">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
        </span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <div v-for="order in dashboard.pedidos_despachados" :key="order.id" class="bg-white/[0.03] border border-white/10 rounded-2xl p-4 flex flex-col gap-3 hover:border-blue-400/30 transition-all">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-black text-blue-400 uppercase tracking-widest">Pedido #{{ order.id }}</span>
            <span class="text-[10px] text-text-muted">{{ formatDate(order.created_at) }}</span>
          </div>
          <p class="text-sm font-black text-white">{{ order.building?.name }}</p>
          <p class="text-[11px] text-text-muted">{{ order.items?.length ?? 0 }} producto<span v-if="(order.items?.length ?? 0) !== 1">s</span></p>
          <button
            type="button"
            class="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-blue-500/20 text-blue-300 border border-blue-500/30 text-[10px] font-black uppercase tracking-widest hover:bg-blue-500/30 transition-all"
            :disabled="ordersStore.isReceivingOrder"
            @click="receiveOrder(order.id)"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
            Confirmar Recepcion
          </button>
        </div>
      </div>
    </div>

    <section class="space-y-10">
      <div class="flex items-end justify-between border-b border-white/5 pb-6">
        <div class="space-y-2">
          <div class="flex items-center gap-3">
            <div class="w-1 h-5 bg-amber rounded-full shadow-[0_0_12px_rgba(242,173,61,0.4)]"></div>
            <span class="eyebrow !text-white text-[10px] tracking-[0.4em]">Activos Directos</span>
          </div>
          <h2 class="text-3xl font-black text-white tracking-tight uppercase">Mis Edificios</h2>
        </div>
        <div class="px-5 py-2.5 bg-white/[0.03] border border-white/10 rounded-xl backdrop-blur-xl">
          <span class="text-[10px] font-black text-amber uppercase tracking-[0.2em]">{{ dashboard.buildings.length }} UNIDADES VINCULADAS</span>
        </div>
      </div>

      <div v-if="dashboard.buildings?.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <article v-for="building in dashboard.buildings" :key="building.id" class="card flex flex-col group overflow-hidden border-white/10 hover:border-amber/30 hover:shadow-[0_20px_50px_rgba(4,17,32,0.4)]">
          <div class="relative h-48 -mx-7 -mt-7 mb-7 overflow-hidden bg-navy/20">
            <img v-if="buildingImage(building)" :src="buildingImage(building)" :alt="building.name" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 opacity-90 group-hover:opacity-100" />
            <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-navy-accent/20 to-navy/30">
              <svg class="w-12 h-12 text-white/10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-navy-deep/80 via-transparent to-transparent opacity-60 group-hover:opacity-40 transition-opacity"></div>
            <div class="absolute bottom-4 left-6 translate-y-2 group-hover:translate-y-0 transition-transform opacity-0 group-hover:opacity-100">
              <p class="text-white text-[10px] font-black uppercase tracking-widest drop-shadow-lg bg-amber/90 px-2 py-1 rounded">Activo</p>
            </div>
          </div>

          <div class="flex flex-col flex-1">
            <div class="mb-6 flex-1">
              <h3 class="text-xl font-black text-rose-50/90 leading-tight mb-2 group-hover:text-amber transition-colors">{{ building.name }}</h3>
              <div class="flex items-center gap-2 text-text-secondary">
                <svg class="w-4 h-4 shrink-0 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span class="text-[13px] font-bold truncate opacity-80">{{ building.address || "Sin direccion registrada" }}</span>
              </div>
            </div>

            <div class="flex flex-col gap-5 mt-auto">
              <div class="flex items-center justify-between px-5 py-4 bg-white/[0.02] rounded-2xl border border-white/5 group-hover:bg-white/[0.05] transition-colors">
                <span class="text-[10px] font-black text-text-muted uppercase tracking-[0.25em]">Pedidos Activos</span>
                <span class="text-xs font-black text-white bg-amber/10 h-9 w-9 flex items-center justify-center rounded-xl border border-amber/20 shadow-lg shadow-amber/5">{{ building.active_orders_count || 0 }}</span>
              </div>

              <button
                type="button"
                class="w-full flex items-center justify-center gap-3 py-4 rounded-2xl bg-amber hover:bg-amber/90 text-navy-deep text-sm font-black uppercase tracking-widest transition-all shadow-lg shadow-amber/20 hover:shadow-amber/40 hover:-translate-y-1 active:translate-y-0"
                :disabled="ordersStore.isCreatingOrder"
                @click="createOrder(building.id)"
              >
                Iniciar Solicitud
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>
          </div>
        </article>
      </div>

      <div v-else class="bg-white/5 rounded-[2rem] border-2 border-dashed border-white/10 p-16 text-center">
        <div class="w-20 h-20 bg-white/5 rounded-3xl flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-white/20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h3 class="text-xl font-black text-white mb-2">Centro de Operaciones Vacio</h3>
        <p class="text-text-muted max-w-sm mx-auto font-medium">No tienes edificios asignados bajo tu administracion. Contacta con el area de compras central.</p>
      </div>
    </section>

    <div class="card overflow-hidden !p-0 border-white/5 shadow-2xl">
      <div class="p-10 border-b border-white/5 flex items-center justify-between bg-white/[0.01]">
        <div class="space-y-1">
          <h3 class="text-xl font-black text-white tracking-tight uppercase">Historial Operativo</h3>
          <p class="text-[10px] font-bold text-text-muted uppercase tracking-[0.3em]">Auditoria de despachos y llegadas</p>
        </div>
        <RouterLink :to="{ name: 'ordersBuildings' }" class="btn btn-outline !px-8 !py-3 hover:bg-amber hover:text-navy-deep transition-all !rounded-xl !text-[10px] !font-black !tracking-widest uppercase shadow-xl">
          Ver todo
        </RouterLink>
      </div>

      <div v-if="dashboard.historial_pedidos?.length" class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="bg-white/[0.03] border-y border-white/5">
            <tr>
              <th class="px-8 py-5 text-[10px] font-black text-amber uppercase tracking-[0.3em]">Folio ID</th>
              <th class="px-8 py-5 text-[10px] font-black text-white/70 uppercase tracking-[0.3em]">Sede Destino</th>
              <th class="px-8 py-5 text-[10px] font-black text-white/70 uppercase tracking-[0.3em]">Fecha</th>
              <th class="px-8 py-5 text-[10px] font-black text-white/70 uppercase tracking-[0.3em]">Estado Logistico</th>
              <th class="px-8 py-5 text-[10px] font-black text-white/70 uppercase tracking-[0.3em] text-right">Detalles</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5">
            <tr v-for="order in dashboard.historial_pedidos" :key="order.id" class="group hover:bg-white/[0.02] transition-all">
              <td class="px-8 py-7">
                <span class="text-[14px] font-black text-white tracking-tight">#{{ order.id }}</span>
              </td>
              <td class="px-8 py-7">
                <p class="text-[15px] font-black text-white group-hover:text-amber transition-colors">{{ order.building?.name }}</p>
                <p class="text-[10px] text-text-muted font-bold mt-1.5 uppercase tracking-widest">{{ order.items?.length ?? 0 }} SKU solicitados</p>
              </td>
              <td class="px-8 py-7">
                <span class="text-[13px] font-bold text-text-secondary">{{ formatDate(order.created_at) }}</span>
              </td>
              <td class="px-8 py-7">
                <span class="inline-flex items-center px-4 py-2.5 rounded-xl text-[9px] font-black uppercase tracking-widest border shadow-sm" :class="statusClass(order.status)">
                  {{ statusLabel(order.status) }}
                </span>
              </td>
              <td class="px-8 py-7 text-right">
                <RouterLink
                  :to="{ name: 'ordersOrderDetail', params: { orderId: order.id } }"
                  class="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-white/[0.05] border border-white/10 text-white hover:bg-amber hover:text-navy-deep hover:border-amber hover:scale-110 transition-all shadow-xl group/btn"
                >
                  <svg class="w-5 h-5 transition-transform group-hover/btn:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="p-12 text-center">
        <p class="text-[13px] font-bold text-slate-400 italic">No hay actividad reciente en tu historial.</p>
      </div>
    </div>
  </div>

  <div v-else class="max-w-[1320px] mx-auto px-5 py-12 md:px-8 xl:px-10">
    <div class="card border border-white/10 text-center space-y-4">
      <p class="text-sm font-black uppercase tracking-[0.2em] text-white">Sin datos disponibles</p>
      <p class="text-text-secondary">No se pudo cargar el dashboard administrativo en este momento.</p>
      <button type="button" class="btn btn-primary mx-auto" @click="reloadDashboard">
        Reintentar carga
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"

import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import { useAuthStore } from "@/stores/authStore"
import { useDashboardStore } from "@/stores/dashboardStore"
import { useOrdersStore } from "@/stores/ordersStore"
import { useUiStore } from "@/stores/uiStore"
import { assetUrl, defaultBuildingUrl, formatDate, statusClass, statusLabel, titleCase } from "@/utils/formatters"

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()
const ordersStore = useOrdersStore()
const uiStore = useUiStore()
const router = useRouter()
const apiStatus = ref("...")

const dashboard = computed(() => dashboardStore.adminDashboard)
const submissionDeadline = computed(() => dashboard.value?.submission_deadline ?? null)
const displayName = computed(() => titleCase(authStore.user?.name || authStore.user?.username || "Usuario"))
const metrics = computed(() => [
  {
    label: "Sedes Activas",
    value: dashboard.value?.buildings?.length ?? 0,
    valueClass: "text-amber",
    cardClass: "hover:border-amber/20",
  },
  {
    label: "Pendientes",
    value: dashboard.value?.pedidos_activos ?? 0,
    valueClass: "text-white",
    cardClass: "hover:border-white/10",
  },
  {
    label: "En Transito",
    value: dashboard.value?.pedidos_en_transito ?? 0,
    valueClass: "text-rose-400",
    cardClass: "hover:border-rose-500/20 col-span-2 lg:col-span-1",
    pulse: (dashboard.value?.pedidos_en_transito ?? 0) > 0,
    pulseClass: "bg-rose-400",
    dotClass: "bg-rose-500",
  },
  {
    label: "Catalyst API",
    value: apiStatus.value,
    valueClass: apiStatus.value === "ON" ? "text-emerald-400" : apiStatus.value === "OFF" ? "text-rose-400" : "text-slate-500",
    cardClass: apiStatus.value === "ON" ? "hover:border-emerald-500/20" : apiStatus.value === "OFF" ? "hover:border-rose-500/20" : "",
    pulse: true,
    pulseClass: apiStatus.value === "ON" ? "bg-emerald-400" : apiStatus.value === "OFF" ? "bg-rose-400" : "bg-slate-400",
    dotClass: apiStatus.value === "ON" ? "bg-emerald-500" : apiStatus.value === "OFF" ? "bg-rose-500" : "bg-slate-500",
  },
])

onMounted(async () => {
  await reloadDashboard()
})

async function reloadDashboard() {
  await dashboardStore.fetchAdminDashboard()
  await checkApiStatus()
}

function buildingImage(building) {
  return assetUrl(building.imagen_frontis, defaultBuildingUrl)
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

function deadlineRelativeCopy(value, state) {
  if (!value) {
    return ""
  }

  const diffMs = new Date(value).getTime() - Date.now()
  const diffHours = Math.round(Math.abs(diffMs) / 36e5)

  if (state === "overdue") {
    if (diffHours < 1) {
      return "El cierre ya expiro."
    }
    return `El cierre expiro hace ${diffHours} hora${diffHours === 1 ? "" : "s"}.`
  }

  if (diffHours < 1) {
    return "El cierre ocurre en menos de una hora."
  }

  return `El cierre ocurre en ${diffHours} hora${diffHours === 1 ? "" : "s"}.`
}

async function createOrder(buildingId) {
  try {
    const order = await ordersStore.createOrder(buildingId)
    uiStore.success(`Se creo la orden #${order.id}.`, "Solicitud iniciada")
    router.push({ name: "ordersOrderDetail", params: { orderId: order.id } })
  } catch (error) {
    uiStore.error(error.message, "No se pudo iniciar la solicitud")
  }
}

async function receiveOrder(orderId) {
  try {
    await ordersStore.updateOrderStatus(orderId, "receive")
    await dashboardStore.fetchAdminDashboard()
    uiStore.success(`Se confirmo la recepcion de la orden #${orderId}.`, "Recepcion registrada")
  } catch (error) {
    uiStore.error(error.message, "No se pudo confirmar la recepcion")
  }
}

async function checkApiStatus() {
  try {
    const baseUrl = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/api\/v1\/?$/, "")
    const response = await fetch(`${baseUrl}/health`)
    apiStatus.value = response.ok ? "ON" : "OFF"
  } catch (error) {
    apiStatus.value = "OFF"
  }
}
</script>
