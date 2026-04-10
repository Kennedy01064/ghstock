# Contrato de API – Stock Mobile (Android)

Este documento resume los endpoints fundamentales que la aplicación Android consumirá para las operaciones básicas de inventario.

## 1. Autenticación
*   **Base URL:** `https://ghstock-production.up.railway.app/api/v1`
*   **Endpoint:** `POST /auth/access-token`
*   **Formato:** `application/x-www-form-urlencoded`
*   **Parámetros:** `username`, `password`
*   **Respuesta Exitosa:**
    ```json
    {
      "access_token": "eyJhbGci...",
      "token_type": "bearer",
      "user": { "username": "...", "role": "..." }
    }
    ```

## 2. Catálogo y Búsqueda
*   **Listar Productos:** `GET /catalog/products`
*   **Detalle por ID:** `GET /catalog/products/{product_id}`
*   **Búsqueda / Filtro:** `GET /catalog/products?search={query}&category_id={id}`
*   **Sugerencia:** Implementar cache local (Room) para que la búsqueda sea instantánea.

## 3. Inventario y Movimientos
*   **Consulta de Stock por Edificio:** `GET /inventory/status/{building_id}`
*   **Historial de Movimientos:** `GET /inventory/movements?product_id={id}`
*   **Ajuste de Stock (Rápido):** `POST /inventory/adjustments`

## 4. Multimedia (Cámara)
*   **Subida de Imágenes:** `POST /media/upload`
*   **Content-Type:** `multipart/form-data`
*   **Campo:** `file` (Binary)
*   **Respuesta:** `{"url": "...", "storage": "supabase"}`

## Convenciones Técnicas
1.  **Header Obligatorio:** `Authorization: Bearer <JWT_TOKEN>` en todas las peticiones excepto Login.
2.  **Manejo de Errores:** La API devuelve códigos de estado HTTP estándar (401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Validation Error).
3.  **Snake Case:** La API utiliza `snake_case` para las llaves JSON. Se recomienda mapear a `camelCase` en Kotlin usando `@SerialName`.
