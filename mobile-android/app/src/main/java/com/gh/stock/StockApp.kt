package com.gh.stock

import android.app.Application
import com.gh.stock.data.local.TokenDataStore
import com.gh.stock.data.remote.ApiClient
import com.gh.stock.di.appModule
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.koin.android.ext.koin.androidContext
import org.koin.android.ext.koin.androidLogger
import org.koin.core.context.startKoin
import org.koin.core.logger.Level

class StockApp : Application() {

    override fun onCreate() {
        super.onCreate()

        startKoin {
            androidLogger(Level.ERROR)
            androidContext(this@StockApp)
            modules(appModule)
        }

        // Inicializar el cliente autenticado si ya existe un token guardado
        CoroutineScope(Dispatchers.IO).launch {
            val tokenDataStore = TokenDataStore(this@StockApp)
            if (tokenDataStore.getAccessToken() != null) {
                ApiClient.initAuthClient(tokenDataStore)
            }
        }
    }
}
