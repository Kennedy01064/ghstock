import apiClient from "@/utils/apiClient"

export default {
  getAll(query = "") {
    return apiClient.get("/catalog/all", {
      params: query ? { q: query } : {},
    })
  },

  getById(id) {
    return apiClient.get(`/catalog/${id}`)
  },

  create(payload) {
    return apiClient.post("/catalog/", payload)
  },

  update(id, payload) {
    return apiClient.put(`/catalog/${id}`, payload)
  },

  toggleStatus(id) {
    return apiClient.patch(`/catalog/${id}/toggle`)
  },

  importCsv(file) {
    const formData = new FormData()
    formData.append("file", file)
    return apiClient.post("/catalog/import-csv", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 120000,
    })
  },

  getUploads() {
    return apiClient.get("/catalog/uploads")
  },

  deleteUpload(id) {
    return apiClient.delete(`/catalog/uploads/${id}`)
  },

  preview(url) {
    return apiClient.post("/catalog/preview", null, {
      params: { url },
    })
  },

  sync(id) {
    return apiClient.put(`/catalog/${id}/sync`)
  },
}
