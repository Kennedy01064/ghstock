package com.gh.stock.data.remote.services

import com.gh.stock.data.remote.models.*
import retrofit2.Response
import retrofit2.http.*

interface OrdersApiService {

    @GET("orders")
    suspend fun getOrders(
        @Query("status") status: String? = null,
        @Query("building_id") buildingId: Int? = null,
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 100
    ): Response<List<OrderDto>>

    @GET("orders/{id}")
    suspend fun getOrderById(@Path("id") id: Int): Response<OrderDto>

    @POST("orders")
    suspend fun createOrder(@Body order: OrderCreateDto): Response<OrderDto>

    @POST("orders/{id}/items")
    suspend fun addOrderItem(
        @Path("id") id: Int,
        @Body item: OrderItemCreateDto
    ): Response<OrderItemDto>

    @POST("orders/{id}/submit")
    suspend fun submitOrder(@Path("id") id: Int): Response<OrderDto>

    @POST("orders/{id}/receive")
    suspend fun receiveOrder(@Path("id") id: Int): Response<OrderDto>

    @POST("orders/{id}/cancel")
    suspend fun cancelOrder(@Path("id") id: Int): Response<OrderDto>
}
