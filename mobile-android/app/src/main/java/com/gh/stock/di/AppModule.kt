package com.gh.stock.di

import com.gh.stock.data.local.TokenDataStore
import com.gh.stock.data.remote.ApiClient
import com.gh.stock.data.repository.*
import com.gh.stock.ui.screens.catalog.CatalogViewModel
import com.gh.stock.ui.screens.catalog.ProductDetailViewModel
import com.gh.stock.ui.screens.catalog.BarcodeScannerViewModel
import com.gh.stock.ui.screens.dashboard.DashboardViewModel
import com.gh.stock.ui.screens.inventory.InventoryViewModel
import com.gh.stock.ui.screens.login.LoginViewModel
import com.gh.stock.ui.screens.orders.OrdersViewModel
import com.gh.stock.ui.screens.reports.ReportsViewModel
import com.gh.stock.util.ConnectivityObserver
import com.gh.stock.util.NetworkConnectivityObserver
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
    single { ApiClient.ordersService }

    // --- Repositories ---
    single { AuthRepository(get()) }
    single { DashboardRepository() }
    single<ConnectivityObserver> { NetworkConnectivityObserver(get()) }
    single { CatalogRepository() }
    single { NotificationRepository() }
    single { InventoryRepository(get()) }
    single { OrdersRepository(get()) }
    single { ReportsRepository(get(), get()) }

    // --- ViewModels ---
    viewModel { LoginViewModel(get()) }
    viewModel { DashboardViewModel(get(), get()) }
    viewModel { CatalogViewModel(get()) }
    viewModel { ProductDetailViewModel(get()) }
    viewModel { InventoryViewModel(get()) }
    viewModel { OrdersViewModel(get()) }
    viewModel { ReportsViewModel(get()) }
    viewModel { BarcodeScannerViewModel(get()) }
}
