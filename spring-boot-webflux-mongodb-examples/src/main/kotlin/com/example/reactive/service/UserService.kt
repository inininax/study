package com.example.reactive.service

import com.example.reactive.dto.CreateUserRequest
import com.example.reactive.dto.UpdateUserRequest
import com.example.reactive.dto.UserResponse
import com.example.reactive.exception.DuplicateResourceException
import com.example.reactive.exception.ResourceNotFoundException
import com.example.reactive.extension.toResponse
import com.example.reactive.model.User
import com.example.reactive.repository.UserRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.reactive.asFlow
import kotlinx.coroutines.reactive.awaitFirst
import kotlinx.coroutines.reactive.awaitFirstOrNull
import org.springframework.stereotype.Service
import java.time.LocalDateTime

@Service
class UserService(
    private val userRepository: UserRepository
) {

    suspend fun createUser(request: CreateUserRequest): UserResponse {
        val existingUser = userRepository.findByEmail(request.email).awaitFirstOrNull()
        if (existingUser != null) {
            throw DuplicateResourceException("User with email ${request.email} already exists")
        }

        val user = User(
            email = request.email,
            name = request.name,
            age = request.age,
            department = request.department,
            createdAt = LocalDateTime.now(),
            updatedAt = LocalDateTime.now()
        )

        val savedUser = userRepository.save(user).awaitFirst()
        return savedUser.toResponse()
    }

    suspend fun getUserById(id: String): UserResponse {
        val user = userRepository.findById(id).awaitFirstOrNull()
            ?: throw ResourceNotFoundException("User not found with id: $id")
        return user.toResponse()
    }

    suspend fun getUserByEmail(email: String): UserResponse {
        val user = userRepository.findByEmail(email).awaitFirstOrNull()
            ?: throw ResourceNotFoundException("User not found with email: $email")
        return user.toResponse()
    }

    fun getAllUsers(): Flow<UserResponse> {
        return userRepository.findAll()
            .asFlow()
            .map { it.toResponse() }
    }

    fun getActiveUsers(): Flow<UserResponse> {
        return userRepository.findByActiveTrue()
            .asFlow()
            .map { it.toResponse() }
    }

    fun getUsersByDepartment(department: String): Flow<UserResponse> {
        return userRepository.findByDepartment(department)
            .asFlow()
            .map { it.toResponse() }
    }

    fun searchUsersByName(name: String): Flow<UserResponse> {
        return userRepository.findByNameContainingIgnoreCase(name)
            .asFlow()
            .map { it.toResponse() }
    }

    fun getUsersByAgeRange(minAge: Int, maxAge: Int): Flow<UserResponse> {
        return userRepository.findByAgeBetween(minAge, maxAge)
            .asFlow()
            .map { it.toResponse() }
    }

    suspend fun updateUser(id: String, request: UpdateUserRequest): UserResponse {
        val existingUser = userRepository.findById(id).awaitFirstOrNull()
            ?: throw ResourceNotFoundException("User not found with id: $id")

        val updatedUser = existingUser.copy(
            name = request.name,
            age = request.age,
            department = request.department,
            active = request.active,
            updatedAt = LocalDateTime.now()
        )

        val savedUser = userRepository.save(updatedUser).awaitFirst()
        return savedUser.toResponse()
    }

    suspend fun deactivateUser(id: String): UserResponse {
        val existingUser = userRepository.findById(id).awaitFirstOrNull()
            ?: throw ResourceNotFoundException("User not found with id: $id")

        val deactivatedUser = existingUser.copy(
            active = false,
            updatedAt = LocalDateTime.now()
        )

        val savedUser = userRepository.save(deactivatedUser).awaitFirst()
        return savedUser.toResponse()
    }

    suspend fun deleteUser(id: String) {
        val exists = userRepository.existsById(id).awaitFirst()
        if (!exists) {
            throw ResourceNotFoundException("User not found with id: $id")
        }
        userRepository.deleteById(id).awaitFirstOrNull()
    }

    suspend fun userExistsByEmail(email: String): Boolean {
        return userRepository.existsByEmail(email).awaitFirst()
    }

}