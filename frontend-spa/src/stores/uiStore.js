import { ref } from "vue"
import { defineStore } from "pinia"

let toastId = 0

export const useUiStore = defineStore("ui", () => {
  const toasts = ref([])

  function removeToast(id) {
    toasts.value = toasts.value.filter((toast) => toast.id !== id)
  }

  function pushToast({
    type = "info",
    title = "",
    message = "",
    duration = 4000,
  }) {
    const id = ++toastId

    toasts.value = [
      ...toasts.value,
      {
        id,
        type,
        title,
        message,
      },
    ]

    if (duration > 0) {
      window.setTimeout(() => {
        removeToast(id)
      }, duration)
    }

    return id
  }

  function success(message, title = "Operacion completada") {
    return pushToast({ type: "success", title, message })
  }

  function error(message, title = "Operacion fallida") {
    return pushToast({ type: "error", title, message, duration: 5500 })
  }

  function info(message, title = "Aviso") {
    return pushToast({ type: "info", title, message })
  }

  function warning(message, title = "Atencion") {
    return pushToast({ type: "warning", title, message, duration: 5000 })
  }

  return {
    toasts,
    pushToast,
    removeToast,
    success,
    error,
    info,
    warning,
  }
})
