package com.gh.stock.ui.screens.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.data.remote.models.OrderSubmissionDeadlineSettingDto
import com.gh.stock.data.repository.AuthRepository
import com.gh.stock.data.repository.NotificationRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class DashboardUiState(
    val deadline: OrderSubmissionDeadlineSettingDto? = null,
    val showDeadlineAlert: Boolean = false,
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)

class DashboardViewModel(
    private val notificationRepository: NotificationRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _uiState.asStateFlow()

    init {
        refreshDashboard()
    }

    fun refreshDashboard() {
        viewModelScope.launch {
            notificationRepository.getActiveDeadline().collect { result ->
                when (result) {
                    is NetworkResult.Loading -> _uiState.value = _uiState.value.copy(isLoading = true)
                    is NetworkResult.Success -> checkTaskCompletion(result.data)
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

    private suspend fun checkTaskCompletion(deadline: OrderSubmissionDeadlineSettingDto?) {
        notificationRepository.isTaskPending().collect { isPending ->
            _uiState.value = _uiState.value.copy(
                deadline = deadline,
                showDeadlineAlert = deadline?.order_submission_deadline_at != null && isPending,
                isLoading = false
            )
        }
    }
}
