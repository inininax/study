package com.example.study.ex03

fun main() {
    val person = Person("코틀린", 12)
    val name = "코틀린2"
    println("이름: ${person.name}, 이름2: $name")

    val withoutIndent =
        """
            ABC
            EFG
        """.trimIndent()
    println(withoutIndent)

    val str = "ABC"
    println(str[2])
}