package com.gh.stock

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import com.gh.stock.ui.screens.dashboard.DashboardScreen
import com.gh.stock.ui.screens.login.LoginScreen
import com.gh.stock.ui.theme.StockTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            StockTheme {
                var currentScreen by remember { mutableStateOf("login") }

                when (currentScreen) {
                    "login" -> LoginScreen(onLoginSuccess = { currentScreen = "dashboard" })
                    "dashboard" -> DashboardScreen()
                }
            }
        }
    }
}
