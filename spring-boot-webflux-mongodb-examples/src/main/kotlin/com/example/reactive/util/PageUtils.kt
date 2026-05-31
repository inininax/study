package com.example.reactive.util

import com.example.reactive.dto.PagedResponse

object PageUtils {
    fun <T> createPagedResponse(
        content: List<T>, 
        page: Int, 
        size: Int, 
        totalElements: Long
    ): PagedResponse<T> {
        val totalPages = if (totalElements == 0L) 0 else ((totalElements + size - 1) / size).toInt()
        
        return PagedResponse(
            content = content,
            page = page,
            size = size,
            totalElements = totalElements,
            totalPages = totalPages,
            hasNext = page < totalPages - 1,
            hasPrevious = page > 0
        )
    }
}