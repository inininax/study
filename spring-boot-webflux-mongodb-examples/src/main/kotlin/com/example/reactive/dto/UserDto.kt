package com.example.reactive.dto

import jakarta.validation.constraints.Email
import jakarta.validation.constraints.Min
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.NotNull
import java.time.LocalDateTime

data class CreateUserRequest(
    @field:Email
    @field:NotBlank
    val email: String,
    
    @field:NotBlank
    val name: String,
    
    @field:NotNull
    @field:Min(0)
    val age: Int,
    
    val department: String? = null
)

data class UpdateUserRequest(
    @field:NotBlank
    val name: String,
    
    @field:NotNull
    @field:Min(0)
    val age: Int,
    
    val department: String? = null,
    
    val active: Boolean = true
)

data class UserResponse(
    val id: String,
    val email: String,
    val name: String,
    val age: Int,
    val department: String?,
    val active: Boolean,
    val createdAt: LocalDateTime?,
    val updatedAt: LocalDateTime?
)