import apiClient from "@/utils/apiClient"

export default {
  getMe() {
    return apiClient.get("/users/me")
  },

  list(role = "", options = {}) {
    const params = {}
    if (role) {
      params.role = role
    }
    if (options.includeInactive) {
      params.include_inactive = true
    }

    return apiClient.get("/users/", {
      params,
    })
  },

  getById(id) {
    return apiClient.get(`/users/${id}`)
  },

  create(payload) {
    return apiClient.post("/users/", payload)
  },

  update(id, payload, queryParams = {}) {
    return apiClient.put(`/users/${id}`, payload, {
      params: queryParams,
      paramsSerializer: {
        indexes: null,
      },
    })
  },

  toggleActive(id) {
    return apiClient.patch(`/users/${id}/toggle-active`)
  },

  delete(id) {
    return apiClient.delete(`/users/${id}`)
  },
}
