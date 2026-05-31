package study.coroutine

import kotlinx.coroutines.*
import kotlinx.coroutines.future.await
import java.util.concurrent.CompletableFuture

fun ex08Suspend1() = runBlocking {
    val result1: Deferred<Int> = async {
        deferredCall1()
    }

    val result2 = async {
        deferredCall2(result1.await())
    }

    printWithThread(result2.await())
}

fun deferredCall1(): Int {
    Thread.sleep(1_000L)
    return 100
}

fun deferredCall2(num: Int): Int {
    Thread.sleep(1_000L)
    return num * 2
}

//

fun ex08Suspend2() = runBlocking {
    val result1: Int = call1()
    val result2: Int = call2(result1)
    printWithThread(result2)
}

suspend fun call1(): Int {
    return CoroutineScope(Dispatchers.Default).async {
        Thread.sleep(1_000L)
        100
    }.await()
}

suspend fun call2(num: Int): Int {
    return CompletableFuture.supplyAsync {
        Thread.sleep(1_000L)
        num * 2
    }.await()
}

//

fun ex08Calculate() = runBlocking {
    printWithThread("08 START")
    printWithThread(calculateResult())
    printWithThread("08 END")
}

//suspend fun calculateResult(): Int = coroutineScope {
suspend fun calculateResult(): Int = withContext(Dispatchers.Default) {
    val num1 = async {
        delay(1_000L)
        10
    }
    val num2 = async {
        delay(1_000L)
        20
    }
    num1.await() + num2.await()
}

//

fun ex08Timeout() = runBlocking {
    val result = withTimeout(1_000L) {
        delay(1_500L)
        10 + 20
    }
    printWithThread(result)
}

//

fun ex08TimeoutOrNull() = runBlocking {
    val result = withTimeoutOrNull(1_000L) {
        delay(1_500L)
        10 + 20
    }
    printWithThread(result ?: " null")
}