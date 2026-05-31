# 01. 데코레이터 심화

## 🎯 학습 목표
- 데코레이터의 동작 원리를 이해한다
- 인자가 있는 데코레이터를 만든다
- 클래스 기반 데코레이터를 만든다
- 자주 쓰이는 데코레이터 패턴을 안다

## 1. 데코레이터 복습

**데코레이터(Decorator)** 는 함수를 감싸 동작을 추가하는 함수입니다.

### 1.1 기본 구조
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # 함수 호출 전
        result = func(*args, **kwargs)
        # 함수 호출 후
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# = greet = my_decorator(greet)
```

### 1.2 동작 원리
```python
# @ 문법
@my_decorator
def hello():
    pass

# 위와 동일
def hello():
    pass
hello = my_decorator(hello)
```

## 2. functools.wraps 의 중요성

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)                # ← 필수!
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """인사 함수"""
    pass

print(greet.__name__)       # greet (wraps 없으면 'wrapper')
print(greet.__doc__)        # "인사 함수"
```

## 3. 인자가 있는 데코레이터

3중 함수 구조가 필요합니다.

```python
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("Hello!")

hello()
# Hello!
# Hello!
# Hello!
```

### 동작 분석
```python
# @repeat(3) 은 다음과 동등:
# hello = repeat(3)(hello)
# = decorator(hello)
# = wrapper
```

## 4. 인자가 있어도 없어도 되는 데코레이터

```python
from functools import wraps

def smart_decorator(func=None, *, prefix=">>>"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(prefix, end=" ")
            return f(*args, **kwargs)
        return wrapper

    if func is None:
        return decorator
    return decorator(func)

@smart_decorator
def hello1():
    print("Hello1")

@smart_decorator(prefix="!!!")
def hello2():
    print("Hello2")

hello1()    # >>> Hello1
hello2()    # !!! Hello2
```

## 5. 클래스 기반 데코레이터

### 5.1 인스턴스를 호출 가능하게
```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} 호출 횟수: {self.count}")
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    print("Hello!")

hello()    # hello 호출 횟수: 1, Hello!
hello()    # hello 호출 횟수: 2, Hello!
print(hello.count)  # 2
```

### 5.2 인자 받는 클래스 데코레이터
```python
class Repeat:
    def __init__(self, times):
        self.times = times

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(self.times):
                result = func(*args, **kwargs)
            return result
        return wrapper

@Repeat(times=3)
def greet(name):
    print(f"Hi, {name}!")

greet("Alice")
```

## 6. 자주 쓰이는 데코레이터 패턴

### 6.1 실행 시간 측정
```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()
```

### 6.2 로깅
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"호출: {func.__name__}({args}, {kwargs})")
        try:
            result = func(*args, **kwargs)
            logger.info(f"반환: {result}")
            return result
        except Exception as e:
            logger.exception(f"에러: {e}")
            raise
    return wrapper

@log_calls
def divide(a, b):
    return a / b
```

### 6.3 메모이제이션
```python
def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache  # 외부에서 확인 가능
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(50))    # 매우 빠름!
```

> 💡 보통은 `functools.lru_cache` 또는 `functools.cache` (3.9+) 사용

### 6.4 재시도
```python
import time

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(f"시도 {attempt} 실패: {e}, {delay}초 후 재시도")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2, exceptions=(ConnectionError,))
def fetch_data():
    # 외부 API 호출 등
    pass
```

### 6.5 인증/권한 체크
```python
def require_auth(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get("authenticated"):
            raise PermissionError("로그인이 필요합니다")
        return func(user, *args, **kwargs)
    return wrapper

def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != role:
                raise PermissionError(f"{role} 권한이 필요합니다")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_auth
@require_role("admin")
def delete_user(user, user_id):
    print(f"Deleting user {user_id}")
```

### 6.6 입력 검증
```python
def validate_types(**type_specs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for name, expected_type in type_specs.items():
                value = kwargs.get(name)
                if value is not None and not isinstance(value, expected_type):
                    raise TypeError(
                        f"{name}는 {expected_type.__name__}여야 합니다"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(age=int, name=str)
def create_user(name, age):
    return {"name": name, "age": age}

create_user(name="Alice", age=25)     # OK
# create_user(name="Bob", age="20")   # TypeError
```

### 6.7 속도 제한 (Rate Limit)
```python
import time
from collections import deque

def rate_limit(max_calls, period):
    def decorator(func):
        calls = deque()

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # 윈도우 밖의 호출 제거
            while calls and calls[0] < now - period:
                calls.popleft()

            if len(calls) >= max_calls:
                wait = period - (now - calls[0])
                raise RuntimeError(f"속도 제한 초과. {wait:.1f}초 후 재시도")

            calls.append(now)
            return func(*args, **kwargs)

        return wrapper
    return decorator

@rate_limit(max_calls=3, period=10)  # 10초에 3회
def api_call():
    print("API 호출")
```

## 7. 데코레이터 스택

여러 데코레이터를 함께 사용할 수 있습니다.

```python
@timer
@log_calls
@retry(max_attempts=3)
def process(data):
    return data * 2

# 적용 순서: process = timer(log_calls(retry(3)(process)))
# 호출 순서: timer → log_calls → retry → process
```

## 8. 메서드 데코레이터

### 8.1 @staticmethod / @classmethod
```python
class MyClass:
    @staticmethod
    def static_func(x, y):
        return x + y

    @classmethod
    def class_func(cls):
        return cls.__name__

    def instance_func(self):
        return id(self)
```

### 8.2 @property
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError
        self._radius = value

    @radius.deleter
    def radius(self):
        del self._radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2
```

### 8.3 @cached_property
```python
from functools import cached_property

class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    @cached_property
    def expensive_result(self):
        print("계산 중...")
        return sum(x ** 2 for x in self.data)

a = DataAnalyzer(range(1000000))
print(a.expensive_result)  # 계산 중... (오래 걸림)
print(a.expensive_result)  # 즉시 반환 (캐시됨)
```

## 9. 클래스 데코레이터

클래스 자체를 데코레이트할 수도 있습니다.

```python
def add_repr(cls):
    """클래스에 자동으로 __repr__ 추가"""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

print(Point(3, 4))  # Point(x=3, y=4)
```

### singleton 패턴
```python
def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Database:
    def __init__(self):
        print("DB 연결")

db1 = Database()  # DB 연결
db2 = Database()  # (이미 있음)
print(db1 is db2)  # True
```

## 10. 표준 데코레이터들

| 데코레이터 | 용도 |
|-----------|------|
| `@staticmethod` | 정적 메서드 |
| `@classmethod` | 클래스 메서드 |
| `@property` | getter |
| `@functools.wraps` | 메타데이터 보존 |
| `@functools.lru_cache` | 메모이제이션 (제한적) |
| `@functools.cache` | 메모이제이션 (Python 3.9+) |
| `@functools.cached_property` | 계산된 속성 캐싱 |
| `@functools.total_ordering` | 비교 메서드 자동 생성 |
| `@functools.singledispatch` | 타입 기반 함수 디스패치 |
| `@contextlib.contextmanager` | 컨텍스트 매니저 |
| `@dataclasses.dataclass` | 데이터 클래스 |
| `@abc.abstractmethod` | 추상 메서드 |

## 11. singledispatch 데코레이터

타입에 따라 다른 구현을 호출.

```python
from functools import singledispatch

@singledispatch
def describe(obj):
    print(f"객체: {obj}")

@describe.register
def _(obj: int):
    print(f"정수: {obj}")

@describe.register
def _(obj: str):
    print(f"문자열: '{obj}'")

@describe.register
def _(obj: list):
    print(f"리스트 (길이 {len(obj)})")

describe(42)         # 정수: 42
describe("hello")    # 문자열: 'hello'
describe([1, 2, 3])  # 리스트 (길이 3)
describe(3.14)       # 객체: 3.14
```

## 12. 실전 예제

### 예제 1: Flask 스타일 라우팅
```python
class App:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def handle(self, path):
        if path in self.routes:
            return self.routes[path]()
        return "404 Not Found"

app = App()

@app.route("/")
def home():
    return "Welcome!"

@app.route("/about")
def about():
    return "About page"

print(app.handle("/"))       # Welcome!
print(app.handle("/about"))  # About page
print(app.handle("/xxx"))    # 404 Not Found
```

### 예제 2: 트랜잭션 관리
```python
def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("트랜잭션 시작")
        try:
            result = func(*args, **kwargs)
            print("커밋")
            return result
        except Exception:
            print("롤백")
            raise
    return wrapper

@transactional
def transfer(from_id, to_id, amount):
    # DB 작업...
    print(f"{from_id} → {to_id}: {amount}")

transfer(1, 2, 100)
```

### 예제 3: 자동 등록
```python
HANDLERS = {}

def register(event_type):
    def decorator(func):
        HANDLERS[event_type] = func
        return func
    return decorator

@register("user_created")
def handle_user_created(user):
    print(f"새 사용자: {user}")

@register("user_deleted")
def handle_user_deleted(user_id):
    print(f"삭제: {user_id}")

# 이벤트 디스패치
def emit(event_type, data):
    if event_type in HANDLERS:
        HANDLERS[event_type](data)

emit("user_created", {"name": "Alice"})
emit("user_deleted", 42)
```

## 📝 연습 문제

### 문제 1: @timer
함수의 실행 시간을 측정해 출력하는 데코레이터를 만드세요.

### 문제 2: @log
함수 호출 시 인자와 반환값을 로깅하는 데코레이터를 만드세요.

### 문제 3: @cache
인자와 결과를 캐시하는 데코레이터를 lru_cache 없이 구현하세요.

### 문제 4: @validate
함수 인자가 모두 정수인지 검증하는 데코레이터를 만드세요.

### 문제 5: @retry
함수가 예외를 던지면 최대 N번까지 재시도하는 데코레이터를 만드세요.

### 문제 6: 다중 데코레이터
@timer 와 @cache 를 함께 적용해 fibonacci 함수를 최적화하세요.

## ✅ 체크리스트
- [ ] 기본 데코레이터를 작성한다
- [ ] @wraps 의 중요성을 안다
- [ ] 인자 있는 데코레이터를 만든다
- [ ] 클래스 기반 데코레이터를 안다
- [ ] 여러 데코레이터를 함께 사용한다
- [ ] 자주 쓰는 패턴을 응용한다

## 🔗 다음 챕터
👉 [02. 메타클래스와 디스크립터](./02-metaclasses.md)
