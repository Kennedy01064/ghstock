package com.gh.stock.data.repository

import com.gh.stock.data.local.TokenDataStore
import com.gh.stock.data.remote.ApiClient
import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.data.remote.models.UserDto
import com.gh.stock.util.safeApiCall

class AuthRepository(private val tokenDataStore: TokenDataStore) {

    suspend fun login(username: String, password: String): NetworkResult<UserDto> {
        val tokenResult = safeApiCall { ApiClient.authService.login(username, password) }

        if (tokenResult is NetworkResult.Error) {
            return NetworkResult.Error(tokenResult.message ?: "Error de autenticacion")
        }

        val tokenResponse = (tokenResult as NetworkResult.Success).data
        if (tokenResponse == null) {
            return NetworkResult.Error("Respuesta de token vacía")
        }
        
        tokenDataStore.saveTokens(tokenResponse.accessToken, tokenResponse.refreshToken)

        // Inicializar el cliente autenticado con el token recien guardado
        ApiClient.initAuthClient(tokenDataStore)

        return safeApiCall { ApiClient.authService.getCurrentUser() }
    }

    suspend fun hasSession(): Boolean = tokenDataStore.getAccessToken() != null

    suspend fun logout() {
        tokenDataStore.clearTokens()
    }
}
