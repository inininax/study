package com.example.study.ex02

fun main() {
    //val person = Person("kotlin을 공부하고 있어요.")
    val person = Person(null)
    println(startWithA(person.name))
}

fun startWithA(str: String): Boolean {
    return str.startsWith("A")
}