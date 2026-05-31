package com.example.study.ex06

fun main() {
    val numbers = listOf(1L, 2L, 3L)
    for (number in numbers) {
        println(number)
    }

    for (i in 1..3) {
        println("seq $i")
    }

    // downTo, step은 중위 호출 함수

    for (i in 3 downTo 1) {
        println("downTo $i")
    }

    for (i in 1..5 step 2) {
        println("step $i")
    }

    var i = 0;
    while (i < 3) {
        println("while $i")
        i++
    }
}
