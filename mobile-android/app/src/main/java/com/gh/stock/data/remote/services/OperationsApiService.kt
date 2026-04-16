package com.gh.stock.data.remote.services

import com.gh.stock.data.remote.models.*
import retrofit2.Response
import retrofit2.http.*

interface OperationsApiService {

    @GET("operations/order-deadline")
    suspend fun getOrderDeadline(): Response<OrderSubmissionDeadlineSettingDto>

    @PUT("operations/order-deadline")
    suspend fun updateOrderDeadline(
        @Body deadline: OrderSubmissionDeadlineUpdateDto
    ): Response<OrderSubmissionDeadlineSettingDto>

    @GET("operations/pending-status")
    suspend fun getPendingStatus(
        @Query("building_id") buildingId: Int? = null
    ): Response<PendingTasksStatusDto>

    // --- Inventory Endpoints (Fase 5) ---

    @GET("operations/inventory")
    suspend fun getInventoryByBuilding(
        @Query("building_id") buildingId: Int,
        @Query("search") search: String? = null
    ): Response<List<InventoryItemDto>>

    @POST("inventory/adjust")
    suspend fun adjustStock(@Body request: AdjustStockRequest): Response<Unit>

    @GET("inventory/history")
    suspend fun getInventoryHistory(
        @Query("building_id") buildingId: Int? = null,
        @Query("product_id") productId: Int? = null,
        @Query("movement_type") movementType: String? = null,
        @Query("month") month: Int? = null,
        @Query("year") year: Int? = null,
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 100
    ): Response<List<InventoryMovementDto>>
}
