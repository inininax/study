package com.example.study.ex03

import com.example.study.ex04.JavaMoney

fun main() {
    val money1 = JavaMoney(2_000L)
    val money2 = JavaMoney(1_000L)

    // 객체 비교 시 자동으로 compareTo를 호출
    if (money1 > money2) {
        println("money1 > money2")
    }

    val money3 = money2
    val money4 = JavaMoney(1_000L)

    if (money2 === money3) {
        println("money2 === money3")
    }
    if (money2 == money3) {
        println("money2 == money3")
    }
    if (money2 === money4) {
        println("money2 === money4") // X
    }
    if (money2 == money4) {
        println("money2 == money4")
    }

    // Lazy 연산
    if (fun1() || fun2()) {
        println("fun1() || fun2()")
    }

    println(money1 + money2)

    // in, !in

    // a..b
}

fun fun1(): Boolean {
    println("fun1")
    return true;
}

fun fun2(): Boolean {
    println("fun2")
    return false;
}