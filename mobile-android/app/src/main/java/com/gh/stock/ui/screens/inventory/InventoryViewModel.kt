package com.gh.stock.ui.screens.inventory

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.gh.stock.data.remote.models.InventoryItemDto
import com.gh.stock.data.remote.models.StockAdjustmentDto
import com.gh.stock.data.repository.InventoryRepository
import com.gh.stock.data.remote.NetworkResult
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

sealed class InventoryUiState {
    object Loading : InventoryUiState()
    data class Success(val items: List<InventoryItemDto>) : InventoryUiState()
    data class Error(val message: String) : InventoryUiState()
}

class InventoryViewModel(
    private val repository: InventoryRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<InventoryUiState>(InventoryUiState.Loading)
    val uiState: StateFlow<InventoryUiState> = _uiState.asStateFlow()

    private val _adjustmentState = MutableStateFlow<NetworkResult<Unit>?>(null)
    val adjustmentState: StateFlow<NetworkResult<Unit>?> = _adjustmentState.asStateFlow()

    private var currentBuildingId: Int? = null
    private val _searchQuery = MutableStateFlow("")

    fun loadInventory(buildingId: Int) {
        currentBuildingId = buildingId
        observeInventory()
    }

    fun onSearchQueryChanged(query: String) {
        _searchQuery.value = query
    }

    private fun observeInventory() {
        val buildingId = currentBuildingId ?: return
        
        _searchQuery
            .debounce(300)
            .flatMapLatest { query ->
                repository.getInventory(buildingId, query.ifBlank { null })
            }
            .onEach { result ->
                when (result) {
                    is NetworkResult.Loading<*> -> _uiState.value = InventoryUiState.Loading
                    is NetworkResult.Success<*> -> _uiState.value = InventoryUiState.Success(result.data!!)
                    is NetworkResult.Error<*> -> _uiState.value = InventoryUiState.Error(result.message ?: "Error desconocido")
                }
            }
            .launchIn(viewModelScope)
    }

    fun adjustStock(
        productId: Int,
        quantityChange: Double,
        reason: String,
        type: String
    ) {
        val buildingId = currentBuildingId ?: return

        viewModelScope.launch {
            _adjustmentState.value = NetworkResult.Loading()
            val result = repository.adjustStock(
                StockAdjustmentDto(
                    buildingId = buildingId,
                    productId = productId,
                    quantityChange = quantityChange,
                    reason = reason,
                    type = type
                )
            )
            _adjustmentState.value = result
            
            if (result is NetworkResult.Success<*>) {
                // Refresh list
                observeInventory()
            }
        }
    }

    fun clearAdjustmentState() {
        _adjustmentState.value = null
    }
}
