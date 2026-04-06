import { computed, ref } from "vue"
import { defineStore } from "pinia"

import apiClient from "@/utils/apiClient"
import { clearAuthSession, getStoredToken, persistAuthSession, readAuthSession } from "@/utils/authSession"
import { dashboardRouteForRole } from "@/utils/roleRoutes"

export const useAuthStore = defineStore("auth", () => {
  const token = ref("")
  const user = ref(null)
  const rememberSession = ref(true)
  const isInitializing = ref(false)
  const isLoading = ref(false)
  const error = ref("")

  const isAuthenticated = computed(() => Boolean(token.value))
  const currentRole = computed(() => user.value?.role ?? "admin")
  const isManagement = computed(() => ["superadmin", "manager"].includes(currentRole.value))
  const homeRoute = computed(() => dashboardRouteForRole(currentRole.value))

  function hydrateFromStorage() {
    const session = readAuthSession()
    token.value = session.token ?? ""
    user.value = session.user ?? null
    rememberSession.value = Boolean(window.localStorage.getItem("stock-spa-auth"))
  }

  function setSession(sessionToken, sessionUser, remember = true) {
    token.value = sessionToken ?? ""
    user.value = sessionUser ?? null
    rememberSession.value = remember
    persistAuthSession(token.value, user.value, rememberSession.value)
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
    persistAuthSession(token.value, user.value, rememberSession.value)
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
    } catch {
      clearSession()
    } finally {
      isInitializing.value = false
    }
  }

  async function login({ username, password, remember = true }) {
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

      setSession(data.access_token, null, remember)
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
    clearSession()
  }

  if (getStoredToken() && !token.value) {
    hydrateFromStorage()
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
    fetchCurrentUser,
    setSession,
    clearSession,
  }
})
