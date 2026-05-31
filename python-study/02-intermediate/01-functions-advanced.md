# 01. 함수 심화 (람다/클로저/고차함수)

## 🎯 학습 목표
- 일급 객체로서의 함수를 이해한다
- 람다, 클로저, 고차함수를 활용한다
- map, filter, reduce를 사용한다
- 함수형 프로그래밍의 개념을 안다

## 1. 함수는 일급 객체 (First-Class Object)

Python에서 함수는 다른 객체처럼 다룰 수 있습니다.

```python
def greet(name):
    return f"Hello, {name}!"

# 변수에 할당
say_hi = greet
print(say_hi("Alice"))  # Hello, Alice!

# 리스트에 저장
functions = [greet, str.upper, len]
for f in functions:
    print(f("Python"))

# 딕셔너리에 저장
operations = {
    "greet": greet,
    "shout": lambda s: s.upper() + "!",
}
print(operations["shout"]("hello"))  # HELLO!
```

## 2. 람다 함수 (Lambda)

### 2.1 문법
```python
# def 문
def add(a, b):
    return a + b

# 람다 (동등)
add = lambda a, b: a + b
```

### 2.2 사용 예
```python
# 한 줄 함수
square = lambda x: x ** 2
print(square(5))  # 25

# 조건부 표현식
abs_val = lambda x: x if x >= 0 else -x

# 키 함수로 활용 (가장 흔한 패턴)
words = ["banana", "apple", "cherry"]

# 길이순 정렬
sorted_by_len = sorted(words, key=lambda w: len(w))

# 마지막 글자 순
sorted_by_last = sorted(words, key=lambda w: w[-1])

# 튜플 리스트 정렬
people = [("Alice", 25), ("Bob", 30), ("Charlie", 22)]
by_age = sorted(people, key=lambda p: p[1])
```

### 2.3 람다의 제한
```python
# ❌ 람다는 단일 표현식만 가능
# bad = lambda x: print(x); return x * 2  # 불가능

# ❌ 복잡한 로직은 def 사용
# def 가 더 명확하면 def 사용

# ✅ 람다가 적합한 경우
# - 짧고 단순한 함수
# - 즉시 한 번만 사용
# - 다른 함수에 인자로 전달
```

## 3. 고차 함수 (Higher-Order Functions)

함수를 **인자로 받거나** **반환하는** 함수입니다.

### 3.1 map() — 모든 요소에 함수 적용
```python
numbers = [1, 2, 3, 4, 5]

# map(함수, 이터러블)
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# 여러 이터러블
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print(sums)  # [11, 22, 33]

# 타입 변환
strings = ["1", "2", "3"]
ints = list(map(int, strings))
print(ints)  # [1, 2, 3]

# 💡 보통은 컴프리헨션이 더 Pythonic
squared = [x ** 2 for x in numbers]
```

### 3.2 filter() — 조건에 맞는 요소만
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 짝수만
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# None 값 제거
items = [1, None, 2, "", 3, 0, "hello"]
truthy = list(filter(None, items))  # falsy 값 제거
print(truthy)  # [1, 2, 3, 'hello']

# 💡 컴프리헨션이 더 Pythonic
evens = [x for x in numbers if x % 2 == 0]
```

### 3.3 reduce() — 누적 계산
```python
from functools import reduce

# 모든 요소의 곱
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda acc, x: acc * x, numbers)
print(product)  # 120

# 초기값 제공
total = reduce(lambda acc, x: acc + x, numbers, 100)
print(total)  # 115

# 최대값 찾기
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)  # 5
```

### 3.4 sorted() with key
```python
# 기본 정렬
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(nums))               # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(nums, reverse=True)) # [9, 6, 5, 4, 3, 2, 1, 1]

# 키 함수
words = ["apple", "Banana", "cherry"]
print(sorted(words))               # 대소문자 구분
print(sorted(words, key=str.lower))  # 무시

# 복잡한 정렬: 길이순, 같으면 알파벳순
items = ["bb", "aaa", "c", "dd"]
print(sorted(items, key=lambda x: (len(x), x)))
# ['c', 'bb', 'dd', 'aaa']
```

## 4. 클로저 (Closure)

내부 함수가 외부 함수의 변수를 **기억** 하는 것입니다.

### 4.1 기본 클로저
```python
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter

c1 = make_counter()
print(c1())  # 1
print(c1())  # 2
print(c1())  # 3

c2 = make_counter()  # 독립된 카운터
print(c2())  # 1
print(c1())  # 4 (c1은 자기 카운트 유지)
```

### 4.2 함수 팩토리
```python
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

times2 = make_multiplier(2)
times10 = make_multiplier(10)

print(times2(5))    # 10
print(times10(5))   # 50
```

### 4.3 데코레이터 (미리보기)
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"호출 전: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"호출 후: {func.__name__}")
        return result
    return wrapper

@my_decorator
def hello(name):
    print(f"Hello, {name}!")

hello("Alice")
# 호출 전: hello
# Hello, Alice!
# 호출 후: hello
```

## 5. functools 모듈

### 5.1 partial — 부분 적용
```python
from functools import partial

def power(base, exponent):
    return base ** exponent

# 일부 인자를 고정
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(3))    # 27

# 첫 인자 고정
power_of_2 = partial(power, 2)
print(power_of_2(10))  # 1024
```

### 5.2 reduce
```python
from functools import reduce

# 누적
print(reduce(lambda a, b: a + b, [1, 2, 3, 4, 5]))  # 15

# 문자열 연결
words = ["Hello", "World", "Python"]
sentence = reduce(lambda a, b: a + " " + b, words)
print(sentence)  # Hello World Python
```

### 5.3 lru_cache — 메모이제이션
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(50))  # 빠르게 계산됨!

# 캐시 정보
print(fibonacci.cache_info())
```

## 6. itertools 모듈

함수형 프로그래밍을 위한 강력한 도구들.

### 6.1 무한 이터레이터
```python
from itertools import count, cycle, repeat

# count - 무한 카운터
for i in count(10, 2):  # 10부터 2씩
    if i > 20:
        break
    print(i)  # 10, 12, 14, 16, 18, 20

# cycle - 반복
colors = cycle(["red", "green", "blue"])
for _ in range(5):
    print(next(colors))  # red, green, blue, red, green

# repeat - 같은 값 반복
for x in repeat("Hi", 3):
    print(x)  # Hi, Hi, Hi
```

### 6.2 종료 이터레이터
```python
from itertools import chain, zip_longest, islice

# chain - 연결
a = [1, 2, 3]
b = [4, 5, 6]
print(list(chain(a, b)))  # [1, 2, 3, 4, 5, 6]

# zip_longest - 긴 쪽 기준
print(list(zip_longest([1, 2, 3], ["a", "b"], fillvalue="-")))
# [(1, 'a'), (2, 'b'), (3, '-')]

# islice - 슬라이싱
print(list(islice(count(), 10)))  # [0, 1, ..., 9]
```

### 6.3 조합과 순열
```python
from itertools import combinations, permutations, product

# 조합 (순서 X)
print(list(combinations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 3)]

# 순열 (순서 O)
print(list(permutations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# 곱집합
print(list(product([1, 2], ["a", "b"])))
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
```

### 6.4 그룹화
```python
from itertools import groupby

data = [("apple", 1), ("apple", 2), ("banana", 3), ("apple", 4)]
# ⚠️ groupby는 연속된 그룹만 묶음. 미리 정렬 필요!
data.sort(key=lambda x: x[0])

for key, group in groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# apple: [('apple', 1), ('apple', 2), ('apple', 4)]
# banana: [('banana', 3)]
```

## 7. 재귀 (Recursion)

함수가 자신을 호출하는 것.

### 7.1 기본 예시
```python
def factorial(n):
    if n <= 1:           # 기저 조건 (필수!)
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120
```

### 7.2 피보나치
```python
# 단순 재귀 (느림 - O(2^n))
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

# 메모이제이션 (빠름 - O(n))
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_fast(n):
    if n < 2:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)

# 반복문으로 (가장 빠름, 메모리 적음)
def fib_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

### 7.3 재귀의 한계
```python
import sys
print(sys.getrecursionlimit())  # 보통 1000

# 깊은 재귀 시 RecursionError 발생
# 가능하면 반복문으로 변환
```

## 8. 함수형 프로그래밍 패턴

### 8.1 순수 함수 (Pure Function)
- 같은 입력 → 같은 출력
- 부수 효과(side effect) 없음

```python
# ❌ 순수 함수 아님 (외부 상태 변경)
total = 0
def add_to_total(x):
    global total
    total += x
    return total

# ✅ 순수 함수
def add(a, b):
    return a + b
```

### 8.2 불변성 (Immutability)
```python
# ❌ 원본 수정
def add_item(lst, item):
    lst.append(item)
    return lst

# ✅ 새 리스트 반환
def add_item(lst, item):
    return lst + [item]
```

### 8.3 함수 합성
```python
def compose(*funcs):
    def composed(x):
        for f in reversed(funcs):
            x = f(x)
        return x
    return composed

# f(g(h(x)))
process = compose(
    lambda x: x * 2,
    lambda x: x + 1,
    lambda x: x ** 2,
)

print(process(3))  # ((3^2) + 1) * 2 = 20
```

## 9. 실전 예제

### 예제 1: 데이터 파이프라인
```python
data = [
    {"name": "Alice", "age": 25, "salary": 50000},
    {"name": "Bob", "age": 30, "salary": 60000},
    {"name": "Charlie", "age": 35, "salary": 75000},
    {"name": "David", "age": 28, "salary": 55000},
]

# 30세 이상의 평균 연봉
result = sum(
    map(lambda p: p["salary"],
        filter(lambda p: p["age"] >= 30, data))
) / sum(1 for p in data if p["age"] >= 30)

# 더 Pythonic
salaries = [p["salary"] for p in data if p["age"] >= 30]
avg = sum(salaries) / len(salaries) if salaries else 0
print(f"평균: {avg:,.0f}")
```

### 예제 2: 함수 디스패치
```python
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b if b != 0 else None

operations = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
}

def calculate(a, op, b):
    if op in operations:
        return operations[op](a, b)
    raise ValueError(f"알 수 없는 연산자: {op}")

print(calculate(10, "+", 5))  # 15
```

## 📝 연습 문제

### 문제 1: 람다 정렬
딕셔너리 리스트를 특정 키로 정렬하는 람다를 작성하세요.

### 문제 2: 함수 합성
두 함수를 합성하여 하나의 함수로 만드는 `compose(f, g)` 를 구현하세요.

### 문제 3: 클로저 카운터
`make_counter(start=0, step=1)` 을 호출하면 호출할 때마다 증가하는 카운터를 만드세요.

### 문제 4: 메모이제이션 데코레이터
`@memoize` 데코레이터를 직접 구현하세요. (lru_cache 사용 X)

### 문제 5: map/filter/reduce
`[1, 2, 3, 4, 5]` 에서 짝수의 제곱의 합을 map/filter/reduce 만으로 구하세요.

## ✅ 체크리스트
- [ ] 람다 함수를 작성할 수 있다
- [ ] map, filter, reduce 의 차이를 안다
- [ ] 클로저의 개념을 이해한다
- [ ] functools.partial 을 활용할 수 있다
- [ ] 재귀 함수를 작성할 수 있다
- [ ] 순수 함수와 부수 효과를 이해한다

## 🔗 다음 챕터
👉 [02. 객체지향 프로그래밍 (OOP)](./02-oop.md)
