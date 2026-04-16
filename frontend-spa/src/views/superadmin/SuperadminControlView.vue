<template>
  <div class="space-y-10 pb-24">
    <div class="flex flex-col xl:flex-row xl:items-end justify-between gap-8 border-b border-slate-200 pb-8">
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-6 rounded-full bg-rose-400 shadow-[0_0_14px_rgba(251,113,133,0.4)]" />
          <span class="eyebrow tracking-[0.35em] !text-rose-300 text-[10px]">Control de Superadmin</span>
        </div>
        <h1 class="text-5xl font-black tracking-tighter leading-none text-slate-900">
          Centro de <span class="text-amber">Control</span>
        </h1>
        <p class="max-w-2xl text-sm md:text-base font-medium text-text-muted">
          Gobierno operativo del sistema, suspensión global, identidad institucional y trazabilidad de cambios críticos.
        </p>
      </div>

      <div class="flex flex-wrap gap-4">
        <article class="card min-w-[180px] !py-5">
          <p class="eyebrow !text-text-muted/60">Usuarios activos</p>
          <p class="mt-2 text-4xl font-black text-slate-900">{{ activeUsers }}</p>
        </article>
        <article class="card min-w-[180px] !py-5 border-rose-500/10">
          <p class="eyebrow !text-text-muted/60">Usuarios suspendidos</p>
          <p class="mt-2 text-4xl font-black text-rose-300">{{ inactiveUsers }}</p>
        </article>
        <article class="card min-w-[180px] !py-5" :class="systemStore.isLocked ? 'border-rose-500/20 bg-rose-500/10' : 'border-emerald-500/10 bg-emerald-500/5'">
          <p class="eyebrow !text-text-muted/60">Estado plataforma</p>
          <p class="mt-2 text-lg font-black uppercase tracking-[0.2em]" :class="systemStore.isLocked ? 'text-rose-300' : 'text-emerald-300'">
            {{ systemStore.isLocked ? "Bloqueada" : "Operativa" }}
          </p>
        </article>
      </div>
    </div>

    <div v-if="systemStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ systemStore.error }}
    </div>

    <div class="grid gap-8 xl:grid-cols-[minmax(0,1.1fr)_420px]">
      <section class="card space-y-7">
        <div class="flex items-start justify-between gap-6">
          <div>
            <p class="eyebrow !text-amber">Identidad institucional</p>
            <h2 class="mt-3 text-2xl font-black tracking-tight text-slate-900">Configuración visible del sistema</h2>
            <p class="mt-3 max-w-xl text-sm leading-7 text-text-secondary">
              Ajusta el nombre institucional y el recurso visual principal conservando la línea gráfica actual.
            </p>
          </div>
          <div class="hidden sm:flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl border border-slate-200 bg-slate-50 shadow-inner">
            <img :src="brandingPreview" alt="Vista previa" class="h-9 w-9 object-contain" />
          </div>
        </div>

        <form class="grid gap-6 md:grid-cols-2" @submit.prevent="saveBranding">
          <div class="space-y-2 md:col-span-2">
            <label class="label-premium">Nombre institucional</label>
            <input v-model="brandingForm.institutional_name" type="text" class="input-field font-bold" placeholder="Grupo Hernandez" />
          </div>

          <div class="space-y-2 md:col-span-2">
            <label class="label-premium">Logo / URL principal</label>
            <input v-model="brandingForm.institutional_logo_url" type="text" class="input-field" placeholder="/static/img/logo_trans.png o https://..." />
          </div>

          <div class="md:col-span-2 flex items-center gap-4 rounded-[28px] border border-slate-200 bg-slate-50 p-5">
            <div class="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border border-slate-200 bg-slate-50">
              <img :src="brandingPreview" alt="Logo" class="h-11 w-11 object-contain" />
            </div>
            <div>
              <p class="text-sm font-black text-slate-900">{{ brandingForm.institutional_name || "Stock Management System" }}</p>
              <p class="mt-1 text-[11px] font-medium uppercase tracking-[0.2em] text-text-muted">Vista previa aplicada a login y control central</p>
            </div>
          </div>

          <div class="md:col-span-2 flex flex-col sm:flex-row gap-4 border-t border-slate-200 pt-6">
            <button type="submit" class="btn btn-primary flex-1" :disabled="systemStore.isSavingSettings">
              {{ systemStore.isSavingSettings ? "Guardando..." : "Guardar identidad" }}
            </button>
            <button type="button" class="btn btn-secondary flex-1" @click="resetBranding">
              Restablecer formulario
            </button>
          </div>
        </form>
      </section>

      <aside class="card space-y-6 border-rose-500/10">
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="eyebrow !text-rose-300">Seguridad operativa</p>
            <h2 class="mt-3 text-2xl font-black tracking-tight text-slate-900">Bloqueo global</h2>
          </div>
          <span class="inline-flex items-center rounded-full border px-3 py-1 text-[10px] font-black uppercase tracking-[0.2em]" :class="systemStore.isLocked ? 'border-rose-400/30 bg-rose-500/10 text-rose-200' : 'border-emerald-400/30 bg-emerald-500/10 text-emerald-200'">
            {{ systemStore.isLocked ? "Activo" : "Inactivo" }}
          </span>
        </div>

        <div class="rounded-[28px] border border-slate-200 bg-slate-50 p-5 space-y-4">
          <p class="text-sm leading-7 text-text-secondary">
            Cuando el bloqueo está activo, solo el superadmin puede iniciar sesión. El resto de usuarios recibe un aviso para contactar al desarrollador.
          </p>
          <div class="rounded-2xl border px-4 py-4 text-sm font-semibold" :class="systemStore.isLocked ? 'border-rose-400/20 bg-rose-500/10 text-rose-100' : 'border-slate-200 bg-slate-50 text-text-secondary'">
            {{ lockdownMessage }}
          </div>
        </div>

        <button
          type="button"
          class="btn w-full"
          :class="systemStore.isLocked ? 'bg-emerald-500 text-navy-deep hover:bg-emerald-400' : 'bg-rose-500 text-slate-900 hover:bg-rose-400'"
          @click="lockdownModalOpen = true"
        >
          {{ systemStore.isLocked ? "Reactivar sistema" : "Suspender sistema" }}
        </button>

        <div class="rounded-[28px] border border-slate-200 bg-slate-100/40 p-5 space-y-3">
          <p class="text-[11px] font-black uppercase tracking-[0.2em] text-slate-900/50">Ultima sincronización</p>
          <p class="text-lg font-black text-slate-900">{{ formatDate(systemStore.settings?.last_updated) }}</p>
          <p class="text-xs leading-6 text-text-muted">
            Cualquier cambio aplicado aquí se refleja en el login institucional y en el control de acceso del backend.
          </p>
        </div>
      </aside>
    </div>

    <section class="card !p-0 overflow-hidden">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-5 border-b border-slate-200 px-8 py-6 bg-slate-50">
        <div>
          <p class="eyebrow !text-amber">Auditoría</p>
          <h2 class="mt-2 text-2xl font-black tracking-tight text-slate-900">Eventos críticos recientes</h2>
        </div>

        <div class="flex flex-col sm:flex-row gap-3">
          <div class="relative min-w-[260px]">
            <input v-model="auditSearch" type="search" class="input-field !py-2.5 !pl-10 text-sm font-semibold" placeholder="Buscar por acción o detalle..." />
            <svg class="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <button type="button" class="btn btn-secondary" :disabled="systemStore.isLoadingAudit" @click="reloadAudit">
            {{ systemStore.isLoadingAudit ? "Actualizando..." : "Recargar" }}
          </button>
        </div>
      </div>

      <div v-if="systemStore.isLoadingAudit && !systemStore.auditLogs.length" class="px-8 py-10 text-sm text-text-secondary">
        Cargando trazabilidad del sistema...
      </div>

      <div v-else-if="!filteredLogs.length" class="px-8 py-12 text-center text-sm text-text-secondary">
        No se encontraron eventos para ese criterio.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200">
              <th class="px-8 py-4 text-[10px] font-black uppercase tracking-[0.2em] text-text-muted">Evento</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase tracking-[0.2em] text-text-muted">Usuario</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase tracking-[0.2em] text-text-muted">Detalle</th>
              <th class="px-8 py-4 text-[10px] font-black uppercase tracking-[0.2em] text-text-muted text-right">Fecha</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="log in filteredLogs" :key="log.id" class="hover:bg-slate-50 transition-colors">
              <td class="px-8 py-5">
                <div class="space-y-1">
                  <p class="text-sm font-black text-slate-900">{{ humanizeAction(log.action) }}</p>
                  <p class="text-[10px] font-bold uppercase tracking-[0.2em] text-text-muted">
                    {{ log.resource_type || "Sistema" }} <span v-if="log.resource_id">#{{ log.resource_id }}</span>
                  </p>
                </div>
              </td>
              <td class="px-6 py-5">
                <span class="inline-flex items-center rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-[11px] font-black uppercase tracking-[0.15em] text-slate-900/80">
                  {{ log.username || "Sistema" }}
                </span>
              </td>
              <td class="px-6 py-5 text-sm leading-7 text-text-secondary">
                {{ log.details || "Sin detalle adicional." }}
              </td>
              <td class="px-8 py-5 text-right text-[11px] font-black uppercase tracking-[0.18em] text-text-muted">
                {{ formatDate(log.timestamp) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <AppModal
      :open="lockdownModalOpen"
      eyebrow="Seguridad crítica"
      :title="systemStore.isLocked ? 'Reactivar el acceso general' : 'Suspender acceso general'"
      :description="systemStore.isLocked ? 'Se restablecerá el acceso para managers y administradores.' : 'Solo el superadmin podrá entrar al sistema hasta nuevo aviso.'"
      :confirm-label="systemStore.isLocked ? 'Reactivar sistema' : 'Suspender sistema'"
      :confirm-variant="systemStore.isLocked ? 'primary' : 'danger'"
      :loading="systemStore.isSavingSettings"
      @close="lockdownModalOpen = false"
      @confirm="toggleLockdown"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"

import AppModal from "@/components/ui/AppModal.vue"
import { useSystemStore } from "@/stores/systemStore"
import { useUiStore } from "@/stores/uiStore"
import { useUserStore } from "@/stores/userStore"
import { assetUrl, formatDate, logoUrl } from "@/utils/formatters"

const systemStore = useSystemStore()
const uiStore = useUiStore()
const userStore = useUserStore()

const lockdownModalOpen = ref(false)
const auditSearch = ref("")
const brandingForm = reactive({
  institutional_name: "",
  institutional_logo_url: "",
})

const activeUsers = computed(() =>
  userStore.users.filter((user) => user.is_active !== false).length,
)
const inactiveUsers = computed(() =>
  userStore.users.filter((user) => user.is_active === false).length,
)
const brandingPreview = computed(() =>
  assetUrl(brandingForm.institutional_logo_url || systemStore.settings?.institutional_logo_url, logoUrl),
)
const lockdownMessage = computed(() =>
  systemStore.isLocked
    ? "Sistema temporalmente bloqueado. Contacte al desarrollador."
    : "Acceso operativo normal para superadmin, managers y administradores habilitados.",
)
const filteredLogs = computed(() => {
  const term = auditSearch.value.trim().toLowerCase()
  if (!term) {
    return systemStore.auditLogs
  }

  return systemStore.auditLogs.filter((log) =>
    `${log.action} ${log.username || ""} ${log.details || ""} ${log.resource_type || ""} ${log.resource_id || ""}`
      .toLowerCase()
      .includes(term),
  )
})

function syncBrandingForm() {
  brandingForm.institutional_name = systemStore.settings?.institutional_name ?? ""
  brandingForm.institutional_logo_url = systemStore.settings?.institutional_logo_url ?? ""
}

function resetBranding() {
  syncBrandingForm()
}

async function saveBranding() {
  try {
    await systemStore.updateSettings({
      institutional_name: brandingForm.institutional_name,
      institutional_logo_url: brandingForm.institutional_logo_url,
    })
    uiStore.success("La identidad institucional fue actualizada.", "Configuración guardada")
  } catch (error) {
    uiStore.error(error.message, "No se pudo guardar la configuración")
  }
}

async function toggleLockdown() {
  try {
    await systemStore.updateSettings({
      lockdown_enabled: !systemStore.isLocked,
    })
    lockdownModalOpen.value = false
    uiStore.warning(
      systemStore.isLocked
        ? "El acceso quedó restringido exclusivamente para superadmin."
        : "El acceso general fue restablecido para el resto del sistema.",
      systemStore.isLocked ? "Sistema suspendido" : "Sistema reactivado",
    )
    await reloadAudit()
  } catch (error) {
    uiStore.error(error.message, "No se pudo cambiar el estado del sistema")
  }
}

async function reloadAudit() {
  try {
    await systemStore.fetchAuditLogs({ limit: 80 })
  } catch (error) {
    uiStore.error(error.message, "No se pudo cargar la auditoría")
  }
}

function humanizeAction(action) {
  const dictionary = {
    "system.settings.updated": "Configuración del sistema",
    "user.created": "Alta de usuario",
    "user.updated": "Actualización de usuario",
    "user.deleted": "Eliminación de usuario",
    "user.toggled_active": "Cambio de estado de usuario",
  }

  return dictionary[action] ?? action
}

onMounted(async () => {
  try {
    await Promise.all([
      systemStore.fetchSettings(),
      systemStore.fetchAuditLogs({ limit: 80 }),
      userStore.fetchUsers("", { includeInactive: true }),
    ])
    syncBrandingForm()
  } catch (error) {
    uiStore.error(error.message, "No se pudo cargar el centro de control")
  }
})
</script>
