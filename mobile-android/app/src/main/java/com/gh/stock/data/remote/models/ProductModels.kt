package com.gh.stock.data.remote.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ProductDto(
    @SerialName("id") val id: Int,
    @SerialName("sku") val sku: String?,
    @SerialName("barcode") val barcode: String?,
    @SerialName("name") val name: String,
    @SerialName("categoria") val category: String? = "General",
    @SerialName("description") val description: String?,
    @SerialName("precio") val price: Double?,
    @SerialName("imagen_url") val imageUrl: String?,
    @SerialName("stock_actual") val currentStock: Int,
    @SerialName("stock_minimo") val minStock: Int,
    @SerialName("unit_name") val unitName: String? = "unid.",
    @SerialName("is_active") val isActive: Boolean
)
