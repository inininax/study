package com.example.study

fun main(args: Array<String>) {
    println("hello kotlin")

    // ?: Elvis 연산자
    // ?. Safe call

    val str: String? = "ABC"
    println(str?.length ?: 0)

    println(startWith("A"))
}

fun startWithA1(str: String?): Boolean {
    /*if (str == null) {
        throw IllegalArgumentException("str is null")
    }
    return str.startsWith("A")*/

    return str?.startsWith("A") ?: throw IllegalArgumentException("str is null")
}

fun startWithA2(str: String?): Boolean? {
    /*if (str == null) {
        return null
    }
    return str.startsWith("A")*/

    return str?.startsWith("A")
}

fun startWithA3(str: String?): Boolean {
    /*if (str == null) {
        return false
    }
    return str.startsWith("A")*/

    return str?.startsWith("A") ?: false
}

fun startWithA4(str: String): Boolean {
    return str.startsWith("A")
}

fun startWith(str: String?): Boolean {
    return str!!.startsWith("A") // null 아님 단언!!
}