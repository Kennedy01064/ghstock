<template>
  <div class="max-w-[1320px] mx-auto space-y-12 pb-32 px-4">
    <div class="flex flex-col xl:flex-row xl:items-end justify-between gap-10 border-b border-white/5 pb-10">
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-6 bg-amber rounded-full shadow-[0_0_12px_rgba(242,173,61,0.4)]"></div>
          <span class="eyebrow tracking-[0.4em] !text-white text-[10px]">Logistica Central</span>
        </div>
        <h1 class="text-4xl font-black tracking-tight text-white">Almacen Maestro</h1>
        <p class="text-text-muted font-medium text-sm max-w-xl">Control volumetrico y gestion tecnica de existencias corporativas con sincronizacion en tiempo real.</p>
      </div>

      <div class="flex flex-col md:flex-row items-center gap-4 w-full xl:w-auto">
        <div class="relative w-full md:w-96 group">
          <input v-model="query" type="text" placeholder="Filtrar por SKU o Nombre..." class="input-field !pl-12 shadow-xl transition-all" />
          <div class="absolute left-4 top-1/2 -translate-y-1/2 transition-colors group-focus-within:text-amber text-text-muted">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        <div class="flex items-center gap-3 w-full xl:w-auto">
          <button type="button" class="btn btn-secondary !rounded-xl px-6 !h-[52px] group/web" @click="isDynamicModalOpen = true">
            <svg class="w-5 h-5 transition-transform group-hover/web:rotate-180 duration-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
            <span class="font-bold text-[11px] tracking-widest uppercase">Web Scraping</span>
          </button>
          <RouterLink :to="{ name: 'catalogUploadCsv' }" class="btn btn-secondary !rounded-xl px-5 !h-[52px]">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <span class="font-bold text-[11px] tracking-widest uppercase">CSV</span>
          </RouterLink>
          <RouterLink :to="{ name: 'catalogProductCreate' }" class="btn btn-primary !rounded-xl px-6 !h-[52px] shadow-lg shadow-amber/10">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
            </svg>
            <span class="font-bold text-[11px] tracking-widest uppercase text-navy-deep">Anadir Item</span>
          </RouterLink>
        </div>
      </div>
    </div>

    <div v-if="catalogStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ catalogStore.error }}
    </div>

    <div v-if="catalogStore.isLoading" class="space-y-6">
      <DashboardSkeleton />
    </div>

    <div v-else-if="!filteredProducts.length" class="py-12">
      <EmptyState
        :title="query.trim() ? 'Sin resultados' : 'Catalogo vacio'"
        :description="query.trim() ? `No encontramos coincidencias para '${query}'.` : 'No hay productos registrados en el sistema.'"
      />
    </div>

    <div v-else class="card !p-0 overflow-hidden border-white/5 bg-white/[0.01] backdrop-blur-3xl shadow-[0_32px_64px_-16px_rgba(0,0,0,0.5)]">
      <WarehouseRows :products="filteredProducts" @toggle="toggleProduct" @sync="syncProduct" />
    </div>

    <div class="flex items-center justify-between px-2 pt-4 border-t border-white/5">
      <p class="text-[10px] font-black uppercase tracking-[0.4em] text-text-muted/50">Grupo Hernandez - Logistica Vulcano (C) 2026</p>
      <div class="flex gap-8">
        <div class="flex items-center gap-3">
          <span class="text-[10px] font-black text-text-muted uppercase tracking-widest">Sistema Optimizado</span>
          <span class="text-sm font-black text-amber italic tracking-tighter">Alta Velocidad</span>
        </div>
      </div>
    </div>

    <AppModal
      :open="Boolean(pendingProduct)"
      eyebrow="Catalogo maestro"
      :title="pendingProduct?.active ? 'Desactivar producto' : 'Activar producto'"
      :description="pendingProduct ? `Confirma el cambio de estado para ${pendingProduct.name}.` : ''"
      :confirm-label="pendingProduct?.active ? 'Desactivar' : 'Activar'"
      :loading="catalogStore.isTogglingProduct"
      @close="pendingProductId = null"
      @confirm="confirmToggle"
    />

    <Transition name="modal-fade">
      <div v-if="isDynamicModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center bg-navy-deep/95 backdrop-blur-md p-6">
        <div class="card w-full max-w-2xl !bg-navy-accent/50 border-white/10 !p-10 animate-in fade-in zoom-in duration-500 shadow-[0_64px_128px_-32px_rgba(0,0,0,0.8)] relative overflow-hidden">
          <div class="absolute top-0 right-0 w-64 h-64 bg-amber/5 rounded-full blur-[100px] -mr-32 -mt-32"></div>

          <div class="flex items-center justify-between mb-10 relative z-10">
            <div class="space-y-2">
              <div class="flex items-center gap-2.5">
                <div class="w-1.5 h-4 bg-amber rounded-full"></div>
                <span class="eyebrow !text-amber text-[10px]">Inteligencia Artificial</span>
              </div>
              <h3 class="text-3xl font-black text-white tracking-tight">Importacion Dinamica</h3>
              <p class="text-text-muted text-sm font-medium">Extraiga metadatos tecnicos directamente desde portales retail.</p>
            </div>
            <button type="button" class="w-12 h-12 rounded-2xl hover:bg-white/10 flex items-center justify-center transition-all hover:rotate-90 group" @click="closeDynamicModal">
              <svg class="w-6 h-6 text-white group-hover:text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="space-y-8 relative z-10">
            <div class="space-y-3">
              <label class="label-premium px-1">Enlace del Producto Corporativo</label>
              <div class="flex gap-3">
                <div class="relative grow group">
                  <input v-model="dynamicUrl" type="url" placeholder="https://www.sodimac.com.pe/..." class="input-field !pl-12 !h-16 grow font-bold shadow-inner" />
                  <svg class="w-5 h-5 text-white/20 absolute left-4 top-1/2 -translate-y-1/2 transition-colors group-focus-within:text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.803a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
                <button type="button" class="btn btn-primary !h-16 px-10 !rounded-2xl group/scrape shadow-xl shadow-amber/10" :disabled="catalogStore.isPreviewingProduct" @click="previewProduct">
                  <span class="tracking-widest font-black text-xs">{{ catalogStore.isPreviewingProduct && !dynamicPreview ? "Procesando" : "Extraer" }}</span>
                  <svg class="w-5 h-5 transition-transform group-hover/scrape:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </button>
              </div>
            </div>

            <div v-if="isPreviewLoading" class="flex flex-col items-center justify-center py-16 space-y-6">
              <div class="relative">
                <div class="w-16 h-16 border-4 border-white/10 rounded-full"></div>
                <div class="w-16 h-16 border-4 border-amber border-t-transparent rounded-full animate-spin absolute inset-0 shadow-[0_0_20px_rgba(242,173,61,0.3)]"></div>
              </div>
              <div class="text-center space-y-2">
                <p class="text-xs font-black text-white uppercase tracking-[0.3em] animate-pulse">Analizando Esquema de Datos</p>
                <p class="text-[10px] font-bold text-text-muted uppercase tracking-[0.1em]">Conectando con servidores retail...</p>
              </div>
            </div>

            <div v-else-if="dynamicPreview" class="p-8 rounded-3xl border border-white/10 bg-white/5 space-y-6 animate-in slide-in-from-bottom-5 duration-700">
              <div class="flex gap-6">
                <div class="w-32 h-32 rounded-2xl bg-navy-deep overflow-hidden border border-white/10 shrink-0 shadow-2xl">
                  <img :src="dynamicPreview.image_url || defaultProductUrl" class="w-full h-full object-cover" />
                </div>
                <div class="grow min-w-0 space-y-3">
                  <h4 class="text-xl font-black text-white truncate leading-tight uppercase">{{ dynamicPreview.name || "Nombre del Producto" }}</h4>
                  <div class="flex items-center gap-4">
                    <p class="text-3xl font-black text-amber leading-none">S/ {{ previewPrice }}</p>
                    <div class="h-6 w-px bg-white/10"></div>
                    <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.3em]">SKU: {{ dynamicPreview.sku || "N/A" }}</p>
                  </div>
                </div>
              </div>
              <div class="pt-6 border-t border-white/10">
                <button type="button" class="btn btn-primary w-full !h-16 !rounded-2xl shadow-2xl shadow-amber/20" :disabled="catalogStore.isSubmittingProduct" @click="saveDynamicProduct">
                  <span class="tracking-widest font-black text-sm">Vincular al Catalogo Maestro</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"

import WarehouseRows from "@/components/catalog/WarehouseRows.vue"
import AppModal from "@/components/ui/AppModal.vue"
import EmptyState from "@/components/ui/EmptyState.vue"
import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import { useCatalogStore } from "@/stores/catalogStore"
import { useUiStore } from "@/stores/uiStore"
import { defaultProductUrl } from "@/utils/formatters"
import { normalizeProduct } from "@/utils/normalizers"

const catalogStore = useCatalogStore()
const uiStore = useUiStore()
const query = ref("")
const pendingProductId = ref(null)
const isDynamicModalOpen = ref(false)
const dynamicUrl = ref("")
const dynamicPreview = ref(null)
const isPreviewLoading = ref(false)

const normalizedProducts = computed(() => catalogStore.products.map(normalizeProduct))
const filteredProducts = computed(() => {
  const term = query.value.trim().toLowerCase()

  if (!term) {
    return normalizedProducts.value
  }

  return normalizedProducts.value.filter((product) =>
    `${product.name} ${product.sku ?? ""}`.toLowerCase().includes(term),
  )
})
const pendingProduct = computed(() => normalizedProducts.value.find((product) => product.id === pendingProductId.value) ?? null)
const previewPrice = computed(() => Number(dynamicPreview.value?.price ?? 0).toFixed(2))

onMounted(() => {
  catalogStore.fetchProducts()
})

function toggleProduct(productId) {
  pendingProductId.value = productId
}

async function confirmToggle() {
  if (!pendingProduct.value) {
    return
  }

  try {
    await catalogStore.toggleProduct(pendingProduct.value.id)
    uiStore.success(
      `${pendingProduct.value.name} ahora esta ${pendingProduct.value.active ? "inactivo" : "activo"}.`,
      "Estado actualizado",
    )
    pendingProductId.value = null
  } catch (error) {
    uiStore.error(error.message, "No se pudo actualizar el producto")
  }
}

async function syncProduct(productId) {
  const product = normalizedProducts.value.find((item) => item.id === productId)

  if (!product) {
    return
  }

  try {
    await catalogStore.syncProduct(productId)
    uiStore.success(`Se sincronizo ${product.name}.`, "Producto actualizado")
  } catch (error) {
    uiStore.error(error.message, "No se pudo sincronizar el producto")
  }
}

function closeDynamicModal() {
  isDynamicModalOpen.value = false
  dynamicUrl.value = ""
  dynamicPreview.value = null
  isPreviewLoading.value = false
}

async function previewProduct() {
  if (!dynamicUrl.value.trim()) {
    uiStore.warning("Ingresa un enlace valido para continuar.", "Atencion corporativa")
    return
  }

  isPreviewLoading.value = true
  dynamicPreview.value = null

  try {
    dynamicPreview.value = await catalogStore.previewProduct(dynamicUrl.value.trim())
  } catch (error) {
    uiStore.error(error.message, "Fallo de protocolo")
  } finally {
    isPreviewLoading.value = false
  }
}

async function saveDynamicProduct() {
  if (!dynamicPreview.value) {
    return
  }

  try {
    await catalogStore.createProduct({
      sku: dynamicPreview.value.sku || null,
      name: dynamicPreview.value.name || "Producto dinamico",
      description: dynamicPreview.value.description || null,
      precio: Number(dynamicPreview.value.price || 0),
      imagen_url: dynamicPreview.value.image_url || defaultProductUrl,
      source_url: dynamicUrl.value.trim(),
      is_dynamic: true,
      unit: "Unidad",
    })
    uiStore.success(`${dynamicPreview.value.name} fue vinculado al catalogo.`, "Importacion completada")
    closeDynamicModal()
  } catch (error) {
    uiStore.error(error.message, "Error de guardado")
  }
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #f2ad3d;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.24s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
