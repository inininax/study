# 05. 타입 힌트와 정적 분석

## 🎯 학습 목표
- 타입 힌트 문법을 자유롭게 사용한다
- 복잡한 타입을 표현할 수 있다
- mypy 로 정적 분석을 수행한다
- 제네릭과 프로토콜을 이해한다

## 1. 타입 힌트 기본

### 1.1 왜 타입 힌트?
- 📖 **문서화**: 코드의 의도가 명확해짐
- 🐛 **버그 예방**: 정적 분석으로 타입 오류 사전 감지
- 🤖 **IDE 지원**: 자동완성, 리팩토링 향상
- ⚡ **성능**: 런타임에는 영향 없음 (선택적)

### 1.2 기본 문법
```python
# 변수
name: str = "Alice"
age: int = 25
pi: float = 3.14
is_active: bool = True

# 함수
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

# 반환값 없음
def print_hello() -> None:
    print("Hello!")
```

> 💡 타입 힌트는 **런타임에 검사하지 않습니다.** mypy 같은 도구로 검증.

### 1.3 기본 타입
```python
# Python 3.9+ 부터는 내장 타입 직접 사용
names: list[str] = ["Alice", "Bob"]
ages: dict[str, int] = {"Alice": 25}
point: tuple[int, int] = (3, 4)
unique: set[int] = {1, 2, 3}

# Python 3.8 이하: typing 모듈
from typing import List, Dict, Tuple, Set
names: List[str] = ["Alice", "Bob"]
```

## 2. 복잡한 타입

### 2.1 Optional / None
```python
from typing import Optional

# 둘 다 동등 (Python 3.10+)
def find_user(id: int) -> Optional[str]:
    ...

def find_user(id: int) -> str | None:
    ...
```

### 2.2 Union — 여러 타입
```python
from typing import Union

# Python 3.10+ : |
def process(value: int | str) -> str:
    return str(value)

# Python 3.9 이하: Union
def process(value: Union[int, str]) -> str:
    return str(value)
```

### 2.3 Any — 모든 타입
```python
from typing import Any

def get_value() -> Any:
    return some_data
# Any 는 타입 체크를 비활성화함. 가능하면 피하세요.
```

### 2.4 Literal — 특정 값
```python
from typing import Literal

def open_file(mode: Literal["r", "w", "a"]) -> None:
    ...

open_file("r")     # OK
open_file("rb")    # 타입 에러
```

### 2.5 Final — 변경 불가
```python
from typing import Final

MAX_SIZE: Final = 100
MAX_SIZE = 200       # 타입 에러 (mypy)

class Config:
    PI: Final[float] = 3.14159
```

### 2.6 Callable — 호출 가능
```python
from typing import Callable

def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

apply(lambda x, y: x + y, 1, 2)

# 인자/반환 타입 미지정
def use(fn: Callable) -> None:
    fn()
```

## 3. 컬렉션 타입

### 3.1 List, Tuple, Dict, Set
```python
# 동형 컬렉션
names: list[str] = []
counts: dict[str, int] = {}

# 이형 튜플
record: tuple[str, int, float] = ("Alice", 25, 165.5)

# 가변 길이 튜플
many: tuple[int, ...] = (1, 2, 3, 4, 5)
```

### 3.2 Sequence, Mapping, Iterable
구체적 타입 대신 추상 타입 사용 시.

```python
from typing import Sequence, Mapping, Iterable

# 더 일반적 (list, tuple 모두 받음)
def process(items: Sequence[int]) -> int:
    return sum(items)

# dict, OrderedDict 모두 받음
def show(data: Mapping[str, int]) -> None:
    for k, v in data.items():
        print(f"{k}: {v}")

# 어떤 iterable 든
def total(nums: Iterable[int]) -> int:
    return sum(nums)
```

## 4. 클래스와 타입 힌트

### 4.1 클래스 자체를 타입으로
```python
class User:
    def __init__(self, name: str) -> None:
        self.name = name

def find_user(name: str) -> User | None:
    ...

def greet(user: User) -> str:
    return f"Hello, {user.name}!"
```

### 4.2 자기 자신 참조 (Forward Reference)
```python
from __future__ import annotations  # Python 3.10+ 기본

class Node:
    def __init__(self, value: int, next: Node | None = None) -> None:
        self.value = value
        self.next = next
```

Python 3.10 미만:
```python
class Node:
    def __init__(self, value: int, next: "Node" | None = None) -> None:
        ...
```

### 4.3 Self (Python 3.11+)
```python
from typing import Self

class Builder:
    def add(self, item: str) -> Self:
        self.items.append(item)
        return self

class SpecialBuilder(Builder):
    pass

b = SpecialBuilder().add("x")  # SpecialBuilder 타입으로 추론
```

## 5. 제네릭 (Generics)

### 5.1 TypeVar
```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

first([1, 2, 3])         # int
first(["a", "b"])        # str
```

### 5.2 제약 (Constraints)
```python
from typing import TypeVar

# Number 는 int 나 float 만
Number = TypeVar("Number", int, float)

def average(values: list[Number]) -> Number:
    return sum(values) / len(values)

# 또는 bound (상위 타입 제한)
class Comparable:
    def __lt__(self, other): ...

C = TypeVar("C", bound=Comparable)

def maximum(items: list[C]) -> C:
    return max(items)
```

### 5.3 제네릭 클래스 (Python 3.12+)
```python
# Python 3.12+ 새 문법
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

s: Stack[int] = Stack()
s.push(1)

# Python 3.11 이하
from typing import Generic, TypeVar
T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()
```

## 6. 프로토콜 (Protocol) — 구조적 타이핑

덕 타이핑을 정적 타입에 적용.

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing square")

def render(shape: Drawable) -> None:
    shape.draw()

# 상속 없이도 Drawable 로 인정됨!
render(Circle())
render(Square())
```

### 표준 프로토콜
```python
from typing import Iterator, Iterable, Sized, Hashable

class Container:
    def __iter__(self) -> Iterator[int]: ...
    def __len__(self) -> int: ...
    def __contains__(self, item) -> bool: ...
    def __hash__(self) -> int: ...
```

## 7. TypedDict — 구조화된 dict

```python
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    email: str

def greet_user(u: User) -> str:
    return f"Hello, {u['name']}!"

user: User = {"name": "Alice", "age": 25, "email": "a@x.com"}

# Optional 키 (Python 3.11+)
class Config(TypedDict):
    host: str
    port: int

class ConfigWithOptional(Config, total=False):  # 모두 optional
    debug: bool
    verbose: bool
```

## 8. NewType — 별칭

```python
from typing import NewType

UserId = NewType("UserId", int)
ProductId = NewType("ProductId", int)

def get_user(uid: UserId) -> str: ...
def get_product(pid: ProductId) -> str: ...

uid = UserId(123)
pid = ProductId(456)

# get_user(pid)  # 타입 에러! (둘 다 int 지만 다른 타입)
get_user(uid)    # OK
```

## 9. 타입 별칭 (Type Alias)

```python
# Python 3.12+ 새 문법
type Vector = list[float]
type Point = tuple[float, float]
type Matrix = list[list[float]]

def scale(v: Vector, factor: float) -> Vector:
    return [x * factor for x in v]

# Python 3.11 이하
from typing import TypeAlias

Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]
```

## 10. ParamSpec — 데코레이터 타입

```python
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec("P")
T = TypeVar("T")

def log_calls(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"호출: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a: int, b: int) -> int:
    return a + b

result: int = add(1, 2)  # 타입 보존됨
```

## 11. mypy — 정적 타입 검사

### 11.1 설치 및 사용
```bash
pip install mypy

# 파일 검사
mypy script.py

# 디렉토리 검사
mypy src/

# 설정 (pyproject.toml)
[tool.mypy]
strict = true
python_version = "3.12"
```

### 11.2 검사 예시
```python
# example.py
def add(a: int, b: int) -> int:
    return a + b

result: str = add(1, 2)  # 에러: int -> str
```

```bash
$ mypy example.py
example.py:4: error: Incompatible types in assignment (expression has type "int", variable has type "str")
```

### 11.3 점진적 도입
```python
from typing import Any

# 일부만 타입 힌트
def process(data: list[dict[str, Any]]) -> int:
    return len(data)

# 기존 코드는 그대로
def legacy_function(x, y):
    return x + y
```

### 11.4 mypy 옵션
```ini
# mypy.ini 또는 pyproject.toml
[mypy]
python_version = 3.12
disallow_untyped_defs = true       # 모든 함수에 타입 필수
warn_return_any = true             # Any 반환 경고
warn_unused_ignores = true
strict_optional = true             # None 엄격 체크
no_implicit_optional = true
```

## 12. 런타임 타입 검증

mypy 와 별개로, 런타임에 타입을 검증하고 싶다면.

### 12.1 isinstance
```python
def process(value: int | str) -> str:
    if isinstance(value, int):
        return str(value * 2)
    return value.upper()
```

### 12.2 pydantic (강력 추천)
```python
from pydantic import BaseModel, EmailStr, Field, validator

class User(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=150)
    email: EmailStr
    tags: list[str] = []

    @validator("name")
    def name_must_be_capitalized(cls, v):
        if not v[0].isupper():
            raise ValueError("이름은 대문자로 시작")
        return v

# 자동 검증 + 타입 변환
u = User(name="Alice", age=25, email="a@example.com")
# u = User(name="alice", age=-1, email="invalid")  # ValidationError
```

## 13. 실전 예제

### 예제 1: 잘 타입된 함수
```python
from typing import Iterable

def average(numbers: Iterable[float]) -> float | None:
    nums = list(numbers)
    if not nums:
        return None
    return sum(nums) / len(nums)

result: float | None = average([1.0, 2.0, 3.0])
```

### 예제 2: 제네릭 컨테이너
```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Cache(Generic[T]):
    def __init__(self) -> None:
        self._data: dict[str, T] = {}

    def get(self, key: str) -> T | None:
        return self._data.get(key)

    def set(self, key: str, value: T) -> None:
        self._data[key] = value

# 사용
user_cache: Cache[dict] = Cache()
user_cache.set("alice", {"age": 25})

int_cache: Cache[int] = Cache()
int_cache.set("count", 42)
# int_cache.set("count", "hello")  # 타입 에러
```

### 예제 3: 프로토콜로 인터페이스
```python
from typing import Protocol

class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...
    def __eq__(self, other) -> bool: ...

def sort_items[T: Comparable](items: list[T]) -> list[T]:
    return sorted(items)
```

## 14. 타입 힌트 베스트 프랙티스

### Do ✅
```python
# 모든 public 함수에 타입 힌트
def process(data: list[dict[str, str]]) -> int:
    ...

# Optional 명시
def find(id: int) -> User | None:
    ...

# 추상 타입 사용
def total(items: Iterable[int]) -> int:
    ...
```

### Don't ❌
```python
# Any 남용
def process(data: Any) -> Any:  # 타입 없는 거나 마찬가지
    ...

# 너무 구체적
def process(items: list[int]) -> int:  # tuple 받을 수 있으면 Iterable
    ...
```

## 📝 연습 문제

### 문제 1: 기본 타입 힌트
다음 함수에 타입 힌트를 추가하세요.
```python
def greet(name, greetings):
    return f"{greetings}, {name}!"
```

### 문제 2: Optional
사용자 ID 로 사용자 정보를 찾되, 없으면 None 을 반환하는 함수에 타입 힌트를 추가하세요.

### 문제 3: 제네릭
스택(LIFO) 자료구조를 제네릭으로 구현하세요.

### 문제 4: TypedDict
사용자 정보 dict 의 구조를 TypedDict 로 정의하세요.

### 문제 5: Protocol
"길이를 가진" 객체를 표현하는 Protocol 을 만들고, 길이를 출력하는 함수를 작성하세요.

## ✅ 체크리스트
- [ ] 기본 타입 힌트를 사용한다
- [ ] Optional, Union 을 안다
- [ ] 컬렉션 타입을 표현할 수 있다
- [ ] 제네릭과 TypeVar 를 이해한다
- [ ] Protocol 의 용도를 안다
- [ ] mypy 로 정적 검사를 한다

## 🔗 다음 챕터
👉 [06. 테스팅 (pytest, TDD)](./06-testing.md)
