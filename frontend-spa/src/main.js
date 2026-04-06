import { createApp } from "vue"
import { createPinia } from "pinia"

import App from "./App.vue"
import router from "./router"
import { useAuthStore } from "./stores/authStore"
import "./assets/input.css"
import "./assets/main.css"

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
await useAuthStore(pinia).initialize()
app.use(router)
app.mount("#app")
