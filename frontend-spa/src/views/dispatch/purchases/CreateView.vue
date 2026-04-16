<template>
  <div class="max-w-5xl mx-auto space-y-10 pb-40">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 px-2">
      <div class="space-y-2">
        <span class="eyebrow tracking-[0.4em] !text-amber">Control de Abastecimiento</span>
        <h1 class="h2 italic !tracking-tighter">Nueva Compra</h1>
        <p class="text-text-muted font-medium text-sm">Ingrese los detalles del comprobante y la relacion de items adquiridos.</p>
      </div>
      <div class="h-14 w-14 rounded-3xl bg-amber/10 border border-amber/20 flex items-center justify-center text-amber shadow-2xl shadow-amber/10 shrink-0">
        <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
        </svg>
      </div>
    </div>

    <div v-if="submitError" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
      {{ submitError }}
    </div>

    <form class="space-y-10" @submit.prevent="submitPurchase">
      <div class="card bg-slate-50 border-slate-200 shadow-[0_30px_60px_-15px_rgba(0,0,0,0.5)] relative z-10">
        <div class="flex items-center gap-3 mb-8 px-2">
          <div class="w-1.5 h-6 bg-amber rounded-full" />
          <h2 class="text-lg font-black text-slate-900 uppercase tracking-tight">Informacion del Comprobante</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="space-y-3">
            <label class="eyebrow !text-text-muted">Proveedor</label>
            <input v-model="form.supplier" type="text" :disabled="dispatchStore.isPurchasing" placeholder="Razon Social / Nombre" class="input-field font-bold uppercase tracking-widest text-[11px] placeholder:text-slate-900/10">
          </div>
          <div class="space-y-3">
            <label class="eyebrow !text-text-muted">N° de Factura / Guia</label>
            <input v-model="form.invoiceNumber" type="text" :disabled="dispatchStore.isPurchasing" placeholder="Ej: F001-00123" class="input-field font-bold uppercase tracking-widest text-[11px] placeholder:text-slate-900/10">
          </div>
          <div class="space-y-3">
            <label class="eyebrow !text-text-muted">Fecha de Operacion <span class="text-amber">*</span></label>
            <PremiumDateTimePicker v-model="form.purchaseDate" type="date" :disabled="dispatchStore.isPurchasing" />
          </div>
          <div class="md:col-span-3 space-y-3">
            <label class="eyebrow !text-text-muted">Observaciones Internas</label>
            <textarea v-model="form.notes" rows="2" :disabled="dispatchStore.isPurchasing" placeholder="Detalles relevantes de la transaccion..." class="input-field min-h-[80px] py-4 placeholder:text-slate-900/10" />
          </div>
        </div>
      </div>

      <div class="card bg-slate-50 border-slate-200">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-6 mb-10 px-2">
          <div class="flex items-center gap-3">
            <div class="w-1.5 h-6 bg-amber rounded-full" />
            <h2 class="text-lg font-black text-slate-900 uppercase tracking-tight">Relacion de Articulos</h2>
          </div>

          <div class="flex flex-wrap gap-3 w-full sm:w-auto">
            <button type="button" class="flex-1 sm:flex-none h-12 flex items-center justify-center gap-3 px-6 rounded-2xl bg-slate-50 border border-slate-200 text-[10px] font-black text-slate-900 uppercase tracking-widest hover:bg-slate-50 hover:border-amber/40 hover:text-amber transition-all group disabled:opacity-50" :disabled="dispatchStore.isPurchasing" @click="selectorOpen = true">
              <svg class="w-4 h-4 text-amber transition-transform group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              BUSCAR EN CATALOGO
            </button>
            <button type="button" class="flex-1 sm:flex-none h-12 flex items-center justify-center gap-3 px-6 rounded-2xl bg-amber/10 border border-amber/20 text-[10px] font-black text-amber uppercase tracking-widest hover:bg-amber hover:text-navy-deep transition-all group disabled:opacity-50" :disabled="dispatchStore.isPurchasing" @click="addManualRow">
              <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
              </svg>
              NUEVA ENTRADA
            </button>
          </div>
        </div>

        <div v-if="rows.length" class="space-y-4">
          <div v-for="row in rows" :key="row.id" class="grid grid-cols-1 sm:grid-cols-12 gap-5 p-6 bg-slate-50 border border-slate-200 rounded-[1.8rem] group/row hover:border-slate-300 transition-all">
            <div class="sm:col-span-6 space-y-2">
              <label class="eyebrow !text-text-muted !text-[9px]">Producto / Descripcion</label>
              <input v-model="row.name" type="text" required :disabled="dispatchStore.isPurchasing" placeholder="Descripcion material" class="input-field h-12 !px-4 !rounded-xl font-bold uppercase tracking-widest text-[11px] bg-slate-200/60 group-hover/row:bg-slate-200/80">
            </div>
            <div class="sm:col-span-2 space-y-2 text-center">
              <label class="eyebrow !text-text-muted !text-[9px]">Cantidad</label>
              <input v-model.number="row.quantity" type="number" min="1" :disabled="dispatchStore.isPurchasing" class="input-field h-12 !px-4 !rounded-xl text-center font-black text-amber text-lg bg-slate-200/60">
            </div>
            <div class="sm:col-span-3 space-y-2">
              <label class="eyebrow !text-text-muted !text-[9px]">P. Unitario (S/)</label>
              <input v-model.number="row.unitPrice" type="number" min="0" step="0.01" :disabled="dispatchStore.isPurchasing" class="input-field h-12 !px-4 !rounded-xl font-black text-emerald-400 placeholder:text-slate-900/5 bg-slate-200/60">
            </div>
            <div class="sm:col-span-1 flex items-end justify-center pb-1">
              <button type="button" class="w-10 h-10 flex items-center justify-center rounded-xl bg-red-500/5 text-red-500/40 border border-red-500/10 hover:bg-red-500 hover:text-slate-900 hover:border-red-500 transition-all disabled:opacity-50" :disabled="dispatchStore.isPurchasing" @click="removeRow(row.id)">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div v-else class="py-20 text-center border-2 border-dashed border-slate-200 rounded-[2.5rem] bg-slate-200/60">
          <p class="text-text-muted font-bold text-sm italic">No se han agregado productos a la lista todavia.</p>
        </div>
      </div>

      <div class="flex flex-col sm:flex-row items-center justify-end gap-6 pt-6 border-t border-slate-200">
        <RouterLink :to="{ name: 'dispatchPurchases' }" class="btn btn-secondary w-full sm:w-auto px-12 !py-4 border-slate-200 text-slate-900/40 hover:text-slate-900">
          CANCELAR
        </RouterLink>
        <button type="submit" class="btn btn-primary w-full sm:w-auto px-16 !py-5 shadow-2xl shadow-amber/20 group" :disabled="dispatchStore.isPurchasing">
          <span v-if="!dispatchStore.isPurchasing">FINALIZAR REGISTRO</span>
          <span v-else class="flex items-center gap-2">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-navy-deep" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            PROCESANDO...
          </span>
          <svg v-if="!dispatchStore.isPurchasing" class="w-6 h-6 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </button>
      </div>
    </form>

    <Transition name="fade">
      <div v-if="selectorOpen" class="fixed inset-0 bg-slate-100/80 backdrop-blur-2xl items-center justify-center z-[100] p-6 flex">
        <div class="bg-white border border-slate-200 rounded-[3rem] shadow-[0_50px_100px_-20px_rgba(0,0,0,1)] w-full max-w-2xl overflow-hidden flex flex-col max-h-[85vh]">
          <div class="p-10 border-b border-slate-200 flex items-center justify-between bg-slate-50">
            <div class="space-y-1">
              <h3 class="h2 !text-3xl italic">Catalogo Maestro</h3>
              <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.3em]">Seleccione un articulo existente</p>
            </div>
            <button type="button" class="w-12 h-12 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-900/20 hover:text-slate-900 hover:bg-red-500/20 hover:border-red-500/40 transition-all" @click="selectorOpen = false">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="p-10 flex flex-col gap-6 flex-1 min-h-0 overflow-hidden">
            <div class="relative group shrink-0">
              <input v-model="selectorQuery" type="text" placeholder="Filtrar por nombre o categoria..." class="input-field !pl-14 font-bold tracking-widest text-[11px] !bg-slate-100/80 !border-white/15 focus:!bg-slate-100 focus:!border-amber/40 transition-all">
              <div class="absolute left-6 top-1/2 -translate-y-1/2 text-slate-900/10 group-focus-within:text-amber transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            <div class="flex-1 min-h-0 space-y-3 overflow-y-auto pr-4 custom-scrollbar">
              <div v-for="product in filteredProducts" :key="product.id" class="group/item relative overflow-hidden flex items-center justify-between p-5 bg-slate-50 border border-slate-200 rounded-[1.5rem] hover:bg-amber/5 hover:border-amber/30 cursor-pointer transition-all">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-[10px] font-black text-amber border border-slate-200 group-hover/item:border-amber/40 group-hover/item:bg-amber group-hover/item:text-navy-deep transition-all">
                    {{ (product.categoria || "G").slice(0, 1).toUpperCase() }}
                  </div>
                  <div class="flex flex-col">
                    <p class="text-sm font-black text-slate-900 uppercase tracking-tight group-hover/item:text-amber transition-colors">{{ product.name }}</p>
                    <p class="text-[9px] font-black text-text-muted uppercase tracking-widest mt-0.5">{{ product.categoria }} • STOCK: {{ product.stockActual }}</p>
                  </div>
                </div>

                <button type="button" class="h-10 px-6 rounded-xl bg-slate-50 border border-slate-200 text-[9px] font-black text-slate-900 hover:bg-amber hover:text-navy-deep hover:border-amber transition-all uppercase tracking-widest shadow-xl" @click="selectProduct(product)">
                  ELEGIR
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
import { computed, onMounted, reactive, ref } from "vue"
import { useRouter } from "vue-router"

import { useProductStore } from "@/stores/productStore"
import { useDispatchStore } from "@/stores/dispatchStore"
import { useUiStore } from "@/stores/uiStore"
import { normalizeProduct } from "@/utils/normalizers"
import PremiumDateTimePicker from "@/components/ui/PremiumDateTimePicker.vue"

const router = useRouter()
const productStore = useProductStore()
const dispatchStore = useDispatchStore()
const uiStore = useUiStore()

const form = reactive({
  supplier: "",
  invoiceNumber: "",
  purchaseDate: new Date().toISOString().slice(0, 10),
  notes: "",
})

const rows = ref([])
const rowSeed = ref(1)
const selectorOpen = ref(false)
const selectorQuery = ref("")
const submitError = ref("")

const products = computed(() => productStore.products.map(normalizeProduct))
const filteredProducts = computed(() => {
  const query = selectorQuery.value.trim().toLowerCase()
  if (!query) {
    return products.value
  }
  return products.value.filter((product) =>
    product.name.toLowerCase().includes(query) ||
    (product.categoria || "").toLowerCase().includes(query),
  )
})

function addManualRow(product = null) {
  rows.value.push({
    id: rowSeed.value++,
    productId: product?.id ?? null,
    name: product?.name ?? "",
    quantity: 1,
    unitPrice: product?.price ?? 0,
  })
}

function removeRow(rowId) {
  rows.value = rows.value.filter((row) => row.id !== rowId)
}

function selectProduct(product) {
  addManualRow(product)
  selectorOpen.value = false
  selectorQuery.value = ""
}

async function resolveProductId(row) {
  if (row.productId) {
    return row.productId
  }

  const created = await productStore.createProduct({
    name: row.name,
    sku: null,
    categoria: "General",
    unit: "UND",
    precio: Number(row.unitPrice || 0),
    imagen_url: "/static/img/default-product.png",
    stock_actual: 0,
    stock_minimo: 10,
    description: null,
    is_active: true,
    is_dynamic: false,
  })

  return created.id
}

async function submitPurchase() {
  submitError.value = ""

  if (!rows.value.length) {
    submitError.value = "Debe agregar al menos un producto a la relacion."
    return
  }

  if (rows.value.some((row) => !row.name.trim() || Number(row.quantity) <= 0)) {
    submitError.value = "Todos los items deben tener descripcion y cantidad valida."
    return
  }

  if (dispatchStore.isPurchasing) return

  try {
    const items = []
    for (const row of rows.value) {
      const productId = await resolveProductId(row)
      items.push({
        product_id: Number(productId),
        quantity: Number(row.quantity),
        unit_price: Number(row.unitPrice || 0),
      })
    }

    const purchase = await dispatchStore.createPurchase({
      supplier: form.supplier || null,
      invoice_number: form.invoiceNumber || null,
      purchase_date: form.purchaseDate,
      notes: form.notes || null,
      items,
    })

    uiStore.success("La compra fue registrada correctamente.", "Compra creada")
    await router.push({ name: "dispatchPurchaseDetail", params: { purchaseId: purchase.id } })
  } catch (error) {
    submitError.value = error.message
    uiStore.error(error.message, "No se pudo registrar la compra")
  } finally {
    // El store maneja isPurchasing
  }
}

onMounted(() => {
  productStore.fetchProducts()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
