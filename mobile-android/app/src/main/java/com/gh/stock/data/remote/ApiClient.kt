package com.gh.stock.data.remote

import com.gh.stock.data.local.TokenDataStore
import com.gh.stock.data.remote.services.AuthApiService
import com.gh.stock.data.remote.services.CatalogApiService
import com.gh.stock.data.remote.services.DashboardApiService
import com.gh.stock.data.remote.services.OperationsApiService
import com.gh.stock.data.remote.services.OrdersApiService
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import java.util.concurrent.TimeUnit

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

    // Cliente sin auth — solo para el endpoint de login
    private val publicClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .writeTimeout(15, TimeUnit.SECONDS)
        .build()

    // Cliente con auth — para todos los endpoints protegidos
    private var _authenticatedClient: OkHttpClient? = null

    fun initAuthClient(tokenDataStore: TokenDataStore) {
        _authenticatedClient = OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor(tokenDataStore))
            .addInterceptor(loggingInterceptor)
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(15, TimeUnit.SECONDS)
            .writeTimeout(15, TimeUnit.SECONDS)
            .build()
    }

    private fun buildRetrofit(client: OkHttpClient): Retrofit {
        val contentType = "application/json".toMediaType()
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(json.asConverterFactory(contentType))
            .build()
    }

    // Retrofit publico (login)
    private val publicRetrofit: Retrofit by lazy { buildRetrofit(publicClient) }

    // Retrofit autenticado (lazy — se construye tras initAuthClient)
    private val authRetrofit: Retrofit get() = buildRetrofit(
        _authenticatedClient ?: publicClient
    )

    val authService: AuthApiService by lazy {
        publicRetrofit.create(AuthApiService::class.java)
    }

    val catalogService: CatalogApiService get() =
        authRetrofit.create(CatalogApiService::class.java)

    val dashboardService: DashboardApiService get() =
        authRetrofit.create(DashboardApiService::class.java)

    val operationsService: OperationsApiService get() =
        authRetrofit.create(OperationsApiService::class.java)

    val ordersService: OrdersApiService get() =
        authRetrofit.create(OrdersApiService::class.java)
}
