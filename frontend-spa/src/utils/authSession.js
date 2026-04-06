const STORAGE_KEY = "stock-spa-auth"

function parseSession(value) {
  if (!value) {
    return null
  }

  try {
    return JSON.parse(value)
  } catch {
    return null
  }
}

function getBrowserStorage(type) {
  if (typeof window === "undefined") {
    return null
  }

  return type === "session" ? window.sessionStorage : window.localStorage
}

export function readAuthSession() {
  const localSession = parseSession(getBrowserStorage("local")?.getItem(STORAGE_KEY))
  const sessionSession = parseSession(getBrowserStorage("session")?.getItem(STORAGE_KEY))

  return localSession ?? sessionSession ?? { token: "", user: null }
}

export function persistAuthSession(token, user, remember = true) {
  clearAuthSession()

  const storage = getBrowserStorage(remember ? "local" : "session")

  if (!storage) {
    return
  }

  storage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      token,
      user,
    }),
  )
}

export function clearAuthSession() {
  getBrowserStorage("local")?.removeItem(STORAGE_KEY)
  getBrowserStorage("session")?.removeItem(STORAGE_KEY)
}

export function getStoredToken() {
  return readAuthSession().token ?? ""
}

export function getStoredUser() {
  return readAuthSession().user ?? null
}
