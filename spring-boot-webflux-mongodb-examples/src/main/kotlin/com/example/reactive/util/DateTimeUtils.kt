package com.example.reactive.util

import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

object DateTimeUtils {
    val ISO_FORMATTER: DateTimeFormatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME
    
    fun formatCurrentTime(): String = LocalDateTime.now().format(ISO_FORMATTER)
    
    fun formatTime(dateTime: LocalDateTime): String = dateTime.format(ISO_FORMATTER)
}