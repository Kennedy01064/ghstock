<template>
  <div v-if="catalogStore.isLoading && !admin" class="card text-text-secondary">
    Cargando datos del usuario...
  </div>

  <div v-else-if="admin" class="max-w-2xl mx-auto space-y-8 pb-32 px-4">
    <div class="flex flex-col gap-6">
      <RouterLink :to="{ name: 'catalogAdmins' }" class="inline-flex items-center gap-2 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted hover:text-amber transition-colors group">
        <svg class="w-4 h-4 transition-transform group-hover:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Cerrar Edicion
      </RouterLink>

      <div class="flex items-center justify-between">
        <div class="space-y-2">
          <span class="eyebrow">Ajustes de Cuenta</span>
          <h1 class="h2">Modificar Perfil</h1>
          <p class="text-text-muted font-medium">Actualizando parametros de acceso para: <span class="text-white">@{{ admin.username }}</span></p>
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
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="eyebrow !text-text-muted">Nombre Completo <span class="text-amber">*</span></label>
            <input v-model="form.name" type="text" required class="input-field font-bold">
          </div>
          <div class="space-y-2">
            <label class="eyebrow !text-text-muted">ID de Usuario <span class="text-amber">*</span></label>
            <input v-model="form.username" type="text" required class="input-field font-bold lowercase tracking-wider">
          </div>
        </div>

        <div class="space-y-2">
          <label class="eyebrow !text-text-muted">Nivel de Acceso Corporativo <span class="text-amber">*</span></label>
          <div class="relative">
            <button type="button" class="input-field flex justify-between items-center text-left" :class="authStore.currentRole !== 'superadmin' ? 'opacity-60 cursor-not-allowed' : ''" :disabled="authStore.currentRole !== 'superadmin'" @click="roleMenuOpen = !roleMenuOpen">
              <div class="flex items-center gap-3 min-w-0">
                <div class="w-2 h-2 rounded-full bg-amber shadow-[0_0_8px_rgba(242,173,61,0.5)]" />
                <span class="font-bold truncate uppercase tracking-widest text-[13px]">{{ roleDisplay }}</span>
              </div>
              <svg v-if="authStore.currentRole === 'superadmin'" class="w-4 h-4 text-text-muted transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <ul v-if="roleMenuOpen && authStore.currentRole === 'superadmin'" class="absolute z-50 w-full mt-3 bg-navy-accent border border-white/10 rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden backdrop-blur-xl">
              <li>
                <button type="button" class="w-full text-left px-5 py-4 hover:bg-white/5 transition-colors border-b border-white/5 group" @click="selectRole('admin')">
                  <div class="flex items-center gap-3">
                    <div class="w-1.5 h-1.5 rounded-full bg-amber/40 group-hover:bg-amber transition-colors" />
                    <span class="text-sm font-black text-white group-hover:text-amber transition-all">Perfil Operativo</span>
                  </div>
                  <p class="text-[10px] font-medium text-text-muted mt-1 ml-4.5">Gestion directa de pedidos y suministros de activos asignados.</p>
                </button>
              </li>
              <li>
                <button type="button" class="w-full text-left px-5 py-4 hover:bg-white/5 transition-colors group" @click="selectRole('manager')">
                  <div class="flex items-center gap-3">
                    <div class="w-1.5 h-1.5 rounded-full bg-amber/40 group-hover:bg-amber transition-colors" />
                    <span class="text-sm font-black text-white group-hover:text-amber transition-all">Perfil Directivo</span>
                  </div>
                  <p class="text-[10px] font-medium text-text-muted mt-1 ml-4.5">Control total del catalogo, infraestructura y auditoria de personal.</p>
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div class="space-y-2">
          <label class="eyebrow !text-text-muted">Nueva Contraseña <span class="text-[10px] lowercase text-text-muted opacity-50">(Opcional)</span></label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-white/20 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.1" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
            </div>
            <input v-model="form.password" type="password" placeholder="Dejar en blanco para conservar la actual" class="input-field !pl-12 font-bold tracking-widest">
          </div>
        </div>

        <div class="space-y-4 pt-4">
          <div class="flex items-center justify-between">
            <label class="eyebrow !text-text-muted">Infraestructura Asignada</label>
            <button type="button" class="text-[10px] font-black uppercase tracking-widest text-amber hover:text-white transition-colors" @click="toggleAllVisible">
              {{ allVisibleSelected ? "Desmarcar Todo" : "Seleccionar Todo" }}
            </button>
          </div>

          <div class="relative group">
            <input v-model="searchBuildings" type="text" placeholder="Filtrar sedes..." class="input-field !py-2.5 !pl-10 !text-xs font-bold bg-white/[0.02]">
            <svg class="w-4 h-4 text-text-muted absolute left-3.5 top-1/2 -translate-y-1/2 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar p-1">
            <label v-for="building in visibleBuildings" :key="building.id" class="relative flex items-center gap-4 p-4 rounded-2xl bg-white/[0.03] border border-white/5 cursor-pointer hover:bg-white/[0.06] hover:border-white/10 transition-all group/item">
              <input v-model="selectedBuildingIds" type="checkbox" :value="building.id" class="w-5 h-5 rounded-lg border-white/10 bg-navy-deep text-amber focus:ring-amber/40 focus:ring-offset-navy-deep transition-all cursor-pointer">
              <div class="min-w-0">
                <p class="text-[13px] font-black text-white truncate">{{ building.name }}</p>
                <p class="text-[10px] font-medium text-text-muted truncate mt-0.5">{{ building.address || "Sede sin direccion fiscal" }}</p>
              </div>
            </label>

            <div v-if="!visibleBuildings.length" class="col-span-full py-10 text-center border border-dashed border-white/10 rounded-2xl bg-white/[0.01]">
              <p class="text-xs font-medium text-text-muted">No se detectan sedes para ese filtro.</p>
            </div>
          </div>
        </div>

        <div class="pt-6 flex flex-col md:flex-row gap-4 border-t border-white/10">
          <RouterLink :to="{ name: 'catalogAdmins' }" class="btn btn-secondary flex-1">Descartar Cambios</RouterLink>
          <button type="submit" class="btn btn-primary flex-1 shadow-2xl shadow-amber/10" :disabled="catalogStore.isSubmittingAdmin">
            <svg v-if="!catalogStore.isSubmittingAdmin" class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else class="w-5 h-5 mr-1 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ catalogStore.isSubmittingAdmin ? "SINCRONIZANDO..." : "Sincronizar Datos" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import { useAuthStore } from "@/stores/authStore"
import { useCatalogStore } from "@/stores/catalogStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizeBuilding, normalizeUser } from "@/utils/normalizers"

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const catalogStore = useCatalogStore()
const uiStore = useUiStore()

const roleMenuOpen = ref(false)
const submitError = ref("")
const searchBuildings = ref("")
const selectedBuildingIds = ref([])
const form = reactive({
  name: "",
  username: "",
  role: "admin",
  password: "",
})

const admin = computed(() => (catalogStore.currentAdmin ? normalizeUser(catalogStore.currentAdmin) : null))
const buildings = computed(() => catalogStore.buildings.map(normalizeBuilding))
const visibleBuildings = computed(() =>
  buildings.value.filter((building) => building.name.toLowerCase().includes(searchBuildings.value.trim().toLowerCase())),
)
const allVisibleSelected = computed(() =>
  visibleBuildings.value.length > 0 && visibleBuildings.value.every((building) => selectedBuildingIds.value.includes(building.id)),
)
const roleDisplay = computed(() =>
  form.role === "manager" ? "Gerente de Operaciones (Manager)" : "Administrador de Edificio (Admin)",
)

function selectRole(role) {
  form.role = role
  roleMenuOpen.value = false
}

function toggleAllVisible() {
  if (allVisibleSelected.value) {
    const visibleIds = new Set(visibleBuildings.value.map((building) => building.id))
    selectedBuildingIds.value = selectedBuildingIds.value.filter((id) => !visibleIds.has(id))
    return
  }

  const merged = new Set(selectedBuildingIds.value)
  visibleBuildings.value.forEach((building) => merged.add(building.id))
  selectedBuildingIds.value = [...merged]
}

async function submitForm() {
  if (catalogStore.isSubmittingAdmin) return
  submitError.value = ""

  try {
    const payload = {
      name: form.name,
      username: form.username,
      role: authStore.currentRole === "superadmin" ? form.role : admin.value.role,
    }

    if (form.password) {
      payload.password = form.password
    }

    await catalogStore.updateAdmin(route.params.adminId, payload, {
      buildingIds: selectedBuildingIds.value,
      clearBuildings: selectedBuildingIds.value.length === 0,
    })

    uiStore.success("El perfil fue actualizado correctamente.", "Usuario sincronizado")
    await router.push({ name: "catalogAdmins" })
  } catch (error) {
    if (error.isConflict) {
      uiStore.error("El nombre de usuario ya esta en uso por otro administrador.", "Conflicto de Usuario")
      submitError.value = "Nombre de usuario ya registrado."
    } else {
      submitError.value = error.message
    }
  }
}

onMounted(async () => {
  await Promise.all([catalogStore.fetchAdmin(route.params.adminId), catalogStore.fetchBuildings()])

  if (admin.value) {
    form.name = admin.value.name ?? ""
    form.username = admin.value.username ?? ""
    form.role = admin.value.role ?? "admin"
    selectedBuildingIds.value = admin.value.assignedBuildings.map((building) => building.id)
  }
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #f2ad3d;
}
</style>
