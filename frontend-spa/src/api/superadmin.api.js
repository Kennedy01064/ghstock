import apiClient from "@/utils/apiClient"

export default {
  getSettings() {
    return apiClient.get("/superadmin/settings")
  },

  updateSettings(payload) {
    return apiClient.put("/superadmin/settings", payload)
  },

  getAuditLogs(params = {}) {
    return apiClient.get("/superadmin/audit-logs", { params })
  },
}
