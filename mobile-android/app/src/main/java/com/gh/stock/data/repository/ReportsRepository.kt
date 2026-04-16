package com.gh.stock.data.repository

import com.gh.stock.data.remote.models.AnalyticsReportDto
import com.gh.stock.data.remote.models.InventoryMovementDto
import com.gh.stock.data.remote.services.DashboardApiService
import com.gh.stock.data.remote.services.OperationsApiService
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import android.util.Log

class ReportsRepository(
    private val operationsApi: OperationsApiService,
    private val dashboardApi: DashboardApiService
) {
    /**
     * Obtiene el historial de movimientos filtrado por mes y año.
     */
    fun getMovementHistory(
        buildingId: Int? = null,
        productId: Int? = null,
        movementType: String? = null,
        month: Int? = null,
        year: Int? = null
    ): Flow<Result<List<InventoryMovementDto>>> = flow {
        try {
            val response = operationsApi.getInventoryHistory(
                buildingId = buildingId,
                productId = productId,
                movementType = movementType,
                month = month,
                year = year
            )
            if (response.isSuccessful && response.body() != null) {
                emit(Result.success(response.body()!!))
            } else {
                emit(Result.failure(Exception("Error de red: ${response.code()}")))
            }
        } catch (e: Exception) {
            Log.e("ReportsRepository", "Error fetching movement history", e)
            emit(Result.failure(e))
        }
    }

    /**
     * Obtiene las analíticas detalladas para el dashboard de reportes.
     */
    suspend fun getAnalyticsReport(
        month: Int? = null,
        year: Int? = null
    ): Result<AnalyticsReportDto> {
        return try {
            val response = dashboardApi.getManagerDashboard()
            if (response.isSuccessful && response.body() != null) {
                // NOTA: ManagerDashboardDto y AnalyticsReportDto son diferentes. 
                // Devolvemos error controlado indicando que este reporte detallado no est disponible
                // va el endpoint del dashboard general.
                Result.failure(Exception("Endpoint de analtica detallada no disponible"))
            } else {
                Result.failure(Exception("Error en respuesta del servidor: ${response.code()}"))
            }
        } catch (e: Exception) {
            Log.e("ReportsRepository", "Error fetching analytics report", e)
            Result.failure(e)
        }
    }

    /**
     * Genera la URL para descargar el PDF de inventario.
     */
    fun getInventoryPdfUrl(month: Int, year: Int, buildingId: Int?): String {
        val baseUrl = "https://ghstock-production.up.railway.app/api/v1/reporting/inventory-pdf"
        val params = mutableListOf("month=$month", "year=$year")
        buildingId?.let { params.add("building_id=$it") }
        
        // El backend requiere autenticación. En una app real usaríamos un downloader que pase headers
        // o un token temporal en la URL. Usaremos la URL base para ahora.
        return "$baseUrl?${params.joinToString("&")}"
    }
}
