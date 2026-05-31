package com.example.reactive.controller

import com.example.reactive.dto.CreateUserRequest
import com.example.reactive.dto.UpdateUserRequest
import com.example.reactive.dto.UserResponse
import com.example.reactive.service.UserService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.Parameter
import io.swagger.v3.oas.annotations.tags.Tag
import jakarta.validation.Valid
import kotlinx.coroutines.flow.Flow
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "User Management", description = "APIs for managing users")
class UserController(
    private val userService: UserService
) {

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Create a new user", description = "Creates a new user with the provided information")
    suspend fun createUser(
        @Valid @RequestBody request: CreateUserRequest
    ): UserResponse {
        return userService.createUser(request)
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID", description = "Retrieves a user by their unique identifier")
    suspend fun getUserById(
        @Parameter(description = "User ID") @PathVariable id: String
    ): UserResponse {
        return userService.getUserById(id)
    }

    @GetMapping("/email/{email}")
    @Operation(summary = "Get user by email", description = "Retrieves a user by their email address")
    suspend fun getUserByEmail(
        @Parameter(description = "User email") @PathVariable email: String
    ): UserResponse {
        return userService.getUserByEmail(email)
    }

    @GetMapping
    @Operation(summary = "Get all users", description = "Retrieves all users in the system")
    fun getAllUsers(): Flow<UserResponse> {
        return userService.getAllUsers()
    }

    @GetMapping("/active")
    @Operation(summary = "Get active users", description = "Retrieves all active users")
    fun getActiveUsers(): Flow<UserResponse> {
        return userService.getActiveUsers()
    }

    @GetMapping("/department/{department}")
    @Operation(summary = "Get users by department", description = "Retrieves users belonging to a specific department")
    fun getUsersByDepartment(
        @Parameter(description = "Department name") @PathVariable department: String
    ): Flow<UserResponse> {
        return userService.getUsersByDepartment(department)
    }

    @GetMapping("/search")
    @Operation(summary = "Search users by name", description = "Search users by partial name match")
    fun searchUsers(
        @Parameter(description = "Search term for name") @RequestParam name: String
    ): Flow<UserResponse> {
        return userService.searchUsersByName(name)
    }

    @GetMapping("/age-range")
    @Operation(summary = "Get users by age range", description = "Retrieves users within a specific age range")
    fun getUsersByAgeRange(
        @Parameter(description = "Minimum age") @RequestParam minAge: Int,
        @Parameter(description = "Maximum age") @RequestParam maxAge: Int
    ): Flow<UserResponse> {
        return userService.getUsersByAgeRange(minAge, maxAge)
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update user", description = "Updates an existing user with new information")
    suspend fun updateUser(
        @Parameter(description = "User ID") @PathVariable id: String,
        @Valid @RequestBody request: UpdateUserRequest
    ): UserResponse {
        return userService.updateUser(id, request)
    }

    @PatchMapping("/{id}/deactivate")
    @Operation(summary = "Deactivate user", description = "Deactivates a user account")
    suspend fun deactivateUser(
        @Parameter(description = "User ID") @PathVariable id: String
    ): UserResponse {
        return userService.deactivateUser(id)
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Operation(summary = "Delete user", description = "Permanently deletes a user from the system")
    suspend fun deleteUser(
        @Parameter(description = "User ID") @PathVariable id: String
    ) {
        userService.deleteUser(id)
    }

    @GetMapping("/exists/email/{email}")
    @Operation(summary = "Check if user exists by email", description = "Checks if a user with the given email exists")
    suspend fun userExistsByEmail(
        @Parameter(description = "User email") @PathVariable email: String
    ): Boolean {
        return userService.userExistsByEmail(email)
    }
}