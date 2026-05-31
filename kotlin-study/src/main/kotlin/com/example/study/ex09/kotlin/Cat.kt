package com.example.study.ex09.kotlin

// extends 시 ":" 사용
class Cat(species: String) : Animal(species, 4) {

    override fun move() {
        println("kotlin 고양이")
    }

}