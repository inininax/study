package com.example.study.ex09

import com.example.study.ex09.java.JavaPerson

fun main() {
    val person = Person("A", 1)
    println("name: ${person.name}, age: ${person.age}")

    person.age = 10 // setter
    println("name: ${person.name}, age: ${person.age}")

    // Java Class도 "." 사용 가능
    val javaPerson = JavaPerson("JAVA", 100)
    println("name: ${javaPerson.name}, age: ${javaPerson.age}")

    javaPerson.age = 200
    println("name: ${javaPerson.name}, age: ${javaPerson.age}")

    val person2 = Person("2 constructor")
    println("name: ${person2.name}, age: ${person2.age}")

    val person3 = Person()
    /*
        init
        2번째 constructor
        3번째 constructor
    */
    println("name: ${person3.name}, age: ${person3.age}")
}

/*
class Person constructor(name: String, age: Int) {
    val name = name
    val age = age
}

// constructor 생략
class Person(name: String, age: Int) {
    val name = name
    val age = age
}

// 필드선언 생략 가능
class Person(
    val name: String,
    var age: Int
)

class Person(
    val name: String,
    var age: Int
) {
    init {
        if (age <= 0) {
            throw IllegalArgumentException("Invalid age")
        }
        println("init") // 1
    }

    constructor(name: String) : this(name, 1) {
        println("2번째 constructor") // 2
    }

    // 3번째 constructor
    constructor() : this("Test") {
        println("3번째 constructor") // 3
    }
}
*/

class Person(
    name2: String = "Test",
    var age: Int = 10
) {
    // custom getter
    var name = name2
        set(value) {
            field = value.uppercase()
        }
        get() = field.uppercase() // backing field

    init {
        if (age <= 0) {
            throw IllegalArgumentException("Invalid age")
        }
    }

    /*
    // function 으로 정의
    fun isAdult(): Boolean {
        return this.age >= 20
    }

    // custom getter 정의
    val isAdult2: Boolean
        get() {
            return this.age >= 20
        }
    */
    val isAdult: Boolean
        get() = this.age >= 20
}