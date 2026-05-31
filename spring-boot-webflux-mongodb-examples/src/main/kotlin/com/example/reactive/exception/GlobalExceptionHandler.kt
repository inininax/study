package com.example.reactive.exception

import com.example.reactive.util.DateTimeUtils
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.bind.support.WebExchangeBindException
import org.springframework.web.server.ServerWebExchange

@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException::class)
    fun handleResourceNotFoundException(
        ex: ResourceNotFoundException,
        exchange: ServerWebExchange
    ): ResponseEntity<ErrorResponse> {
        val errorResponse = ErrorResponse(
            message = ex.message ?: "Resource not found",
            timestamp = DateTimeUtils.formatCurrentTime(),
            path = exchange.request.path.value(),
            status = HttpStatus.NOT_FOUND.value()
        )
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorResponse)
    }

    @ExceptionHandler(DuplicateResourceException::class)
    fun handleDuplicateResourceException(
        ex: DuplicateResourceException,
        exchange: ServerWebExchange
    ): ResponseEntity<ErrorResponse> {
        val errorResponse = ErrorResponse(
            message = ex.message ?: "Resource already exists",
            timestamp = DateTimeUtils.formatCurrentTime(),
            path = exchange.request.path.value(),
            status = HttpStatus.CONFLICT.value()
        )
        return ResponseEntity.status(HttpStatus.CONFLICT).body(errorResponse)
    }

    @ExceptionHandler(InvalidRequestException::class)
    fun handleInvalidRequestException(
        ex: InvalidRequestException,
        exchange: ServerWebExchange
    ): ResponseEntity<ErrorResponse> {
        val errorResponse = ErrorResponse(
            message = ex.message ?: "Invalid request",
            timestamp = DateTimeUtils.formatCurrentTime(),
            path = exchange.request.path.value(),
            status = HttpStatus.BAD_REQUEST.value()
        )
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errorResponse)
    }

    @ExceptionHandler(WebExchangeBindException::class)
    fun handleValidationException(
        ex: WebExchangeBindException,
        exchange: ServerWebExchange
    ): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.fieldErrors.map { error ->
            "${error.field}: ${error.defaultMessage}"
        }.joinToString(", ")

        val errorResponse = ErrorResponse(
            message = "Validation failed: $errors",
            timestamp = DateTimeUtils.formatCurrentTime(),
            path = exchange.request.path.value(),
            status = HttpStatus.BAD_REQUEST.value()
        )
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errorResponse)
    }

    @ExceptionHandler(Exception::class)
    fun handleGenericException(
        ex: Exception,
        exchange: ServerWebExchange
    ): ResponseEntity<ErrorResponse> {
        val errorResponse = ErrorResponse(
            message = "Internal server error: ${ex.message}",
            timestamp = DateTimeUtils.formatCurrentTime(),
            path = exchange.request.path.value(),
            status = HttpStatus.INTERNAL_SERVER_ERROR.value()
        )
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse)
    }
}