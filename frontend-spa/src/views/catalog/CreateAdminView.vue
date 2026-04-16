<template>
  <div class="max-w-2xl mx-auto space-y-8 pb-20 px-4">
    <div class="flex flex-col gap-6">
      <RouterLink :to="{ name: 'catalogAdmins' }" class="inline-flex items-center gap-2 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted hover:text-amber transition-colors group">
        <svg class="w-4 h-4 transition-transform group-hover:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Volver al Listado
      </RouterLink>

      <div class="flex items-center justify-between">
        <div class="space-y-2">
          <span class="eyebrow">Gestion de Talento</span>
          <h1 class="h2">Alta de Personal</h1>
          <p class="text-text-muted font-medium">Configuracion de credenciales y permisos corporativos.</p>
        </div>
        <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-white/[0.12] bg-white/[0.04] shadow-inner">
          <svg class="w-6 h-6 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
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
          <div class="space-y-1">
            <label class="label-premium">Nombre Completo <span class="text-amber">*</span></label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-900/20 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <input data-testid="user-fullname" v-model="form.name" type="text" required autofocus placeholder="Juan Perez" class="input-field !pl-12">
            </div>
          </div>

          <div class="space-y-1">
            <label class="label-premium">ID de Usuario <span class="text-amber">*</span></label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <span class="text-slate-900/20 font-black group-focus-within:text-amber transition-colors">@</span>
              </div>
              <input data-testid="user-username" v-model="form.username" type="text" required placeholder="jperez_gh" class="input-field !pl-12 lowercase">
            </div>
          </div>
        </div>

        <div class="space-y-2">
          <label class="eyebrow !text-text-muted">Nivel de Acceso <span class="text-amber">*</span></label>
          <div class="relative">
            <button
              type="button"
              class="input-field flex justify-between items-center text-left"
              :class="authStore.currentRole !== 'superadmin' ? 'opacity-60 cursor-not-allowed' : ''"
              :disabled="authStore.currentRole !== 'superadmin'"
              @click="roleMenuOpen = !roleMenuOpen"
            >
              <div class="flex items-center gap-3 min-w-0">
                <div class="w-2 h-2 rounded-full bg-amber shadow-[0_0_8px_rgba(242,173,61,0.5)]" />
                <span class="font-bold truncate">{{ roleDisplay }}</span>
              </div>
              <svg v-if="authStore.currentRole === 'superadmin'" class="w-4 h-4 text-text-muted transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <ul v-if="roleMenuOpen && authStore.currentRole === 'superadmin'" class="absolute z-50 w-full mt-3 bg-[#1e293b] border border-white/[0.12] rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden backdrop-blur-xl">
              <li>
                <button type="button" class="w-full text-left px-5 py-4 hover:bg-white/[0.04] transition-colors border-b border-white/[0.07] group" @click="selectRole('admin')">
                  <div class="flex items-center gap-3">
                    <div class="w-1.5 h-1.5 rounded-full bg-amber/40 group-hover:bg-amber transition-colors" />
                    <span class="text-sm font-black text-slate-900 group-hover:text-amber transition-all">Perfil Operativo</span>
                  </div>
                  <p class="text-[10px] font-medium text-text-muted mt-1 ml-4.5">Gestion directa de pedidos y suministros de activos asignados.</p>
                </button>
              </li>
              <li>
                <button type="button" class="w-full text-left px-5 py-4 hover:bg-white/[0.04] transition-colors group" @click="selectRole('manager')">
                  <div class="flex items-center gap-3">
                    <div class="w-1.5 h-1.5 rounded-full bg-amber/40 group-hover:bg-amber transition-colors" />
                    <span class="text-sm font-black text-slate-900 group-hover:text-amber transition-all">Perfil Directivo</span>
                  </div>
                  <p class="text-[10px] font-medium text-text-muted mt-1 ml-4.5">Gestion integral de catalogo, edificios y alta de cuentas administrativas.</p>
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-1">
            <label class="label-premium">Contraseña Maestra <span class="text-amber">*</span></label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-900/20 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input data-testid="user-password" v-model="form.password" type="password" required placeholder="6+ caracteres" class="input-field !pl-12 tracking-widest">
            </div>
          </div>

          <div class="space-y-1">
            <label class="label-premium">Verificacion <span class="text-amber">*</span></label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-900/20 group-focus-within:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <input data-testid="user-confirm-password" v-model="form.confirmPassword" type="password" required placeholder="Repetir clave" class="input-field !pl-12 tracking-widest">
            </div>
          </div>
        </div>

        <div class="pt-6 flex flex-col md:flex-row gap-4 border-t border-white/[0.12]">
          <RouterLink :to="{ name: 'catalogAdmins' }" class="btn btn-secondary flex-1">Cancelar</RouterLink>
          <button data-testid="user-submit" type="submit" class="btn btn-primary flex-1 shadow-2xl shadow-amber/10" :disabled="userStore.isSubmitting">
            <svg v-if="!userStore.isSubmitting" class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
            <svg v-else class="w-5 h-5 mr-1 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ userStore.isSubmitting ? "REGISTRANDO..." : "Confirmar Registro" }}
          </button>
        </div>
      </form>
    </div>

    <div class="p-5 rounded-2xl bg-white/[0.04] border border-white/[0.07] flex items-start gap-4">
      <div class="h-10 w-10 flex items-center justify-center rounded-xl bg-amber/10 border border-amber/20 text-amber shrink-0">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      </div>
      <div class="space-y-1">
        <p class="text-xs font-black text-slate-900 uppercase tracking-widest">Protocolo de Seguridad</p>
        <p class="text-[11px] font-medium text-text-muted leading-relaxed">
          Las contraseñas deben ser unicas para cada usuario. Se recomienda el uso de caracteres alfanumericos y simbolos para mayor proteccion de la infraestructura logistica.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue"
import { useRouter } from "vue-router"

import { useAuthStore } from "@/stores/authStore"
import { useUserStore } from "@/stores/userStore"
import { useUiStore } from "@/stores/uiStore"

const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()
const uiStore = useUiStore()

const roleMenuOpen = ref(false)
const submitError = ref("")
const form = reactive({
  name: "",
  username: "",
  role: "admin",
  password: "",
  confirmPassword: "",
})

const roleDisplay = computed(() =>
  form.role === "manager" ? "Gerente de Operaciones (Manager)" : "Administrador de Edificio (Admin)",
)

function selectRole(role) {
  form.role = role
  roleMenuOpen.value = false
}

async function submitForm() {
  if (userStore.isSubmitting) return
  submitError.value = ""

  if (form.password !== form.confirmPassword) {
    submitError.value = "La verificacion de contraseña no coincide."
    return
  }

  try {
    await userStore.createUser({
      name: form.name,
      username: form.username,
      role: authStore.currentRole === "superadmin" ? form.role : "admin",
      password: form.password,
    })
    uiStore.success("El usuario fue registrado correctamente.", "Alta completada")
    await router.push({ name: "catalogAdmins" })
  } catch (error) {
    if (error.isConflict) {
      submitError.value = `El ID de usuario (@${form.username}) ya está en uso. Por favor, elige uno diferente.`
    } else {
      submitError.value = error.message
    }
  }
}
</script>
