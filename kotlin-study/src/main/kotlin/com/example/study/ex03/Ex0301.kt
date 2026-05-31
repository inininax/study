package com.example.study.ex03

fun main() {
    val number1: Int? = 3
    val number2: Long = number1?.toLong() ?: 0L

    val number3 = 3.0  // Double
    val number4 = 3.0f // Float

    println((number1 ?: 0) + number2)
}