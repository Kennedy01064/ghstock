<template>
  <section class="min-h-screen flex items-center justify-center px-6 py-6">
    <div class="w-full max-w-sm animate-in fade-in zoom-in duration-700">
      <div class="text-center mb-5 flex flex-col items-center group">
        <span class="flex h-20 w-20 items-center justify-center mb-4 rounded-full border border-white/10 bg-white/[0.03] shadow-2xl transition-transform group-hover:scale-105 duration-500">
          <img :src="logoUrl" alt="Grupo Hernandez" class="h-12 w-12 object-contain drop-shadow-2xl" />
        </span>
        <h1 class="text-2xl font-display font-black text-white tracking-[-0.05em] leading-none mb-1 uppercase">Grupo Hernandez</h1>
        <div class="flex items-center gap-3">
          <div class="h-px w-8 bg-amber/30"></div>
          <p class="text-[0.65rem] font-black text-amber uppercase tracking-[0.3em]">Gestion de Inventario</p>
          <div class="h-px w-8 bg-amber/30"></div>
        </div>
      </div>

      <div class="relative group">
        <div class="absolute -inset-1 bg-gradient-to-r from-amber/20 to-transparent rounded-[2.5rem] blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
        <div class="relative bg-navy-accent/20 backdrop-blur-3xl rounded-[2.5rem] border border-white/10 overflow-hidden shadow-2xl">
          <div class="px-8 pt-8 pb-2">
            <h2 class="text-xl font-black text-white uppercase tracking-tight">Acceso Institucional</h2>
            <p class="text-[10px] font-medium text-text-muted mt-2 uppercase tracking-widest">Ingrese sus credenciales de servicio</p>
          </div>

          <form class="px-8 py-6 space-y-5" @submit.prevent="handleLogin">
            <div class="space-y-1">
              <label class="label-premium">Identificador Unico</label>
              <div class="relative group/input">
                <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none z-10">
                  <svg class="w-4 h-4 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                </div>
                <input data-testid="login-username" v-model="form.username" type="text" autocomplete="username" placeholder="Nombre de Usuario" class="input-field !pl-14 !bg-white/[0.05] !text-white" />
              </div>
            </div>

            <div class="space-y-1">
              <label class="label-premium">Clave de Seguridad</label>
              <div class="relative group/input">
                <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none z-10">
                  <svg class="w-4 h-4 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                </div>
                <input data-testid="login-password" v-model="form.password" :type="showPassword ? 'text' : 'password'" autocomplete="current-password" placeholder="Password Institucional" class="input-field !pl-14 !pr-14 !bg-white/[0.05] !text-white" />
                <button type="button" class="absolute inset-y-0 right-0 pr-5 flex items-center text-white/30 hover:text-amber transition-colors z-10" @click="showPassword = !showPassword">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                </button>
              </div>
            </div>

            <label class="flex items-center cursor-pointer group/check pl-1">
              <input v-model="form.remember" type="checkbox" class="peer hidden" />
              <div class="w-5 h-5 rounded-lg border-2 border-white/10 bg-white/5 flex items-center justify-center transition-all peer-checked:bg-amber peer-checked:border-amber group-hover/check:border-white/20">
                <svg class="w-3 h-3 text-navy-deep opacity-0 peer-checked:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M5 13l4 4L19 7" /></svg>
              </div>
              <span class="ml-3 text-[10px] font-bold text-text-muted uppercase tracking-widest group-hover/check:text-white transition-colors">Recordar sesion</span>
            </label>

            <div v-if="authStore.error" data-testid="login-error" class="rounded-2xl border border-rose-500/20 bg-rose-500/10 px-4 py-3 text-[11px] uppercase tracking-[0.18em] text-rose-200">
              {{ authStore.error }}
            </div>

            <button data-testid="login-submit" type="submit" class="btn btn-primary w-full !min-h-[56px] !px-6 !tracking-[0.15em] !shadow-xl !shadow-amber/20 active:scale-[0.98] mt-2" :disabled="authStore.isLoading">
              {{ authStore.isLoading ? "Validando..." : "Entrar al Sistema" }}
            </button>
          </form>

          <div class="px-8 pb-6 text-center">
            <p class="text-[9px] text-white/20 font-black uppercase tracking-[0.2em]">Acceso Restringido ? Grupo Hernandez S.A.C.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import { useAuthStore } from "@/stores/authStore"
import { useUiStore } from "@/stores/uiStore"
import { logoUrl } from "@/utils/formatters"
import { dashboardRouteForRole } from "@/utils/roleRoutes"

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUiStore()
const showPassword = ref(false)
const form = reactive({ username: "", password: "", remember: true })

async function handleLogin() {
  try {
    const user = await authStore.login({
      username: form.username,
      password: form.password,
      remember: form.remember,
    })

    uiStore.success(`Sesion iniciada como ${user.name || user.username}.`, "Acceso concedido")

    const redirect = typeof route.query.redirect === "string" ? route.query.redirect : null

    if (redirect) {
      router.push(redirect)
      return
    }

    router.push(dashboardRouteForRole(user.role))
  } catch (error) {
    uiStore.error(error.message, "Acceso denegado")
  }
}
</script>
