package com.example.reactive.repository

import com.example.reactive.model.User
import org.springframework.data.domain.Pageable
import org.springframework.data.mongodb.repository.ReactiveMongoRepository
import org.springframework.stereotype.Repository
import reactor.core.publisher.Flux
import reactor.core.publisher.Mono

@Repository
interface UserRepository : ReactiveMongoRepository<User, String> {
    
    fun findByEmail(email: String): Mono<User>
    
    fun findByEmailIgnoreCase(email: String): Mono<User>
    
    fun findByActiveTrue(): Flux<User>
    
    fun findByActiveFalse(): Flux<User>
    
    fun findByDepartment(department: String): Flux<User>
    
    fun findByNameContainingIgnoreCase(name: String): Flux<User>
    
    fun findByAgeBetween(minAge: Int, maxAge: Int): Flux<User>
    
    fun existsByEmail(email: String): Mono<Boolean>
}