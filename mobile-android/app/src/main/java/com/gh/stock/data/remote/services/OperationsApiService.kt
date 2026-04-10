package com.gh.stock.data.remote.services

import com.gh.stock.data.remote.models.OrderSubmissionDeadlineSettingDto
import com.gh.stock.data.remote.models.OrderSubmissionDeadlineUpdateDto
import com.gh.stock.data.remote.models.PendingTasksStatusDto
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PUT
import retrofit2.http.Query

interface OperationsApiService {

    @GET("operations/order-deadline")
    suspend fun getOrderDeadline(): Response<OrderSubmissionDeadlineSettingDto>

    @PUT("operations/order-deadline")
    suspend fun updateOrderDeadline(
        @Body deadline: OrderSubmissionDeadlineUpdateDto
    ): Response<OrderSubmissionDeadlineSettingDto>

    /**
     * Helper para verificar si hay tareas pendientes (pedidos sin procesar)
     */
    @GET("operations/pending-status")
    suspend fun getPendingStatus(
        @Query("building_id") buildingId: Int? = null
    ): Response<PendingTasksStatusDto>
}
