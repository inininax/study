package study.coroutine

import kotlinx.coroutines.*
import java.util.concurrent.Executors

fun ex07CoroutineScope() = runBlocking {
    // coroutineScope로 감싸면 자식 launch가 끝날 때까지 블록이 대기한다
    coroutineScope {
        launch {
            printWithThread("Job 1")
            delay(1_000L)
            printWithThread("Job 2") // 이제 반드시 출력됨
        }
    }
//    val job1 = CoroutineScope(Dispatchers.Default).launch { // 구버전: 별도 스코프라 대기 없음 → Job 2 미출력
//        printWithThread("Job 1")
//        delay(1_000L)
//        printWithThread("Job 2")
//    }
}

fun ex07Executors() = runBlocking {
    val threadPool = Executors.newSingleThreadExecutor()
    val launch = CoroutineScope(threadPool.asCoroutineDispatcher()).launch {
        printWithThread("새로운 코루틴")
    }
    launch.join() // 코루틴 종료를 기다린 뒤 shutdown (종료 전 shutdown하면 작업이 거부될 수 있다)
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