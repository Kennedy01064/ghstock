<template>
  <div class="space-y-12 pb-32 max-w-5xl mx-auto">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-8 border-b border-slate-200 pb-8">
      <div class="space-y-3">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-6 bg-amber rounded-full shadow-[0_0_12px_rgba(242,173,61,0.4)]" />
          <span class="eyebrow tracking-[0.4em] !text-slate-900 text-[10px]">Gestion de Activos</span>
        </div>
        <h1 data-testid="buildings-page-title" class="h2 !text-3xl !tracking-tight">Seleccion de Sede</h1>
        <p class="text-text-muted font-medium text-sm max-w-xl">
          Identifique la unidad inmobiliaria para iniciar el manifiesto de requerimientos y control de existencias.
        </p>
      </div>
      <div class="h-16 w-16 rounded-[2rem] bg-white border border-slate-200 flex items-center justify-center text-amber shadow-[inset_0_2px_4px_rgba(255,255,255,0.05)] shrink-0">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      </div>
    </div>

    <div v-if="buildingStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ buildingStore.error }}
    </div>

    <div v-if="buildingStore.isLoading && !buildings.length" class="card text-text-muted">
      Cargando sedes...
    </div>

    <div v-else-if="buildings.length" class="grid grid-cols-1 gap-8">
      <article
        v-for="building in buildings"
        :key="building.id"
        class="card !p-0 overflow-hidden border-slate-200 hover:border-amber/30 transition-all group/card shadow-[0_32px_64px_-12px_rgba(0,0,0,0.6)] backdrop-blur-3xl relative"
      >
        <div class="absolute inset-0 bg-gradient-to-r from-amber/5 to-transparent opacity-0 group-hover/card:opacity-100 transition-opacity duration-700" />

        <div class="flex flex-col lg:flex-row min-h-[220px] relative z-10">
          <div class="w-full lg:w-80 bg-slate-100 relative overflow-hidden shrink-0 border-b lg:border-b-0 lg:border-r border-slate-200">
            <img
              v-if="building.imageUrl"
              :src="building.imageUrl"
              :alt="building.name"
              class="w-full h-full object-cover group-hover/card:scale-110 transition-transform duration-1000 opacity-40 group-hover/card:opacity-80"
            >
            <div v-else class="w-full h-full flex items-center justify-center text-slate-900/[0.03]">
              <svg class="w-24 h-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>

            <div class="absolute top-4 left-4">
              <span class="px-3 py-1 transparent-blur-amber rounded-lg text-[9px] font-black tracking-widest uppercase border border-amber/30 text-amber shadow-lg shadow-amber/20">
                Activo Corporativo
              </span>
            </div>
          </div>

          <div class="flex-1 p-8 md:p-10 flex flex-col justify-between gap-8">
            <div class="space-y-4">
              <div class="flex items-start justify-between gap-6">
                <div class="space-y-2">
                  <h3 class="text-2xl font-black text-slate-900 uppercase tracking-tight group-hover/card:text-amber transition-colors leading-none">
                    {{ building.name }}
                  </h3>
                  <div class="flex items-center gap-2.5 text-text-muted">
                    <div class="w-5 h-5 flex items-center justify-center rounded-lg bg-slate-50 border border-slate-200">
                      <svg class="w-3 h-3 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </div>
                    <span class="text-xs font-bold tracking-wide">{{ building.address || "Ubicacion institucional seleccionada" }}</span>
                  </div>
                </div>

                <div
                  v-if="draftBuildingIds.has(building.id)"
                  class="flex items-center gap-2.5 px-4 py-2 rounded-2xl bg-amber/10 border border-amber/30 animate-pulse shadow-lg shadow-amber/10"
                >
                  <div class="w-2 h-2 rounded-full bg-amber shadow-[0_0_12px_rgba(242,173,61,0.8)]" />
                  <span class="text-[9px] font-black text-amber uppercase tracking-[0.2em]">Manifiesto en Curso</span>
                </div>
              </div>

              <div class="h-px w-12 bg-slate-50 group-hover/card:w-24 group-hover/card:bg-amber transition-all duration-700" />
            </div>

            <button
              type="button"
              class="btn btn-primary !rounded-2xl !py-4.5 px-12 self-start group/btn shadow-[0_20px_40px_-12px_rgba(242,173,61,0.25)] h-14"
              :disabled="ordersStore.isCreatingOrder"
              @click="startOrder(building.id)"
            >
              <span class="tracking-widest font-black text-xs">ACCEDER A LA SEDE</span>
              <svg class="w-5 h-5 transition-transform group-hover/btn:translate-x-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
          </div>
        </div>
      </article>
    </div>

    <div v-else class="card flex flex-col items-center justify-center py-32 border-dashed border-slate-200 bg-slate-50 rounded-[3rem]">
      <div class="w-24 h-24 rounded-[2.5rem] bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-900/5 mb-8 shadow-inner">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      </div>
      <h3 class="text-xl font-black text-slate-900 uppercase tracking-[0.3em]">Acceso Restringido</h3>
      <p class="text-text-muted text-sm font-medium mt-3 max-w-sm text-center italic leading-relaxed opacity-60">
        No se han detectado sedes vinculadas a su credencial corporativa. Por favor, solicite su alta en la Direccion General.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import { useBuildingStore } from "@/stores/buildingStore"
import { useOrdersStore } from "@/stores/ordersStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizeBuilding, normalizeOrder } from "@/utils/normalizers"

const router = useRouter()
const buildingStore = useBuildingStore()
const ordersStore = useOrdersStore()
const uiStore = useUiStore()

const buildings = computed(() => buildingStore.buildings.map(normalizeBuilding))
const draftBuildingIds = computed(() => {
  const ids = new Set()

  ordersStore.orders
    .map(normalizeOrder)
    .filter((order) => order.status === "draft")
    .forEach((order) => {
      ids.add(order.building_id)
    })

  return ids
})

async function startOrder(buildingId) {
  if (ordersStore.isCreatingOrder) return
  try {
    const order = await ordersStore.createOrder(buildingId)
    await router.push({ name: "ordersOrderDetail", params: { orderId: order.id } })
  } catch (error) {
    uiStore.error(error.message, "No se pudo abrir la sede")
  }
}

onMounted(() => {
  Promise.all([buildingStore.fetchBuildings(), ordersStore.fetchOrders({ status: "draft" })])
})
</script>
