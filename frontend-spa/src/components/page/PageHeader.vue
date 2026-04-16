<template>
  <div class="flex flex-col xl:flex-row xl:items-end justify-between gap-8 border-b border-slate-200 pb-10">
    <div class="space-y-4">
      <RouterLink
        v-if="backTo"
        :to="backTo"
        class="inline-flex items-center gap-3 text-[11px] font-black uppercase tracking-[0.25em] text-text-muted hover:text-slate-900 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
        </svg>
        {{ backLabel }}
      </RouterLink>

      <div class="flex items-center gap-3">
        <div class="w-1.5 h-6 bg-amber rounded-full shadow-[0_0_12px_rgba(242,173,61,0.4)]"></div>
        <span class="eyebrow tracking-[0.4em] !text-amber text-[10px]">{{ eyebrow }}</span>
      </div>

      <h1 class="h2 !text-5xl !tracking-tighter italic leading-none">{{ title }}</h1>
      <p class="text-text-muted font-medium text-sm md:text-base max-w-2xl">{{ description }}</p>
    </div>

    <div v-if="$slots.meta || meta" class="flex items-center gap-5 bg-slate-50 border border-slate-200 backdrop-blur-3xl rounded-[2rem] px-8 py-5 shadow-2xl self-start xl:self-auto">
      <slot name="meta">
        <div class="text-right">
          <p class="label-premium !mb-0">{{ meta.label }}</p>
          <p class="text-slate-900 font-black text-sm tracking-widest tabular-nums uppercase">{{ meta.value }}</p>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  eyebrow: { type: String, required: true },
  title: { type: String, required: true },
  description: { type: String, required: true },
  backTo: { type: [String, Object], default: null },
  backLabel: { type: String, default: "Volver" },
  meta: { type: Object, default: null },
})
</script>
