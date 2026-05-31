package study.coroutine

import kotlinx.coroutines.*

fun ex05ThrowException(): Nothing = runBlocking {
    val job1 = CoroutineScope(Dispatchers.Default).launch {
        printWithThread("Job 1")
        throw IllegalArgumentException()
    }

    val job2 = CoroutineScope(Dispatchers.Default).async {
        printWithThread("Job 2")
        throw IllegalArgumentException()
    }

    delay(1_000L)
    job2.await()
}

fun ex05SupervisorJob() = runBlocking {
//    val job = async { // 에러 전파
    val job = async(context = SupervisorJob()) { // 에러 전파하지 않음
        throw IllegalArgumentException()
    }
    delay(1_000L)
}

fun ex05ExceptionHandler() = runBlocking {
    val exceptionHandler = CoroutineExceptionHandler { _, _ ->
        printWithThread("예외!!")
    }

    val job = CoroutineScope(context = Dispatchers.Default).launch(context = exceptionHandler) {
        throw IllegalArgumentException()
    }

    delay(1_000L)
}
