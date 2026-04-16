package com.gh.stock.ui.screens.orders

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.material3.TabRowDefaults.tabIndicatorOffset
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.data.remote.models.OrderDto
import com.gh.stock.ui.components.GlassCard
import com.gh.stock.ui.components.PremiumEmptyState
import com.gh.stock.ui.components.ProductSkeleton
import com.gh.stock.ui.theme.*
import androidx.compose.animation.Crossfade
import org.koin.androidx.compose.koinViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OrdersListScreen(
    onNavigateBack: () -> Unit,
    onNavigateToOrderDetail: (Int) -> Unit,
    viewModel: OrdersViewModel = koinViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    var selectedTab by remember { mutableStateOf(0) }
    val tabs = listOf("En Tránsito", "Pendientes", "Entregados")
    val statusMap = listOf("dispatched", "submitted", "delivered")

    LaunchedEffect(selectedTab) {
        viewModel.loadOrders(status = statusMap[selectedTab])
    }

    Scaffold(
        topBar = {
            Surface(
                color = NavySurface,
                shadowElevation = 8.dp
            ) {
                Column {
                    TopAppBar(
                        title = {
                            Text(
                                "Gestión de Pedidos",
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        },
                        navigationIcon = {
                            IconButton(onClick = onNavigateBack) {
                                Icon(Icons.Default.ArrowBack, contentDescription = "Volver", tint = AmberAccent)
                            }
                        },
                        colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
                    )
                    
                    ScrollableTabRow(
                        selectedTabIndex = selectedTab,
                        containerColor = Color.Transparent,
                        contentColor = AmberAccent,
                        indicator = { tabPositions ->
                            TabRowDefaults.Indicator(
                                modifier = Modifier.tabIndicatorOffset(tabPositions[selectedTab]),
                                color = AmberAccent
                            )
                        },
                        divider = {},
                        edgePadding = 16.dp
                    ) {
                        tabs.forEachIndexed { index, title ->
                            Tab(
                                selected = selectedTab == index,
                                onClick = { selectedTab = index },
                                text = {
                                    Text(
                                        title,
                                        fontSize = 13.sp,
                                        fontWeight = if (selectedTab == index) FontWeight.Bold else FontWeight.Normal
                                    )
                                }
                            )
                        }
                    }
                }
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
            Crossfade(
                targetState = uiState.isLoading,
                label = "orders_transition"
            ) { isLoading ->
                if (isLoading) {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        items(6) {
                            ProductSkeleton()
                        }
                    }
                } else if (uiState.orders.isEmpty()) {
                    PremiumEmptyState(
                        message = "No hay pedidos en esta categoría",
                        icon = Icons.Default.List
                    )
                } else {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        items(uiState.orders) { order ->
                            OrderCard(
                                order = order,
                                onClick = { onNavigateToOrderDetail(order.id) }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun OrderCard(order: OrderDto, onClick: () -> Unit) {
    GlassCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Icon Background
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .background(
                        color = when (order.status) {
                            "dispatched" -> AmberAccent.copy(alpha = 0.1f)
                            "submitted" -> Color.White.copy(alpha = 0.05f)
                            "delivered" -> Color.Green.copy(alpha = 0.1f)
                            else -> Color.White.copy(alpha = 0.05f)
                        },
                        shape = RoundedCornerShape(12.dp)
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = when (order.status) {
                        "dispatched" -> Icons.Default.ArrowForward
                        "delivered" -> Icons.Default.List
                        else -> Icons.Default.Info
                    },
                    contentDescription = null,
                    tint = when (order.status) {
                        "dispatched" -> AmberAccent
                        "delivered" -> Color.Green
                        else -> TextSecondary
                    },
                    modifier = Modifier.size(24.dp)
                )
            }

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "Pedido #${order.id}",
                    fontWeight = FontWeight.Bold,
                    color = TextPrimary,
                    fontSize = 16.sp
                )
                Text(
                    text = order.building?.name ?: "Sede no especificada",
                    color = TextSecondary,
                    fontSize = 12.sp
                )
                Text(
                    text = "${order.items.size} productos",
                    color = TextMuted,
                    fontSize = 11.sp
                )
            }

            Column(horizontalAlignment = Alignment.End) {
                StatusBadge(status = order.status)
                Spacer(modifier = Modifier.height(4.dp))
                // Formatear fecha simple (en producción se usaría un date formatter real)
                val date = order.createdAt?.split("T")?.get(0) ?: ""
                Text(text = date, color = TextMuted, fontSize = 10.sp)
            }
        }
    }
}

@Composable
fun StatusBadge(status: String) {
    val (text, color) = when (status) {
        "draft" -> "Borrador" to Color.Gray
        "submitted" -> "Pendiente" to AmberAccent
        "approved" -> "Aprobado" to Color.Cyan
        "processing" -> "En Almacén" to Color.Magenta
        "dispatched" -> "En Camino" to Color(0xFF3B82F6) // Bright Blue
        "delivered" -> "Entregado" to Color(0xFF10B981) // Emerald
        "cancelled" -> "Cancelado" to Color.Red
        "rejected" -> "Rechazado" to Color.Red
        else -> status to Color.Gray
    }

    Surface(
        color = color.copy(alpha = 0.12f),
        shape = RoundedCornerShape(4.dp),
        border = androidx.compose.foundation.BorderStroke(1.dp, color.copy(alpha = 0.3f))
    ) {
        Text(
            text = text.uppercase(),
            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
            fontSize = 9.sp,
            fontWeight = FontWeight.Bold,
            color = color,
            letterSpacing = 0.5.sp
        )
    }
}

