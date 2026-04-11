package com.gh.stock

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import androidx.lifecycle.lifecycleScope
import com.gh.stock.data.local.TokenDataStore
import com.gh.stock.data.remote.SessionManager
import com.gh.stock.ui.screens.dashboard.DashboardScreen
import com.gh.stock.ui.screens.login.LoginScreen
import com.gh.stock.ui.theme.StockTheme
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.runBlocking

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Check inicial de sesion (sincrono, rapido — solo lee DataStore)
        val hasSession = runBlocking {
            TokenDataStore(applicationContext).getAccessToken() != null
        }

        setContent {
            StockTheme {
                var currentScreen by remember {
                    mutableStateOf(if (hasSession) "dashboard" else "login")
                }

                // Observar sesion expirada → forzar regreso al Login
                LaunchedEffect(Unit) {
                    SessionManager.sessionExpiredFlow.onEach {
                        currentScreen = "login"
                    }.launchIn(this)
                }

                when (currentScreen) {
                    "login" -> LoginScreen(onLoginSuccess = { currentScreen = "dashboard" })
                    "dashboard" -> DashboardScreen()
                }
            }
        }
    }
}
