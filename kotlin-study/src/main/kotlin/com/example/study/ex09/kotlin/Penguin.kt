package com.example.study.ex09.kotlin

class Penguin(
    species: String
) : Animal(species, 2), Swimable, Flyable {

    private val wingCount: Int = 2

    override fun move() {
        println("kotlin penguin")
    }

    // super class property에 open keyword 필요
    override val legCount: Int
        get() = super.legCount + this.wingCount

    override fun act() {
        super<Swimable>.act();
        super<Flyable>.act();
    }

    override fun fly() {
        // 펭귄은 날 수 없다 - Flyable 의 구현 의무만 채우고 no-op 로 안전하게 처리
        // (TODO() 로 두면 호출 시점에 NotImplementedError 발생)
        println("펭귄은 날 수 없습니다")
    }
}