package com.gh.stock.ui.screens.reports

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.gh.stock.data.remote.models.AnalyticsReportDto
import com.gh.stock.data.remote.models.InventoryMovementDto
import com.gh.stock.data.repository.ReportsRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.util.Calendar

data class ReportsState(
    val isLoading: Boolean = false,
    val movements: List<InventoryMovementDto> = emptyList(),
    val analytics: AnalyticsReportDto? = null,
    val selectedMonth: Int = Calendar.getInstance().get(Calendar.MONTH) + 1,
    val selectedYear: Int = Calendar.getInstance().get(Calendar.YEAR),
    val selectedBuildingId: Int? = null,
    val errorMessage: String? = null
)

class ReportsViewModel(
    private val repository: ReportsRepository
) : ViewModel() {

    private val _state = MutableStateFlow(ReportsState())
    val state: StateFlow<ReportsState> = _state.asStateFlow()

    init {
        loadData()
    }

    fun loadData() {
        _state.update { it.copy(isLoading = true, errorMessage = null) }
        viewModelScope.launch {
            val currentState = _state.value
            
            // Cargar Historial
            repository.getMovementHistory(
                buildingId = currentState.selectedBuildingId,
                month = currentState.selectedMonth,
                year = currentState.selectedYear
            ).collect { result ->
                result.onSuccess { movements ->
                    _state.update { it.copy(movements = movements) }
                }.onFailure { e ->
                    _state.update { it.copy(errorMessage = "Error al cargar historial: ${e.message}") }
                }
            }

            // Cargar Analíticas
            val analyticsResult = repository.getAnalyticsReport(
                month = currentState.selectedMonth,
                year = currentState.selectedYear
            )
            analyticsResult.onSuccess { analytics ->
                _state.update { it.copy(analytics = analytics, isLoading = false) }
            }.onFailure { e ->
                _state.update { it.copy(errorMessage = "Error al cargar reportes: ${e.message}", isLoading = false) }
            }
        }
    }

    fun onMonthSelected(month: Int) {
        _state.update { it.copy(selectedMonth = month) }
        loadData()
    }

    fun onYearSelected(year: Int) {
        _state.update { it.copy(selectedYear = year) }
        loadData()
    }

    fun onBuildingSelected(buildingId: Int?) {
        _state.update { it.copy(selectedBuildingId = buildingId) }
        loadData()
    }

    suspend fun getExportUrl(): String {
        val state = _state.value
        return repository.getInventoryPdfUrl(
            month = state.selectedMonth,
            year = state.selectedYear,
            buildingId = state.selectedBuildingId
        )
    }
}
