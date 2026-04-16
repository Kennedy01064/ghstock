package com.gh.stock.data.remote.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class OrderDto(
    @SerialName("id") val id: Int,
    @SerialName("building_id") val buildingId: Int,
    @SerialName("created_by_id") val createdById: Int,
    @SerialName("status") val status: String,
    @SerialName("items") val items: List<OrderItemDto> = emptyList(),
    @SerialName("building") val building: BuildingNameDto? = null,
    @SerialName("created_at") val createdAt: String? = null,
    @SerialName("rejection_note") val rejectionNote: String? = null
)

@Serializable
data class OrderItemDto(
    @SerialName("id") val id: Int,
    @SerialName("order_id") val orderId: Int,
    @SerialName("product_id") val productId: Int,
    @SerialName("quantity") val quantity: Int,
    @SerialName("nombre_producto_snapshot") val productNameSnapshot: String? = null,
    @SerialName("precio_unitario") val unitPrice: Double? = 0.0,
    @SerialName("product") val product: ProductDto? = null
)

@Serializable
data class OrderCreateDto(
    @SerialName("building_id") val buildingId: Int
)

@Serializable
data class OrderItemCreateDto(
    @SerialName("product_id") val productId: Int,
    @SerialName("quantity") val quantity: Int
)

@Serializable
data class OrderItemUpdateDto(
    @SerialName("quantity") val quantity: Int
)
