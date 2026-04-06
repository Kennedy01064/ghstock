export const logoUrl = "/static/img/logo_trans.png"
export const defaultProductUrl = "/static/img/default-product.png"
export const defaultBuildingUrl = "/static/img/default-building.png"
export const mockupBuildingUrl = "/static/uploads/mockup_torre_norte.png"

export const currentUser = {
  id: 1,
  name: "Mariana Hernandez",
  username: "mhernandez",
  role: "superadmin",
}

export const admins = [
  { id: 1, name: "Mariana Hernandez", username: "mhernandez", role: "superadmin", buildingCount: 4, email: "mariana@grupohernandez.pe", status: "activo" },
  { id: 2, name: "Luis Ortega", username: "lortega", role: "manager", buildingCount: 3, email: "luis@grupohernandez.pe", status: "activo" },
  { id: 3, name: "Valeria Campos", username: "vcampos", role: "admin", buildingCount: 2, email: "valeria@grupohernandez.pe", status: "activo" },
  { id: 4, name: "Carlos Paredes", username: "cparedes", role: "admin", buildingCount: 1, email: "carlos@grupohernandez.pe", status: "suspendido" },
]

export const buildings = [
  { id: 1, name: "Torre Norte", address: "Av. Primavera 180", units: 24, adminId: 3, adminName: "Valeria Campos", imageUrl: mockupBuildingUrl, district: "Surco", status: "activo" },
  { id: 2, name: "Residencial Aurora", address: "Calle Las Camelias 541", units: 18, adminId: 4, adminName: "Carlos Paredes", imageUrl: defaultBuildingUrl, district: "San Isidro", status: "activo" },
  { id: 3, name: "Altos del Parque", address: "Jr. Los Nogales 700", units: 32, adminId: null, adminName: "Sin asignar", imageUrl: defaultBuildingUrl, district: "Miraflores", status: "activo" },
  { id: 4, name: "Mirador Central", address: "Av. Del Ejercito 440", units: 21, adminId: 3, adminName: "Valeria Campos", imageUrl: mockupBuildingUrl, district: "Magdalena", status: "mantenimiento" },
]

export const products = [
  { id: 1, name: "Detergente industrial", sku: "SKU-001", categoria: "Limpieza", unit: "GAL", price: 74.5, stockActual: 8, stockMinimo: 12, description: "Detergente concentrado para mantenimiento intensivo.", imageUrl: defaultProductUrl, active: true },
  { id: 2, name: "Papel toalla premium", sku: "SKU-002", categoria: "Consumibles", unit: "PQT", price: 18.9, stockActual: 42, stockMinimo: 20, description: "Presentacion institucional de alta rotacion.", imageUrl: defaultProductUrl, active: true },
  { id: 3, name: "Desinfectante citrico", sku: "SKU-003", categoria: "Limpieza", unit: "GAL", price: 63.2, stockActual: 0, stockMinimo: 10, description: "Desinfectante de alto rendimiento para superficies comunes.", imageUrl: defaultProductUrl, active: true },
  { id: 4, name: "Bolsas negras 140L", sku: "SKU-004", categoria: "Desechos", unit: "PQT", price: 26.8, stockActual: 16, stockMinimo: 15, description: "Bolsa reforzada para cuartos de residuos.", imageUrl: defaultProductUrl, active: false },
  { id: 5, name: "Jabon espuma", sku: "SKU-005", categoria: "Higiene", unit: "UND", price: 21.5, stockActual: 27, stockMinimo: 12, description: "Recarga de jabon espuma para dispensadores.", imageUrl: defaultProductUrl, active: true },
]

export const purchases = [
  {
    id: 101,
    supplier: "Clean Supply SAC",
    createdAt: "2026-03-20",
    status: "recibida",
    total: 1850.4,
    note: "Reposicion semanal de insumos de limpieza.",
    items: [
      { id: 1, name: "Detergente industrial", quantity: 12, unit: "GAL", price: 74.5 },
      { id: 2, name: "Desinfectante citrico", quantity: 8, unit: "GAL", price: 63.2 },
    ],
  },
  {
    id: 102,
    supplier: "Higiene Total",
    createdAt: "2026-03-26",
    status: "en proceso",
    total: 940.8,
    note: "Compra menor para reposicion de higiene.",
    items: [
      { id: 3, name: "Jabon espuma", quantity: 24, unit: "UND", price: 21.5 },
      { id: 4, name: "Papel toalla premium", quantity: 18, unit: "PQT", price: 18.9 },
    ],
  },
]

export const orders = [
  {
    id: 2001,
    buildingId: 1,
    buildingName: "Torre Norte",
    createdBy: { name: "Valeria Campos", username: "vcampos" },
    createdAt: "2026-03-28",
    status: "draft",
    rejectionNote: "",
    items: [
      { id: 1, productId: 1, nombreProductoSnapshot: "Detergente industrial", quantity: 3, unit: "GAL", precioUnitario: 74.5, imageUrl: defaultProductUrl },
      { id: 2, productId: 5, nombreProductoSnapshot: "Jabon espuma", quantity: 6, unit: "UND", precioUnitario: 21.5, imageUrl: defaultProductUrl },
    ],
  },
  {
    id: 2002,
    buildingId: 2,
    buildingName: "Residencial Aurora",
    createdBy: { name: "Carlos Paredes", username: "cparedes" },
    createdAt: "2026-03-26",
    status: "submitted",
    rejectionNote: "",
    items: [
      { id: 3, productId: 2, nombreProductoSnapshot: "Papel toalla premium", quantity: 10, unit: "PQT", precioUnitario: 18.9, imageUrl: defaultProductUrl },
      { id: 4, productId: 3, nombreProductoSnapshot: "Desinfectante citrico", quantity: 4, unit: "GAL", precioUnitario: 63.2, imageUrl: defaultProductUrl },
    ],
  },
  {
    id: 2003,
    buildingId: 4,
    buildingName: "Mirador Central",
    createdBy: { name: "Valeria Campos", username: "vcampos" },
    createdAt: "2026-03-22",
    status: "dispatched",
    rejectionNote: "",
    items: [
      { id: 5, productId: 1, nombreProductoSnapshot: "Detergente industrial", quantity: 2, unit: "GAL", precioUnitario: 74.5, imageUrl: defaultProductUrl },
    ],
  },
]

export const batches = [
  {
    id: 301,
    code: "BATCH-301",
    createdAt: "2026-03-27",
    status: "picking",
    createdBy: { name: "Luis Ortega", username: "lortega" },
    orders: [orders[1]],
    items: [
      { id: 1, name: "Papel toalla premium", requested: 10, picked: 7, unit: "PQT" },
      { id: 2, name: "Desinfectante citrico", requested: 4, picked: 4, unit: "GAL" },
    ],
  },
  {
    id: 302,
    code: "BATCH-302",
    createdAt: "2026-03-18",
    status: "completed",
    createdBy: { name: "Luis Ortega", username: "lortega" },
    orders: [orders[2]],
    items: [
      { id: 3, name: "Detergente industrial", requested: 2, picked: 2, unit: "GAL" },
    ],
  },
]

export const localInventory = [
  { id: 1, quantity: 4, lastMovement: "2026-03-29", product: { id: 1, name: "Detergente industrial", sku: "SKU-001", unit: "GAL", imageUrl: defaultProductUrl, stockMinimo: 6 } },
  { id: 2, quantity: 15, lastMovement: "2026-03-30", product: { id: 2, name: "Papel toalla premium", sku: "SKU-002", unit: "PQT", imageUrl: defaultProductUrl, stockMinimo: 8 } },
  { id: 3, quantity: 0, lastMovement: "2026-03-24", product: { id: 3, name: "Desinfectante citrico", sku: "SKU-003", unit: "GAL", imageUrl: defaultProductUrl, stockMinimo: 5 } },
]

export const csvUploads = [
  { id: 1, fileName: "catalogo-marzo.csv", uploadedAt: "2026-03-15", status: "procesado", rows: 188 },
  { id: 2, fileName: "catalogo-abril.csv", uploadedAt: "2026-04-01", status: "pendiente", rows: 64 },
]

export const chartEdificios = [
  { label: "Torre Norte", value: 12 },
  { label: "Aurora", value: 9 },
  { label: "Altos", value: 6 },
  { label: "Mirador", value: 4 },
]

export const topProductos = [
  { label: "Detergente industrial", value: 26, color: "#F2AD3D" },
  { label: "Papel toalla premium", value: 18, color: "#06286F" },
  { label: "Jabon espuma", value: 15, color: "#4F46E5" },
  { label: "Bolsas negras 140L", value: 12, color: "#10B981" },
  { label: "Desinfectante citrico", value: 8, color: "#6B7280" },
]

export const dashboardMetrics = {
  totalPedidosPendientes: 9,
  totalEdificiosActivos: 4,
  costoDespachadoMes: 12450.8,
  totalProductos: 5,
}

export const managerMetrics = {
  lotesPendientes: 2,
  comprasRecientes: 2,
  alertasStock: 3,
}

export const adminMetrics = {
  pedidosEnTransito: 1,
  pedidosDespachados: 1,
  historialPedidos: 3,
}

export const statusPalette = {
  draft: "bg-amber/10 text-amber border-amber/30",
  submitted: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
  dispatched: "bg-blue-500/10 text-blue-400 border-blue-500/30",
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
  }).format(value)
}

export function formatDate(value) {
  return new Intl.DateTimeFormat("es-PE", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(value))
}

export function titleCase(value) {
  return value
    .split(/\s+/)
    .filter(Boolean)
    .map((token) => token.charAt(0).toUpperCase() + token.slice(1).toLowerCase())
    .join(" ")
}

export function getProduct(productId) {
  return products.find((product) => product.id === Number(productId)) ?? products[0]
}

export function getBuilding(buildingId) {
  return buildings.find((building) => building.id === Number(buildingId)) ?? buildings[0]
}

export function getAdmin(adminId) {
  return admins.find((admin) => admin.id === Number(adminId)) ?? admins[0]
}

export function getOrder(orderId) {
  return orders.find((order) => order.id === Number(orderId)) ?? orders[0]
}

export function getPurchase(purchaseId) {
  return purchases.find((purchase) => purchase.id === Number(purchaseId)) ?? purchases[0]
}

export function getBatch(batchId) {
  return batches.find((batch) => batch.id === Number(batchId)) ?? batches[0]
}

export function assetUpload(filename) {
  return filename ? `/static/uploads/${filename}` : defaultBuildingUrl
}
