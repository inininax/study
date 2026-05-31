package study.coroutine

import kotlinx.coroutines.*

fun ex04Cancel1() = runBlocking {
    val job1 = launch {
        delay(1_000L)
        printWithThread("Job 1") // cancel
    }

    launch {
        delay(1_000L)
        printWithThread("Job 2")
    }

    delay(100)
    job1.cancel()
}

fun ex04Cancel2() = runBlocking {
    val job = launch(Dispatchers.Default) {
        var i = 0
        var nextPrintTime = System.currentTimeMillis()
        while (i < 5) {
            if (nextPrintTime <= System.currentTimeMillis()) {
                printWithThread("${i++} 번째")
                nextPrintTime += 1_000L
            }

            if (!isActive) {
                throw CancellationException()
            }
        }
    }

    delay(100L)
    job.cancel()
}

fun ex04CancellationException() = runBlocking {
    val job = launch {
        try {
            printWithThread("try 1")
            delay(1_000L)
            printWithThread("try 2")
        } catch (e: CancellationException) {
            // nothing
        }
        printWithThread("취소 실패")
    }

    delay(100L)
    printWithThread("취소 시작")
    job.cancel()
}