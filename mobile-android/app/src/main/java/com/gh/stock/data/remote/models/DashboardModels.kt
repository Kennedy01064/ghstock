package com.gh.stock.data.remote.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ManagerDashboardDto(
    @SerialName("buildings") val buildings: List<BuildingSummaryDto> = emptyList(),
    @SerialName("pedidos_activos") val pedidosActivos: Int = 0,
    @SerialName("pedidos_en_transito") val pedidosEnTransito: Int = 0,
    @SerialName("pedidos_despachados") val pedidosDespachados: List<OrderSummaryDto> = emptyList(),
    @SerialName("historial_pedidos") val historialPedidos: List<OrderSummaryDto> = emptyList(),
    @SerialName("submission_deadline") val submissionDeadline: SubmissionDeadlineDto? = null
)

@Serializable
data class BuildingSummaryDto(
    @SerialName("id") val id: Int,
    @SerialName("name") val name: String,
    @SerialName("address") val address: String? = null,
    @SerialName("imagen_frontis") val imagenFrontis: String? = null,
    @SerialName("active_orders_count") val activeOrdersCount: Int = 0
)

@Serializable
data class OrderSummaryDto(
    @SerialName("id") val id: Int,
    @SerialName("status") val status: String,
    @SerialName("created_at") val createdAt: String,
    @SerialName("building") val building: BuildingNameDto? = null,
    @SerialName("items") val items: List<OrderItemCountDto> = emptyList()
)

@Serializable
data class BuildingNameDto(
    @SerialName("id") val id: Int,
    @SerialName("name") val name: String
)

@Serializable
data class OrderItemCountDto(
    @SerialName("id") val id: Int
)

@Serializable
data class SubmissionDeadlineDto(
    @SerialName("deadline_at") val deadlineAt: String? = null,
    @SerialName("note") val note: String? = null,
    @SerialName("state") val state: String = "active",
    @SerialName("pending_orders_count") val pendingOrdersCount: Int = 0
)
