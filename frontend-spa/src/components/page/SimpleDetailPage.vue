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

    <div class="flex flex-wrap gap-3">
      <RouterLink v-for="action in actions" :key="action.label" :to="action.to" class="btn" :class="action.variant === 'secondary' ? 'btn-secondary' : 'btn-primary'">
        {{ action.label }}
      </RouterLink>
    </div>

    <div class="grid gap-5 md:grid-cols-3">
      <article v-for="summary in summaries" :key="summary.label" class="card">
        <span class="section-label">{{ summary.label }}</span>
        <div class="text-3xl font-black text-white tracking-tight">{{ summary.value }}</div>
        <p class="mt-3 text-sm leading-6 text-text-secondary">{{ summary.description }}</p>
      </article>
    </div>

    <div class="grid gap-8 xl:grid-cols-[minmax(0,1fr)_320px]" :class="sidePanels.length ? '' : '!grid-cols-1'">
      <div class="space-y-8">
        <div v-for="section in sections" :key="section.title" class="card !p-0 overflow-hidden">
          <div class="px-8 py-6 border-b border-white/[0.07] bg-white/[0.02]">
            <h3 class="text-base font-bold text-white">{{ section.title }}</h3>
            <p v-if="section.description" class="text-[11px] uppercase tracking-[0.18em] text-text-muted mt-2">{{ section.description }}</p>
          </div>

          <div v-if="section.type === 'table'" class="overflow-x-auto">
            <table class="w-full text-left">
              <thead class="bg-white/[0.03] text-text-muted font-bold text-[10px] uppercase tracking-[0.2em]">
                <tr>
                  <th v-for="column in section.columns" :key="column.key" class="px-8 py-4">{{ column.label }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                <tr v-for="row in section.rows" :key="row.id ?? row.name" class="hover:bg-white/[0.02] transition-colors">
                  <td v-for="column in section.columns" :key="column.key" class="px-8 py-5 text-sm font-bold text-white">
                    {{ typeof column.value === "function" ? column.value(row) : row[column.key] }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="divide-y divide-white/5">
            <div v-for="item in section.items" :key="item.title" class="px-8 py-5">
              <div class="flex items-center justify-between gap-4">
                <div>
                  <p class="text-sm font-black text-white">{{ item.title }}</p>
                  <p class="text-[11px] uppercase tracking-[0.18em] text-text-muted mt-2">{{ item.subtitle }}</p>
                </div>
                <span v-if="item.badge" class="inline-flex items-center px-3 py-1 rounded-full border text-[10px] font-black uppercase tracking-[0.18em]" :class="statusClass(item.badge)">
                  {{ item.badge }}
                </span>
              </div>
            </div>
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
import PageHeader from "@/components/page/PageHeader.vue"
import { statusClass } from "@/utils/formatters"

defineProps({
  eyebrow: String,
  title: String,
  description: String,
  summaries: { type: Array, default: () => [] },
  sections: { type: Array, default: () => [] },
  actions: { type: Array, default: () => [] },
  sidePanels: { type: Array, default: () => [] },
  backTo: { type: [String, Object], default: null },
  backLabel: { type: String, default: "Volver" },
  meta: { type: Object, default: null },
})
</script>
