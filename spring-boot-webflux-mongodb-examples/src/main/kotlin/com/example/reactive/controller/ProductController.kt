package com.example.reactive.controller

import com.example.reactive.dto.CreateProductRequest
import com.example.reactive.dto.PagedResponse
import com.example.reactive.dto.ProductResponse
import com.example.reactive.dto.UpdateProductRequest
import com.example.reactive.service.ProductService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.Parameter
import io.swagger.v3.oas.annotations.tags.Tag
import jakarta.validation.Valid
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*
import java.math.BigDecimal

@RestController
@RequestMapping("/api/v1/products")
@Tag(name = "Product Management", description = "APIs for managing products")
class ProductController(
    private val productService: ProductService
) {

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Create a new product", description = "Creates a new product with the provided information")
    suspend fun createProduct(
        @Valid @RequestBody request: CreateProductRequest
    ): ProductResponse {
        return productService.createProduct(request)
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get product by ID", description = "Retrieves a product by its unique identifier")
    suspend fun getProductById(
        @Parameter(description = "Product ID") @PathVariable id: String
    ): ProductResponse {
        return productService.getProductById(id)
    }

    @GetMapping
    @Operation(summary = "Get all products", description = "Retrieves all products with pagination support")
    suspend fun getAllProducts(
        @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") page: Int,
        @Parameter(description = "Page size") @RequestParam(defaultValue = "20") size: Int,
        @Parameter(description = "Sort field") @RequestParam(defaultValue = "createdAt") sortBy: String
    ): PagedResponse<ProductResponse> {
        return productService.getAllProducts(page, size, sortBy)
    }

    @GetMapping("/search")
    @Operation(summary = "Search products", description = "Search products by name with pagination")
    suspend fun searchProducts(
        @Parameter(description = "Product name search term") @RequestParam name: String,
        @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") page: Int,
        @Parameter(description = "Page size") @RequestParam(defaultValue = "20") size: Int
    ): PagedResponse<ProductResponse> {
        return productService.searchProducts(name, page, size)
    }

    @GetMapping("/category/{category}")
    @Operation(summary = "Get products by category", description = "Retrieves products in a specific category")
    suspend fun getProductsByCategory(
        @Parameter(description = "Product category") @PathVariable category: String,
        @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") page: Int,
        @Parameter(description = "Page size") @RequestParam(defaultValue = "20") size: Int
    ): PagedResponse<ProductResponse> {
        return productService.getProductsByCategory(category, page, size)
    }

    @GetMapping("/available")
    @Operation(summary = "Get available products", description = "Retrieves all products that are in stock")
    suspend fun getAvailableProducts(
        @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") page: Int,
        @Parameter(description = "Page size") @RequestParam(defaultValue = "20") size: Int
    ): PagedResponse<ProductResponse> {
        return productService.getAvailableProducts(page, size)
    }

    @GetMapping("/price-range")
    @Operation(summary = "Get products by price range", description = "Retrieves products within a specific price range")
    suspend fun getProductsByPriceRange(
        @Parameter(description = "Minimum price") @RequestParam minPrice: BigDecimal,
        @Parameter(description = "Maximum price") @RequestParam maxPrice: BigDecimal,
        @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") page: Int,
        @Parameter(description = "Page size") @RequestParam(defaultValue = "20") size: Int
    ): PagedResponse<ProductResponse> {
        return productService.getProductsByPriceRange(minPrice, maxPrice, page, size)
    }

    @GetMapping("/tags")
    @Operation(summary = "Get products by tags", description = "Retrieves products that contain any of the specified tags")
    suspend fun getProductsByTags(
        @Parameter(description = "Product tags (comma-separated)") @RequestParam tags: List<String>,
        @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") page: Int,
        @Parameter(description = "Page size") @RequestParam(defaultValue = "20") size: Int
    ): PagedResponse<ProductResponse> {
        return productService.getProductsByTags(tags, page, size)
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update product", description = "Updates an existing product with new information")
    suspend fun updateProduct(
        @Parameter(description = "Product ID") @PathVariable id: String,
        @Valid @RequestBody request: UpdateProductRequest
    ): ProductResponse {
        return productService.updateProduct(id, request)
    }

    @PatchMapping("/{id}/stock")
    @Operation(summary = "Update product stock", description = "Updates the stock quantity of a product")
    suspend fun updateProductStock(
        @Parameter(description = "Product ID") @PathVariable id: String,
        @Parameter(description = "Stock quantity") @RequestParam quantity: Int
    ): ProductResponse {
        return productService.updateStock(id, quantity)
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Operation(summary = "Delete product", description = "Permanently deletes a product from the system")
    suspend fun deleteProduct(
        @Parameter(description = "Product ID") @PathVariable id: String
    ) {
        productService.deleteProduct(id)
    }
}