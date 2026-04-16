<template>
  <div v-if="dispatchStore.error" class="card border border-rose-500/20 bg-rose-500/10 text-rose-200">
    {{ dispatchStore.error }}
  </div>

  <DashboardSkeleton v-else-if="dispatchStore.isLoading && !batch" />

  <div v-else-if="batch" class="max-w-5xl mx-auto space-y-10 pb-32">
    <div class="relative card !p-0 bg-white/[0.05] border-white/[0.07] overflow-hidden shadow-[0_40px_100px_-20px_rgba(0,0,0,0.6)]">
      <div class="absolute top-0 right-0 w-96 h-96 bg-amber/5 rounded-full -translate-y-1/2 translate-x-1/2 blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-64 h-64 bg-white/[0.04] rounded-full translate-y-1/2 -translate-x-1/2 blur-2xl"></div>

      <div class="relative z-10 p-8 md:p-12">
        <div class="flex flex-col md:flex-row justify-between items-start gap-8">
          <div class="space-y-3">
            <span class="eyebrow tracking-[0.4em] !text-amber">Unidad de Despacho</span>
            <div class="flex items-baseline gap-4">
              <h1 class="text-6xl font-black tracking-tighter text-slate-900 italic">#{{ batch.id }}</h1>
              <span class="px-4 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest border" :class="batch.status === 'dispatched' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-amber/10 text-amber border-amber/20 shadow-[0_0_20px_rgba(242,173,61,0.1)]'">
                {{ batch.status === 'dispatched' ? 'Despachado' : batch.status === 'cancelled' ? 'Cancelado' : 'Pendiente' }}
              </span>
            </div>
            <p class="text-text-muted font-black text-xs uppercase tracking-widest flex items-center gap-2">
              <svg class="w-4 h-4 text-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              GENERADO EL {{ formatDateTime(batch.created_at) }}
            </p>
          </div>

          <div class="grid grid-cols-2 gap-4 w-full md:w-auto">
            <div class="bg-slate-100/60 backdrop-blur-md rounded-2xl p-5 border border-white/[0.07] flex flex-col gap-1 min-w-[140px]">
              <span class="text-[9px] font-black text-text-muted uppercase tracking-[0.3em]">Sedes</span>
              <span class="text-3xl font-black text-slate-900">{{ batch.orders?.length ?? 0 }}</span>
            </div>
            <div class="bg-slate-100/60 backdrop-blur-md rounded-2xl p-5 border border-white/[0.07] flex flex-col gap-1 min-w-[140px]">
              <span class="text-[9px] font-black text-text-muted uppercase tracking-[0.3em]">SKUs</span>
              <span class="text-3xl font-black text-slate-900">{{ batch.items?.length ?? 0 }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
      <div class="lg:col-span-2 space-y-6">
        <div class="flex items-center gap-3 px-2">
          <div class="w-1.5 h-6 bg-amber rounded-full"></div>
          <h3 class="text-lg font-black text-slate-900 uppercase tracking-tight">Lista Maestra de Preparacion</h3>
        </div>

        <div class="card !p-0 border-white/[0.07] bg-white/[0.02] overflow-hidden">
          <div class="divide-y divide-white/[0.03]">
            <div v-for="(item, index) in batch.items" :key="item.id" class="p-6 flex items-center justify-between gap-6 hover:bg-white/[0.02] transition-colors group">
              <div class="flex items-center gap-5 min-w-0">
                <div class="relative">
                  <img :src="item.product?.imagen_url || defaultProductUrl" :alt="item.product?.name" class="w-14 h-14 rounded-2xl object-contain bg-white/[0.04] p-2 border border-white/[0.12] group-hover:border-amber/30 transition-all" />
                  <div class="absolute -top-2 -right-2 w-6 h-6 bg-amber rounded-full flex items-center justify-center text-[10px] font-black text-navy-deep shadow-lg">
                    {{ index + 1 }}
                  </div>
                </div>
                <div class="min-w-0">
                  <p class="text-base font-black text-slate-900 truncate uppercase tracking-tight">{{ item.product?.name }}</p>
                  <p class="text-[10px] font-black text-text-muted uppercase tracking-widest mt-1">{{ item.product?.unit || "Unidades" }}</p>
                </div>
              </div>
              <div class="shrink-0">
                <div class="w-16 h-16 rounded-2xl bg-white/[0.03] border border-white/[0.12] flex items-center justify-center group-hover:bg-amber group-hover:border-amber transition-all shadow-inner">
                  <span class="text-2xl font-black text-slate-900 group-hover:text-navy-deep tabular-nums">{{ item.total_quantity }}</span>
                </div>
              </div>
            </div>
            <div v-if="!batch.items?.length">
              <EmptyState
                title="Bandeja vacia"
                description="No hay items consolidados en este lote todavia."
                class="py-20 bg-transparent border-none shadow-none"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-10">
        <div class="space-y-6">
          <h3 class="text-xs font-black text-text-muted uppercase tracking-[0.4em] px-2">Consolidado de Sedes</h3>
          <div class="grid grid-cols-1 gap-3">
            <div v-for="order in batch.orders" :key="order.id" class="bg-white/[0.04] rounded-2xl p-4 border border-white/[0.07] hover:border-white/[0.12] transition-all space-y-3">
              <div class="flex items-center justify-between gap-2">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-9 h-9 shrink-0 rounded-xl bg-white/[0.04] flex items-center justify-center text-amber border border-white/[0.07]">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5" />
                    </svg>
                  </div>
                  <span class="text-[11px] font-black text-slate-900 uppercase tracking-tight truncate">{{ order.building?.name }}</span>
                </div>
                <span class="text-[10px] font-black text-text-muted bg-white/[0.04] border border-white/[0.07] rounded-lg px-2 py-1 uppercase shrink-0">{{ order.items?.length ?? 0 }} items</span>
              </div>

              <details v-if="batch.status === 'pending'" class="group/rej">
                <summary class="cursor-pointer text-[10px] font-black text-rose-400/60 hover:text-rose-400 uppercase tracking-widest transition-colors list-none flex items-center gap-1.5">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  Rechazar pedido
                </summary>
                <div class="mt-3 space-y-2">
                  <textarea v-model="rejectionNotes[order.id]" rows="2" placeholder="Motivo del rechazo (opcional)..." class="input-field !py-2 !text-xs resize-none"></textarea>
                  <button
                    type="button"
                    class="w-full flex items-center justify-center gap-2 py-2 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20 text-[10px] font-black uppercase tracking-widest hover:bg-rose-500/20 transition-all disabled:opacity-50"
                    :disabled="dispatchStore.isRejectingOrder"
                    @click="handleReject(order.id)"
                  >
                    {{ dispatchStore.isRejectingOrder ? "RECHAZANDO..." : "Confirmar Rechazo" }}
                  </button>
                </div>
              </details>
            </div>
          </div>
        </div>

        <div class="space-y-4 pt-6 mt-6 border-t border-white/[0.07]">
          <RouterLink v-if="batch.status === 'pending'" :to="{ name: 'dispatchPicking', params: { batchId: batch.id } }" class="btn btn-primary w-full !py-5 shadow-2xl shadow-amber/20 group">
            <svg class="w-6 h-6 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
            Confirmar Despacho
          </RouterLink>

          <div class="grid grid-cols-1 gap-3">
            <button
              type="button"
              class="btn btn-secondary w-full !py-4 text-[10px] !rounded-2xl border-white/[0.12] hover:border-amber/40 hover:text-amber group disabled:opacity-50"
              :disabled="dispatchStore.isExporting"
              @click="downloadBatch('consolidated')"
            >
              <svg class="w-4 h-4 text-amber transition-transform group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              {{ dispatchStore.isExporting ? "EXPORTANDO..." : "PDF: LISTA CONSOLIDADA" }}
            </button>
            <button
              type="button"
              class="btn btn-secondary w-full !py-4 text-[10px] !rounded-2xl border-white/[0.12] hover:border-amber/40 hover:text-amber group disabled:opacity-50"
              :disabled="dispatchStore.isExporting"
              @click="downloadBatch('buildings')"
            >
              <svg class="w-4 h-4 text-amber transition-transform group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5" />
              </svg>
              {{ dispatchStore.isExporting ? "EXPORTANDO..." : "PDF: POR EDIFICIO" }}
            </button>
          </div>

          <RouterLink :to="{ name: 'dispatchPending' }" class="flex items-center justify-center gap-2 py-4 text-[10px] font-black text-text-muted hover:text-slate-900 uppercase tracking-widest transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Regresar al Panel
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive } from "vue"
import { useRoute } from "vue-router"

import EmptyState from "@/components/ui/EmptyState.vue"
import DashboardSkeleton from "@/components/common/DashboardSkeleton.vue"
import { useDispatchStore } from "@/stores/dispatchStore"
import { useUiStore } from "@/stores/uiStore"
import { defaultProductUrl } from "@/utils/formatters"

const route = useRoute()
const dispatchStore = useDispatchStore()
const uiStore = useUiStore()
const rejectionNotes = reactive({})

const batch = computed(() => dispatchStore.currentBatch)

onMounted(() => {
  dispatchStore.fetchBatchDetail(route.params.batchId)
})

function formatDateTime(value) {
  return new Intl.DateTimeFormat("es-PE", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value))
}

async function handleReject(orderId) {
  if (dispatchStore.isRejectingOrder) return
  try {
    await dispatchStore.rejectOrder(batch.value.id, orderId, rejectionNotes[orderId] || "")
    uiStore.success(`La orden #${orderId} fue devuelta al administrador.`, "Pedido rechazado")
    rejectionNotes[orderId] = ""
    await dispatchStore.fetchBatchDetail(batch.value.id)
  } catch (error) {
    uiStore.error(error.message, "No se pudo rechazar el pedido")
  }
}

async function downloadBatch(kind) {
  if (dispatchStore.isExporting) return
  try {
    const result = await dispatchStore.exportBatch(batch.value.id, kind)
    const blobUrl = URL.createObjectURL(result.blob)
    const anchor = document.createElement("a")
    anchor.href = blobUrl
    anchor.download = result.filename
    anchor.click()
    URL.revokeObjectURL(blobUrl)
  } catch (error) {
    uiStore.error(error.message, "No se pudo exportar el lote")
  }
}
</script>
