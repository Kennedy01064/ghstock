<template>
  <div v-if="catalogStore.isLoading && !product" class="card text-text-secondary">
    Cargando producto...
  </div>

  <div v-else-if="product" class="max-w-2xl mx-auto space-y-8 pb-20 px-4">
    <div class="flex flex-col gap-6">
      <RouterLink :to="{ name: 'catalogWarehouse' }" class="inline-flex items-center gap-2 text-[11px] font-black uppercase tracking-[0.2em] text-text-muted hover:text-amber transition-colors group">
        <svg class="w-4 h-4 transition-transform group-hover:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Cerrar Edicion
      </RouterLink>

      <div class="flex items-center justify-between">
        <div class="space-y-2">
          <span class="eyebrow">Edicion Tecnica</span>
          <h1 class="h2">Modificar Activo</h1>
          <p class="text-text-muted font-medium">Actualizando parametros de: <span class="text-white">{{ product.name }}</span></p>
        </div>
        <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-white/10 bg-white/5 shadow-inner">
          <svg class="w-6 h-6 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </div>
      </div>
    </div>

    <div v-if="submitError" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ submitError }}
    </div>

    <div class="card">
      <form class="space-y-6" @submit.prevent="submitForm">
        <div class="space-y-2">
          <label class="label-premium">Nombre Comercial <span class="text-amber">*</span></label>
          <input v-model="form.name" type="text" required class="input-field font-bold">
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="label-premium">Codigo SKU</label>
            <input v-model="form.sku" type="text" class="input-field uppercase tracking-wider">
          </div>
          <div class="space-y-2">
            <label class="label-premium">Unidad de Medida</label>
            <input v-model="form.unit" type="text" class="input-field">
          </div>
          <div class="space-y-2">
            <label class="label-premium">Precio Unitario (S/)</label>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-amber font-black">S/</span>
              <input v-model.number="form.price" type="number" step="0.01" min="0" class="input-field !pl-10 font-bold text-amber">
            </div>
          </div>
          <div class="space-y-2">
            <label class="label-premium">Stock Actual</label>
            <input v-model.number="form.stockActual" type="number" min="0" class="input-field">
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="label-premium">Categoria</label>
            <input v-model="form.category" type="text" class="input-field">
          </div>
          <div class="space-y-2">
            <label class="label-premium">Stock Minimo</label>
            <input v-model.number="form.stockMinimo" type="number" min="0" class="input-field">
          </div>
        </div>

        <div class="space-y-2">
          <label class="label-premium">Descripcion Tecnica</label>
          <textarea v-model="form.description" rows="3" class="input-field min-h-[100px] resize-none" />
        </div>

        <div class="space-y-4">
          <label class="label-premium">Fotografia del Activo</label>
          <div v-if="productPreview" class="flex items-center gap-6 p-4 rounded-2xl bg-white/[0.03] border border-white/10 w-fit">
            <div class="relative group">
              <img :src="productPreview" alt="Actual" class="h-24 w-24 object-cover rounded-xl shadow-lg border border-white/10 group-hover:border-amber/40 transition-all">
            </div>
            <div class="space-y-1">
              <p class="text-xs font-black text-white uppercase tracking-widest">Imagen Actual</p>
              <p class="text-[10px] font-medium text-text-muted">Actualice la ruta o URL para reemplazar la imagen.</p>
            </div>
          </div>
          <input v-model="form.imageUrl" type="text" class="input-field" placeholder="/static/img/default-product.png o https://...">
        </div>

        <div class="space-y-2">
          <label class="label-premium">URL de referencia</label>
          <input v-model="form.sourceUrl" type="url" class="input-field" placeholder="https://proveedor.com/item">
        </div>

        <div class="flex items-center gap-3 rounded-xl bg-white/[0.03] border border-white/10 px-4 py-3">
          <input id="active" v-model="form.active" type="checkbox" class="w-4 h-4 rounded border-white/10 bg-navy-deep text-amber focus:ring-amber/40 focus:ring-offset-navy-deep">
          <label for="active" class="text-[11px] font-bold text-white uppercase tracking-widest">Producto activo para despacho</label>
        </div>

        <div class="pt-6 flex flex-col md:flex-row gap-4 border-t border-white/10">
          <RouterLink :to="{ name: 'catalogWarehouse' }" class="btn btn-secondary flex-1">Descartar Cambios</RouterLink>
          <button type="submit" class="btn btn-primary flex-1 shadow-2xl shadow-amber/10" :disabled="catalogStore.isSubmittingProduct">
            <svg v-if="!catalogStore.isSubmittingProduct" class="w-5 h-5 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else class="w-5 h-5 mx-1 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ catalogStore.isSubmittingProduct ? "ACTUALIZANDO..." : "Actualizar Registro" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import { useCatalogStore } from "@/stores/catalogStore"
import { useUiStore } from "@/stores/uiStore"
import { assetUrl, defaultProductUrl } from "@/utils/formatters"
import { normalizeProduct } from "@/utils/normalizers"

const route = useRoute()
const router = useRouter()
const catalogStore = useCatalogStore()
const uiStore = useUiStore()

const submitError = ref("")
const form = reactive({
  name: "",
  sku: "",
  unit: "",
  price: 0,
  stockActual: 0,
  category: "General",
  stockMinimo: 10,
  description: "",
  imageUrl: "",
  sourceUrl: "",
  active: true,
})

const product = computed(() => (catalogStore.currentProduct ? normalizeProduct(catalogStore.currentProduct) : null))
const productPreview = computed(() => assetUrl(form.imageUrl, defaultProductUrl))

async function submitForm() {
  if (catalogStore.isSubmittingProduct) return
  submitError.value = ""

  try {
    await catalogStore.updateProduct(route.params.productId, {
      name: form.name,
      sku: form.sku || null,
      categoria: form.category || "General",
      description: form.description || null,
      unit: form.unit || null,
      precio: Number(form.price || 0),
      imagen_url: form.imageUrl || defaultProductUrl,
      stock_actual: Number(form.stockActual || 0),
      stock_minimo: Number(form.stockMinimo || 10),
      source_url: form.sourceUrl || null,
      is_active: Boolean(form.active),
    })
    uiStore.success("El producto fue actualizado correctamente.", "Catalogo sincronizado")
    await router.push({ name: "catalogWarehouse" })
  } catch (error) {
    if (error.isConflict) {
      submitError.value = "Ya existe otro producto con este SKU o Nombre. El cambio fue rechazado."
    } else {
      submitError.value = error.message
    }
  }
}

onMounted(async () => {
  await catalogStore.fetchProduct(route.params.productId)

  if (product.value) {
    form.name = product.value.name
    form.sku = product.value.sku || ""
    form.unit = product.value.unit || ""
    form.price = product.value.price || 0
    form.stockActual = product.value.stockActual || 0
    form.category = product.value.categoria || "General"
    form.stockMinimo = product.value.stockMinimo || 10
    form.description = product.value.description || ""
    form.imageUrl = product.value.imagen_url || defaultProductUrl
    form.sourceUrl = product.value.source_url || ""
    form.active = product.value.active ?? true
  }
})
</script>
