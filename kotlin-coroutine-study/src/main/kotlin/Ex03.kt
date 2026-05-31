package study.coroutine

import kotlinx.coroutines.*
import kotlin.system.measureTimeMillis

fun ex03() {
    runBlocking {
        printWithThread("03 start") // 1

        launch {
            delay(2_000L)
            printWithThread("03 launch end 2") // 3
        }

        val job1 = launch(start = CoroutineStart.LAZY) {
            delay(2_000L)
            printWithThread("03 launch end 1") // 2
        }
        job1.start()
    }
    printWithThread("03 end") // 4
}

fun ex03Cancel(): Unit = runBlocking {
    val job = launch {
        (1..5).forEach {
            printWithThread(it)
            delay(500L)
        }
    }

    delay(1_000L)
    job.cancel() // 1, 2 출력 후 종료
}

fun ex03Join(): Unit = runBlocking {
    val job1 = launch {
        delay(1_500L)
        printWithThread("job1") // 1
    }
    job1.join() // launch 완료 될때까지 대기 (sync) (async 사용 시에는 await)

    val job2 = launch {
        delay(1_000L)
        printWithThread("job2") // 2
    }
}

fun ex03Async() = runBlocking {
    val time = measureTimeMillis {
        val job1 = async(start = CoroutineStart.LAZY) { apiCall1() }
        val job2 = async(start = CoroutineStart.LAZY) { apiCall2() }
        job1.start()
        job2.start()
        printWithThread(job1.await() + job2.await()) // 3 or 2
    }
    printWithThread("소요 시간: $time ms")
}

suspend fun apiCall1(): Int {
    delay(2_000L)
    return 1
}

suspend fun apiCall2(): Int {
    delay(1_000L)
    return 2
}