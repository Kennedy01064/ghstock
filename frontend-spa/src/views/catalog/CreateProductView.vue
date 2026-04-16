<template>
  <div class="max-w-[1320px] mx-auto space-y-12 pb-32 px-4">
    <div class="flex flex-col gap-6 border-b border-white/[0.07] pb-10">
      <RouterLink :to="{ name: 'catalogWarehouse' }" class="inline-flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.2em] text-text-muted hover:text-amber transition-colors group">
        <svg class="w-4 h-4 transition-transform group-hover:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Volver al Almacen
      </RouterLink>

      <div class="flex items-center justify-between">
        <div class="space-y-2">
          <span class="eyebrow">Catalogo Maestro</span>
          <h1 class="h2">Nuevo Registro</h1>
          <p class="text-text-muted font-medium">Añadir item al inventario central de Grupo Hernandez</p>
        </div>
        <div class="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl border border-white/[0.12] bg-white/[0.04] shadow-inner">
          <svg class="w-7 h-7 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>
    </div>

    <div v-if="submitError" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ submitError }}
    </div>

    <div class="max-w-2xl">
      <div class="card p-10">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div class="space-y-2">
            <label class="label-premium">Nombre Comercial <span class="text-amber">*</span></label>
            <input data-testid="product-name" v-model="form.name" type="text" required placeholder="Ej: Jabon Liquido 5L Industrial" class="input-field font-bold">
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="label-premium">Codigo SKU</label>
              <input data-testid="product-sku" v-model="form.sku" type="text" placeholder="Identificador unico" class="input-field uppercase tracking-wider">
            </div>
            <div class="space-y-2">
              <label class="label-premium">Unidad de Medida</label>
              <input v-model="form.unit" type="text" placeholder="Ej: Galon, Caja, Unidad" class="input-field">
            </div>
            <div class="space-y-2">
              <label class="label-premium">Precio Unitario (S/)</label>
              <div class="relative">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-amber font-bold">S/</span>
                <input data-testid="product-price" v-model.number="form.price" type="number" min="0" step="0.01" class="input-field !pl-10 font-bold text-amber">
              </div>
            </div>
            <div class="space-y-2">
              <label class="label-premium">Stock Inicial</label>
              <input v-model.number="form.stockActual" type="number" min="0" class="input-field">
            </div>
          </div>

          <div class="space-y-2">
            <label class="label-premium">Descripcion Tecnica</label>
            <textarea v-model="form.description" rows="4" placeholder="Detalles de composicion o uso tecnico..." class="input-field min-h-[120px] resize-none" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="label-premium">Categoria</label>
              <input v-model="form.category" type="text" placeholder="General" class="input-field">
            </div>
            <div class="space-y-2">
              <label class="label-premium">Stock Minimo</label>
              <input v-model.number="form.stockMinimo" type="number" min="0" class="input-field">
            </div>
          </div>

          <div class="space-y-3">
            <label class="label-premium">Fotografia del Activo</label>
            <input v-model="form.imageUrl" type="text" placeholder="/static/img/default-product.png o https://..." class="input-field">
            <div v-if="productPreview" class="flex items-center gap-6 p-4 rounded-2xl bg-white/[0.03] border border-white/[0.12] w-fit">
              <img :src="productPreview" alt="Preview" class="h-24 w-24 object-cover rounded-xl shadow-lg border border-white/[0.12]">
              <div class="space-y-1">
                <p class="text-xs font-black text-slate-900 uppercase tracking-widest">Vista Actual</p>
                <p class="text-[10px] font-medium text-text-muted">La API actual recibe la ruta o URL de la imagen.</p>
              </div>
            </div>
          </div>

          <div class="space-y-2">
            <label class="label-premium">URL de referencia</label>
            <input v-model="form.sourceUrl" type="url" placeholder="https://proveedor.com/item" class="input-field">
          </div>

          <div class="pt-10 flex flex-col md:flex-row gap-4 border-t border-white/[0.07]">
            <RouterLink :to="{ name: 'catalogWarehouse' }" class="btn btn-secondary flex-1 !h-[56px] !rounded-xl">
              <span class="font-bold text-[11px] tracking-widest uppercase">CANCELAR</span>
            </RouterLink>
            <button data-testid="product-submit" type="submit" class="btn btn-primary flex-1 !h-[56px] !rounded-xl shadow-lg shadow-amber/10" :disabled="productStore.isSubmitting">
              <svg v-if="!productStore.isSubmitting" class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else class="w-5 h-5 mr-1 animate-spin" fill="none" stroke="currentColor" viewBox="2 2 20 20">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span class="font-bold text-[11px] tracking-widest uppercase text-navy-deep">
                {{ productStore.isSubmitting ? "REGISTRANDO..." : "REGISTRAR PRODUCTO" }}
              </span>
            </button>
          </div>
        </form>
      </div>

      <div class="flex items-center gap-4 p-5 rounded-2xl bg-white/[0.02] border border-white/[0.07] mt-6">
        <div class="h-10 w-10 flex items-center justify-center rounded-xl bg-white border border-white/[0.12] text-amber shrink-0">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[11px] font-medium text-text-muted leading-relaxed">
          <span class="text-slate-900 font-bold">INFO:</span> Los productos registrados aqui apareceran inmediatamente en el Catalogo Maestro y podran ser asignados a despachos masivos.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue"
import { useRouter } from "vue-router"

import { useProductStore } from "@/stores/productStore"
import { useUiStore } from "@/stores/uiStore"
import { assetUrl, defaultProductUrl } from "@/utils/formatters"

const router = useRouter()
const productStore = useProductStore()
const uiStore = useUiStore()

const submitError = ref("")
const form = reactive({
  name: "",
  sku: "",
  unit: "",
  price: 0,
  stockActual: 0,
  description: "",
  category: "General",
  stockMinimo: 10,
  imageUrl: defaultProductUrl,
  sourceUrl: "",
})

const productPreview = computed(() => assetUrl(form.imageUrl, defaultProductUrl))

async function submitForm() {
  if (productStore.isSubmitting) return
  submitError.value = ""

  try {
    await productStore.createProduct({
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
      is_active: true,
      is_dynamic: false,
    })
    uiStore.success("El producto fue registrado correctamente.", "Catalogo actualizado")
    await router.push({ name: "catalogWarehouse" })
  } catch (error) {
    if (error.isConflict) {
      uiStore.error("Ya existe un producto con este SKU o Nombre comercial.", "Conflicto de Catalogo")
      submitError.value = "Identificador SKU o Nombre ya registrado."
    } else {
      submitError.value = error.message
    }
  }
}
</script>

