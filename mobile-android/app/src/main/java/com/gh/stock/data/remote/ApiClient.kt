package com.gh.stock.data.remote

import com.gh.stock.data.remote.services.AuthApiService
import com.gh.stock.data.remote.services.CatalogApiService
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import java.util.concurrent.TimeUnit

/**
 * Singleton para configurar y proveer el cliente de Retrofit.
 * Optimizado para rendimiento en gama baja evitando múltiples instancias de configuración.
 */
object ApiClient {

    private const val BASE_URL = "https://ghstock-production.up.railway.app/api/v1/"

    private val json = Json {
        ignoreUnknownKeys = true
        coerceInputValues = true
        isLenient = true
    }

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .writeTimeout(15, TimeUnit.SECONDS)
        .build()

    private val retrofit: Retrofit by lazy {
        val contentType = "application/json".toMediaType()
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(json.asConverterFactory(contentType))
            .build()
    }

    val authService: AuthApiService by lazy {
        retrofit.create(AuthApiService::class.java)
    }

    val catalogService: CatalogApiService by lazy {
        retrofit.create(CatalogApiService::class.java)
    }

    val operationsService: com.gh.stock.data.remote.services.OperationsApiService by lazy {
        retrofit.create(com.gh.stock.data.remote.services.OperationsApiService::class.java)
    }
}
