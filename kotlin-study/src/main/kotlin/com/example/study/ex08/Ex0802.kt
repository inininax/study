package com.example.study.ex08

fun main() {
    request("A")
    request("B", 2)
    request("C", 4, false)
    println()

    // Kotlin에서 Java 함수를 사용할 때는 named argument 사용 불가
    request("D", useNewLine = false)
}

fun request(
    str: String,
    num: Int = 3,
    useNewLine: Boolean = true
) {
    for (i in 1..num) {
        if (useNewLine) {
            println(str)
        } else {
            print(str)
        }
    }
}