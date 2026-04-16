package com.gh.stock.data.remote.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Representa un producto en el inventario de una sede específica.
 */
@Serializable
data class InventoryItemDto(
    @SerialName("id") val id: Int,
    @SerialName("product_id") val productId: Int,
    @SerialName("building_id") val buildingId: Int,
    @SerialName("current_stock") val currentStock: Double,
    @SerialName("min_stock") val minStock: Double,
    @SerialName("product_name") val productName: String,
    @SerialName("product_sku") val productSku: String? = null,
    @SerialName("product_image") val productImage: String? = null,
    @SerialName("category_name") val categoryName: String? = null,
    @SerialName("unit_name") val unitName: String? = null
)

/**
 * DTO para solicitar un ajuste de stock.
 */
@Serializable
data class StockAdjustmentDto(
    @SerialName("building_id") val buildingId: Int,
    @SerialName("product_id") val productId: Int,
    @SerialName("quantity_change") val quantityChange: Double,
    @SerialName("reason") val reason: String,
    @SerialName("type") val type: String // "ENTRY", "EXIT", "ADJUSTMENT"
)

/**
 * Representa un movimiento histórico en el inventario.
 */
@Serializable
data class MovementDto(
    @SerialName("id") val id: Int,
    @SerialName("product_name") val productName: String,
    @SerialName("type") val type: String,
    @SerialName("quantity") val quantity: Double,
    @SerialName("reason") val reason: String,
    @SerialName("created_at") val createdAt: String,
    @SerialName("user_name") val userName: String
)

@Serializable
data class AdjustStockRequest(
    @SerialName("building_id") val buildingId: Int,
    @SerialName("product_id") val productId: Int,
    @SerialName("quantity_change") val quantityChange: Double,
    @SerialName("reason") val reason: String,
    @SerialName("type") val type: String
)
