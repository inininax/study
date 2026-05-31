package com.example.reactive.extension

import com.example.reactive.dto.UserResponse
import com.example.reactive.dto.ProductResponse
import com.example.reactive.model.User
import com.example.reactive.model.Product

fun User.toResponse(): UserResponse {
    return UserResponse(
        id = this.id!!,
        email = this.email,
        name = this.name,
        age = this.age,
        department = this.department,
        active = this.active,
        createdAt = this.createdAt,
        updatedAt = this.updatedAt
    )
}

fun Product.toResponse(): ProductResponse {
    return ProductResponse(
        id = this.id!!,
        name = this.name,
        description = this.description,
        price = this.price,
        category = this.category,
        tags = this.tags,
        inStock = this.inStock,
        stockQuantity = this.stockQuantity,
        createdAt = this.createdAt,
        updatedAt = this.updatedAt
    )
}