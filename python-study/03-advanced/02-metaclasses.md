# 02. 메타클래스와 디스크립터

## 🎯 학습 목표
- 메타클래스의 개념과 동작을 이해한다
- 디스크립터 프로토콜을 안다
- `__slots__` 의 용도를 안다
- 동적 클래스 생성을 활용한다

## 1. 메타클래스 소개

> "메타클래스는 99%의 사용자가 신경 쓸 필요가 없습니다. 필요한지 의문이 든다면 필요하지 않습니다." — Tim Peters

하지만 라이브러리 개발자나 프레임워크 사용자는 알아두면 좋습니다.

### 1.1 모든 것은 객체
```python
x = 42
print(type(x))           # <class 'int'>
print(type(int))         # <class 'type'>
print(type(type))        # <class 'type'>

class MyClass:
    pass

obj = MyClass()
print(type(obj))         # <class 'MyClass'>
print(type(MyClass))     # <class 'type'>  ← 클래스는 type의 인스턴스!
```

### 1.2 type — 메타클래스의 시작
`type` 은 **메타클래스**입니다. 클래스를 만드는 클래스.

```python
# class 문법
class MyClass:
    x = 10
    def greet(self):
        return "hi"

# type 으로 동적 생성 (동등)
MyClass = type(
    "MyClass",                          # 클래스 이름
    (),                                 # 부모 클래스 튜플
    {                                   # 속성 딕셔너리
        "x": 10,
        "greet": lambda self: "hi",
    }
)
```

## 2. 메타클래스 만들기

### 2.1 type 상속
```python
class UppercaseMeta(type):
    def __new__(mcs, name, bases, namespace):
        # 모든 메서드 이름을 대문자로
        new_namespace = {}
        for key, value in namespace.items():
            if not key.startswith("_") and callable(value):
                new_namespace[key.upper()] = value
            else:
                new_namespace[key] = value

        return super().__new__(mcs, name, bases, new_namespace)

class MyClass(metaclass=UppercaseMeta):
    def hello(self):
        return "Hello!"

obj = MyClass()
print(obj.HELLO())     # Hello! (이름이 대문자로 바뀜)
# obj.hello()          # AttributeError
```

### 2.2 자동 등록
```python
PLUGINS = {}

class PluginMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if name != "Plugin":  # 기본 클래스는 제외
            PLUGINS[name] = cls

class Plugin(metaclass=PluginMeta):
    pass

class EmailPlugin(Plugin):
    def send(self, msg):
        print(f"이메일: {msg}")

class SMSPlugin(Plugin):
    def send(self, msg):
        print(f"SMS: {msg}")

print(PLUGINS)
# {'EmailPlugin': <class 'EmailPlugin'>, 'SMSPlugin': <class 'SMSPlugin'>}
```

### 2.3 ABC (Abstract Base Class) 메타클래스
```python
from abc import ABCMeta, abstractmethod

class Shape(metaclass=ABCMeta):
    @abstractmethod
    def area(self):
        pass

# 또는 (더 간단)
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
```

## 3. `__init_subclass__` — 메타클래스의 대안

Python 3.6+ 에서 추가된 더 간단한 방법.

```python
class Plugin:
    plugins = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.plugins[cls.__name__] = cls

class EmailPlugin(Plugin):
    pass

class SMSPlugin(Plugin):
    pass

print(Plugin.plugins)
# {'EmailPlugin': ..., 'SMSPlugin': ...}
```

> 💡 메타클래스를 만들기 전에 `__init_subclass__` 로 충분한지 검토하세요.

## 4. 디스크립터 (Descriptor)

속성 접근을 가로채는 객체.

### 4.1 디스크립터 프로토콜
- `__get__(self, obj, owner)`
- `__set__(self, obj, value)`
- `__delete__(self, obj)`

```python
class Validated:
    def __init__(self, name=None, validator=None):
        self.name = name
        self.validator = validator

    def __set_name__(self, owner, name):
        # Python 3.6+ : 클래스에 할당될 때 호출
        self.name = name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if self.validator:
            self.validator(value)
        obj.__dict__[self.name] = value

def positive(value):
    if value < 0:
        raise ValueError("음수 불가")

def non_empty(value):
    if not value:
        raise ValueError("비어 있음")

class Person:
    name = Validated(validator=non_empty)
    age = Validated(validator=positive)

p = Person()
p.name = "Alice"
p.age = 25
# p.age = -5   # ValueError
print(p.name)  # Alice
```

### 4.2 property는 디스크립터의 일종
```python
# 이렇게 쓰지만:
class Foo:
    @property
    def x(self):
        return self._x

# 내부적으로 디스크립터 클래스로 구현됨
```

### 4.3 타입 검증 디스크립터
```python
class Typed:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name}은(는) {self.expected_type.__name__}여야 합니다"
            )
        obj.__dict__[self.name] = value

class User:
    name = Typed(str)
    age = Typed(int)
    salary = Typed(float)

u = User()
u.name = "Alice"
u.age = 25
u.salary = 50000.0
# u.age = "twenty"  # TypeError
```

## 5. `__slots__` — 메모리 최적화

`__dict__` 대신 고정된 속성만 허용.

```python
class Point:
    __slots__ = ["x", "y"]

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p.x, p.y)

# p.z = 10  # AttributeError: 'Point' object has no attribute 'z'

# __dict__ 가 없음
# print(p.__dict__)  # AttributeError
```

### 장점
- 메모리 사용량 감소 (수천~수만 객체 생성 시 큰 차이)
- 속성 접근 약간 빠름
- 오타 방지

### 단점
- 동적 속성 추가 불가
- 다중 상속 시 복잡
- weakref, pickle 등 일부 기능 제한

### 측정
```python
import sys

class Regular:
    def __init__(self):
        self.x = 1
        self.y = 2

class Slotted:
    __slots__ = ["x", "y"]
    def __init__(self):
        self.x = 1
        self.y = 2

r = Regular()
s = Slotted()
print(sys.getsizeof(r) + sys.getsizeof(r.__dict__))  # 약 360 bytes
print(sys.getsizeof(s))                              # 약 48 bytes
```

## 6. 동적 속성 (`__getattr__`, `__setattr__`)

### 6.1 `__getattr__` — 없는 속성 접근 시
```python
class Config:
    def __init__(self, **kwargs):
        self._data = kwargs

    def __getattr__(self, name):
        # 일반 속성 검색 실패 시에만 호출
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{name}' 없음")

c = Config(host="localhost", port=8080)
print(c.host)    # localhost
print(c.port)    # 8080
# print(c.user)  # AttributeError
```

### 6.2 `__getattribute__` — 모든 속성 접근
```python
class Tracker:
    def __getattribute__(self, name):
        # 무한 재귀 주의! object 의 메서드 사용
        print(f"접근: {name}")
        return object.__getattribute__(self, name)

class MyClass(Tracker):
    def __init__(self):
        self.x = 10

obj = MyClass()
obj.x        # "접근: x" 출력
```

### 6.3 `__setattr__` / `__delattr__`
```python
class ImmutableAfterInit:
    def __init__(self, value):
        self._initialized = False
        self.value = value
        self._initialized = True

    def __setattr__(self, name, value):
        if getattr(self, "_initialized", False):
            raise AttributeError("초기화 후에는 변경 불가")
        super().__setattr__(name, value)

obj = ImmutableAfterInit(42)
# obj.value = 100  # AttributeError
```

## 7. 동적 클래스 생성

### 7.1 type() 으로 생성
```python
def make_class(name, fields):
    def __init__(self, **kwargs):
        for k in fields:
            setattr(self, k, kwargs.get(k))

    def __repr__(self):
        attrs = ", ".join(f"{k}={getattr(self, k)!r}" for k in fields)
        return f"{name}({attrs})"

    return type(name, (), {
        "__init__": __init__,
        "__repr__": __repr__,
        "fields": fields,
    })

Point = make_class("Point", ["x", "y"])
p = Point(x=3, y=4)
print(p)    # Point(x=3, y=4)
```

### 7.2 ORM 스타일 예시
```python
class Field:
    def __init__(self, field_type):
        self.field_type = field_type

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.field_type):
            raise TypeError(f"{self.name}은(는) {self.field_type.__name__}여야 함")
        obj.__dict__[self.name] = value

class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        # 모든 Field 수집
        fields = {k: v for k, v in namespace.items() if isinstance(v, Field)}
        cls = super().__new__(mcs, name, bases, namespace)
        cls._fields = fields
        return cls

class Model(metaclass=ModelMeta):
    def __repr__(self):
        attrs = ", ".join(f"{k}={getattr(self, k)!r}" for k in self._fields)
        return f"{self.__class__.__name__}({attrs})"

class User(Model):
    name = Field(str)
    age = Field(int)

u = User()
u.name = "Alice"
u.age = 25
print(u)            # User(name='Alice', age=25)
# u.age = "abc"     # TypeError
```

## 8. 매직 메서드 종합

### 자주 쓰는 매직 메서드
```python
class MyClass:
    # 생성/소멸
    def __init__(self, *args): ...
    def __new__(cls, *args): ...
    def __del__(self): ...

    # 문자열
    def __str__(self): ...
    def __repr__(self): ...
    def __format__(self, spec): ...
    def __bytes__(self): ...

    # 비교
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __hash__(self): ...

    # 산술
    def __add__(self, other): ...
    def __sub__(self, other): ...
    def __mul__(self, other): ...
    def __truediv__(self, other): ...
    def __floordiv__(self, other): ...
    def __mod__(self, other): ...
    def __pow__(self, other): ...
    # __radd__, __iadd__ 등도 있음

    # 컨테이너
    def __len__(self): ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, value): ...
    def __delitem__(self, key): ...
    def __contains__(self, item): ...
    def __iter__(self): ...

    # 호출
    def __call__(self, *args, **kwargs): ...

    # 컨텍스트 매니저
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...

    # 속성
    def __getattr__(self, name): ...
    def __setattr__(self, name, value): ...
    def __delattr__(self, name): ...
    def __dir__(self): ...
```

## 9. `__new__` vs `__init__`

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        print("__new__: 인스턴스 생성 직전")
        instance = super().__new__(cls)
        return instance

    def __init__(self, value):
        print("__init__: 인스턴스 초기화")
        self.value = value

obj = MyClass(42)
# __new__: 인스턴스 생성 직전
# __init__: 인스턴스 초기화
```

### 활용: 싱글톤
```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)  # True
```

### 활용: 불변 객체
```python
class ImmutablePoint:
    def __new__(cls, x, y):
        obj = super().__new__(cls)
        obj.__dict__["x"] = x
        obj.__dict__["y"] = y
        return obj

    def __setattr__(self, name, value):
        raise AttributeError("변경 불가")
```

## 10. 실전 예제

### 예제 1: Field validator (dataclass 대안)
```python
class Field:
    def __init__(self, default=None, validators=None):
        self.default = default
        self.validators = validators or []

    def __set_name__(self, owner, name):
        self.name = f"_{name}"
        self.public_name = name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return getattr(obj, self.name, self.default)

    def __set__(self, obj, value):
        for validator in self.validators:
            validator(self.public_name, value)
        setattr(obj, self.name, value)

def min_length(n):
    def validate(name, value):
        if len(value) < n:
            raise ValueError(f"{name}: {n}자 이상")
    return validate

def positive(name, value):
    if value < 0:
        raise ValueError(f"{name}: 음수 불가")

class User:
    username = Field(validators=[min_length(3)])
    age = Field(default=0, validators=[positive])

u = User()
u.username = "Alice"
u.age = 25
# u.username = "ab"  # ValueError
# u.age = -1         # ValueError
```

## 📝 연습 문제

### 문제 1: 자동 등록
하위 클래스를 자동으로 dict 에 등록하는 메타클래스 (또는 `__init_subclass__`) 를 작성하세요.

### 문제 2: 디스크립터
양수만 허용하는 디스크립터 `PositiveNumber` 를 만들어 사용하세요.

### 문제 3: 읽기 전용
값을 한 번만 설정할 수 있는 디스크립터 `WriteOnce` 를 만드세요.

### 문제 4: __slots__
일반 클래스와 __slots__ 사용 클래스의 메모리 사용량을 비교하세요.

### 문제 5: 싱글톤
메타클래스를 사용한 싱글톤 패턴을 구현하세요.

## ✅ 체크리스트
- [ ] 메타클래스의 개념을 이해한다
- [ ] `__init_subclass__` 의 용도를 안다
- [ ] 디스크립터 프로토콜을 활용한다
- [ ] `__slots__` 의 효과를 안다
- [ ] `__new__` 와 `__init__` 의 차이를 안다

## 🔗 다음 챕터
👉 [03. 동시성 (threading/multiprocessing)](./03-concurrency.md)
