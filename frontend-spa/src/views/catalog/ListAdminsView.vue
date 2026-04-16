<template>
  <div class="max-w-7xl mx-auto space-y-8 pb-32 px-4">
    <div class="flex flex-col xl:flex-row xl:items-end justify-between gap-6">
      <div class="space-y-3">
        <span class="eyebrow">{{ isSuperadmin ? "Gestión de accesos" : "Cobertura operativa" }}</span>
        <h1 class="text-4xl font-black tracking-tight text-white">Usuarios del sistema</h1>
        <p class="text-text-muted font-medium max-w-2xl">
          {{
            isSuperadmin
              ? "Administración centralizada de cuentas, roles, contraseñas, activación y cobertura operativa por edificio."
              : "Alta de cuentas admin para operación diaria y monitoreo de su cobertura por edificio."
          }}
        </p>
      </div>

      <div class="flex flex-col sm:flex-row gap-4 w-full xl:w-auto">
        <div class="relative w-full sm:w-80 group">
          <input v-model="query" type="text" placeholder="Buscar por usuario, nombre o edificio..." class="input-field !pl-10 !py-2.5 font-semibold" />
          <svg class="w-4 h-4 text-text-muted absolute left-3.5 top-1/2 -translate-y-1/2 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <RouterLink :to="{ name: 'catalogAssignBuilding' }" class="btn btn-secondary w-full sm:w-auto px-6">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          Asignar edificios
        </RouterLink>
        <RouterLink :to="{ name: 'catalogAdminCreate' }" class="btn btn-primary w-full sm:w-auto px-6 shadow-xl shadow-amber/10">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
          </svg>
          Nuevo usuario
        </RouterLink>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
      <article
        v-for="card in summaryCards"
        :key="card.label"
        class="card !py-5"
        :class="card.cardClass"
      >
        <p class="eyebrow !text-text-muted/60">{{ card.label }}</p>
        <p class="mt-2 text-4xl font-black" :class="card.valueClass">{{ card.value }}</p>
      </article>
    </div>

    <div v-if="userStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ userStore.error }}
    </div>

    <div class="card flex flex-col xl:flex-row gap-4 xl:items-center xl:justify-between">
      <div class="flex flex-wrap gap-2">
        <button
          v-for="option in roleFilters"
          :key="option.value"
          type="button"
          class="rounded-full border px-4 py-2 text-[10px] font-black uppercase tracking-[0.18em] transition-all"
          :class="selectedRole === option.value ? 'border-amber/40 bg-amber/10 text-amber' : 'border-white/[0.12] bg-white/[0.03] text-text-muted hover:text-white'"
          @click="selectedRole = option.value"
        >
          {{ option.label }}
        </button>
      </div>

      <div class="flex flex-wrap gap-2">
        <button
          v-for="option in statusFilters"
          :key="option.value"
          type="button"
          class="rounded-full border px-4 py-2 text-[10px] font-black uppercase tracking-[0.18em] transition-all"
          :class="selectedStatus === option.value ? 'border-white/20 bg-white/[0.06] text-white' : 'border-white/[0.12] bg-white/[0.03] text-text-muted hover:text-white'"
          @click="selectedStatus = option.value"
        >
          {{ option.label }}
        </button>
      </div>
    </div>

    <div v-if="userStore.isLoading" class="space-y-6">
      <DashboardSkeleton />
    </div>

    <div v-else-if="!filteredUsers.length" class="py-12">
      <EmptyState
        :title="query.trim() ? 'Sin coincidencias' : 'Usuarios no registrados'"
        :description="query.trim() ? `No encontramos resultados para '${query}'.` : 'Aún no hay cuentas administrativas disponibles.'"
      />
    </div>

    <div v-else class="card !p-0 overflow-hidden border-white/[0.07] bg-white/[0.02]">
      <div class="overflow-x-auto custom-scrollbar">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-white/[0.04] border-b border-white/[0.07]">
              <th class="px-8 py-5 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted">Cuenta</th>
              <th class="px-6 py-5 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted">Rol</th>
              <th class="px-6 py-5 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted">Estado</th>
              <th class="px-6 py-5 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted">Edificios</th>
              <th v-if="showActionsColumn" class="px-8 py-5 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted text-right">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5">
            <tr v-for="user in filteredUsers" :key="user.id" class="group transition-colors" :class="user.is_active === false ? 'bg-rose-500/[0.03] hover:bg-rose-500/[0.06]' : 'hover:bg-white/[0.03]'">
              <td class="px-8 py-6">
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 rounded-2xl border flex items-center justify-center text-lg font-black shrink-0 shadow-inner transition-transform group-hover:scale-105" :class="user.role === 'superadmin' ? 'bg-rose-500/10 border-rose-400/20 text-rose-300' : 'bg-amber/10 border-amber/20 text-amber'">
                    {{ userInitial(user) }}
                  </div>
                  <div class="min-w-0">
                    <p class="text-[15px] font-black text-white tracking-tight truncate">{{ user.name || "Sin nombre registrado" }}</p>
                    <div class="mt-1 flex items-center gap-2 flex-wrap">
                      <p class="text-[11px] font-bold text-text-muted uppercase tracking-widest">@{{ user.username }}</p>
                      <span v-if="user.role === 'superadmin'" class="inline-flex items-center rounded-lg border border-rose-400/20 bg-rose-500/10 px-2.5 py-1 text-[9px] font-black uppercase tracking-widest text-rose-200">
                        Cuenta protegida
                      </span>
                    </div>
                  </div>
                </div>
              </td>

              <td class="px-6 py-6">
                <span class="inline-flex items-center px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-[0.18em] border" :class="roleClass(user.role)">
                  {{ roleLabel(user.role) }}
                </span>
              </td>

              <td class="px-6 py-6">
                <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-[0.18em] border" :class="user.is_active === false ? 'border-rose-400/20 bg-rose-500/10 text-rose-200' : 'border-emerald-400/20 bg-emerald-500/10 text-emerald-200'">
                  <span class="w-1.5 h-1.5 rounded-full" :class="user.is_active === false ? 'bg-rose-300' : 'bg-emerald-300'" />
                  {{ user.is_active === false ? "Suspendido" : "Activo" }}
                </span>
              </td>

              <td class="px-6 py-6">
                <div v-if="user.assigned_buildings?.length" class="flex flex-wrap gap-2">
                  <span
                    v-for="building in user.assigned_buildings"
                    :key="`${user.id}-${building.id}`"
                    class="inline-flex items-center px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider bg-white/[0.04] border border-white/[0.12] text-white/80 transition-colors"
                  >
                    {{ building.name }}
                  </span>
                </div>
                <span v-else class="text-[10px] font-black uppercase tracking-widest text-text-muted/50 italic">
                  {{ user.role === "admin" ? "Sin cobertura" : "Sin asignación" }}
                </span>
              </td>

              <td v-if="showActionsColumn" class="px-8 py-6 text-right">
                <div class="flex items-center justify-end gap-2">
                  <RouterLink
                    :to="{ name: 'catalogAdminEdit', params: { adminId: user.id } }"
                    class="w-10 h-10 flex items-center justify-center rounded-xl border border-white/[0.07] bg-white/[0.04] text-text-muted hover:text-amber hover:border-amber/30 hover:bg-white/[0.08] transition-all"
                    title="Editar perfil"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </RouterLink>

                  <button
                    type="button"
                    class="w-10 h-10 flex items-center justify-center rounded-xl border border-white/[0.07] bg-white/[0.04] transition-all"
                    :class="user.role === 'superadmin' ? 'text-white/20 cursor-not-allowed' : user.is_active === false ? 'text-emerald-300 hover:border-emerald-400/30 hover:bg-emerald-400/10' : 'text-rose-300 hover:border-rose-500/30 hover:bg-rose-500/10'"
                    :disabled="user.role === 'superadmin'"
                    :title="user.is_active === false ? 'Reactivar cuenta' : 'Suspender cuenta'"
                    @click="openActionModal('toggle', user)"
                  >
                    <svg v-if="user.is_active === false" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                    </svg>
                    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M18.364 5.636l-1.414-1.414L12 9.172 7.05 4.222 5.636 5.636 10.586 10.586 5.636 15.536l1.414 1.414L12 12l4.95 4.95 1.414-1.414-4.95-4.95z" />
                    </svg>
                  </button>

                  <button
                    type="button"
                    class="w-10 h-10 flex items-center justify-center rounded-xl border border-white/[0.07] bg-white/[0.04] transition-all"
                    :class="user.role === 'superadmin' ? 'text-white/20 cursor-not-allowed' : 'text-text-muted hover:text-rose-500 hover:border-rose-500/30 hover:bg-rose-500/10'"
                    :disabled="user.role === 'superadmin'"
                    title="Eliminar registro"
                    @click="openActionModal('delete', user)"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <AppModal
      v-if="showActionsColumn"
      :open="Boolean(pendingAction.user)"
      eyebrow="Gestión de accesos"
      :title="modalTitle"
      :description="modalDescription"
      :confirm-label="modalConfirmLabel"
      :confirm-variant="pendingAction.type === 'delete' ? 'danger' : 'primary'"
      :loading="userStore.isSubmitting || userStore.isDeleting"
      @close="resetAction"
      @confirm="confirmAction"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"

import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import AppModal from "@/components/ui/AppModal.vue"
import EmptyState from "@/components/ui/EmptyState.vue"
import { useAuthStore } from "@/stores/authStore"
import { useUiStore } from "@/stores/uiStore"
import { useUserStore } from "@/stores/userStore"
import { normalizeUser } from "@/utils/normalizers"

const authStore = useAuthStore()
const userStore = useUserStore()
const uiStore = useUiStore()

const query = ref("")
const selectedRole = ref("all")
const selectedStatus = ref("all")
const pendingAction = reactive({
  type: "",
  user: null,
})

const isSuperadmin = computed(() => authStore.currentRole === "superadmin")
const showActionsColumn = computed(() => isSuperadmin.value)

const roleFilters = computed(() =>
  isSuperadmin.value
    ? [
        { value: "all", label: "Todos" },
        { value: "superadmin", label: "Superadmin" },
        { value: "manager", label: "Managers" },
        { value: "admin", label: "Admins" },
      ]
    : [
        { value: "all", label: "Admins" },
        { value: "admin", label: "Cobertura admin" },
      ],
)

const statusFilters = computed(() =>
  isSuperadmin.value
    ? [
        { value: "all", label: "Todos los estados" },
        { value: "active", label: "Solo activas" },
        { value: "inactive", label: "Solo suspendidas" },
      ]
    : [{ value: "all", label: "Cuentas activas" }],
)

const normalizedUsers = computed(() => userStore.users.map(normalizeUser))
const summaryCards = computed(() => {
  if (isSuperadmin.value) {
    return [
      { label: "Total de cuentas", value: normalizedUsers.value.length, valueClass: "text-white", cardClass: "" },
      { label: "Activas", value: normalizedUsers.value.filter((user) => user.is_active !== false).length, valueClass: "text-emerald-300", cardClass: "border-emerald-500/10" },
      { label: "Suspendidas", value: normalizedUsers.value.filter((user) => user.is_active === false).length, valueClass: "text-rose-300", cardClass: "border-rose-500/10" },
      { label: "Managers", value: normalizedUsers.value.filter((user) => user.role === "manager").length, valueClass: "text-white", cardClass: "" },
    ]
  }

  const adminsWithCoverage = normalizedUsers.value.filter((user) => (user.assigned_buildings?.length ?? 0) > 0).length
  const totalAssignedBuildings = normalizedUsers.value.reduce((total, user) => total + (user.assigned_buildings?.length ?? 0), 0)

  return [
    { label: "Admins activos", value: normalizedUsers.value.length, valueClass: "text-white", cardClass: "" },
    { label: "Con cobertura", value: adminsWithCoverage, valueClass: "text-emerald-300", cardClass: "border-emerald-500/10" },
    { label: "Sin cobertura", value: normalizedUsers.value.filter((user) => (user.assigned_buildings?.length ?? 0) === 0).length, valueClass: "text-amber", cardClass: "border-amber/10" },
    { label: "Edificios asignados", value: totalAssignedBuildings, valueClass: "text-white", cardClass: "" },
  ]
})

const filteredUsers = computed(() => {
  const term = query.value.trim().toLowerCase()

  return normalizedUsers.value.filter((user) => {
    if (selectedRole.value !== "all" && user.role !== selectedRole.value) {
      return false
    }

    if (selectedStatus.value === "active" && user.is_active === false) {
      return false
    }

    if (selectedStatus.value === "inactive" && user.is_active !== false) {
      return false
    }

    if (!term) {
      return true
    }

    const buildingNames = (user.assigned_buildings ?? []).map((building) => building.name).join(" ")
    return `${user.name ?? ""} ${user.username} ${user.role} ${buildingNames}`.toLowerCase().includes(term)
  })
})

const modalTitle = computed(() => {
  if (!pendingAction.user) {
    return ""
  }

  return pendingAction.type === "delete"
    ? "Eliminar usuario"
    : pendingAction.user.is_active === false
      ? "Reactivar acceso"
      : "Suspender acceso"
})

const modalDescription = computed(() => {
  if (!pendingAction.user) {
    return ""
  }

  if (pendingAction.type === "delete") {
    return `Se eliminará permanentemente a ${pendingAction.user.name || pendingAction.user.username}. Sus edificios asignados quedarán liberados.`
  }

  return pendingAction.user.is_active === false
    ? `La cuenta de ${pendingAction.user.username} volverá a estar habilitada para ingresar al sistema.`
    : `La cuenta de ${pendingAction.user.username} dejará de tener acceso hasta que sea reactivada por superadmin.`
})

const modalConfirmLabel = computed(() => {
  if (pendingAction.type === "delete") {
    return "Eliminar"
  }

  return pendingAction.user?.is_active === false ? "Reactivar" : "Suspender"
})

function userInitial(user) {
  return String(user.name || user.username || "U").trim().charAt(0).toUpperCase()
}

function roleLabel(role) {
  if (role === "superadmin") return "Superadmin"
  if (role === "manager") return "Manager"
  return "Admin"
}

function roleClass(role) {
  if (role === "superadmin") {
    return "border-rose-400/20 bg-rose-500/10 text-rose-200"
  }
  if (role === "manager") {
    return "border-amber/30 bg-amber/10 text-amber"
  }
  return "border-white/[0.12] bg-white/[0.04] text-text-muted"
}

function openActionModal(type, user) {
  pendingAction.type = type
  pendingAction.user = user
}

function resetAction() {
  pendingAction.type = ""
  pendingAction.user = null
}

async function confirmAction() {
  if (!pendingAction.user) {
    return
  }

  try {
    if (pendingAction.type === "delete") {
      await userStore.deleteUser(pendingAction.user.id)
      uiStore.success(`Se eliminó ${pendingAction.user.username}.`, "Usuario eliminado")
    } else {
      const updated = await userStore.toggleUserActive(pendingAction.user.id)
      uiStore.success(
        updated.is_active === false
          ? `La cuenta ${updated.username} fue suspendida.`
          : `La cuenta ${updated.username} fue reactivada.`,
        updated.is_active === false ? "Acceso suspendido" : "Acceso restablecido",
      )
    }

    resetAction()
  } catch (error) {
    uiStore.error(error.message, "No se pudo completar la acción")
  }
}

onMounted(() => {
  userStore.fetchUsers("", { includeInactive: isSuperadmin.value })
})
</script>


