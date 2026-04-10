import apiClient from "@/utils/apiClient"

export default {
  getPublicStatus() {
    return apiClient.get("/auth/status")
  },
}
