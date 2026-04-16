package com.gh.stock.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.ui.theme.*

/**
 * A premium-styled empty state view using the Glassmorphism theme.
 */
@Composable
fun PremiumEmptyState(
    message: String,
    icon: ImageVector = Icons.Default.List,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        GlassCard(
            modifier = Modifier.size(120.dp),
            cornerRadius = 60.dp,
            padding = 0.dp
        ) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = AmberAccent.copy(alpha = 0.6f),
                    modifier = Modifier.size(56.dp)
                )
            }
        }
        
        Spacer(Modifier.height(32.dp))
        
        Text(
            text = message,
            color = TextPrimary,
            fontSize = 18.sp,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center
        )
        
        Text(
            text = "Todo parece estar vacío por aquí.",
            color = TextMuted,
            fontSize = 14.sp,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(top = 8.dp)
        )
    }
}

/**
 * A premium-styled error state view for network or server issues.
 */
@Composable
fun PremiumErrorState(
    message: String,
    onRetry: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        GlassCard(
            modifier = Modifier.size(120.dp),
            cornerRadius = 32.dp,
            padding = 0.dp
        ) {
            Box(Modifier.fillMaxSize().background(ErrorRed.copy(alpha = 0.1f)), contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.Default.Warning,
                    contentDescription = null,
                    tint = ErrorRed,
                    modifier = Modifier.size(56.dp)
                )
            }
        }
        
        Spacer(Modifier.height(32.dp))
        
        Text(
            text = "¡Ops! Ocurrió un error",
            color = TextPrimary,
            fontSize = 20.sp,
            fontWeight = FontWeight.Black,
            textAlign = TextAlign.Center
        )
        
        Text(
            text = message,
            color = TextSecondary,
            fontSize = 14.sp,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(top = 8.dp, bottom = 48.dp)
        )
        
        Button(
            onClick = onRetry,
            colors = ButtonDefaults.buttonColors(
                containerColor = AmberAccent,
                contentColor = NavyBackground
            ),
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier.height(56.dp).fillMaxWidth(0.7f)
        ) {
            Text("REINTENTAR", fontWeight = FontWeight.Bold, letterSpacing = 2.sp)
        }
    }
}
