package com.gh.stock.data.remote.services

import com.gh.stock.data.remote.models.ProductDto
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface CatalogApiService {

    @GET("catalog/products")
    suspend fun getProducts(
        @Query("search") query: String? = null,
        @Query("category_id") categoryId: Int? = null,
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 50
    ): Response<List<ProductDto>>

    @GET("catalog/products/{id}")
    suspend fun getProductDetails(
        @Path("id") productId: Int
    ): Response<ProductDto>

    @GET("catalog/products/barcode/{code}")
    suspend fun getProductByBarcode(
        @Path("code") barcode: String
    ): Response<ProductDto>
}
