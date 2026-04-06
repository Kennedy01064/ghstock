import { ref } from "vue"
import { defineStore } from "pinia"

import apiClient from "@/utils/apiClient"

export const useDispatchStore = defineStore("dispatch", () => {
  const pendingOrders = ref([])
  const history = ref({ batches: [], orders: [] })
  const currentBatch = ref(null)
  const currentPicking = ref(null)
  const purchases = ref([])
  const currentPurchase = ref(null)
  const isLoading = ref(false)
  const submitLoading = ref(false)
  const error = ref("")

  async function fetchPendingOrders() {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/dispatch/pending-orders")
      pendingOrders.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function consolidateOrders(orderIds) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/dispatch/consolidate", orderIds)
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function fetchHistory() {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/dispatch/history")
      history.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchBatchDetail(batchId) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get(`/dispatch/batch/${batchId}`)
      currentBatch.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchPicking(batchId) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get(`/dispatch/batch/${batchId}/picking`)
      currentPicking.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function confirmBatch(batchId) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post(`/dispatch/batch/${batchId}/confirm`)
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function rejectOrder(batchId, orderId, rejectionNote = "") {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post(`/dispatch/batch/${batchId}/reject-order/${orderId}`, null, {
        params: rejectionNote ? { rejection_note: rejectionNote } : {},
      })
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function exportBatch(batchId, kind = "consolidated") {
    submitLoading.value = true
    error.value = ""

    const endpoint =
      kind === "buildings"
        ? `/dispatch/batch/${batchId}/export/buildings`
        : `/dispatch/batch/${batchId}/export/consolidated`

    try {
      const response = await apiClient.get(endpoint, { responseType: "blob" })
      const header = response.headers["content-disposition"] ?? ""
      const filenameMatch = header.match(/filename=([^;]+)/i)
      const fallback = kind === "buildings" ? `distribucion_edificios_lote_${batchId}.pdf` : `consolidado_lote_${batchId}.pdf`

      return {
        blob: response.data,
        filename: filenameMatch?.[1]?.replace(/"/g, "") ?? fallback,
      }
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function fetchPurchases() {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/dispatch/purchases/")
      purchases.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchPurchase(purchaseId) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get(`/dispatch/purchases/${purchaseId}`)
      currentPurchase.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function createPurchase(payload) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/dispatch/purchases/", payload)
      purchases.value = [data, ...purchases.value]
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  return {
    pendingOrders,
    history,
    currentBatch,
    currentPicking,
    purchases,
    currentPurchase,
    isLoading,
    submitLoading,
    error,
    fetchPendingOrders,
    consolidateOrders,
    fetchHistory,
    fetchBatchDetail,
    fetchPicking,
    confirmBatch,
    rejectOrder,
    exportBatch,
    fetchPurchases,
    fetchPurchase,
    createPurchase,
  }
})
