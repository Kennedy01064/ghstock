package com.gh.stock.ui.navigation

sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Dashboard : Screen("dashboard")
    object Catalog : Screen("catalog")
    object ProductDetail : Screen("product/{productId}") {
        fun createRoute(productId: Int) = "product/$productId"
    }
    object Inventory : Screen("inventory/{buildingId}") {
        fun createRoute(buildingId: Int) = "inventory/$buildingId"
    }
    object AdjustStock : Screen("adjust/{buildingId}/{productId}") {
        fun createRoute(buildingId: Int, productId: Int) = "adjust/$buildingId/$productId"
    }
}
