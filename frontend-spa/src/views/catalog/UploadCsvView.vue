<template>
  <div class="max-w-[1320px] mx-auto space-y-12 pb-32 px-4">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-white/[0.07] pb-10">
      <div class="space-y-2">
        <span class="eyebrow">Catalogo Maestro</span>
        <h1 class="text-4xl font-black tracking-tight text-slate-900">Importacion de Productos</h1>
        <p class="text-text-muted font-medium">Gestion centralizada de inventario via CSV</p>
      </div>
      <div class="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl border border-white/[0.12] bg-white/[0.04] shadow-inner">
        <svg class="w-7 h-7 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
      </div>
    </div>

    <div class="max-w-3xl">
      <div class="card overflow-hidden !p-0">
        <div class="bg-white/[0.02] px-10 py-8 border-b border-white/[0.07]">
          <div class="flex items-center space-x-6">
            <div class="bg-amber/10 border border-amber/10 rounded-2xl p-4 shadow-inner">
              <svg class="w-7 h-7 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <h3 class="font-bold text-xl text-slate-900 tracking-tight">Subir Archivo CSV</h3>
              <p class="text-text-muted text-[13px] font-medium mt-1">Actualizacion masiva de SKUs y Existencias</p>
            </div>
          </div>
        </div>

        <form class="p-10 space-y-10" @submit.prevent="handleUpload">
          <div class="relative">
            <label for="csv_file" class="block cursor-pointer group">
              <div class="border-2 border-dashed border-white/[0.07] rounded-2xl p-16 text-center group-hover:border-amber/40 group-hover:bg-white/[0.01] transition-all duration-700">
                <div class="mx-auto h-20 w-20 bg-white/[0.04] rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-500 border border-white/[0.12]">
                  <svg class="h-8 w-8 text-text-muted group-hover:text-amber transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                </div>
                <p class="text-base font-bold text-slate-900 tracking-tight">{{ selectedFile ? `Archivo listo: ${selectedFile.name}` : "Seleccionar archivo CSV corporativo" }}</p>
                <p class="mt-2 text-[10px] font-black text-text-muted uppercase tracking-[0.2em] opacity-60">Drag and drop o click aqui</p>
              </div>
            </label>
            <input id="csv_file" :key="fileInputKey" type="file" accept=".csv" required class="sr-only" @change="handleFileChange" />
          </div>

          <div class="bg-amber/5 border border-amber/20 rounded-2xl p-6">
            <div class="flex items-start gap-4">
              <div class="bg-amber/10 p-2 rounded-lg">
                <svg class="w-5 h-5 text-amber" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                </svg>
              </div>
              <div>
                <p class="text-xs font-black text-amber uppercase tracking-[0.15em] mb-3">Estructura Requerida del Archivo</p>
                <div class="relative group">
                  <code class="text-[12px] font-bold text-amber-soft block bg-slate-100/50 rounded-xl px-4 py-3 border border-white/[0.07] shadow-inner overflow-x-auto whitespace-nowrap custom-scrollbar group-hover:border-amber/20 transition-colors">sku,nombre,unidad_medida,precio,descripcion,imagen_url,stock_actual</code>
                </div>
                <p class="text-[11px] font-medium text-text-muted mt-3 italic leading-relaxed">
                  Si el <strong class="text-slate-900/80 font-bold">SKU</strong> ya existe, los datos se sincronizaran automaticamente. De lo contrario, se creara una nueva entrada en el Catalogo Maestro.
                </p>
              </div>
            </div>
          </div>

          <div v-if="productStore.error" class="rounded-[24px] border border-rose-500/20 bg-rose-500/10 px-5 py-4 text-sm text-rose-200">
            {{ productStore.error }}
          </div>

          <button type="submit" class="btn btn-primary w-full shadow-2xl shadow-amber/10" :disabled="!selectedFile || productStore.isUploadingCsv">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            {{ productStore.isUploadingCsv ? "Procesando e Importando..." : "Procesar e Importar CSV" }}
          </button>
        </form>
      </div>
    </div>

    <div v-if="productStore.csvUploads.length" class="space-y-6">
      <div class="flex items-center gap-3 px-2">
        <h3 class="text-2xl font-black tracking-tight text-slate-900">Historial de Operaciones</h3>
        <span class="pill">{{ productStore.csvUploads.length }} Cargas</span>
      </div>

      <div class="card !p-0 overflow-hidden divide-y divide-white/5 border-white/[0.07] bg-white/[0.01]">
        <div v-for="upload in productStore.csvUploads" :key="upload.id" class="p-5 flex items-center justify-between hover:bg-white/[0.03] transition-colors group">
          <div class="flex items-center gap-5 min-w-0">
            <div class="bg-white/[0.04] border border-white/[0.12] rounded-2xl p-3.5 shrink-0 shadow-sm transition-transform group-hover:scale-105">
              <svg class="w-6 h-6 text-text-muted group-hover:text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="min-w-0">
              <p class="text-[15px] font-bold text-slate-900 truncate pr-4">{{ upload.filename }}</p>
              <div class="flex flex-wrap items-center gap-3 mt-1.5 opacity-60">
                <span class="text-[11px] font-black uppercase tracking-widest text-text-muted">{{ formatUploadDate(upload.uploaded_at) }}</span>
                <span class="w-1 h-1 rounded-full bg-white/20"></span>
                <span class="text-[11px] font-bold text-emerald-400 capitalize">+{{ upload.products_created }} Creados</span>
                <span class="w-1 h-1 rounded-full bg-white/20"></span>
                <span class="text-[11px] font-bold text-amber capitalize">~{{ upload.products_updated }} Actualizados</span>
              </div>
            </div>
          </div>

          <button
            type="button"
            class="p-3 text-slate-900/20 hover:text-rose-500 hover:bg-rose-500/10 rounded-xl transition-all border border-transparent hover:border-rose-500/20 active:scale-90"
            @click="pendingUploadId = upload.id"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div v-if="catalogPreview.length" class="space-y-6">
      <div class="flex items-center gap-3 px-2">
        <h3 class="text-2xl font-black tracking-tight text-slate-900">Vistazo Rapido al Catalogo</h3>
        <span class="pill !text-emerald-400 !bg-emerald-400/10 !border-emerald-400/20">{{ productStore.products.length }} Items</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="product in catalogPreview" :key="product.id" class="flex items-center gap-5 p-4 rounded-2xl border border-white/[0.07] bg-white/[0.01] hover:bg-white/[0.04] transition-all group">
          <div class="shrink-0 relative overflow-hidden rounded-xl border border-white/[0.12] bg-white/[0.04] w-16 h-16">
            <img :src="product.imageUrl" :alt="product.name" class="w-full h-full object-cover transition-transform group-hover:scale-110" />
          </div>
          <div class="min-w-0 flex-grow">
            <div class="flex items-center gap-2 mb-1">
              <p class="text-sm font-bold text-slate-900 truncate">{{ product.name }}</p>
              <span v-if="product.sku" class="text-[9px] font-black uppercase tracking-widest text-text-muted bg-white px-1.5 py-0.5 rounded">{{ product.sku }}</span>
            </div>
            <div class="flex items-center justify-between">
              <p class="text-[13px] font-black text-amber">S/ {{ Number(product.precio || 0).toFixed(2) }}</p>
              <span class="text-[11px] font-bold text-text-muted opacity-60">Existencia: <span class="text-slate-900">{{ product.stockActual }}</span></span>
            </div>
          </div>
        </div>
        <div v-if="productStore.products.length > 10" class="col-span-full text-center py-4">
          <p class="text-[11px] font-black uppercase tracking-widest text-text-muted italic">+ {{ productStore.products.length - 10 }} productos adicionales ocultos en esta vista</p>
        </div>
      </div>
    </div>

    <div class="flex justify-center pt-8 border-t border-white/[0.07]">
      <RouterLink :to="{ name: 'catalogAssignBuilding' }" class="btn btn-secondary !min-h-[48px] px-8">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Panel de Asignacion
      </RouterLink>
    </div>

    <AppModal
      :open="Boolean(pendingUpload)"
      eyebrow="Catalogo maestro"
      title="Revertir lote CSV"
      :description="pendingUpload ? `Se intentara revertir ${pendingUpload.filename}. Los productos con historial quedaran inactivos.` : ''"
      confirm-label="Eliminar lote"
      confirm-variant="danger"
      :loading="productStore.isDeletingCsv"
      @close="pendingUploadId = null"
      @confirm="confirmDeleteUpload"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"

import AppModal from "@/components/ui/AppModal.vue"
import { useProductStore } from "@/stores/productStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizeProduct } from "@/utils/normalizers"

const productStore = useProductStore()
const uiStore = useUiStore()
const selectedFile = ref(null)
const fileInputKey = ref(0)
const pendingUploadId = ref(null)

const catalogPreview = computed(() => productStore.products.slice(0, 10).map(normalizeProduct))
const pendingUpload = computed(() => productStore.csvUploads.find((upload) => upload.id === pendingUploadId.value) ?? null)

onMounted(async () => {
  await Promise.all([productStore.fetchCsvUploads(), productStore.fetchProducts()])
})

function handleFileChange(event) {
  selectedFile.value = event.target.files?.[0] ?? null
}

function formatUploadDate(value) {
  return new Intl.DateTimeFormat("es-PE", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value))
}

async function handleUpload() {
  if (productStore.isUploadingCsv || !selectedFile.value) {
    return
  }

  try {
    const result = await productStore.uploadCsv(selectedFile.value)
    await productStore.fetchProducts()
    uiStore.success(`${result.products_created} creados, ${result.products_updated} actualizados.`, "Carga CSV completada")
    selectedFile.value = null
    fileInputKey.value += 1
  } catch (error) {
    uiStore.error(error.message, "La carga CSV fallo")
  }
}

async function confirmDeleteUpload() {
  if (productStore.isDeletingCsv || !pendingUpload.value) {
    return
  }

  try {
    const result = await productStore.deleteCsvUpload(pendingUpload.value.id)
    await productStore.fetchProducts()
    uiStore.success(result.message, "Lote revertido")
    pendingUploadId.value = null
  } catch (error) {
    uiStore.error(error.message, "No se pudo revertir el lote")
  }
}
</script>

<style scoped>
</style>
