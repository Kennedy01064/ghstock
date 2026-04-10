<template>
  <div class="max-w-4xl mx-auto space-y-10 pb-32">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 px-2">
      <div class="space-y-2">
        <span class="eyebrow tracking-[0.4em] !text-amber">Operaciones de Almacen</span>
        <h1 class="h2 italic !tracking-tighter">Entrada Manual</h1>
        <p class="text-text-muted font-medium text-sm">
          Registro excepcional de suministros fuera del flujo de despacho estandar.
        </p>
      </div>
      <div class="h-14 w-14 rounded-3xl bg-amber/10 border border-amber/20 flex items-center justify-center text-amber shadow-2xl shadow-amber/10 shrink-0">
        <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
        </svg>
      </div>
    </div>

    <div v-if="inventoryStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ inventoryStore.error }}
    </div>

    <form class="space-y-8" @submit.prevent="submitForm">
      <div class="card bg-navy-accent/40 border-white/5 shadow-[0_30px_60px_-15px_rgba(0,0,0,0.5)]">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="space-y-3">
            <label class="eyebrow !text-text-muted">Sede de Recepcion <span class="text-amber">*</span></label>
            <template v-if="authStore.isManagement">
              <select v-model="form.buildingId" required class="select-field">
                <option disabled value="">Seleccionar destino...</option>
                <option v-for="building in buildingOptions" :key="building.id" :value="String(building.id)">
                  {{ building.name }}
                </option>
              </select>
            </template>
            <template v-else>
              <div class="input-field bg-white/[0.02] border-white/5 text-white/40 flex items-center gap-3">
                <div class="w-1.5 h-1.5 rounded-full bg-amber/40 shadow-sm" />
                <span class="font-black uppercase tracking-widest text-[11px]">
                  {{ selectedBuildingLabel || "Sin Sede Vinculada" }}
                </span>
              </div>
            </template>
          </div>

          <div class="space-y-3">
            <label class="eyebrow !text-text-muted">Insumo a Registrar <span class="text-amber">*</span></label>
            <select v-model="form.productId" required class="select-field">
              <option disabled value="">Localizar producto...</option>
              <option v-for="product in productOptions" :key="product.id" :value="String(product.id)">
                {{ product.name }} | {{ product.categoria }}
              </option>
            </select>
          </div>

          <div class="space-y-3 md:col-span-2">
            <label class="eyebrow !text-text-muted">Volumen de Ingreso <span class="text-amber">*</span></label>
            <div class="relative group max-w-md">
              <input
                v-model.number="form.quantity"
                type="number"
                min="1"
                required
                class="input-field pl-12 font-black text-amber text-lg tracking-widest focus:text-white transition-all shadow-inner bg-white/5"
              >
              <div class="absolute left-4 top-1/2 -translate-y-1/2 text-amber/40 group-focus-within:text-amber transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M7 20l4-16m2 16l4-16" />
                </svg>
              </div>
            </div>
            <p class="text-[10px] font-medium text-text-muted italic">
              Especifique la cantidad fisica recibida en sede.
            </p>
          </div>
        </div>
      </div>

      <div class="flex flex-col sm:flex-row items-center justify-end gap-4 pt-4 border-t border-white/5">
        <RouterLink :to="{ name: 'ordersMyInventory' }" class="btn btn-secondary w-full sm:w-auto px-10 !rounded-2xl border-white/10 hover:border-white/20">
          DESCARTAR
        </RouterLink>
        <button type="submit" class="btn btn-primary w-full sm:w-auto px-12 !py-4 shadow-2xl shadow-amber/10 group" :disabled="inventoryStore.isSubmittingEntry">
          <span class="tracking-widest font-black text-xs">
            {{ inventoryStore.isSubmittingEntry ? "PROCESANDO..." : "EJECUTAR INGRESO" }}
          </span>
          <svg v-if="!inventoryStore.isSubmittingEntry" class="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
          <svg v-else class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive } from "vue"
import { useRouter } from "vue-router"

import { useAuthStore } from "@/stores/authStore"
import { useBuildingStore } from "@/stores/buildingStore"
import { useProductStore } from "@/stores/productStore"
import { useInventoryStore } from "@/stores/inventoryStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizeBuilding, normalizeProduct } from "@/utils/normalizers"

const router = useRouter()
const authStore = useAuthStore()
const buildingStore = useBuildingStore()
const productStore = useProductStore()
const inventoryStore = useInventoryStore()
const uiStore = useUiStore()

const form = reactive({
  buildingId: "",
  productId: "",
  quantity: 1,
})

const buildingOptions = computed(() => buildingStore.buildings.map(normalizeBuilding))
const productOptions = computed(() => productStore.products.map(normalizeProduct))
const selectedBuildingLabel = computed(() => buildingOptions.value.find((item) => String(item.id) === String(form.buildingId))?.name ?? "")

async function submitForm() {
  if (inventoryStore.isSubmittingEntry) return
  try {
    await inventoryStore.addInventory({
      building_id: Number(form.buildingId),
      product_id: Number(form.productId),
      quantity: Number(form.quantity),
    })
    await inventoryStore.fetchInventory(Number(form.buildingId))
    uiStore.success("El ingreso manual fue registrado correctamente.", "Inventario actualizado")
    await router.push({ name: "ordersMyInventory" })
  } catch (error) {
    uiStore.error(error.message, "No se pudo registrar el ingreso")
  }
}

onMounted(async () => {
  await Promise.all([buildingStore.fetchBuildings(), productStore.fetchProducts()])
  form.buildingId = buildingOptions.value[0] ? String(buildingOptions.value[0].id) : ""
  form.productId = productOptions.value[0] ? String(productOptions.value[0].id) : ""
})
</script>
