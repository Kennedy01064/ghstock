import { ref } from "vue"
import { defineStore } from "pinia"

import apiClient from "@/utils/apiClient"

export const useOrdersStore = defineStore("orders", () => {
  const orders = ref([])
  const currentOrder = ref(null)
  const isLoading = ref(false)
  const isCreatingOrder = ref(false)
  const isUpdatingItem = ref(false)
  const isSubmittingOrder = ref(false)
  const isReopeningOrder = ref(false)
  const isCancellingOrder = ref(false)
  const isReceivingOrder = ref(false)
  const error = ref("")

  async function fetchOrders(params = {}) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/orders/", { params })
      orders.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchOrder(orderId) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get(`/orders/${orderId}`)
      currentOrder.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function createOrder(buildingId) {
    if (isCreatingOrder.value) return
    isCreatingOrder.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/orders/", { building_id: buildingId })
      currentOrder.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      isCreatingOrder.value = false
    }
  }

  async function addItem(orderId, payload) {
    if (isUpdatingItem.value) return
    isUpdatingItem.value = true
    error.value = ""

    try {
      await apiClient.post(`/orders/${orderId}/items`, payload)
      return await fetchOrder(orderId)
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      isUpdatingItem.value = false
    }
  }

  async function removeItem(orderId, itemId) {
    if (isUpdatingItem.value) return
    isUpdatingItem.value = true
    error.value = ""

    try {
      await apiClient.delete(`/orders/${orderId}/items/${itemId}`)
      return await fetchOrder(orderId)
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      isUpdatingItem.value = false
    }
  }

  async function updateItem(orderId, itemId, payload) {
    if (isUpdatingItem.value) return
    isUpdatingItem.value = true
    error.value = ""

    try {
      await apiClient.post(`/orders/${orderId}/items/${itemId}/update`, payload)
      return await fetchOrder(orderId)
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      isUpdatingItem.value = false
    }
  }

  async function updateOrderStatus(orderId, action) {
    const stateMap = {
      submit: isSubmittingOrder,
      reopen: isReopeningOrder,
      cancel: isCancellingOrder,
      receive: isReceivingOrder,
    }
    const state = stateMap[action]
    if (state?.value) return
    if (state) state.value = true
    error.value = ""

    try {
      await apiClient.post(`/orders/${orderId}/${action}`)
      return await fetchOrder(orderId)
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      if (state) state.value = false
    }
  }

  return {
    orders,
    currentOrder,
    isLoading,
    isCreatingOrder,
    isUpdatingItem,
    isSubmittingOrder,
    isReopeningOrder,
    isCancellingOrder,
    isReceivingOrder,
    error,
    fetchOrders,
    fetchOrder,
    createOrder,
    addItem,
    removeItem,
    updateItem,
    updateOrderStatus,
  }
})
