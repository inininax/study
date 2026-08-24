package study.coroutine

fun main() {
    printWithThread("main start") // ex: main @coroutine#1

//    ex01()
//    ex02()
//    ex02ThreadSleep()
//    ex02Sequence()
//    ex03()
//    ex03Cancel()
//    ex03Join()
//    ex03Async()
//    ex04Cancel1()
//    ex04Cancel2()
//    ex04CancellationException()
//    try {
//        ex05ThrowException()
//    } catch (e: Exception) {
//        printWithThread(e)
//    }
//    ex05SupervisorJob()
//    ex05ExceptionHandler()
//    try {
//        ex06LifeCycleCancelled()
//    } catch (e: Exception) {
//        printWithThread(e)
//    }

//    ex07CoroutineScope()
//    CoroutineScope(Dispatchers.Default).launch {
//        delay(1_000L)
//        printWithThread("job1")
//    }
//    Thread.sleep(1_500L)

//    CoroutineName("aiaiaiaiai") + Dispatchers.Default
//    ex07Executors()

//    ex08Suspend1()
//    ex08Suspend2()
//    ex08Calculate()

//    try {
//        ex08Timeout()
//    } catch (e: Exception) {
//        printWithThread(e)
//    }

//    try {
//        ex08TimeoutOrNull()
//    } catch (e: Exception) {
//        printWithThread(e)
//    }

    ex09Continuation()

    printWithThread("main end") // ex: main @coroutine#1
}

fun printWithThread(value: Any) {
    println("[${Thread.currentThread().name}] $value")
}