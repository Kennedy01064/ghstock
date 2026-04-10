package com.gh.stock.data.remote.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class TokenResponseDto(
    @SerialName("access_token") val accessToken: String,
    @SerialName("refresh_token") val refreshToken: String,
    @SerialName("token_type") val tokenType: String
)

@Serializable
data class UserDto(
    @SerialName("id") val id: Int,
    @SerialName("username") val username: String,
    @SerialName("name") val name: String?,
    @SerialName("role") val role: String,
    @SerialName("is_active") val isActive: Boolean
)

@Serializable
data class LoginRequestDto(
    @SerialName("username") val username: String,
    @SerialName("password") val password: String
)
