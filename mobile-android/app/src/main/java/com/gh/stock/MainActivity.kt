package com.gh.stock

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.*
import androidx.navigation.compose.rememberNavController
import com.gh.stock.data.local.TokenDataStore
import com.gh.stock.data.remote.SessionManager
import com.gh.stock.data.repository.AuthRepository
import com.gh.stock.ui.theme.*
import com.gh.stock.ui.navigation.*
import androidx.compose.ui.graphics.Color
import com.gh.stock.util.ConnectivityObserver
import androidx.compose.animation.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.runBlocking
import org.koin.android.ext.android.inject

class MainActivity : ComponentActivity() {

    private val authRepository: AuthRepository by inject()
    private val connectivityObserver: ConnectivityObserver by inject()

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)

        val hasSession = runBlocking { authRepository.hasSession() }

        setContent {
            StockTheme {
                val navController = rememberNavController()
                val status by connectivityObserver.observe().collectAsState(initial = ConnectivityObserver.Status.Available)

                Box(modifier = Modifier.fillMaxSize()) {
                    Column {
                        // Banner de Conectividad (Solo si no hay internet)
                        AnimatedVisibility(
                            visible = status != ConnectivityObserver.Status.Available,
                            enter = expandVertically() + fadeIn(),
                            exit = shrinkVertically() + fadeOut()
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .background(ErrorRed)
                                    .padding(vertical = 4.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = "SIN CONEXIÓN A INTERNET",
                                    color = Color.White,
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }

                        Box(modifier = Modifier.weight(1f)) {
                            NavGraph(
                                navController = navController,
                                startDestination = if (hasSession) Screen.Dashboard.route else Screen.Login.route
                            )
                        }
                    }
                }

                // Redirigir a Login cuando la sesion expira (token 401)
                LaunchedEffect(Unit) {
                    SessionManager.sessionExpiredFlow.onEach {
                        navController.navigate(Screen.Login.route) {
                            popUpTo(0) { inclusive = true }
                        }
                    }.launchIn(this)
                }
            }
        }
    }
}
