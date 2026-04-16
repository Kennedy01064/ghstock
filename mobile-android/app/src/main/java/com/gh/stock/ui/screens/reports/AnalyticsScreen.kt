package com.gh.stock.ui.screens.reports

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.data.remote.models.AnalyticsReportDto
import com.gh.stock.ui.components.AnalyticsSkeleton
import com.gh.stock.ui.components.GlassCard
import com.gh.stock.ui.theme.*

@Composable
fun AnalyticsScreen(
    analytics: AnalyticsReportDto?
) {
    if (analytics == null) {
        Box(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            AnalyticsSkeleton()
        }
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(20.dp)
    ) {
        // Tarjeta Principal: Inversión / Gasto
        item {
            TotalInvestmentCard(analytics.costoDespachadoMes)
        }

        // Grid de KPIs
        item {
            Row(modifier = Modifier.fillMaxWidth()) {
                KpiMiniCard(
                    title = "Movimientos",
                    value = analytics.totalMovements.toString(),
                    icon = Icons.Default.Refresh,
                    color = InfoBlue,
                    modifier = Modifier.weight(1f)
                )
                Spacer(modifier = Modifier.width(12.dp))
                KpiMiniCard(
                    title = "Consumos",
                    value = analytics.totalConsumptions.toString(),
                    icon = Icons.Default.ArrowDropDown,
                    color = ErrorRed,
                    modifier = Modifier.weight(1f)
                )
            }
        }

        @Suppress("ConditionCheckOnTypeRawValue")
        if (analytics.mostConsumedProduct != null) {
            item {
                FeaturedProductCard(
                    title = "Producto más Utilizado",
                    name = analytics.mostConsumedProduct.productName,
                    quantity = analytics.mostConsumedProduct.totalConsumed,
                    icon = Icons.Default.Star
                )
            }
        }

        // Distribución por Sede
        item {
            Text(
                text = "Gasto por Sede",
                fontSize = 18.sp,
                fontWeight = FontWeight.Black,
                color = TextPrimary,
                letterSpacing = (-0.5).sp
            )
        }

        items(analytics.pedidosPorEdificio.sortedByDescending { it.gastoTotal ?: 0.0 }) { stat ->
            BuildingStatItem(stat.buildingName, stat.gastoTotal ?: 0.0, analytics.costoDespachadoMes)
        }
    }
}

@Composable
fun TotalInvestmentCard(amount: Double) {
    GlassCard(
        modifier = Modifier.fillMaxWidth(),
        cornerRadius = 24.dp
    ) {
        Column(
            modifier = Modifier
                .background(
                    Brush.linearGradient(
                        colors = listOf(NavySurface, NavyPrimary.copy(alpha = 0.5f))
                    )
                )
                .padding(24.dp)
        ) {
            Text(
                "Inversión Despachada",
                color = TextMuted,
                fontSize = 13.sp,
                fontWeight = FontWeight.Medium
            )
            Text(
                "S/ ${String.format("%,.2f", amount)}",
                color = TextPrimary,
                fontSize = 32.sp,
                fontWeight = FontWeight.Black,
                letterSpacing = (-1).sp
            )
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Default.Info,
                    contentDescription = null,
                    tint = AmberAccent,
                    modifier = Modifier.size(14.dp)
                )
                Spacer(modifier = Modifier.width(4.dp))
                Text(
                    "Suma total de valor de productos enviados a sedes",
                    color = TextSecondary,
                    fontSize = 11.sp
                )
            }
        }
    }
}

@Composable
fun KpiMiniCard(
    title: String,
    value: String,
    icon: ImageVector,
    color: Color,
    modifier: Modifier = Modifier
) {
    GlassCard(
        modifier = modifier,
        cornerRadius = 16.dp
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Icon(imageVector = icon, contentDescription = null, tint = color, modifier = Modifier.size(24.dp))
            Spacer(modifier = Modifier.height(12.dp))
            Text(value, fontSize = 20.sp, fontWeight = FontWeight.Black, color = TextPrimary)
            Text(title, fontSize = 11.sp, color = TextMuted)
        }
    }
}

@Composable
fun FeaturedProductCard(
    title: String,
    name: String,
    quantity: Int,
    icon: ImageVector
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = AmberAccent.copy(alpha = 0.1f),
        shape = RoundedCornerShape(16.dp),
        border = AssistChipDefaults.assistChipBorder(enabled = true, borderColor = AmberAccent.copy(alpha = 0.3f))
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(imageVector = icon, contentDescription = null, tint = AmberAccent, modifier = Modifier.size(32.dp))
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(title, fontSize = 11.sp, color = AmberAccent, fontWeight = FontWeight.Bold)
                Text(name, fontSize = 16.sp, color = TextPrimary, fontWeight = FontWeight.Bold)
                Text("$quantity unidades consumidas", fontSize = 12.sp, color = TextSecondary)
            }
        }
    }
}

@Composable
fun BuildingStatItem(name: String, amount: Double, total: Double) {
    val percentage = if (total > 0) (amount / total).toFloat() else 0f
    
    Column(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.Bottom
        ) {
            Text(name, color = TextPrimary, fontSize = 14.sp, fontWeight = FontWeight.Bold)
            Text("S/ ${String.format("%.2f", amount)}", color = TextSecondary, fontSize = 13.sp)
        }
        Spacer(modifier = Modifier.height(8.dp))
        LinearProgressIndicator(
            progress = { percentage },
            modifier = Modifier
                .fillMaxWidth()
                .height(6.dp)
                .clip(RoundedCornerShape(3.dp)),
            color = AmberAccent,
            trackColor = NavySurface
        )
    }
}
