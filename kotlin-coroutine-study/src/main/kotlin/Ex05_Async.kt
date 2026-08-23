package study.coroutine

import kotlinx.coroutines.*

fun ex05ThrowException(): Nothing = runBlocking {
    // CoroutineScope(...).launch 대신 coroutineScope로 감싸면
    // job1/job2가 runBlocking의 "자식"이 되어 예외 전파와 완료 대기가 정상 동작한다
    coroutineScope {
        val job1 = launch {
            printWithThread("Job 1")
            throw IllegalArgumentException()
        }

        val job2 = async {
            printWithThread("Job 2")
            throw IllegalArgumentException()
        }

        delay(1_000L)
        job2.await()
    }
}

fun ex05SupervisorJob() = runBlocking {
//    val job = async { // 에러 전파
    // SupervisorJob을 루트로 하는 별도 스코프 — 자식 실패가 다른 자식/부모로 전파되지 않음
    val scope = CoroutineScope(SupervisorJob()) // 에러 전파하지 않음
    val job = scope.async {
        throw IllegalArgumentException()
    }
    delay(1_000L)
    scope.cancel() // SupervisorJob은 부모가 없어 자동 종료되지 않으므로 직접 취소해야 누수가 없다
}

fun ex05ExceptionHandler() = runBlocking {
    val exceptionHandler = CoroutineExceptionHandler { _, _ ->
        printWithThread("예외!!")
    }

    // CoroutineScope(...) 대신 runBlocking의 자식으로 launch + join()으로 완료 대기
    // 주의: CoroutineExceptionHandler는 루트 코루틴에서만 동작하므로,
    //       자식인 경우 핸들러는 무시되고 예외가 부모(runBlocking)로 전파된다
    val job = launch(context = Dispatchers.Default + exceptionHandler) {
        throw IllegalArgumentException()
    }

    job.join()
}
