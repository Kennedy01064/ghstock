package com.gh.stock.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.gh.stock.ui.screens.catalog.CatalogScreen
import com.gh.stock.ui.screens.catalog.ProductDetailScreen
import com.gh.stock.ui.screens.dashboard.DashboardScreen
import com.gh.stock.ui.screens.inventory.InventoryScreen
import com.gh.stock.ui.screens.login.LoginScreen
import com.gh.stock.ui.screens.orders.OrderDetailScreen
import com.gh.stock.ui.screens.orders.OrdersListScreen
import com.gh.stock.ui.screens.reports.ReportsContainerScreen
import com.gh.stock.ui.screens.catalog.BarcodeScannerScreen

@Composable
fun NavGraph(
    navController: NavHostController,
    startDestination: String
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {

        composable(Screen.Login.route) {
            LoginScreen(
                onLoginSuccess = {
                    navController.navigate(Screen.Dashboard.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.Dashboard.route) {
            DashboardScreen(
                onNavigateToCatalog = {
                    navController.navigate(Screen.Catalog.route)
                },
                onNavigateToInventory = { id, name ->
                    navController.navigate(Screen.Inventory.createRoute(id, name))
                },
                onNavigateToOrders = {
                    navController.navigate(Screen.OrdersList.route)
                },
                onNavigateToReports = {
                    navController.navigate(Screen.Reports.route)
                },
                onLogout = {
                    navController.navigate(Screen.Login.route) {
                        popUpTo(Screen.Dashboard.route) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.Catalog.route) {
            CatalogScreen(
                onNavigateBack = { navController.popBackStack() },
                onNavigateToProduct = { productId ->
                    navController.navigate(Screen.ProductDetail.createRoute(productId) + "?fromCatalog=true")
                },
                onNavigateToScanner = {
                    navController.navigate(Screen.BarcodeScanner.route)
                }
            )
        }

        composable(Screen.BarcodeScanner.route) {
            BarcodeScannerScreen(
                onNavigateBack = { navController.popBackStack() },
                onProductFound = { productId ->
                    navController.navigate(Screen.ProductDetail.createRoute(productId) + "?fromCatalog=true") {
                        popUpTo(Screen.BarcodeScanner.route) { inclusive = true }
                    }
                }
            )
        }

        composable(
            route = Screen.ProductDetail.route + "?fromCatalog={fromCatalog}",
            arguments = listOf(
                navArgument("productId") { type = NavType.IntType },
                navArgument("fromCatalog") { type = NavType.BoolType; defaultValue = false }
            )
        ) { backStackEntry ->
            val productId = backStackEntry.arguments?.getInt("productId") ?: return@composable
            ProductDetailScreen(
                productId = productId,
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable(
            route = Screen.Inventory.route,
            arguments = listOf(
                navArgument("buildingId") { type = NavType.IntType },
                navArgument("buildingName") { type = NavType.StringType }
            )
        ) { backStackEntry ->
            val buildingId = backStackEntry.arguments?.getInt("buildingId") ?: return@composable
            val buildingName = backStackEntry.arguments?.getString("buildingName") ?: ""
            InventoryScreen(
                buildingId = buildingId,
                buildingName = buildingName,
                onBack = { navController.popBackStack() }
            )
        }

        composable(Screen.OrdersList.route) {
            OrdersListScreen(
                onNavigateBack = { navController.popBackStack() },
                onNavigateToOrderDetail = { id ->
                    navController.navigate(Screen.OrderDetail.createRoute(id))
                }
            )
        }

        composable(
            route = Screen.OrderDetail.route,
            arguments = listOf(navArgument("orderId") { type = NavType.IntType })
        ) { backStackEntry ->
            val orderId = backStackEntry.arguments?.getInt("orderId") ?: 0
            OrderDetailScreen(
                orderId = orderId,
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable(Screen.Reports.route) {
            ReportsContainerScreen(
                onBack = { navController.popBackStack() }
            )
        }
    }
}
