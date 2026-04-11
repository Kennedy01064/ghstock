package com.gh.stock.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.gh.stock.ui.screens.dashboard.DashboardScreen
import com.gh.stock.ui.screens.login.LoginScreen

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
                        // Limpiar el back-stack para que el usuario no pueda
                        // volver al Login con el boton de atras
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
                onNavigateToInventory = { buildingId ->
                    navController.navigate(Screen.Inventory.createRoute(buildingId))
                },
                onLogout = {
                    navController.navigate(Screen.Login.route) {
                        popUpTo(Screen.Dashboard.route) { inclusive = true }
                    }
                }
            )
        }

        // Pantallas futuras — se implementan en Fases 4 y 5
        composable(Screen.Catalog.route) {
            // CatalogScreen — Fase 4
        }

        composable(
            route = Screen.ProductDetail.route,
            arguments = listOf(navArgument("productId") { type = NavType.IntType })
        ) { backStackEntry ->
            val productId = backStackEntry.arguments?.getInt("productId") ?: return@composable
            // ProductDetailScreen(productId) — Fase 4
        }

        composable(
            route = Screen.Inventory.route,
            arguments = listOf(navArgument("buildingId") { type = NavType.IntType })
        ) { backStackEntry ->
            val buildingId = backStackEntry.arguments?.getInt("buildingId") ?: return@composable
            // InventoryScreen(buildingId) — Fase 5
        }

        composable(
            route = Screen.AdjustStock.route,
            arguments = listOf(
                navArgument("buildingId") { type = NavType.IntType },
                navArgument("productId") { type = NavType.IntType }
            )
        ) { backStackEntry ->
            val buildingId = backStackEntry.arguments?.getInt("buildingId") ?: return@composable
            val productId = backStackEntry.arguments?.getInt("productId") ?: return@composable
            // AdjustStockSheet(buildingId, productId) — Fase 5
        }
    }
}
