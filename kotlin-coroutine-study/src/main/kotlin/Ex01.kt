package study.coroutine

import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.yield

fun ex01() = runBlocking {
    printWithThread("01 START") // 1
    launch {
        printWithThread("01 launch 1") // 2
        newRoutine()
        printWithThread("01 launch 2") // 5
    }
    yield()
    printWithThread("01 END") // 3
}

suspend fun newRoutine() {
    val num1 = 1
    val num2 = 2
    yield()
    printWithThread("01 launch newRoutine ${num1 + num2}") // 4
}
