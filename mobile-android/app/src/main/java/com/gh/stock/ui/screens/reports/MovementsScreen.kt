package com.gh.stock.ui.screens.reports

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.data.remote.models.InventoryMovementDto
import com.gh.stock.ui.components.GlassCard
import com.gh.stock.ui.components.PremiumEmptyState
import com.gh.stock.ui.theme.*
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter

@Composable
fun MovementsScreen(
    movements: List<InventoryMovementDto>
) {
    if (movements.isEmpty()) {
        PremiumEmptyState(
            message = "Sin movimientos registrados",
            icon = Icons.Default.List
        )
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(movements) { movement ->
                MovementItem(movement)
            }
        }
    }
}

@Composable
fun MovementItem(movement: InventoryMovementDto) {
    val typeConfig = getMovementTypeConfig(movement.movementType, movement.quantity)
    
    GlassCard(
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Icono de Tipo
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(typeConfig.color.copy(alpha = 0.2f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = typeConfig.icon,
                    contentDescription = null,
                    tint = typeConfig.color,
                    modifier = Modifier.size(20.dp)
                )
            }

            Spacer(modifier = Modifier.width(16.dp))

            // Información
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = movement.product.name,
                    color = TextPrimary,
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp
                )
                Text(
                    text = "${typeConfig.label} • ${formatDate(movement.createdAt)}",
                    color = TextMuted,
                    fontSize = 12.sp
                )
                if (movement.referenceType != null) {
                    Text(
                        text = "Ref: ${movement.referenceType}",
                        color = AmberAccent.copy(alpha = 0.7f),
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            // Cantidad y Precio (Visibilidad de costos confirmada por usuario)
            Column(horizontalAlignment = Alignment.End) {
                val prefix = if (movement.quantity > 0) "+" else ""
                Text(
                    text = "$prefix${movement.quantity}",
                    color = typeConfig.color,
                    fontWeight = FontWeight.Black,
                    fontSize = 16.sp
                )
                val unitPrice = movement.product.price ?: 0.0
                val totalValue = movement.quantity * unitPrice
                Text(
                    text = "S/ ${String.format("%.2f", Math.abs(totalValue))}",
                    color = TextSecondary,
                    fontSize = 11.sp
                )
            }
        }
    }
}

data class MovementTypeConfig(
    val label: String,
    val icon: ImageVector,
    val color: Color
)

private fun getMovementTypeConfig(type: String, quantity: Int): MovementTypeConfig {
    return when (type) {
        "receive", "manual_add" -> MovementTypeConfig("Entrada", Icons.Default.Add, SuccessGreen)
        "consume" -> MovementTypeConfig("Consumo", Icons.Default.ArrowDropDown, ErrorRed)
        "adjust" -> {
            if (quantity > 0) MovementTypeConfig("Ajuste (+)", Icons.Default.Add, AmberAccent)
            else MovementTypeConfig("Ajuste (-)", Icons.Default.Add, AmberAccent)
        }
        "transfer_in" -> MovementTypeConfig("Transf. Recibida", Icons.Default.ArrowBack, SuccessGreen)
        "transfer_out" -> MovementTypeConfig("Transf. Enviada", Icons.Default.ArrowForward, ErrorRed)
        "return_out" -> MovementTypeConfig("Devolución", Icons.Default.Refresh, TextMuted)
        "shrinkage" -> MovementTypeConfig("Merma / Daño", Icons.Default.Delete, ErrorRed)
        else -> MovementTypeConfig("Movimiento", Icons.Default.Info, TextPrimary)
    }
}

private fun formatDate(dateStr: String): String {
    return try {
        val date = ZonedDateTime.parse(dateStr)
        date.format(DateTimeFormatter.ofPattern("dd/MM HH:mm"))
    } catch (e: Exception) {
        dateStr
    }
}
