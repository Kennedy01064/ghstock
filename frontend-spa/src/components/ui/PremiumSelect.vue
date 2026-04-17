<template>
  <div class="relative" ref="containerRef">
    <!-- Trigger -->
    <div
      class="select-field flex items-center justify-between gap-3 cursor-pointer select-none"
      :class="[isOpen ? 'border-amber/60 ring-4 ring-amber/10' : '', disabled ? 'opacity-50 pointer-events-none' : '']"
      @click="toggle"
    >
      <span class="truncate" :class="hasValue ? 'text-slate-900 font-medium' : 'text-slate-400'">
        {{ selectedLabel }}
      </span>
      <svg
        class="w-4 h-4 text-slate-400 shrink-0 transition-transform duration-200"
        :class="{ 'rotate-180': isOpen }"
        fill="none" stroke="currentColor" viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
      </svg>
    </div>

    <!-- Dropdown -->
    <Transition name="premium-select">
      <div
        v-if="isOpen"
        class="absolute z-[70] left-0 top-full mt-1.5 w-full min-w-[200px] rounded-2xl border border-slate-200 bg-white shadow-[0_20px_60px_-10px_rgba(0,0,0,0.15)] overflow-hidden"
      >
        <div class="py-1.5 max-h-64 overflow-y-auto custom-scrollbar">
          <button
            v-for="option in options"
            :key="option.value"
            type="button"
            class="w-full text-left px-4 py-2.5 text-sm font-medium transition-colors flex items-center gap-3"
            :class="
              option.value === modelValue
                ? 'bg-amber/10 text-amber-700 font-black'
                : 'text-slate-700 hover:bg-slate-50 hover:text-slate-900'
            "
            @click="select(option)"
          >
            <span
              v-if="option.value === modelValue"
              class="w-1.5 h-1.5 rounded-full bg-amber shrink-0"
            ></span>
            <span v-else class="w-1.5 h-1.5 shrink-0"></span>
            {{ option.label }}
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue"

const props = defineProps({
  modelValue: { type: [String, Number], default: "" },
  options: { type: Array, default: () => [] },
  placeholder: { type: String, default: "Seleccionar" },
  disabled: { type: Boolean, default: false },
})

const emit = defineEmits(["update:modelValue", "change"])

const containerRef = ref(null)
const isOpen = ref(false)

const hasValue = computed(() => props.modelValue !== "" && props.modelValue !== null && props.modelValue !== undefined)

const selectedLabel = computed(() => {
  const found = props.options.find(o => String(o.value) === String(props.modelValue))
  return found ? found.label : props.placeholder
})

function toggle() {
  isOpen.value = !isOpen.value
}

function select(option) {
  emit("update:modelValue", option.value)
  emit("change", option.value)
  isOpen.value = false
}

function handleClickOutside(e) {
  if (containerRef.value && !containerRef.value.contains(e.target)) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener("click", handleClickOutside))
onUnmounted(() => document.removeEventListener("click", handleClickOutside))
</script>

<style scoped>
.premium-select-enter-active,
.premium-select-leave-active {
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
}
.premium-select-enter-from,
.premium-select-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.98);
}
</style>
