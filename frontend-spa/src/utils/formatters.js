export const logoUrl = "/static/img/logo_trans.png"
export const defaultProductUrl = "/static/img/default-product.png"
export const defaultBuildingUrl = "/static/img/default-building.png"

const statusPalette = {
  draft: "bg-amber/10 text-amber border-amber/30",
  submitted: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
  processing: "bg-amber/10 text-amber border-amber/30",
  dispatched: "bg-blue-500/10 text-blue-400 border-blue-500/30",
  delivered: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
  cancelled: "bg-rose-500/10 text-rose-400 border-rose-500/30",
  pending: "bg-amber/10 text-amber border-amber/30",
  picking: "bg-amber/10 text-amber border-amber/30",
  completed: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
  recibida: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
  "en proceso": "bg-amber/10 text-amber border-amber/30",
  activo: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
  suspendido: "bg-rose-500/10 text-rose-400 border-rose-500/30",
  mantenimiento: "bg-white/5 text-text-muted border-white/10",
  procesado: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
  pendiente: "bg-amber/10 text-amber border-amber/30",
}

export function statusClass(status) {
  return statusPalette[status] ?? "bg-white/5 text-text-muted border-white/10"
}

export function formatCurrency(value) {
  return new Intl.NumberFormat("es-PE", {
    style: "currency",
    currency: "PEN",
    maximumFractionDigits: 2,
  }).format(Number(value) || 0)
}

export function formatDate(value) {
  if (!value) {
    return "-"
  }

  return new Intl.DateTimeFormat("es-PE", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(value))
}

export function titleCase(value) {
  return String(value ?? "")
    .split(/\s+/)
    .filter(Boolean)
    .map((token) => token.charAt(0).toUpperCase() + token.slice(1).toLowerCase())
    .join(" ")
}

export function assetUrl(value, fallback = defaultProductUrl) {
  if (!value) {
    return fallback
  }

  if (
    value.startsWith("http://") ||
    value.startsWith("https://") ||
    value.startsWith("/") ||
    value.startsWith("data:")
  ) {
    return value
  }

  return `/static/uploads/${value}`
}
