<template>
  <div class="relative w-full" :class="{ 'z-[60]': isOpen }" ref="containerRef">
    <!-- Trigger Button -->
    <div 
      class="relative group cursor-pointer" 
      @click="togglePicker"
    >
      <div class="absolute left-5 top-1/2 -translate-y-1/2 w-5 h-5 text-amber pointer-events-none transition-transform group-hover:scale-110 z-10">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
      
      <div 
        class="input-field !pl-14 font-black uppercase text-xs tracking-[0.15em] hover:border-amber/40 transition-all flex items-center min-h-[52px]"
        :class="{ 'border-amber/40 ring-4 ring-amber/5': isOpen }"
      >
        <span v-if="modelValue" class="text-slate-900">{{ displayValue }}</span>
        <span v-else class="text-slate-900/20">Seleccionar {{ type === 'date' ? 'fecha' : 'fecha y hora' }}</span>
      </div>
    </div>

    <!-- Picker Dropdown -->
    <Transition name="picker-fade">
      <div 
        v-if="isOpen" 
        class="absolute left-0 top-full mt-3 z-[100] w-[95vw] sm:w-[520px] rounded-[2rem] border border-slate-200 bg-white shadow-[0_40px_100px_-15px_rgba(0,0,0,0.25)] overflow-hidden"
      >
        <!-- Calendar Header -->
        <div class="px-6 py-3.5 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <button 
            type="button" 
            class="w-9 h-9 flex items-center justify-center rounded-xl bg-slate-100 hover:bg-slate-200 hover:text-amber transition-all"
            @click="prevMonth"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          
          <div class="text-center">
            <p class="text-[10px] font-black uppercase tracking-[0.2em] text-amber mb-0.5">{{ currentYear }}</p>
            <p class="text-sm font-black text-slate-900 uppercase tracking-wider">{{ currentMonthName }}</p>
          </div>

          <button 
            type="button" 
            class="w-9 h-9 flex items-center justify-center rounded-xl bg-slate-100 hover:bg-slate-200 hover:text-amber transition-all"
            @click="nextMonth"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        <!-- Content Area: Horizontal on Desktop -->
        <div class="flex flex-col sm:flex-row divide-y sm:divide-y-0 sm:divide-x divide-slate-200">
          <!-- Left: Calendar -->
          <div class="p-4 flex-1">
            <!-- Weekdays -->
            <div class="grid grid-cols-7 gap-0.5 mb-1">
              <span 
                v-for="day in ['L', 'M', 'X', 'J', 'V', 'S', 'D']" 
                :key="day" 
                class="text-[9px] font-black text-text-muted/60 text-center py-2"
              >
                {{ day }}
              </span>
            </div>

            <!-- Days Grid -->
            <div class="grid grid-cols-7 gap-1">
              <button
                v-for="date in calendarDays"
                :key="date.id"
                type="button"
                class="relative aspect-square flex items-center justify-center rounded-xl text-xs sm:text-[10px] font-bold transition-all"
                :class="[
                  date.isCurrentMonth ? 'text-slate-900' : 'text-slate-400',
                  date.isSelected ? 'bg-amber !text-slate-900 shadow-lg shadow-amber/40 scale-105 !font-black' : 'hover:bg-slate-100',
                  date.isToday && !date.isSelected ? 'border border-amber/30 text-amber' : ''
                ]"
                @click="selectDay(date)"
              >
                {{ date.day }}
                <span v-if="date.isToday && !date.isSelected" class="absolute bottom-1 w-1 h-1 bg-amber rounded-full"></span>
              </button>
            </div>
          </div>

          <!-- Right: Time Selector -->
          <div v-if="type === 'datetime'" class="p-5 sm:w-[170px] flex flex-col justify-center bg-slate-50">
            <p class="text-[9px] font-black uppercase tracking-[0.2em] text-amber mb-4 text-center">Hora</p>
            
            <div class="flex flex-col items-center gap-4">
              <div class="flex items-center gap-2">
                <div class="space-y-1.5">
                  <input 
                    type="number" 
                    v-model="time.hours" 
                    min="0" 
                    max="23"
                    class="w-11 h-11 bg-white border border-slate-200 rounded-xl text-center text-lg font-black text-slate-900 focus:border-amber/40 focus:bg-slate-50 outline-none transition-all tabular-nums"
                    @change="updateTime"
                  />
                  <p class="text-[7px] font-black text-center text-text-muted uppercase tracking-widest">HRS</p>
                </div>
                
                <span class="text-xl font-black text-amber/40 mb-4">:</span>

                <div class="space-y-1.5">
                  <input 
                    type="number" 
                    v-model="time.minutes" 
                    min="0" 
                    max="59" 
                    step="5"
                    class="w-11 h-11 bg-white border border-slate-200 rounded-xl text-center text-lg font-black text-slate-900 focus:border-amber/40 focus:bg-slate-50 outline-none transition-all tabular-nums"
                    @change="updateTime"
                  />
                  <p class="text-[7px] font-black text-center text-text-muted uppercase tracking-widest">MIN</p>
                </div>
              </div>

              <!-- Quick Time Suggestions -->
              <div class="grid grid-cols-2 gap-2 w-full mt-2">
                <button type="button" @click="time.hours = 12; time.minutes = 0; updateTime()" class="py-2.5 px-1.5 rounded-lg bg-slate-100 text-[8px] sm:text-[7px] font-black text-slate-500 uppercase hover:bg-slate-200 transition-all tracking-tighter">Mediodía</button>
                <button type="button" @click="time.hours = 23; time.minutes = 59; updateTime()" class="py-2.5 px-1.5 rounded-lg bg-slate-100 text-[8px] sm:text-[7px] font-black text-slate-500 uppercase hover:bg-slate-200 transition-all tracking-tighter">Cierre</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer Actions -->
        <div class="px-5 py-4 bg-slate-50 border-t border-slate-200 flex gap-3">
          <button 
            type="button" 
            class="flex-1 py-2.5 px-4 rounded-xl border border-slate-300 bg-white text-[10px] font-black text-slate-600 hover:bg-slate-100 transition-all uppercase tracking-widest"
            @click="clear"
          >
            Limpiar
          </button>
          <button 
            type="button" 
            class="flex-1 py-2.5 px-4 rounded-xl bg-amber text-slate-900 text-[10px] font-black hover:bg-amber-hover hover:scale-[1.02] transition-all uppercase tracking-widest shadow-lg shadow-amber/10"
            @click="close"
          >
            Aceptar
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, reactive, ref, watch } from "vue"

const props = defineProps({
  modelValue: { type: String, default: "" },
  type: { type: String, default: "datetime" }
})

const emit = defineEmits(["update:modelValue", "change"])

const containerRef = ref(null)
const isOpen = ref(false)
const viewDate = ref(new Date())
const time = reactive({
  hours: 12,
  minutes: 0
})

const monthNames = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

// Formatting current selection for display
const displayValue = computed(() => {
  if (!props.modelValue) return ""
  const date = new Date(props.modelValue)
  
  const options = {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }

  if (props.type === "datetime") {
    options.hour = "2-digit"
    options.minute = "2-digit"
    options.hour12 = false
  }

  return new Intl.DateTimeFormat("es-PE", options).format(date).replace(",", "")
})

const currentMonthName = computed(() => monthNames[viewDate.value.getMonth()])
const currentYear = computed(() => viewDate.value.getFullYear())

// Calendar Logic
const calendarDays = computed(() => {
  const year = viewDate.value.getFullYear()
  const month = viewDate.value.getMonth()
  
  const firstDay = new Date(year, month, 1).getDay()
  // Adjust for Monday-start week (0 is Sunday in JS, we want 0 for Monday)
  const startOffset = firstDay === 0 ? 6 : firstDay - 1
  
  const totalDaysInMonth = new Date(year, month + 1, 0).getDate()
  const totalDaysInPrevMonth = new Date(year, month, 0).getDate()
  
  const days = []
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const selected = props.modelValue ? new Date(props.modelValue) : null
  if (selected) selected.setHours(0, 0, 0, 0)

  // Previous Month Padding
  for (let i = startOffset - 1; i >= 0; i--) {
    const d = totalDaysInPrevMonth - i
    days.push({ id: `prev-${d}`, day: d, isCurrentMonth: false })
  }

  // Current Month
  for (let d = 1; d <= totalDaysInMonth; d++) {
    const dateObj = new Date(year, month, d)
    days.push({
      id: `current-${d}`,
      day: d,
      isCurrentMonth: true,
      isToday: dateObj.getTime() === today.getTime(),
      isSelected: selected && dateObj.getTime() === selected.getTime(),
      date: dateObj
    })
  }

  // Next Month Padding
  const remaining = 42 - days.length
  for (let d = 1; d <= remaining; d++) {
    days.push({ id: `next-${d}`, day: d, isCurrentMonth: false })
  }

  return days
})

// Handlers
function togglePicker() {
  isOpen.value = !isOpen.value
}

function close() {
  isOpen.value = false
}

function clear() {
  emit("update:modelValue", "")
  emit("change", "")
  close()
}

function prevMonth() {
  viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() - 1, 1)
}

function nextMonth() {
  viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() + 1, 1)
}

function selectDay(date) {
  if (!date.isCurrentMonth) return
  
  const newDate = new Date(date.date)
  if (props.type === 'datetime') {
    newDate.setHours(time.hours, time.minutes, 0, 0)
    emit("update:modelValue", newDate.toISOString())
    emit("change", newDate.toISOString())
  } else {
    // For date type, we just want YYYY-MM-DD
    const dateStr = newDate.toISOString().split('T')[0]
    emit("update:modelValue", dateStr)
    emit("change", dateStr)
  }
}

function updateTime() {
  if (!props.modelValue) return
  
  const current = new Date(props.modelValue)
  current.setHours(time.hours, time.minutes, 0, 0)
  
  emit("update:modelValue", current.toISOString())
  emit("change", current.toISOString())
}

// Click outside to close
function handleClickOutside(event) {
  if (containerRef.value && !containerRef.value.contains(event.target)) {
    close()
  }
}

watch(() => props.modelValue, (val) => {
  if (val) {
    const d = new Date(val)
    time.hours = d.getHours()
    time.minutes = d.getMinutes()
    // Align view date if opening for first time or value changes externally
    if (!isOpen.value) {
      viewDate.value = new Date(d.getFullYear(), d.getMonth(), 1)
    }
  }
}, { immediate: true })

onMounted(() => {
  document.addEventListener("click", handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside)
})
</script>

<style scoped>
.picker-fade-enter-active,
.picker-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.picker-fade-enter-from,
.picker-fade-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.95);
  filter: blur(10px);
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}
</style>
