package com.example.reactive.service

import com.example.reactive.dto.CreateProductRequest
import com.example.reactive.dto.PagedResponse
import com.example.reactive.dto.ProductResponse
import com.example.reactive.dto.UpdateProductRequest
import com.example.reactive.exception.ResourceNotFoundException
import com.example.reactive.extension.toResponse
import com.example.reactive.model.Product
import com.example.reactive.repository.ProductRepository
import com.example.reactive.util.PageUtils
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.reactive.asFlow
import kotlinx.coroutines.reactive.awaitFirst
import kotlinx.coroutines.reactive.awaitFirstOrNull
import org.springframework.data.domain.PageRequest
import org.springframework.data.domain.Pageable
import org.springframework.data.domain.Sort
import org.springframework.stereotype.Service
import java.math.BigDecimal
import java.time.LocalDateTime

@Service
class ProductService(
    private val productRepository: ProductRepository
) {

    suspend fun createProduct(request: CreateProductRequest): ProductResponse {
        val product = Product(
            name = request.name,
            description = request.description,
            price = request.price,
            category = request.category,
            tags = request.tags,
            inStock = request.stockQuantity > 0,
            stockQuantity = request.stockQuantity,
            createdAt = LocalDateTime.now(),
            updatedAt = LocalDateTime.now()
        )

        val savedProduct = productRepository.save(product).awaitFirst()
        return savedProduct.toResponse()
    }

    suspend fun getProductById(id: String): ProductResponse {
        val product = productRepository.findById(id).awaitFirstOrNull()
            ?: throw ResourceNotFoundException("Product not found with id: $id")
        return product.toResponse()
    }

    suspend fun getAllProducts(page: Int = 0, size: Int = 20, sortBy: String = "createdAt"): PagedResponse<ProductResponse> {
        val pageable: Pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, sortBy))
        val totalElements = productRepository.count().awaitFirst()
        
        val products = productRepository.findAll(Sort.by(Sort.Direction.DESC, sortBy))
            .asFlow()
            .map { it.toResponse() }
            .toList()

        return PageUtils.createPagedResponse(products, page, size, totalElements)
    }

    suspend fun searchProducts(name: String, page: Int = 0, size: Int = 20): PagedResponse<ProductResponse> {
        val pageable: Pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"))
        val products = productRepository.findByNameContainingIgnoreCase(name, pageable)
            .asFlow()
            .map { it.toResponse() }
            .toList()
        val totalElements = products.size.toLong()

        return PageUtils.createPagedResponse(products, page, size, totalElements)
    }

    suspend fun getProductsByCategory(category: String, page: Int = 0, size: Int = 20): PagedResponse<ProductResponse> {
        val pageable: Pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"))
        val totalElements = productRepository.countByCategory(category).awaitFirst()
        
        val products = productRepository.findByCategoryIgnoreCase(category, pageable)
            .asFlow()
            .map { it.toResponse() }
            .toList()

        return PageUtils.createPagedResponse(products, page, size, totalElements)
    }

    suspend fun getAvailableProducts(page: Int = 0, size: Int = 20): PagedResponse<ProductResponse> {
        val pageable: Pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"))
        val totalElements = productRepository.countByInStockTrue().awaitFirst()
        
        val products = productRepository.findByInStockTrue(pageable)
            .asFlow()
            .map { it.toResponse() }
            .toList()

        return PageUtils.createPagedResponse(products, page, size, totalElements)
    }

    suspend fun getProductsByPriceRange(
        minPrice: BigDecimal, 
        maxPrice: BigDecimal, 
        page: Int = 0, 
        size: Int = 20
    ): PagedResponse<ProductResponse> {
        val pageable: Pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.ASC, "price"))
        val totalElements = productRepository.count().awaitFirst()
        
        val products = productRepository.findByPriceBetween(minPrice, maxPrice, pageable)
            .asFlow()
            .map { it.toResponse() }
            .toList()
        val actualTotalElements = products.size.toLong()

        return PageUtils.createPagedResponse(products, page, size, actualTotalElements)
    }

    suspend fun getProductsByTags(tags: List<String>, page: Int = 0, size: Int = 20): PagedResponse<ProductResponse> {
        val pageable: Pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"))
        val totalElements = productRepository.count().awaitFirst()
        
        val products = productRepository.findByTagsIn(tags, pageable)
            .asFlow()
            .map { it.toResponse() }
            .toList()
        val actualTotalElements = products.size.toLong()

        return PageUtils.createPagedResponse(products, page, size, actualTotalElements)
    }

    suspend fun updateProduct(id: String, request: UpdateProductRequest): ProductResponse {
        val existingProduct = productRepository.findById(id).awaitFirstOrNull()
            ?: throw ResourceNotFoundException("Product not found with id: $id")

        val updatedProduct = existingProduct.copy(
            name = request.name,
            description = request.description,
            price = request.price,
            category = request.category,
            tags = request.tags,
            inStock = request.inStock && request.stockQuantity > 0,
            stockQuantity = request.stockQuantity,
            updatedAt = LocalDateTime.now()
        )

        val savedProduct = productRepository.save(updatedProduct).awaitFirst()
        return savedProduct.toResponse()
    }

    suspend fun updateStock(id: String, quantity: Int): ProductResponse {
        val existingProduct = productRepository.findById(id).awaitFirstOrNull()
            ?: throw ResourceNotFoundException("Product not found with id: $id")

        val updatedProduct = existingProduct.copy(
            stockQuantity = quantity,
            inStock = quantity > 0,
            updatedAt = LocalDateTime.now()
        )

        val savedProduct = productRepository.save(updatedProduct).awaitFirst()
        return savedProduct.toResponse()
    }

    suspend fun deleteProduct(id: String) {
        val exists = productRepository.existsById(id).awaitFirst()
        if (!exists) {
            throw ResourceNotFoundException("Product not found with id: $id")
        }
        productRepository.deleteById(id).awaitFirstOrNull()
    }

}