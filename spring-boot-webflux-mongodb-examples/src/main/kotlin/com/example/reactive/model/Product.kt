package com.example.reactive.model

import org.springframework.data.annotation.CreatedDate
import org.springframework.data.annotation.Id
import org.springframework.data.annotation.LastModifiedDate
import org.springframework.data.mongodb.core.index.Indexed
import org.springframework.data.mongodb.core.mapping.Document
import java.math.BigDecimal
import java.time.LocalDateTime

@Document(collection = "products")
data class Product(
    @Id
    val id: String? = null,
    
    @Indexed
    val name: String,
    
    val description: String,
    val price: BigDecimal,
    val category: String,
    val tags: List<String> = emptyList(),
    val inStock: Boolean = true,
    val stockQuantity: Int = 0,
    
    @CreatedDate
    val createdAt: LocalDateTime? = null,
    
    @LastModifiedDate
    val updatedAt: LocalDateTime? = null
)