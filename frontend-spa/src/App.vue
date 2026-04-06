<template>
  <RouterView />
  <ToastViewport />
</template>

<script setup>
import { RouterView } from "vue-router"

import ToastViewport from "@/components/ui/ToastViewport.vue"
</script>
