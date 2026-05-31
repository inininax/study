package com.example.study.ex07

fun main() {
    println(parseIntOrThrow("1"))
    //println(parseIntOrThrow("A"))

    println(parseIntOrNull("1"))
    println(parseIntOrNull("A"))
}

fun parseIntOrThrow(str: String): Int {
    return try {
        str.toInt()
    } catch (e: NumberFormatException) {
        throw IllegalArgumentException("not number: ${str}")
    }
}

fun parseIntOrNull(str: String): Int? {
    return try {
        str.toInt()
    } catch (e: NumberFormatException) {
        null
    }
}