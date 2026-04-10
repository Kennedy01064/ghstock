package com.gh.stock.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable

private val DarkColorScheme = darkColorScheme(
    primary = NavyPrimary,
    secondary = NavySecondary,
    tertiary = AmberAccent,
    background = NavyBackground,
    surface = NavySecondary,
    onPrimary = TextPrimary,
    onSecondary = TextPrimary,
    onTertiary = NavyBackground,
    onBackground = TextPrimary,
    onSurface = TextPrimary,
)

@Composable
fun StockTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = DarkColorScheme,
        // typography = Typography, // Se puede expandir luego
        content = content
    )
}
