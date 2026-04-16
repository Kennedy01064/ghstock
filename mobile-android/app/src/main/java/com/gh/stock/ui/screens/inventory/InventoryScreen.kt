package com.gh.stock.ui.screens.inventory

import androidx.compose.animation.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.gh.stock.data.remote.models.InventoryItemDto
import com.gh.stock.ui.components.GlassCard
import com.gh.stock.ui.components.InventorySkeleton
import com.gh.stock.ui.components.PremiumEmptyState
import com.gh.stock.ui.components.PremiumErrorState
import com.gh.stock.ui.screens.inventory.components.AdjustStockBottomSheet
import com.gh.stock.ui.theme.*
import org.koin.androidx.compose.koinViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun InventoryScreen(
    buildingId: Int,
    buildingName: String,
    onBack: () -> Unit,
    viewModel: InventoryViewModel = koinViewModel()
) {
    var searchQuery by remember { mutableStateOf("") }
    var selectedItem by remember { mutableStateOf<InventoryItemDto?>(null) }
    var showAdjustSheet by remember { mutableStateOf(false) }

    val uiState by viewModel.uiState.collectAsState()
    val adjustmentState by viewModel.adjustmentState.collectAsState()

    LaunchedEffect(buildingId) {
        viewModel.loadInventory(buildingId)
    }

    Scaffold(
        topBar = {
            InventoryTopBar(
                title = buildingName,
                onBack = onBack,
                searchQuery = searchQuery,
                onSearchChange = {
                    searchQuery = it
                    viewModel.onSearchQueryChanged(it)
                }
            )
        },
        containerColor = NavyBackground
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .imePadding() // Key for keyboard scroll stability
                .background(
                    Brush.verticalGradient(
                        colors = listOf(NavyBackground, NavyPrimary)
                    )
                )
        ) {
            Crossfade(targetState = uiState, label = "inventory_transition") { state ->
                when (state) {
                    is InventoryUiState.Loading -> {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(16.dp),
                            verticalArrangement = Arrangement.spacedBy(16.dp)
                        ) {
                            items(8) {
                                InventorySkeleton()
                            }
                        }
                    }
                    is InventoryUiState.Success -> {
                        if (state.items.isEmpty()) {
                            PremiumEmptyState(
                                message = "No hay insumos cargados en esta sede",
                                icon = Icons.Default.ShoppingCart
                            )
                        } else {
                            InventoryList(
                                items = state.items,
                                onItemClick = {
                                    selectedItem = it
                                    showAdjustSheet = true
                                }
                            )
                        }
                    }
                    is InventoryUiState.Error -> {
                        PremiumErrorState(
                            message = state.message,
                            onRetry = { viewModel.loadInventory(buildingId) }
                        )
                    }
                }
            }
        }
    }

    if (showAdjustSheet && selectedItem != null) {
        AdjustStockBottomSheet(
            item = selectedItem!!,
            onDismiss = { 
                showAdjustSheet = false 
                viewModel.clearAdjustmentState()
            },
            onConfirm = { change, reason, type ->
                viewModel.adjustStock(selectedItem!!.productId, change, reason, type)
            },
            adjustmentState = adjustmentState
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun InventoryTopBar(
    title: String,
    onBack: () -> Unit,
    searchQuery: String,
    onSearchChange: (String) -> Unit
) {
    Surface(
        color = NavySurface,
        tonalElevation = 8.dp,
        shadowElevation = 8.dp
    ) {
        Column(modifier = Modifier.padding(bottom = 12.dp)) {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            text = title,
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                        Text(
                            text = "Inventario de Sede",
                            fontSize = 12.sp,
                            color = AmberAccent,
                            fontWeight = FontWeight.Medium
                        )
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Volver", tint = TextPrimary)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
            
            // Premium Search Bar
            OutlinedTextField(
                value = searchQuery,
                onValueChange = onSearchChange,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
                    .height(56.dp),
                placeholder = { Text("Buscar en esta sede...", color = TextSecondary, fontSize = 14.sp) },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null, tint = AmberAccent) },
                trailingIcon = {
                    if (searchQuery.isNotEmpty()) {
                        IconButton(onClick = { onSearchChange("") }) {
                            Icon(Icons.Default.Close, contentDescription = "Limpiar", tint = TextMuted)
                        }
                    }
                },
                shape = RoundedCornerShape(28.dp),
                singleLine = true,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = NavySurface,
                    unfocusedContainerColor = NavyBackground.copy(alpha = 0.5f),
                    focusedBorderColor = AmberAccent,
                    unfocusedBorderColor = Color.White.copy(alpha = 0.1f),
                    focusedTextColor = TextPrimary,
                    unfocusedTextColor = TextPrimary,
                    cursorColor = AmberAccent
                )
            )
        }
    }
}

@Composable
fun InventoryList(
    items: List<InventoryItemDto>,
    onItemClick: (InventoryItemDto) -> Unit
) {
    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(items) { item ->
            InventoryItemCard(item = item, onClick = { onItemClick(item) })
        }
    }
}

@Composable
fun InventoryItemCard(
    item: InventoryItemDto,
    onClick: () -> Unit
) {
    val isCritical = item.currentStock <= item.minStock

    GlassCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        cornerRadius = 24.dp,
        padding = 12.dp
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Image with status border
            Box(
                modifier = Modifier
                    .size(80.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(Color.White.copy(alpha = 0.05f))
            ) {
                AsyncImage(
                    model = ImageRequest.Builder(LocalContext.current)
                        .data(item.productImage)
                        .crossfade(true)
                        .build(),
                    contentDescription = item.productName,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                
                if (isCritical) {
                    Box(
                        modifier = Modifier
                            .align(Alignment.TopEnd)
                            .padding(4.dp)
                            .size(12.dp)
                            .background(ErrorRed, CircleShape)
                    )
                }
            }

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = item.productName,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = TextPrimary,
                    maxLines = 1
                )
                Text(
                    text = (item.categoryName ?: "Sin categoría").uppercase(),
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Black,
                    color = AmberAccent,
                    letterSpacing = 1.sp
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Row(verticalAlignment = Alignment.Bottom) {
                    Text(
                        text = "${item.currentStock}",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = if (isCritical) ErrorRed else TextPrimary
                    )
                    Text(
                        text = " ${item.unitName ?: "und"}",
                        fontSize = 14.sp,
                        color = TextSecondary,
                        modifier = Modifier.padding(bottom = 4.dp)
                    )
                    
                    Spacer(modifier = Modifier.weight(1f))
                    
                    Column(horizontalAlignment = Alignment.End) {
                        Text(
                            text = "Mínimo",
                            fontSize = 10.sp,
                            color = TextMuted
                        )
                        Text(
                            text = "${item.minStock}",
                            fontSize = 12.sp,
                            color = TextSecondary,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
            
            Icon(
                Icons.Default.ArrowForward,
                contentDescription = null,
                tint = TextMuted,
                modifier = Modifier.size(20.dp)
            )
        }
    }
}

