# 07. 성능 최적화와 프로파일링

## 🎯 학습 목표
- 코드 성능을 측정하고 분석한다
- 병목 지점을 찾는다
- Python 코드를 최적화한다
- 적절한 자료구조를 선택한다

## 1. 성능 측정 기본

### 1.1 시간 측정 — timeit
```python
import timeit

# 한 줄 코드
t = timeit.timeit("'-'.join(str(n) for n in range(100))", number=10000)
print(f"{t:.4f}초")

# 멀티라인
code = """
result = []
for i in range(100):
    result.append(str(i))
'-'.join(result)
"""
t = timeit.timeit(code, number=10000)

# 함수 측정
def my_function():
    return [x ** 2 for x in range(1000)]

t = timeit.timeit(my_function, number=1000)
```

### 1.2 IPython/Jupyter 매직 명령
```ipython
%timeit "-".join(str(n) for n in range(100))
%%timeit
result = []
for i in range(100):
    result.append(str(i))
```

### 1.3 time / perf_counter
```python
import time

start = time.perf_counter()
# 측정할 코드
result = sum(range(1_000_000))
elapsed = time.perf_counter() - start
print(f"{elapsed:.4f}초")

# 컨텍스트 매니저로
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.perf_counter()
    yield
    print(f"{label}: {time.perf_counter() - start:.4f}s")

with timer("sum"):
    sum(range(1_000_000))
```

## 2. 프로파일링

### 2.1 cProfile — 함수별 시간
```python
import cProfile
import pstats

def slow_function():
    total = 0
    for i in range(1_000_000):
        total += i ** 2
    return total

# 직접 실행
cProfile.run("slow_function()")

# 상세 분석
profiler = cProfile.Profile()
profiler.enable()
slow_function()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats(10)  # 상위 10개
```

명령줄:
```bash
python -m cProfile -o profile.out script.py
python -m pstats profile.out
```

### 2.2 line_profiler — 줄별 시간
```bash
pip install line_profiler
```

```python
@profile  # 데코레이터 사용 (kernprof 로 실행)
def slow_function():
    total = 0
    for i in range(1_000_000):
        total += i ** 2
    return total
```

```bash
kernprof -l -v script.py
```

### 2.3 memory_profiler — 메모리
```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def memory_hog():
    data = [i ** 2 for i in range(1_000_000)]
    return sum(data)

memory_hog()
```

### 2.4 py-spy — 샘플링 프로파일러
```bash
pip install py-spy

# 실행 중인 프로세스
py-spy top --pid 12345

# 결과를 SVG 로
py-spy record -o profile.svg -- python script.py
```

## 3. Python 성능 팁

### 3.1 자료구조 선택
```python
# 멤버십 테스트
items_list = list(range(10000))
items_set = set(range(10000))

# list: O(n) — 느림
9999 in items_list

# set: O(1) — 빠름!
9999 in items_set

# 시간 비교 (IPython/Jupyter)
# %timeit 9999 in items_list   # ~100 µs
# %timeit 9999 in items_set    # ~30 ns
```

| 연산 | list | set/dict | tuple | deque |
|------|------|----------|-------|-------|
| 검색 | O(n) | O(1) | O(n) | O(n) |
| 끝 추가 | O(1) | O(1) | ❌ | O(1) |
| 앞 추가 | O(n) | O(1) | ❌ | O(1) |
| 인덱싱 | O(1) | ❌ | O(1) | O(n) |
| 삭제 | O(n) | O(1) | ❌ | O(1) |

### 3.2 컴프리헨션이 빠르다
```python
# 느림
result = []
for i in range(1000):
    result.append(i ** 2)

# 빠름 ✅
result = [i ** 2 for i in range(1000)]

# 더 빠름 (간단한 경우)
result = list(map(lambda x: x**2, range(1000)))
```

### 3.3 문자열 연결
```python
# ❌ 매우 느림 (n²)
result = ""
for s in strings:
    result += s

# ✅ 빠름 (n)
result = "".join(strings)

# ✅ f-string
name = "Alice"
greeting = f"Hello, {name}!"

# ✅ format
greeting = "Hello, {}!".format(name)
```

### 3.4 지역 변수 사용
```python
# 느림 (전역 검색)
import math
def slow():
    result = []
    for i in range(1000):
        result.append(math.sqrt(i))

# 빠름 (지역 참조)
def fast():
    sqrt = math.sqrt
    result = []
    for i in range(1000):
        result.append(sqrt(i))
```

### 3.5 빌트인 함수 사용
```python
# 느림
total = 0
for x in nums:
    total += x

# 빠름 ✅
total = sum(nums)

# 느림
nums = [1, 2, 3]
for n in nums:
    if n == target:
        found = True

# 빠름
found = target in nums

# 다른 빌트인: any, all, min, max, sorted, filter, map
```

### 3.6 메모이제이션
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci(100)  # 매우 빠름

# Python 3.9+
from functools import cache

@cache  # 무제한 캐시
def expensive(n):
    return n ** 2
```

### 3.7 제너레이터로 메모리 절약
```python
# 메모리 많이 사용 (전부 메모리에)
nums = [x ** 2 for x in range(10_000_000)]
total = sum(nums)

# 메모리 효율적 (lazy)
nums = (x ** 2 for x in range(10_000_000))
total = sum(nums)
```

## 4. Numpy / Pandas 로 가속

CPU 집약적 수치 계산은 numpy 를 쓰는 것이 훨씬 빠릅니다.

```python
import numpy as np
import time

# Pure Python
def py_sum_squares(n):
    return sum(i ** 2 for i in range(n))

# Numpy
def np_sum_squares(n):
    arr = np.arange(n)
    return (arr ** 2).sum()

n = 10_000_000

start = time.time()
py_sum_squares(n)
print(f"Python: {time.time() - start:.2f}s")  # ~2초

start = time.time()
np_sum_squares(n)
print(f"Numpy:  {time.time() - start:.2f}s")  # ~0.05초 (40배!)
```

## 5. JIT 컴파일러 — Numba

```bash
pip install numba
```

```python
from numba import jit
import time

@jit(nopython=True)
def fast_sum(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# 첫 호출은 컴파일 시간 포함
fast_sum(1000)

# 이후 호출은 매우 빠름
start = time.time()
fast_sum(10_000_000)
print(f"{time.time() - start:.4f}s")
```

## 6. Cython — C 확장

매우 빠르지만 빌드 단계 필요.

```cython
# example.pyx (Cython 코드 — 표준 Python 신택스가 아닙니다)
def fast_sum(int n):
    cdef int total = 0
    cdef int i
    for i in range(n):
        total += i * i
    return total
```

```python
# setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("example.pyx"))
```

```bash
python setup.py build_ext --inplace
```

## 7. 동시성으로 성능 향상

### 7.1 I/O bound → threading / asyncio
```python
import requests
from concurrent.futures import ThreadPoolExecutor

urls = ["http://example.com"] * 100

# 순차 (느림)
results = [requests.get(url).status_code for url in urls]

# 병렬 (10배 이상 빠름)
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(lambda u: requests.get(u).status_code, urls))
```

### 7.2 CPU bound → multiprocessing
```python
from concurrent.futures import ProcessPoolExecutor

def cpu_task(n):
    return sum(i ** 2 for i in range(n))

if __name__ == "__main__":
    inputs = [10**7] * 8

    # CPU 코어 수만큼 병렬
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_task, inputs))
```

## 8. 메모리 최적화

### 8.1 __slots__
```python
class Regular:
    def __init__(self):
        self.x = 1
        self.y = 2

class Slotted:
    __slots__ = ["x", "y"]
    def __init__(self):
        self.x = 1
        self.y = 2

import sys
r = Regular()
s = Slotted()

# Slotted 가 메모리 약 50% 적게 사용
```

### 8.2 제너레이터로 lazy 평가
```python
# ❌ 전체를 메모리에
lines = open("huge.log").readlines()
for line in lines:
    process(line)

# ✅ 한 줄씩
with open("huge.log") as f:
    for line in f:
        process(line)
```

### 8.3 array 모듈 (동질 배열)
```python
import array

# 일반 리스트: 객체 참조 (메모리 많음)
lst = [1, 2, 3, 4, 5]

# array: C 배열 (메모리 적음)
arr = array.array("i", [1, 2, 3, 4, 5])  # 'i' = int
```

### 8.4 __del__ 과 weakref
```python
import weakref

class Big:
    pass

# 강한 참조
big = Big()
ref = big          # big 살아있게 함

# 약한 참조
weak = weakref.ref(big)
print(weak())      # Big 객체 또는 None
del big
print(weak())      # None (가비지 컬렉션됨)
```

## 9. 최적화 사례

### 사례 1: 단어 빈도
```python
import time

# v1: 느림 (n²)
def word_freq_v1(text):
    words = text.split()
    freq = {}
    for word in words:
        if word in freq:  # 매번 검색
            freq[word] += 1
        else:
            freq[word] = 1
    return freq

# v2: dict.get
def word_freq_v2(text):
    freq = {}
    for word in text.split():
        freq[word] = freq.get(word, 0) + 1
    return freq

# v3: defaultdict
from collections import defaultdict

def word_freq_v3(text):
    freq = defaultdict(int)
    for word in text.split():
        freq[word] += 1
    return freq

# v4: Counter (가장 빠름)
from collections import Counter

def word_freq_v4(text):
    return Counter(text.split())
```

### 사례 2: 중복 제거 + 순서 유지
```python
# v1: 느림 (n²)
def unique_v1(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result

# v2: set 으로 추적 (O(n))
def unique_v2(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# v3: dict (Python 3.7+ 순서 유지)
def unique_v3(items):
    return list(dict.fromkeys(items))
```

### 사례 3: 합산
```python
import time
import numpy as np

n = 10_000_000

# v1: for 루프
def sum_v1():
    total = 0
    for i in range(n):
        total += i
    return total

# v2: sum() 빌트인
def sum_v2():
    return sum(range(n))

# v3: numpy
def sum_v3():
    return np.arange(n).sum()

# v4: math.fsum
import math
def sum_v4():
    return math.fsum(range(n))

# 측정
for name, func in [("v1", sum_v1), ("v2", sum_v2), ("v3", sum_v3)]:
    start = time.time()
    func()
    print(f"{name}: {time.time() - start:.4f}s")
```

## 10. 최적화 원칙

### "premature optimization is the root of all evil" — Donald Knuth

1. **측정 먼저**: 추측하지 말고 프로파일링
2. **80/20 규칙**: 코드의 20% 가 시간의 80% 차지
3. **알고리즘 우선**: O(n²) → O(n log n) 이 미세 최적화보다 효과적
4. **가독성 우선**: 1ms 차이 vs 유지보수
5. **C 확장 마지막**: numpy, numba, cython 은 마지막 수단

### 최적화 체크리스트
- [ ] 정말 느린가? (측정함?)
- [ ] 가장 느린 부분이 어디인가? (프로파일링)
- [ ] 알고리즘을 개선할 수 있나? (O 표기법)
- [ ] 자료구조가 적절한가? (set vs list)
- [ ] 빌트인을 활용했나? (sum, any, map)
- [ ] 캐싱이 가능한가? (lru_cache)
- [ ] 병렬화가 도움될까? (threading/multiprocessing)
- [ ] numpy 로 가속 가능한가? (수치 계산)

## 11. 실전 예제

### 예제 1: 큰 파일 처리 최적화
```python
# ❌ 메모리에 다 올림
def process_v1(filename):
    with open(filename) as f:
        lines = f.readlines()  # 전체 로드
    return sum(1 for line in lines if "ERROR" in line)

# ✅ 한 줄씩
def process_v2(filename):
    count = 0
    with open(filename) as f:
        for line in f:
            if "ERROR" in line:
                count += 1
    return count

# ✅ 더 간결
def process_v3(filename):
    with open(filename) as f:
        return sum(1 for line in f if "ERROR" in line)
```

### 예제 2: 자료구조 변환
```python
# ❌ 매번 검색
def find_duplicates_v1(items):
    duplicates = []
    for i, item in enumerate(items):
        if item in items[i+1:]:  # O(n)
            if item not in duplicates:
                duplicates.append(item)
    return duplicates
# O(n³)

# ✅ Counter 사용
from collections import Counter
def find_duplicates_v2(items):
    return [item for item, count in Counter(items).items() if count > 1]
# O(n)
```

## 📝 연습 문제

### 문제 1: 측정
같은 작업을 list vs set 으로 했을 때 시간 차이를 측정하세요.
(예: 10000개 중 5000번 멤버십 테스트)

### 문제 2: 프로파일링
복잡한 함수를 만들고 cProfile 로 분석하세요.

### 문제 3: 최적화 전후 비교
회문 판별 함수를 3가지 방식으로 구현하고 성능 비교.

### 문제 4: 메모리 비교
일반 클래스 vs __slots__ 클래스로 백만 개 객체 생성 시 메모리 비교.

### 문제 5: numpy vs Python
백만 개 숫자의 표준편차 계산. 순수 Python vs numpy 시간 비교.

## ✅ 체크리스트
- [ ] timeit 으로 측정한다
- [ ] cProfile 로 프로파일링한다
- [ ] 적절한 자료구조를 선택한다
- [ ] 빌트인 함수를 활용한다
- [ ] 제너레이터로 메모리를 절약한다
- [ ] lru_cache 로 메모이제이션한다
- [ ] CPU 작업에 numpy/numba 를 고려한다

## 🔗 다음 챕터
👉 [08. 패키징과 배포](./08-packaging.md)
