# Plan de Diseño — Migración a Tema Gris/Slate

**Contexto:** El cliente reportó que el fondo negro (`#041120` / `#0B1F33`) reduce la visibilidad de algunos elementos. La propuesta es migrar a una paleta **gris oscuro / slate** que mantenga el look profesional pero mejore el contraste percibido y la lectura de texto, botones y controles.

---

## Paleta Actual vs Propuesta

### Fondos principales

| Rol | Color actual | Color propuesto |
|-----|-------------|-----------------|
| Fondo más profundo | `#041120` (`navy-deep`) | `#0f172a` (`slate-deep`) |
| Fondo principal | `#0B1F33` (`navy`) | `#1e293b` (`slate`) |
| Fondo tarjetas/modales | `#06286F` (`navy-accent`) | `#263244` (`slate-accent`) |
| Gradiente custom no tokenizado | `#05142b` (solo en AdminDashboard) | `#172032` |

> **Por qué slate y no gris neutro:** Un gris puro (`#1a1a1a`) se siente apagado. El slate tiene temperatura fría que acompaña el ámbar dorado del acento, conserva el carácter del sistema y da ~30–35% más luminancia — suficiente para que textos secundarios y bordes sean visibles sin cambiar la identidad.

---

## Cambios por componente

### 1. Tokens globales

**`frontend-spa/tailwind.config.js`** — cambiar solo los valores hex, mantener los nombres:

```
navy-deep:   #041120  →  #0f172a
navy:        #0B1F33  →  #1e293b
navy-accent: #06286F  →  #263244
```

**`frontend-spa/src/assets/main.css`** — variables CSS:

```
--navy-default: #0B1F33  →  #1e293b
--navy-accent:  #06286F  →  #263244
--navy-deep:    #041120  →  #0f172a
```

> Mantener los mismos nombres reduce el diff en el resto del código.

---

### 2. Texto

| Rol | Actual | Propuesto |
|-----|--------|-----------|
| Primario | `#ffffff` | Sin cambio |
| Secundario | `rgba(248,245,239, 0.75)` | `rgba(248,245,239, 0.85)` |
| Muted | `rgba(248,245,239, 0.50)` | `rgba(248,245,239, 0.60)` |
| Placeholder inputs | `rgba(248,245,239, 0.15)` | `rgba(248,245,239, 0.25)` |

---

### 3. Tarjetas (Cards)

| Elemento | Actual | Propuesto |
|----------|--------|-----------|
| Fondo | `rgba(255,255,255, 0.03)` | `rgba(255,255,255, 0.04)` |
| Hover fondo | `rgba(255,255,255, 0.05)` | `rgba(255,255,255, 0.06)` |
| Header | `rgba(255,255,255, 0.02)` | `rgba(255,255,255, 0.03)` |
| Borde | `rgba(255,255,255, 0.10)` | `rgba(255,255,255, 0.12)` |
| Hover borde | `rgba(242,173,61, 0.20)` | Sin cambio |
| Divisores | `rgba(255,255,255, 0.05)` | `rgba(255,255,255, 0.07)` |

---

### 4. Navbar

| Elemento | Actual | Propuesto |
|----------|--------|-----------|
| Fondo inline | `rgba(4,17,32, 0.92)` | `rgba(15,23,42, 0.92)` |
| Borde inline | `rgba(255,255,255, 0.08)` | `rgba(255,255,255, 0.10)` |
| Menú móvil | `bg-navy` | automático por token |

**Archivo:** `frontend-spa/src/components/AppNavbar.vue` — estilos inline en línea 4, reemplazar directamente.

---

### 5. Botones

| Variante | Elemento | Actual | Propuesto |
|----------|----------|--------|-----------|
| Secundario/Outline | Fondo | `rgba(255,255,255, 0.04)` | `rgba(255,255,255, 0.06)` |
| Secundario/Outline | Fondo hover | `rgba(255,255,255, 0.08)` | `rgba(255,255,255, 0.10)` |
| Secundario/Outline | Borde | `rgba(255,255,255, 0.10)` | `rgba(255,255,255, 0.14)` |
| Primario (ámbar) | Todo | Sin cambio | Sin cambio |
| Danger / Success | Todo | Sin cambio | Sin cambio |

---

### 6. Inputs y Selects

| Elemento | Actual | Propuesto |
|----------|--------|-----------|
| Fondo input | `rgba(255,255,255, 0.04)` | `rgba(255,255,255, 0.06)` |
| Fondo focus | `rgba(255,255,255, 0.07)` | `rgba(255,255,255, 0.09)` |
| Borde normal | `rgba(255,255,255, 0.10)` | `rgba(255,255,255, 0.14)` |
| Borde focus | `rgba(242,173,61, 0.40)` | Sin cambio |
| Fondo `<option>` (select nativo) | `#041120` | `#1e293b` |
| Flecha SVG (data URI en main.css) | `%23F2AD3D` | Sin cambio |

---

### 7. Pills / Badges / Checkboxes

| Elemento | Actual | Propuesto |
|----------|--------|-----------|
| Pill fondo | `rgba(200,166,107, 0.10)` | `rgba(200,166,107, 0.14)` |
| Pill borde | `rgba(200,166,107, 0.15)` | `rgba(200,166,107, 0.20)` |
| Badge inactivo | `bg-white/5` | `bg-white/8` |
| Checkbox fondo | `rgba(255,255,255, 0.05)` | `rgba(255,255,255, 0.08)` |
| Checkbox borde | `rgba(255,255,255, 0.10)` | `rgba(255,255,255, 0.15)` |

---

### 8. Scrollbars (scoped — varios archivos)

Los estilos de scrollbar están duplicados en `<style scoped>` de varios componentes en lugar de centralizarse. Todos usan los mismos colores:

| Elemento | Actual | Propuesto |
|----------|--------|-----------|
| Track | `rgba(255,255,255, 0.02)` | `rgba(255,255,255, 0.03)` |
| Thumb | `rgba(255,255,255, 0.10)` | `rgba(255,255,255, 0.14)` |
| Thumb hover | `rgba(242,173,61, 0.30)` | Sin cambio |

**Archivos con estilos de scrollbar hardcodeados** (requieren edición individual):

| Archivo | Línea(s) |
|---------|----------|
| `src/views/dashboard/IndexView.vue` | 441–457 |
| `src/views/catalog/ListAdminsView.vue` | 410–423 |
| `src/views/catalog/EditAdminView.vue` | 303 |
| `src/views/catalog/WarehouseView.vue` | 254 |
| `src/views/catalog/UploadCsvView.vue` | 254, 274 |
| `src/views/dispatch/purchases/CreateView.vue` | 300–316 |

---

### 9. Gradiente de AdminDashboard

**Archivo:** `src/views/dashboard/AdminDashboardView.vue` — línea 9

```html
<!-- ACTUAL -->
class="bg-gradient-to-br from-[#041120] via-[#05142b] to-black"

<!-- PROPUESTO -->
class="bg-gradient-to-br from-[#0f172a] via-[#172032] to-[#0a1220]"
```

---

### 10. Clases Tailwind con valores arbitrarios hardcodeados

Estos bypasean el sistema de tokens y requieren edición directa:

| Archivo | Línea | Clase actual | Clase propuesta |
|---------|-------|-------------|-----------------|
| `src/components/PremiumDateTimePicker.vue` | 27 | `bg-[#0B1F33]` | `bg-navy` (usa el token) |
| `src/views/dispatch/SimpleFormPage.vue` | 45 | `accent-[#F2AD3D]` | `accent-amber` |
| `src/views/dispatch/PickingView.vue` | 31 | `accent-[#F2AD3D]` | `accent-amber` |
| `src/views/orders/PendingOrdersView.vue` | 27 | `accent-[#F2AD3D]` | `accent-amber` |
| `src/views/users/AssignBuildingView.vue` | 44 | `accent-[#F2AD3D]` | `accent-amber` |

> Los `accent-[#F2AD3D]` solo afectan el color de checkboxes nativos del navegador — si se cambian a `accent-amber` quedan tokenizados y no necesitan edición manual en el futuro. El fondo no cambia aquí, solo el ámbar.

---

### 11. Colores en configuración de Chart.js (JavaScript)

Los gráficos usan colores en objetos JS — no CSS — por lo que Tailwind no los toca.

**Archivos:** `src/views/dashboard/IndexView.vue` y `src/views/dashboard/ManagerDashboardView.vue`

| Elemento | Color actual | Propuesto |
|----------|-------------|-----------|
| Tooltip background | `#0B1F33` | `#1e293b` |
| Borde exterior doughnut | `#041120` | `#0f172a` |
| Segmento navy-accent en doughnut | `#06286F` | `#263244` |
| Gradiente de líneas (ámbar) | `#F2AD3D` | Sin cambio |
| Segmentos indigo/emerald/gray | `#4F46E5`, `#10B981`, `#6B7280` | Sin cambio |

**Líneas afectadas:** IndexView ~374, ~405, ~427 · ManagerDashboardView ~569, ~600, ~627

---

## Lo que NO cambia

- Acento principal: ámbar `#F2AD3D` / `#D9921E` / `#C8A66B`
- Colores semánticos: emerald (éxito), rose (error), indigo (info)
- Efectos glassmorphism: `backdrop-filter: blur(12px)`
- Sombras amber, animaciones, transiciones, tipografía

---

## Inventario completo de archivos a modificar

| Archivo | Tipo de cambio |
|---------|---------------|
| `tailwind.config.js` | Cambiar hex de tokens `navy.*` |
| `src/assets/main.css` | Variables CSS, `.card`, `.input-field`, `.select-field`, `.btn-secondary`, `.pill`, `.checkbox-premium`, `.custom-scrollbar`, `.select-field option` |
| `src/assets/input.css` | Revisar colores hardcodeados en capas `@layer` |
| `src/components/AppNavbar.vue` | Estilos inline en línea 4 |
| `src/components/PremiumDateTimePicker.vue` | Clase arbitraria `bg-[#0B1F33]` → `bg-navy` |
| `src/views/dashboard/AdminDashboardView.vue` | Clases de gradiente hardcodeadas |
| `src/views/dashboard/IndexView.vue` | Colores Chart.js + scrollbar scoped |
| `src/views/dashboard/ManagerDashboardView.vue` | Colores Chart.js |
| `src/views/catalog/ListAdminsView.vue` | Scrollbar scoped |
| `src/views/catalog/EditAdminView.vue` | Scrollbar scoped |
| `src/views/catalog/WarehouseView.vue` | Scrollbar scoped |
| `src/views/catalog/UploadCsvView.vue` | Scrollbar scoped |
| `src/views/dispatch/purchases/CreateView.vue` | Scrollbar scoped |
| `src/views/dispatch/SimpleFormPage.vue` | `accent-[#F2AD3D]` → `accent-amber` |
| `src/views/dispatch/PickingView.vue` | `accent-[#F2AD3D]` → `accent-amber` |
| `src/views/orders/PendingOrdersView.vue` | `accent-[#F2AD3D]` → `accent-amber` |
| `src/views/users/AssignBuildingView.vue` | `accent-[#F2AD3D]` → `accent-amber` |

**Total: 17 archivos**

---

## Comparación visual rápida

```
ANTES (navy)                   DESPUÉS (slate)
─────────────────────────────────────────────────────
Fondo app:    ████ #041120     Fondo app:    ████ #0f172a  (+30% lum.)
Fondo card:   ████ #0B1F33     Fondo card:   ████ #1e293b  (+35% lum.)
Modal/overlay:████ #06286F     Modal/overlay:████ #263244  (+20% lum.)
Acento:       ████ #F2AD3D     Acento:       ████ #F2AD3D  (sin cambio)
```

---

*Plan listo para implementación. Aprobado el plan, los cambios se ejecutan en el orden: tokens globales → main.css → componentes individuales → Chart.js.*
