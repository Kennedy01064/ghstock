package com.gh.stock.ui.screens.login

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.R
import com.gh.stock.ui.components.GlassCard
import com.gh.stock.ui.theme.*
import org.koin.androidx.compose.koinViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(
    onLoginSuccess: () -> Unit,
    viewModel: LoginViewModel = koinViewModel()
) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val haptic = LocalHapticFeedback.current
    val uiState by viewModel.uiState.collectAsState()

    // Animación de entrada para el contenido
    var visible by remember { mutableStateOf(false) }
    LaunchedEffect(Unit) { visible = true }

    LaunchedEffect(uiState) {
        if (uiState is LoginUiState.Success) {
            onLoginSuccess()
        } else if (uiState is LoginUiState.Error) {
            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(NavySecondary, NavyBackground)
                )
            )
    ) {
        // Círculos decorativos de fondo para mejorar el efecto glassmorphism
        Box(
            modifier = Modifier
                .offset(x = (-50).dp, y = (-50).dp)
                .size(300.dp)
                .background(AmberAccent.copy(alpha = 0.05f), RoundedCornerShape(150.dp))
                .blur(80.dp)
        )

        AnimatedVisibility(
            visible = visible,
            enter = fadeIn(animationSpec = tween(1000)) + slideInVertically(initialOffsetY = { 50 }),
            modifier = Modifier.fillMaxSize()
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .systemBarsPadding()
                    .padding(horizontal = 32.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                // Logo Section con el nuevo arte corporal
                Image(
                    painter = painterResource(id = R.drawable.logo_grupo_hernandez),
                    contentDescription = "Grupo Hernández",
                    modifier = Modifier
                        .size(220.dp)
                        .padding(bottom = 16.dp)
                )
                
                Text(
                    text = "CONTROL DE INVENTARIO",
                    fontSize = 14.sp,
                    color = AmberAccent,
                    fontWeight = FontWeight.Light,
                    letterSpacing = 4.sp,
                    modifier = Modifier.padding(bottom = 40.dp)
                )

                GlassCard(
                    modifier = Modifier.fillMaxWidth(),
                    cornerRadius = 32.dp,
                    padding = 24.dp,
                    borderWidth = 0.5.dp
                ) {
                    Column(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "Bienvenido",
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary,
                            modifier = Modifier.padding(bottom = 24.dp).align(Alignment.Start)
                        )

                        PremiumTextField(
                            value = username,
                            onValueChange = {
                                username = it
                                if (uiState is LoginUiState.Error) viewModel.clearError()
                            },
                            label = "Usuario",
                            icon = Icons.Default.Person,
                            enabled = uiState !is LoginUiState.Loading
                        )

                        Spacer(modifier = Modifier.height(16.dp))

                        PremiumTextField(
                            value = password,
                            onValueChange = {
                                password = it
                                if (uiState is LoginUiState.Error) viewModel.clearError()
                            },
                            label = "Contraseña",
                            icon = Icons.Default.Lock,
                            isPassword = true,
                            enabled = uiState !is LoginUiState.Loading
                        )

                        if (uiState is LoginUiState.Error) {
                            Text(
                                text = (uiState as LoginUiState.Error).message,
                                color = ErrorRed,
                                fontSize = 12.sp,
                                modifier = Modifier.padding(top = 16.dp).fillMaxWidth()
                            )
                        }

                        Spacer(modifier = Modifier.height(32.dp))

                        Button(
                            onClick = { 
                                haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                                viewModel.login(username, password) 
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(56.dp),
                            enabled = uiState !is LoginUiState.Loading,
                            colors = ButtonDefaults.buttonColors(
                                containerColor = AmberAccent,
                                contentColor = NavyBackground,
                                disabledContainerColor = AmberAccent.copy(alpha = 0.3f)
                            ),
                            shape = RoundedCornerShape(16.dp),
                            elevation = ButtonDefaults.buttonElevation(defaultElevation = 8.dp)
                        ) {
                            if (uiState is LoginUiState.Loading) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(24.dp),
                                    color = NavyBackground,
                                    strokeWidth = 3.dp
                                )
                            } else {
                                Text(
                                    "INICIAR SESIÓN",
                                    fontWeight = FontWeight.ExtraBold,
                                    letterSpacing = 1.sp
                                )
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(32.dp))
                Text(
                    text = "v1.5 Premium Hub",
                    color = TextMuted,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}

@Composable
fun PremiumTextField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    enabled: Boolean = true,
    isPassword: Boolean = false
) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Text(
            text = label,
            color = TextSecondary,
            fontSize = 13.sp,
            fontWeight = FontWeight.Medium,
            modifier = Modifier.padding(bottom = 8.dp, start = 4.dp)
        )
        OutlinedTextField(
            value = value,
            onValueChange = onValueChange,
            leadingIcon = { Icon(icon, contentDescription = null, tint = AmberAccent.copy(alpha = 0.8f)) },
            visualTransformation = if (isPassword) PasswordVisualTransformation() else androidx.compose.ui.text.input.VisualTransformation.None,
            modifier = Modifier.fillMaxWidth(),
            enabled = enabled,
            shape = RoundedCornerShape(16.dp),
            singleLine = true,
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = AmberAccent,
                unfocusedBorderColor = Color.White.copy(alpha = 0.15f),
                focusedTextColor = TextPrimary,
                unfocusedTextColor = TextPrimary,
                cursorColor = AmberAccent,
                focusedContainerColor = Color.White.copy(alpha = 0.03f),
                unfocusedContainerColor = Color.White.copy(alpha = 0.03f)
            )
        )
    }
}
