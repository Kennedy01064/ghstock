import axios from "axios"

import { clearAuthSession, getStoredToken } from "@/utils/authSession"

export const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1"

const apiClient = axios.create({
  baseURL: apiBaseUrl,
  headers: {
    Accept: "application/json",
  },
})

apiClient.interceptors.request.use((config) => {
  const token = getStoredToken()

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearAuthSession()
    }

    const detail = error.response?.data?.detail
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((issue) => issue.msg).join(", ")
          : error.message || "No se pudo completar la solicitud."

    const normalizedError = new Error(message)
    normalizedError.status = error.response?.status ?? 500
    normalizedError.detail = detail
    normalizedError.original = error

    return Promise.reject(normalizedError)
  },
)

export default apiClient
