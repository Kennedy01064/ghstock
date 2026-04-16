<template>
  <footer class="border-t border-white/[0.07] bg-navy-deep py-12">
    <div class="max-w-[1320px] mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-8">
      <div class="flex flex-col items-center sm:items-start gap-4">
        <div class="flex items-center gap-3">
          <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-white/[0.12] bg-white/[0.04]">
            <img :src="logoUrl" alt="Logo" class="h-8 w-auto" />
          </span>
          <span class="font-display font-extrabold text-white tracking-tight">Grupo Hernandez</span>
        </div>
        <p class="text-xs font-semibold text-text-muted tracking-widest uppercase">
          &copy; 2026 Sistema de Control de Inventario
        </p>
      </div>

      <div class="flex items-center gap-6">
        <div class="flex items-center gap-2 bg-emerald-400/10 border border-emerald-400/20 px-3 py-1.5 rounded-full">
          <div class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
          <p class="text-[10px] font-black text-emerald-400 tracking-[0.14em] uppercase">Estatus: En linea</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const logoUrl = "/static/img/logo_trans.png"
</script>
