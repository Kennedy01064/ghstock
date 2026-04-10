import axios from "axios"

import { emitLockdown, emitUnauthorized } from "@/utils/authBus"
import { clearAuthSession, getStoredToken, getStoredRefreshToken, persistAuthSession, getStoredUser } from "@/utils/authSession"

export const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1"

const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 15000,
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

let isRefreshing = false
let pendingQueue = []

function processQueue(error, token = null) {
  pendingQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error)
    else resolve(token)
  })
  pendingQueue = []
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      const refreshToken = getStoredRefreshToken()

      if (refreshToken) {
        if (isRefreshing) {
          return new Promise((resolve, reject) => {
            pendingQueue.push({ resolve, reject })
          }).then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return apiClient(originalRequest)
          })
        }

        originalRequest._retry = true
        isRefreshing = true

        try {
          const resp = await axios.post(
            `${apiBaseUrl}/auth/refresh`,
            { refresh_token: refreshToken },
            { headers: { "Content-Type": "application/json" } },
          )
          const newToken = resp.data.access_token
          const newRefresh = resp.data.refresh_token ?? refreshToken
          const user = getStoredUser()
          persistAuthSession(newToken, user, true, newRefresh)
          processQueue(null, newToken)
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return apiClient(originalRequest)
        } catch (refreshError) {
          processQueue(refreshError, null)
          clearAuthSession()
          emitUnauthorized()
          return Promise.reject(refreshError)
        } finally {
          isRefreshing = false
        }
      }

      clearAuthSession()
      emitUnauthorized()
    }
    if (error.response?.status === 423) {
      clearAuthSession()
      emitLockdown(typeof error.response?.data?.detail === "string" ? error.response.data.detail : "")
    }

    const isTimeout = error.code === "ECONNABORTED" || error.message.includes("timeout")
    const isNetworkError = !error.response && error.request && !isTimeout
    const status = error.response?.status ?? (isTimeout ? 408 : 500)

    const detail = error.response?.data?.detail
    const message = isTimeout
      ? "La solicitud tardó demasiado. Por favor, revisa tu conexión e inténtalo de nuevo."
      : isNetworkError
        ? "No se pudo conectar con el servidor. Verifica tu conexión a internet."
        : typeof detail === "string"
          ? detail
          : Array.isArray(detail)
            ? detail.map((issue) => issue.msg).join(", ")
            : error.message || "No se pudo completar la solicitud."

    const normalizedError = new Error(message)
    normalizedError.status = status
    normalizedError.detail = detail
    normalizedError.original = error
    
    // Semantic flags
    normalizedError.isTimeout = isTimeout
    normalizedError.isNetworkError = isNetworkError
    normalizedError.isUnauthorized = status === 401
    normalizedError.isForbidden = status === 403
    normalizedError.isNotFound = status === 404
    normalizedError.isConflict = status === 409
    normalizedError.isValidation = status === 422

    return Promise.reject(normalizedError)
  },
)

export default apiClient
