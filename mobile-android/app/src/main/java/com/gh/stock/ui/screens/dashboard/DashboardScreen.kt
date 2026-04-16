package com.gh.stock.ui.screens.dashboard

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.ui.screens.dashboard.components.BuildingCard
import com.gh.stock.ui.screens.dashboard.components.DeadlineBanner
import com.gh.stock.ui.screens.dashboard.components.StatsSummaryCard
import com.gh.stock.ui.components.MetricSkeleton
import com.gh.stock.ui.components.ProductSkeleton
import com.gh.stock.ui.theme.*
import org.koin.androidx.compose.koinViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(
    onNavigateToCatalog: () -> Unit = {},
    onNavigateToInventory: (buildingId: Int, buildingName: String) -> Unit = { _, _ -> },
    onNavigateToOrders: () -> Unit = {},
    onNavigateToReports: () -> Unit = {},
    onLogout: () -> Unit = {},
    viewModel: DashboardViewModel = koinViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            Surface(
                color = NavySurface,
                shadowElevation = 8.dp
            ) {
                TopAppBar(
                    title = {
                        Column {
                            Text(
                                "Stock GH",
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary,
                                fontSize = 20.sp
                            )
                            Text(
                                "Panel de Control",
                                fontSize = 11.sp,
                                color = AmberAccent,
                                fontWeight = FontWeight.Medium,
                                letterSpacing = 1.sp
                            )
                        }
                    },
                    actions = {
                        IconButton(onClick = onNavigateToOrders) {
                            Icon(
                                imageVector = Icons.Default.List,
                                contentDescription = "Pedidos",
                                tint = AmberAccent
                            )
                        }
                        IconButton(onClick = onNavigateToReports) {
                            Icon(
                                imageVector = Icons.Default.Star,
                                contentDescription = "Reportes",
                                tint = AmberAccent
                            )
                        }
                        IconButton(onClick = onNavigateToCatalog) {
                            Icon(
                                imageVector = Icons.Default.ShoppingCart,
                                contentDescription = "Catalogo",
                                tint = AmberAccent
                            )
                        }
                        IconButton(onClick = {
                            viewModel.logout()
                            onLogout()
                        }) {
                            Icon(
                                imageVector = Icons.Default.ArrowForward,
                                contentDescription = "Cerrar sesion",
                                tint = TextSecondary
                            )
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = Color.Transparent
                    )
                )
            }
        },
        containerColor = NavyBackground
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(
                    Brush.verticalGradient(
                        colors = listOf(NavyBackground, NavyPrimary)
                    )
                )
        ) {
            Column(modifier = Modifier.fillMaxSize()) {
                if (uiState.showDeadlineAlert && uiState.deadline != null) {
                    DeadlineBanner(
                        deadlineAt = uiState.deadline?.deadlineAt ?: "",
                        note = uiState.deadline?.note
                    )
                }

                if (uiState.isLoading) {
                    Column(
                        modifier = Modifier.fillMaxSize().padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        MetricSkeleton()
                        Spacer(modifier = Modifier.height(16.dp))
                        repeat(3) {
                            ProductSkeleton() // Reuse as building skeleton
                        }
                    }
                } else {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        item {
                            StatsSummaryCard(
                                pedidosActivos = uiState.pedidosActivos,
                                pedidosEnTransito = uiState.pedidosEnTransito,
                                totalBuildings = uiState.buildings.size,
                                onClick = onNavigateToOrders
                            )
                        }

                        item {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "Mis Sedes Registradas",
                                fontSize = 18.sp,
                                fontWeight = FontWeight.Black,
                                color = TextPrimary,
                                letterSpacing = (-0.5).sp
                            )
                            Text(
                                text = "Selecciona una sede para gestionar inventario",
                                fontSize = 11.sp,
                                color = TextMuted
                            )
                        }

                        items(uiState.buildings) { building ->
                            BuildingCard(
                                building = building,
                                onNavigateToInventory = onNavigateToInventory
                            )
                        }
                    }
                }
            }
        }
    }
}
