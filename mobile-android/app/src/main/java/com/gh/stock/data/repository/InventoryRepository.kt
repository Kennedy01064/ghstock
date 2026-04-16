package com.gh.stock.data.repository

import com.gh.stock.data.remote.models.*
import com.gh.stock.data.remote.services.OperationsApiService
import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.util.safeApiCall
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class InventoryRepository(private val apiService: OperationsApiService) {

    fun getInventory(buildingId: Int, search: String? = null): Flow<NetworkResult<List<InventoryItemDto>>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { apiService.getInventoryByBuilding(buildingId, search) })
    }

    suspend fun adjustStock(adjustment: StockAdjustmentDto): NetworkResult<Unit> {
        return safeApiCall { 
            apiService.adjustStock(
                AdjustStockRequest(
                    buildingId = adjustment.buildingId,
                    productId = adjustment.productId,
                    quantityChange = adjustment.quantityChange,
                    reason = adjustment.reason,
                    type = adjustment.type
                )
            )
        }
    }

    fun getMovements(buildingId: Int, productId: Int? = null): Flow<NetworkResult<List<InventoryMovementDto>>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { apiService.getInventoryHistory(buildingId = buildingId, productId = productId) })
    }
}
