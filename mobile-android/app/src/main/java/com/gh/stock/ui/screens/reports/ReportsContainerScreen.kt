package com.gh.stock.ui.screens.reports

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.material3.TabRowDefaults.tabIndicatorOffset
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import android.content.Intent
import android.net.Uri
import kotlinx.coroutines.launch
import androidx.compose.ui.Modifier
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.gh.stock.ui.screens.reports.components.MonthYearPicker
import com.gh.stock.ui.components.AnalyticsSkeleton
import com.gh.stock.ui.theme.*
import org.koin.androidx.compose.koinViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReportsContainerScreen(
    onBack: () -> Unit = {},
    viewModel: ReportsViewModel = koinViewModel()
) {
    val state by viewModel.state.collectAsState()
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    val haptic = LocalHapticFeedback.current
    var selectedTab by remember { mutableIntStateOf(0) }
    val tabs = listOf("Auditoría", "Estadísticas")

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text("Reportes y Auditoría", fontWeight = FontWeight.Bold)
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(imageVector = Icons.Default.ArrowBack, contentDescription = "Atrás")
                    }
                },
                actions = {
                    TextButton(
                        onClick = {
                            haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                            scope.launch {
                                val url = viewModel.getExportUrl()
                                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                                context.startActivity(intent)
                            }
                        }
                    ) {
                        Icon(
                            imageVector = Icons.Default.Info,
                            contentDescription = null,
                            tint = AmberAccent,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("EXPORTAR", color = AmberAccent, fontSize = 12.sp, fontWeight = FontWeight.Black)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = NavySurface,
                    titleContentColor = TextPrimary,
                    navigationIconContentColor = TextPrimary
                )
            )
        },
        containerColor = NavyBackground
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(
                    Brush.verticalGradient(
                        colors = listOf(NavySurface, NavyBackground)
                    )
                )
        ) {
            // Selector de Periodo (Mes/Año)
            MonthYearPicker(
                selectedMonth = state.selectedMonth,
                selectedYear = state.selectedYear,
                onMonthYearSelected = { m, y ->
                    viewModel.onMonthSelected(m)
                    viewModel.onYearSelected(y)
                },
                modifier = Modifier.padding(16.dp)
            )

            // Tabs con diseño premium
            TabRow(
                selectedTabIndex = selectedTab,
                containerColor = Color.Transparent,
                contentColor = AmberAccent,
                indicator = { tabPositions ->
                    TabRowDefaults.SecondaryIndicator(
                        Modifier.tabIndicatorOffset(tabPositions[selectedTab]),
                        color = AmberAccent
                    )
                },
                divider = {}
            ) {
                tabs.forEachIndexed { index, title ->
                    Tab(
                        selected = selectedTab == index,
                        onClick = { 
                            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                            selectedTab = index 
                        },
                        text = {
                            Text(
                                text = title,
                                fontWeight = if (selectedTab == index) FontWeight.Bold else FontWeight.Normal,
                                fontSize = 14.sp
                            )
                        }
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Contenido dinámico
            Box(modifier = Modifier.fillMaxSize()) {
                if (state.isLoading) {
                    Box(modifier = Modifier.fillMaxSize().padding(16.dp)) {
                        AnalyticsSkeleton()
                    }
                } else {
                    when (selectedTab) {
                        0 -> MovementsScreen(movements = state.movements)
                        1 -> AnalyticsScreen(analytics = state.analytics)
                    }
                }
            }
        }
    }
}
