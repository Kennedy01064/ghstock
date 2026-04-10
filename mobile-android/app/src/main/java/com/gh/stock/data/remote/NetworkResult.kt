package com.gh.stock.data.remote

/**
 * Clase sellada para envolver las respuestas de la red y manejar estados.
 * Esto asegura que la UI siempre sepa si los datos están cargando, fueron exitosos o fallaron.
 */
sealed class NetworkResult<T>(
    val data: T? = null,
    val message: String? = null
) {
    class Success<T>(data: T) : NetworkResult<T>(data)
    class Error<T>(message: String, data: T? = null) : NetworkResult<T>(data, message)
    class Loading<T> : NetworkResult<T>()
}
