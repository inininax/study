# 05. 함수 기초

## 🎯 학습 목표
- 함수의 개념과 필요성을 이해한다
- 함수를 정의하고 호출할 수 있다
- 매개변수와 인자, 반환값을 활용할 수 있다
- 변수의 스코프를 이해한다

## 1. 함수란?

**함수(function)** 는 특정 작업을 수행하는 코드의 묶음입니다.

### 함수의 장점
- 🔁 **재사용성**: 같은 코드를 반복하지 않음
- 📦 **모듈화**: 큰 문제를 작은 단위로 분리
- 🧪 **테스트 용이**: 각 함수를 독립적으로 테스트
- 📖 **가독성**: 코드의 의도를 명확히 표현

## 2. 함수 정의와 호출

### 기본 구조
```python
def 함수이름(매개변수):
    """문서화 문자열 (docstring)"""
    # 함수 본체
    return 반환값
```

### 첫 함수
```python
def greet():
    print("안녕하세요!")

# 호출
greet()  # 안녕하세요!
greet()  # 안녕하세요!
```

### 매개변수가 있는 함수
```python
def greet(name):
    print(f"안녕하세요, {name}님!")

greet("Alice")    # 안녕하세요, Alice님!
greet("Bob")      # 안녕하세요, Bob님!
```

### 반환값이 있는 함수
```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8
```

### 여러 값 반환 (튜플)
```python
def get_min_max(numbers):
    return min(numbers), max(numbers)

low, high = get_min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(f"최소: {low}, 최대: {high}")
```

## 3. 매개변수 (Parameters)

### 3.1 위치 인자 (Positional Arguments)
```python
def divide(a, b):
    return a / b

print(divide(10, 2))  # 5.0
print(divide(2, 10))  # 0.2 (순서가 중요!)
```

### 3.2 키워드 인자 (Keyword Arguments)
```python
def introduce(name, age, city):
    print(f"{name}, {age}살, {city} 거주")

# 키워드로 명시
introduce(name="Alice", age=25, city="Seoul")
introduce(city="Busan", name="Bob", age=30)  # 순서 무관
```

### 3.3 기본값 매개변수 (Default Parameters)
```python
def greet(name, message="안녕하세요"):
    print(f"{message}, {name}님!")

greet("Alice")                    # 안녕하세요, Alice님!
greet("Bob", "반갑습니다")        # 반갑습니다, Bob님!
greet("Charlie", message="Hi")    # Hi, Charlie님!
```

> ⚠️ **주의**: 기본값으로 가변 객체(리스트, 딕셔너리 등)를 사용하지 마세요!
```python
# ❌ 위험한 패턴
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2]  ← 기대와 다름!

# ✅ 올바른 패턴
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 3.4 가변 위치 인자 (`*args`)
```python
def sum_all(*numbers):
    """가변 개수의 숫자를 받아 합을 반환"""
    total = 0
    for n in numbers:
        total += n
    return total

print(sum_all(1, 2, 3))           # 6
print(sum_all(1, 2, 3, 4, 5))     # 15
print(sum_all())                  # 0
```

### 3.5 가변 키워드 인자 (`**kwargs`)
```python
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="Seoul")
# name: Alice
# age: 25
# city: Seoul
```

### 3.6 모든 매개변수 조합
```python
def example(pos1, pos2, default="hi", *args, **kwargs):
    print(f"pos1={pos1}, pos2={pos2}, default={default}")
    print(f"args={args}, kwargs={kwargs}")

example(1, 2, "hello", 3, 4, 5, name="Alice", age=25)
# pos1=1, pos2=2, default=hello
# args=(3, 4, 5), kwargs={'name': 'Alice', 'age': 25}
```

### 3.7 키워드 전용 인자 (`*` 사용)
```python
def create_user(name, *, role="user", active=True):
    """role과 active는 반드시 키워드로 전달"""
    return {"name": name, "role": role, "active": active}

create_user("Alice")                          # OK
create_user("Bob", role="admin")              # OK
# create_user("Charlie", "admin")             # TypeError!
```

### 3.8 위치 전용 인자 (`/` 사용, Python 3.8+)
```python
def divide(a, b, /):
    """a와 b는 반드시 위치 인자로 전달"""
    return a / b

divide(10, 2)            # OK
# divide(a=10, b=2)      # TypeError!
```

## 4. return 문

### 4.1 명시적 return
```python
def square(x):
    return x ** 2

print(square(5))  # 25
```

### 4.2 return 없으면 None 반환
```python
def no_return():
    print("Hello")

result = no_return()
print(result)  # None
```

### 4.3 조기 반환 (Early Return)
```python
def divide(a, b):
    if b == 0:
        return None  # 조기 반환으로 예외 케이스 처리
    return a / b
```

## 5. 변수의 스코프 (Scope)

### 5.1 지역 변수 (Local)
```python
def my_func():
    x = 10  # 지역 변수
    print(x)

my_func()
# print(x)  # NameError: x는 함수 밖에서 접근 불가
```

### 5.2 전역 변수 (Global)
```python
count = 0  # 전역 변수

def increment():
    global count  # 전역 변수 수정 선언
    count += 1

increment()
increment()
print(count)  # 2
```

> 💡 **권장**: `global` 사용은 최소화하세요. 대신 매개변수와 반환값을 활용하세요.
```python
# ❌ 비권장
total = 0
def add(x):
    global total
    total += x

# ✅ 권장
def add(total, x):
    return total + x
```

### 5.3 LEGB 규칙
Python은 변수를 찾을 때 다음 순서로 검색합니다.

1. **L**ocal: 현재 함수
2. **E**nclosing: 감싸는 함수
3. **G**lobal: 모듈 전역
4. **B**uilt-in: 내장

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)  # local

    inner()
    print(x)      # enclosing

outer()
print(x)          # global
```

### 5.4 nonlocal 키워드
```python
def outer():
    count = 0

    def inner():
        nonlocal count  # 감싸는 함수의 변수 수정
        count += 1
        return count

    return inner

counter = outer()
print(counter())  # 1
print(counter())  # 2
```

## 6. Docstring (문서화 문자열)

함수의 설명을 적는 문자열입니다. `help()` 로 확인 가능합니다.

```python
def calculate_bmi(weight, height):
    """
    BMI(체질량지수)를 계산합니다.

    Args:
        weight (float): 체중 (kg)
        height (float): 키 (m)

    Returns:
        float: BMI 값

    Examples:
        >>> calculate_bmi(70, 1.75)
        22.86
    """
    return weight / (height ** 2)

help(calculate_bmi)  # 문서 확인
print(calculate_bmi.__doc__)
```

### Docstring 스타일
- **Google Style** (가독성)
- **NumPy Style** (과학 계산)
- **reStructuredText** (Sphinx)

## 7. 함수도 객체

Python에서 함수는 **일급 객체(First-Class Object)** 입니다.

### 변수에 할당
```python
def greet(name):
    return f"Hello, {name}!"

say_hi = greet  # 함수를 변수에 할당
print(say_hi("Alice"))  # Hello, Alice!
```

### 함수를 인자로 전달
```python
def apply(func, value):
    return func(value)

def double(x):
    return x * 2

print(apply(double, 5))  # 10
```

### 함수를 반환
```python
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

times3 = make_multiplier(3)
print(times3(10))  # 30
```

## 8. 람다 함수 (Lambda)

간단한 익명 함수를 만들 때 사용합니다.

```python
# 일반 함수
def square(x):
    return x ** 2

# 람다 함수
square = lambda x: x ** 2

print(square(5))  # 25

# 자주 쓰이는 패턴
add = lambda a, b: a + b
print(add(3, 5))  # 8

# 정렬에 활용
words = ["banana", "apple", "cherry"]
sorted_words = sorted(words, key=lambda w: len(w))
print(sorted_words)  # ['apple', 'cherry', 'banana']
```

## 9. 타입 힌트 (Type Hints)

Python 3.5+ 에서 도입된 타입 정보 표기법입니다.

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def get_user(user_id: int) -> dict:
    return {"id": user_id, "name": "Alice"}

# 기본값과 함께
def greet(name: str = "World") -> str:
    return f"Hello, {name}!"
```

> 💡 타입 힌트는 **힌트일 뿐** 강제되지 않습니다. mypy 같은 도구로 검증합니다.

## 10. 실전 예제

### 예제 1: 계산기 함수
```python
def calculator(a, b, operation="add"):
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else None,
    }

    if operation not in operations:
        return None
    return operations[operation](a, b)

print(calculator(10, 5, "add"))      # 15
print(calculator(10, 5, "multiply")) # 50
```

### 예제 2: 학점 계산
```python
def get_grade(score: int) -> str:
    """점수에 따른 학점을 반환합니다."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"

print(get_grade(85))  # B
```

### 예제 3: 통계 함수
```python
def stats(*numbers):
    """숫자들의 통계를 반환합니다."""
    if not numbers:
        return None
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "avg": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers),
    }

result = stats(10, 20, 30, 40, 50)
print(result)
```

## 📝 연습 문제

### 문제 1: 두 수 사이의 합
두 정수 a, b를 받아 a부터 b까지의 합을 반환하는 함수를 작성하세요.

### 문제 2: 팩토리얼
n의 팩토리얼을 계산하는 함수를 작성하세요. (n! = n × (n-1) × ... × 1)

### 문제 3: 회문 판별
문자열이 회문(palindrome)인지 판별하는 함수를 작성하세요. (예: "level", "racecar")

### 문제 4: 평균 계산
가변 인자로 숫자들을 받아 평균을 계산하는 함수를 작성하세요.

### 문제 5: 함수 합성
두 함수 f, g를 받아 `f(g(x))` 를 계산하는 함수를 작성하세요.

## ✅ 체크리스트
- [ ] 함수를 정의하고 호출할 수 있다
- [ ] 매개변수와 인자를 구별할 수 있다
- [ ] 기본값, *args, **kwargs를 사용할 수 있다
- [ ] return 으로 값을 반환할 수 있다
- [ ] 지역/전역 변수의 차이를 안다
- [ ] 람다 함수를 작성할 수 있다
- [ ] docstring 을 작성한다

## 🔗 다음 챕터
👉 [06. 자료구조](./06-data-structures.md)
