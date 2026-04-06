import { ref } from "vue"
import { defineStore } from "pinia"

import apiClient from "@/utils/apiClient"

export const useDashboardStore = defineStore("dashboard", () => {
  const superadminDashboard = ref(null)
  const managerDashboard = ref(null)
  const adminDashboard = ref(null)
  const isLoading = ref(false)
  const error = ref("")

  async function fetchSuperadminDashboard() {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/analytics/superadmin")
      superadminDashboard.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchManagerDashboard() {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/analytics/manager")
      managerDashboard.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchAdminDashboard() {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/analytics/admin")
      adminDashboard.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    superadminDashboard,
    managerDashboard,
    adminDashboard,
    isLoading,
    error,
    fetchSuperadminDashboard,
    fetchManagerDashboard,
    fetchAdminDashboard,
  }
})
