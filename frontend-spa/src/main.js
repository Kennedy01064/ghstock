import { createApp } from "vue"
import { createPinia } from "pinia"

import App from "./App.vue"
import router from "./router"
import { useAuthStore } from "./stores/authStore"
import { useSystemStore } from "./stores/systemStore"
import "./assets/input.css"
import "./assets/main.css"

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

await useSystemStore(pinia).fetchPublicStatus()
// Initialize store AFTER router to ensure redirects work correctly
await useAuthStore(pinia).initialize()

app.mount("#app")
