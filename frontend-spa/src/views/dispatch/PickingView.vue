<template>
  <div class="space-y-10" v-if="picking">
    <PageHeader
      eyebrow="Picking"
      :title="`Preparacion BATCH-${route.params.batchId}`"
      description="Vista migrada para confirmar cantidades pickeadas antes del despacho final."
      :meta="{ label: 'Items', value: `${items.length}` }"
      :back-to="{ name: 'dispatchBatchDetail', params: { batchId: route.params.batchId } }"
      back-label="Volver al batch"
    />

    <div v-if="dispatchStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ dispatchStore.error }}
    </div>

    <div class="card !p-0 overflow-hidden overflow-x-auto">
      <table class="w-full text-left">
        <thead class="bg-white/[0.03] text-text-muted font-bold text-[10px] uppercase tracking-[0.2em]">
          <tr>
            <th class="px-8 py-4">Producto</th>
            <th class="px-8 py-4">Solicitado</th>
            <th class="px-8 py-4">Pickeado</th>
            <th class="px-8 py-4 text-right">Completar</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/5">
          <tr v-for="item in items" :key="item.id">
            <td class="px-8 py-5 text-sm font-black text-white">{{ item.name }}</td>
            <td class="px-8 py-5 text-sm font-bold text-white">{{ item.requested }} {{ item.unit }}</td>
            <td class="px-8 py-5"><input v-model.number="item.picked" type="number" min="0" :max="item.requested" class="input-field !py-3 max-w-[120px]" /></td>
            <td class="px-8 py-5 text-right"><input :checked="item.picked >= item.requested" type="checkbox" class="h-4 w-4 accent-[#F2AD3D]" /></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex justify-end">
      <button type="button" class="btn btn-primary" :disabled="dispatchStore.isConfirmingBatch" @click="isConfirmOpen = true">
        {{ dispatchStore.isConfirmingBatch ? "Confirmando..." : "Confirmar despacho" }}
      </button>
    </div>

    <AppModal
      :open="isConfirmOpen"
      eyebrow="Picking"
      title="Confirmar despacho"
      description="Se descontara el stock central y las ordenes del batch pasaran a estado despachado."
      confirm-label="Despachar"
      :loading="dispatchStore.isConfirmingBatch"
      @close="isConfirmOpen = false"
      @confirm="confirmDispatch"
    />
  </div>

  <DashboardSkeleton v-else-if="dispatchStore.isLoading" />
  
  <EmptyState
    v-else-if="!dispatchStore.isLoading && !items.length"
    title="Sin items por pickear"
    description="No hay productos registrados en este batch para preparacion."
  />
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"

import PageHeader from "@/components/page/PageHeader.vue"
import AppModal from "@/components/ui/AppModal.vue"
import EmptyState from "@/components/ui/EmptyState.vue"
import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import { useDispatchStore } from "@/stores/dispatchStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizePickingResponse } from "@/utils/normalizers"

const route = useRoute()
const dispatchStore = useDispatchStore()
const uiStore = useUiStore()
const isConfirmOpen = ref(false)

const picking = computed(() => (dispatchStore.currentPicking ? normalizePickingResponse(dispatchStore.currentPicking) : null))
const items = computed(() => picking.value?.items ?? [])

async function confirmDispatch() {
  if (dispatchStore.isConfirmingBatch) return
  try {
    const result = await dispatchStore.confirmBatch(route.params.batchId)
    isConfirmOpen.value = false
    uiStore.success(result.message, "Despacho confirmado")
  } catch (error) {
    uiStore.error(error.message, "No se pudo confirmar el despacho")
  }
}

onMounted(() => {
  dispatchStore.fetchPicking(route.params.batchId)
})
</script>
