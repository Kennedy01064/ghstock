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

    <div class="grid gap-8 lg:grid-cols-[minmax(0,1fr)_320px]">
      <form class="card space-y-6" @submit.prevent="handleSubmit">
        <div v-for="group in fieldGroups" :key="group.title" class="space-y-5">
          <div v-if="group.title" class="border-b border-white/[0.07] pb-3">
            <span class="section-label !mb-0">{{ group.title }}</span>
          </div>

          <div class="grid gap-5 md:grid-cols-2">
            <div v-for="field in group.fields" :key="field.key" :class="field.fullWidth ? 'md:col-span-2' : ''">
              <label class="label-premium">{{ field.label }}</label>

              <textarea
                v-if="field.type === 'textarea'"
                v-model="form[field.key]"
                :rows="field.rows ?? 4"
                :placeholder="field.placeholder"
                class="input-field min-h-[140px]"
              />

              <select
                v-else-if="field.type === 'select'"
                v-model="form[field.key]"
                class="select-field"
              >
                <option v-for="option in field.options" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>

              <label
                v-else-if="field.type === 'checkbox'"
                class="flex items-center gap-3 rounded-2xl border border-white/[0.12] bg-white/[0.03] px-4 py-4 cursor-pointer"
              >
                <input v-model="form[field.key]" type="checkbox" class="h-4 w-4 accent-amber" />
                <span class="text-sm text-text-secondary">{{ field.placeholder }}</span>
              </label>

              <div
                v-else-if="field.type === 'file'"
                class="rounded-[24px] border border-dashed border-white/15 bg-white/[0.03] p-6"
              >
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 rounded-2xl bg-amber/10 border border-amber/20 flex items-center justify-center text-amber">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm font-bold text-white">{{ field.placeholder }}</p>
                    <p class="text-[11px] text-text-muted mt-1">{{ field.help ?? "Campo preparado para integrar carga real en Fase 4." }}</p>
                  </div>
                </div>
              </div>

              <input
                v-else
                v-model="form[field.key]"
                :type="field.type ?? 'text'"
                :placeholder="field.placeholder"
                class="input-field"
              />

              <p v-if="field.help && field.type !== 'file'" class="mt-2 text-[11px] text-text-muted">{{ field.help }}</p>
            </div>
          </div>
        </div>

        <div v-if="infoNote" class="rounded-[24px] border border-white/[0.12] bg-white/[0.03] px-5 py-4 text-sm text-text-secondary">
          {{ infoNote }}
        </div>

        <div v-if="submitError" class="rounded-[24px] border border-rose-500/20 bg-rose-500/10 px-5 py-4 text-sm text-rose-200">
          {{ submitError }}
        </div>

        <div v-if="showSuccessMessage" class="rounded-[24px] border border-emerald-500/20 bg-emerald-500/10 px-5 py-4 text-sm text-emerald-300">
          {{ successMessage }}
        </div>

        <div class="flex flex-col sm:flex-row gap-4">
          <button type="submit" class="btn btn-primary flex-1" :disabled="isSubmitting">{{ isSubmitting ? "Guardando..." : submitLabel }}</button>
          <RouterLink :to="cancelTo" class="btn btn-secondary flex-1">{{ cancelLabel }}</RouterLink>
        </div>
      </form>

      <aside class="space-y-6">
        <div v-if="preview" class="card">
          <span class="section-label">Vista previa</span>
          <div class="rounded-[24px] overflow-hidden border border-white/[0.12] bg-white/[0.03]">
            <img :src="preview.image" :alt="preview.title" class="h-48 w-full object-cover" />
          </div>
          <h3 class="mt-4 text-lg font-black text-white">{{ preview.title }}</h3>
          <p class="mt-2 text-sm leading-6 text-text-secondary">{{ preview.description }}</p>
        </div>

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
import { computed, reactive, ref, watch } from "vue"

import PageHeader from "@/components/page/PageHeader.vue"
import { useUiStore } from "@/stores/uiStore"

const props = defineProps({
  eyebrow: String,
  title: String,
  description: String,
  submitLabel: String,
  cancelLabel: { type: String, default: "Cancelar" },
  backLabel: { type: String, default: "Volver" },
  backTo: { type: [String, Object], default: null },
  cancelTo: { type: [String, Object], required: true },
  meta: { type: Object, default: null },
  fieldGroups: { type: Array, default: () => [] },
  initialValues: { type: Object, default: () => ({}) },
  infoNote: { type: String, default: "" },
  sidePanels: { type: Array, default: () => [] },
  preview: { type: Object, default: null },
  submitHandler: { type: Function, default: null },
  isSubmitting: { type: Boolean, default: false },
  submitError: { type: String, default: "" },
  submitSuccess: { type: Boolean, default: false },
  successMessage: { type: String, default: "Cambios guardados correctamente." },
  resetOnSuccess: { type: Boolean, default: false },
})

const uiStore = useUiStore()
const emittedSuccess = ref(false)
const form = reactive({})

watch(
  () => props.initialValues,
  (values) => {
    Object.keys(form).forEach((key) => {
      delete form[key]
    })

    Object.assign(form, values ?? {})
  },
  { immediate: true, deep: true },
)

const showSuccessMessage = computed(() => props.submitSuccess || emittedSuccess.value)

async function handleSubmit() {
  emittedSuccess.value = false

  if (!props.submitHandler) {
    emittedSuccess.value = true
    uiStore.success(props.successMessage)
    return
  }

  try {
    await props.submitHandler({ ...form })
    emittedSuccess.value = true
    uiStore.success(props.successMessage)

    if (props.resetOnSuccess) {
      Object.keys(form).forEach((key) => {
        delete form[key]
      })

      Object.assign(form, props.initialValues ?? {})
    }
  } catch {
    emittedSuccess.value = false
    uiStore.error(props.submitError || "No se pudo completar la operacion.")
  }
}
</script>
