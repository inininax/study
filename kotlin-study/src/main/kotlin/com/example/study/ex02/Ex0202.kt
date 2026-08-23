package com.example.study.ex02

fun main() {
//    val person = Person("kotlin을 공부하고 있어요.")
//    println(startWithA(person.name)) // name이 null이면 NPE 발생 (원래 예제)
    val person = Person(null)
    println(startWithA(person.name)) // null-safe: null이면 false 반환
}

fun startWithA(str: String?): Boolean { // nullable 파라미터 허용
    return str?.startsWith("A") ?: false
}
