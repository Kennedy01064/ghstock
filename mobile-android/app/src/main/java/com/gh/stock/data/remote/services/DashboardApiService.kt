package com.gh.stock.data.remote.services

import com.gh.stock.data.remote.models.ManagerDashboardDto
import retrofit2.Response
import retrofit2.http.GET

interface DashboardApiService {

    @GET("dashboard/manager")
    suspend fun getManagerDashboard(): Response<ManagerDashboardDto>
}
