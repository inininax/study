# Coroutine study

## 루틴 vs 코루틴
- 진입, 종료 / 진입, 중단, 재개, 종료
- 지역변수 스택 메모리 초기화 / 스위칭 
- 디버깅 VM options
```text
-Dkotlinx.coroutines.debug
```

## 스레드 vs 코루틴
- 코루틴의 코드가 실행되려면 스레드가 필요
- 코루틴의 코드가 스레드에 배정
- process context switching
  - heap area (stack1, 2...) 통째로 교체
- thread context switching
  - 동일한 process 내에서 heap area 공유
  - thread는 각각의 stack area 보유
  - stack memory만 교체하여 비용이 적음
- 하나의 쓰레드로 동시성 확보
- 한 코루틴의 코드가 여러 스레드에서 실행 가능
- coroutine context switching
  - coroutine이 thread에 배정 시
  - 동일한 thread 일 경우 heap / stack을 모두 공유하여
  - thread context switching 보다 비용이 적음

## 코루틴 빌더와 Job
- runBlocking
- launch
  - start
  - cancel
  - join: 완료 될때까지 대기 (sync)
- async
  - start
  - await, CoroutineStart.LAZY 사용 시 결과 대기

## 코루틴 취소
- delay, yield 같은 kotlinx.coroutines 패키지의 suspend 사용
- CancellationException
```kotlin
public actual typealias CancellationException = java.util.concurrent.CancellationException
```

- isActive를 통해 상태 체크
- 코루틴을 다른 스레드에 배정하도록취소
  CoroutineContext를 Dispatchers.Default와 같이 지정하여 취소

```kotlin
public fun CoroutineScope.launch(
    context: CoroutineContext = EmptyCoroutineContext,
    start: CoroutineStart = CoroutineStart.DEFAULT,
    block: suspend CoroutineScope.() -> Unit
): Job {
    val newContext = newCoroutineContext(context)
    val coroutine = if (start.isLazy)
        LazyStandaloneCoroutine(newContext, block) else
        StandaloneCoroutine(newContext, active = true)
    coroutine.start(start, coroutine, block)
    return coroutine
}

public fun <T> CoroutineScope.async(
  context: CoroutineContext = EmptyCoroutineContext,
  start: CoroutineStart = CoroutineStart.DEFAULT,
  block: suspend CoroutineScope.() -> T
): Deferred<T> {
  val newContext = newCoroutineContext(context)
  val coroutine = if (start.isLazy)
    LazyDeferredCoroutine(newContext, block) else
    DeferredCoroutine<T>(newContext, active = true)
  coroutine.start(start, coroutine, block)
  return coroutine
}

public suspend fun delay(timeMillis: Long) {
  if (timeMillis <= 0) return // don't delay
  return suspendCancellableCoroutine sc@ { cont: CancellableContinuation<Unit> ->
    if (timeMillis < Long.MAX_VALUE) {
      cont.context.delay.scheduleResumeAfterDelay(timeMillis, cont)
    }
  }
}

public suspend fun yield(): Unit = suspendCoroutineUninterceptedOrReturn sc@ { uCont ->
  val context = uCont.context
  context.ensureActive()
  val cont = uCont.intercepted() as? DispatchedContinuation<Unit> ?: return@sc Unit
  if (cont.dispatcher.isDispatchNeeded(context)) {
    cont.dispatchYield(context, Unit)
  } else {
    val yieldContext = YieldContext()
    cont.dispatchYield(context + yieldContext, Unit)
    if (yieldContext.dispatcherWasUnconfined) {
      return@sc if (cont.yieldUndispatched()) COROUTINE_SUSPENDED else Unit
    }
  }
  COROUTINE_SUSPENDED
}
```

## 코루틴의 예외 처리와 Job의 상태 변경
- 자식 코루틴의 예외는 부모 코루틴에게 전달
- root 코루틴 상생 CoroutineScope(Dispatchers.Default).launch
- 전파 하지 않음 SupervisorJob()
- CoroutineExceptionHandler, 부모 코루틴 존재 시 동작 안함, launch에만 적용 가능
```kotlin
    val exceptionHandler = CoroutineExceptionHandler { _, _ ->
        printWithThread("예외!!")
    }
```

## Structured concurrency
- 코루틴 Life sycle
  - new > active > completing > completed
  - ________ cancelling > cancelled
- 자식 코루틴이 여러개일 경우 기다리다 예외 발생 처리를 위해
  completing, completed 2단계 구분
- 자식 코루틴 중 예외가 발생 시 부모 코루틴에 예외 전파 > 부모 코루틴 취소

## CoroutineScope, CoroutineContext
- CoroutineScope(Dispatchers.Default)
- launch, async는 CoroutineScope의 확장함수
- runBlocking이 CoroutineScope을 제공
  - CoroutineScope을 직접 만들면 runBlocking일 필요하지 않음
- CoroutineScope의 주요 역할은 CoroutineContext에 데이터를 보관
- CoroutineContext란
  - CoroutineExceptionHandler
  - Coroutine Dispatchers
  - Coroutine Name
  - Coroutine과 관련된 데이터를 보관
- Coroutine Structured Concurrency 기반에 따라 자식 코루틴 생성 시 부모 Context를 copy해 내용을 덮어쓴다.
- Dispatchers
  - Coroutine이 어떤 Thread에 배정될지 관리 
  - Dispatchers.Default
    - CPU 자원을 많이 쓸 때 권장
  - Dispatchers.IO
    - I/O 작업에 최적화된 디스패처
  - Dispatchers.Main
    - 일반적으로 UI 컴퍼넌트를 조작하기 위해 사용
  - ExecutorService를 Dispatchers로 변환
    - asCoroutineDispatcher() 확장함수 활용

## Suspending function
- suspend 키워드가 붙은 다름 함수 호출
- 정지 / 중지 / 유예
- 코루틴이 중지되었다가 재개될 수 있다. (와우...yeild냐?) suspension point
- 제어권을 넘길 수 있기 때문에 비동기 처리 시 편의
- 추가적인 suspend function
  - coroutineScope
  - withContext
  - withTimeout
  - withTimeoutOrNull

## Continuation
- continuation 구현 예시 소스 참고
- Continuation Interface
```kotlin
public interface Continuation<in T> {
  public val context: CoroutineContext
  public fun resumeWith(result: Result<T>)
}

@InlineOnly
public inline fun <T> Continuation(
    context: CoroutineContext,
    crossinline resumeWith: (Result<T>) -> Unit
): Continuation<T> =
    object : Continuation<T> {
        override val context: CoroutineContext
            get() = context

        override fun resumeWith(result: Result<T>) =
            resumeWith(result)
    }
```

## 활용
- callback hell 해결
- 비동기 non-blocking 또는 동시성 처리 시
- Asynchronous UI