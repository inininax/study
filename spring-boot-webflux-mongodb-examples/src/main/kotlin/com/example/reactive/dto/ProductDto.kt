package com.example.reactive.dto

import jakarta.validation.constraints.DecimalMin
import jakarta.validation.constraints.Min
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.NotNull
import java.math.BigDecimal
import java.time.LocalDateTime

data class CreateProductRequest(
    @field:NotBlank
    val name: String,
    
    @field:NotBlank
    val description: String,
    
    @field:NotNull
    @field:DecimalMin("0.0")
    val price: BigDecimal,
    
    @field:NotBlank
    val category: String,
    
    val tags: List<String> = emptyList(),
    
    @field:Min(0)
    val stockQuantity: Int = 0
)

data class UpdateProductRequest(
    @field:NotBlank
    val name: String,
    
    @field:NotBlank
    val description: String,
    
    @field:NotNull
    @field:DecimalMin("0.0")
    val price: BigDecimal,
    
    @field:NotBlank
    val category: String,
    
    val tags: List<String> = emptyList(),
    val inStock: Boolean = true,
    
    @field:Min(0)
    val stockQuantity: Int = 0
)

data class ProductResponse(
    val id: String,
    val name: String,
    val description: String,
    val price: BigDecimal,
    val category: String,
    val tags: List<String>,
    val inStock: Boolean,
    val stockQuantity: Int,
    val createdAt: LocalDateTime?,
    val updatedAt: LocalDateTime?
)

data class PagedResponse<T>(
    val content: List<T>,
    val page: Int,
    val size: Int,
    val totalElements: Long,
    val totalPages: Int,
    val hasNext: Boolean,
    val hasPrevious: Boolean
)