<template>
  <div v-if="catalogStore.isLoading && !building" class="card text-text-secondary">
    Cargando edificio...
  </div>

  <div v-else-if="building" class="max-w-2xl mx-auto space-y-8 pb-32 px-4">
    <div class="flex flex-col gap-6">
      <RouterLink :to="{ name: 'catalogBuildings' }" class="inline-flex items-center gap-2 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted hover:text-amber transition-colors group">
        <svg class="w-4 h-4 transition-transform group-hover:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Cerrar Edicion
      </RouterLink>

      <div class="flex items-center justify-between">
        <div class="space-y-2">
          <span class="eyebrow">Mantenimiento de Sede</span>
          <h1 class="h2">Editar Infraestructura</h1>
          <p class="text-text-muted font-medium">Actualizando parametros tecnicos de: <span class="text-white">{{ building.name }}</span></p>
        </div>
        <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-white/10 bg-white/5 shadow-inner">
          <svg class="w-6 h-6 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </div>
      </div>
    </div>

    <div v-if="submitError" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ submitError }}
    </div>

    <div class="card">
      <form class="space-y-6" @submit.prevent="submitForm">
        <div class="space-y-2">
          <label class="eyebrow !text-text-muted">Nombre de la Sede <span class="text-amber">*</span></label>
          <input v-model="form.name" type="text" required class="input-field font-bold">
        </div>

        <div class="space-y-2">
          <label class="eyebrow !text-text-muted">Direccion / Localizacion</label>
          <input v-model="form.address" type="text" class="input-field font-bold">
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="eyebrow !text-text-muted">Capacidad Habitacional</label>
            <input v-model.number="form.departmentsCount" type="number" min="0" class="input-field font-bold">
          </div>

          <div class="space-y-2">
            <label class="eyebrow !text-text-muted">Gestor de Sede</label>
            <div class="relative">
              <button type="button" class="input-field flex justify-between items-center text-left" @click="adminMenuOpen = !adminMenuOpen">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-2 h-2 rounded-full bg-amber shadow-[0_0_8px_rgba(242,173,61,0.5)]" />
                  <span class="font-bold truncate text-[13px] uppercase tracking-widest">{{ selectedAdminLabel }}</span>
                </div>
                <svg class="w-4 h-4 text-text-muted transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <ul v-if="adminMenuOpen" class="absolute z-50 w-full mt-3 bg-navy-accent border border-white/10 rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden backdrop-blur-xl">
                <li>
                  <button type="button" class="w-full text-left px-5 py-3 hover:bg-white/5 transition-colors border-b border-white/5 text-xs font-black uppercase tracking-widest text-text-muted" @click="selectAdmin('')">
                    Liberar Gestion
                  </button>
                </li>
                <li v-for="admin in adminOptions" :key="admin.id">
                  <button type="button" class="w-full text-left px-5 py-4 hover:bg-white/5 transition-colors group" @click="selectAdmin(admin.id)">
                    <div class="flex items-center gap-3">
                      <div class="w-1.5 h-1.5 rounded-full bg-amber/40 group-hover:bg-amber transition-colors" />
                      <span class="text-sm font-black text-white group-hover:text-amber transition-all">{{ admin.name || admin.username }}</span>
                    </div>
                    <p class="text-[10px] font-medium text-text-muted mt-1 ml-4.5">@{{ admin.username }}</p>
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="space-y-4">
          <label class="eyebrow !text-text-muted">Evidencia Fotografica (Frontis)</label>
          <div v-if="buildingPreview" class="flex items-center gap-6 p-4 rounded-2xl bg-white/[0.03] border border-white/10 w-fit group/img">
            <div class="relative h-24 w-24 rounded-xl overflow-hidden shadow-lg border border-white/10">
              <img :src="buildingPreview" alt="Fachada" class="h-full w-full object-cover transition-transform group-hover/img:scale-110">
            </div>
            <div class="space-y-1">
              <p class="text-xs font-black text-white uppercase tracking-widest">Archivo Actual</p>
              <p class="text-[10px] font-medium text-text-muted">Actualice la ruta o URL para cambiar la vista del edificio.</p>
            </div>
          </div>
          <input v-model="form.imageUrl" type="text" placeholder="/static/uploads/frontis.png o https://..." class="input-field">
        </div>

        <div class="pt-6 flex flex-col md:flex-row gap-4 border-t border-white/10">
          <RouterLink :to="{ name: 'catalogBuildings' }" class="btn btn-secondary flex-1">Descartar</RouterLink>
          <button type="submit" class="btn btn-primary flex-1 shadow-2xl shadow-amber/10" :disabled="catalogStore.submitLoading">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
            </svg>
            Guardar Cambios
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import { useCatalogStore } from "@/stores/catalogStore"
import { useUiStore } from "@/stores/uiStore"
import { assetUrl, defaultBuildingUrl } from "@/utils/formatters"
import { normalizeBuilding, normalizeUser } from "@/utils/normalizers"

const route = useRoute()
const router = useRouter()
const catalogStore = useCatalogStore()
const uiStore = useUiStore()

const adminMenuOpen = ref(false)
const submitError = ref("")
const form = reactive({
  name: "",
  address: "",
  departmentsCount: 0,
  adminId: "",
  imageUrl: "",
})

const building = computed(() => (catalogStore.currentBuilding ? normalizeBuilding(catalogStore.currentBuilding) : null))
const adminOptions = computed(() =>
  catalogStore.admins.map(normalizeUser).filter((admin) => admin.role === "admin"),
)
const selectedAdminLabel = computed(() => {
  if (!form.adminId) {
    return "— Sin asignar —"
  }
  const selected = adminOptions.value.find((admin) => String(admin.id) === String(form.adminId))
  return selected ? (selected.name || selected.username) : "— Sin asignar —"
})
const buildingPreview = computed(() => (form.imageUrl ? assetUrl(form.imageUrl, defaultBuildingUrl) : ""))

function selectAdmin(value) {
  form.adminId = value ? String(value) : ""
  adminMenuOpen.value = false
}

async function submitForm() {
  submitError.value = ""

  try {
    await catalogStore.updateBuilding(route.params.buildingId, {
      name: form.name,
      address: form.address || null,
      departments_count: Number(form.departmentsCount || 0),
      admin_id: form.adminId ? Number(form.adminId) : null,
      imagen_frontis: form.imageUrl || null,
    })
    uiStore.success("La sede fue actualizada correctamente.", "Infraestructura sincronizada")
    await router.push({ name: 'catalogBuildings' })
  } catch (error) {
    submitError.value = error.message
  }
}

onMounted(async () => {
  await Promise.all([catalogStore.fetchAdmins("admin"), catalogStore.fetchBuilding(route.params.buildingId)])

  if (building.value) {
    form.name = building.value.name
    form.address = building.value.address || ""
    form.departmentsCount = building.value.departments_count ?? building.value.units ?? 0
    form.adminId = building.value.admin_id ? String(building.value.admin_id) : ""
    form.imageUrl = building.value.imagen_frontis || ""
  }
})
</script>
