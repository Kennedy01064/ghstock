<template>
  <div class="space-y-10">
    <PageHeader
      :back-to="backTo"
      :back-label="backLabel"
      :eyebrow="eyebrow"
      :title="title"
      :description="description"
      :meta="meta"
    >
      <template v-if="$slots.meta" #meta>
        <slot name="meta" />
      </template>
    </PageHeader>

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

    <div class="grid gap-8 xl:grid-cols-[minmax(0,1fr)_300px]" :class="sidePanels.length ? '' : '!grid-cols-1'">
      <div class="card !p-0 overflow-hidden">
        <!-- Desktop Table View -->
        <div class="hidden md:block overflow-x-auto">
          <table class="w-full text-left">
            <thead class="bg-white/[0.03] text-text-muted font-bold text-[10px] uppercase tracking-[0.2em]">
              <tr>
                <th v-for="column in columns" :key="column.key" class="px-4 lg:px-8 py-4" :class="column.align === 'right' ? 'text-right' : ''">
                  {{ column.label }}
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr v-for="row in filteredRows" :key="row.id ?? row.code ?? row.fileName ?? row.name" class="group hover:bg-white/[0.02] transition-all duration-300">
                <td v-for="column in columns" :key="column.key" class="px-4 lg:px-8 py-5" :class="column.align === 'right' ? 'text-right' : ''">
                  <slot :name="`cell-${column.key}`" :row="row">
                    <span v-if="column.type === 'status'" class="inline-flex items-center px-3 py-1 rounded-full border text-[10px] font-black uppercase tracking-[0.18em]" :class="statusClass(row[column.key])">
                      {{ row[column.key] }}
                    </span>
                    <span v-else class="text-sm font-bold text-slate-900">{{ resolveValue(row, column) }}</span>
                  </slot>
                </td>
              </tr>
              <tr v-if="!filteredRows.length">
                <td :colspan="columns.length" class="px-8 py-12 text-center text-text-muted text-sm">{{ emptyMessage }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Mobile Stack View -->
        <div class="md:hidden divide-y divide-white/5">
          <div 
            v-for="row in filteredRows" 
            :key="row.id ?? row.code ?? row.fileName ?? row.name"
            class="p-6 space-y-4 active:bg-white/[0.04] transition-colors"
          >
            <div v-for="column in columns" :key="column.key" class="flex flex-col gap-1">
              <span class="text-[9px] font-black uppercase tracking-[0.2em] text-text-muted">{{ column.label }}</span>
              <div :class="column.align === 'right' ? 'text-right' : ''">
                <slot :name="`cell-${column.key}`" :row="row">
                  <span v-if="column.type === 'status'" class="inline-flex items-center px-3 py-1 rounded-full border text-[10px] font-black uppercase tracking-[0.18em]" :class="statusClass(row[column.key])">
                    {{ row[column.key] }}
                  </span>
                  <span v-else class="text-sm font-bold text-slate-900">{{ resolveValue(row, column) }}</span>
                </slot>
              </div>
            </div>
          </div>
          <div v-if="!filteredRows.length" class="px-8 py-12 text-center text-text-muted text-sm border-t border-white/[0.07]">
            {{ emptyMessage }}
          </div>
        </div>
      </div>

      <aside v-if="sidePanels.length" class="space-y-6">
        <div v-for="panel in sidePanels" :key="panel.title" class="card">
          <span class="section-label">{{ panel.title }}</span>
          <p class="text-sm leading-7 text-text-secondary">{{ panel.text }}</p>
          <ul v-if="panel.items?.length" class="mt-4 space-y-3">
            <li v-for="item in panel.items" :key="item" class="flex items-start gap-3 text-sm text-text-secondary">
              <span class="mt-1 h-2 w-2 rounded-full bg-amber"></span>
              <span>{{ item }}</span>
            </li>
          </ul>
        </div>
      </aside>
    </div>
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
  columns: { type: Array, default: () => [] },
  rows: { type: Array, default: () => [] },
  actions: { type: Array, default: () => [] },
  sidePanels: { type: Array, default: () => [] },
  searchable: { type: Boolean, default: true },
  emptyMessage: { type: String, default: "No hay registros disponibles." },
  backTo: { type: [String, Object], default: null },
  backLabel: { type: String, default: "Volver" },
  meta: { type: Object, default: null },
})

const query = ref("")

const filteredRows = computed(() => {
  if (!props.searchable || !query.value.trim()) {
    return props.rows
  }

  const term = query.value.trim().toLowerCase()

  return props.rows.filter((row) =>
    Object.values(row).some((value) => String(value).toLowerCase().includes(term)),
  )
})

function resolveValue(row, column) {
  if (typeof column.value === "function") {
    return column.value(row)
  }

  return row[column.key]
}
</script>
