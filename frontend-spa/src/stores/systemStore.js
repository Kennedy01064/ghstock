import { computed, ref } from "vue"
import { defineStore } from "pinia"

import superadminApi from "@/api/superadmin.api"
import systemApi from "@/api/system.api"

export const useSystemStore = defineStore("system", () => {
  const publicStatus = ref(null)
  const settings = ref(null)
  const auditLogs = ref([])

  const isLoadingStatus = ref(false)
  const isLoadingSettings = ref(false)
  const isLoadingAudit = ref(false)
  const isSavingSettings = ref(false)
  const error = ref("")

  const isLocked = computed(() => Boolean(publicStatus.value?.lockdown_enabled))

  async function fetchPublicStatus() {
    isLoadingStatus.value = true
    error.value = ""

    try {
      const { data } = await systemApi.getPublicStatus()
      publicStatus.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoadingStatus.value = false
    }
  }

  async function fetchSettings() {
    isLoadingSettings.value = true
    error.value = ""

    try {
      const { data } = await superadminApi.getSettings()
      settings.value = data
      publicStatus.value = {
        lockdown_enabled: data.lockdown_enabled,
        message: data.lockdown_enabled ? "Sistema bloqueado. Contacte al desarrollador." : "",
        institutional_name: data.institutional_name,
        institutional_logo_url: data.institutional_logo_url,
      }
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      isLoadingSettings.value = false
    }
  }

  async function updateSettings(payload) {
    isSavingSettings.value = true
    error.value = ""

    try {
      const { data } = await superadminApi.updateSettings(payload)
      settings.value = data
      publicStatus.value = {
        lockdown_enabled: data.lockdown_enabled,
        message: data.lockdown_enabled ? "Sistema bloqueado. Contacte al desarrollador." : "",
        institutional_name: data.institutional_name,
        institutional_logo_url: data.institutional_logo_url,
      }
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      isSavingSettings.value = false
    }
  }

  async function fetchAuditLogs(params = {}) {
    isLoadingAudit.value = true
    error.value = ""

    try {
      const { data } = await superadminApi.getAuditLogs(params)
      auditLogs.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      isLoadingAudit.value = false
    }
  }

  return {
    publicStatus,
    settings,
    auditLogs,
    isLoadingStatus,
    isLoadingSettings,
    isLoadingAudit,
    isSavingSettings,
    isLocked,
    error,
    fetchPublicStatus,
    fetchSettings,
    updateSettings,
    fetchAuditLogs,
  }
})
