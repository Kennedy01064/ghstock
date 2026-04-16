<template>
  <div class="space-y-12 animate-pulse">
    <!-- Header Skeleton -->
    <div class="flex flex-col xl:flex-row xl:items-end justify-between gap-10 border-b border-slate-200 pb-10">
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-6 bg-slate-200 rounded-full"></div>
          <div class="h-3 w-24 bg-slate-100 rounded"></div>
        </div>
        <div class="h-12 w-64 bg-slate-200 rounded-2xl"></div>
        <div class="h-4 w-96 bg-slate-100 rounded"></div>
      </div>
      <div class="w-48 h-16 bg-slate-100 rounded-3xl"></div>
    </div>

    <!-- Metrics Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="i in 4" :key="i" class="card h-40 !bg-white">
        <div class="w-14 h-14 bg-slate-100 rounded-2xl mb-6"></div>
        <div class="h-10 w-24 bg-slate-200 rounded-xl mb-3"></div>
        <div class="h-3 w-32 bg-slate-100 rounded"></div>
      </div>
    </div>

    <!-- Charts / Content Row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div v-for="i in 2" :key="i" class="card h-[400px] !bg-white !p-0 overflow-hidden">
        <div class="h-16 w-full bg-slate-50 border-b border-slate-200"></div>
        <div class="flex-grow p-8 flex items-center justify-center">
          <div class="w-48 h-48 rounded-full border-8 border-slate-100"></div>
        </div>
      </div>
    </div>

    <!-- Table Skeleton -->
    <div class="card !p-0 overflow-hidden !bg-white">
      <div class="h-16 w-full bg-slate-50 border-b border-slate-200 px-8 flex items-center">
        <div class="h-4 w-48 bg-slate-200 rounded"></div>
      </div>
      <div class="p-8 space-y-6">
        <div v-for="i in 5" :key="i" class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-slate-100 rounded-xl"></div>
            <div class="h-4 w-32 bg-slate-100 rounded"></div>
          </div>
          <div class="h-4 w-20 bg-slate-200 rounded"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Purely presentational skeleton
</script>
