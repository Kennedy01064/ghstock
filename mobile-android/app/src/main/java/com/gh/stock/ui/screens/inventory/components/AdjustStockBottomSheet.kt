package com.gh.stock.ui.screens.inventory.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.data.remote.models.InventoryItemDto
import com.gh.stock.ui.theme.*
import com.gh.stock.data.remote.NetworkResult

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AdjustStockBottomSheet(
    item: InventoryItemDto,
    onDismiss: () -> Unit,
    onConfirm: (change: Double, reason: String, type: String) -> Unit,
    adjustmentState: NetworkResult<*>?
) {
    var quantityChange by remember { mutableStateOf(0.0) }
    var reason by remember { mutableStateOf("") }
    var selectedType by remember { mutableStateOf("ADJUSTMENT") }

    val sheetState = rememberModalBottomSheetState()
    val haptic = LocalHapticFeedback.current

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = NavySurface,
        scrimColor = Color.Black.copy(alpha = 0.8f),
        dragHandle = { BottomSheetDefaults.DragHandle(color = AmberAccent.copy(alpha = 0.4f)) }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .padding(horizontal = 24.dp)
                .padding(bottom = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Ajustar Stock",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = TextPrimary
            )
            Text(
                text = item.productName,
                fontSize = 14.sp,
                color = AmberAccent,
                modifier = Modifier.padding(bottom = 24.dp)
            )

            // Selector de Tipo
            Row(
                modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                TypeButton("ENTRADA", "ENTRY", selectedType == "ENTRY", Modifier.weight(1f)) { selectedType = it }
                TypeButton("SALIDA", "EXIT", selectedType == "EXIT", Modifier.weight(1f)) { selectedType = it }
                TypeButton("AJUSTE", "ADJUSTMENT", selectedType == "ADJUSTMENT", Modifier.weight(1f)) { selectedType = it }
            }

            // Cantidad Control
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center,
                modifier = Modifier.padding(bottom = 24.dp)
            ) {
                IconButton(
                    onClick = { 
                        quantityChange -= 1.0 
                        haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                    },
                    modifier = Modifier.background(NavySecondary, CircleShape)
                ) {
                    Text("-", color = TextPrimary, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                }

                Text(
                    text = "${if (quantityChange > 0) "+" else ""}$quantityChange",
                    fontSize = 32.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = if (quantityChange >= 0) SuccessGreen else ErrorRed,
                    modifier = Modifier.padding(horizontal = 32.dp)
                )

                IconButton(
                    onClick = { 
                        quantityChange += 1.0 
                        haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                    },
                    modifier = Modifier.background(AmberAccent, CircleShape)
                ) {
                    Icon(Icons.Default.Add, contentDescription = null, tint = NavyBackground)
                }
            }

            // Motivo
            OutlinedTextField(
                value = reason,
                onValueChange = { reason = it },
                label = { Text("Motivo / Nota", color = TextSecondary) },
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                minLines = 2,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = AmberAccent,
                    unfocusedBorderColor = Color.White.copy(alpha = 0.1f)
                )
            )

            Spacer(modifier = Modifier.height(32.dp))

            // Acciones
            Button(
                onClick = { 
                    haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                    onConfirm(quantityChange, reason, selectedType) 
                },
                modifier = Modifier.fillMaxWidth().height(56.dp),
                enabled = adjustmentState !is NetworkResult.Loading<*> && quantityChange != 0.0,
                colors = ButtonDefaults.buttonColors(
                    containerColor = AmberAccent,
                    contentColor = NavyBackground
                ),
                shape = RoundedCornerShape(16.dp)
            ) {
                if (adjustmentState is NetworkResult.Loading<*>) {
                    CircularProgressIndicator(modifier = Modifier.size(24.dp), color = NavyBackground)
                } else {
                    Text("GUARDAR AJUSTE", fontWeight = FontWeight.Bold)
                }
            }
            
            if (adjustmentState is NetworkResult.Success) {
                LaunchedEffect(Unit) { onDismiss() }
            }
        }
    }
}

@Composable
fun TypeButton(
    label: String,
    value: String,
    isSelected: Boolean,
    modifier: Modifier,
    onClick: (String) -> Unit
) {
    Surface(
        onClick = { onClick(value) },
        modifier = modifier.height(40.dp),
        shape = RoundedCornerShape(12.dp),
        color = if (isSelected) AmberAccent else NavySecondary.copy(alpha = 0.5f),
        contentColor = if (isSelected) NavyBackground else TextSecondary
    ) {
        Box(contentAlignment = Alignment.Center) {
            Text(label, fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
    }
}
