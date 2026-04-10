import router from "@/router"
import { computed, ref } from "vue"
import { defineStore } from "pinia"

import apiClient from "@/utils/apiClient"
import { onLockdown, onUnauthorized } from "@/utils/authBus"
import { clearAuthSession, getStoredToken, getStoredRefreshToken, persistAuthSession, readAuthSession } from "@/utils/authSession"
import { dashboardRouteForRole } from "@/utils/roleRoutes"

export const useAuthStore = defineStore("auth", () => {
  const token = ref("")
  const user = ref(null)
  const rememberSession = ref(true)
  const isInitializing = ref(false)
  const isLoading = ref(false)
  const isLoggingOut = ref(false)
  const error = ref("")

  const isAuthenticated = computed(() => Boolean(token.value))
  // currentRole is null until /auth/me resolves — prevents false role assumptions during bootstrap.
  const currentRole = computed(() => user.value?.role ?? null)
  const isManagement = computed(() => ["superadmin", "manager"].includes(currentRole.value))
  const homeRoute = computed(() => dashboardRouteForRole(currentRole.value))

  function hydrateFromStorage() {
    const session = readAuthSession()
    token.value = session.token ?? ""
    user.value = session.user ?? null
    rememberSession.value = Boolean(window.localStorage.getItem("stock-spa-auth"))
  }

  function setSession(sessionToken, sessionUser, remember = true, refreshToken = "") {
    token.value = sessionToken ?? ""
    user.value = sessionUser ?? null
    rememberSession.value = remember
    persistAuthSession(token.value, user.value, rememberSession.value, refreshToken)
  }

  function clearSession() {
    token.value = ""
    user.value = null
    error.value = ""
    clearAuthSession()
  }

  async function fetchCurrentUser() {
    const { data } = await apiClient.get("/auth/me")
    user.value = data
    persistAuthSession(token.value, user.value, rememberSession.value, getStoredRefreshToken())
    return data
  }

  async function initialize() {
    if (isInitializing.value) {
      return
    }

    isInitializing.value = true

    try {
      hydrateFromStorage()

      if (!token.value) {
        return
      }

      await fetchCurrentUser()
    } catch (requestError) {
      if (requestError?.status === 423) {
        token.value = ""
        user.value = null
        clearAuthSession()
      } else {
        clearSession()
      }
    } finally {
      isInitializing.value = false
    }
  }

  async function login({ username, password, remember = true }) {
    if (isLoading.value) return
    isLoading.value = true
    error.value = ""

    try {
      const credentials = new URLSearchParams()
      credentials.set("username", username)
      credentials.set("password", password)

      const { data } = await apiClient.post("/auth/login", credentials, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })

      setSession(data.access_token, null, remember, data.refresh_token ?? "")
      const currentUser = await fetchCurrentUser()

      return currentUser
    } catch (requestError) {
      clearSession()
      error.value = requestError.message
      throw requestError
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    if (isLoggingOut.value) return
    isLoggingOut.value = true
    try {
      clearSession()
    } finally {
      isLoggingOut.value = false
    }
  }

  if (getStoredToken() && !token.value) {
    hydrateFromStorage()
  }

  onUnauthorized.value = () => {
    const hadToken = Boolean(token.value)
    
    // Clear reactive state
    token.value = ""
    user.value = null
    
    if (hadToken) {
      error.value = "Tu sesión ha expirado. Por favor ingresa nuevamente."
      
      const currentRoute = router.currentRoute.value
      // Avoid redundant redirect if already on login page
      if (currentRoute?.name !== "login") {
        const query = currentRoute?.meta?.requiresAuth ? { redirect: currentRoute.fullPath } : {}
        router.push({ name: "login", query })
      }
    }
  }

  onLockdown.value = (message = "Sistema bloqueado. Contacte al desarrollador.") => {
    const hadToken = Boolean(token.value)

    token.value = ""
    user.value = null
    error.value = message

    if (hadToken) {
      const currentRoute = router.currentRoute.value
      if (currentRoute?.name !== "login") {
        const query = { locked: "1" }
        router.push({ name: "login", query })
      }
    }
  }

  return {
    token,
    user,
    error,
    isLoading,
    isInitializing,
    isAuthenticated,
    currentRole,
    isManagement,
    homeRoute,
    initialize,
    login,
    logout,
    isLoggingOut,
    fetchCurrentUser,
    setSession,
    clearSession,
  }
})
