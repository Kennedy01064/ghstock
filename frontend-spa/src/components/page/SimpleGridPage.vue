<template>
  <div class="space-y-10">
    <PageHeader
      :back-to="backTo"
      :back-label="backLabel"
      :eyebrow="eyebrow"
      :title="title"
      :description="description"
      :meta="meta"
    />

    <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <div v-if="searchable" class="relative max-w-md w-full">
        <input v-model="query" type="search" placeholder="Buscar..." class="input-field !pl-12" />
        <svg class="w-4 h-4 text-slate-900/40 absolute left-5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-4.35-4.35m1.85-5.15a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>

      <div class="flex flex-wrap gap-3">
        <RouterLink v-for="action in actions" :key="action.label" :to="action.to" class="btn" :class="action.variant === 'secondary' ? 'btn-secondary' : 'btn-primary'">
          {{ action.label }}
        </RouterLink>
      </div>
    </div>

    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
      <article v-for="item in filteredItems" :key="item.id" class="card !p-0 overflow-hidden group">
        <div class="h-48 bg-slate-50 border-b border-slate-200 overflow-hidden">
          <img :src="item.imageUrl" :alt="item.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
        </div>
        <div class="p-6 space-y-4">
          <div class="flex items-start justify-between gap-4">
            <div>
              <h3 class="text-lg font-black text-slate-900">{{ item.name }}</h3>
              <p class="text-[11px] uppercase tracking-[0.18em] text-text-muted mt-1">{{ item.subtitle }}</p>
            </div>
            <span v-if="item.status" class="inline-flex items-center px-3 py-1 rounded-full border text-[10px] font-black uppercase tracking-[0.18em]" :class="statusClass(item.status)">
              {{ item.status }}
            </span>
          </div>

          <div class="space-y-2 text-sm text-text-secondary">
            <div v-for="fact in item.facts" :key="fact.label" class="flex items-center justify-between gap-4">
              <span class="text-text-muted">{{ fact.label }}</span>
              <span class="font-bold text-slate-900">{{ fact.value }}</span>
            </div>
          </div>

          <div class="flex flex-wrap gap-3">
            <RouterLink v-for="action in item.actions" :key="action.label" :to="resolveAction(action, item)" class="btn" :class="action.variant === 'secondary' ? 'btn-secondary !min-h-[44px] !px-5' : 'btn-primary !min-h-[44px] !px-5'">
              {{ action.label }}
            </RouterLink>
          </div>
        </div>
      </article>
    </div>

    <div v-if="!filteredItems.length" class="card text-center py-12 text-text-muted">No se encontraron resultados.</div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"

import PageHeader from "@/components/page/PageHeader.vue"
import { statusClass } from "@/utils/formatters"

const props = defineProps({
  eyebrow: String,
  title: String,
  description: String,
  items: { type: Array, default: () => [] },
  actions: { type: Array, default: () => [] },
  searchable: { type: Boolean, default: true },
  backTo: { type: [String, Object], default: null },
  backLabel: { type: String, default: "Volver" },
  meta: { type: Object, default: null },
})

const query = ref("")

const filteredItems = computed(() => {
  if (!props.searchable || !query.value.trim()) {
    return props.items
  }

  const term = query.value.toLowerCase()
  return props.items.filter((item) => `${item.name} ${item.subtitle}`.toLowerCase().includes(term))
})

function resolveAction(action, item) {
  return typeof action.to === "function" ? action.to(item) : action.to
}
</script>
