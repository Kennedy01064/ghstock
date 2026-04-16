package com.gh.stock.ui.screens.reports.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.ui.theme.*

@OptIn(ExperimentalLayoutApi::class, ExperimentalMaterial3Api::class)

@Composable
fun MonthYearPicker(
    selectedMonth: Int,
    selectedYear: Int,
    onMonthYearSelected: (Int, Int) -> Unit,
    modifier: Modifier = Modifier
) {
    var showDialog by remember { mutableStateOf(false) }

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .clickable { showDialog = true },
        color = NavySurface.copy(alpha = 0.6f),
        border = AssistChipDefaults.assistChipBorder(enabled = true, borderColor = GlassBorder)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Default.Info,
                    contentDescription = null,
                    tint = AmberAccent,
                    modifier = Modifier.size(24.dp)
                )
                Spacer(modifier = Modifier.width(12.dp))
                Column {
                    Text(
                        text = "Periodo Seleccionado",
                        fontSize = 11.sp,
                        color = TextMuted
                    )
                    Text(
                        text = "${getMonthName(selectedMonth)} $selectedYear",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary
                    )
                }
            }
            Text(
                text = "CAMBIAR",
                fontSize = 12.sp,
                fontWeight = FontWeight.Black,
                color = AmberAccent
            )
        }
    }

    if (showDialog) {
        AlertDialog(
            onDismissRequest = { showDialog = false },
            containerColor = NavySurface,
            title = {
                Text("Seleccionar Periodo", color = TextPrimary)
            },
            text = {
                Column {
                    // Año Simple por ahora
                    Text("Año", color = TextMuted, fontSize = 12.sp)
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        listOf(2024, 2025, 2026).forEach { year ->
                            FilterChip(
                                selected = selectedYear == year,
                                onClick = { onMonthYearSelected(selectedMonth, year) },
                                label = { Text(year.toString()) },
                                colors = FilterChipDefaults.filterChipColors(
                                    selectedContainerColor = AmberAccent,
                                    selectedLabelColor = Color.Black
                                )
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Text("Mes", color = TextMuted, fontSize = 12.sp)
                    // Grid simple de meses
                    FlowRow(
                        maxItemsInEachRow = 4,
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Center
                    ) {
                        (1..12).forEach { month ->
                            Box(
                                modifier = Modifier
                                    .padding(4.dp)
                                    .size(width = 60.dp, height = 36.dp)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(if (selectedMonth == month) AmberAccent else NavyPrimary)
                                    .clickable { 
                                        onMonthYearSelected(month, selectedYear)
                                        showDialog = false
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = getMonthAbbreviation(month),
                                    color = if (selectedMonth == month) Color.Black else TextPrimary,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 12.sp
                                )
                            }
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showDialog = false }) {
                    Text("CERRAR", color = AmberAccent)
                }
            }
        )
    }
}

private fun getMonthName(month: Int): String {
    return when (month) {
        1 -> "Enero"
        2 -> "Febrero"
        3 -> "Marzo"
        4 -> "Abril"
        5 -> "Mayo"
        6 -> "Junio"
        7 -> "Julio"
        8 -> "Agosto"
        9 -> "Septiembre"
        10 -> "Octubre"
        11 -> "Noviembre"
        12 -> "Diciembre"
        else -> ""
    }
}

private fun getMonthAbbreviation(month: Int): String {
    return when (month) {
        1 -> "ENE"
        2 -> "FEB"
        3 -> "MAR"
        4 -> "ABR"
        5 -> "MAY"
        6 -> "JUN"
        7 -> "JUL"
        8 -> "AGO"
        9 -> "SEP"
        10 -> "OCT"
        11 -> "NOV"
        12 -> "DIC"
        else -> ""
    }
}
