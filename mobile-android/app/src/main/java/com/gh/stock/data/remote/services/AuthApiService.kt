package com.gh.stock.data.remote.services

import com.gh.stock.data.remote.models.LoginRequestDto
import com.gh.stock.data.remote.models.TokenResponseDto
import com.gh.stock.data.remote.models.UserDto
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.GET
import retrofit2.http.POST

interface AuthApiService {

    /**
     * El backend usa OAuth2 Password Flow (form-urlencoded) por defecto para el login
     */
    @FormUrlEncoded
    @POST("auth/login")
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String
    ): Response<TokenResponseDto>

    @GET("auth/me")
    suspend fun getCurrentUser(): Response<UserDto>

    @POST("auth/refresh")
    suspend fun refreshToken(
        @Field("refresh_token") token: String
    ): Response<TokenResponseDto>
}
