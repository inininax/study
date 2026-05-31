package com.example.reactive.repository

import com.example.reactive.model.Product
import org.springframework.data.domain.Pageable
import org.springframework.data.mongodb.repository.Query
import org.springframework.data.mongodb.repository.ReactiveMongoRepository
import org.springframework.stereotype.Repository
import reactor.core.publisher.Flux
import reactor.core.publisher.Mono
import java.math.BigDecimal

@Repository
interface ProductRepository : ReactiveMongoRepository<Product, String> {
    
    fun findByNameContainingIgnoreCase(name: String, pageable: Pageable): Flux<Product>
    
    fun findByCategory(category: String, pageable: Pageable): Flux<Product>
    
    fun findByCategoryIgnoreCase(category: String, pageable: Pageable): Flux<Product>
    
    fun findByInStockTrue(pageable: Pageable): Flux<Product>
    
    fun findByInStockFalse(pageable: Pageable): Flux<Product>
    
    fun findByPriceBetween(minPrice: BigDecimal, maxPrice: BigDecimal, pageable: Pageable): Flux<Product>
    
    fun findByPriceLessThanEqual(maxPrice: BigDecimal, pageable: Pageable): Flux<Product>
    
    fun findByPriceGreaterThanEqual(minPrice: BigDecimal, pageable: Pageable): Flux<Product>
    
    @Query("{ 'tags': { \$in: ?0 } }")
    fun findByTagsIn(tags: List<String>, pageable: Pageable): Flux<Product>
    
    @Query("{ 'stockQuantity': { \$gt: 0 } }")
    fun findAvailableProducts(pageable: Pageable): Flux<Product>
    
    fun countByCategory(category: String): Mono<Long>
    
    fun countByInStockTrue(): Mono<Long>
}