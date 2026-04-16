<template>
  <header class="sticky top-0 z-50 border-b border-white/10 transition-colors duration-300" style="background: #0f172a; backdrop-filter: blur(12px);">
    <div class="mx-auto flex w-full max-w-[1320px] items-center gap-4 px-5 py-4 md:px-8 xl:px-10">
      <RouterLink :to="dashboardRoute" class="group flex min-w-0 items-center gap-3 pr-2">
        <span class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-white/20 bg-white/10 transition duration-200">
          <img :src="logoUrl" alt="Logo Grupo Hernandez" class="h-10 w-auto object-contain" />
        </span>
        <span class="min-w-0">
          <span class="block truncate font-display text-[1.1rem] md:text-[1.2rem] font-extrabold tracking-[-0.04em] text-white leading-none mb-1">
            Grupo Hernandez
          </span>
          <span class="block truncate text-[0.64rem] md:text-[0.68rem] font-semibold uppercase tracking-[0.18em] text-slate-400 leading-none">
            Administracion de edificios
          </span>
        </span>
      </RouterLink>

      <div v-if="showAuthenticatedShell" class="flex flex-1 items-center justify-end gap-5">
        <nav class="hidden lg:flex items-center gap-7 xl:gap-9">
          <RouterLink
            :to="dashboardRoute"
            class="relative inline-flex items-center py-2 text-[0.88rem] font-bold tracking-[-0.01em] transition duration-200"
            :class="desktopLinkClass('dashboard')"
          >
            Dashboard
          </RouterLink>

          <template v-if="showManagementNavigation">
            <RouterLink
              :to="{ name: 'dispatchPending' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-semibold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('dispatchPending')"
            >
              Despacho
            </RouterLink>
            <RouterLink
              :to="{ name: 'dispatchHistory' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-semibold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('dispatchHistory')"
            >
              Historial
            </RouterLink>
            <RouterLink
              :to="{ name: 'dispatchPurchases' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-semibold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('dispatchPurchases')"
            >
              Compras
            </RouterLink>
            <RouterLink
              :to="{ name: 'catalogWarehouse' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-semibold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('catalogWarehouse')"
            >
              Almacen
            </RouterLink>
            <RouterLink
              :to="{ name: 'catalogBuildings' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-semibold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('catalogBuildings', 'text-amber-soft hover:text-amber')"
            >
              Edificios
            </RouterLink>
            <RouterLink
              v-if="showManagementNavigation"
              :to="{ name: 'catalogAdmins' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-semibold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('catalogAdmins', 'text-amber-soft hover:text-amber')"
            >
              Usuarios
            </RouterLink>
            <RouterLink
              v-if="currentUser.role === 'superadmin'"
              :to="{ name: 'superadminControl' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-semibold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('superadminControl', 'text-rose-300 hover:text-rose-200')"
            >
              Control SA
            </RouterLink>
            <a
              v-if="showApiDocs"
              :href="apiDocsUrl"
              target="_blank"
              rel="noreferrer"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-bold tracking-[-0.01em] text-emerald-400 hover:text-emerald-300 transition duration-200"
            >
              Docs API
            </a>
          </template>

          <template v-else>
            <RouterLink
              :to="{ name: 'ordersMyOrders' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-bold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('ordersMyOrders')"
            >
              Mis Pedidos
            </RouterLink>
            <RouterLink
              :to="{ name: 'ordersMyInventory' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-bold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('ordersMyInventory')"
            >
              Inventario
            </RouterLink>
            <RouterLink
              :to="{ name: 'ordersConsumption' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-bold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('ordersConsumption')"
            >
              Consumos
            </RouterLink>
            <RouterLink
              :to="{ name: 'ordersBuildings' }"
              class="relative inline-flex items-center py-2 text-[0.88rem] font-bold tracking-[-0.01em] transition duration-200"
              :class="desktopLinkClass('ordersBuildings', 'text-amber-soft hover:text-amber')"
            >
              Nueva Solicitud
            </RouterLink>
          </template>
        </nav>

        <div class="flex items-center gap-4">
          <div
            v-if="currentUser.role === 'superadmin' && systemStore.publicStatus"
            class="hidden xl:flex items-center gap-2 rounded-full border px-3 py-2 text-[9px] font-black uppercase tracking-[0.18em]"
            :class="systemStore.isLocked ? 'border-rose-400/20 bg-rose-500/10 text-rose-300' : 'border-emerald-400/20 bg-emerald-500/10 text-emerald-300'"
          >
            <span class="h-1.5 w-1.5 rounded-full" :class="systemStore.isLocked ? 'bg-rose-300' : 'bg-emerald-300'"></span>
            {{ systemStore.isLocked ? "Bloqueo activo" : "Sistema activo" }}
          </div>
          <button
            v-if="showRoleToggle"
            type="button"
            class="hidden md:flex items-center justify-center h-10 px-5 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all shadow-lg group"
            :class="viewAsAdmin ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20 hover:bg-rose-500/20 shadow-rose-500/5' : 'bg-amber/10 text-amber border border-amber/20 hover:bg-amber/20 shadow-amber/5'"
            :title="viewAsAdmin ? 'Cerrar vista de administrador' : 'Ver como administrador'"
            @click="toggleRoleView"
          >
            <svg class="w-4 h-4 mr-2 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2.5"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
              />
            </svg>
            {{ viewAsAdmin ? "Volver a Superadmin" : "Ver como Admin" }}
          </button>

          <div class="hidden md:flex items-center gap-4 pl-5 border-l border-white/20">
            <div class="flex flex-col items-start">
              <span data-testid="navbar-user-name" class="text-[13px] font-black text-white leading-none mb-1 tracking-tight">{{ displayName }}</span>
              <span class="text-[9px] font-black text-amber tracking-[0.15em] uppercase leading-none opacity-80">{{ displayRole }}</span>
              <span v-if="viewAsAdmin" class="mt-1 text-[8px] font-black text-rose-300 tracking-[0.2em] uppercase leading-none opacity-90">Vista Admin</span>
            </div>
            <div
              class="w-10 h-10 bg-amber ring-4 ring-white/10 rounded-full flex items-center justify-center text-sm font-black text-navy-deep uppercase shadow-xl transition-transform hover:scale-105"
            >
              {{ displayInitial }}
            </div>
          </div>

          <button
            type="button"
            class="flex items-center justify-center w-10 h-10 rounded-full text-white/40 bg-white/10 border border-white/20 hover:text-rose-400 hover:border-rose-400/40 transition-all"
            title="Cerrar Sesion"
            @click="handleLogout"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>

          <button
            type="button"
            class="lg:hidden flex items-center justify-center w-12 h-12 rounded-full border border-white/20 bg-white/10 text-white/70"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div v-if="showAuthenticatedShell && mobileMenuOpen" id="mobile-menu" class="xl:hidden border-t border-white/10 bg-slate-900 shadow-2xl">
      <nav class="px-4 py-4 flex flex-col gap-1.5">
        <RouterLink :to="dashboardRoute" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-300 hover:text-white hover:bg-white/10 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Dashboard
        </RouterLink>

        <template v-if="showManagementNavigation">
          <RouterLink :to="{ name: 'dispatchPending' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-300 hover:text-white hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
            Despacho
          </RouterLink>
          <RouterLink :to="{ name: 'dispatchHistory' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-300 hover:text-white hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Historial
          </RouterLink>
          <RouterLink :to="{ name: 'dispatchPurchases' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-300 hover:text-white hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            Compras Directas
          </RouterLink>
          <RouterLink :to="{ name: 'catalogWarehouse' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-300 hover:text-white hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Almacen
          </RouterLink>
          <RouterLink :to="{ name: 'catalogUploadCsv' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-300 hover:text-white hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Catalogo CSV
          </RouterLink>
          <RouterLink :to="{ name: 'catalogBuildings' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-amber-soft hover:text-amber hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21h18M5 21V5a2 2 0 012-2h10a2 2 0 012 2v16m-14 0h14" />
            </svg>
            Edificios
          </RouterLink>
          <RouterLink v-if="currentUser.role === 'superadmin'" :to="{ name: 'superadminControl' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-rose-400 hover:text-rose-300 hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8a4 4 0 00-4 4v3a2 2 0 002 2h4a2 2 0 002-2v-3a4 4 0 00-4-4zm0 0V5m0 14v-2m7-5h-2M7 12H5" />
            </svg>
            Control SA
          </RouterLink>
          <RouterLink v-if="showManagementNavigation" :to="{ name: 'catalogAdmins' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-amber-soft hover:text-amber hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            Usuarios
          </RouterLink>
        </template>

        <template v-else>
          <RouterLink :to="{ name: 'ordersMyOrders' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-300 hover:text-white hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            Mis Pedidos
          </RouterLink>
          <RouterLink :to="{ name: 'ordersMyInventory' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-300 hover:text-white hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            Inventario Local
          </RouterLink>
          <RouterLink :to="{ name: 'ordersConsumption' }" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-300 hover:text-white hover:bg-white/10 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Consumos
          </RouterLink>
        </template>

        <button
          v-if="showRoleToggle"
          type="button"
          class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold transition-colors"
          :class="viewAsAdmin ? 'text-red-400 hover:bg-red-500/10' : 'text-amber hover:bg-amber/10'"
          @click="toggleRoleView"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          {{ viewAsAdmin ? "Volver a Superadmin" : "Ver como Admin" }}
        </button>

        <div class="mt-2 pt-4 border-t border-white/10 flex items-center gap-3 px-2">
          <div class="w-10 h-10 bg-amber rounded-xl flex items-center justify-center text-sm font-black text-navy-deep uppercase shadow-md">
            {{ displayInitial }}
          </div>
          <div>
            <p class="text-sm font-bold text-white leading-none">{{ mobileDisplayName }}</p>
            <p class="text-xs font-bold text-amber-soft uppercase mt-1 tracking-widest">{{ displayRole }}</p>
            <p v-if="viewAsAdmin" class="text-[10px] font-black text-rose-300 uppercase mt-1 tracking-widest">Vista Admin</p>
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { computed, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import { useAuthStore } from "@/stores/authStore"
import { useSystemStore } from "@/stores/systemStore"
import { useUiStore } from "@/stores/uiStore"
import { logoUrl, titleCase } from "@/utils/formatters"
import { dashboardRouteForRole } from "@/utils/roleRoutes"

const apiDocsUrl = import.meta.env.VITE_API_DOCS_URL ?? "http://127.0.0.1:8000/docs"
const adminViewStorageKey = "gh_view_as_admin"

const authStore = useAuthStore()
const systemStore = useSystemStore()
const uiStore = useUiStore()
const route = useRoute()
const router = useRouter()
const mobileMenuOpen = ref(false)
const viewAsAdmin = ref(sessionStorage.getItem(adminViewStorageKey) === "true")

const currentUser = computed(() => authStore.user ?? { name: "Usuario", username: "usuario", role: "admin" })

const accountRole = computed(() => currentUser.value.role ?? "admin")
const effectiveRole = computed(() => {
  if (viewAsAdmin.value && currentUser.value.role === "superadmin") {
    return "admin"
  }

  return currentUser.value.role ?? "admin"
})

const dashboardRoute = computed(() => dashboardRouteForRole(effectiveRole.value))
const accountDashboardRoute = computed(() => dashboardRouteForRole(accountRole.value))
const showAuthenticatedShell = computed(() => authStore.isAuthenticated)
const showManagementNavigation = computed(() => ["superadmin", "manager"].includes(effectiveRole.value))
const showRoleToggle = computed(() => currentUser.value.role === "superadmin")
const showApiDocs = computed(() => currentUser.value.role === "superadmin" && showManagementNavigation.value)
const displayRole = computed(() => accountRole.value)

const displayName = computed(() => {
  const source = currentUser.value.name || currentUser.value.username || "Usuario"
  return titleCase(source)
})

const mobileDisplayName = computed(() => {
  const source = currentUser.value.name || currentUser.value.username || "Usuario"
  const firstToken = source.trim().split(/\s+/)[0] ?? source
  return capitalize(firstToken)
})

const displayInitial = computed(() => {
  const source = currentUser.value.name || currentUser.value.username || "U"
  return source.trim().charAt(0).toUpperCase()
})

watch(
  () => route.fullPath,
  () => {
    mobileMenuOpen.value = false
  },
)

watch(viewAsAdmin, (value) => {
  sessionStorage.setItem(adminViewStorageKey, String(value))
})

function desktopLinkClass(name, inactiveClass = "text-slate-400 hover:text-white") {
  return isActiveRoute(name)
    ? "text-white after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-amber"
    : inactiveClass
}

function toggleRoleView() {
  viewAsAdmin.value = !viewAsAdmin.value
  router.push(viewAsAdmin.value ? { name: "dashboardAdmin" } : accountDashboardRoute.value)
}

function handleLogout() {
  mobileMenuOpen.value = false
  viewAsAdmin.value = false
  authStore.logout()
  uiStore.info("La sesion actual se cerro correctamente.", "Sesion finalizada")
  router.push({ name: "login" })
}

function capitalize(value) {
  if (!value) {
    return ""
  }

  return value.charAt(0).toUpperCase() + value.slice(1).toLowerCase()
}

function isActiveRoute(name) {
  const routeName = String(route.name ?? "")
  const groups = {
    dashboard: ["dashboard", "dashboardAdmin", "dashboardManager"],
    dispatchPending: ["dispatchPending", "dispatchBatchDetail", "dispatchPicking"],
    dispatchHistory: ["dispatchHistory"],
    dispatchPurchases: ["dispatchPurchases", "dispatchPurchaseCreate", "dispatchPurchaseDetail"],
    catalogWarehouse: ["catalogWarehouse", "catalogProductCreate", "catalogProductEdit", "catalogUploadCsv"],
    catalogBuildings: ["catalogBuildings", "catalogBuildingCreate", "catalogBuildingEdit", "catalogAssignBuilding"],
    catalogAdmins: ["catalogAdmins", "catalogAdminCreate", "catalogAdminEdit"],
    superadminControl: ["superadminControl"],
    ordersMyOrders: ["ordersMyOrders", "ordersOrderDetail"],
    ordersMyInventory: ["ordersMyInventory", "ordersAddInventory"],
    ordersConsumption: ["ordersConsumption"],
    ordersBuildings: ["ordersBuildings"],
  }

  return (groups[name] ?? [name]).includes(routeName)
}
</script>
