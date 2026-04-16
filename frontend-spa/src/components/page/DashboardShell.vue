<template>
  <div class="space-y-12 pb-24">
    <PageHeader :eyebrow="eyebrow" :title="title" :description="description" :meta="meta" />

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <article v-for="metric in metrics" :key="metric.label" class="card group overflow-hidden">
        <div class="relative z-10">
          <div class="flex justify-between items-start mb-6">
            <div class="w-14 h-14 rounded-2xl flex items-center justify-center border shadow-inner" :class="metric.iconWrapClass">
              <svg class="w-7 h-7" :class="metric.iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" :d="metric.iconPath" />
              </svg>
            </div>
          </div>
          <div class="space-y-1">
            <p class="text-5xl font-black text-slate-900 tracking-tighter">{{ metric.value }}</p>
            <span class="eyebrow !text-text-muted/60">{{ metric.label }}</span>
          </div>
        </div>
      </article>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <article v-for="panel in primaryPanels" :key="panel.title" class="card !p-0 overflow-hidden">
        <div class="px-8 py-6 border-b border-slate-100 bg-slate-50/50">
          <h3 class="text-base font-bold text-slate-900">{{ panel.title }}</h3>
          <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-2">{{ panel.caption }}</p>
        </div>
        <div class="p-8 space-y-4">
          <div v-for="item in panel.items" :key="item.label" class="space-y-2">
            <div class="flex items-center justify-between gap-4 text-sm">
              <span class="font-bold text-slate-900">{{ item.label }}</span>
              <span class="text-text-muted">{{ item.value }}</span>
            </div>
            <div class="h-2 rounded-full bg-slate-100 overflow-hidden">
              <div class="h-full rounded-full bg-gradient-to-r from-amber to-amber-hover" :style="{ width: `${item.percent}%` }"></div>
            </div>
          </div>
        </div>
      </article>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,0.8fr)] gap-8">
      <article class="card !p-0 overflow-hidden">
        <div class="px-8 py-6 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
          <div>
            <h3 class="text-base font-bold text-slate-900">{{ table.title }}</h3>
            <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-2">{{ table.caption }}</p>
          </div>
          <RouterLink v-if="table.action" :to="table.action.to" class="text-[10px] font-black text-amber uppercase tracking-[0.18em]">
            {{ table.action.label }}
          </RouterLink>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead class="bg-slate-50/30 text-text-muted font-bold text-[10px] uppercase tracking-[0.2em]">
              <tr>
                <th v-for="column in table.columns" :key="column.key" class="px-8 py-4">{{ column.label }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="row in table.rows" :key="row.id ?? row.label" class="hover:bg-slate-50/50 transition-colors">
                <td v-for="column in table.columns" :key="column.key" class="px-8 py-5 text-sm font-bold text-slate-900">
                  {{ typeof column.value === "function" ? column.value(row) : row[column.key] }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>

      <article class="card !p-0 overflow-hidden">
        <div class="px-8 py-6 border-b border-slate-100 bg-slate-50/50">
          <h3 class="text-base font-bold text-slate-900">{{ feed.title }}</h3>
          <p class="text-[10px] font-black text-text-muted uppercase tracking-[0.2em] mt-2">{{ feed.caption }}</p>
        </div>
        <div class="divide-y divide-slate-100">
          <div v-for="item in feed.items" :key="item.title" class="px-8 py-5 flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl border border-slate-200 bg-slate-50 flex items-center justify-center text-amber">
              <span class="text-xs font-black">{{ item.badge }}</span>
            </div>
            <div class="min-w-0">
              <p class="text-sm font-black text-slate-900">{{ item.title }}</p>
              <p class="text-[11px] uppercase tracking-[0.18em] text-text-muted mt-2">{{ item.subtitle }}</p>
            </div>
          </div>
        </div>
      </article>
    </div>

    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
      <RouterLink
        v-for="link in quickLinks"
        :key="link.label"
        :to="link.to"
        class="card !p-6 flex flex-col items-center justify-center gap-3 group hover:border-amber/40 hover:bg-amber/5 transition-all duration-300"
      >
        <div class="relative">
          <div class="w-12 h-12 bg-slate-100 rounded-2xl flex items-center justify-center group-hover:scale-110 group-hover:bg-amber transition-all duration-500 shadow-lg">
            <svg class="w-6 h-6 text-slate-900 group-hover:text-navy-deep" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" :d="link.iconPath" />
            </svg>
          </div>
          <span
            v-if="link.count"
            class="absolute -top-1 -right-1 w-5 h-5 bg-rose-500 text-slate-900 text-[10px] font-black rounded-full flex items-center justify-center border-2 border-navy-deep shadow-lg"
          >
            {{ link.count }}
          </span>
        </div>
        <p class="text-[11px] font-black text-text-muted uppercase tracking-[0.2em] group-hover:text-slate-900 transition-colors text-center">{{ link.label }}</p>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import PageHeader from "@/components/page/PageHeader.vue"

defineProps({
  eyebrow: String,
  title: String,
  description: String,
  meta: Object,
  metrics: { type: Array, default: () => [] },
  primaryPanels: { type: Array, default: () => [] },
  table: { type: Object, required: true },
  feed: { type: Object, required: true },
  quickLinks: { type: Array, default: () => [] },
})
</script>
