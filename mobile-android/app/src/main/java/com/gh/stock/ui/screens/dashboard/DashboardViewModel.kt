package com.gh.stock.ui.screens.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.data.remote.models.BuildingSummaryDto
import com.gh.stock.data.remote.models.ManagerDashboardDto
import com.gh.stock.data.remote.models.SubmissionDeadlineDto
import com.gh.stock.data.repository.AuthRepository
import com.gh.stock.data.repository.DashboardRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class DashboardUiState(
    val buildings: List<BuildingSummaryDto> = emptyList(),
    val pedidosActivos: Int = 0,
    val pedidosEnTransito: Int = 0,
    val deadline: SubmissionDeadlineDto? = null,
    val showDeadlineAlert: Boolean = false,
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)

class DashboardViewModel(
    private val dashboardRepository: DashboardRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _uiState.asStateFlow()

    init {
        refreshDashboard()
    }

    fun refreshDashboard() {
        viewModelScope.launch {
            dashboardRepository.getManagerDashboard().collect { result ->
                when (result) {
                    is NetworkResult.Loading -> _uiState.value = _uiState.value.copy(
                        isLoading = true,
                        errorMessage = null
                    )
                    is NetworkResult.Success -> {
                        val data: ManagerDashboardDto = result.data!!
                        val deadline = data.submissionDeadline
                        _uiState.value = _uiState.value.copy(
                            buildings = data.buildings,
                            pedidosActivos = data.pedidosActivos,
                            pedidosEnTransito = data.pedidosEnTransito,
                            deadline = deadline,
                            showDeadlineAlert = deadline != null &&
                                    deadline.deadlineAt != null &&
                                    deadline.pendingOrdersCount > 0,
                            isLoading = false
                        )
                    }
                    is NetworkResult.Error -> _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        errorMessage = result.message
                    )
                }
            }
        }
    }

    fun logout() {
        viewModelScope.launch {
            authRepository.logout()
        }
    }
}
