package com.example.study.ex09

fun main() {
    Derived(200)
}

open class Base(
    open val number: Int = 100
) {
    init {
        println("base init")
        println(number) // 0
    }
}

class Derived(
    override val number: Int
) : Base(number) {
    init {
        println("Derived init")
        println(number) // 200
    }
}