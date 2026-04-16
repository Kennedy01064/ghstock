package com.gh.stock.ui.screens.dashboard.components

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.ui.components.GlassCard
import com.gh.stock.ui.theme.AmberAccent
import com.gh.stock.ui.theme.NavySecondary
import com.gh.stock.ui.theme.TextPrimary
import com.gh.stock.ui.theme.TextSecondary
import androidx.compose.material3.VerticalDivider

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*

@Composable
fun StatsSummaryCard(
    pedidosActivos: Int,
    pedidosEnTransito: Int,
    totalBuildings: Int,
    onClick: () -> Unit = {}
) {
    GlassCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            StatItem(
                value = totalBuildings.toString(),
                label = "Sedes"
            )
            StatDivider()
            StatItem(
                value = pedidosActivos.toString(),
                label = "Pedidos activos"
            )
            StatDivider()
            StatItem(
                value = pedidosEnTransito.toString(),
                label = "En tránsito"
            )
        }
    }
}

@Composable
private fun StatItem(value: String, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = value,
            color = AmberAccent,
            fontSize = 28.sp,
            fontWeight = FontWeight.ExtraBold
        )
        Text(
            text = label,
            color = TextSecondary,
            fontSize = 11.sp
        )
    }
}

@Composable
private fun RowScope.StatDivider() {
    VerticalDivider(
        modifier = Modifier.height(30.dp).align(Alignment.CenterVertically),
        thickness = 1.dp,
        color = TextPrimary.copy(alpha = 0.1f)
    )
}
