package com.example.study.ex05

fun main() {
    val score = 30
    val grade = getPassOrFail(score)

    println("score: $score, grade: $grade")

    println(score in 0..100)
    println(-1 in 0..100)
}

// Expression
fun getPassOrFail(score: Int): String {
    return if (score >= 90) {
        "A"
    } else if (score >= 80) {
        "B"
    } else if (score >= 50) {
        "D"
    } else {
        "F"
    }
}