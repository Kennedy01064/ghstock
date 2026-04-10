// Simple event bus to coordinate auth events without circular dependencies
import { ref } from "vue"

export const onUnauthorized = ref(null)
export const onLockdown = ref(null)

export function emitUnauthorized() {
  if (onUnauthorized.value) {
    onUnauthorized.value()
  }
}

export function emitLockdown(message = "") {
  if (onLockdown.value) {
    onLockdown.value(message)
  }
}
