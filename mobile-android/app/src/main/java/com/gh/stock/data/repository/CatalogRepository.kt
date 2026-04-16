package com.gh.stock.data.repository

import com.gh.stock.data.remote.ApiClient
import com.gh.stock.data.remote.NetworkResult
import com.gh.stock.data.remote.models.ProductDto
import com.gh.stock.util.safeApiCall
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class CatalogRepository {

    suspend fun getProducts(
        query: String? = null,
        categoryId: Int? = null,
        skip: Int = 0,
        limit: Int = 50
    ): Flow<NetworkResult<List<ProductDto>>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { 
            ApiClient.catalogService.getProducts(query, categoryId, skip, limit) 
        })
    }

    suspend fun getProductDetails(productId: Int): Flow<NetworkResult<ProductDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { 
            ApiClient.catalogService.getProductDetails(productId) 
        })
    }

    suspend fun getProductByBarcode(barcode: String): Flow<NetworkResult<ProductDto>> = flow {
        emit(NetworkResult.Loading())
        emit(safeApiCall { 
            ApiClient.catalogService.getProductByBarcode(barcode) 
        })
    }
}
