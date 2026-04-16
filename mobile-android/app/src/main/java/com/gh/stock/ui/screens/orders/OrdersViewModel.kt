package com.gh.stock.ui.screens.orders

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.data.remote.models.OrderDto
import com.gh.stock.data.repository.OrdersRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class OrdersUiState(
    val orders: List<OrderDto> = emptyList(),
    val filteredOrders: List<OrderDto> = emptyList(),
    val currentStatusTab: String? = null, // null means "All" or a default
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
    val selectedOrder: OrderDto? = null,
    val isActionLoading: Boolean = false,
    val successMessage: String? = null
)

class OrdersViewModel(
    private val ordersRepository: OrdersRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(OrdersUiState())
    val uiState: StateFlow<OrdersUiState> = _uiState.asStateFlow()

    fun loadOrders(status: String? = null, buildingId: Int? = null) {
        viewModelScope.launch {
            ordersRepository.getOrders(status, buildingId).collect { result ->
                when (result) {
                    is NetworkResult.Loading -> {
                        _uiState.value = _uiState.value.copy(isLoading = true, errorMessage = null)
                    }
                    is NetworkResult.Success -> {
                        val orders = result.data ?: emptyList()
                        _uiState.value = _uiState.value.copy(
                            isLoading = false,
                            orders = orders,
                            filteredOrders = orders,
                            currentStatusTab = status
                        )
                    }
                    is NetworkResult.Error -> {
                        _uiState.value = _uiState.value.copy(
                            isLoading = false,
                            errorMessage = result.message
                        )
                    }
                }
            }
        }
    }

    fun loadOrderDetails(orderId: Int) {
        viewModelScope.launch {
            ordersRepository.getOrderById(orderId).collect { result ->
                when (result) {
                    is NetworkResult.Loading -> {
                        _uiState.value = _uiState.value.copy(isLoading = true, errorMessage = null)
                    }
                    is NetworkResult.Success -> {
                        _uiState.value = _uiState.value.copy(
                            isLoading = false,
                            selectedOrder = result.data
                        )
                    }
                    is NetworkResult.Error -> {
                        _uiState.value = _uiState.value.copy(
                            isLoading = false,
                            errorMessage = result.message
                        )
                    }
                }
            }
        }
    }

    fun receiveOrder(orderId: Int) {
        viewModelScope.launch {
            ordersRepository.receiveOrder(orderId).collect { result ->
                when (result) {
                    is NetworkResult.Loading -> {
                        _uiState.value = _uiState.value.copy(isActionLoading = true)
                    }
                    is NetworkResult.Success -> {
                        _uiState.value = _uiState.value.copy(
                            isActionLoading = false,
                            successMessage = "Pedido recibido correctamente. El inventario ha sido actualizado."
                        )
                        // Refresh the list to reflect "Delivered" status
                        loadOrders(_uiState.value.currentStatusTab)
                    }
                    is NetworkResult.Error -> {
                        _uiState.value = _uiState.value.copy(
                            isActionLoading = false,
                            errorMessage = result.message
                        )
                    }
                }
            }
        }
    }

    fun clearMessages() {
        _uiState.value = _uiState.value.copy(errorMessage = null, successMessage = null)
    }
}
