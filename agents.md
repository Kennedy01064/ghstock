# Plan de Migración: Frontend de Flask a Vue 3 (SPA)

## Objetivo Principal
Migrar la actual interfaz de usuario renderizada en servidor (Flask/Jinja) a una Single Page Application (SPA) utilizando Vue 3 y Vite. 
El sistema debe conectarse directamente al backend en FastAPI. 
**Regla de oro:** El diseño visual actual debe mantenerse intacto. Se reutilizarán las clases de Tailwind CSS existentes. Se eliminarán las recargas de página completas, introduciendo transiciones animadas y fluidas entre las distintas vistas.

---

## Fase 1: Inicialización y Configuración Base
**Objetivo:** Establecer el entorno de Vue 3 replicando el entorno de estilos actual.

1. **Creación del Proyecto:**
   - Inicializar un nuevo proyecto con Vite y Vue 3.
   - Configurar Vue Router para el manejo de rutas en el cliente.
   - Configurar Pinia para la gestión del estado (autenticación, inventario global).

2. **Migración de Estilos (Tailwind CSS):**
   - Instalar Tailwind CSS, PostCSS y Autoprefixer en el nuevo proyecto Vue.
   - Copiar el contenido exacto del archivo `tailwind.config.js` del proyecto Flask al nuevo entorno.
   - Copiar los estilos globales (`frontend/app/static/css/input.css` y `main.css`) al directorio `src/assets/` de Vue y asegurar su importación en `main.js`.
   - Migrar los recursos estáticos (imágenes en `frontend/app/static/img/` y `uploads/`) a la carpeta `public/` o `src/assets/` de Vue.

---

## Fase 2: Construcción del Layout Principal (Replicando `base.html`)
**Objetivo:** Transformar la plantilla base de Jinja en componentes reutilizables de Vue.

1. **Componentización Estructural:**
   - Analizar `frontend/app/templates/base.html`.
   - Crear un componente `Sidebar.vue` o `Navbar.vue` (según la estructura actual) copiando el HTML exacto e inyectando las clases de Tailwind.
   - Crear un componente `Layout.vue` que envuelva la navegación y contenga la etiqueta `<router-view>` donde se renderizará el contenido dinámico.

2. **Configuración de Transiciones Globales:**
   - Envolver el `<router-view>` dentro de un componente `<Transition>` de Vue.
   - Definir las clases CSS para una transición fluida (por ejemplo, un *fade-slide* suave):
     ```css
     .fade-enter-active, .fade-leave-active {
       transition: opacity 0.3s ease, transform 0.3s ease;
     }
     .fade-enter-from, .fade-leave-to {
       opacity: 0;
       transform: translateY(10px);
     }
     ```

---

## Fase 3: Migración de Vistas (De Jinja a Vue)
**Objetivo:** Convertir cada archivo `.html` de la carpeta `templates/` a archivos `.vue` de un solo archivo (Single-File Components).

1. **Traducción de Sintaxis Jinja a Vue:**
   - Reemplazar bucles `{% for item en items %}` por `v-for="item in items"`.
   - Reemplazar condicionales `{% if condicion %}` por `v-if="condicion"`.
   - Convertir la inyección de variables `{{ variable }}` a la sintaxis reactiva de Vue.

2. **Migración por Módulos (Orden sugerido):**
   - **Módulo de Autenticación:** `login.html` a `LoginView.vue`.
   - **Módulo de Dashboard:** `index.html`, `admin_dashboard.html`, `manager_dashboard.html` a sus respectivas vistas en Vue.
   - **Módulo de Catálogo:** Vistas de creación/edición de productos y edificios, y `warehouse.html`.
   - **Módulo de Despachos (Dispatch) y Órdenes:** Vistas de `pending_orders.html`, `picking.html`, `history.html`.

---

## Fase 4: Integración Directa con FastAPI
**Objetivo:** Reemplazar las rutas de Flask por llamadas asíncronas desde el cliente.

1. **Cliente API:**
   - Crear un archivo `src/utils/apiClient.js` (basado en el actual `frontend/app/utils/api_client.py` pero usando Axios o Fetch de JavaScript).
   - Configurar interceptores para adjuntar automáticamente el token de autenticación (JWT) en cada petición hacia FastAPI.

2. **Gestión de Estado (Pinia):**
   - Crear un store de autenticación (`authStore.js`) para manejar el login y guardar el token/usuario actual (reemplazando las sesiones de Flask).
   - Conectar las vistas migradas en la Fase 3 para que consuman el `apiClient.js` en los hooks del ciclo de vida de Vue (ej. `onMounted`) y pueblen la interfaz con datos reales.

---

## Fase 5: Refinamiento de Interactividad (Cero Recargas)
**Objetivo:** Asegurar que las acciones del usuario sean instantáneas.

1. **Formularios Dinámicos:**
   - Modificar todos los `<form>` que hacían POST tradicional en Flask para usar `@submit.prevent` en Vue.
   - Manejar el envío de datos de manera asíncrona y mostrar notificaciones de éxito/error directamente en la interfaz sin recargar la página.

2. **Modales y Componentes de UI:**
   - Convertir cualquier modal de Tailwind existente impulsado por Alpine.js o JavaScript puro a componentes condicionales de Vue (`v-if="isModalOpen"`).
   - Aplicar el componente `<Transition>` también a los modales para mantener la sensación de fluidez y modernidad en toda la plataforma.