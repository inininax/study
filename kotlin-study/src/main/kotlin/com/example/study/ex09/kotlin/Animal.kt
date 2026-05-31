package com.example.study.ex09.kotlin

abstract class Animal(
    protected val species: String,

    // 추상 프로퍼티가 아니라면 상속 받을 경우 open을 붙여줘야 한다.
    protected open val legCount: Int
) {
    abstract fun move()
}