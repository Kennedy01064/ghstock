package com.gh.stock.data.remote

import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow

/**
 * Canal global para eventos de sesion expirada.
 * MainActivity observa este flow y navega a Login cuando se emite.
 */
object SessionManager {

    private val _sessionExpiredFlow = MutableSharedFlow<Unit>(extraBufferCapacity = 1)
    val sessionExpiredFlow = _sessionExpiredFlow.asSharedFlow()

    fun notifySessionExpired() {
        _sessionExpiredFlow.tryEmit(Unit)
    }
}
