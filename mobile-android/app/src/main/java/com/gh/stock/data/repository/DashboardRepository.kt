package com.gh.stock.data.repository

import com.gh.stock.data.remote.ApiClient
import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.data.remote.models.ManagerDashboardDto
import com.gh.stock.util.safeApiCall
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class DashboardRepository {

    suspend fun getManagerDashboard(): Flow<NetworkResult<ManagerDashboardDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { ApiClient.dashboardService.getManagerDashboard() })
    }
}
