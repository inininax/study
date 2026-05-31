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
        TODO("Not yet implemented")
    }
}