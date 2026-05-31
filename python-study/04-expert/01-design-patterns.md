# 01. 디자인 패턴

## 🎯 학습 목표
- 자주 쓰이는 디자인 패턴을 Python 답게 구현한다
- 패턴이 해결하는 문제를 이해한다
- 언제 패턴을 적용하고 언제 피할지 안다

> 💡 Python 의 동적 특성 덕분에 일부 GoF 패턴은 더 간단합니다.

## 1. 생성 패턴 (Creational)

### 1.1 Singleton — 인스턴스 하나만
```python
# 방법 1: 모듈 (가장 Pythonic) ✅
# config.py
_settings = {"debug": False}

def get_setting(key):
    return _settings.get(key)

def set_setting(key, value):
    _settings[key] = value

# 모든 모듈에서 import 해도 같은 객체

# 방법 2: __new__
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 방법 3: 메타클래스
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    pass

db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

### 1.2 Factory — 객체 생성 추상화
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self): pass

class Dog(Animal):
    def speak(self): return "Woof!"

class Cat(Animal):
    def speak(self): return "Meow!"

# Simple Factory
class AnimalFactory:
    @staticmethod
    def create(kind):
        if kind == "dog":
            return Dog()
        if kind == "cat":
            return Cat()
        raise ValueError(f"Unknown: {kind}")

animal = AnimalFactory.create("dog")

# Python 답게: dict + 함수
ANIMALS = {"dog": Dog, "cat": Cat}

def create_animal(kind):
    cls = ANIMALS.get(kind)
    if not cls:
        raise ValueError(f"Unknown: {kind}")
    return cls()
```

### 1.3 Builder — 복잡한 객체 단계별 생성
```python
class Pizza:
    def __init__(self):
        self.size = None
        self.toppings = []
        self.crust = "regular"

    def __str__(self):
        return f"Pizza({self.size}, {self.crust}, {self.toppings})"

class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def size(self, s):
        self.pizza.size = s
        return self    # 체이닝!

    def topping(self, t):
        self.pizza.toppings.append(t)
        return self

    def crust(self, c):
        self.pizza.crust = c
        return self

    def build(self):
        return self.pizza

pizza = (
    PizzaBuilder()
    .size("large")
    .crust("thin")
    .topping("cheese")
    .topping("pepperoni")
    .build()
)
print(pizza)
```

> 💡 dataclass 또는 키워드 인자가 더 Python 다울 수 있습니다.
```python
from dataclasses import dataclass, field

@dataclass
class Pizza:
    size: str
    crust: str = "regular"
    toppings: list = field(default_factory=list)

pizza = Pizza("large", "thin", ["cheese", "pepperoni"])
```

### 1.4 Prototype — 복제로 생성
```python
import copy

class Document:
    def __init__(self, content, style):
        self.content = content
        self.style = style

original = Document("Hello", {"font": "Arial", "size": 12})

# 얕은 복사
shallow = copy.copy(original)

# 깊은 복사 (중첩 객체까지)
deep = copy.deepcopy(original)
deep.style["size"] = 16  # original 영향 없음
```

## 2. 구조 패턴 (Structural)

### 2.1 Adapter — 인터페이스 변환
```python
# 기존 시스템
class OldPrinter:
    def print_message(self, msg):
        print(f"[OLD] {msg}")

# 새 시스템 인터페이스
class NewPrinter:
    def output(self, text):
        raise NotImplementedError

# 어댑터
class PrinterAdapter(NewPrinter):
    def __init__(self, old_printer):
        self.old_printer = old_printer

    def output(self, text):
        self.old_printer.print_message(text)

# 사용
adapter = PrinterAdapter(OldPrinter())
adapter.output("Hello")  # [OLD] Hello
```

### 2.2 Decorator — 기능 동적 추가
```python
# Python 데코레이터로 자연스럽게
def log(func):
    def wrapper(*args, **kwargs):
        print(f"호출: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def greet(name):
    print(f"Hi, {name}")
```

### 2.3 Facade — 복잡한 시스템의 단순 인터페이스
```python
class CPU:
    def freeze(self): print("CPU freeze")
    def jump(self, pos): print(f"CPU jump to {pos}")
    def execute(self): print("CPU execute")

class Memory:
    def load(self, pos, data): print(f"Memory load {data} to {pos}")

class HardDrive:
    def read(self, pos): return "boot_data"

# Facade
class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = HardDrive()

    def start(self):
        self.cpu.freeze()
        self.memory.load(0, self.disk.read(100))
        self.cpu.jump(0)
        self.cpu.execute()

computer = ComputerFacade()
computer.start()  # 복잡한 절차를 한 줄로!
```

### 2.4 Proxy — 대리 객체
```python
class HeavyResource:
    def __init__(self):
        print("로딩 중...")
        self.data = "큰 데이터"

    def get(self):
        return self.data

# Lazy 프록시
class LazyProxy:
    def __init__(self):
        self._resource = None

    def get(self):
        if self._resource is None:
            self._resource = HeavyResource()
        return self._resource.get()

proxy = LazyProxy()
# HeavyResource 는 첫 .get() 호출 전까지 생성 안 됨
```

## 3. 행위 패턴 (Behavioral)

### 3.1 Strategy — 알고리즘 교체
```python
# 함수로 (Pythonic) ✅
def bubble_sort(data):
    return sorted(data)  # 실제로는 다른 구현

def quick_sort(data):
    return sorted(data)

class Sorter:
    def __init__(self, strategy):
        self.strategy = strategy

    def sort(self, data):
        return self.strategy(data)

sorter = Sorter(quick_sort)
sorter.sort([3, 1, 2])

# 또는 sorted 의 key 처럼
sorted_items = sorted(items, key=lambda x: x.priority)
```

### 3.2 Observer — 이벤트 구독
```python
class EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def publish(self, event, data):
        for callback in self._listeners.get(event, []):
            callback(data)

bus = EventBus()

bus.subscribe("user_created", lambda u: print(f"환영합니다, {u}!"))
bus.subscribe("user_created", lambda u: print(f"DB 저장: {u}"))

bus.publish("user_created", "Alice")
# 환영합니다, Alice!
# DB 저장: Alice
```

### 3.3 Command — 작업을 객체로
```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self): pass

    @abstractmethod
    def undo(self): pass

class WriteCommand(Command):
    def __init__(self, doc, text):
        self.doc = doc
        self.text = text

    def execute(self):
        self.doc.content += self.text

    def undo(self):
        self.doc.content = self.doc.content[:-len(self.text)]

class Document:
    def __init__(self):
        self.content = ""
        self.history = []

    def execute(self, cmd):
        cmd.execute()
        self.history.append(cmd)

    def undo(self):
        if self.history:
            self.history.pop().undo()

doc = Document()
doc.execute(WriteCommand(doc, "Hello "))
doc.execute(WriteCommand(doc, "World"))
print(doc.content)  # Hello World
doc.undo()
print(doc.content)  # Hello
```

### 3.4 Template Method — 알고리즘 골격
```python
from abc import ABC, abstractmethod

class DataPipeline(ABC):
    def run(self):
        """템플릿 메서드"""
        data = self.extract()
        transformed = self.transform(data)
        self.load(transformed)

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def transform(self, data): pass

    @abstractmethod
    def load(self, data): pass

class CSVPipeline(DataPipeline):
    def extract(self):
        return [1, 2, 3]

    def transform(self, data):
        return [x * 2 for x in data]

    def load(self, data):
        print(f"저장: {data}")

CSVPipeline().run()
```

### 3.5 Chain of Responsibility — 핸들러 체인
```python
class Handler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, request):
        if self.successor:
            return self.successor.handle(request)
        return None

class AuthHandler(Handler):
    def handle(self, request):
        if not request.get("user"):
            return "401 Unauthorized"
        return super().handle(request)

class ValidationHandler(Handler):
    def handle(self, request):
        if not request.get("data"):
            return "400 Bad Request"
        return super().handle(request)

class ProcessHandler(Handler):
    def handle(self, request):
        return f"Processed: {request['data']}"

chain = AuthHandler(ValidationHandler(ProcessHandler()))

print(chain.handle({}))                              # 401
print(chain.handle({"user": "Alice"}))               # 400
print(chain.handle({"user": "Alice", "data": "x"}))  # Processed: x
```

### 3.6 State — 상태에 따른 동작 변경
```python
class State:
    def handle(self, context):
        raise NotImplementedError

class IdleState(State):
    def handle(self, context):
        print("시작!")
        context.state = RunningState()

class RunningState(State):
    def handle(self, context):
        print("정지!")
        context.state = IdleState()

class Machine:
    def __init__(self):
        self.state = IdleState()

    def press_button(self):
        self.state.handle(self)

m = Machine()
m.press_button()  # 시작!
m.press_button()  # 정지!
m.press_button()  # 시작!
```

### 3.7 Iterator — Python에 내장
```python
# 클래스로 이터레이터 만들기
class CountDown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        result = self.start
        self.start -= 1
        return result

# 또는 제너레이터로 (간단)
def countdown(start):
    while start > 0:
        yield start
        start -= 1
```

## 4. Python 특유의 패턴

### 4.1 Context Manager (RAII 패턴)
```python
from contextlib import contextmanager

@contextmanager
def transaction(db):
    db.begin()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise

with transaction(db) as t:
    t.execute("INSERT ...")
```

### 4.2 Mixin — 다중 상속으로 기능 조합
```python
class JSONMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class LogMixin:
    def log(self, msg):
        print(f"[{self.__class__.__name__}] {msg}")

class User(JSONMixin, LogMixin):
    def __init__(self, name):
        self.name = name

u = User("Alice")
print(u.to_json())  # {"name": "Alice"}
u.log("Created")    # [User] Created
```

### 4.3 Registry — 객체 등록
```python
HANDLERS = {}

def register(name):
    def decorator(func):
        HANDLERS[name] = func
        return func
    return decorator

@register("greet")
def greet_handler(data):
    return f"Hello, {data['name']}"

@register("bye")
def bye_handler(data):
    return f"Bye, {data['name']}"

def dispatch(event, data):
    return HANDLERS[event](data)

print(dispatch("greet", {"name": "Alice"}))
```

### 4.4 Plugin 시스템 (`__init_subclass__`)
```python
class Plugin:
    plugins = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.plugins[cls.__name__] = cls

class EmailPlugin(Plugin):
    def send(self, msg): print(f"📧 {msg}")

class SMSPlugin(Plugin):
    def send(self, msg): print(f"📱 {msg}")

# 모든 플러그인이 자동 등록됨
for name, plugin_cls in Plugin.plugins.items():
    plugin_cls().send("Hello")
```

## 5. SOLID 원칙

### S — Single Responsibility (단일 책임)
한 클래스는 한 가지 책임만.

```python
# ❌ 여러 책임
class User:
    def save_to_db(self): ...
    def send_email(self): ...
    def validate(self): ...

# ✅ 분리
class User:
    def validate(self): ...

class UserRepository:
    def save(self, user): ...

class EmailService:
    def send(self, user): ...
```

### O — Open/Closed (개방-폐쇄)
확장에는 열려 있고 수정에는 닫혀 있어야.

```python
# ❌ 새 타입 추가 시 함수 수정
def calculate(shape, type):
    if type == "circle":
        return 3.14 * shape.r ** 2
    elif type == "square":
        return shape.side ** 2

# ✅ 새 클래스 추가만으로 확장
class Shape(ABC):
    @abstractmethod
    def area(self): pass

class Circle(Shape):
    def area(self): return 3.14 * self.r ** 2
```

### L — Liskov Substitution (리스코프 치환)
하위 타입은 상위 타입을 대체할 수 있어야.

```python
# ❌ Penguin(Bird) 가 fly() 를 깨뜨림
class Bird:
    def fly(self): ...

class Penguin(Bird):
    def fly(self):
        raise Exception("못 날아!")

# ✅ 계층 분리
class Bird: ...
class FlyingBird(Bird):
    def fly(self): ...
class Penguin(Bird): ...
```

### I — Interface Segregation (인터페이스 분리)
큰 인터페이스보다 작은 인터페이스 여러 개.

```python
# ❌ 너무 큰 인터페이스
class Worker(ABC):
    def work(self): ...
    def eat(self): ...
    def sleep(self): ...

# Robot은 eat, sleep 불필요!

# ✅ 분리
class Workable(ABC):
    def work(self): ...
class Eatable(ABC):
    def eat(self): ...

class Human(Workable, Eatable): ...
class Robot(Workable): ...
```

### D — Dependency Inversion (의존성 역전)
구체적 구현이 아닌 추상에 의존.

```python
# ❌ 구체적 구현에 의존
class Service:
    def __init__(self):
        self.db = MySQLDatabase()  # 강한 결합

# ✅ 추상에 의존 (의존성 주입)
class Database(ABC):
    @abstractmethod
    def save(self, data): ...

class Service:
    def __init__(self, db: Database):
        self.db = db  # 약한 결합
```

## 6. 안티 패턴 (피해야 할 것)

### God Object — 모든 것을 하는 클래스
```python
# ❌
class Application:
    def parse_args(self): ...
    def read_config(self): ...
    def connect_db(self): ...
    def render_ui(self): ...
    def send_email(self): ...
    # 1000줄...
```

### Magic Numbers — 의미 없는 숫자
```python
# ❌
if user.age >= 18 and user.score > 80:
    pass

# ✅
ADULT_AGE = 18
PASSING_SCORE = 80

if user.age >= ADULT_AGE and user.score > PASSING_SCORE:
    pass
```

### Premature Optimization — 성급한 최적화
```python
# ❌ 처음부터 복잡한 최적화
class CacheManager:
    """캐싱이 정말 필요한지 알기 전에..."""

# ✅ 필요할 때 도입
```

### Over-engineering — 과한 추상화
```python
# ❌ 너무 많은 계층
class AbstractFactoryFactoryBuilderManager: ...

# ✅ 단순하게
def create_user(name): return User(name)
```

## 7. 실전 예제

### 예제: 알림 시스템
```python
from abc import ABC, abstractmethod

# Strategy
class Notifier(ABC):
    @abstractmethod
    def send(self, message): pass

class EmailNotifier(Notifier):
    def send(self, message):
        print(f"📧 Email: {message}")

class SMSNotifier(Notifier):
    def send(self, message):
        print(f"📱 SMS: {message}")

class SlackNotifier(Notifier):
    def send(self, message):
        print(f"💬 Slack: {message}")

# Observer + Strategy
class NotificationCenter:
    def __init__(self):
        self.notifiers = []

    def subscribe(self, notifier: Notifier):
        self.notifiers.append(notifier)

    def notify_all(self, message):
        for n in self.notifiers:
            n.send(message)

# 사용
center = NotificationCenter()
center.subscribe(EmailNotifier())
center.subscribe(SMSNotifier())
center.subscribe(SlackNotifier())

center.notify_all("긴급: 서버 다운!")
```

## 📝 연습 문제

### 문제 1: Singleton 로거
어디서든 같은 인스턴스를 받는 Logger 클래스를 만드세요.

### 문제 2: Factory
도형 종류(circle, rectangle, triangle)를 받아 적절한 객체를 생성하는 팩토리를 만드세요.

### 문제 3: Observer
주식 가격 변동 이벤트에 여러 핸들러를 구독시키는 시스템을 만드세요.

### 문제 4: Strategy
정렬 알고리즘 3가지를 Strategy 패턴으로 구현하세요.

### 문제 5: Command + Undo
간단한 텍스트 에디터에 실행취소(undo) 기능을 Command 패턴으로 추가하세요.

## ✅ 체크리스트
- [ ] 주요 디자인 패턴을 안다
- [ ] Python 답게 패턴을 구현할 수 있다
- [ ] SOLID 원칙을 이해한다
- [ ] 안티 패턴을 알아차린다
- [ ] 언제 패턴을 적용할지 판단한다

## 🔗 다음 챕터
👉 [02. 웹 개발 (FastAPI/Flask)](./02-web-development.md)
