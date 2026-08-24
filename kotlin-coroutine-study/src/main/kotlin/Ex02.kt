package study.coroutine

import kotlinx.coroutines.*
import kotlin.system.measureTimeMillis

// Ex02: suspend 함수와 delay - 스레드를 점유하지 않는 비동기 대기와 순차 실행

fun ex02() = runBlocking {
    printWithThread("02 START") // 1

    launch {
        printWithThread("02 launch start") // 2
        delay(1_000L) // Thread.sleep 과 달리 스레드를 점유하지 않고 코루틴만 일시 중단된다
        printWithThread("02 launch end") // 4
    }

    delay(500L)
    printWithThread("02 END") // 3 (delay 동안 메인 스레드는 다른 일을 할 수 있다)
}

fun ex02ThreadSleep() = runBlocking {
    // Thread.sleep 은 스레드 자체를 잠근다 - runBlocking 의 유일한 스레드가 막혀
    // 두 작업이 사실상 순차적으로 실행된다
    val time = measureTimeMillis {
        val job1 = launch {
            Thread.sleep(1_000L) // 블로킹
        }
        val job2 = launch {
            Thread.sleep(1_000L) // job1 이 끝난 뒤에야 실행됨
        }
        job1.join()
        job2.join()
    }
    printWithThread("02 Thread.sleep 소요 시간: ${time}ms") // 약 2000ms

    // delay 는 스레드를 놓아주므로 두 launch 가 병렬로 대기한다
    val time2 = measureTimeMillis {
        val job1 = launch {
            delay(1_000L)
        }
        val job2 = launch {
            delay(1_000L)
        }
        job1.join()
        job2.join()
    }
    printWithThread("02 delay 소요 시간: ${time2}ms") // 약 1000ms
}

fun ex02Sequence() = runBlocking {
    // suspend 함수는 호출한 곳에서 결과를 기다린다 (순차 실행)
    val time = measureTimeMillis {
        val one = fetchOne()
        val result = process(one)
        printWithThread("02 순차 결과: $result")
    }
    printWithThread("02 순차 소요 시간: ${time}ms") // 각 delay 의 합 (약 2000ms)
}

suspend fun fetchOne(): Int {
    delay(1_000L)
    return 10
}

suspend fun process(num: Int): Int {
    delay(1_000L)
    return num * 2
}
