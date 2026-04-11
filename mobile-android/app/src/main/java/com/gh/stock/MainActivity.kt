package com.gh.stock

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import androidx.navigation.compose.rememberNavController
import com.gh.stock.data.local.TokenDataStore
import com.gh.stock.data.remote.SessionManager
import com.gh.stock.data.repository.AuthRepository
import com.gh.stock.ui.navigation.NavGraph
import com.gh.stock.ui.navigation.Screen
import com.gh.stock.ui.theme.StockTheme
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.runBlocking
import org.koin.android.ext.android.inject

class MainActivity : ComponentActivity() {

    private val authRepository: AuthRepository by inject()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val hasSession = runBlocking { authRepository.hasSession() }

        setContent {
            StockTheme {
                val navController = rememberNavController()

                // Redirigir a Login cuando la sesion expira (token 401)
                LaunchedEffect(Unit) {
                    SessionManager.sessionExpiredFlow.onEach {
                        navController.navigate(Screen.Login.route) {
                            popUpTo(0) { inclusive = true }
                        }
                    }.launchIn(this)
                }

                NavGraph(
                    navController = navController,
                    startDestination = if (hasSession) Screen.Dashboard.route else Screen.Login.route
                )
            }
        }
    }
}
