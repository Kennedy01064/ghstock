<template>
  <div class="space-y-10">
    <PageHeader
      eyebrow="Asignacion operativa"
      title="Asignar edificios"
      description="Relaciona administradores con edificios desde una interfaz reactiva y sin recargas."
      :meta="{ label: 'Cobertura', value: `${filteredBuildings.length} edificios` }"
    />

    <div v-if="buildingStore.error || userStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ buildingStore.error || userStore.error }}
    </div>

    <div class="grid gap-8 xl:grid-cols-[320px_minmax(0,1fr)]">
      <div class="card space-y-5">
        <div>
          <label class="label-premium">Administrador</label>
          <select v-model="selectedAdminId" class="select-field">
            <option v-for="admin in admins" :key="admin.id" :value="admin.id">{{ admin.name }} - {{ admin.role }}</option>
          </select>
        </div>
        <div>
          <label class="label-premium">Buscar edificio</label>
          <input v-model="query" type="search" placeholder="Filtrar por nombre o direccion" class="input-field" />
        </div>
        <button type="button" class="btn btn-primary w-full" :disabled="!selectedAdminId || !selectedBuildingIds.length || buildingStore.isAssigning" @click="handleAssign">
          {{ buildingStore.isAssigning ? "Guardando..." : "Guardar asignacion" }}
        </button>
      </div>

      <div v-if="(buildingStore.isLoading || userStore.isLoading) && !buildings.length" class="card text-text-secondary">
        Cargando edificios...
      </div>

      <div v-else class="grid gap-5 md:grid-cols-2">
        <article v-for="building in filteredBuildings" :key="building.id" class="card !p-0 overflow-hidden">
          <img :src="building.imageUrl" :alt="building.name" class="h-44 w-full object-cover border-b border-white/[0.07]" />
          <div class="p-6 space-y-4">
            <div class="flex items-start justify-between gap-4">
              <div>
                <h3 class="text-lg font-black text-white">{{ building.name }}</h3>
                <p class="text-[11px] uppercase tracking-[0.18em] text-text-muted mt-2">{{ building.address }}</p>
              </div>
              <input v-model="selectedBuildingIds" type="checkbox" :value="building.id" class="h-4 w-4 accent-amber" />
            </div>
            <div class="text-sm text-text-secondary space-y-2">
              <p>Administrador actual: <span class="text-white font-bold">{{ building.adminName }}</span></p>
              <p>Unidades: <span class="text-white font-bold">{{ building.units }}</span></p>
            </div>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"

import PageHeader from "@/components/page/PageHeader.vue"
import { useBuildingStore } from "@/stores/buildingStore"
import { useUserStore } from "@/stores/userStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizeBuilding, normalizeUser } from "@/utils/normalizers"

const buildingStore = useBuildingStore()
const userStore = useUserStore()
const uiStore = useUiStore()
const selectedAdminId = ref(null)
const selectedBuildingIds = ref([])
const query = ref("")

const admins = computed(() =>
  userStore.users.map(normalizeUser).filter((admin) => admin.role === "admin" && admin.is_active !== false),
)
const buildings = computed(() => buildingStore.buildings.map(normalizeBuilding))
const filteredBuildings = computed(() => {
  if (!query.value.trim()) {
    return buildings.value
  }

  const term = query.value.toLowerCase()
  return buildings.value.filter((building) =>
    `${building.name} ${building.address} ${building.adminName}`.toLowerCase().includes(term),
  )
})

async function handleAssign() {
  if (buildingStore.isAssigning) return

  try {
    const result = await buildingStore.assignToAdmin(selectedAdminId.value, selectedBuildingIds.value)
    uiStore.success(result.message, "Asignacion actualizada")
    selectedBuildingIds.value = []
    await Promise.all([buildingStore.fetchBuildings(), userStore.fetchUsers("admin", { includeInactive: false })])
  } catch (error) {
    uiStore.error(error.message, "No se pudo asignar edificios")
  }
}

onMounted(async () => {
  await Promise.all([userStore.fetchUsers("admin", { includeInactive: false }), buildingStore.fetchBuildings()])
  selectedAdminId.value = admins.value[0]?.id ?? null
})
</script>
