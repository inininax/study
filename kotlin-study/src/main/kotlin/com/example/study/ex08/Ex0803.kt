package com.example.study.ex08

fun main() {
    printNameAndGender(name = "A", gender = "M")

    print2("A", "B", "C")

    val array = arrayOf("A1", "B1", "C1")
    print2(*array)
}

fun printNameAndGender(name: String, gender: String) {
    println("name: ${name}, gender: ${gender}")
}

fun print2(vararg strings: String) {
    for (str in strings) {
        println(str)
    }
}