package com.example.reactive.exception

class ResourceNotFoundException(message: String) : RuntimeException(message)

class DuplicateResourceException(message: String) : RuntimeException(message)

class InvalidRequestException(message: String) : RuntimeException(message)

data class ErrorResponse(
    val message: String,
    val timestamp: String,
    val path: String? = null,
    val status: Int
)