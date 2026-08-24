"""
고급 연습 문제 — 정답 예시

먼저 스스로 풀어본 후 참고하세요!

실행: python3 solutions.py  (표준 라이브러리만 사용, 외부 의존성 없음)
참고: 네트워크 문제는 외부 연결 없이 data: URI 로 검증합니다.
"""

import asyncio
import concurrent.futures
import cProfile
import gc
import html.parser
import importlib
import io
import json
import math
import multiprocessing
import pstats
import queue
import sqlite3
import statistics
import sys
import tempfile
import threading
import time
import tracemalloc
import urllib.parse
import urllib.request
from collections import OrderedDict
from contextlib import redirect_stdout
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Generic, Optional, Protocol, TypeVar
from unittest.mock import patch


# ════════════════════════════════════════════════
# 01. 데코레이터
# ════════════════════════════════════════════════

# === 문제 1.1: @timer ===
def timer(func: Callable) -> Callable:
    """실행 시간을 측정해 wrapper.last_elapsed 에 저장하는 데코레이터."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 핵심 아이디어: time.perf_counter 는 고해상도 시간 측정에 표준
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper.last_elapsed = time.perf_counter() - start
        return result

    wrapper.last_elapsed = 0.0
    return wrapper


# === 문제 1.2: @log ===
def log(func: Callable) -> Callable:
    """호출 인자와 반환값을 stdout 으로 로깅."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[log] 호출 {func.__name__} args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[log] 반환 {func.__name__} -> {result!r}")
        return result

    return wrapper


# === 문제 1.3: @cache (직접 구현) ===
def cache(func: Callable) -> Callable:
    """결과 캐싱 + 히트/미스 통계 제공 (functools.lru_cache 미사용)."""

    memo: dict[tuple, Any] = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in memo:
            wrapper.cache_hits += 1
            return memo[key]
        wrapper.cache_misses += 1
        result = func(*args, **kwargs)
        memo[key] = result
        return result

    wrapper.cache_hits = 0
    wrapper.cache_misses = 0
    wrapper.clear_cache = memo.clear
    return wrapper


# === 문제 1.4: @validate ===
def validate_ints(func: Callable) -> Callable:
    """모든 위치 인자가 정수인지 검증 (bool 은 정수의 자식이므로 거부)."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in (*args, *kwargs.values()):
            # 핵심 아이디어: bool 도 int 의 하위 클래스 — 명시적으로 배제
            if not isinstance(arg, int) or isinstance(arg, bool):
                raise TypeError(f"정수만 허용: {arg!r}")
        return func(*args, **kwargs)

    return wrapper


# === 문제 1.5: @retry ===
def retry(max_attempts: int = 3, delay: float = 0.0) -> Callable:
    """실패 시 최대 max_attempts 번 재시도. delay 초 만큼 대기."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if attempt < max_attempts and delay:
                        time.sleep(delay)
            raise RuntimeError(f"재시도 {max_attempts}회 모두 실패") from last_exc

        wrapper.max_attempts = max_attempts
        return wrapper

    return decorator


# === 문제 1.6: 다중 데코레이터 ===
@timer
@cache
def fibonacci(n: int) -> int:
    """@timer 와 @cache 를 함께 적용 — 아래에서 재귀 호출도 전부 캐시됨."""
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)


# ════════════════════════════════════════════════
# 02. 메타클래스 · 디스크립터
# ════════════════════════════════════════════════

# === 문제 2.1: 자동 등록 (__init_subclass__) ===
class Animal:
    """하위 클래스가 정의되는 순간 자동으로 _registry 에 등록된다."""

    _registry: dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 핵심 아이디어: __init_subclass__ 는 메타클래스 없이 클래스 생성을 가로챈다
        Animal._registry[cls.__name__.lower()] = cls


class Dog(Animal):
    def speak(self) -> str:
        return "멍멍"


class Cat(Animal):
    def speak(self) -> str:
        return "야옹"


# === 문제 2.2: PositiveNumber 디스크립터 ===
class PositiveNumber:
    """양수만 허용하는 데이터 디스크립터."""

    def __set_name__(self, owner: type, name: str):
        # 핵심 아이디어: __set_name__ 으로 속성 이름을 자동 전달받는다 (3.6+)
        self.name = "_" + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError(f"{self.name[1:]}: 숫자여야 합니다")
        if value <= 0:
            raise ValueError(f"{self.name[1:]}: 양수여야 합니다 (입력 {value})")
        instance.__dict__[self.name] = value


class Order:
    price = PositiveNumber()
    quantity = PositiveNumber()

    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity


# === 문제 2.3: WriteOnce 디스크립터 ===
class WriteOnce:
    """값을 한 번만 설정할 수 있는 디스크립터 (재할당 시 AttributeError)."""

    def __set_name__(self, owner: type, name: str):
        self.name = "_" + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if hasattr(instance, self.name):
            raise AttributeError(f"'{self.name[1:]}' 는 다시 설정할 수 없습니다")
        instance.__dict__[self.name] = value


class Config:
    host = WriteOnce()

    def __init__(self, host):
        self.host = host


# === 문제 2.4: __slots__ 메모리 ===
@dataclass
class RegularPoint:
    x: int
    y: int


@dataclass(slots=True)  # Python 3.10+ dataclass slots 옵션
class SlotPoint:
    x: int
    y: int


def measure_instance_memory(factory: Callable[[int], object], n: int) -> float:
    """객체 n 개 생성 시 실제 확보 메모리(MB). tracemalloc 사용."""
    gc.collect()
    tracemalloc.start()
    objects = [factory(i) for i in range(n)]
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del objects
    return peak / 1024 / 1024


# === 문제 2.5: 메타클래스 싱글톤 ===
class SingletonMeta(type):
    """클래스 호출(=인스턴스 생성) 자체를 가로채는 메타클래스 싱글톤."""

    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
    def __init__(self, debug: bool = False):
        self.debug = debug


class OtherConfig(metaclass=SingletonMeta):
    pass


# ════════════════════════════════════════════════
# 03. 동시성
# ════════════════════════════════════════════════

# === 문제 3.1: 병렬 카운터 ===
UNSAFE_ITERATIONS = 1000
THREADS = 5


def unsafe_count() -> int:
    counter = 0

    def worker():
        nonlocal counter
        for _ in range(UNSAFE_ITERATIONS):
            counter += 1  # 읽기→더하기→쓰기 사이 경합 발생 가능

    threads = [threading.Thread(target=worker) for _ in range(THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter


def locked_count() -> int:
    counter = 0
    lock = threading.Lock()

    def worker():
        nonlocal counter
        for _ in range(UNSAFE_ITERATIONS):
            # 핵심 아이디어: += 는 원자적이지 않다 — Lock 으로 임계구역 보호
            with lock:
                counter += 1

    threads = [threading.Thread(target=worker) for _ in range(THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter


# === 문제 3.2: URL 상태 확인 (ThreadPoolExecutor) ===
def _http_status(url: str, timeout: float = 5.0) -> int:
    """단일 URL 의 HTTP 상태 코드. 실패 시 0."""
    try:
        # 핵심 아이디어: urlopen 이 예외 없이 열리면 접근 가능한 응답이다.
        # data: 처럼 상태 코드를 주지 않는 스킴은 성공(200)으로 간주한다.
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            code = getattr(resp, "status", None) or resp.getcode()
            return code or 200
    except Exception:
        return 0


def check_urls(urls: list[str]) -> list[int]:
    """URL 목록을 스레드 풀로 병렬 확인 — I/O 바운드에 적합."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as pool:
        return list(pool.map(_http_status, urls))


# === 문제 3.3: 소수 카운트 (multiprocessing) ===
def _sieve_upto(n: int) -> list[int]:
    """2..n 까지의 소수 리스트 (기본 체)."""
    if n < 2:
        return []
    flags = bytearray([1]) * (n + 1)
    flags[0] = flags[1] = 0
    for p in range(2, math.isqrt(n) + 1):
        if flags[p]:
            flags[p * p :: p] = bytearray(len(flags[p * p :: p]))
    return [i for i, flag in enumerate(flags) if flag]


def _count_primes_in_range(bounds: tuple[int, int, list[int]]) -> int:
    """[lo, hi] 구간 소수 개수 — base_primes 로 지우는 구간별 체."""
    lo, hi, base_primes = bounds
    size = hi - lo + 1
    flags = bytearray([1]) * size
    for p in base_primes:
        start = max(p * p, ((lo + p - 1) // p) * p)
        if start > hi:
            continue
        flags[start - lo :: p] = bytearray(len(range(start - lo, size, p)))
    return sum(flags)


def count_primes_parallel(limit: int, processes: int = 4) -> int:
    """2..limit 소수 개수를 프로세스 풀로 병렬 계산.

    CPU 바운드 작업은 GIL 때문에 프로세스 병렬화가 정답.
    """
    base_primes = _sieve_upto(math.isqrt(limit))
    chunk_size = max(1, (limit - 1) // processes)
    tasks = []
    lo = 2
    while lo <= limit:
        hi = min(limit, lo + chunk_size - 1)
        tasks.append((lo, hi, base_primes))
        lo = hi + 1
    with multiprocessing.Pool(processes=processes) as pool:
        return sum(pool.map(_count_primes_in_range, tasks))


# === 문제 3.4: 생산자-소비자 ===
def producer_consumer(num_producers: int = 3, num_consumers: int = 2, per: int = 5):
    """Queue 로 통신하는 생산자/소비자 — processed 개수와 합계 반환."""
    q: "queue.Queue" = queue.Queue()
    processed: list[int] = []
    processed_lock = threading.Lock()
    SENTINEL = None  # 소비자 종료 신호

    def produce(pid: int):
        for i in range(1, per + 1):
            q.put(pid * 100 + i)

    def consume():
        while True:
            item = q.get()
            if item is SENTINEL:
                q.task_done()
                break
            with processed_lock:
                processed.append(item)
            q.task_done()

    producers = [threading.Thread(target=produce, args=(p,)) for p in range(num_producers)]
    consumers = [threading.Thread(target=consume) for _ in range(num_consumers)]
    for t in producers + consumers:
        t.start()
    for t in producers:
        t.join()
    for _ in consumers:  # 생산 끝나면 소비자 수만큼 종료 신호 전송
        q.put(SENTINEL)
    for t in consumers:
        t.join()
    return processed


# === 문제 3.5: 데드락 시뮬레이션과 해결 ===
class Account:
    def __init__(self, name: str, balance: int):
        self.name = name
        self.balance = balance
        self.lock = threading.Lock()


# ❌ 데드락 버전 — 절대 실행 금지 (두 스레드가 서로의 lock 을 교차 대기)
#
# def transfer_deadlock(src, dst, amount):
#     with src.lock:                    # 스레드1: A.lock 획득
#         time.sleep(0.001)
#         with dst.lock:                # 스레드2: B.lock 획득 후 A.lock 대기 → 영원히 대기
#             ...


def transfer_safe(src: Account, dst: Account, amount: int) -> None:
    """✅ 해결: 항상 정렬된 순서(lock ordering)로 획득하면 순환 대기가 없다."""
    first, second = sorted([src, dst], key=lambda a: a.name)
    with first.lock, second.lock:
        if src.balance >= amount:
            src.balance -= amount
            dst.balance += amount


# ════════════════════════════════════════════════
# 04. asyncio
# ════════════════════════════════════════════════

# === 문제 4.1: 비동기 카운트다운 ===
async def countdown(name: str, n: int, delay: float = 0.05) -> list[str]:
    """delay 초 간격으로 n 부터 1 까지 카운트다운."""
    ticks = []
    for i in range(n, 0, -1):
        ticks.append(f"{name}: {i}")
        await asyncio.sleep(delay)
    return ticks


async def run_countdowns_concurrently() -> tuple[list[str], float]:
    """여러 카운트다운을 동시 실행 — 총 시간이 순차 실행보다 짧아진다."""
    start = time.perf_counter()
    results = await asyncio.gather(
        countdown("A", 3), countdown("B", 3), countdown("C", 3)
    )
    elapsed = time.perf_counter() - start
    return [tick for ticks in results for tick in ticks], elapsed


# === 문제 4.2: URL 상태 (비동기) ===
async def fetch_status_async(urls: list[str]) -> list[int]:
    """asyncio + 실행자(executor)로 병렬 HTTP 확인.

    실무에서는 aiohttp 를 쓰지만, 표준 라이브러리만으로도
    loop.run_in_executor 로 블로킹 호출을 비동기처럼 감쌀 수 있다.
    """
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(None, _http_status, url) for url in urls]
    return list(await asyncio.gather(*tasks))


# === 문제 4.3: 비동기 큐 처리 ===
async def async_producer_consumer(num_producers: int = 2, num_consumers: int = 3):
    """asyncio.Queue 기반 생산자/소비자 — 처리 합계 반환."""
    q: asyncio.Queue = asyncio.Queue()
    total = 0
    SENTINEL = -1

    async def produce(pid: int):
        for i in range(1, 6):
            await q.put(i)

    async def consume():
        nonlocal total
        while True:
            item = await q.get()
            if item == SENTINEL:
                q.task_done()
                break
            await asyncio.sleep(0)  # yield to event loop
            total += item
            q.task_done()

    consumers = [asyncio.create_task(consume()) for _ in range(num_consumers)]
    producers = [asyncio.create_task(produce(p)) for p in range(num_producers)]
    await asyncio.gather(*producers)
    for _ in consumers:  # 소비자 수만큼 종료 신호
        await q.put(SENTINEL)
    await asyncio.gather(*consumers)
    return total


# === 문제 4.4: 동시 실행 제한 ===
async def bounded_workers(count: int = 25, limit: int = 10) -> int:
    """Semaphore 로 동시 실행을 최대 limit 개로 제한 — 피크 동시성 반환."""
    semaphore = asyncio.Semaphore(limit)
    active = [0]
    peak = [0]

    async def worker(i: int):
        async with semaphore:  # 핵심 아이디어: 세마포어 진입에 동시성 상한이 걸린다
            active[0] += 1
            peak[0] = max(peak[0], active[0])
            await asyncio.sleep(0.01)
            active[0] -= 1

    await asyncio.gather(*(worker(i) for i in range(count)))
    return peak[0]


# === 문제 4.5: 타임아웃 ===
async def slow_task(seconds: float = 10.0) -> str:
    await asyncio.sleep(seconds)
    return "완료"


async def guarded_slow_task(timeout: float = 0.05) -> str:
    """오래 걸리는 작업에 타임아웃을 걸고 TimeoutError 를 우아하게 처리."""
    try:
        return await asyncio.wait_for(slow_task(), timeout=timeout)
    except (TimeoutError, asyncio.TimeoutError):
        return "타임아웃! 기본값 사용"


# ════════════════════════════════════════════════
# 05. 타입 힌트
# ════════════════════════════════════════════════

# === 문제 5.1: 타입 힌트 추가 ===
def scale(values: list[float], factor: float = 2.0) -> list[float]:
    """각 값을 factor 배율로 조정.

    ❌ 원래 코드: def scale(values, factor=2.0): return [v * factor for v in values]
    ✅ 힌트 추가: 인자/반환 타입이 문서 없이도 명확해진다.
    """
    return [v * factor for v in values]


# === 문제 5.2: Optional 반환 ===
def find_user(users: dict[int, str], uid: int) -> Optional[str]:
    """ID 로 사용자 찾기 — 없으면 None (호출자가 None 체크 강제)."""
    return users.get(uid)


# === 문제 5.3: 제네릭 Stack ===
T = TypeVar("T")


class Stack(Generic[T]):
    """타입 파라미터 T 를 갖는 LIFO 스택."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("빈 스택")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("빈 스택")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items


# === 문제 5.4: TypedDict ===
from typing import TypedDict  # noqa: E402


class User(TypedDict):
    """사용자 정보 dict 의 구조를 명시 — 키 오타/누락을 mypy 가 잡아준다."""

    name: str
    age: int


def adult_names(users: list[User]) -> list[str]:
    return [u["name"] for u in users if u["age"] >= 19]


# === 문제 5.5: Protocol ===
class HasLength(Protocol):
    """__len__ 만 갖추면 어떤 객체든 이 프로토콜을 만족한다 (구조적 타이핑)."""

    def __len__(self) -> int: ...


def print_length(obj: HasLength) -> int:
    return len(obj)


# ════════════════════════════════════════════════
# 06. 테스팅
# ════════════════════════════════════════════════

# === 문제 6.1: 기본 테스트 ===
def calc_add(a: float, b: float) -> float:
    return a + b


def calc_sub(a: float, b: float) -> float:
    return a - b


def calc_mul(a: float, b: float) -> float:
    return a * b


def calc_div(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("0 으로 나눌 수 없음")
    return a / b


# === 문제 6.2: 예외 테스트 ===
def factorial(n: int) -> int:
    """음수 입력 시 ValueError."""
    if n < 0:
        raise ValueError("n 은 0 이상이어야 합니다")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# === 문제 6.3: Parametrize ===
def is_palindrome(text: str) -> bool:
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


PALINDROME_CASES = [
    ("level", True),
    ("hello", False),
    ("racecar", True),
    ("", True),
    ("소주 만 병만 주소", True),
]


def test_palindrome_parametrized() -> None:
    # pytest 의 @pytest.mark.parametrize 를 흉내 — 케이스 테이블 순회
    for text, expected in PALINDROME_CASES:
        result = is_palindrome(text)
        assert result is expected, f"실패 케이스: {text!r}"


# === 문제 6.4: Fixture ===
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def tmp_text_file(tmp_dir: Path, content: str = "hello fixture") -> Path:
    """pytest fixture 처럼 테스트용 자원을 준비하는 헬퍼."""
    path = tmp_dir / "fixture.txt"
    path.write_text(content, encoding="utf-8")
    return path


# === 문제 6.5: 모킹 ===
def fetch_json(url: str) -> dict:
    """외부 API 호출 (실제 네트워크 사용 — 테스트에서는 mock 으로 대체)."""
    with urllib.request.urlopen(url, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_weather(city: str) -> dict:
    url = f"https://api.example.com/weather?city={urllib.parse.quote(city)}"
    return fetch_json(url)


def test_get_weather_with_mock() -> None:
    canned = {"city": "Seoul", "temp": 31}
    with patch(f"{__name__}.fetch_json", return_value=canned) as mock_fetch:
        # 핵심 아이디어: 외부 의존을 가짜 객체로 교체해 네트워크 없이 테스트
        result = get_weather("Seoul")
    assert result == canned
    mock_fetch.assert_called_once_with(
        "https://api.example.com/weather?city=Seoul"
    )


# === 문제 6.6: TDD BankAccount ===
class TddBankAccount:
    """TDD 로 구현한 계좌 — 거래 내역까지 기록."""

    def __init__(self, balance: int = 0):
        if balance < 0:
            raise ValueError("초기 잔액은 0 이상")
        self.balance = balance
        self.history: list[str] = []

    def deposit(self, amount: int) -> int:
        if amount <= 0:
            raise ValueError("입금액은 양수")
        self.balance += amount
        self.history.append(f"입금 {amount}")
        return self.balance

    def withdraw(self, amount: int) -> int:
        if amount <= 0:
            raise ValueError("출금액은 양수")
        if amount > self.balance:
            raise ValueError("잔액 부족")
        self.balance -= amount
        self.history.append(f"출금 {amount}")
        return self.balance


# ════════════════════════════════════════════════
# 07. 성능
# ════════════════════════════════════════════════

# === 문제 7.1: 측정 — list vs set 멤버십 ===
def benchmark_membership(size: int = 100_000, lookups: int = 20) -> tuple[float, float]:
    """in 연산: list 는 O(n) 선형 탐색, set 은 O(1) 해시 탐색."""
    data = list(range(size))
    hash_set = set(data)
    missing = -1  # 없는 값으로 최악의 선형 탐색 유도

    def scan_list():
        for _ in range(lookups):
            missing in data

    def scan_set():
        for _ in range(lookups):
            missing in hash_set

    best_list = min(_timeit_once(scan_list) for _ in range(3))
    best_set = min(_timeit_once(scan_set) for _ in range(3))
    return best_list, best_set


def _timeit_once(func: Callable[[], None]) -> float:
    start = time.perf_counter()
    func()
    return time.perf_counter() - start


# === 문제 7.2: 프로파일링 ===
def slow_sum(n: int) -> int:
    total = 0
    for i in range(n):
        for j in range(20):
            total += (i * j) % 7
    return total


def profile_slow_sum(n: int = 20000) -> str:
    """cProfile 로 병목 함수 분석 — 보고서 문자열 반환."""
    profiler = cProfile.Profile()
    profiler.enable()
    slow_sum(n)
    profiler.disable()
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative").print_stats(5)
    return stream.getvalue()


# === 문제 7.3: 최적화 전후 — 회문 3가지 방식 ===
def palindrome_slice(s: str) -> bool:
    c = s.lower().replace(" ", "")
    return c == c[::-1]


def palindrome_reversed(s: str) -> bool:
    c = s.lower().replace(" ", "")
    return c == "".join(reversed(c))


def palindrome_two_pointer(s: str) -> bool:
    c = s.lower().replace(" ", "")
    left, right = 0, len(c) - 1
    while left < right:
        if c[left] != c[right]:
            return False
        left += 1
        right -= 1
    return True


# === 문제 7.4: 메모리 비교 → 2.4 의 measure_instance_memory 재사용 ===


# === 문제 7.5: 표준편차 Python vs numpy ===
def stddev_manual(data: list[float]) -> float:
    """순수 Python 표준편차 (모표준편차). numpy 가 없어도 동일 수식 구현 가능."""
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    return math.sqrt(variance)


# ════════════════════════════════════════════════
# 08. 패키징
# ════════════════════════════════════════════════

HELLO_PYPROJECT = """\
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "hello-world-study"
version = "0.1.0"
description = "최소 파이썬 패키지 예제"
"""

LINECOUNTER_PYPROJECT = """\
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "linecounter"
version = "0.1.0"

[project.scripts]
linecounter = "linecounter.cli:main"

[project.optional-dependencies]
http = ["requests"]   # 8.3: 외부 의존성 추가 예시
"""

PUBLISH_GUIDE = """\
# 8.5 TestPyPI 배포 절차
python -m pip install --upgrade build twine
python -m build                       # dist/*.whl + *.tar.gz 생성
python -m twine upload --repository testpypi dist/*
# 다른 가상 환경에서 확인:
python -m venv /tmp/checkenv && source /tmp/checkenv/bin/activate
pip install --index-url https://test.pypi.org/simple/ hello-world-study
"""


def write_hello_package(root: Path) -> Path:
    pkg = root / "hello_world"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text(
        'def say_hello():\n    return "Hello, world!"\n', encoding="utf-8"
    )
    (root / "pyproject.toml").write_text(HELLO_PYPROJECT, encoding="utf-8")
    return pkg


def write_linecounter_package(root: Path) -> Path:
    pkg = root / "linecounter"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "cli.py").write_text(
        "import sys\n"
        "\n"
        "def count_lines(path):\n"
        '    with open(path, encoding="utf-8") as f:\n'
        "        return sum(1 for _ in f)\n"
        "\n"
        "def main(argv=None):\n"
        "    argv = argv if argv is not None else sys.argv[1:]\n"
        "    if not argv:\n"
        '        print("사용법: linecounter <파일>")\n'
        "        return 2\n"
        "    print(count_lines(argv[0]))\n"
        "    return 0\n",
        encoding="utf-8",
    )
    (root / "pyproject.toml").write_text(LINECOUNTER_PYPROJECT, encoding="utf-8")
    return pkg


# ════════════════════════════════════════════════
# 종합 프로젝트 1: 비동기 웹 스크래퍼 (stdlib 버전)
# ════════════════════════════════════════════════


class _HeadingCollector(html.parser.HTMLParser):
    """h1~h3 태그 안의 텍스트를 수집하는 파서."""

    def __init__(self):
        super().__init__()
        self.headings: list[str] = []
        self._stack: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3"):
            self._stack.append((tag, []))

    def handle_endtag(self, tag):
        if self._stack and self._stack[-1][0] == tag:
            _, buf = self._stack.pop()
            text = "".join(buf).strip()
            if text:
                self.headings.append(text)

    def handle_data(self, data):
        if self._stack:
            self._stack[-1][1].append(data)


def extract_headings(html_text: str) -> list[str]:
    parser = _HeadingCollector()
    parser.feed(html_text)
    return parser.headings


def data_uri(html_text: str) -> str:
    """외부 네트워크 없이 테스트하기 위한 data: URI."""
    return "data:text/html;charset=utf-8," + urllib.parse.quote(html_text)


async def fetch_html_async(url: str, retries: int = 2, timeout: float = 5.0) -> str:
    """재시도 로직이 포함된 비동기 HTML 가져오기 (executor 로 urllib 감싸기)."""
    loop = asyncio.get_running_loop()

    def _get():
        req = urllib.request.Request(url, headers={"User-Agent": "study-scraper"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")

    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return await loop.run_in_executor(None, _get)
        except Exception as exc:
            last_exc = exc
            await asyncio.sleep(0.01 * (attempt + 1))  # 백오프
    raise RuntimeError(f"가져오기 실패: {url}") from last_exc


async def scrape_all(urls: list[str], concurrency: int = 3) -> list[dict]:
    """Semaphore 로 동시성을 제한하며 N 개 URL 스크랩 — 진행률 출력 포함."""
    semaphore = asyncio.Semaphore(concurrency)

    async def one(url: str) -> dict:
        async with semaphore:
            html_text = await fetch_html_async(url)
            headings = extract_headings(html_text)
            print(f"   진행 {done[0]}/{len(urls)} — {headings[:1]}")
            done[0] += 1
            return {"url": url, "headings": headings}

    done = [0]
    return list(await asyncio.gather(*(one(u) for u in urls)))


def save_pages(db_path: Path, rows: list[dict]) -> int:
    """결과를 SQLite 에 저장하고 저장된 행 수 반환."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS pages ("
            "url TEXT PRIMARY KEY, h1 TEXT, headings TEXT)"
        )
        conn.executemany(
            "INSERT OR REPLACE INTO pages VALUES (?, ?, ?)",
            [
                (
                    r["url"],
                    r["headings"][0] if r["headings"] else "",
                    json.dumps(r["headings"], ensure_ascii=False),
                )
                for r in rows
            ],
        )
        conn.commit()
        return conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
    finally:
        conn.close()


# ════════════════════════════════════════════════
# 종합 프로젝트 2: 모니터링 시스템
# ════════════════════════════════════════════════


class Monitor:
    """백그라운드 스레드로 주기 검사 → 결과 기록 + 실패 알림."""

    def __init__(self, interval: float = 0.01):
        self.interval = interval
        self.checks: dict[str, Callable[[], bool]] = {}
        self.results: dict[str, list[bool]] = {}
        self.alerts: list[str] = []
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def add_check(self, name: str, check: Callable[[], bool]) -> None:
        self.checks[name] = check

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self):
        # 핵심 아이디어: Event.wait(interval) 는 깨어날 시간을 정확히 제어
        while not self._stop.wait(self.interval):
            with self._lock:
                for name, check in self.checks.items():
                    ok = check()
                    self.results.setdefault(name, []).append(ok)
                    if not ok:
                        self.alerts.append(name)


# ════════════════════════════════════════════════
# 종합 프로젝트 3: 캐시 라이브러리 (LRU / TTL / LFU)
# ════════════════════════════════════════════════


class Cache:
    """정책 교체 가능한 인메모리 캐시 + 히트율 통계."""

    def __init__(self, maxsize: int = 3, ttl: float | None = None,
                 policy: str = "lru"):
        if policy not in ("lru", "ttl", "lfu"):
            raise ValueError(f"미지원 정책: {policy}")
        self.maxsize = maxsize
        self.ttl = ttl
        self.policy = policy
        # key -> [value, expires_at] — dict 는 삽입 순서 유지(LRU 후보 추적에 활용)
        self._store: OrderedDict = OrderedDict()
        self._freq: dict[Any, int] = {}
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

    def __contains__(self, key) -> bool:
        return key in self._store

    def get(self, key):
        entry = self._store.get(key)
        if entry is None:
            self.misses += 1
            return None
        value, expires_at = entry
        if expires_at <= time.monotonic():  # TTL 만료
            del self._store[key]
            self._freq.pop(key, None)
            self.misses += 1
            return None
        self.hits += 1
        self._freq[key] = self._freq.get(key, 0) + 1
        if self.policy == "lru":
            self._store.move_to_end(key)  # 최근 사용으로 이동
        return value

    def set(self, key, value) -> None:
        if key in self._store:
            self._store[key] = [value, self._expiry()]
            self._store.move_to_end(key)
            return
        if len(self._store) >= self.maxsize:
            self._evict_one()
        expires_at = self._expiry()
        self._store[key] = [value, expires_at]
        self._freq[key] = 1

    def _expiry(self) -> float:
        return time.monotonic() + self.ttl if self.ttl else math.inf

    def _evict_one(self) -> None:
        if self.policy == "lru":
            victim, _ = self._store.popitem(last=False)  # 가장 오래 미사용
        elif self.policy == "ttl":
            victim = min(self._store, key=lambda k: self._store[k][1])  # 곧 만료
            del self._store[victim]
        else:  # lfu
            victim = min(self._store, key=lambda k: self._freq.get(k, 0))
            del self._store[victim]
        self._freq.pop(victim, None)
        self.evictions += 1


def cached(mem: Cache) -> Callable:
    """캐시 인스턴스를 받는 데코레이터."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            if key in mem:
                return mem.get(key)
            result = func(*args, **kwargs)
            mem.set(key, result)
            return result

        return wrapper

    return decorator


# ════════════════════════════════════════════════
# 검증 — python3 solutions.py 로 실행
# ════════════════════════════════════════════════
if __name__ == "__main__":
    # ── 01. 데코레이터 ──
    @timer
    def busy(n: int) -> int:
        return sum(range(n))

    assert busy(100_000) > 0
    assert busy.last_elapsed >= 0

    log_buffer = io.StringIO()
    with redirect_stdout(log_buffer):

        @log
        def greet(name: str) -> str:
            return f"안녕, {name}"

        greet("민수")
    logged = log_buffer.getvalue()
    assert "호출 greet" in logged and "'안녕, 민수'" in logged

    @cache
    def slow_double(x: int, offset: int = 0) -> int:
        return x * 2 + offset

    assert slow_double(21) == 42
    assert slow_double(21) == 42          # 캐시 히트
    assert slow_double(21, offset=1) == 43
    assert slow_double.cache_hits == 1 and slow_double.cache_misses == 2

    @validate_ints
    def calc_mul_checked(a: int, b: int) -> int:
        return a * b

    assert calc_mul_checked(6, 7) == 42
    for bad in ("6", 6.0, True):
        try:
            calc_mul_checked(bad, 2)
            assert False, f"{bad!r} 는 거부되어야 함"
        except TypeError:
            pass

    retry_calls: list[int] = []

    @retry(max_attempts=3, delay=0)
    def flaky_operation() -> str:
        retry_calls.append(len(retry_calls))
        if len(retry_calls) < 3:
            raise ConnectionError("일시 장애")
        return "복구"

    assert flaky_operation() == "복구" and len(retry_calls) == 3

    fib_memo = fibonacci.__wrapped__  # 내부의 cache wrapper
    assert fibonacci(30) == 832_040   # 캐시 덕분에 즉시 계산
    assert fib_memo.cache_misses <= 31  # 0..30 각 한 번만 실계산
    assert fibonacci.last_elapsed < 0.5
    print("✅ 01. 데코레이터 (6 문제)")

    # ── 02. 메타클래스 · 디스크립터 ──
    assert {"dog", "cat"} <= set(Animal._registry)
    buddy = Animal._registry["dog"]()
    assert buddy.speak() == "멍멍"

    order = Order(price=1500, quantity=3)
    assert order.total() == 4500
    for bad_price in (-100, 0, "비쌈"):
        try:
            Order(price=bad_price, quantity=1)
            assert False
        except (ValueError, TypeError):
            pass

    cfg = Config(host="example.com")
    assert cfg.host == "example.com"
    try:
        cfg.host = "other.com"
        assert False, "WriteOnce 재할당은 AttributeError 여야 함"
    except AttributeError:
        pass

    regular_mb = measure_instance_memory(lambda i: RegularPoint(i, i), 20_000)
    slot_mb = measure_instance_memory(lambda i: SlotPoint(i, i), 20_000)
    assert regular_mb > slot_mb * 1.3  # __slots__ 가 확실히 작음
    print(f"   💡 메모리: 일반 {regular_mb:.1f}MB vs __slots__ {slot_mb:.1f}MB "
          "(2만 개)")

    assert AppConfig() is AppConfig()      # 같은 인스턴스
    assert OtherConfig() is OtherConfig()  # 클래스별로 독립 관리
    AppConfig().debug = True
    assert AppConfig().debug is True
    print("✅ 02. 메타클래스 · 디스크립터 (5 문제)")

    # ── 03. 동시성 ──
    locked = locked_count()
    assert locked == THREADS * UNSAFE_ITERATIONS  # Lock 이면 항상 정확
    unsafe = unsafe_count()  # GIL 환경에 따라 우연히 맞을 수도, 어긋날 수도
    assert unsafe in range(THREADS * UNSAFE_ITERATIONS + 1)
    print(f"   💡 Lock 없음: {unsafe} / Lock 있음: {locked}")

    statuses = check_urls(
        ["data:text/plain,ok", "data:text/plain,hola", "http://127.0.0.1:9/nope"]
    )
    assert statuses == [200, 200, 0]  # 마지막은 접속 불가 → 0 처리

    prime_count = count_primes_parallel(1_000_000, processes=4)
    assert prime_count == 78_498  # π(10^6)
    # 전체 범위 실행 예: count_primes_parallel(10_000_000) == 664_579

    processed_items = producer_consumer(num_producers=3, num_consumers=2, per=5)
    assert sorted(processed_items) == sorted(
        p * 100 + i for p in range(3) for i in range(1, 6)
    )

    a = Account("A", 500)
    b = Account("B", 300)

    def hammer(src: Account, dst: Account):
        for _ in range(100):
            transfer_safe(src, dst, 1)

    threads = []
    for i in range(4):
        src, dst = (a, b) if i % 2 == 0 else (b, a)
        threads.append(threading.Thread(target=hammer, args=(src, dst)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()  # lock ordering 덕분에 데드락 없이 종료
    assert a.balance + b.balance == 800  # 총액 보존
    print("✅ 03. 동시성 (5 문제)")

    # ── 04. asyncio ──
    ticks, elapsed = asyncio.run(run_countdowns_concurrently())
    assert len(ticks) == 9
    assert elapsed < 3 * 3 * 0.05  # 순차 실행(0.45s)보다 빠름 = 동시성 확인
    statuses_a = asyncio.run(
        fetch_status_async(
            ["data:text/plain,a", "data:text/plain,b", "data:text/plain,c"]
        )
    )
    assert statuses_a == [200, 200, 200]

    consumed_total = asyncio.run(async_producer_consumer())
    assert consumed_total == 2 * (1 + 2 + 3 + 4 + 5)  # 생산자 2 × 15

    peak = asyncio.run(bounded_workers(count=25, limit=10))
    assert peak == 10  # 상한을 정확히 지키며 동시 실행

    assert asyncio.run(guarded_slow_task()) == "타임아웃! 기본값 사용"
    print("✅ 04. asyncio (5 문제)")

    # ── 05. 타입 힌트 ──
    assert scale([1, 2, 3]) == [2, 4, 6]
    assert scale([1.5], factor=2.0) == [3.0]

    users_map = {1: "김철수", 2: "이영희"}
    assert find_user(users_map, 1) == "김철수"
    assert find_user(users_map, 99) is None

    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    assert int_stack.pop() == 2
    assert int_stack.peek() == 1
    assert not int_stack.is_empty()
    int_stack.pop()
    assert int_stack.is_empty()
    try:
        int_stack.pop()
        assert False
    except IndexError:
        pass

    typed_users: list[User] = [
        {"name": "김철수", "age": 17},
        {"name": "이영희", "age": 25},
        {"name": "박민수", "age": 19},
    ]
    assert adult_names(typed_users) == ["이영희", "박민수"]

    assert print_length("abc") == 3
    assert print_length([1, 2]) == 2
    assert print_length({"a": 1}) == 1
    print("✅ 05. 타입 힌트 (5 문제)")

    # ── 06. 테스팅 ──
    assert calc_add(2, 3) == 5
    assert calc_sub(5, 2) == 3
    assert calc_mul(3, 4) == 12
    assert calc_div(10, 4) == 2.5
    try:
        calc_div(1, 0)
        assert False
    except ZeroDivisionError:
        pass

    assert factorial(5) == 120 and factorial(0) == 1
    try:
        factorial(-1)
        assert False, "ValueError 발생해야 함"
    except ValueError:
        pass

    test_palindrome_parametrized()  # 5 케이스 통과

    with tempfile.TemporaryDirectory() as tmp:
        fixture_path = tmp_text_file(Path(tmp))
        assert read_text(fixture_path) == "hello fixture"

    test_get_weather_with_mock()  # mock 으로 외부 API 대체

    account = TddBankAccount(100)
    assert account.deposit(50) == 150
    assert account.withdraw(30) == 120
    assert account.history == ["입금 50", "출금 30"]
    try:
        account.withdraw(9999)
        assert False
    except ValueError:
        pass
    try:
        TddBankAccount(-1)
        assert False
    except ValueError:
        pass
    print("✅ 06. 테스팅 (6 문제)")

    # ── 07. 성능 ──
    t_list, t_set = benchmark_membership()
    assert t_set < t_list  # set 멤버십이 압도적으로 빠름
    print(f"   💡 list 멤버십 {t_list * 1000:.2f}ms vs set 멤버십 "
          f"{t_set * 1000:.3f}ms")

    profile_report = profile_slow_sum()
    assert "slow_sum" in profile_report

    pal_funcs = {
        "slice": palindrome_slice,
        "reversed": palindrome_reversed,
        "two_pointer": palindrome_two_pointer,
    }
    long_text = "a" * 500 + "b" + "a" * 500
    for name, func in pal_funcs.items():
        assert func("level") and func("소주 만 병만 주소") and not func("hello")
        assert func(long_text)  # a...ab...a 구조의 회문
    timings = {name: _timeit_once(lambda f=func: f(long_text))
               for name, func in pal_funcs.items()}
    print(f"   💡 회문 3방식: {', '.join(f'{k}={v * 1000:.2f}ms' for k, v in timings.items())}")

    regular_mb2 = measure_instance_memory(lambda i: RegularPoint(i, i), 20_000)
    slot_mb2 = measure_instance_memory(lambda i: SlotPoint(i, i), 20_000)
    assert regular_mb2 > slot_mb2

    sample = [2, 4, 4, 4, 5, 5, 7, 9]
    assert math.isclose(stddev_manual(sample), 2.0)
    assert math.isclose(stddev_manual(sample), statistics.pstdev(sample))
    # numpy 를 쓴다면: numpy.std(sample) 과도 동일 결과
    print("✅ 07. 성능 (5 문제)")

    # ── 08. 패키징 ──
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        hello_pkg_dir = write_hello_package(tmp_path / "hello_proj")
        sys.path.insert(0, str(hello_pkg_dir.parent))
        try:
            hello_world = importlib.import_module("hello_world")
            assert hello_world.say_hello() == "Hello, world!"
        finally:
            sys.path.remove(str(hello_pkg_dir.parent))
            sys.modules.pop("hello_world", None)

        lc_pkg_dir = write_linecounter_package(tmp_path / "lc_proj")
        sys.path.insert(0, str(lc_pkg_dir.parent))
        try:
            linecounter_cli = importlib.import_module("linecounter.cli")
            sample_file = tmp_path / "sample.txt"
            sample_file.write_text("한 줄\n두 줄\n세 줄\n", encoding="utf-8")
            assert linecounter_cli.count_lines(str(sample_file)) == 3
            assert linecounter_cli.main([str(sample_file)]) == 0
            assert linecounter_cli.main([]) == 2  # 인자 없음 → 사용법 안내
        finally:
            sys.path.remove(str(lc_pkg_dir.parent))
            for name in [m for m in sys.modules if m.split(".")[0] == "linecounter"]:
                del sys.modules[name]

        assert 'dependencies' not in HELLO_PYPROJECT
        assert '"requests"' in LINECOUNTER_PYPROJECT  # 8.3 의존성 선언 예시

        try:
            import tomllib
        except ImportError:
            tomllib = None
        if tomllib is not None:
            tomllib.loads(HELLO_PYPROJECT)
            tomllib.loads(LINECOUNTER_PYPROJECT)
        print(PUBLISH_GUIDE)
    print("✅ 08. 패키징 (5 문제)")

    # ── 종합 프로젝트 1: 비동기 웹 스크래퍼 ──
    samples = [
        "<html><h1>뉴스 속보</h1><h2>경제 헤드라인</h2></html>",
        "<html><h1>스포츠 소식</h1><h3>축구 결승</h3></html>",
        "<html><body><h2>날씨 정보</h2><p>맑음</p></body></html>",
    ]
    scraped_rows = asyncio.run(scrape_all([data_uri(s) for s in samples]))
    assert len(scraped_rows) == 3
    assert scraped_rows[0]["headings"] == ["뉴스 속보", "경제 헤드라인"]
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "scrape.db"
        saved = save_pages(db_path, scraped_rows)
        assert saved == 3
        with sqlite3.connect(db_path) as conn:
            first_h1 = conn.execute(
                "SELECT h1 FROM pages ORDER BY url LIMIT 1"
            ).fetchone()[0]
        assert any(first_h1 in r["headings"] for r in scraped_rows)
    print("✅ 프로젝트 1: 비동기 웹 스크래퍼")

    # ── 종합 프로젝트 2: 모니터링 시스템 ──
    monitor = Monitor(interval=0.005)
    monitor.add_check("db", lambda: True)
    monitor.add_check("api", lambda: False)  # 항상 실패하는 검사
    monitor.start()
    time.sleep(0.05)
    monitor.stop()
    assert len(monitor.results["db"]) > 0
    assert all(monitor.results["db"])
    assert monitor.alerts.count("api") == len(monitor.results["api"]) > 0
    print(f"✅ 프로젝트 2: 모니터링 ({len(monitor.results['db'])}회 폴링, "
          f"알림 {len(monitor.alerts)}건)")

    # ── 종합 프로젝트 3: 캐시 라이브러리 ──
    lru_cache_ = Cache(maxsize=2, policy="lru")
    lru_cache_.set("a", 1)
    lru_cache_.set("b", 2)
    assert lru_cache_.get("a") == 1       # a 를 최근 사용으로
    lru_cache_.set("c", 3)                # 가장 오래된 b 축출
    assert "b" not in lru_cache_ and lru_cache_.evictions == 1
    assert lru_cache_.get("a") == 1

    ttl_cache = Cache(policy="ttl", ttl=0.05)
    ttl_cache.set("k", "v")
    assert ttl_cache.get("k") == "v"
    time.sleep(0.06)
    assert ttl_cache.get("k") is None     # TTL 만료 → 미스

    lfu_cache = Cache(maxsize=2, policy="lfu")
    lfu_cache.set("x", 1)
    lfu_cache.set("y", 2)
    lfu_cache.get("x")
    lfu_cache.get("x")                    # x 빈도 3
    lfu_cache.get("y")                    # y 빈도 2
    lfu_cache.set("z", 3)                 # y 축출
    assert "y" not in lfu_cache and lfu_cache.get("x") == 1

    call_count = [0]

    @cached(Cache(maxsize=8))
    def expensive_square(n: int) -> int:
        call_count[0] += 1
        return n * n

    assert expensive_square(12) == 144
    assert expensive_square(12) == 144    # 두 번째는 캐시에서
    assert call_count[0] == 1

    stats_cache = lru_cache_
    assert stats_cache.get("없는 키") is None  # 명시적 미스 → 통계 기록
    assert 0 < stats_cache.hit_rate < 1
    assert stats_cache.hits >= 2 and stats_cache.misses >= 1
    print(f"✅ 프로젝트 3: 캐시 라이브러리 (히트율 {stats_cache.hit_rate:.0%})")

    print("\n🎉 모든 테스트 통과! (본문 42문제 + 프로젝트 3개)")
