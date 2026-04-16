<template>
  <div class="max-w-2xl mx-auto space-y-8 pb-20 px-4">
    <div class="flex flex-col gap-6">
      <RouterLink :to="{ name: 'dashboard' }" class="inline-flex items-center gap-2 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted hover:text-amber transition-colors group">
        <svg class="w-4 h-4 transition-transform group-hover:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Volver al Inicio
      </RouterLink>

      <div class="flex items-center justify-between">
        <div class="space-y-2">
          <span class="eyebrow">Gestion de Activos Fijos</span>
          <h1 class="h2">Nueva Sede</h1>
          <p class="text-text-muted font-medium">Registro de infraestructura para control de inventarios.</p>
        </div>
        <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-white/[0.12] bg-white/[0.04] shadow-inner">
          <svg class="w-6 h-6 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5" />
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
          <label class="label-premium">Denominacion de Sede <span class="text-amber">*</span></label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-slate-900/10 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5" />
              </svg>
            </div>
            <input v-model="form.name" type="text" required autofocus placeholder="Ej: Torre Empresarial Norte, Almacen Callao..." class="input-field !pl-12 font-bold">
          </div>
        </div>

        <div class="space-y-2">
          <label class="label-premium">Direccion Fiscal / Referencia</label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-slate-900/10 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0zM15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <input v-model="form.address" type="text" placeholder="Ej: Av. Javier Prado Este 123, San Isidro" class="input-field !pl-12">
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="label-premium">Unidades Habitacionales</label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-900/10 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <input v-model.number="form.departmentsCount" type="number" min="0" class="input-field !pl-12 font-bold">
            </div>
          </div>

          <div class="space-y-2">
            <label class="label-premium">Administrador Responsable</label>
            <div class="relative">
              <button type="button" class="input-field flex justify-between items-center text-left" @click="adminMenuOpen = !adminMenuOpen">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-2 h-2 rounded-full bg-amber shadow-[0_0_8px_rgba(242,173,61,0.5)]" />
                  <span class="font-bold truncate">{{ selectedAdminLabel }}</span>
                </div>
                <svg class="w-4 h-4 text-text-muted transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <ul v-if="adminMenuOpen" class="absolute z-50 w-full mt-3 bg-white border border-white/[0.12] rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden backdrop-blur-xl">
                <li>
                  <button type="button" class="w-full text-left px-5 py-3 hover:bg-white/[0.04] transition-colors border-b border-white/[0.07] text-xs font-black uppercase tracking-widest text-text-muted" @click="selectAdmin('')">
                    Liberar Asignacion
                  </button>
                </li>
                <li v-for="admin in adminOptions" :key="admin.id">
                  <button type="button" class="w-full text-left px-5 py-4 hover:bg-white/[0.04] transition-colors group" @click="selectAdmin(admin.id)">
                    <div class="flex items-center gap-3">
                      <div class="w-1.5 h-1.5 rounded-full bg-amber/40 group-hover:bg-amber transition-colors" />
                      <span class="text-sm font-black text-slate-900 group-hover:text-amber transition-all">@{{ admin.username }}</span>
                    </div>
                    <p class="text-[10px] font-medium text-text-muted mt-1 ml-4.5">{{ admin.name || "Gestor Corporativo" }}</p>
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="space-y-4">
          <label class="label-premium">Fachada / Imagen del Edificio</label>

          <!-- Mode toggle -->
          <div class="flex gap-2">
            <button
              type="button"
              class="px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all"
              :class="imageMode === 'url' ? 'bg-amber text-navy-deep' : 'bg-white/[0.04] text-text-muted hover:bg-white/[0.06]'"
              @click="imageMode = 'url'"
            >Enlace URL</button>
            <button
              type="button"
              class="px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all"
              :class="imageMode === 'file' ? 'bg-amber text-navy-deep' : 'bg-white/[0.04] text-text-muted hover:bg-white/[0.06]'"
              @click="imageMode = 'file'"
            >Subir Archivo</button>
          </div>

          <!-- URL input -->
          <input v-if="imageMode === 'url'" v-model="form.imageUrl" type="text" placeholder="https://... o /static/uploads/frontis.png" class="input-field">

          <!-- File upload -->
          <div v-else>
            <label
              class="flex flex-col items-center justify-center w-full h-32 rounded-2xl border-2 border-dashed border-white/[0.12] bg-white/[0.02] hover:border-amber/30 hover:bg-amber/5 transition-all cursor-pointer"
              :class="isUploading ? 'pointer-events-none opacity-60' : ''"
            >
              <div v-if="isUploading" class="flex flex-col items-center gap-2">
                <svg class="w-6 h-6 text-amber animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span class="text-[10px] font-black uppercase tracking-widest text-amber">Subiendo...</span>
              </div>
              <div v-else class="flex flex-col items-center gap-2">
                <svg class="w-8 h-8 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="text-[10px] font-black uppercase tracking-widest text-text-muted">Haz clic o arrastra una imagen</span>
                <span class="text-[9px] text-text-muted/60">JPG, PNG o WEBP</span>
              </div>
              <input type="file" accept="image/jpeg,image/png,image/webp" class="hidden" @change="handleFileUpload">
            </label>
            <p v-if="uploadError" class="text-[10px] text-rose-400 mt-2 font-bold">{{ uploadError }}</p>
          </div>

          <!-- Preview -->
          <div v-if="buildingPreview" class="flex items-center gap-6 p-4 rounded-2xl bg-white/[0.03] border border-white/[0.12] w-fit group/img">
            <div class="relative h-24 w-24 rounded-xl overflow-hidden shadow-lg border border-white/[0.12]">
              <img :src="buildingPreview" alt="Preview" class="h-full w-full object-cover transition-transform group-hover/img:scale-110">
            </div>
            <div class="space-y-1">
              <p class="text-xs font-black text-slate-900 uppercase tracking-widest">Vista previa</p>
              <p class="text-[10px] font-medium text-text-muted">Imagen vinculada al edificio.</p>
            </div>
          </div>
        </div>

        <div class="pt-6 flex flex-col md:flex-row gap-4 border-t border-white/[0.12]">
          <RouterLink :to="{ name: 'dashboard' }" class="btn btn-secondary flex-1">Cancelar</RouterLink>
          <button type="submit" class="btn btn-primary flex-1 shadow-2xl shadow-amber/10" :disabled="buildingStore.isSubmitting">
            <svg v-if="!buildingStore.isSubmitting" class="w-5 h-5 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
            </svg>
            <svg v-else class="w-5 h-5 mx-1 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ buildingStore.isSubmitting ? "REGISTRANDO..." : "Registrar Sede" }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="!adminOptions.length" class="flex items-center gap-4 p-5 rounded-2xl bg-amber/5 border border-amber/10 text-amber">
      <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <p class="text-[11px] font-medium">
        <span class="font-black uppercase tracking-widest block mb-1">Aviso Critico:</span>
        No se detectan administradores registrados. Se recomienda vincular un responsable despues de la creacion.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useRouter } from "vue-router"

import { useBuildingStore } from "@/stores/buildingStore"
import { useUserStore } from "@/stores/userStore"
import { useUiStore } from "@/stores/uiStore"
import { assetUrl, defaultBuildingUrl } from "@/utils/formatters"
import { normalizeUser } from "@/utils/normalizers"
import mediaApi from "@/api/media.api"

const router = useRouter()
const buildingStore = useBuildingStore()
const userStore = useUserStore()
const uiStore = useUiStore()

const adminMenuOpen = ref(false)
const submitError = ref("")
const imageMode = ref("url")
const isUploading = ref(false)
const uploadError = ref("")
const form = reactive({
  name: "",
  address: "",
  departmentsCount: 0,
  adminId: "",
  imageUrl: "",
})

const adminOptions = computed(() =>
  userStore.users.map(normalizeUser).filter((admin) => admin.role === "admin" && admin.is_active !== false),
)
const selectedAdminLabel = computed(() => {
  if (!form.adminId) {
    return "— Sin asignar —"
  }
  return adminOptions.value.find((admin) => String(admin.id) === String(form.adminId))?.username || "— Sin asignar —"
})
const buildingPreview = computed(() => assetUrl(form.imageUrl, defaultBuildingUrl))

function selectAdmin(value) {
  form.adminId = value ? String(value) : ""
  adminMenuOpen.value = false
}

async function handleFileUpload(event) {
  const file = event.target.files?.[0]
  if (!file) return
  uploadError.value = ""
  isUploading.value = true
  try {
    const { data } = await mediaApi.uploadImage(file)
    form.imageUrl = data.url
  } catch {
    uploadError.value = "No se pudo subir la imagen. Intenta de nuevo."
  } finally {
    isUploading.value = false
  }
}

async function submitForm() {
  if (buildingStore.isSubmitting) return
  submitError.value = ""

  try {
    await buildingStore.createBuilding({
      name: form.name,
      address: form.address || null,
      departments_count: Number(form.departmentsCount || 0),
      admin_id: form.adminId ? Number(form.adminId) : null,
      imagen_frontis: form.imageUrl || null,
    })
    uiStore.success("La sede fue registrada correctamente.", "Infraestructura creada")
    await router.push({ name: "catalogBuildings" })
  } catch (error) {
    if (error.isConflict) {
      submitError.value = "El nombre de la sede ya existe. Por favor, elige uno diferente."
    } else {
      submitError.value = error.message
    }
  }
}

onMounted(() => {
  userStore.fetchUsers("admin", { includeInactive: false })
})
</script>
