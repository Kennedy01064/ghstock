package com.gh.stock.ui.screens.orders

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest
import androidx.compose.ui.platform.LocalContext
import com.gh.stock.data.remote.models.OrderItemDto
import com.gh.stock.ui.components.GlassCard
import com.gh.stock.ui.components.OrderSkeleton
import com.gh.stock.ui.theme.*
import org.koin.androidx.compose.koinViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OrderDetailScreen(
    orderId: Int,
    onNavigateBack: () -> Unit,
    viewModel: OrdersViewModel = koinViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val order = uiState.selectedOrder

    LaunchedEffect(orderId) {
        viewModel.loadOrderDetails(orderId)
    }

    Scaffold(
        topBar = {
            Surface(
                color = NavySurface,
                shadowElevation = 8.dp
            ) {
                TopAppBar(
                    title = {
                        Text(
                            "Detalle de Pedido #${orderId}",
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
            }
        },
        containerColor = NavyBackground,
        bottomBar = {
            if (order?.status == "dispatched") {
                Surface(
                    color = NavySurface,
                    modifier = Modifier.navigationBarsPadding(),
                    shadowElevation = 16.dp
                ) {
                    Button(
                        onClick = { viewModel.receiveOrder(orderId) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp)
                            .height(56.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = AmberAccent),
                        shape = RoundedCornerShape(16.dp),
                        enabled = !uiState.isActionLoading
                    ) {
                        if (uiState.isActionLoading) {
                            CircularProgressIndicator(modifier = Modifier.size(24.dp), color = NavyPrimary)
                        } else {
                            Icon(Icons.Default.CheckCircle, contentDescription = null)
                            Spacer(Modifier.width(8.dp))
                            Text("CONFIRMAR RECEPCIÓN", fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
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
            if (uiState.isLoading) {
                Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
                    OrderSkeleton()
                }
            } else if (order != null) {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // Order Header Info
                    item {
                        OrderHeaderCard(order = order)
                    }

                    item {
                        Text(
                            text = "Productos en el Pedido",
                            color = TextPrimary,
                            fontWeight = FontWeight.Bold,
                            fontSize = 18.sp,
                            modifier = Modifier.padding(top = 8.dp)
                        )
                    }

                    items(order.items) { item ->
                        OrderItemRow(item = item)
                    }

                    if (order.rejectionNote != null) {
                        item {
                            RejectionNoteCard(note = order.rejectionNote!!)
                        }
                    }

                    item { Spacer(Modifier.height(80.dp)) }
                }
            }

            // Success Message Overlay
            if (uiState.successMessage != null) {
                AlertDialog(
                    onDismissRequest = { viewModel.clearMessages() },
                    confirmButton = {
                        TextButton(onClick = { viewModel.clearMessages(); onNavigateBack() }) {
                            Text("ACEPTAR", color = AmberAccent)
                        }
                    },
                    title = { Text("¡Éxito!", color = TextPrimary) },
                    text = { Text(uiState.successMessage!!, color = TextSecondary) },
                    containerColor = NavySurface,
                    shape = RoundedCornerShape(24.dp)
                )
            }
        }
    }
}

@Composable
fun OrderHeaderCard(order: com.gh.stock.data.remote.models.OrderDto) {
    GlassCard(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Home, contentDescription = null, tint = AmberAccent, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(8.dp))
                Text(order.building?.name ?: "Sede", color = TextPrimary, fontWeight = FontWeight.Bold)
                Spacer(Modifier.weight(1f))
                StatusBadge(status = order.status)
            }
            
            HorizontalDivider(color = Color.White.copy(alpha = 0.1f), modifier = Modifier.padding(vertical = 12.dp))
            
            InfoRow(label = "Fecha de Creación", value = order.createdAt?.split("T")?.get(0) ?: "N/A")
            InfoRow(label = "Solicitado por", value = "Admin Sede") // Podría venir del DTO si se expande
            InfoRow(label = "Items Totales", value = order.items.size.toString())
        }
    }
}

@Composable
fun OrderItemRow(item: OrderItemDto) {
    GlassCard(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Product Image
            AsyncImage(
                model = ImageRequest.Builder(LocalContext.current)
                    .data(item.product?.imageUrl ?: "https://via.placeholder.com/150")
                    .crossfade(true)
                    .build(),
                contentDescription = null,
                modifier = Modifier
                    .size(56.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(Color.White.copy(alpha = 0.05f)),
                contentScale = ContentScale.Crop
            )

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = item.productNameSnapshot ?: item.product?.name ?: "Producto",
                    color = TextPrimary,
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp
                )
                Text(
                    text = "SKU: ${item.product?.sku ?: "N/A"}",
                    color = TextMuted,
                    fontSize = 11.sp
                )
            }

            Column(horizontalAlignment = Alignment.End) {
                Text(
                    text = "${item.quantity}",
                    color = AmberAccent,
                    fontWeight = FontWeight.Black,
                    fontSize = 18.sp
                )
                Text(
                    text = item.product?.unitName ?: "unid.",
                    color = TextMuted,
                    fontSize = 11.sp
                )
            }
        }
    }
}

@Composable
fun RejectionNoteCard(note: String) {
    GlassCard(
        modifier = Modifier.fillMaxWidth(),
        cornerRadius = 16.dp
    ) {
        Column(
            modifier = Modifier
                .background(ErrorRed.copy(alpha = 0.1f))
                .padding(16.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Info, contentDescription = null, tint = ErrorRed, modifier = Modifier.size(20.dp))
                Spacer(Modifier.width(12.dp))
                Text("Nota de Rechazo", color = ErrorRed, fontWeight = FontWeight.Bold, fontSize = 14.sp)
            }
            Spacer(Modifier.height(8.dp))
            Text(note, color = TextPrimary, fontSize = 14.sp, lineHeight = 20.sp)
        }
    }
}

@Composable
fun InfoRow(label: String, value: String) {
    Row(modifier = Modifier.padding(vertical = 2.dp), verticalAlignment = Alignment.CenterVertically) {
        Text(label, color = TextMuted, fontSize = 12.sp, modifier = Modifier.width(120.dp))
        Text(value, color = TextSecondary, fontSize = 12.sp)
    }
}
