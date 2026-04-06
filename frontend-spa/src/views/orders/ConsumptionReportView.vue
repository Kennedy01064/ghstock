<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-8 py-8 space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
      <div class="space-y-2">
        <span class="eyebrow !text-amber/60">Inventario Local</span>
        <h1 class="text-3xl md:text-4xl font-black text-white tracking-tight uppercase">Reporte de Consumo</h1>
        <p class="text-text-muted text-sm">Historico de productos consumidos por sede.</p>
      </div>
    </div>

    <form class="card !p-5 border-white/5 flex flex-col sm:flex-row gap-4 items-end" @submit.prevent="applyFilters">
      <div class="flex-1">
        <label class="label-premium">Filtrar por Sede</label>
        <select v-model="selectedBuildingId" class="select-field !py-3">
          <option value="">Todas las sedes</option>
          <option v-for="building in buildings" :key="building.id" :value="String(building.id)">
            {{ building.name }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary !py-3 !px-5 !min-h-0 text-[11px] shrink-0">Aplicar</button>
      <button
        v-if="selectedBuildingId"
        type="button"
        class="btn btn-secondary !py-3 !px-5 !min-h-0 text-[11px] shrink-0"
        @click="clearFilters"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
        </svg>
        Limpiar
      </button>
    </form>

    <div v-if="inventoryStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ inventoryStore.error }}
    </div>

    <div v-if="rows.length" class="card !p-0 overflow-hidden border-white/5">
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="bg-white/[0.03] border-b border-white/5">
            <tr>
              <th class="px-6 py-4 text-[10px] font-black text-amber uppercase tracking-[0.3em]">Producto</th>
              <th class="px-6 py-4 text-[10px] font-black text-white/60 uppercase tracking-[0.3em] hidden sm:table-cell">Sede</th>
              <th class="px-6 py-4 text-[10px] font-black text-white/60 uppercase tracking-[0.3em] text-right">Total Consumido</th>
              <th class="px-6 py-4 text-[10px] font-black text-white/60 uppercase tracking-[0.3em] text-right hidden md:table-cell">Eventos</th>
              <th class="px-6 py-4 text-[10px] font-black text-white/60 uppercase tracking-[0.3em] hidden lg:table-cell">Ultimo Reporte</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/[0.04]">
            <tr v-for="row in rows" :key="row.key" class="hover:bg-white/[0.02] transition-colors group">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3 min-w-0">
                  <img
                    :src="row.imageUrl"
                    :alt="row.productName"
                    class="w-9 h-9 rounded-xl object-contain bg-white/5 p-1.5 border border-white/10 shrink-0"
                  >
                  <div class="min-w-0">
                    <p class="text-sm font-black text-white group-hover:text-amber transition-colors truncate">{{ row.productName }}</p>
                    <p class="text-[10px] text-text-muted sm:hidden">{{ row.buildingName }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-[13px] text-text-muted font-bold hidden sm:table-cell">{{ row.buildingName }}</td>
              <td class="px-6 py-4 text-right">
                <span class="text-base font-black text-white">{{ row.totalConsumed }}</span>
                <span class="text-[10px] text-text-muted ml-1">{{ row.unit }}</span>
              </td>
              <td class="px-6 py-4 text-right hidden md:table-cell">
                <span class="text-[12px] font-bold text-text-muted">{{ row.events }}</span>
              </td>
              <td class="px-6 py-4 text-[12px] text-text-muted hidden lg:table-cell">
                {{ row.lastReported }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else class="card border-dashed border-white/10 bg-white/[0.01] py-20 text-center">
      <div class="w-16 h-16 bg-white/5 rounded-3xl flex items-center justify-center mx-auto mb-5">
        <svg class="w-8 h-8 text-white/20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      </div>
      <h3 class="text-lg font-black text-white mb-2">Sin datos de consumo</h3>
      <p class="text-text-muted text-sm max-w-xs mx-auto">Registra consumos desde la seccion Inventario Local para ver reportes aqui.</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"

import { useCatalogStore } from "@/stores/catalogStore"
import { useInventoryStore } from "@/stores/inventoryStore"
import { assetUrl, defaultProductUrl, formatDate } from "@/utils/formatters"
import { normalizeBuilding } from "@/utils/normalizers"

const catalogStore = useCatalogStore()
const inventoryStore = useInventoryStore()
const selectedBuildingId = ref("")

const buildings = computed(() => catalogStore.buildings.map(normalizeBuilding))
const rows = computed(() =>
  inventoryStore.consumptionRows.map((row, index) => ({
    key: `${row.building_name}-${row.product_name}-${index}`,
    buildingName: row.building_name,
    productName: row.product_name,
    unit: row.unit,
    imageUrl: assetUrl(row.imagen_url, defaultProductUrl),
    totalConsumed: row.total_consumed,
    events: row.events,
    lastReported: row.last_reported ? formatDate(row.last_reported) : "-",
  })),
)

function applyFilters() {
  inventoryStore.fetchConsumptionReport(selectedBuildingId.value ? Number(selectedBuildingId.value) : undefined)
}

function clearFilters() {
  selectedBuildingId.value = ""
  inventoryStore.fetchConsumptionReport()
}

onMounted(() => {
  Promise.all([catalogStore.fetchBuildings(), inventoryStore.fetchConsumptionReport()])
})
</script>
