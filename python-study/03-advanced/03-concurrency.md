# 03. 동시성 (Threading & Multiprocessing)

## 🎯 학습 목표
- threading, multiprocessing, asyncio 의 차이를 안다
- GIL(Global Interpreter Lock)을 이해한다
- 적절한 동시성 모델을 선택할 수 있다
- 동기화 도구를 사용한다

## 1. 동시성 모델 비교

| 모델 | 적합한 작업 | 메모리 | 데이터 공유 |
|------|------------|--------|------------|
| threading | I/O bound | 공유 | 쉬움 |
| multiprocessing | CPU bound | 분리 | 어려움 (IPC) |
| asyncio | 많은 I/O | 단일 스레드 | 쉬움 |

### GIL (Global Interpreter Lock)
- CPython의 한계: 한 번에 **한 스레드만 Python 바이트코드 실행**
- I/O 작업 시에는 GIL 해제 → threading 유용
- CPU 작업은 multiprocessing 사용
- (Python 3.13+ free-threaded 모드 실험적 지원)

## 2. threading 모듈

### 2.1 기본 사용
```python
import threading
import time

def worker(name, delay):
    print(f"{name} 시작")
    time.sleep(delay)
    print(f"{name} 완료")

# Thread 객체 생성
t1 = threading.Thread(target=worker, args=("Worker-1", 2))
t2 = threading.Thread(target=worker, args=("Worker-2", 1))

# 시작
t1.start()
t2.start()

# 완료 대기
t1.join()
t2.join()

print("모두 완료")
```

### 2.2 클래스로 만들기
```python
class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(f"{self.name} 실행 중")
        time.sleep(1)
        print(f"{self.name} 완료")

t = MyThread("Thread-1")
t.start()
t.join()
```

### 2.3 데몬 스레드
메인 프로그램 종료 시 함께 종료되는 스레드.

```python
def background_task():
    while True:
        print("작업 중...")
        time.sleep(1)

t = threading.Thread(target=background_task, daemon=True)
t.start()

time.sleep(3)
print("메인 종료")
# 메인 종료 시 데몬도 함께 종료
```

## 3. 동기화 (Synchronization)

### 3.1 Lock — 상호 배제
```python
counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:               # critical section
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # 500000 (Lock 없으면 더 작은 값)
```

### 3.2 RLock — 재진입 가능
같은 스레드에서 여러 번 획득 가능.

```python
rlock = threading.RLock()

def func1():
    with rlock:
        func2()  # 같은 lock 다시 획득 가능

def func2():
    with rlock:
        print("inside func2")
```

### 3.3 Semaphore — 동시 접근 제한
```python
sem = threading.Semaphore(3)  # 최대 3개

def worker(n):
    with sem:
        print(f"Worker {n} 작업 중")
        time.sleep(1)

threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for t in threads: t.start()
for t in threads: t.join()
# 한 번에 3개씩만 실행됨
```

### 3.4 Event — 신호
```python
event = threading.Event()

def waiter():
    print("대기 중...")
    event.wait()
    print("신호 받음!")

def notifier():
    time.sleep(2)
    print("신호 보냄")
    event.set()

t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=notifier)
t1.start(); t2.start()
t1.join(); t2.join()
```

### 3.5 Condition — 조건 변수
```python
condition = threading.Condition()
items = []

def producer():
    for i in range(5):
        with condition:
            items.append(i)
            print(f"생산: {i}")
            condition.notify()       # 대기 중인 소비자 깨움
        time.sleep(0.5)

def consumer():
    while True:
        with condition:
            while not items:
                condition.wait()    # 데이터 올 때까지 대기
            item = items.pop(0)
            print(f"소비: {item}")
        if item == 4:
            break

threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
```

### 3.6 Queue — 스레드 안전 큐
```python
from queue import Queue

q = Queue(maxsize=10)

def producer():
    for i in range(5):
        q.put(i)
        print(f"생산: {i}")

def consumer():
    while True:
        item = q.get()
        print(f"소비: {item}")
        q.task_done()
        if item == 4:
            break

threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
q.join()  # 모든 작업 완료 대기
```

## 4. ThreadPoolExecutor — 권장 방식

`concurrent.futures` 모듈의 추상화. 더 사용하기 쉽습니다.

### 4.1 기본
```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_url(url):
    print(f"가져오는 중: {url}")
    time.sleep(1)
    return f"{url} done"

urls = [f"http://site{i}.com" for i in range(5)]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(fetch_url, urls)
    for r in results:
        print(r)
```

### 4.2 submit & Future
```python
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(fetch_url, url) for url in urls]

    for future in futures:
        try:
            result = future.result(timeout=5)
            print(result)
        except Exception as e:
            print(f"실패: {e}")
```

### 4.3 as_completed — 완료 순서대로
```python
from concurrent.futures import as_completed

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}

    for future in as_completed(futures):
        url = futures[future]
        try:
            print(f"{url}: {future.result()}")
        except Exception as e:
            print(f"{url} 실패: {e}")
```

## 5. multiprocessing — CPU 작업

### 5.1 기본 Process
```python
from multiprocessing import Process
import os

def worker(name):
    print(f"{name} (PID: {os.getpid()})")

if __name__ == "__main__":  # 중요!
    processes = []
    for i in range(3):
        p = Process(target=worker, args=(f"Worker-{i}",))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
```

> ⚠️ Windows/macOS에서 `if __name__ == "__main__":` 필수!

### 5.2 ProcessPoolExecutor
```python
from concurrent.futures import ProcessPoolExecutor
import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    numbers = [10**9 + i for i in range(20)]

    with ProcessPoolExecutor() as executor:
        results = executor.map(is_prime, numbers)
        for n, prime in zip(numbers, results):
            print(f"{n}: {prime}")
```

### 5.3 Pool — 더 많은 메서드
```python
from multiprocessing import Pool

def square(x):
    return x ** 2

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        # map
        results = pool.map(square, range(10))

        # imap (제너레이터, 메모리 효율적)
        for r in pool.imap(square, range(10)):
            print(r)

        # apply_async (비동기)
        result = pool.apply_async(square, (5,))
        print(result.get())     # 25
```

### 5.4 프로세스 간 데이터 공유
프로세스는 메모리가 분리되어 있어 직접 공유 불가.

```python
from multiprocessing import Process, Queue, Value, Array, Manager

# Queue (안전)
def producer(q):
    for i in range(5):
        q.put(i)

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(item)

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    p1.start(); p2.start()
    p1.join()
    q.put(None)
    p2.join()

# Shared memory (Value, Array)
def increment(counter):
    for _ in range(1000):
        with counter.get_lock():
            counter.value += 1

if __name__ == "__main__":
    counter = Value("i", 0)  # int
    processes = [Process(target=increment, args=(counter,)) for _ in range(5)]
    for p in processes: p.start()
    for p in processes: p.join()
    print(counter.value)

# Manager (Python 객체 공유)
if __name__ == "__main__":
    with Manager() as manager:
        shared_list = manager.list()
        shared_dict = manager.dict()
        # 여러 프로세스에서 접근 가능
```

## 6. threading vs multiprocessing 선택

```python
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# I/O bound (네트워크, 파일)
def io_task(n):
    time.sleep(1)
    return n

# CPU bound (계산)
def cpu_task(n):
    return sum(i ** 2 for i in range(n))

# I/O bound → ThreadPoolExecutor 추천
with ThreadPoolExecutor() as executor:
    results = list(executor.map(io_task, range(10)))

# CPU bound → ProcessPoolExecutor 추천
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_task, [10**6] * 10))
```

## 7. 동시성 패턴

### 7.1 생산자-소비자
```python
from queue import Queue
import threading
import time

def producer(q, n):
    for i in range(n):
        item = f"item-{i}"
        q.put(item)
        print(f"생산: {item}")
        time.sleep(0.1)
    q.put(None)  # 종료 신호

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"소비: {item}")
        time.sleep(0.2)
        q.task_done()

q = Queue()
t_prod = threading.Thread(target=producer, args=(q, 10))
t_cons = threading.Thread(target=consumer, args=(q,))
t_prod.start(); t_cons.start()
t_prod.join(); t_cons.join()
```

### 7.2 Worker Pool
```python
from queue import Queue
import threading

def worker(q, worker_id):
    while True:
        task = q.get()
        if task is None:
            break
        print(f"Worker {worker_id}: {task}")
        q.task_done()

q = Queue()
workers = []
for i in range(4):
    t = threading.Thread(target=worker, args=(q, i))
    t.start()
    workers.append(t)

# 작업 추가
for i in range(20):
    q.put(f"task-{i}")

q.join()  # 모든 작업 완료 대기

# 종료
for _ in workers:
    q.put(None)
for t in workers:
    t.join()
```

### 7.3 Fan-out / Fan-in
```python
from concurrent.futures import ThreadPoolExecutor

def process_chunk(chunk):
    return sum(chunk)

def parallel_sum(data, chunk_size=1000):
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    with ThreadPoolExecutor() as executor:
        partials = list(executor.map(process_chunk, chunks))

    return sum(partials)

result = parallel_sum(list(range(100000)))
```

## 8. 주의사항

### 8.1 GIL 의 함정
```python
# Python threading 으로는 CPU 작업 가속 안 됨
import time
from concurrent.futures import ThreadPoolExecutor

def cpu_intensive(n):
    return sum(i ** 2 for i in range(n))

# 단일 스레드
start = time.time()
for _ in range(4):
    cpu_intensive(10**7)
print(f"단일: {time.time() - start:.2f}s")

# 스레드 (GIL 때문에 별로 안 빨라짐)
start = time.time()
with ThreadPoolExecutor(max_workers=4) as executor:
    list(executor.map(cpu_intensive, [10**7] * 4))
print(f"스레드: {time.time() - start:.2f}s")

# 프로세스 (진짜 빠름)
from concurrent.futures import ProcessPoolExecutor
if __name__ == "__main__":
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_intensive, [10**7] * 4))
    print(f"프로세스: {time.time() - start:.2f}s")
```

### 8.2 Race Condition
```python
# ❌ 위험
counter = 0
def unsafe_increment():
    global counter
    for _ in range(100000):
        counter += 1   # 원자적이지 않음!

# ✅ 안전
lock = threading.Lock()
def safe_increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1
```

### 8.3 Deadlock
```python
# ❌ 데드락 위험: 두 lock 을 다른 순서로 획득
lock1 = threading.Lock()
lock2 = threading.Lock()

def func_a():
    with lock1:
        time.sleep(0.1)
        with lock2:  # B가 lock2를 들고 있으면 대기
            pass

def func_b():
    with lock2:
        time.sleep(0.1)
        with lock1:  # A가 lock1을 들고 있으면 대기
            pass

# ✅ 항상 같은 순서로 획득
```

## 9. 실전 예제

### 예제 1: 병렬 다운로더
```python
from concurrent.futures import ThreadPoolExecutor
import requests
from pathlib import Path

def download(url, dest):
    print(f"다운로드: {url}")
    resp = requests.get(url, timeout=10)
    Path(dest).write_bytes(resp.content)
    return dest

urls = [
    ("https://example.com/file1.zip", "file1.zip"),
    ("https://example.com/file2.zip", "file2.zip"),
    ("https://example.com/file3.zip", "file3.zip"),
]

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(download, url, dest) for url, dest in urls]
    for f in futures:
        try:
            print(f"완료: {f.result()}")
        except Exception as e:
            print(f"실패: {e}")
```

### 예제 2: 멀티프로세싱 데이터 처리
```python
from multiprocessing import Pool
import math

def process_data(item):
    # CPU 집약적 작업
    return sum(math.sqrt(i) for i in range(item))

if __name__ == "__main__":
    data = [10**5] * 8
    with Pool() as pool:
        results = pool.map(process_data, data)
    print(f"합계: {sum(results):.2f}")
```

## 📝 연습 문제

### 문제 1: 병렬 카운터
스레드 5개로 각각 1000번 카운터를 증가시키는 프로그램을 작성하세요. Lock 사용 전후 결과 비교.

### 문제 2: URL 상태 확인
URL 리스트의 HTTP 상태를 ThreadPoolExecutor 로 병렬 확인하세요.

### 문제 3: 소수 카운트 (multiprocessing)
1부터 10,000,000 까지 소수의 개수를 4개 프로세스로 병렬 계산하세요.

### 문제 4: 생산자-소비자
3개의 생산자와 2개의 소비자가 Queue 로 통신하는 프로그램을 작성하세요.

### 문제 5: 데드락 시뮬레이션
2개의 lock 을 이용해 데드락 상황을 만들고, 해결하세요.

## ✅ 체크리스트
- [ ] GIL 의 영향을 이해한다
- [ ] threading 과 multiprocessing 의 차이를 안다
- [ ] Lock 으로 동기화한다
- [ ] ThreadPoolExecutor / ProcessPoolExecutor 를 사용한다
- [ ] Queue 로 데이터를 전달한다

## 🔗 다음 챕터
👉 [04. asyncio와 비동기 프로그래밍](./04-asyncio.md)
