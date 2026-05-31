# 07. 컴프리헨션과 제너레이터

## 🎯 학습 목표
- 리스트/딕셔너리/셋 컴프리헨션을 활용한다
- 제너레이터의 개념과 동작 원리를 이해한다
- yield 문을 활용한다
- 이터레이터 프로토콜을 안다

## 1. 컴프리헨션 (Comprehension)

**간결하고 Pythonic한** 컬렉션 생성 방식.

### 1.1 리스트 컴프리헨션
```python
# 일반 방식
squares = []
for x in range(10):
    squares.append(x ** 2)

# 컴프리헨션 (한 줄!)
squares = [x ** 2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### 1.2 조건 필터링
```python
# 짝수의 제곱
evens_squared = [x ** 2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# 양수만
positives = [x for x in [-2, -1, 0, 1, 2] if x > 0]
# [1, 2]
```

### 1.3 조건부 표현식
```python
# x 가 짝수면 2배, 홀수면 그대로
result = [x * 2 if x % 2 == 0 else x for x in range(5)]
# [0, 1, 4, 3, 8]
```

> ⚠️ `if` 의 위치 주의!
> - `[x for x in ... if 조건]` : 필터
> - `[x if 조건 else y for x in ...]` : 변환

### 1.4 중첩 반복
```python
# 곱셈표
mult_table = [(i, j, i * j) for i in range(1, 4) for j in range(1, 4)]

# 평탄화 (flatten)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 2차원 행렬 생성
matrix = [[i * j for j in range(3)] for i in range(3)]
```

### 1.5 딕셔너리 컴프리헨션
```python
# {키: 값 for ...}
squares = {x: x ** 2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 딕셔너리 변환
prices = {"apple": 1000, "banana": 500, "cherry": 3000}
sale = {fruit: price * 0.8 for fruit, price in prices.items()}

# 키-값 뒤집기
inv = {v: k for k, v in prices.items()}

# 필터
expensive = {k: v for k, v in prices.items() if v > 1000}
```

### 1.6 셋 컴프리헨션
```python
# {값 for ...}
unique_lengths = {len(w) for w in ["apple", "banana", "kiwi"]}
# {5, 6, 4}

# 중복 제거 + 변환
chars = {c.upper() for c in "Hello"}
# {'H', 'E', 'L', 'O'}
```

### 1.7 컴프리헨션 vs 함수형
```python
nums = [1, 2, 3, 4, 5]

# map + filter
result = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, nums)))

# 컴프리헨션 (더 Pythonic ✅)
result = [x ** 2 for x in nums if x % 2 == 0]
```

### 1.8 가독성 주의!
```python
# ❌ 너무 복잡한 컴프리헨션
result = [x*y for x in range(10) if x > 2 for y in range(10) if y < 5 if x*y > 8]

# ✅ 차라리 for 문으로
result = []
for x in range(10):
    if x <= 2:
        continue
    for y in range(10):
        if y >= 5:
            continue
        if x * y <= 8:
            continue
        result.append(x * y)
```

> 💡 한 줄에 들어가지 않으면 일반 for 문을 사용하세요.

## 2. 제너레이터 (Generator)

값을 **하나씩 생산**하는 함수/객체. 메모리 효율적!

### 2.1 제너레이터 표현식
```python
# 리스트 컴프리헨션 → 메모리에 모두 저장
squares_list = [x ** 2 for x in range(1000000)]  # 수십 MB

# 제너레이터 표현식 → 필요할 때만 생성
squares_gen = (x ** 2 for x in range(1000000))   # 거의 0 MB

# 사용
for s in squares_gen:
    if s > 100:
        break
    print(s)
```

### 2.2 제너레이터 함수 (yield)
```python
def counter(start, end):
    current = start
    while current < end:
        yield current
        current += 1

# 사용
for n in counter(1, 5):
    print(n)
# 1, 2, 3, 4

# 또는
gen = counter(1, 5)
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
```

### 2.3 yield 동작 원리
```python
def my_gen():
    print("start")
    yield 1
    print("after first yield")
    yield 2
    print("after second yield")
    yield 3
    print("end")

gen = my_gen()
print(next(gen))  # start \n 1
print(next(gen))  # after first yield \n 2
print(next(gen))  # after second yield \n 3
# print(next(gen)) # StopIteration!
```

### 2.4 무한 시퀀스
```python
def naturals():
    n = 1
    while True:
        yield n
        n += 1

# 처음 10개
nat = naturals()
for _ in range(10):
    print(next(nat))

# 활용: 첫 100개 소수
def primes():
    n = 2
    while True:
        if all(n % i != 0 for i in range(2, int(n**0.5) + 1)):
            yield n
        n += 1

p = primes()
first_100 = [next(p) for _ in range(100)]
```

### 2.5 fibonacci 제너레이터
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for _ in range(10):
    print(next(fib), end=" ")
# 0 1 1 2 3 5 8 13 21 34
```

### 2.6 yield from — 위임
```python
def chain(*iterables):
    for it in iterables:
        yield from it  # for x in it: yield x 와 동등

print(list(chain([1, 2], [3, 4], [5, 6])))
# [1, 2, 3, 4, 5, 6]
```

### 2.7 제너레이터에 값 보내기 (send)
```python
def echo():
    while True:
        received = yield
        print(f"받음: {received}")

gen = echo()
next(gen)  # 시작
gen.send("hello")  # 받음: hello
gen.send("world")  # 받음: world
```

## 3. 이터레이터 (Iterator)

### 3.1 이터러블 vs 이터레이터
- **이터러블(Iterable)**: `__iter__()` 메서드를 가짐 (list, tuple, dict, str 등)
- **이터레이터(Iterator)**: `__iter__()` 와 `__next__()` 메서드를 가짐

```python
lst = [1, 2, 3]              # 이터러블
it = iter(lst)               # 이터레이터 생성
print(next(it))              # 1
print(next(it))              # 2
print(next(it))              # 3
# print(next(it))            # StopIteration
```

### 3.2 직접 이터레이터 만들기
```python
class Squares:
    def __init__(self, max_n):
        self.max_n = max_n
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n >= self.max_n:
            raise StopIteration
        result = self.n ** 2
        self.n += 1
        return result

# 사용
for s in Squares(5):
    print(s)  # 0, 1, 4, 9, 16
```

### 3.3 클래스로 이터러블 만들기
```python
class Counter:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        # 새 이터레이터 반환
        current = self.start
        while current < self.end:
            yield current
            current += 1

# 여러 번 순회 가능
c = Counter(1, 4)
print(list(c))  # [1, 2, 3]
print(list(c))  # [1, 2, 3]  (다시 가능)
```

## 4. 컴프리헨션 vs 제너레이터 vs map/filter

```python
data = range(10)

# 1. 리스트 컴프리헨션
squares_list = [x ** 2 for x in data if x % 2 == 0]
# 메모리에 즉시 모두 저장

# 2. 제너레이터 표현식
squares_gen = (x ** 2 for x in data if x % 2 == 0)
# 필요할 때 생성 (lazy)

# 3. map + filter
squares_map = map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, data))
# 제너레이터와 비슷 (lazy)
```

| 방식 | 메모리 | 속도 | 가독성 | 재사용 |
|------|--------|------|--------|--------|
| 리스트 | 많음 | 빠름 | 좋음 | ✅ |
| 제너레이터 | 적음 | 보통 | 좋음 | ❌ (한 번만) |
| map/filter | 적음 | 보통 | 보통 | ❌ |

## 5. 사용 시점

### 리스트 컴프리헨션 사용
- 결과를 여러 번 순회해야 할 때
- 인덱스로 접근해야 할 때
- 길이를 알아야 할 때
- 작은 데이터

```python
data = [x ** 2 for x in range(100)]
print(len(data))   # OK
print(data[50])    # OK
```

### 제너레이터 사용
- 데이터가 매우 클 때
- 한 번만 순회하면 될 때
- 무한 시퀀스가 필요할 때
- 메모리가 제한적일 때

```python
# 큰 파일 읽기
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()

# 메모리 효율적
for line in read_large_file("huge.log"):
    if "ERROR" in line:
        print(line)
```

## 6. 실전 예제

### 예제 1: 큰 파일 처리
```python
def process_csv(path):
    """메모리 효율적인 CSV 처리"""
    with open(path, encoding="utf-8") as f:
        header = next(f).strip().split(",")
        for line in f:
            values = line.strip().split(",")
            yield dict(zip(header, values))

# 1GB 파일도 메모리 적게 사용
for row in process_csv("big_data.csv"):
    if row["status"] == "active":
        process(row)
```

### 예제 2: 페이지네이션
```python
def paginate(items, page_size):
    """리스트를 페이지로 나눔"""
    for i in range(0, len(items), page_size):
        yield items[i:i + page_size]

data = list(range(25))
for page_num, page in enumerate(paginate(data, 10), 1):
    print(f"Page {page_num}: {page}")
# Page 1: [0, 1, ..., 9]
# Page 2: [10, 11, ..., 19]
# Page 3: [20, 21, ..., 24]
```

### 예제 3: 단어 통계
```python
from collections import Counter

def word_counts(filename):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            for word in line.split():
                yield word.lower()

# Counter 와 결합
counter = Counter(word_counts("article.txt"))
print(counter.most_common(10))
```

### 예제 4: 윈도우 슬라이딩
```python
from collections import deque

def sliding_window(iterable, n):
    """크기 n의 슬라이딩 윈도우"""
    it = iter(iterable)
    window = deque(maxlen=n)
    for x in it:
        window.append(x)
        if len(window) == n:
            yield tuple(window)

for w in sliding_window([1, 2, 3, 4, 5], 3):
    print(w)
# (1, 2, 3)
# (2, 3, 4)
# (3, 4, 5)
```

### 예제 5: 트리 순회
```python
def walk_tree(tree):
    """트리를 깊이 우선으로 순회"""
    yield tree["value"]
    for child in tree.get("children", []):
        yield from walk_tree(child)

tree = {
    "value": 1,
    "children": [
        {"value": 2, "children": [
            {"value": 4},
            {"value": 5},
        ]},
        {"value": 3, "children": [
            {"value": 6},
        ]},
    ]
}

print(list(walk_tree(tree)))  # [1, 2, 4, 5, 3, 6]
```

### 예제 6: 무한 데이터 처리
```python
from itertools import islice

def random_data():
    import random
    while True:
        yield random.randint(1, 100)

# 처음 10개만
first_10 = list(islice(random_data(), 10))

# 조건 만족할 때까지
for x in random_data():
    if x > 95:
        print(f"찾음: {x}")
        break
```

## 7. itertools 와 결합

```python
from itertools import takewhile, dropwhile, accumulate

# takewhile: 조건 거짓이 될 때까지
nums = [1, 4, 6, 8, 3, 7]
print(list(takewhile(lambda x: x < 7, nums)))
# [1, 4, 6]

# dropwhile: 조건 거짓이 될 때까지 건너뜀
print(list(dropwhile(lambda x: x < 7, nums)))
# [8, 3, 7]

# accumulate: 누적
print(list(accumulate([1, 2, 3, 4, 5])))
# [1, 3, 6, 10, 15]
```

## 📝 연습 문제

### 문제 1: 짝수 제곱
1-20 중 짝수만 골라 제곱한 리스트를 컴프리헨션으로 만드세요.

### 문제 2: 단어 길이 딕셔너리
단어 리스트를 받아 `{단어: 길이}` 딕셔너리를 만드세요.

### 문제 3: 평면화
중첩 리스트 `[[1,2],[3,4],[5,6]]` 을 `[1,2,3,4,5,6]` 으로 평면화하세요.

### 문제 4: 무한 카운터
0부터 시작해서 1씩 증가하는 무한 카운터 제너레이터를 만드세요.

### 문제 5: 제너레이터로 파일 그렙
파일 경로와 패턴을 받아 패턴이 포함된 줄만 yield 하는 제너레이터를 작성하세요.

### 문제 6: 짝 만들기
리스트에서 인접한 두 요소의 쌍을 yield 하는 제너레이터를 작성하세요.
`[1, 2, 3, 4]` → `(1, 2), (2, 3), (3, 4)`

## ✅ 체크리스트
- [ ] 리스트 컴프리헨션을 자유롭게 쓴다
- [ ] 딕셔너리/셋 컴프리헨션을 안다
- [ ] yield 와 제너레이터를 이해한다
- [ ] 제너레이터 vs 리스트의 차이를 안다
- [ ] yield from 을 활용한다
- [ ] 큰 데이터 처리에 제너레이터를 사용한다

## 🔗 다음 챕터
👉 [08. 유용한 표준 라이브러리](./08-stdlib.md)
