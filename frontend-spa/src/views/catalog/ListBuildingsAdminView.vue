<template>
  <div class="space-y-8 pb-32">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <span class="eyebrow tracking-[0.3em]">Gestion de Infraestructura</span>
        <h1 class="text-4xl font-black tracking-tight text-slate-900">Listado de Sedes</h1>
        <p class="text-text-muted font-medium">Control centralizado de edificios, capacidades y administradores locales.</p>
      </div>

      <div class="flex flex-col sm:flex-row items-center gap-4 w-full md:w-auto">
        <div class="relative w-full sm:w-80 group">
          <input v-model="query" type="text" placeholder="Filtrar por nombre o direccion..." class="input-field !pl-12" />
          <svg class="w-5 h-5 text-text-muted absolute left-4 top-1/2 -translate-y-1/2 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        <RouterLink :to="{ name: 'catalogBuildingCreate' }" class="btn btn-primary w-full sm:w-auto shadow-2xl shadow-amber/10">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
          </svg>
          Registrar Sede
        </RouterLink>
      </div>
    </div>

    <div v-if="buildingStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ buildingStore.error }}
    </div>

    <div class="card !p-0 overflow-hidden border-slate-200 shadow-2xl shadow-slate-200/50">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50">
              <th class="px-8 py-5 eyebrow !text-text-muted text-[10px]">Identificacion</th>
              <th class="px-6 py-5 eyebrow !text-text-muted text-[10px] text-center">Unidades</th>
              <th class="px-6 py-5 eyebrow !text-text-muted text-[10px] text-center">Gestion Asignada</th>
              <th class="px-8 py-5 eyebrow !text-text-muted text-[10px] text-right">Controles</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="building in filteredBuildings" :key="building.id" class="group hover:bg-slate-50 transition-colors">
              <td class="px-8 py-6">
                <div class="flex items-center gap-5">
                  <div v-if="building.imageUrl" class="w-14 h-14 rounded-2xl overflow-hidden shrink-0 shadow-lg border border-slate-200">
                    <img :src="building.imageUrl" alt="Frontis" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                  </div>
                  <div v-else class="w-14 h-14 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-text-muted shrink-0 shadow-inner group-hover:text-amber transition-colors">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                  <div class="space-y-1 min-w-0">
                    <p class="font-black text-slate-900 text-sm uppercase tracking-wider group-hover:text-amber transition-colors">{{ building.name }}</p>
                    <div class="flex items-center gap-2 text-text-muted">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      <span class="text-[11px] font-bold truncate max-w-[240px]" :title="building.address || 'Sin direccion'">
                        {{ building.address || "Ubicacion no especificada" }}
                      </span>
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-6 text-center">
                <span class="inline-flex items-center justify-center min-w-[32px] h-8 rounded-lg bg-slate-100 border border-slate-200 text-[13px] font-black text-amber">
                  {{ building.departments_count ?? 0 }}
                </span>
              </td>
              <td class="px-6 py-6 text-center">
                <div v-if="building.admin" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber/5 border border-amber/20">
                  <div class="w-1.5 h-1.5 rounded-full bg-amber shadow-[0_0_8px_rgba(242,173,61,0.5)]"></div>
                  <span class="text-[10px] font-black text-amber uppercase tracking-widest">
                    {{ building.admin.name || building.admin.username }}
                  </span>
                </div>
                <span v-else class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] italic">Desocupado</span>
              </td>
              <td class="px-8 py-6 text-right">
                <div class="flex items-center justify-end gap-3">
                  <RouterLink
                    :to="{ name: 'catalogBuildingEdit', params: { buildingId: building.id } }"
                    class="h-10 w-10 flex items-center justify-center rounded-xl bg-slate-50 border border-slate-200 text-text-muted hover:border-amber/40 hover:text-amber hover:bg-amber/5 transition-all group/edit"
                    title="Editar Sede"
                  >
                    <svg class="w-5 h-5 transition-transform group-hover/edit:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </RouterLink>
                  <button
                    type="button"
                    class="h-10 w-10 flex items-center justify-center rounded-xl bg-slate-50 border border-slate-200 text-red-400/60 hover:border-red-500/40 hover:text-red-500 hover:bg-red-500/5 transition-all group/del"
                    title="Eliminar Sede"
                    @click="pendingBuildingId = building.id"
                  >
                    <svg class="w-5 h-5 transition-transform group-hover/del:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!buildingStore.isLoading && !filteredBuildings.length">
              <td colspan="4" class="px-8 py-20 text-center">
                <div class="flex flex-col items-center gap-4">
                  <div class="w-16 h-16 rounded-full bg-slate-50 flex items-center justify-center text-slate-900/10">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                  <div class="space-y-1">
                    <p class="text-slate-900 font-black uppercase tracking-widest text-sm">
                      {{ query.trim() ? "Sin coincidencias" : "Sin Sedes Registradas" }}
                    </p>
                    <p class="text-text-muted text-xs font-medium">
                      {{ query.trim() ? "Ajusta el filtro de busqueda para ver mas resultados." : "Inicie la configuracion agregando su primer edificio corporativo." }}
                    </p>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <AppModal
      :open="Boolean(pendingBuilding)"
      eyebrow="Gestion de infraestructura"
      title="Eliminar sede"
      :description="pendingBuilding ? `Confirmar desactivacion de ${pendingBuilding.name}. Si tiene pedidos asociados, el backend bloqueara la operacion.` : ''"
      confirm-label="Eliminar"
      confirm-variant="danger"
      :loading="buildingStore.isDeleting"
      @close="pendingBuildingId = null"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"

import AppModal from "@/components/ui/AppModal.vue"
import { useBuildingStore } from "@/stores/buildingStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizeBuilding } from "@/utils/normalizers"

const buildingStore = useBuildingStore()
const uiStore = useUiStore()
const query = ref("")
const pendingBuildingId = ref(null)

const buildings = computed(() => buildingStore.buildings.map(normalizeBuilding))
const filteredBuildings = computed(() => {
  const term = query.value.trim().toLowerCase()

  if (!term) {
    return buildings.value
  }

  return buildings.value.filter((building) =>
    `${building.name} ${building.address ?? ""} ${building.admin?.name ?? ""} ${building.admin?.username ?? ""}`.toLowerCase().includes(term),
  )
})
const pendingBuilding = computed(() => buildings.value.find((building) => building.id === pendingBuildingId.value) ?? null)

onMounted(() => {
  buildingStore.fetchBuildings()
})

async function confirmDelete() {
  if (!pendingBuilding.value) {
    return
  }

  try {
    await buildingStore.deleteBuilding(pendingBuilding.value.id)
    uiStore.success(`Se elimino ${pendingBuilding.value.name}.`, "Sede eliminada")
    pendingBuildingId.value = null
  } catch (error) {
    uiStore.error(error.message, "No se pudo eliminar la sede")
  }
}
</script>
