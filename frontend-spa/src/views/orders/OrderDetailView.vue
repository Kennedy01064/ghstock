<template>
  <div v-if="ordersStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
    {{ ordersStore.error }}
  </div>

  <DashboardSkeleton v-else-if="ordersStore.isLoading && !order" />

  <div v-else-if="order" class="space-y-8 pb-32">
    <!-- Rejection Alert -->
    <div v-if="order.rejectionNote" class="rounded-2xl border border-rose-500/30 bg-rose-500/5 p-5 flex items-start gap-4">
      <div class="w-9 h-9 shrink-0 rounded-xl bg-rose-500/20 border border-rose-500/30 flex items-center justify-center text-rose-400">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <div>
        <p class="text-[10px] font-black text-rose-400 uppercase tracking-[0.3em] mb-1">Pedido Rechazado por Almacen</p>
        <p class="text-sm font-medium text-rose-200/80">{{ order.rejectionNote }}</p>
        <p class="text-[10px] text-text-muted mt-2">Puedes modificar el pedido y volver a enviarlo.</p>
      </div>
    </div>

    <!-- ... (Page header card remains same) ... -->
    <div class="card flex flex-col md:flex-row md:items-center justify-between gap-8 border-slate-200 shadow-[0_32px_64px_-12px_rgba(0,0,0,0.6)] backdrop-blur-3xl overflow-hidden relative group/header">
      <div class="absolute inset-0 bg-gradient-to-r from-amber/5 to-transparent opacity-0 group-hover/header:opacity-100 transition-opacity duration-700" />
      <div class="flex items-center gap-6 relative z-10">
        <div class="h-14 w-14 rounded-2xl bg-white border border-slate-200 flex items-center justify-center text-amber shadow-[inset_0_2px_4px_rgba(255,255,255,0.05)]">
          <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <div class="space-y-1.5">
          <span class="eyebrow tracking-[0.4em] !text-text-muted text-[10px]">Centro de Operaciones</span>
          <h1 class="h2 !text-2xl !tracking-tight">{{ order.buildingName }}</h1>
        </div>
      </div>
      <div class="flex items-center gap-6 relative z-10">
        <div class="text-right hidden sm:block border-r border-slate-200 pr-6">
          <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.3em]">Referencia Interna</p>
          <p class="text-xs font-bold text-slate-900 uppercase mt-1">G-ORD-{{ String(order.id).padStart(5, "0") }}</p>
        </div>
        <div class="flex flex-col items-end gap-2">
          <span class="px-5 py-2.5 rounded-xl text-[10px] font-black tracking-[0.3em] uppercase border shadow-2xl transition-all" :class="statusClass(order.status)">
            {{ statusLabel(order.status) }}
          </span>
        </div>
      </div>
    </div>

    <div class="grid gap-8 xl:grid-cols-[minmax(0,0.68fr)_minmax(0,0.32fr)]">
      <section class="space-y-8 xl:order-none order-last">
        <!-- Critical Inventory remains same -->
        <div v-if="order.status === 'draft' && criticalInventory.length" class="p-8 rounded-[2.5rem] bg-red-950/20 border border-red-500/20 shadow-[0_24px_48px_-12px_rgba(153,27,27,0.3)] backdrop-blur-xl">
          <div class="flex items-center gap-5 mb-8">
            <div class="w-12 h-12 rounded-2xl bg-red-500/20 border border-red-500/30 flex items-center justify-center text-red-500 shadow-lg animate-pulse">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <h2 class="text-[10px] font-black text-red-400 uppercase tracking-[0.4em] mb-1">Reposicion Etica Prioritaria</h2>
              <p class="text-base font-black text-slate-900 tracking-tight">Stock Critico Detectado en Sede</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <article v-for="inv in criticalInventory" :key="inv.id" class="bg-slate-50 border border-slate-200 rounded-2xl p-4 flex items-center gap-4">
              <div class="w-14 h-14 shrink-0 bg-slate-100 border border-slate-200 flex items-center justify-center rounded-xl p-2 shadow-2xl">
                <img :src="inv.product.imageUrl" :alt="inv.product.name" class="max-h-full object-contain">
              </div>
              <div class="flex-grow min-w-0">
                <h3 class="text-[10px] font-black text-slate-900 uppercase truncate">{{ inv.product.name }}</h3>
                <div class="flex items-center gap-2 mt-1.5">
                  <span class="px-2 py-0.5 rounded-lg text-[8px] font-black bg-red-500 text-slate-900 uppercase tracking-widest">{{ inv.quantity }} {{ inv.product.unit || "UN" }}</span>
                  <span class="text-[9px] font-bold text-text-muted">Min: {{ inv.product.stockMinimo }}</span>
                </div>
              </div>
              <button
                type="button"
                class="w-10 h-10 flex items-center justify-center rounded-xl bg-amber text-navy-deep transition-all hover:scale-105 disabled:opacity-50"
                :disabled="ordersStore.isUpdatingItem"
                @click="addItem(inv.product, Math.max((inv.product.stockMinimo || 0) - inv.quantity, 1))"
              >
                <svg v-if="!ordersStore.isUpdatingItem" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
                </svg>
                <svg v-else class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
            </article>
          </div>
        </div>

        <article class="card !p-0 overflow-hidden" v-if="order.status === 'draft'">
          <div class="px-4 md:px-8 py-5 border-b border-slate-200 bg-slate-50 space-y-4">
            <div class="flex items-center justify-between gap-3">
              <div>
                <h3 class="text-base font-bold text-slate-900">Catalogo disponible</h3>
                <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-1">Agregar productos a la orden</p>
              </div>
              <span class="shrink-0 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-[10px] font-black text-amber uppercase tracking-widest">{{ filteredProducts.length }} items</span>
            </div>
            <div class="grid gap-3 md:grid-cols-[minmax(0,1fr)_200px]">
              <div class="relative">
                <input v-model="catalogSearch" type="text" placeholder="Localizar producto o codigo de insumo..." class="input-field !pl-12">
                <svg class="w-4 h-4 text-text-muted absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <PremiumSelect
                v-model="categoryFilter"
                :options="[{ value: '', label: 'Todas las Categorias' }, ...categories.map(c => ({ value: c, label: c }))]"
                placeholder="Todas las Categorias"
              />
            </div>
          </div>
          
          <div v-if="filteredProducts.length" class="p-3 sm:p-6 grid gap-3 sm:gap-4 md:grid-cols-2 max-h-[520px] overflow-y-auto custom-scrollbar">
            <article v-for="product in filteredProducts" :key="product.id" class="rounded-[24px] border border-slate-200 bg-slate-50 p-4 flex flex-col gap-4">
              <div class="flex items-center gap-4">
                <img :src="product.imageUrl" :alt="product.name" class="w-16 h-16 rounded-2xl object-cover border border-slate-200 bg-slate-50" />
                <div class="min-w-0">
                  <p class="text-sm font-black text-slate-900 truncate">{{ product.name }}</p>
                  <p class="text-[10px] uppercase tracking-[0.18em] text-text-muted mt-2">{{ product.categoria }}</p>
                </div>
              </div>
              <div class="flex items-center justify-between text-sm text-text-secondary">
                <span>{{ product.unit }}</span>
                <span>{{ formatCurrency(product.price) }}</span>
              </div>
              <div class="grid grid-cols-[72px_minmax(0,1fr)] gap-3">
                <input v-model.number="productQuantities[product.id]" type="number" min="1" class="input-field !px-3 !py-3 text-center">
                <button
                  type="button"
                  class="btn btn-primary !min-h-[44px]"
                  :disabled="ordersStore.isUpdatingItem"
                  @click="addItem(product, productQuantities[product.id])"
                >
                  {{ ordersStore.isUpdatingItem ? "..." : "Agregar" }}
                </button>
              </div>
            </article>
          </div>

          <div v-else class="p-20">
            <EmptyState
              title="Sin resultados"
              description="No encontramos productos que coincidan con tu busqueda o categoria."
              class="bg-transparent border-none shadow-none"
            />
          </div>
        </article>

        <article class="card !p-0 overflow-hidden">
          <div class="px-4 md:px-8 py-5 border-b border-slate-200 bg-slate-50 flex items-center justify-between gap-3">
            <div>
              <h3 class="text-base font-bold text-slate-900">Items de la orden</h3>
              <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-1">Resumen del requerimiento</p>
            </div>
            <span class="inline-flex items-center px-3 py-1 rounded-full border text-[10px] font-black uppercase tracking-[0.18em]" :class="statusClass(order.status)">{{ statusLabel(order.status) }}</span>
          </div>
          <OrderItemsList :items="order.items" :editable="order.status === 'draft'" :loading="ordersStore.isUpdatingItem" @remove="removeItem" />
        </article>
      </section>

      <aside class="space-y-8 xl:order-none order-first">
        <article class="card">
          <span class="section-label">Resumen</span>
          <div class="space-y-3 text-sm text-text-secondary">
            <div class="flex items-center justify-between gap-4"><span>Edificio</span><span class="font-bold text-slate-900">{{ order.buildingName }}</span></div>
            <div class="flex items-center justify-between gap-4"><span>Solicitante</span><span class="font-bold text-slate-900">{{ order.createdBy?.name || '-' }}</span></div>
            <div class="flex items-center justify-between gap-4"><span>Total estimado</span><span class="font-bold text-slate-900">{{ formatCurrency(totalAmount) }}</span></div>
          </div>
        </article>

        <article class="card space-y-4">
          <span class="section-label">Acciones</span>
          <button v-if="order.status === 'draft'" type="button" class="btn btn-primary w-full" :disabled="ordersStore.isSubmittingOrder" @click="openStatusModal('submit')">
            {{ ordersStore.isSubmittingOrder ? "Enviando..." : "Enviar orden" }}
          </button>
          <button v-else-if="['submitted', 'rejected'].includes(order.status)" type="button" class="btn btn-secondary w-full" :disabled="ordersStore.isReopeningOrder" @click="openStatusModal('reopen')">
            {{ ordersStore.isReopeningOrder ? "Reabriendo..." : "Reabrir orden" }}
          </button>
          <button v-else-if="order.status === 'dispatched'" type="button" class="btn btn-primary w-full" :disabled="ordersStore.isReceivingOrder" @click="openStatusModal('receive')">
            {{ ordersStore.isReceivingOrder ? "Confirmando..." : "Confirmar recepcion" }}
          </button>
          <button v-if="['draft', 'submitted'].includes(order.status)" type="button" class="btn btn-secondary w-full" :disabled="ordersStore.isCancellingOrder" @click="openStatusModal('cancel')">
            {{ ordersStore.isCancellingOrder ? "Cancelando..." : "Cancelar orden" }}
          </button>
        </article>
      </aside>
    </div>

    <AppModal
      :open="Boolean(pendingAction)"
      eyebrow="Ordenes"
      :title="modalContent.title"
      :description="modalContent.description"
      :confirm-label="modalContent.confirmLabel"
      :confirm-variant="modalContent.confirmVariant"
      :loading="ordersStore.isSubmittingOrder || ordersStore.isReopeningOrder || ordersStore.isCancellingOrder || ordersStore.isReceivingOrder"
      @close="pendingAction = ''"
      @confirm="confirmStatusAction"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import OrderItemsList from "@/components/orders/OrderItemsList.vue"
import AppModal from "@/components/ui/AppModal.vue"
import PremiumSelect from "@/components/ui/PremiumSelect.vue"
import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import EmptyState from "@/components/ui/EmptyState.vue"
import { useProductStore } from "@/stores/productStore"
import { useInventoryStore } from "@/stores/inventoryStore"
import { useOrdersStore } from "@/stores/ordersStore"
import { useUiStore } from "@/stores/uiStore"
import { formatCurrency, statusClass, statusLabel } from "@/utils/formatters"
import { normalizeInventoryItem, normalizeOrder, normalizeProduct } from "@/utils/normalizers"

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const inventoryStore = useInventoryStore()
const ordersStore = useOrdersStore()
const uiStore = useUiStore()
const pendingAction = ref("")
const catalogSearch = ref("")
const categoryFilter = ref("")
const productQuantities = reactive({})

const order = computed(() => (ordersStore.currentOrder ? normalizeOrder(ordersStore.currentOrder) : null))
const products = computed(() => productStore.products.map(normalizeProduct).filter((product) => product.active))
const inventoryItems = computed(() => inventoryStore.items.map(normalizeInventoryItem))
const criticalInventory = computed(() => inventoryItems.value.filter((item) => item.quantity <= item.product.stockMinimo))
const categories = computed(() => [...new Set(products.value.map((product) => product.categoria).filter(Boolean))].sort())
const filteredProducts = computed(() =>
  products.value.filter((product) => {
    const query = catalogSearch.value.trim().toLowerCase()
    const matchesQuery =
      !query ||
      product.name.toLowerCase().includes(query) ||
      (product.description || "").toLowerCase().includes(query) ||
      (product.sku || "").toLowerCase().includes(query)
    const matchesCategory = !categoryFilter.value || product.categoria === categoryFilter.value
    return matchesQuery && matchesCategory
  }),
)
const totalAmount = computed(() => order.value?.items.reduce((total, item) => total + item.quantity * (item.precioUnitario || 0), 0) ?? 0)
const modalContent = computed(() => {
  if (pendingAction.value === "submit") {
    return {
      title: "Enviar orden",
      description: "La orden pasara a estado enviado para consolidacion.",
      confirmLabel: "Enviar",
      confirmVariant: "primary",
    }
  }

  if (pendingAction.value === "reopen") {
    return {
      title: "Reabrir orden",
      description: "La orden volvera a estado borrador para seguir editandose.",
      confirmLabel: "Reabrir",
      confirmVariant: "primary",
    }
  }

  if (pendingAction.value === "receive") {
    return {
      title: "Confirmar recepcion",
      description: "Esta accion movera el pedido al inventario local del edificio.",
      confirmLabel: "Confirmar",
      confirmVariant: "primary",
    }
  }

  return {
    title: "Cancelar orden",
    description: "La orden se cancelara y dejara de estar disponible para despacho.",
    confirmLabel: "Cancelar orden",
    confirmVariant: "danger",
  }
})

async function ensureOrder() {
  await productStore.fetchProducts()

  if (route.params.orderId === "new") {
    const buildingId = Number(route.query.buildingId)
    const createdOrder = await ordersStore.createOrder(buildingId)
    await ordersStore.fetchOrder(createdOrder.id)
    await router.replace({ name: "ordersOrderDetail", params: { orderId: createdOrder.id } })
    return
  }

  await ordersStore.fetchOrder(route.params.orderId)

  if (ordersStore.currentOrder?.building_id) {
    await inventoryStore.fetchInventory(ordersStore.currentOrder.building_id)
  }
}

async function addItem(product, quantity = 1) {
  if (ordersStore.isUpdatingItem) return
  try {
    await ordersStore.addItem(order.value.id, {
      product_id: product.id,
      quantity: Math.max(1, Number(quantity) || 1),
    })
    productQuantities[product.id] = 1
    uiStore.success(`${product.name} fue agregado a la orden.`, "Item agregado")
  } catch (error) {
    uiStore.error(error.message, "No se pudo agregar el item")
  }
}

async function removeItem(itemId) {
  if (ordersStore.isUpdatingItem) return
  try {
    await ordersStore.removeItem(order.value.id, itemId)
    uiStore.success("El item fue retirado de la orden.", "Item removido")
  } catch (error) {
    uiStore.error(error.message, "No se pudo quitar el item")
  }
}

function openStatusModal(action) {
  pendingAction.value = action
}

async function confirmStatusAction() {
  if (!pendingAction.value ||
      ordersStore.isSubmittingOrder ||
      ordersStore.isReopeningOrder ||
      ordersStore.isCancellingOrder ||
      ordersStore.isReceivingOrder) {
    return
  }

  const action = pendingAction.value
  try {
    await ordersStore.updateOrderStatus(order.value.id, action)
    pendingAction.value = ""

    const messages = {
      submit: "La orden fue enviada correctamente.",
      reopen: "La orden volvio a borrador.",
      receive: "La recepcion se confirmo y el inventario local fue actualizado.",
      cancel: "La orden fue cancelada.",
    }

    uiStore.success(messages[action], "Estado actualizado")
  } catch (error) {
    uiStore.error(error.message, "No se pudo actualizar la orden")
  }
}

onMounted(() => {
  ensureOrder().catch((error) => {
    uiStore.error(error.message, "No se pudo cargar la orden")
  })
})

watch(
  products,
  (items) => {
    items.forEach((product) => {
      if (!productQuantities[product.id]) {
        productQuantities[product.id] = 1
      }
    })
  },
  { immediate: true },
)
</script>
