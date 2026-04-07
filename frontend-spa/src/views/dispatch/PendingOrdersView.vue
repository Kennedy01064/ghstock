<template>
  <div class="space-y-10">
    <PageHeader
      eyebrow="Despacho"
      title="Ordenes pendientes"
      description="Selecciona solicitudes para consolidarlas en batches sin abandonar el shell de la SPA."
      :meta="{ label: 'Pendientes', value: `${pendingOrders.length}` }"
    />

    <div v-if="dispatchStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ dispatchStore.error }}
    </div>

    <DashboardSkeleton v-if="dispatchStore.isLoading && !pendingOrders.length" />
    
    <EmptyState
      v-else-if="!dispatchStore.isLoading && !pendingOrders.length"
      title="Sin ordenes pendientes"
      description="No hay solicitudes de edificios esperando consolidacion en este momento."
    />

    <div v-else class="space-y-5">
      <article v-for="order in pendingOrders" :key="order.id" class="card">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5">
          <div>
            <div class="flex items-center gap-3">
              <input v-model="selectedOrderIds" type="checkbox" :value="order.id" class="h-4 w-4 accent-[#F2AD3D]" />
              <h3 class="text-lg font-black text-white">Orden #{{ order.id }} - {{ order.buildingName }}</h3>
            </div>
            <p class="text-[11px] uppercase tracking-[0.18em] text-text-muted mt-3">{{ order.items.length }} items - {{ order.createdBy?.name || 'Sin usuario' }}</p>
          </div>
          <div class="flex gap-3">
            <RouterLink :to="{ name: 'ordersOrderDetail', params: { orderId: order.id } }" class="btn btn-secondary">Ver detalle</RouterLink>
          </div>
        </div>
      </article>
    </div>

    <div class="card flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <span class="section-label">Seleccion actual</span>
        <p class="text-white font-black text-xl">{{ selectedOrderIds.length }} orden(es)</p>
      </div>
      <button type="button" class="btn btn-primary" :disabled="!selectedOrderIds.length || dispatchStore.isConsolidating" @click="isConfirmOpen = true">
        {{ dispatchStore.isConsolidating ? "Consolidando..." : "Consolidar en batch" }}
      </button>
    </div>

    <div v-if="latestBatchId" class="card border border-emerald-500/20 bg-emerald-500/10 text-emerald-300 text-sm flex items-center justify-between gap-4">
      <span>Batch #{{ latestBatchId }} creado correctamente.</span>
      <RouterLink :to="{ name: 'dispatchBatchDetail', params: { batchId: latestBatchId } }" class="btn btn-secondary !min-h-[40px] !px-4">
        Ver batch
      </RouterLink>
    </div>

    <AppModal
      :open="isConfirmOpen"
      eyebrow="Despacho"
      title="Consolidar ordenes"
      :description="`Se consolidaran ${selectedOrderIds.length} orden(es) en un nuevo batch.`"
      confirm-label="Crear batch"
      :loading="dispatchStore.isConsolidating"
      @close="isConfirmOpen = false"
      @confirm="consolidate"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"

import PageHeader from "@/components/page/PageHeader.vue"
import AppModal from "@/components/ui/AppModal.vue"
import EmptyState from "@/components/ui/EmptyState.vue"
import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import { useDispatchStore } from "@/stores/dispatchStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizeOrder } from "@/utils/normalizers"

const dispatchStore = useDispatchStore()
const uiStore = useUiStore()
const selectedOrderIds = ref([])
const latestBatchId = ref(null)
const isConfirmOpen = ref(false)
const pendingOrders = computed(() => dispatchStore.pendingOrders.map(normalizeOrder))

async function consolidate() {
  if (dispatchStore.isConsolidating) return

  try {
    const result = await dispatchStore.consolidateOrders(selectedOrderIds.value)
    latestBatchId.value = result.batch_id
    selectedOrderIds.value = []
    isConfirmOpen.value = false
    await dispatchStore.fetchPendingOrders()
    uiStore.success(`Batch #${result.batch_id} creado con ${result.orders_count} orden(es).`, "Consolidacion completada")
  } catch (error) {
    uiStore.error(error.message, "No se pudo consolidar el batch")
  }
}

onMounted(() => {
  dispatchStore.fetchPendingOrders()
})
</script>
