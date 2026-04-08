<template>
  <div class="max-w-6xl mx-auto space-y-8 pb-32 px-4">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
      <div class="space-y-2">
        <span class="eyebrow">Gestion de Accesos</span>
        <h1 class="text-4xl font-black tracking-tight text-white">Usuarios</h1>
        <p class="text-text-muted font-medium">Control de cuentas, roles y asignaciones de infraestructura.</p>
      </div>

      <div class="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto">
        <div class="relative w-full sm:w-72 group">
          <input v-model="query" type="text" placeholder="Buscar administrador..." class="input-field !pl-10 !py-2.5 font-semibold" />
          <svg class="w-4 h-4 text-text-muted absolute left-3.5 top-1/2 -translate-y-1/2 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <RouterLink :to="{ name: 'catalogAdminCreate' }" class="btn btn-primary w-full sm:w-auto px-6 shadow-xl shadow-amber/10">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
          </svg>
          Nuevo Registro
        </RouterLink>
      </div>
    </div>

    <div v-if="userStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ userStore.error }}
    </div>

    <div v-if="userStore.isLoading" class="space-y-6">
      <DashboardSkeleton />
    </div>

    <div v-else-if="!filteredAdmins.length" class="py-12">
      <EmptyState
        :title="query.trim() ? 'Sin resultados' : 'Usuarios no registrados'"
        :description="query.trim() ? `No encontramos coincidencias para '${query}'.` : 'No hay administradores registrados en el sistema corporativo.'"
      />
    </div>

    <div v-else class="card !p-0 overflow-hidden border-white/5 bg-white/[0.02]">
      <div class="overflow-x-auto custom-scrollbar">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-white/[0.04] border-b border-white/5">
              <th class="px-8 py-5 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted">Perfil / Usuario</th>
              <th class="px-6 py-5 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted text-center">Edificios Asignados</th>
              <th class="px-8 py-5 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted text-right">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5">
            <tr v-for="admin in filteredAdmins" :key="admin.id" class="group hover:bg-white/[0.03] transition-colors">
              <td class="px-8 py-6">
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 rounded-2xl bg-amber/10 border border-amber/20 flex items-center justify-center text-amber text-lg font-black shrink-0 shadow-inner group-hover:scale-105 transition-transform">
                    {{ adminInitial(admin) }}
                  </div>
                  <div class="min-w-0">
                    <p class="text-[15px] font-black text-white tracking-tight truncate">{{ admin.name || "Sin Nombre Registrado" }}</p>
                    <div class="mt-1 flex items-center gap-2 flex-wrap">
                      <p class="text-[11px] font-bold text-text-muted uppercase tracking-widest">@{{ admin.username }}</p>
                      <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest border" :class="admin.role === 'manager' ? 'bg-amber/10 text-amber border-amber/30' : 'bg-white/5 text-text-muted border-white/10'">
                        {{ admin.role === "manager" ? "Manager" : "Admin" }}
                      </span>
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-6">
                <div v-if="admin.assigned_buildings?.length" class="flex flex-wrap justify-center gap-2">
                  <span
                    v-for="building in admin.assigned_buildings"
                    :key="`${admin.id}-${building.id}`"
                    class="inline-flex items-center px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider bg-white/5 border border-white/10 text-white/80 group-hover:border-amber/30 transition-colors"
                  >
                    {{ building.name }}
                  </span>
                </div>
                <div v-else class="flex justify-center">
                  <span class="text-[10px] font-black uppercase tracking-widest text-text-muted/40 italic">Inactivo</span>
                </div>
              </td>
              <td class="px-8 py-6 text-right">
                <div class="flex items-center justify-end gap-2">
                  <RouterLink
                    :to="{ name: 'catalogAdminEdit', params: { adminId: admin.id } }"
                    class="w-10 h-10 flex items-center justify-center rounded-xl border border-white/5 bg-white/5 text-text-muted hover:text-amber hover:border-amber/30 hover:bg-white/[0.08] transition-all"
                    title="Editar Perfil"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </RouterLink>
                  <button
                    type="button"
                    class="w-10 h-10 flex items-center justify-center rounded-xl border border-white/5 bg-white/5 text-text-muted hover:text-rose-500 hover:border-rose-500/30 hover:bg-rose-500/10 transition-all"
                    title="Eliminar Registro"
                    @click="pendingAdminId = admin.id"
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
      :open="Boolean(pendingAdmin)"
      eyebrow="Gestion de accesos"
      title="Eliminar administrador"
      :description="pendingAdmin ? `Confirma la eliminacion permanente de ${pendingAdmin.name || pendingAdmin.username}.` : ''"
      confirm-label="Eliminar"
      confirm-variant="danger"
      :loading="userStore.isDeleting"
      @close="pendingAdminId = null"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"

import AppModal from "@/components/ui/AppModal.vue"
import EmptyState from "@/components/ui/EmptyState.vue"
import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import { useUserStore } from "@/stores/userStore"
import { useUiStore } from "@/stores/uiStore"

const userStore = useUserStore()
const uiStore = useUiStore()
const query = ref("")
const pendingAdminId = ref(null)

const filteredAdmins = computed(() => {
  const admins = userStore.users ?? []
  const term = query.value.trim().toLowerCase()

  if (!term) {
    return admins
  }

  return admins.filter((admin) => {
    const assigned = (admin.assigned_buildings ?? []).map((building) => building.name).join(" ")
    return `${admin.name ?? ""} ${admin.username} ${assigned}`.toLowerCase().includes(term)
  })
})

const pendingAdmin = computed(() => userStore.users.find((admin) => admin.id === pendingAdminId.value) ?? null)

onMounted(() => {
  userStore.fetchUsers("admin")
})

function adminInitial(admin) {
  return String(admin.name || admin.username || "U").trim().charAt(0).toUpperCase()
}

async function confirmDelete() {
  if (!pendingAdmin.value) {
    return
  }

  try {
    await userStore.deleteUser(pendingAdmin.value.id)
    uiStore.success(`Se elimino ${pendingAdmin.value.username}.`, "Administrador eliminado")
    pendingAdminId.value = null
  } catch (error) {
    uiStore.error(error.message, "No se pudo eliminar el administrador")
  }
}
</script>

