# Stock Mobile – Android App (Kotlin + Compose)

Esta es la aplicación nativa de Android para el sistema de gestión de inventarios de **Stock**.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Kotlin 2.0+
- **UI:** Jetpack Compose (Declarativo)
- **Arquitectura:** MVVM (Model-View-ViewModel) + Clean Architecture
- **Inyección de Dependencias:** Koin
- **Base de Datos:** Room (para cache local)
- **Networking:** Retrofit 2 + Kotlin Serialization

## 📁 Estructura del Proyecto Recomendada
```text
app/src/main/java/com/gh/stock/
├── data/               # Repositorios, APIs (Retrofit), Modelos de Red
├── domain/             # Casos de Uso, Modelos de Dominio
├── ui/
│   ├── components/     # Composables reutilizables (Botones, Inputs)
│   ├── screens/        # Pantallas completas (Login, Dashboard)
│   ├── theme/          # Colores, Tipografía (Ver docs/MOBILE_IDENTITY.md)
│   └── navigation/     # NavHost y rutas
└── StockApp.kt         # Clase Application (Setup de Koin)
```

## 🚀 Guía de Inicio para Desarrolladores
1. Abrir **Android Studio Jellyfish** (o superior).
2. Crear un nuevo proyecto **"Empty Compose Activity"**.
3. Configurar el package name a `com.gh.stock`.
4. Seguir las guías de diseño en `docs/MOBILE_IDENTITY.md`.
5. Consultar los endpoints en `docs/MOBILE_API_CONTRACT.md`.

---
*Mantenido por Antigravity*
