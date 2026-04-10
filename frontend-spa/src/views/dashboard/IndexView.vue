<template>
  <div v-if="dashboardStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
    {{ dashboardStore.error }}
  </div>

  <DashboardSkeleton v-else-if="dashboardStore.isLoading && !dashboard" />

  <div v-else-if="dashboard" class="space-y-12 pb-24">
    <div class="flex flex-col xl:flex-row xl:items-end justify-between gap-10 border-b border-white/5 pb-10">
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-6 bg-amber rounded-full shadow-[0_0_12px_rgba(242,173,61,0.4)]"></div>
          <span class="eyebrow tracking-[0.4em] !text-amber text-[10px]">Logistica Central</span>
        </div>
        <h1 class="text-5xl font-black tracking-tighter italic leading-none text-white">
          Panel de <span class="text-amber">Control</span>
        </h1>
        <p class="text-text-muted font-medium text-sm md:text-base max-w-xl">
          Estado logistico en tiempo real para <span class="text-white font-bold capitalize">{{ displayName }}</span>.
        </p>
      </div>

      <div class="flex items-center gap-5 bg-white/[0.03] border border-white/5 backdrop-blur-3xl rounded-[2rem] px-8 py-5 shadow-2xl self-start xl:self-auto">
        <div class="text-right">
          <p class="label-premium !mb-0">Fecha Operativa</p>
          <p class="text-white font-black text-sm tracking-widest tabular-nums uppercase">{{ formatDate(new Date()) }}</p>
        </div>
        <div class="w-[1px] h-10 bg-white/10"></div>
        <div class="w-10 h-10 bg-amber/10 rounded-xl flex items-center justify-center border border-amber/20 shadow-lg shadow-amber/10">
          <svg class="w-5 h-5 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
      </div>
    </div>

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
              <span class="text-xl font-bold text-amber/40 tabular-nums">{{ metric.prefix }}</span>
              <p class="text-5xl font-black text-white tracking-tighter">{{ metric.value }}</p>
            </div>
            <p v-else class="text-5xl font-black text-white tracking-tighter">{{ metric.value }}</p>
            <div class="flex items-center gap-2" :class="metric.dot ? '' : 'pt-1'">
              <span v-if="metric.dot" class="w-1.5 h-1.5 rounded-full bg-amber animate-pulse"></span>
              <span class="eyebrow !text-text-muted/60">{{ metric.label }}</span>
            </div>
          </div>
        </div>
      </article>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <article class="card !p-0 overflow-hidden group">
        <div class="px-8 py-6 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-amber/10 rounded-xl flex items-center justify-center border border-amber/20 shadow-lg shadow-amber/5">
              <svg class="w-5 h-5 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <h3 class="text-base font-bold text-white">Pedidos por Edificio</h3>
              <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-0.5">Distribucion de Solicitudes</p>
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
        <div class="px-8 py-6 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-indigo-500/10 rounded-xl flex items-center justify-center border border-indigo-500/20 shadow-lg shadow-indigo-500/5">
              <svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
              </svg>
            </div>
            <div>
              <h3 class="text-base font-bold text-white">Top 5 Movimientos</h3>
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

    <div class="grid grid-cols-1 lg:grid-cols-5 gap-8">
      <article class="lg:col-span-3 card !p-0 overflow-hidden flex flex-col">
        <div class="px-8 py-6 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-emerald-500/10 rounded-xl flex items-center justify-center border border-emerald-500/20 shadow-lg shadow-emerald-500/5">
              <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
            </div>
            <div>
              <h3 class="text-base font-bold text-white">Inversion por Sede</h3>
              <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-0.5">Distribucion de Costos Totales</p>
            </div>
          </div>
        </div>

        <div class="overflow-x-auto flex-grow">
          <table class="w-full text-left">
            <thead class="bg-white/[0.03] text-text-muted font-bold text-[10px] uppercase tracking-[0.2em]">
              <tr>
                <th class="px-8 py-4">Edificio</th>
                <th class="px-8 py-4 text-right">Inversion Total</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr v-for="item in dashboard.costos_por_edificio" :key="item.building_name" class="group hover:bg-white/[0.02] transition-all duration-300">
                <td class="px-8 py-5">
                  <div class="flex items-center gap-3">
                    <div class="w-2 h-2 rounded-full bg-emerald-500/40"></div>
                    <span class="text-sm font-bold text-white group-hover:text-amber transition-colors">{{ item.building_name }}</span>
                  </div>
                </td>
                <td class="px-8 py-5 text-right font-black text-emerald-400 tabular-nums">
                  <span class="text-[10px] opacity-40 mr-1">S/</span>{{ formatDecimal(item.gasto_total) }}
                </td>
              </tr>
              <tr v-if="!dashboard.costos_por_edificio?.length">
                <td colspan="2" class="px-8 py-12 text-center text-text-muted text-xs font-medium italic opacity-50">No hay registros operativos.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>

      <article class="lg:col-span-2 flex flex-col gap-6">
        <div class="card !p-0 overflow-hidden border-rose-500/10 h-full flex flex-col">
          <div class="px-8 py-6 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 bg-rose-500/10 rounded-xl flex items-center justify-center border border-rose-500/20 shadow-lg shadow-rose-500/5">
                <svg class="w-5 h-5 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div>
                <h3 class="text-base font-bold text-white">Alertas Criticas</h3>
                <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-0.5">Reposicion Inmediata</p>
              </div>
            </div>
          </div>

          <div class="flex-grow overflow-y-auto max-h-[500px] custom-scrollbar">
            <template v-if="dashboard.alertas_stock?.length">
              <div class="px-6 py-3 bg-white/[0.02] border-b border-white/5">
                <span class="text-[9px] font-black text-white/40 uppercase tracking-[0.25em]">Almacen Central</span>
              </div>
              <div class="divide-y divide-white/5">
                <div v-for="product in dashboard.alertas_stock" :key="product.id" class="px-6 py-4 flex items-center gap-4 hover:bg-white/[0.03] transition-all group">
                  <div class="w-12 h-12 rounded-xl bg-white/5 border border-white/10 overflow-hidden flex-shrink-0">
                    <img :src="product.imagen_url || defaultProductUrl" alt="" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" />
                  </div>
                  <div class="flex-grow min-w-0">
                    <p class="text-[13px] font-extrabold text-white truncate group-hover:text-amber transition-colors">{{ product.name }}</p>
                    <p class="text-[10px] font-bold text-text-muted uppercase tracking-wider">Stock: <span class="text-rose-400">{{ product.stock_actual }}</span> / Min: {{ product.stock_minimo }}</p>
                  </div>
                  <div class="px-2 py-1 rounded-md bg-rose-500/10 border border-rose-500/20">
                    <span class="text-[10px] font-black text-rose-400 uppercase">Critico</span>
                  </div>
                </div>
              </div>
            </template>
            <div v-else class="flex flex-col items-center justify-center p-12 text-center h-full">
              <div class="w-16 h-16 bg-emerald-500/10 rounded-full flex items-center justify-center mb-4 border border-emerald-500/20">
                <svg class="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h4 class="text-white font-bold mb-1">Operaciones Estables</h4>
              <p class="text-xs text-text-muted max-w-[200px]">No se detectan quiebres de stock en la red.</p>
            </div>
          </div>
        </div>
      </article>
    </div>

    <div class="mt-12 space-y-6">
      <div class="flex items-center gap-4">
        <h3 class="label-premium !mb-0 whitespace-nowrap">Acceso Rapido al Sistema</h3>
        <div class="h-px bg-white/5 flex-grow"></div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <RouterLink
          v-for="item in navItems"
          :key="item.label"
          :to="item.to"
          class="card !p-6 flex flex-col items-center justify-center gap-3 group hover:border-amber/40 hover:bg-amber/5 transition-all duration-300"
        >
          <div class="relative">
            <div class="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center group-hover:scale-110 group-hover:bg-amber group-hover:text-navy transition-all duration-500 shadow-lg">
              <svg class="w-6 h-6 text-white group-hover:text-navy" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" :d="item.iconPath" />
              </svg>
            </div>
            <span v-if="item.count" class="absolute -top-1 -right-1 w-5 h-5 bg-rose-500 text-white text-[10px] font-black rounded-full flex items-center justify-center border-2 border-navy-deep shadow-lg">
              {{ item.count }}
            </span>
          </div>
          <p class="text-[11px] font-black text-text-muted uppercase tracking-[0.2em] group-hover:text-white transition-colors text-center">{{ item.label }}</p>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Chart } from "chart.js/auto"
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue"

import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import { useAuthStore } from "@/stores/authStore"
import { useDashboardStore } from "@/stores/dashboardStore"
import { defaultProductUrl, formatDate, logoUrl } from "@/utils/formatters"

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()
const barChartRef = ref(null)
const doughnutChartRef = ref(null)
let barChart = null
let doughnutChart = null

const dashboard = computed(() => dashboardStore.superadminDashboard)
const displayName = computed(() => authStore.user?.name || authStore.user?.username || "Usuario")
const metrics = computed(() => [
  {
    label: "Pedidos en Espera",
    value: dashboard.value?.total_pedidos_pendientes ?? 0,
    iconWrapClass: "bg-amber/5 group-hover:bg-amber/10 border-amber/10 group-hover:border-amber/30",
    iconClass: "text-amber",
    iconPath: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2",
    dot: true,
    cardClass: "hover:shadow-[0_30px_60px_-15px_rgba(242,173,61,0.1)]",
  },
  {
    label: "Edificios Operativos",
    value: dashboard.value?.total_edificios_activos ?? 0,
    iconWrapClass: "bg-white/5 group-hover:bg-white/10 border-white/5 group-hover:border-white/20",
    iconClass: "text-white/50 group-hover:text-white/80 transition-colors",
    iconPath: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4",
    cardClass: "hover:shadow-[0_30px_60px_-15px_rgba(255,255,255,0.05)]",
  },
  {
    label: "Flujo Mensual",
    value: formatDecimal(dashboard.value?.costo_despachado_mes ?? 0),
    prefix: "S/",
    iconWrapClass: "bg-emerald-500/5 group-hover:bg-emerald-500/10 border-emerald-500/10 group-hover:border-emerald-500/30",
    iconClass: "text-emerald-400",
    iconPath: "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
    cardClass: "border-emerald-500/10 hover:shadow-[0_30px_60px_-15px_rgba(16,185,129,0.08)]",
  },
  {
    label: "Catalogo de Items",
    value: dashboard.value?.total_productos ?? 0,
    iconWrapClass: "bg-white/5 group-hover:bg-white/10 border-white/5 group-hover:border-white/20",
    iconClass: "text-white/50 group-hover:text-white/80 transition-colors",
    iconPath: "M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4",
    cardClass: "hover:shadow-[0_30px_60px_-15px_rgba(255,255,255,0.05)]",
  },
])

const navItems = computed(() => [
  { to: { name: "dispatchPending" }, iconPath: "M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4", label: "Despacho", count: dashboard.value?.total_pedidos_pendientes ?? 0 },
  { to: { name: "catalogUploadCsv" }, iconPath: "M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12", label: "Catalogo CSV" },
  { to: { name: "catalogAssignBuilding" }, iconPath: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4", label: "Asignar Edif." },
  { to: { name: "catalogBuildingCreate" }, iconPath: "M12 4v16m8-8H4", label: "Nuevo Edificio" },
  { to: { name: "catalogAdminCreate" }, iconPath: "M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0z", label: "Nuevo Admin" },
  { to: { name: "superadminControl" }, iconPath: "M12 8a4 4 0 00-4 4v3a2 2 0 002 2h4a2 2 0 002-2v-3a4 4 0 00-4-4zm0 0V5m0 14v-2m7-5h-2M7 12H5", label: "Control SA" },
])

onMounted(() => {
  dashboardStore.fetchSuperadminDashboard()
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

onBeforeUnmount(() => {
  destroyCharts()
})

function formatDecimal(value) {
  return Number(value ?? 0).toFixed(2)
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
  gradient.addColorStop(1, "rgba(242, 173, 61, 0.1)")

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
          backgroundColor: "#0B1F33",
          titleColor: "#F2AD3D",
          bodyColor: "#ffffff",
          borderColor: "rgba(255,255,255,0.1)",
          borderWidth: 1,
          padding: 16,
          cornerRadius: 16,
          displayColors: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1, color: "rgba(255,255,255,0.3)" },
          grid: { color: "rgba(255,255,255,0.03)", drawBorder: false },
        },
        x: {
          ticks: { color: "rgba(255,255,255,0.6)" },
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
          backgroundColor: ["#F2AD3D", "#06286F", "#4F46E5", "#10B981", "#6B7280"],
          borderColor: "#041120",
          borderWidth: 8,
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
            usePointStyle: true,
            pointStyleWidth: 12,
            color: "rgba(255,255,255,0.5)",
          },
        },
        tooltip: {
          backgroundColor: "#0B1F33",
          titleColor: "#F2AD3D",
          bodyColor: "#ffffff",
          borderColor: "rgba(255,255,255,0.1)",
          borderWidth: 1,
          padding: 16,
          cornerRadius: 16,
        },
      },
    },
  })
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(242, 173, 61, 0.3);
}
</style>
