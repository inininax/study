package com.example.study.ex03

fun main() {
    // is
    // !is
    // as?

    printAgeIfPerson(null)
    printAgeIfPerson(37)
    printAgeIfPerson(Person("", 37))

    printAgeIfPerson2(null)
    printAgeIfPerson2(37)
    printAgeIfPerson2(Person("", 37))
}

fun printAgeIfPerson(obj: Any?) {
    if (obj is Person) {
        /*val person = obj as? Person
        println(person.age)*/

        println(obj.age) // smart case
    }

    if (obj !is Person) {
        println("not is Person")
    }
}

fun printAgeIfPerson2(obj: Any?) {
    var person = obj as? Person
    println(person?.age)
}