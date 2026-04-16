package com.gh.stock.ui.navigation

sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Dashboard : Screen("dashboard")
    object Catalog : Screen("catalog")
    object ProductDetail : Screen("product/{productId}") {
        fun createRoute(productId: Int) = "product/$productId"
    }
    object Inventory : Screen("inventory/{buildingId}/{buildingName}") {
        fun createRoute(buildingId: Int, buildingName: String) = "inventory/$buildingId/$buildingName"
    }
    object AdjustStock : Screen("adjust/{buildingId}/{productId}") {
        fun createRoute(buildingId: Int, productId: Int) = "adjust/$buildingId/$productId"
    }
    object OrdersList : Screen("orders")
    object OrderDetail : Screen("orders/{orderId}") {
        fun createRoute(orderId: Int) = "orders/$orderId"
    }
    object Reports : Screen("reports")
    object BarcodeScanner : Screen("barcode_scanner")
}
