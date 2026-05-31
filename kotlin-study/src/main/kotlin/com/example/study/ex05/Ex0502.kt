package com.example.study.ex05

fun main() {
    println(getGradeWithSwitch(90))
    println(getGradeWithSwitch(80))
    println(getGradeWithSwitch(70))
    println(getGradeWithSwitch(60))
    println(getGradeWithSwitch(50))
    println(startWithA("ABC"))
    println(startWithA("EEE"))

    judgeNumber(1)
    judgeNumber(2)
    judgeNumber(3)
    judgeNumber(0)
}

// Expression
fun getGradeWithSwitch(score: Int): String {
    return when (score) {
        in 90..99 -> "A"
        in 80..89 -> "B"
        in 70..79 -> "C"
        in 60..69 -> "D"
        else -> "F"
    }
}

fun startWithA(obj: Any): Boolean {
    return when (obj) {
        is String -> obj.startsWith("A")
        else -> false
    }
}

fun judgeNumber(number: Int) {
    when (number) {
        1, 0, -1 -> println("1, 0, -1")
        else -> println("not 1, 0, -1")
    }
}