# Python 문법 치트시트

## 변수 & 타입

```python
# 변수 선언
name: str = "Kim"
age: int = 30
items: list[str] = ["a", "b"]

# 타입 확인
type(name)           # <class 'str'>
isinstance(name, str) # True

# None 체크
if value is None:    # ✅ 올바름
if value == None:    # ❌ 피하세요
```

## 컬렉션

```python
# List
items = [1, 2, 3]
items.append(4)
items.extend([5, 6])
items[0]             # 첫 번째
items[-1]            # 마지막
items[1:3]           # 슬라이싱

# Dict
d = {"a": 1, "b": 2}
d["c"] = 3
d.get("x", "default")
for k, v in d.items():

# Set
s = {1, 2, 3}
s.add(4)
s1 | s2              # 합집합
s1 & s2              # 교집합
```

## Comprehension

```python
# List Comprehension
[x**2 for x in range(10)]
[x for x in items if x > 0]

# Dict Comprehension
{k: v*2 for k, v in d.items()}

# Set Comprehension
{x**2 for x in items}

# Generator Expression
(x**2 for x in range(10))
```

## 함수

```python
# 기본 함수
def add(a: int, b: int) -> int:
    return a + b

# 기본값 인자
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# *args, **kwargs
def func(*args, **kwargs):
    pass

# 람다
square = lambda x: x ** 2
```

## 클래스

```python
# 기본 클래스
class Person:
    def __init__(self, name: str):
        self.name = name
    
    def greet(self) -> str:
        return f"Hello, {self.name}"

# dataclass
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str = ""
```

## 에러 처리

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Error: {e}")
except (TypeError, KeyError):
    pass
else:
    print("성공!")
finally:
    cleanup()
```

## Context Manager

```python
with open("file.txt") as f:
    content = f.read()

# 여러 리소스
with open("a.txt") as a, open("b.txt") as b:
    pass
```

## f-string

```python
name = "Kim"
age = 30

f"이름: {name}"
f"나이: {age:03d}"        # 003
f"값: {value:.2f}"        # 소수점 2자리
f"{name=}, {age=}"        # 디버깅용 (3.8+)
```

## 주요 내장 함수

```python
len(items)               # 길이
range(10)                # 0~9
enumerate(items)         # 인덱스와 값
zip(list1, list2)        # 병렬 순회
map(func, items)         # 매핑
filter(func, items)      # 필터링
sorted(items)            # 정렬 (새 리스트)
reversed(items)          # 역순
any(items)               # 하나라도 True
all(items)               # 모두 True
```

