package com.gh.stock.data.repository

import com.gh.stock.data.remote.ApiClient
import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.data.remote.models.OrderSubmissionDeadlineSettingDto
import com.gh.stock.util.safeApiCall
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class NotificationRepository {

    private val api = ApiClient.operationsService

    suspend fun getActiveDeadline(): Flow<NetworkResult<OrderSubmissionDeadlineSettingDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { api.getOrderDeadline() })
    }

    suspend fun isTaskPending(): Flow<Boolean> = flow {
        val response = api.getPendingStatus()
        if (response.isSuccessful) {
            emit(response.body()?.has_pending_orders ?: false)
        } else {
            emit(false)
        }
    }
}
