# PLAN DE DESARROLLO — Stock Mobile Android

Estado auditado al 2026-04-10. Completitud actual estimada: **~20-25%**.  
La app **no arranca** en su estado actual (ver Fase 0).

---

## Resumen de fases

| Fase | Descripcion | Estimado |
|------|-------------|----------|
| 0 | Corregir bloqueantes de compilacion/runtime | 2-3 h |
| 1 | Autenticacion real + almacenamiento de token | 5-7 h |
| 2 | Navegacion con NavGraph | 3-4 h |
| 3 | Dashboard funcional | 4-5 h |
| 4 | Catalogo de productos | 5-7 h |
| 5 | Inventario por sede + ajuste de stock | 6-8 h |
| 6 | Escaner de codigo de barras | 4-5 h |
| 7 | Cache local con Room | 4-6 h |
| 8 | Pulido, manejo de errores, testing | 6-8 h |

---

## Fase 0 — Que compile y arranque
> **Prioridad maxima.** Ninguna otra fase se puede ejecutar hasta resolver esto.

### 0.1 Corregir `libs.versions.toml` (linea 32)
**Archivo:** `gradle/libs.versions.toml`  
**Problema:** Comilla faltante en el plugin ID de Kotlin.  
```toml
# INCORRECTO
kotlin-android = { id = "org.jetbrains.kotlin = "kotlin", version.ref = "kotlin" }

# CORRECTO
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
```

### 0.2 Corregir import en `GlassComponents.kt`
**Archivo:** `ui/components/GlassComponents.kt`  
**Problema:** Clase inexistente `RoundedCornerSender`.  
```kotlin
// INCORRECTO
import androidx.compose.foundation.shape.RoundedCornerSender

// CORRECTO
import androidx.compose.foundation.shape.RoundedCornerShape
```

### 0.3 Crear `res/values/strings.xml`
**Archivo nuevo:** `app/src/main/res/values/strings.xml`  
**Problema:** `AndroidManifest.xml` referencia `@string/app_name` pero el archivo no existe.  
```xml
<resources>
    <string name="app_name">Stock GH</string>
</resources>
```
Tambien crear `res/mipmap-*` con iconos de la app, o usar el launcher icon por defecto de Android Studio.

### 0.4 Crear `StockApp.kt`
**Archivo nuevo:** `app/src/main/java/com/gh/stock/StockApp.kt`  
**Problema:** `AndroidManifest.xml` declara `android:name=".StockApp"` pero el archivo no existe → `ClassNotFoundException` en arranque.  
```kotlin
class StockApp : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@StockApp)
            modules(appModule)
        }
    }
}
```

### 0.5 Definir `OrderSubmissionDeadlineUpdateDto`
**Archivo:** `data/remote/models/SystemModels.kt`  
**Problema:** `OperationsApiService` importa este DTO pero no esta definido.  
```kotlin
@Serializable
data class OrderSubmissionDeadlineUpdateDto(
    @SerialName("deadline_at") val deadlineAt: String?,
    val note: String? = null,
    @SerialName("is_active") val isActive: Boolean = true
)
```

### 0.6 Exponer `CatalogApiService` en `ApiClient`
**Archivo:** `data/remote/ApiClient.kt`  
**Problema:** `CatalogApiService` esta definida pero no es accesible desde `ApiClient`.  
```kotlin
// Agregar dentro del objeto ApiClient:
val catalogService: CatalogApiService by lazy {
    retrofit.create(CatalogApiService::class.java)
}
```

### 0.7 Crear modulo Koin base
**Archivo nuevo:** `app/src/main/java/com/gh/stock/di/AppModule.kt`  
**Problema:** Koin declarado en build.gradle pero ningun modulo configurado. ViewModels instanciados manualmente.  
```kotlin
val appModule = module {
    single { ApiClient.authService }
    single { ApiClient.catalogService }
    single { NotificationRepository(get()) }
    viewModel { DashboardViewModel(get()) }
    // Agregar ViewModels en fases posteriores
}
```

---

## Fase 1 — Autenticacion real
> Sin un token valido, todos los endpoints retornan 401.

### 1.1 Almacenamiento de token con DataStore
**Archivo nuevo:** `data/local/TokenDataStore.kt`  
Usar `androidx.datastore:datastore-preferences`. Guardar `access_token` de forma persistente.  
```kotlin
class TokenDataStore(private val context: Context) {
    suspend fun saveToken(token: String)
    suspend fun getToken(): String?
    suspend fun clearToken()
}
```
Agregar al modulo Koin: `single { TokenDataStore(androidContext()) }`

### 1.2 Auth Interceptor de OkHttp
**Archivo:** `data/remote/ApiClient.kt`  
**Problema critico:** Ninguna peticion lleva el header `Authorization: Bearer`.  
```kotlin
class AuthInterceptor(private val tokenDataStore: TokenDataStore) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = runBlocking { tokenDataStore.getToken() }
        val request = chain.request().newBuilder()
            .apply { if (token != null) addHeader("Authorization", "Bearer $token") }
            .build()
        return chain.proceed(request)
    }
}
```
Agregar el interceptor al `OkHttpClient` en `ApiClient`.

### 1.3 Conectar `LoginScreen` al API real
**Archivos:** `ui/screens/login/LoginScreen.kt` + nuevo `LoginViewModel.kt`  
Crear `LoginViewModel` que:
1. Llame a `AuthApiService.login(username, password)`
2. En exito: guarde el token via `TokenDataStore` y navegue a Dashboard
3. En error: muestre mensaje en pantalla (estado `LoginUiState.Error`)

**Archivo nuevo:** `data/repository/AuthRepository.kt`  
Wrapper que encapsula `AuthApiService` y `TokenDataStore`.

### 1.4 Manejo de token expirado
En `AuthInterceptor`, si la respuesta es 401:
1. Intentar refresh con `AuthApiService.refreshToken()`
2. Si el refresh falla → limpiar token y emitir evento de "sesion expirada"
3. `MainActivity` escucha ese evento y navega a Login

---

## Fase 2 — Navegacion
> Prerequisito: Fase 1 completa.

### 2.1 Crear NavGraph
**Archivo nuevo:** `ui/navigation/NavGraph.kt`  
Rutas tipadas con `sealed class Screen`:
```kotlin
sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Dashboard : Screen("dashboard")
    object Catalog : Screen("catalog")
    object ProductDetail : Screen("product/{productId}")
    object Inventory : Screen("inventory/{buildingId}")
}
```

### 2.2 Reemplazar navegacion por strings en `MainActivity`
**Archivo:** `MainActivity.kt`  
Reemplazar el `when("login")` hardcodeado por un `NavHost` real.

### 2.3 Check de sesion al inicio
Al arrancar la app, leer `TokenDataStore`:
- Si hay token → navegar directamente a Dashboard (sin mostrar Login)
- Si no hay token → mostrar Login

---

## Fase 3 — Dashboard funcional
> Prerequisito: Fases 1 y 2 completas.

### 3.1 Endpoint de dashboard manager
**API:** `GET /dashboard/manager` (ver `MOBILE_API_CONTRACT.md`)  
**Archivos nuevos:**
- `data/remote/services/DashboardApiService.kt`
- `data/remote/models/DashboardModels.kt` (ManagerDashboardDto, BuildingSummaryDto)
- `data/repository/DashboardRepository.kt`

### 3.2 Tarjetas de edificios asignados
Iterar `dashboard.buildings` y mostrar:
- Nombre del edificio
- Conteo de pedidos activos
- Boton "Ver inventario" → navega a `Inventory/{buildingId}`

### 3.3 Tarjetas de metricas
Mostrar: pedidos pendientes, pedidos en transito, total de SKUs.

### 3.4 Completar `DashboardViewModel`
El `DashboardViewModel` actual solo maneja el deadline banner. Expandirlo para cargar tambien los datos del dashboard (buildings, metricas).

---

## Fase 4 — Catalogo de productos
> Prerequisito: Fase 2 completa.

### 4.1 Pantalla de lista de productos
**Archivo nuevo:** `ui/screens/catalog/CatalogScreen.kt`  
- `LazyColumn` con tarjetas de producto (imagen, nombre, SKU, stock actual)
- Barra de busqueda en la parte superior
- Filtro por categoria
- Imagen con placeholder si `imagen_url` es null
- `CatalogApiService` ya esta definido, solo falta la UI y el ViewModel

### 4.2 `CatalogViewModel`
**Archivo nuevo:** `ui/screens/catalog/CatalogViewModel.kt`  
- Cargar productos paginados (`skip`/`limit`)
- Filtrar por `search` y `category_id`
- Estado: `loading`, `products`, `error`, `endReached`

### 4.3 Pantalla de detalle de producto
**Archivo nuevo:** `ui/screens/catalog/ProductDetailScreen.kt`  
- Imagen grande del producto
- Nombre, SKU, categoria, unidad, precio
- Stock actual vs stock minimo (barra de progreso con color amber si critico)
- Boton "Ajustar Stock" → navega a flujo de ajuste (Fase 5)

### 4.4 Repository de catalogo
**Archivo nuevo:** `data/repository/CatalogRepository.kt`  
Encapsula `CatalogApiService`. En Fase 7 aqui se agrega el cache Room.

---

## Fase 5 — Inventario por sede + ajuste de stock
> Prerequisito: Fase 3 (Dashboard con navegacion a edificio).

### 5.1 Servicios de API faltantes
**Archivo:** `data/remote/services/OperationsApiService.kt`  
Agregar los 3 endpoints que faltan:
```kotlin
@GET("inventory/status/{buildingId}")
suspend fun getInventoryByBuilding(@Path("buildingId") buildingId: Int): List<InventoryItemDto>

@GET("inventory/movements")
suspend fun getMovements(@Query("product_id") productId: Int): List<MovementDto>

@POST("inventory/adjustments")
suspend fun adjustStock(@Body payload: StockAdjustmentDto): InventoryItemDto
```

### 5.2 Modelos de inventario
**Archivo nuevo/actualizar:** `data/remote/models/InventoryModels.kt`  
```kotlin
@Serializable data class InventoryItemDto(...)
@Serializable data class MovementDto(...)
@Serializable data class StockAdjustmentDto(
    @SerialName("product_id") val productId: Int,
    @SerialName("building_id") val buildingId: Int,
    val quantity: Int,
    val notes: String? = null
)
```

### 5.3 Pantalla de inventario por sede
**Archivo nuevo:** `ui/screens/inventory/InventoryScreen.kt`  
- Lista de productos en esa sede con su stock actual
- Indicador visual: verde (ok), amber (bajo), rojo (critico)
- Tap en producto → ver historial de movimientos

### 5.4 Bottom sheet de ajuste de stock
**Archivo nuevo:** `ui/screens/inventory/AdjustStockSheet.kt`  
- Campo numerico para cantidad
- Boton "Sumar" / "Restar" / "Establecer"
- Confirmacion con feedback haptico

---

## Fase 6 — Escaner de codigo de barras
> Prerequisito: Fase 4 (Catalogo funcional).

### 6.1 Permiso de camara
**Archivo:** `AndroidManifest.xml`  
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-feature android:name="android.hardware.camera" android:required="false" />
```
Solicitar permiso en runtime con `rememberPermissionState` (Accompanist).

### 6.2 Dependencia de escaneo
Agregar a `build.gradle.kts`:
```kotlin
implementation("com.google.mlkit:barcode-scanning:17.2.0")
// o usar CameraX + ML Kit
implementation("androidx.camera:camera-camera2:1.3.0")
implementation("androidx.camera:camera-lifecycle:1.3.0")
implementation("androidx.camera:camera-view:1.3.0")
```

### 6.3 Pantalla de escaneo
**Archivo nuevo:** `ui/screens/catalog/BarcodeScannerScreen.kt`  
- Preview de camara fullscreen
- Overlay con reticula de escaneo
- Al detectar codigo → llamar `GET /catalog/products/barcode/{code}`
- Exito: navegar a `ProductDetail`
- No encontrado: mostrar dialogo "Producto no registrado"

---

## Fase 7 — Cache local con Room
> Prerequisito: Fases 4 y 5 completadas.

### 7.1 Configurar Room
**Archivos nuevos en** `data/local/`:
- `AppDatabase.kt` (RoomDatabase)
- `entities/ProductEntity.kt`
- `entities/InventoryItemEntity.kt`
- `dao/ProductDao.kt`
- `dao/InventoryDao.kt`

### 7.2 Estrategia de cache
- Al abrir `CatalogScreen`: mostrar datos locales inmediatamente, luego actualizar desde API en segundo plano
- Al abrir `InventoryScreen`: misma estrategia
- TTL de 15 minutos: si los datos tienen mas de 15 minutos, forzar refresh
- `CatalogRepository` actua como fuente unica de verdad (single source of truth)

### 7.3 Agregar al modulo Koin
```kotlin
single { Room.databaseBuilder(androidContext(), AppDatabase::class.java, "stock_db").build() }
single { get<AppDatabase>().productDao() }
single { get<AppDatabase>().inventoryDao() }
```

---

## Fase 8 — Pulido final

### 8.1 Pantalla de error global
Componente reutilizable `ErrorScreen` con:
- Icono de error
- Mensaje descriptivo
- Boton "Reintentar"

### 8.2 Estados de carga
Todos los `LazyColumn` deben tener skeleton loaders (rectangulos animados con shimmer) en lugar de spinners.

### 8.3 Feedback haptico
En acciones criticas (ajuste de stock, escaneo exitoso): usar `HapticFeedbackType.LongPress`.

### 8.4 Pantalla de perfil / configuracion
- Mostrar nombre de usuario y rol
- Boton "Cerrar sesion" (limpia `TokenDataStore` y navega a Login)

### 8.5 Manejo de conectividad
Detectar cuando no hay red y mostrar banner de "Sin conexion" en lugar de errores generico.

---

## Estructura de archivos objetivo

```
app/src/main/java/com/gh/stock/
├── StockApp.kt                          [CREAR - Fase 0]
├── MainActivity.kt                      [MODIFICAR - Fase 2]
├── di/
│   └── AppModule.kt                     [CREAR - Fase 0]
├── data/
│   ├── local/                           [CREAR - Fase 7]
│   │   ├── AppDatabase.kt
│   │   ├── TokenDataStore.kt            [CREAR - Fase 1]
│   │   ├── dao/
│   │   │   ├── ProductDao.kt
│   │   │   └── InventoryDao.kt
│   │   └── entities/
│   │       ├── ProductEntity.kt
│   │       └── InventoryItemEntity.kt
│   ├── remote/
│   │   ├── ApiClient.kt                 [MODIFICAR - Fases 0, 1]
│   │   ├── AuthInterceptor.kt           [CREAR - Fase 1]
│   │   ├── NetworkResult.kt             [OK]
│   │   ├── models/
│   │   │   ├── AuthModels.kt            [OK]
│   │   │   ├── ProductModels.kt         [OK]
│   │   │   ├── SystemModels.kt          [MODIFICAR - Fase 0]
│   │   │   ├── DashboardModels.kt       [CREAR - Fase 3]
│   │   │   └── InventoryModels.kt       [CREAR - Fase 5]
│   │   └── services/
│   │       ├── AuthApiService.kt        [OK]
│   │       ├── CatalogApiService.kt     [OK]
│   │       ├── DashboardApiService.kt   [CREAR - Fase 3]
│   │       └── OperationsApiService.kt  [MODIFICAR - Fase 5]
│   └── repository/
│       ├── AuthRepository.kt            [CREAR - Fase 1]
│       ├── CatalogRepository.kt         [CREAR - Fase 4]
│       ├── DashboardRepository.kt       [CREAR - Fase 3]
│       ├── InventoryRepository.kt       [CREAR - Fase 5]
│       └── NotificationRepository.kt   [OK]
├── ui/
│   ├── components/
│   │   ├── GlassComponents.kt           [CORREGIR - Fase 0]
│   │   ├── SkeletonLoader.kt            [CREAR - Fase 8]
│   │   └── ErrorScreen.kt              [CREAR - Fase 8]
│   ├── navigation/
│   │   └── NavGraph.kt                  [CREAR - Fase 2]
│   ├── screens/
│   │   ├── login/
│   │   │   ├── LoginScreen.kt           [MODIFICAR - Fase 1]
│   │   │   └── LoginViewModel.kt        [CREAR - Fase 1]
│   │   ├── dashboard/
│   │   │   ├── DashboardScreen.kt       [MODIFICAR - Fase 3]
│   │   │   ├── DashboardViewModel.kt    [MODIFICAR - Fase 3]
│   │   │   └── components/
│   │   │       └── DeadlineBanner.kt    [OK]
│   │   ├── catalog/
│   │   │   ├── CatalogScreen.kt         [CREAR - Fase 4]
│   │   │   ├── CatalogViewModel.kt      [CREAR - Fase 4]
│   │   │   ├── ProductDetailScreen.kt   [CREAR - Fase 4]
│   │   │   └── BarcodeScannerScreen.kt  [CREAR - Fase 6]
│   │   └── inventory/
│   │       ├── InventoryScreen.kt       [CREAR - Fase 5]
│   │       ├── InventoryViewModel.kt    [CREAR - Fase 5]
│   │       └── AdjustStockSheet.kt      [CREAR - Fase 5]
│   └── theme/
│       ├── Color.kt                     [OK]
│       └── Theme.kt                     [OK]
└── util/
    └── NetworkUtils.kt                  [OK]
```

---

## Dependencias adicionales a agregar en `build.gradle.kts`

```kotlin
// DataStore (token storage)
implementation("androidx.datastore:datastore-preferences:1.1.1")

// Room (cache local)
implementation("androidx.room:room-runtime:2.6.1")
implementation("androidx.room:room-ktx:2.6.1")
ksp("androidx.room:room-compiler:2.6.1")

// CameraX + ML Kit (barcode)
implementation("androidx.camera:camera-camera2:1.3.4")
implementation("androidx.camera:camera-lifecycle:1.3.4")
implementation("androidx.camera:camera-view:1.3.4")
implementation("com.google.mlkit:barcode-scanning:17.2.0")

// Coil (carga de imagenes desde URL)
implementation("io.coil-kt:coil-compose:2.6.0")

// Accompanist (permisos en Compose)
implementation("com.google.accompanist:accompanist-permissions:0.34.0")
```

---

*Plan generado el 2026-04-10 — Stock Mobile Android v1.0*
