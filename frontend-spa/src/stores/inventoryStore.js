import { ref } from "vue"
import { defineStore } from "pinia"

import apiClient from "@/utils/apiClient"

export const useInventoryStore = defineStore("inventory", () => {
  const items = ref([])
  const consumptionRows = ref([])
  const isLoading = ref(false)
  const submitLoading = ref(false)
  const error = ref("")

  async function fetchInventory(buildingId) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/inventory/", {
        params: buildingId ? { building_id: buildingId } : {},
      })
      items.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function addInventory(payload) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/inventory/", payload)
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function consumeInventory(itemId, payload) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post(`/inventory/${itemId}/consume`, payload)
      items.value = items.value.map((item) => (item.id === data.id ? data : item))
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function adjustInventory(itemId, payload) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post(`/inventory/${itemId}/adjust`, payload)
      items.value = items.value.map((item) => (item.id === data.id ? data : item))
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function fetchConsumptionReport(buildingId) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/orders/consumption-report", {
        params: buildingId ? { building_id: buildingId } : {},
      })
      consumptionRows.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    items,
    consumptionRows,
    isLoading,
    submitLoading,
    error,
    fetchInventory,
    addInventory,
    consumeInventory,
    adjustInventory,
    fetchConsumptionReport,
  }
})
