<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-8 py-8 space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
      <div class="space-y-2">
        <span class="eyebrow !text-amber/60">Seguimiento de Solicitudes</span>
        <h1 data-testid="orders-page-title" class="text-3xl md:text-4xl font-black text-white tracking-tight uppercase">Mis Pedidos</h1>
      </div>
      <RouterLink :to="{ name: 'ordersBuildings' }" class="btn btn-primary !py-3 !px-7 self-start sm:self-auto shrink-0">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
        </svg>
        Nueva Solicitud
      </RouterLink>
    </div>

    <form class="card !p-5 border-white/5 flex flex-col sm:flex-row gap-4 items-end" @submit.prevent="applyFilters">
      <div class="flex-1">
        <label class="label-premium">Estado</label>
        <select v-model="filters.status" class="select-field !py-3">
          <option value="">Todos los estados</option>
          <option v-for="option in statusOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>
      <div class="flex-1">
        <label class="label-premium">Sede</label>
        <select v-model="filters.buildingId" class="select-field !py-3">
          <option value="">Todas las sedes</option>
          <option v-for="building in buildings" :key="building.id" :value="String(building.id)">
            {{ building.name }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary !py-3 !px-5 whitespace-nowrap text-[11px] shrink-0">Aplicar</button>
      <button
        v-if="filters.status || filters.buildingId"
        type="button"
        class="btn btn-secondary !py-3 !px-5 whitespace-nowrap text-[11px] shrink-0"
        @click="clearFilters"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
        </svg>
        Limpiar
      </button>
    </form>

    <div v-if="ordersStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ ordersStore.error }}
    </div>

    <div v-if="orders.length" class="space-y-3" data-testid="orders-list">
      <article
        v-for="order in orders"
        :key="order.id"
        class="card !p-0 overflow-hidden border-white/5 hover:border-white/10 transition-all group"
      >
        <div v-if="order.rejectionNote" class="px-6 py-3 bg-rose-500/10 border-b border-rose-500/20 flex items-start gap-3">
          <svg class="w-4 h-4 text-rose-400 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <p class="text-[11px] font-bold text-rose-300">
            <span class="font-black text-rose-400">Rechazado por almacen:</span>
            {{ order.rejectionNote }}
          </p>
        </div>

        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 sm:p-6">
          <div class="flex items-center gap-4 min-w-0">
            <div
              class="w-10 h-10 shrink-0 rounded-xl flex items-center justify-center border"
              :class="statusDotClass(order.status)"
            >
              <svg v-if="order.status === 'draft'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              <svg v-else-if="order.status === 'submitted'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              <svg v-else-if="order.status === 'processing'" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <svg v-else-if="order.status === 'dispatched' || order.status === 'partially_dispatched'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
              </svg>
              <svg v-else-if="order.status === 'delivered'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="order.status === 'rejected' || order.status === 'cancelled'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="min-w-0">
              <div class="flex flex-wrap items-center gap-2 mb-0.5">
                <p class="text-sm font-black text-white group-hover:text-amber transition-colors">
                  #{{ order.id }} - {{ order.buildingName }}
                </p>
                <span class="inline-flex items-center px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest border" :class="statusBadgeClass(order.status)">
                  {{ statusLabel(order.status) }}
                </span>
              </div>
              <p class="text-[11px] text-text-muted font-bold">
                {{ formatDate(order.createdAt) }} · {{ order.items.length }} producto<span v-if="order.items.length !== 1">s</span>
              </p>
            </div>
          </div>

          <div class="flex items-center gap-2 shrink-0 flex-wrap justify-end">
            <button
              v-if="['submitted', 'rejected'].includes(order.status)"
              type="button"
              class="btn btn-secondary !py-2.5 !px-5 !text-[10px] !min-h-0"
              :disabled="ordersStore.isReopeningOrder"
              @click="openAction(order.id, 'reopen')"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Reabrir para Editar
            </button>

            <button
              v-if="['dispatched', 'partially_dispatched'].includes(order.status)"
              type="button"
              class="btn btn-primary !py-2.5 !px-5 !text-[10px] !min-h-0 shadow-amber/20"
              :disabled="ordersStore.isReceivingOrder"
              @click="openAction(order.id, 'receive')"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              Confirmar Recepcion
            </button>

            <button
              v-if="['draft', 'submitted'].includes(order.status)"
              type="button"
              class="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20 text-[10px] font-black uppercase tracking-widest hover:bg-rose-500/20 transition-all"
              :disabled="ordersStore.isCancellingOrder"
              @click="openAction(order.id, 'cancel')"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Cancelar
            </button>

            <RouterLink
              :to="{ name: 'ordersOrderDetail', params: { orderId: order.id } }"
              class="w-10 h-10 rounded-xl bg-white/[0.05] border border-white/10 text-white hover:bg-amber hover:text-navy-deep hover:border-amber transition-all flex items-center justify-center"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </RouterLink>
          </div>
        </div>
      </article>
    </div>

    <EmptyState
      v-else
      :title="filters.status || filters.buildingId ? 'Sin coincidencias' : 'Sin pedidos'"
      :description="filters.status || filters.buildingId ? 'No hay pedidos con los filtros seleccionados.' : 'Aun no has creado ninguna solicitud de pedido.'"
    >
      <template #action>
        <RouterLink :to="{ name: 'ordersBuildings' }" class="btn btn-primary !py-3 !px-7 font-black text-[11px]">
          NUEVA SOLICITUD
        </RouterLink>
      </template>
    </EmptyState>

    <AppModal
      :open="Boolean(pendingAction)"
      eyebrow="Pedidos"
      :title="pendingAction === 'receive' ? 'Confirmar recepcion' : 'Cancelar pedido'"
      :description="pendingAction === 'receive' ? 'El pedido pasara a entregado y se cargara al inventario local.' : 'El pedido sera cancelado y dejara de estar disponible para despacho.'"
      :confirm-label="pendingAction === 'receive' ? 'Confirmar' : 'Cancelar pedido'"
      :confirm-variant="pendingAction === 'receive' ? 'primary' : 'danger'"
      :loading="ordersStore.isReceivingOrder || ordersStore.isCancellingOrder"
      @close="closeAction"
      @confirm="confirmAction"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import EmptyState from "@/components/ui/EmptyState.vue"
import AppModal from "@/components/ui/AppModal.vue"
import { useBuildingStore } from "@/stores/buildingStore"
import { useOrdersStore } from "@/stores/ordersStore"
import { useUiStore } from "@/stores/uiStore"
import { formatDate } from "@/utils/formatters"
import { normalizeBuilding, normalizeOrder } from "@/utils/normalizers"

const route = useRoute()
const router = useRouter()
const buildingStore = useBuildingStore()
const ordersStore = useOrdersStore()
const uiStore = useUiStore()

const filters = reactive({
  status: "",
  buildingId: "",
})

const pendingAction = ref("")
const pendingOrderId = ref(null)

const statusOptions = [
  { value: "draft", label: "Borrador" },
  { value: "submitted", label: "Enviado" },
  { value: "processing", label: "En proceso" },
  { value: "dispatched", label: "Despachado" },
  { value: "partially_dispatched", label: "Parcialmente Despachado" },
  { value: "delivered", label: "Entregado" },
  { value: "cancelled", label: "Cancelado" },
  { value: "rejected", label: "Rechazado" },
]

const buildings = computed(() => buildingStore.buildings.map(normalizeBuilding))
const orders = computed(() => ordersStore.orders.map(normalizeOrder))

function statusLabel(status) {
  const labels = {
    draft: "Borrador",
    submitted: "Enviado",
    processing: "En proceso",
    dispatched: "Despachado",
    partially_dispatched: "Parcia. Despachado",
    delivered: "Entregado",
    cancelled: "Cancelado",
    rejected: "Rechazado",
  }
  return labels[status] ?? status
}

function statusBadgeClass(status) {
  return {
    draft: "bg-amber/10 text-amber border-amber/20",
    submitted: "bg-cyan-400/10 text-cyan-400 border-cyan-400/20",
    processing: "bg-violet-400/10 text-violet-400 border-violet-400/20",
    dispatched: "bg-blue-400/10 text-blue-400 border-blue-400/20",
    partially_dispatched: "bg-blue-500/5 text-blue-300 border-blue-500/20",
    delivered: "bg-emerald-400/10 text-emerald-400 border-emerald-400/20",
    cancelled: "bg-rose-400/10 text-rose-400 border-rose-400/20",
    rejected: "bg-rose-500/10 text-rose-400 border-rose-500/30",
  }[status] ?? "bg-white/5 text-white/40 border-white/10"
}

function statusDotClass(status) {
  return {
    draft: "bg-amber/10 border-amber/20 text-amber",
    submitted: "bg-cyan-400/10 border-cyan-400/20 text-cyan-400",
    processing: "bg-violet-400/10 border-violet-400/20 text-violet-400",
    dispatched: "bg-blue-400/10 border-blue-400/20 text-blue-400",
    partially_dispatched: "bg-blue-500/10 border-blue-500/20 text-blue-300",
    delivered: "bg-emerald-400/10 border-emerald-400/20 text-emerald-400",
    cancelled: "bg-rose-400/10 border-rose-400/20 text-rose-400",
    rejected: "bg-rose-500/10 border-rose-500/30 text-rose-400",
  }[status] ?? "bg-white/5 border-white/10 text-white/50"
}

async function loadOrders() {
  await ordersStore.fetchOrders({
    status: filters.status || undefined,
    building_id: filters.buildingId ? Number(filters.buildingId) : undefined,
  })
}

async function applyFilters() {
  await router.replace({
    name: "ordersMyOrders",
    query: {
      ...(filters.status ? { status: filters.status } : {}),
      ...(filters.buildingId ? { buildingId: filters.buildingId } : {}),
    },
  })
  await loadOrders()
}

async function clearFilters() {
  filters.status = ""
  filters.buildingId = ""
  await router.replace({ name: "ordersMyOrders" })
  await loadOrders()
}

function openAction(orderId, action) {
  pendingOrderId.value = orderId
  pendingAction.value = action
}

function closeAction() {
  pendingAction.value = ""
  pendingOrderId.value = null
}

async function confirmAction() {
  if (!pendingAction.value || !pendingOrderId.value) {
    return
  }

  try {
    await ordersStore.updateOrderStatus(pendingOrderId.value, pendingAction.value)
    uiStore.success(
      pendingAction.value === "receive" ? "La recepcion fue confirmada." : "El pedido fue cancelado.",
      "Pedido actualizado",
    )
    closeAction()
    await loadOrders()
  } catch (error) {
    uiStore.error(error.message, "No se pudo actualizar el pedido")
  }
}

onMounted(async () => {
  filters.status = typeof route.query.status === "string" ? route.query.status : ""
  filters.buildingId = typeof route.query.buildingId === "string" ? route.query.buildingId : ""
  await Promise.all([buildingStore.fetchBuildings(), loadOrders()])
})
</script>
