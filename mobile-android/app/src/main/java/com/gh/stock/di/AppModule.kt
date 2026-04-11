package com.gh.stock.di

import com.gh.stock.data.remote.ApiClient
import com.gh.stock.data.repository.NotificationRepository
import com.gh.stock.ui.screens.dashboard.DashboardViewModel
import org.koin.androidx.viewmodel.dsl.viewModel
import org.koin.dsl.module

val appModule = module {

    // --- API Services ---
    single { ApiClient.authService }
    single { ApiClient.catalogService }
    single { ApiClient.operationsService }

    // --- Repositories ---
    single { NotificationRepository() }

    // --- ViewModels ---
    viewModel { DashboardViewModel(get()) }
}
