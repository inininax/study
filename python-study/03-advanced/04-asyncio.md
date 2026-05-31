# 04. asyncio와 비동기 프로그래밍

## 🎯 학습 목표
- 비동기 프로그래밍의 개념을 이해한다
- async/await 문법을 사용한다
- asyncio 의 핵심 API 를 안다
- 동기 vs 비동기 코드를 구별한다

## 1. 동기 vs 비동기

### 동기 (Synchronous)
```python
import requests
import time

def fetch(url):
    time.sleep(1)  # I/O 대기 (블록킹)
    return f"{url} done"

start = time.time()
for url in ["a.com", "b.com", "c.com"]:
    print(fetch(url))
print(f"동기: {time.time() - start:.2f}s")  # 약 3초
```

### 비동기 (Asynchronous)
```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)  # I/O 대기 (논블록킹)
    return f"{url} done"

async def main():
    results = await asyncio.gather(
        fetch("a.com"),
        fetch("b.com"),
        fetch("c.com"),
    )
    for r in results:
        print(r)

start = time.time()
asyncio.run(main())
print(f"비동기: {time.time() - start:.2f}s")  # 약 1초!
```

## 2. async / await 기본

### 2.1 코루틴 (Coroutine)
```python
async def my_function():
    return 42

# 직접 호출 시 코루틴 객체 반환 (실행 X)
result = my_function()
print(result)  # <coroutine object ...>

# 실행하려면 await 또는 asyncio.run
asyncio.run(my_function())
```

### 2.2 await
```python
async def say_hello():
    await asyncio.sleep(1)
    print("Hello!")

async def main():
    await say_hello()       # 코루틴 대기
    await say_hello()

asyncio.run(main())
```

> 💡 `await` 는 **코루틴 함수 안에서만** 사용 가능!

### 2.3 asyncio.run() — 진입점
```python
async def main():
    print("Hello, async!")

# 한 번만 호출 (이벤트 루프 시작/종료)
asyncio.run(main())
```

## 3. 태스크 (Task)

### 3.1 동시 실행
```python
async def task(name, delay):
    print(f"{name} 시작")
    await asyncio.sleep(delay)
    print(f"{name} 완료")
    return name

async def main():
    # ❌ 순차 실행 (5초)
    await task("A", 2)
    await task("B", 1)
    await task("C", 2)

    # ✅ 동시 실행 (2초)
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 2),
    )

asyncio.run(main())
```

### 3.2 asyncio.gather
```python
async def fetch(url):
    await asyncio.sleep(1)
    return f"data from {url}"

async def main():
    # 모든 결과 한 번에
    results = await asyncio.gather(
        fetch("a.com"),
        fetch("b.com"),
        fetch("c.com"),
        return_exceptions=True,  # 예외도 결과로
    )
    print(results)

asyncio.run(main())
```

### 3.3 asyncio.create_task
```python
async def main():
    # Task 생성 (즉시 스케줄)
    task1 = asyncio.create_task(fetch("a.com"))
    task2 = asyncio.create_task(fetch("b.com"))

    # 다른 작업 하다가
    print("작업 중...")
    await asyncio.sleep(0.5)

    # 결과 받기
    result1 = await task1
    result2 = await task2

asyncio.run(main())
```

### 3.4 TaskGroup (Python 3.11+)
```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch("a.com"))
        task2 = tg.create_task(fetch("b.com"))
    # 블록 종료 시 모든 task 완료 대기
    # 한 task 가 실패하면 다른 task 자동 취소

    print(task1.result(), task2.result())

asyncio.run(main())
```

## 4. asyncio 핵심 API

### 4.1 sleep & wait_for
```python
async def slow_task():
    await asyncio.sleep(5)
    return "완료"

async def main():
    try:
        # 3초 안에 완료 안 되면 TimeoutError
        result = await asyncio.wait_for(slow_task(), timeout=3)
    except asyncio.TimeoutError:
        print("시간 초과")

asyncio.run(main())
```

### 4.2 as_completed — 완료 순서대로
```python
async def fetch(name, delay):
    await asyncio.sleep(delay)
    return f"{name} done"

async def main():
    tasks = [
        fetch("A", 3),
        fetch("B", 1),
        fetch("C", 2),
    ]

    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"받음: {result}")
    # B done → C done → A done

asyncio.run(main())
```

### 4.3 wait — 더 세밀한 제어
```python
async def main():
    tasks = [asyncio.create_task(fetch(f"task-{i}", i)) for i in range(1, 5)]

    # FIRST_COMPLETED: 첫 완료 시 반환
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED,
        timeout=2,
    )

    for t in done:
        print(f"완료: {t.result()}")
    for t in pending:
        t.cancel()

asyncio.run(main())
```

### 4.4 shield — 취소 방지
```python
async def critical_task():
    await asyncio.sleep(10)
    return "중요한 결과"

async def main():
    # shield 로 감싸면 외부 cancel 에도 살아남음
    task = asyncio.shield(critical_task())
    try:
        result = await asyncio.wait_for(task, timeout=2)
    except asyncio.TimeoutError:
        pass  # critical_task 는 백그라운드 계속 실행
```

## 5. 비동기 컨텍스트 매니저

### 5.1 async with
```python
class AsyncResource:
    async def __aenter__(self):
        print("리소스 열기")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("리소스 닫기")
        await asyncio.sleep(0.1)

async def main():
    async with AsyncResource() as r:
        print("작업 중")

asyncio.run(main())
```

### 5.2 @asynccontextmanager
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def open_resource():
    print("열기")
    try:
        yield "resource"
    finally:
        print("닫기")

async def main():
    async with open_resource() as r:
        print(f"사용: {r}")
```

## 6. 비동기 이터레이터

### 6.1 async for
```python
class AsyncCounter:
    def __init__(self, max):
        self.max = max
        self.n = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.n >= self.max:
            raise StopAsyncIteration
        self.n += 1
        await asyncio.sleep(0.1)
        return self.n

async def main():
    async for n in AsyncCounter(5):
        print(n)
```

### 6.2 비동기 제너레이터
```python
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for i in async_range(5):
        print(i)
```

## 7. 동기 코드와의 통합

### 7.1 동기 함수 호출
```python
import asyncio

def blocking_io():
    # 동기 함수 (블록킹)
    import time
    time.sleep(1)
    return "done"

async def main():
    # 별도 스레드에서 실행
    result = await asyncio.to_thread(blocking_io)
    print(result)

asyncio.run(main())
```

### 7.2 run_in_executor
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

async def main():
    loop = asyncio.get_running_loop()

    # 스레드 풀 사용
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_io)

    # 프로세스 풀 사용
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_intensive)
```

## 8. aiohttp — 비동기 HTTP

```python
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        "https://example.com",
        "https://python.org",
        "https://github.com",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for url, content in zip(urls, results):
            print(f"{url}: {len(content)} bytes")

asyncio.run(main())
```

## 9. asyncio Queue

```python
import asyncio
import random

async def producer(queue, name):
    for i in range(5):
        item = f"{name}-{i}"
        await asyncio.sleep(random.random())
        await queue.put(item)
        print(f"생산: {item}")

async def consumer(queue, name):
    while True:
        item = await queue.get()
        print(f"{name} 소비: {item}")
        await asyncio.sleep(random.random())
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=10)

    producers = [asyncio.create_task(producer(queue, f"P{i}")) for i in range(2)]
    consumers = [asyncio.create_task(consumer(queue, f"C{i}")) for i in range(3)]

    await asyncio.gather(*producers)
    await queue.join()           # 모든 아이템 처리 대기

    for c in consumers:
        c.cancel()

asyncio.run(main())
```

## 10. 동기화 도구

```python
import asyncio

# Lock
lock = asyncio.Lock()
async def critical():
    async with lock:
        # critical section
        pass

# Event
event = asyncio.Event()
async def waiter():
    await event.wait()
    print("신호 받음")

async def notifier():
    await asyncio.sleep(2)
    event.set()

# Semaphore
sem = asyncio.Semaphore(3)
async def limited():
    async with sem:
        # 동시에 3개만 실행
        pass
```

## 11. asyncio vs threading vs multiprocessing

| 상황 | 추천 |
|------|------|
| 적은 수의 I/O 작업 | threading |
| 많은 수의 I/O 작업 (수백~수천) | **asyncio** ✅ |
| CPU 집약적 작업 | multiprocessing |
| 외부 동기 라이브러리만 있음 | threading |
| 비동기 라이브러리 가능 | asyncio |

```python
# 1000개 URL 동시 요청
# threading: 1000 스레드 = 메모리 부담
# asyncio: 효율적!

import asyncio
import aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        return await asyncio.gather(*tasks)

# 수천 개 URL도 빠르고 가볍게
```

## 12. 자주 하는 실수

### 12.1 동기 함수 호출
```python
# ❌ 이벤트 루프 블록!
async def bad():
    import time
    time.sleep(1)  # 블록킹

# ✅ asyncio.sleep
async def good():
    await asyncio.sleep(1)

# 또는 동기 함수가 필수면
async def with_blocking():
    await asyncio.to_thread(time.sleep, 1)
```

### 12.2 await 빠뜨림
```python
async def task():
    return 42

# ❌ 결과 안 받음 (워닝 발생)
async def bad():
    task()  # 코루틴 객체만 생성

# ✅
async def good():
    result = await task()
```

### 12.3 너무 많은 동시 작업
```python
# ❌ 메모리 문제 가능 (urls 가 100,000개 이상이라고 가정)
async def bad(urls):
    tasks = [fetch(url) for url in urls]
    await asyncio.gather(*tasks)

# ✅ Semaphore 로 제한
async def good(urls):
    sem = asyncio.Semaphore(100)

    async def bounded_fetch(url):
        async with sem:
            return await fetch(url)

    tasks = [bounded_fetch(url) for url in urls]
    await asyncio.gather(*tasks)
```

## 13. 실전 예제

### 예제 1: 비동기 웹 스크래퍼
```python
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as r:
        return await r.text()

async def parse_title(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.string if soup.title else ""

async def scrape(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        title = await parse_title(html)
        return url, title

async def main(urls):
    results = await asyncio.gather(*(scrape(url) for url in urls))
    for url, title in results:
        print(f"{url}: {title}")

# urls = [...]
# asyncio.run(main(urls))
```

### 예제 2: 비동기 채팅 서버
```python
import asyncio

clients = set()

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"연결: {addr}")
    clients.add(writer)
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            msg = data.decode().strip()
            broadcast = f"[{addr}] {msg}\n".encode()
            for c in clients:
                if c != writer:
                    c.write(broadcast)
                    await c.drain()
    finally:
        clients.remove(writer)
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)
    async with server:
        await server.serve_forever()

# asyncio.run(main())
```

## 📝 연습 문제

### 문제 1: 비동기 카운트다운
1초마다 숫자를 출력하는 비동기 카운트다운을 만들고, 여러 개 동시 실행하세요.

### 문제 2: URL 상태 체크 (비동기)
URL 리스트의 HTTP 상태를 asyncio + aiohttp 로 병렬 체크하세요.

### 문제 3: 비동기 큐 처리
생산자 2개, 소비자 3개가 asyncio.Queue 로 통신하는 프로그램을 작성하세요.

### 문제 4: 동시 실행 제한
asyncio.Semaphore 를 사용해 최대 10개씩만 동시 실행되도록 구현하세요.

### 문제 5: 타임아웃 처리
오래 걸리는 작업에 5초 타임아웃을 적용하고, 타임아웃 시 적절히 처리하세요.

## ✅ 체크리스트
- [ ] async/await 문법을 안다
- [ ] asyncio.run / gather / create_task 를 사용한다
- [ ] async for, async with 를 안다
- [ ] 동기 함수와 asyncio 의 통합 방법을 안다
- [ ] threading 과의 차이를 안다

## 🔗 다음 챕터
👉 [05. 타입 힌트와 정적 분석](./05-type-hints.md)
