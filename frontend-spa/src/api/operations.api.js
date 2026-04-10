import apiClient from "@/utils/apiClient"

export default {
  getOrderDeadline() {
    return apiClient.get("/operations/order-deadline")
  },

  updateOrderDeadline(payload) {
    return apiClient.put("/operations/order-deadline", payload)
  },
}
