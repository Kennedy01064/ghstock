<template>
  <div class="space-y-10">
    <div class="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <span class="eyebrow tracking-[0.3em]">Control de Suministros</span>
        <div class="flex items-center gap-4">
          <h1 class="h2">Inventario Local</h1>
          <span class="px-3 py-1 rounded-lg bg-amber text-navy-deep text-[10px] font-black uppercase tracking-widest shadow-lg shadow-amber/20">ACTIVO</span>
        </div>
        <p class="text-text-muted font-medium text-sm">
          Monitoreo de consumos y disponibilidad de insumos en sedes asignadas.
        </p>
      </div>

      <RouterLink :to="{ name: 'ordersAddInventory' }" class="btn btn-primary shadow-2xl shadow-amber/10 group">
        <svg class="w-5 h-5 transition-transform group-hover:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
        </svg>
        REGISTRAR PRODUCTO
      </RouterLink>
    </div>

    <div v-if="inventoryStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ inventoryStore.error }}
    </div>

    <div v-if="inventoryStore.isLoading && !inventory.length" class="card text-text-muted">
      Cargando inventario...
    </div>

    <div v-else-if="inventory.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
      <InventoryCard
        v-for="item in inventory"
        :key="item.id"
        :inventory="item"
        :is-consuming="inventoryStore.isConsuming"
        :is-adjusting="inventoryStore.isAdjusting"
        @consume="consumeInventory"
        @adjust="adjustInventory"
      />
    </div>

    <EmptyState
      v-else
      title="Sin Existencias Locales"
      description="Aun no se han registrado o despachado suministros hacia sus sedes de gestion."
    >
      <template #action>
        <RouterLink :to="{ name: 'ordersAddInventory' }" class="btn btn-primary !rounded-xl !py-4 shadow-xl shadow-amber/10 px-10">
          INICIAR PRIMER REGISTRO
        </RouterLink>
      </template>
    </EmptyState>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"

import EmptyState from "@/components/ui/EmptyState.vue"
import InventoryCard from "@/components/orders/InventoryCard.vue"
import { useInventoryStore } from "@/stores/inventoryStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizeInventoryItem } from "@/utils/normalizers"

const inventoryStore = useInventoryStore()
const uiStore = useUiStore()
const inventory = computed(() => inventoryStore.items.map(normalizeInventoryItem))

async function consumeInventory({ id, quantity }) {
// ...
  if (inventoryStore.isConsuming || inventoryStore.isAdjusting) return
  try {
    const updated = await inventoryStore.consumeInventory(id, { quantity: Number(quantity) })
    const item = normalizeInventoryItem(updated)
    uiStore.success(`Quedan ${item.quantity} ${item.product.unit} de ${item.product.name}.`, "Consumo registrado")
  } catch (error) {
    uiStore.error(error.message, "No se pudo registrar el consumo")
  }
}

async function adjustInventory({ id, quantity }) {
  if (inventoryStore.isConsuming || inventoryStore.isAdjusting) return
  try {
    const updated = await inventoryStore.adjustInventory(id, { quantity: Number(quantity) })
    const item = normalizeInventoryItem(updated)
    uiStore.success(`Nuevo saldo: ${item.quantity} ${item.product.unit}.`, "Inventario actualizado")
  } catch (error) {
    uiStore.error(error.message, "No se pudo ajustar el inventario")
  }
}

onMounted(() => {
  inventoryStore.fetchInventory()
})
</script>
