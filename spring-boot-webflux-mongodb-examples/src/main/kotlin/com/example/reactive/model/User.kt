package com.example.reactive.model

import org.springframework.data.annotation.CreatedDate
import org.springframework.data.annotation.Id
import org.springframework.data.annotation.LastModifiedDate
import org.springframework.data.mongodb.core.index.Indexed
import org.springframework.data.mongodb.core.mapping.Document
import java.time.LocalDateTime

@Document(collection = "users")
data class User(
    @Id
    val id: String? = null,
    
    @Indexed(unique = true)
    val email: String,
    
    val name: String,
    val age: Int,
    val department: String?,
    val active: Boolean = true,
    
    @CreatedDate
    val createdAt: LocalDateTime? = null,
    
    @LastModifiedDate
    val updatedAt: LocalDateTime? = null
)