package com.gh.stock.util

import com.gh.stock.data.remote.NetworkResult
import retrofit2.Response

suspend fun <T> safeApiCall(call: suspend () -> Response<T>): NetworkResult<T> {
    return try {
        val response = call()
        if (response.isSuccessful) {
            val body = response.body()
            if (body != null) {
                NetworkResult.Success(body)
            } else {
                NetworkResult.Error("Cuerpo de respuesta vacío")
            }
        } else {
            NetworkResult.Error("Error: ${response.code()} ${response.message()}")
        }
    } catch (e: Exception) {
        NetworkResult.Error(e.message ?: "Error desconocido")
    }
}
