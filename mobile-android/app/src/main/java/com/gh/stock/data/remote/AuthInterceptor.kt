package com.gh.stock.data.remote

import com.gh.stock.data.local.TokenDataStore
import kotlinx.coroutines.runBlocking
import okhttp3.Interceptor
import okhttp3.Response

class AuthInterceptor(private val tokenDataStore: TokenDataStore) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        val token = runBlocking { tokenDataStore.getAccessToken() }
        val request = chain.request().newBuilder().apply {
            if (token != null) {
                addHeader("Authorization", "Bearer $token")
            }
        }.build()

        val response = chain.proceed(request)

        // Si el token expiró, limpiar sesión — la UI reacciona via SessionManager
        if (response.code == 401) {
            runBlocking { tokenDataStore.clearTokens() }
            SessionManager.notifySessionExpired()
        }

        return response
    }
}
