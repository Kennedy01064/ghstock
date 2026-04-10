import { ref } from "vue"
import { defineStore } from "pinia"
import usersApi from "@/api/users.api"

export const useUserStore = defineStore("users", () => {
  const users = ref([])
  const currentUser = ref(null)
  
  const isLoading = ref(false)
  const isSubmitting = ref(false)
  const isDeleting = ref(false)
  const error = ref("")

  async function fetchUsers(role = "", options = {}) {
    isLoading.value = true
    error.value = ""
    try {
      const { data } = await usersApi.list(role, options)
      users.value = data
      return data
    } catch (err) {
      error.value = err.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchUser(id) {
    isLoading.value = true
    error.value = ""
    try {
      const { data } = await usersApi.getById(id)
      currentUser.value = data
      return data
    } catch (err) {
      error.value = err.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function createUser(payload) {
    if (isSubmitting.value) return
    isSubmitting.value = true
    error.value = ""
    try {
      const { data } = await usersApi.create(payload)
      users.value = [data, ...users.value]
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isSubmitting.value = false
    }
  }

  async function updateUser(id, payload, options = {}) {
    if (isSubmitting.value) return
    isSubmitting.value = true
    error.value = ""
    try {
      const params = {}
      if (Array.isArray(options.buildingIds)) params.building_ids = options.buildingIds
      if (options.clearBuildings) params.clear_buildings = true

      const { data } = await usersApi.update(id, payload, params)
      currentUser.value = data
      users.value = users.value.map(u => u.id === data.id ? data : u)
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isSubmitting.value = false
    }
  }

  async function deleteUser(id) {
    if (isDeleting.value) return
    isDeleting.value = true
    error.value = ""
    try {
      await usersApi.delete(id)
      users.value = users.value.filter(u => u.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isDeleting.value = false
    }
  }

  async function toggleUserActive(id) {
    if (isSubmitting.value) return
    isSubmitting.value = true
    error.value = ""
    try {
      const { data } = await usersApi.toggleActive(id)
      currentUser.value = data
      users.value = users.value.map((user) => (user.id === data.id ? data : user))
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isSubmitting.value = false
    }
  }

  return {
    users,
    currentUser,
    isLoading,
    isSubmitting,
    isDeleting,
    error,
    fetchUsers,
    fetchUser,
    createUser,
    updateUser,
    toggleUserActive,
    deleteUser
  }
})
