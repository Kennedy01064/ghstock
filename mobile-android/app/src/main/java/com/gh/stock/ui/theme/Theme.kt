package com.gh.stock.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable

private val DarkColorScheme = darkColorScheme(
    primary = AmberAccent,
    secondary = NavySecondary,
    tertiary = InfoBlue,
    background = NavyBackground,
    surface = NavySurface,
    onPrimary = NavyBackground,
    onSecondary = TextPrimary,
    onTertiary = TextPrimary,
    onBackground = TextPrimary,
    onSurface = TextPrimary,
    error = ErrorRed,
    onError = TextPrimary
)

@Composable
fun StockTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = DarkColorScheme,
        // TODO: Implement custom Typography here (Fase 5)
        content = content
    )
}
