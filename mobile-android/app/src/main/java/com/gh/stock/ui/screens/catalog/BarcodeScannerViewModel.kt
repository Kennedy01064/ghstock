package com.gh.stock.ui.screens.catalog

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.data.remote.models.ProductDto
import com.gh.stock.data.repository.CatalogRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed class BarcodeScannerUiState {
    object Idle : BarcodeScannerUiState()
    object Loading : BarcodeScannerUiState()
    data class Success(val product: ProductDto) : BarcodeScannerUiState()
    data class Error(val message: String) : BarcodeScannerUiState()
}

class BarcodeScannerViewModel(
    private val repository: CatalogRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<BarcodeScannerUiState>(BarcodeScannerUiState.Idle)
    val uiState: StateFlow<BarcodeScannerUiState> = _uiState.asStateFlow()

    private var isProcessing = false

    fun onBarcodeDetected(barcode: String) {
        if (isProcessing) return
        
        viewModelScope.launch {
            isProcessing = true
            _uiState.value = BarcodeScannerUiState.Loading
            
            repository.getProductByBarcode(barcode).collect { result ->
                when (result) {
                    is NetworkResult.Success -> {
                        _uiState.value = BarcodeScannerUiState.Success(result.data!!)
                    }
                    is NetworkResult.Error -> {
                        _uiState.value = BarcodeScannerUiState.Error(result.message ?: "Producto no encontrado")
                        // Permitir reintentar después de un tiempo
                        kotlinx.coroutines.delay(2000)
                        isProcessing = false
                        _uiState.value = BarcodeScannerUiState.Idle
                    }
                    is NetworkResult.Loading -> {
                        _uiState.value = BarcodeScannerUiState.Loading
                    }
                }
            }
        }
    }

    fun resetState() {
        isProcessing = false
        _uiState.value = BarcodeScannerUiState.Idle
    }
}
