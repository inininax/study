package study.coroutine

import kotlinx.coroutines.*
import java.util.concurrent.Executors

fun ex07CoroutineScope() = runBlocking {
    val job1 = CoroutineScope(Dispatchers.Default).launch {
        printWithThread("Job 1")
        delay(1_000L)
        printWithThread("Job 2") // scope을 생성했기 때문에 호출 부분에서 대기하지 않으면 출력되지 않음
    }
}

fun ex07Executors() {
    val threadPool = Executors.newSingleThreadExecutor()
    val launch = CoroutineScope(threadPool.asCoroutineDispatcher()).launch {
        printWithThread("새로운 코루틴")
    }
    threadPool.shutdown()
}

class AsyncLogin {
    private val scope = CoroutineScope(Dispatchers.Default)

    fun doSomething() {
        scope.launch {
            // 무언가 코루틴이 시작
        }
    }

    fun destroy() {
        scope.cancel()
    }
}