import { createRouter, createWebHistory } from "vue-router"

import { getStoredToken, getStoredUser } from "@/utils/authSession"
import { dashboardRouteForRole } from "@/utils/roleRoutes"

const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/auth/LoginView.vue"),
    meta: { title: "Acceso Institucional", guestOnly: true },
  },
  {
    path: "/",
    component: () => import("@/layouts/Layout.vue"),
    meta: { requiresAuth: true },
    children: [
      { path: "", name: "dashboard", component: () => import("@/views/dashboard/IndexView.vue"), meta: { title: "Dashboard" } },
      { path: "dashboard/admin", name: "dashboardAdmin", component: () => import("@/views/dashboard/AdminDashboardView.vue"), meta: { title: "Dashboard Admin" } },
      { path: "dashboard/manager", name: "dashboardManager", component: () => import("@/views/dashboard/ManagerDashboardView.vue"), meta: { title: "Dashboard Manager" } },

      { path: "catalog/warehouse", name: "catalogWarehouse", component: () => import("@/views/catalog/WarehouseView.vue"), meta: { title: "Almacen" } },
      { path: "catalog/products/create", name: "catalogProductCreate", component: () => import("@/views/catalog/CreateProductView.vue"), meta: { title: "Crear producto" } },
      { path: "catalog/products/:productId/edit", name: "catalogProductEdit", component: () => import("@/views/catalog/EditProductView.vue"), meta: { title: "Editar producto" } },
      { path: "catalog/buildings", name: "catalogBuildings", component: () => import("@/views/catalog/ListBuildingsAdminView.vue"), meta: { title: "Edificios" } },
      { path: "catalog/buildings/create", name: "catalogBuildingCreate", component: () => import("@/views/catalog/CreateBuildingView.vue"), meta: { title: "Crear edificio" } },
      { path: "catalog/buildings/:buildingId/edit", name: "catalogBuildingEdit", component: () => import("@/views/catalog/EditBuildingView.vue"), meta: { title: "Editar edificio" } },
      { path: "catalog/admins", name: "catalogAdmins", component: () => import("@/views/catalog/ListAdminsView.vue"), meta: { title: "Administradores" } },
      { path: "catalog/admins/create", name: "catalogAdminCreate", component: () => import("@/views/catalog/CreateAdminView.vue"), meta: { title: "Crear administrador" } },
      { path: "catalog/admins/:adminId/edit", name: "catalogAdminEdit", component: () => import("@/views/catalog/EditAdminView.vue"), meta: { title: "Editar administrador" } },
      { path: "catalog/assign-building", name: "catalogAssignBuilding", component: () => import("@/views/catalog/AssignBuildingView.vue"), meta: { title: "Asignar edificios" } },
      { path: "catalog/upload-csv", name: "catalogUploadCsv", component: () => import("@/views/catalog/UploadCsvView.vue"), meta: { title: "Catalogo CSV" } },

      { path: "dispatch/pending", name: "dispatchPending", component: () => import("@/views/dispatch/PendingOrdersView.vue"), meta: { title: "Ordenes pendientes" } },
      { path: "dispatch/history", name: "dispatchHistory", component: () => import("@/views/dispatch/HistoryView.vue"), meta: { title: "Historial" } },
      { path: "dispatch/batches/:batchId", name: "dispatchBatchDetail", component: () => import("@/views/dispatch/BatchDetailView.vue"), meta: { title: "Detalle de batch" } },
      { path: "dispatch/batches/:batchId/picking", name: "dispatchPicking", component: () => import("@/views/dispatch/PickingView.vue"), meta: { title: "Picking" } },
      { path: "dispatch/purchases", name: "dispatchPurchases", component: () => import("@/views/dispatch/purchases/ListView.vue"), meta: { title: "Compras" } },
      { path: "dispatch/purchases/create", name: "dispatchPurchaseCreate", component: () => import("@/views/dispatch/purchases/CreateView.vue"), meta: { title: "Registrar compra" } },
      { path: "dispatch/purchases/:purchaseId", name: "dispatchPurchaseDetail", component: () => import("@/views/dispatch/purchases/DetailView.vue"), meta: { title: "Detalle de compra" } },

      { path: "orders/my-orders", name: "ordersMyOrders", component: () => import("@/views/orders/MyOrdersView.vue"), meta: { title: "Mis pedidos" } },
      { path: "orders/inventory", name: "ordersMyInventory", component: () => import("@/views/orders/MyInventoryView.vue"), meta: { title: "Mi inventario" } },
      { path: "orders/inventory/add", name: "ordersAddInventory", component: () => import("@/views/orders/AddInventoryView.vue"), meta: { title: "Agregar inventario" } },
      { path: "orders/consumption", name: "ordersConsumption", component: () => import("@/views/orders/ConsumptionReportView.vue"), meta: { title: "Consumos" } },
      { path: "orders/buildings", name: "ordersBuildings", component: () => import("@/views/orders/ListBuildingsView.vue"), meta: { title: "Nueva solicitud" } },
      { path: "orders/:orderId", name: "ordersOrderDetail", component: () => import("@/views/orders/OrderDetailView.vue"), meta: { title: "Detalle de orden" } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const token = getStoredToken()
  const storedUser = getStoredUser()
  const requiresAuth = to.matched.some((record) => record.meta?.requiresAuth)
  const guestOnly = to.matched.some((record) => record.meta?.guestOnly)

  if (requiresAuth && !token) {
    return { name: "login", query: { redirect: to.fullPath } }
  }

  if (guestOnly && token) {
    return dashboardRouteForRole(storedUser?.role)
  }

  return true
})

router.afterEach((to) => {
  document.title = to.meta?.title ? `Stock Control | ${to.meta.title}` : "Stock Control"
})

export default router
