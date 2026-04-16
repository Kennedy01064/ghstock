package com.gh.stock.data.remote.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class InventoryMovementDto(
    @SerialName("id") val id: Int,
    @SerialName("product_id") val productId: Int,
    @SerialName("quantity") val quantity: Int,
    @SerialName("movement_type") val movementType: String,
    @SerialName("building_id") val buildingId: Int? = null,
    @SerialName("reference_id") val referenceId: Int? = null,
    @SerialName("reference_type") val referenceType: String? = null,
    @SerialName("created_at") val createdAt: String,
    @SerialName("created_by_id") val createdById: Int,
    @SerialName("product") val product: ProductDto
)

@Serializable
data class AnalyticsReportDto(
    @SerialName("pedidos_submitted") val pedidosSubmitted: Int,
    @SerialName("total_edificios_activos") val totalEdificiosActivos: Int,
    @SerialName("costo_despachado_mes") val costoDespachadoMes: Double,
    @SerialName("total_productos") val totalProductos: Int,
    @SerialName("total_movements") val totalMovements: Int,
    @SerialName("total_consumptions") val totalConsumptions: Int,
    @SerialName("most_consumed_product") val mostConsumedProduct: TopProductDto? = null,
    @SerialName("alertas_stock") val alertasStock: List<ProductDto> = emptyList(),
    @SerialName("pedidos_por_edificio") val pedidosPorEdificio: List<BuildingStatsDto> = emptyList(),
    @SerialName("chart_edificios_labels") val chartEdificiosLabels: List<String> = emptyList(),
    @SerialName("chart_edificios_data") val chartEdificiosData: List<Int> = emptyList(),
    @SerialName("chart_productos_labels") val chartProductosLabels: List<String> = emptyList(),
    @SerialName("chart_productos_data") val chartProductosData: List<Int> = emptyList()
)

@Serializable
data class TopProductDto(
    @SerialName("product_name") val productName: String,
    @SerialName("total_consumed") val totalConsumed: Int
)

@Serializable
data class BuildingStatsDto(
    @SerialName("building_name") val buildingName: String,
    @SerialName("total_pedidos") val totalPedidos: Int,
    @SerialName("gasto_total") val gastoTotal: Double? = null
)
