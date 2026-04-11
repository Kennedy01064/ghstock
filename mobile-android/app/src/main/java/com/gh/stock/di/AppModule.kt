package com.gh.stock.di

import com.gh.stock.data.local.TokenDataStore
import com.gh.stock.data.remote.ApiClient
import com.gh.stock.data.repository.AuthRepository
import com.gh.stock.data.repository.NotificationRepository
import com.gh.stock.ui.screens.dashboard.DashboardViewModel
import com.gh.stock.ui.screens.login.LoginViewModel
import org.koin.android.ext.koin.androidContext
import org.koin.androidx.viewmodel.dsl.viewModel
import org.koin.dsl.module

val appModule = module {

    // --- Local storage ---
    single { TokenDataStore(androidContext()) }

    // --- API Services ---
    single { ApiClient.authService }
    single { ApiClient.catalogService }
    single { ApiClient.operationsService }

    // --- Repositories ---
    single { AuthRepository(get()) }
    single { NotificationRepository() }

    // --- ViewModels ---
    viewModel { LoginViewModel(get()) }
    viewModel { DashboardViewModel(get(), get()) }
}
