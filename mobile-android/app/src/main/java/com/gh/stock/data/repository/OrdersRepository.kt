package com.gh.stock.data.repository

import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.data.remote.models.*
import com.gh.stock.data.remote.services.OrdersApiService
import com.gh.stock.util.safeApiCall
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class OrdersRepository(private val api: OrdersApiService) {

    suspend fun getOrders(
        status: String? = null,
        buildingId: Int? = null
    ): Flow<NetworkResult<List<OrderDto>>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { api.getOrders(status, buildingId) })
    }

    suspend fun getOrderById(id: Int): Flow<NetworkResult<OrderDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { api.getOrderById(id) })
    }

    suspend fun createOrder(buildingId: Int): Flow<NetworkResult<OrderDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { api.createOrder(OrderCreateDto(buildingId)) })
    }

    suspend fun addOrderItem(orderId: Int, productId: Int, quantity: Int): Flow<NetworkResult<OrderItemDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { api.addOrderItem(orderId, OrderItemCreateDto(productId, quantity)) })
    }

    suspend fun submitOrder(orderId: Int): Flow<NetworkResult<OrderDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { api.submitOrder(orderId) })
    }

    suspend fun receiveOrder(orderId: Int): Flow<NetworkResult<OrderDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { api.receiveOrder(orderId) })
    }

    suspend fun cancelOrder(orderId: Int): Flow<NetworkResult<OrderDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { api.cancelOrder(orderId) })
    }
}
