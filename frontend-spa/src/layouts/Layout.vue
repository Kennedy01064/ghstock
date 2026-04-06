<template>
  <div class="min-h-screen flex flex-col">
    <AppNavbar />

    <main class="flex-grow w-full max-w-[1320px] mx-auto px-6 py-10 md:px-8 md:py-12">
      <RouterView v-slot="{ Component, route }">
        <Transition name="route-shell" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </Transition>
      </RouterView>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router"

import AppFooter from "@/components/AppFooter.vue"
import AppNavbar from "@/components/AppNavbar.vue"
</script>

<style>
.route-shell-enter-active,
.route-shell-leave-active {
  transition:
    opacity 0.32s ease,
    transform 0.32s ease,
    filter 0.32s ease;
  will-change: opacity, transform, filter;
}

.route-shell-enter-from,
.route-shell-leave-to {
  opacity: 0;
  transform: translateY(12px);
  filter: blur(4px);
}

@media (prefers-reduced-motion: reduce) {
  .route-shell-enter-active,
  .route-shell-leave-active {
    transition: opacity 0.01s linear;
  }

  .route-shell-enter-from,
  .route-shell-leave-to {
    transform: none;
    filter: none;
  }
}
</style>
