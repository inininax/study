package com.example.study.ex08

fun main() {
    println(max(10, 1))
    println(max(1, 15))
}

/*fun max2(a: Int, b: Int): Int {
    return if (a > b) {
        a
    } else {
        b
    }
}*/
//fun max(a: Int, b: Int): Int = if (a > b) a else b
fun max(a: Int, b: Int) = if (a > b) a else b
