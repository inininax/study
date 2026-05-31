# Python 성능 치트시트

## 시간 복잡도

| 자료구조 | 조회 | 삽입 | 삭제 | 검색 |
|----------|------|------|------|------|
| list | O(1) | O(1)* | O(n) | O(n) |
| dict | O(1) | O(1) | O(1) | O(1) |
| set | - | O(1) | O(1) | O(1) |
| deque | O(n) | O(1)** | O(1)** | O(n) |

*끝에 삽입 / **양끝 삽입/삭제

## Comprehension vs for문

```python
# ✅ 더 빠름 (내부 최적화)
squares = [x**2 for x in range(1000)]

# ❌ 더 느림
squares = []
for x in range(1000):
    squares.append(x**2)
```

## Generator vs List

```python
# ✅ 메모리 효율적 (대용량 데이터)
gen = (x**2 for x in range(1000000))

# ❌ 메모리 많이 사용
lst = [x**2 for x in range(1000000)]

# 한 번만 순회하면 Generator
# 여러 번 순회하면 List
```

## 문자열 연결

```python
# ❌ 느림 (매번 새 객체)
s = ""
for word in words:
    s += word

# ✅ 빠름
s = "".join(words)

# ✅ f-string (가독성)
s = f"{first} {second}"
```

## dict 조회 최적화

```python
# ❌ 두 번 조회
if key in d:
    value = d[key]

# ✅ 한 번 조회
value = d.get(key)
if value is not None:
    ...

# ✅ 또는
try:
    value = d[key]
except KeyError:
    ...
```

## 멤버십 테스트

```python
# ❌ 느림 - O(n)
if item in some_list:
    ...

# ✅ 빠름 - O(1)
some_set = set(some_list)
if item in some_set:
    ...
```

## __slots__ 메모리 최적화

```python
# 일반 클래스: __dict__ 사용
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# __slots__: 메모리 절약 (~40%)
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

## 프로파일링

```bash
# 시간 프로파일링
python -m cProfile -s tottime script.py

# 라인별 프로파일링
pip install line_profiler
kernprof -l -v script.py

# 메모리 프로파일링
pip install memory_profiler
python -m memory_profiler script.py
```

## 동시성 선택 가이드

```
I/O 바운드 (네트워크, 파일):
  → asyncio (권장)
  → threading
  
CPU 바운드 (계산):
  → multiprocessing
  → ProcessPoolExecutor
  
❌ CPU 바운드에 threading 사용하지 마세요 (GIL)
```

## 캐싱

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    # 복잡한 계산
    return result

# Python 3.9+ functools.cache (무제한)
from functools import cache

@cache
def expensive_function(n):
    return result
```

## 주요 최적화 팁

| 상황 | 최적화 |
|------|--------|
| 리스트 검색 많음 | set으로 변환 |
| 문자열 연결 많음 | "".join() 사용 |
| 대용량 데이터 순회 | Generator 사용 |
| 함수 반복 호출 | @lru_cache 사용 |
| CPU 집약 작업 | multiprocessing |
| I/O 대기 많음 | asyncio |
| 많은 객체 생성 | __slots__ 사용 |
| 정렬 | sorted(key=) 활용 |

