package com.gh.stock.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.gh.stock.ui.theme.NavySurface

@Composable
fun ShimmerBrush(
    showShimmer: Boolean = true,
    targetValue: Float = 1000f
): Brush {
    return if (showShimmer) {
        val shimmerColors = listOf(
            NavySurface.copy(alpha = 0.6f),
            NavySurface.copy(alpha = 0.2f),
            NavySurface.copy(alpha = 0.6f),
        )

        val transition = rememberInfiniteTransition(label = "shimmer")
        val translateAnimation = transition.animateFloat(
            initialValue = 0f,
            targetValue = targetValue,
            animationSpec = infiniteRepeatable(
                animation = tween(800), repeatMode = RepeatMode.Restart
            ),
            label = "shimmer"
        )

        Brush.linearGradient(
            colors = shimmerColors,
            start = Offset.Zero,
            end = Offset(x = translateAnimation.value, y = translateAnimation.value)
        )
    } else {
        Brush.linearGradient(
            colors = listOf(Color.Transparent, Color.Transparent),
            start = Offset.Zero,
            end = Offset.Zero
        )
    }
}

@Composable
fun ProductSkeleton() {
    val brush = ShimmerBrush()
    
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(100.dp)
            .background(brush, RoundedCornerShape(16.dp))
    )
}

@Composable
fun InventorySkeleton() {
    val brush = ShimmerBrush()
    
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Box(
            modifier = Modifier
                .size(50.dp)
                .background(brush, RoundedCornerShape(8.dp))
        )
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Box(
                modifier = Modifier
                    .width(150.dp)
                    .height(20.dp)
                    .background(brush, RoundedCornerShape(4.dp))
            )
            Box(
                modifier = Modifier
                    .width(100.dp)
                    .height(14.dp)
                    .background(brush, RoundedCornerShape(4.dp))
            )
        }
    }
}

@Composable
fun MetricSkeleton() {
    val brush = ShimmerBrush()
    Box(
        modifier = Modifier
            .width(160.dp)
            .height(120.dp)
            .background(brush, RoundedCornerShape(24.dp))
    )
}

@Composable
fun OrderSkeleton() {
    val brush = ShimmerBrush()
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(80.dp)
                .background(brush, RoundedCornerShape(16.dp))
        )
        Box(
            modifier = Modifier
                .width(200.dp)
                .height(20.dp)
                .background(brush, RoundedCornerShape(4.dp))
        )
    }
}

@Composable
fun AnalyticsSkeleton() {
    val brush = ShimmerBrush()
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(20.dp)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(160.dp)
                .background(brush, RoundedCornerShape(24.dp))
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(Modifier.weight(1f).height(100.dp).background(brush, RoundedCornerShape(16.dp)))
            Box(Modifier.weight(1f).height(100.dp).background(brush, RoundedCornerShape(16.dp)))
        }
        repeat(3) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(40.dp)
                    .background(brush, RoundedCornerShape(8.dp))
            )
        }
    }
}
