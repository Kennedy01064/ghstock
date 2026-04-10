import { assetUrl, defaultBuildingUrl, defaultProductUrl, formatDate } from "@/utils/formatters"

export function normalizeProduct(product) {
  return {
    ...product,
    price: product.precio ?? 0,
    stockActual: product.stock_actual ?? 0,
    stockMinimo: product.stock_minimo ?? 0,
    imageUrl: assetUrl(product.imagen_url, defaultProductUrl),
    active: product.is_active !== false,
  }
}

export function normalizeUser(user) {
  const assignedBuildings = user.assigned_buildings ?? []

  return {
    ...user,
    buildingCount: assignedBuildings.length,
    assignedBuildings,
    status: user.is_active === false ? "suspendido" : "activo",
  }
}

export function normalizeBuilding(building) {
  return {
    ...building,
    units: building.departments_count ?? 0,
    district: "Lima",
    adminName: building.admin?.name ?? "Sin asignar",
    imageUrl: assetUrl(building.imagen_frontis, defaultBuildingUrl),
    status: building.admin_id ? "activo" : "pendiente",
  }
}

export function normalizeOrderItem(item) {
  const product = item.product ?? {}

  return {
    ...item,
    unit: product.unit ?? "-",
    imageUrl: assetUrl(product.imagen_url, defaultProductUrl),
    precioUnitario: item.precio_unitario ?? 0,
    nombreProductoSnapshot: item.nombre_producto_snapshot ?? product.name ?? "Producto",
  }
}

export function normalizeOrder(order) {
  return {
    ...order,
    buildingName: order.building?.name ?? `Edificio #${order.building_id}`,
    createdBy: order.created_by ?? null,
    createdAt: order.created_at,
    rejectionNote: order.rejection_note ?? "",
    items: (order.items ?? []).map(normalizeOrderItem),
  }
}

export function normalizeInventoryItem(item) {
  return {
    ...item,
    lastMovement: formatDate(item.last_updated),
    product: normalizeProduct(item.product ?? {}),
  }
}

export function normalizeBatch(batch) {
  return {
    ...batch,
    code: `BATCH-${batch.id}`,
    createdBy: batch.created_by ?? null,
    createdAt: batch.created_at,
    orders: (batch.orders ?? []).map(normalizeOrder),
    items: (batch.items ?? []).map((item) => ({
      ...item,
      name: item.product?.name ?? "Producto",
      requested: item.total_quantity ?? 0,
      picked: item.total_quantity ?? 0,
      unit: item.product?.unit ?? "-",
    })),
  }
}

export function normalizePickingResponse(picking) {
  return {
    ...picking,
    items: (picking.items ?? []).map((item) => ({
      id: `${picking.batch_id}-${item.product_id}`,
      productId: item.product_id,
      name: item.product_name,
      requested: item.total_quantity,
      picked: item.total_quantity,
      unit: item.unit,
      stockActual: item.stock_actual,
    })),
  }
}

export function normalizePurchase(purchase) {
  return {
    ...purchase,
    createdAt: purchase.created_at,
    purchaseDate: formatDate(purchase.purchase_date),
    total: purchase.total_amount ?? 0,
    status: "recibida", // Purchases are always "received" in this system
    note: purchase.notes ?? "",
    items: (purchase.items ?? []).map((item) => ({
      ...item,
      name: item.product?.name ?? "Producto",
      unit: item.product?.unit ?? "-",
      price: item.unit_price ?? 0,
    })),
  }
}
