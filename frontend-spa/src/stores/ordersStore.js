import { ref } from "vue"
import { defineStore } from "pinia"

import apiClient from "@/utils/apiClient"

export const useOrdersStore = defineStore("orders", () => {
  const orders = ref([])
  const currentOrder = ref(null)
  const isLoading = ref(false)
  const submitLoading = ref(false)
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
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/orders/", { building_id: buildingId })
      currentOrder.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function addItem(orderId, payload) {
    submitLoading.value = true
    error.value = ""

    try {
      await apiClient.post(`/orders/${orderId}/items`, payload)
      return await fetchOrder(orderId)
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function removeItem(orderId, itemId) {
    submitLoading.value = true
    error.value = ""

    try {
      await apiClient.delete(`/orders/${orderId}/items/${itemId}`)
      return await fetchOrder(orderId)
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function updateItem(orderId, itemId, payload) {
    submitLoading.value = true
    error.value = ""

    try {
      await apiClient.post(`/orders/${orderId}/items/${itemId}/update`, payload)
      return await fetchOrder(orderId)
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function updateOrderStatus(orderId, action) {
    submitLoading.value = true
    error.value = ""

    try {
      await apiClient.post(`/orders/${orderId}/${action}`)
      return await fetchOrder(orderId)
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  return {
    orders,
    currentOrder,
    isLoading,
    submitLoading,
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
