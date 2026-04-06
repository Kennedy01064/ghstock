import { ref } from "vue"
import { defineStore } from "pinia"

import apiClient from "@/utils/apiClient"

export const useCatalogStore = defineStore("catalog", () => {
  const products = ref([])
  const currentProduct = ref(null)
  const admins = ref([])
  const currentAdmin = ref(null)
  const buildings = ref([])
  const unassignedBuildings = ref([])
  const currentBuilding = ref(null)
  const csvUploads = ref([])
  const lastCsvUpload = ref(null)
  const isLoading = ref(false)
  const submitLoading = ref(false)
  const error = ref("")

  async function fetchProducts(query = "") {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/catalog/all", {
        params: query ? { q: query } : {},
      })
      products.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchProduct(productId) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get(`/catalog/${productId}`)
      currentProduct.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function createProduct(payload) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/catalog/", payload)
      products.value = [data, ...products.value]
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function updateProduct(productId, payload) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.put(`/catalog/${productId}`, payload)
      currentProduct.value = data
      products.value = products.value.map((product) => (product.id === data.id ? data : product))
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function toggleProduct(productId) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.patch(`/catalog/${productId}/toggle`)
      products.value = products.value.map((product) => (product.id === data.id ? data : product))
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function uploadCsv(file) {
    submitLoading.value = true
    error.value = ""

    try {
      const formData = new FormData()
      formData.append("file", file)
      const { data } = await apiClient.post("/catalog/import-csv", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      lastCsvUpload.value = data
      await fetchCsvUploads()
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function fetchAdmins(role = "") {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/users/", {
        params: role ? { role } : {},
      })
      admins.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchAdmin(adminId) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get(`/users/${adminId}`)
      currentAdmin.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function createAdmin(payload) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/users/", payload)
      admins.value = [data, ...admins.value]
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function updateAdmin(adminId, payload, options = {}) {
    submitLoading.value = true
    error.value = ""

    try {
      const params = {}
      if (Array.isArray(options.buildingIds)) {
        params.building_ids = options.buildingIds
      }
      if (options.clearBuildings) {
        params.clear_buildings = true
      }

      const { data } = await apiClient.put(`/users/${adminId}`, payload, { params })
      currentAdmin.value = data
      admins.value = admins.value.map((admin) => (admin.id === data.id ? data : admin))
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function deleteAdmin(adminId) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.delete(`/users/${adminId}`)
      admins.value = admins.value.filter((admin) => admin.id !== adminId)
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function fetchBuildings() {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/buildings/")
      buildings.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchBuilding(buildingId) {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get(`/buildings/${buildingId}`)
      currentBuilding.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchUnassignedBuildings() {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/buildings/unassigned")
      unassignedBuildings.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function createBuilding(payload) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/buildings/", payload)
      buildings.value = [data, ...buildings.value]
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function updateBuilding(buildingId, payload) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.put(`/buildings/${buildingId}`, payload)
      currentBuilding.value = data
      buildings.value = buildings.value.map((building) => (building.id === data.id ? data : building))
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function deleteBuilding(buildingId) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.delete(`/buildings/${buildingId}`)
      buildings.value = buildings.value.filter((building) => building.id !== buildingId)
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function assignBuildings(adminId, buildingIds) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/buildings/assign", {
        admin_id: adminId,
        building_ids: buildingIds,
      })
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function fetchCsvUploads() {
    isLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.get("/catalog/uploads")
      csvUploads.value = data
      return data
    } catch (requestError) {
      error.value = requestError.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function deleteCsvUpload(uploadId) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.delete(`/catalog/uploads/${uploadId}`)
      csvUploads.value = csvUploads.value.filter((upload) => upload.id !== uploadId)
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function previewProduct(sourceUrl) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.post("/catalog/preview", null, {
        params: { url: sourceUrl },
      })
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  async function syncProduct(productId) {
    submitLoading.value = true
    error.value = ""

    try {
      const { data } = await apiClient.put(`/catalog/${productId}/sync`)
      products.value = products.value.map((product) => (product.id === data.id ? data : product))
      if (currentProduct.value?.id === data.id) {
        currentProduct.value = data
      }
      return data
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      submitLoading.value = false
    }
  }

  return {
    products,
    currentProduct,
    admins,
    currentAdmin,
    buildings,
    currentBuilding,
    unassignedBuildings,
    csvUploads,
    lastCsvUpload,
    isLoading,
    submitLoading,
    error,
    fetchProducts,
    fetchProduct,
    createProduct,
    updateProduct,
    toggleProduct,
    uploadCsv,
    fetchAdmins,
    fetchAdmin,
    createAdmin,
    updateAdmin,
    deleteAdmin,
    fetchBuildings,
    fetchBuilding,
    fetchUnassignedBuildings,
    createBuilding,
    updateBuilding,
    deleteBuilding,
    assignBuildings,
    fetchCsvUploads,
    deleteCsvUpload,
    previewProduct,
    syncProduct,
  }
})
