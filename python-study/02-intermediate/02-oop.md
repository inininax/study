# 02. 객체지향 프로그래밍 (OOP)

## 🎯 학습 목표
- 클래스와 객체의 개념을 이해한다
- 상속, 다형성, 캡슐화를 활용한다
- 매직 메서드(던더 메서드)를 활용한다
- 추상 클래스와 인터페이스를 이해한다

## 1. 클래스의 기초

### 1.1 클래스와 객체
- **클래스(Class)**: 객체의 설계도 (틀)
- **객체(Object) / 인스턴스(Instance)**: 클래스로 만든 실체

```python
class Dog:
    """강아지 클래스"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name}: 멍멍!")

# 객체 생성
dog1 = Dog("Buddy", 3)
dog2 = Dog("Max", 5)

dog1.bark()  # Buddy: 멍멍!
dog2.bark()  # Max: 멍멍!

print(dog1.name)  # Buddy
print(dog2.age)   # 5
```

### 1.2 `__init__` 생성자
객체가 생성될 때 자동으로 호출됩니다.

```python
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

p1 = Point()         # x=0, y=0
p2 = Point(3, 4)     # x=3, y=4
p3 = Point(x=5, y=6) # 키워드 인자
```

### 1.3 `self` 키워드
- 인스턴스 자신을 가리킴
- 메서드의 첫 인자 (자동으로 전달됨)
- 다른 언어의 `this` 와 같음

## 2. 속성과 메서드

### 2.1 인스턴스 속성 (Instance Attribute)
각 객체마다 독립된 값을 가집니다.

```python
class Car:
    def __init__(self, brand, color):
        self.brand = brand    # 인스턴스 속성
        self.color = color
        self.speed = 0

car1 = Car("BMW", "Black")
car2 = Car("Audi", "White")
car1.speed = 60       # car2.speed 는 영향 없음
print(car2.speed)     # 0
```

### 2.2 클래스 속성 (Class Attribute)
모든 객체가 공유하는 값입니다.

```python
class Dog:
    species = "Canis familiaris"  # 클래스 속성

    def __init__(self, name):
        self.name = name           # 인스턴스 속성

d1 = Dog("Buddy")
d2 = Dog("Max")
print(d1.species)  # Canis familiaris
print(d2.species)  # Canis familiaris

# 클래스 속성 변경 (모두 영향)
Dog.species = "Canis lupus"
print(d1.species)  # Canis lupus
```

> ⚠️ **주의**: 가변 객체를 클래스 속성으로 두면 공유됨!
```python
# ❌ 위험한 패턴
class Student:
    grades = []  # 모든 학생이 공유!

    def add_grade(self, grade):
        self.grades.append(grade)

s1 = Student()
s2 = Student()
s1.add_grade(90)
print(s2.grades)  # [90] ← 다른 학생도 영향!

# ✅ 올바른 패턴
class Student:
    def __init__(self):
        self.grades = []  # 각자 가짐
```

### 2.3 메서드의 종류
```python
class MyClass:
    class_attr = "Hello"

    # 1. 인스턴스 메서드 (self)
    def instance_method(self):
        return f"인스턴스: {self}"

    # 2. 클래스 메서드 (cls)
    @classmethod
    def class_method(cls):
        return f"클래스: {cls}, {cls.class_attr}"

    # 3. 스태틱 메서드
    @staticmethod
    def static_method(x, y):
        return x + y

obj = MyClass()
obj.instance_method()           # OK
MyClass.class_method()          # OK
MyClass.static_method(1, 2)     # OK
```

### 2.4 클래스 메서드의 활용
```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_str):
        """문자열로부터 객체 생성 (팩토리 메서드)"""
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)

    @classmethod
    def today(cls):
        import datetime
        d = datetime.date.today()
        return cls(d.year, d.month, d.day)

d1 = Date(2026, 5, 12)
d2 = Date.from_string("2026-05-12")
d3 = Date.today()
```

## 3. 캡슐화 (Encapsulation)

### 3.1 접근 제어 (관례)
Python은 진정한 private이 없지만, 관례로 표현합니다.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner          # public
        self._balance = balance     # protected (관례)
        self.__pin = "1234"         # private (네임 맹글링)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def get_balance(self):
        return self._balance

acc = BankAccount("Alice", 1000)
print(acc.owner)        # OK
print(acc._balance)     # 접근은 가능 but 비권장
# print(acc.__pin)      # AttributeError
print(acc._BankAccount__pin)  # 우회 접근 (가능하지만 하지 말것)
```

### 3.2 property — Getter/Setter
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """getter"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """setter"""
        if value < 0:
            raise ValueError("반지름은 음수일 수 없습니다")
        self._radius = value

    @property
    def area(self):
        """계산된 속성"""
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.radius)   # 5 (메서드 호출 X, 속성처럼 접근)
print(c.area)     # 78.53975

c.radius = 10     # setter 호출
# c.radius = -1   # ValueError
```

## 4. 상속 (Inheritance)

### 4.1 기본 상속
```python
# 부모 클래스 (슈퍼클래스)
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name}이(가) 먹습니다")

    def sleep(self):
        print(f"{self.name}이(가) 잡니다")

# 자식 클래스 (서브클래스)
class Dog(Animal):
    def bark(self):
        print(f"{self.name}: 멍멍!")

class Cat(Animal):
    def meow(self):
        print(f"{self.name}: 야옹~")

d = Dog("Buddy")
d.eat()    # 상속받음
d.sleep()  # 상속받음
d.bark()   # Dog 고유 메서드
```

### 4.2 super() — 부모 호출
```python
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # 부모 __init__ 호출
        self.breed = breed

    def describe(self):
        return f"{self.name}, {self.age}살, {self.breed}"

d = Dog("Buddy", 3, "Bulldog")
print(d.describe())
```

### 4.3 메서드 오버라이딩
```python
class Animal:
    def speak(self):
        print("동물 소리")

class Dog(Animal):
    def speak(self):  # 오버라이딩
        print("멍멍!")

class Cat(Animal):
    def speak(self):
        print("야옹~")

for animal in [Dog(), Cat(), Animal()]:
    animal.speak()
# 멍멍!
# 야옹~
# 동물 소리
```

### 4.4 다중 상속
```python
class Swimmer:
    def swim(self):
        print("수영합니다")

class Flyer:
    def fly(self):
        print("날아갑니다")

class Duck(Swimmer, Flyer):  # 둘 다 상속
    def quack(self):
        print("꽥꽥!")

d = Duck()
d.swim()
d.fly()
d.quack()
```

### 4.5 MRO (Method Resolution Order)
```python
class A:
    def hello(self): print("A")

class B(A):
    def hello(self): print("B")

class C(A):
    def hello(self): print("C")

class D(B, C):
    pass

d = D()
d.hello()              # B
print(D.__mro__)       # D -> B -> C -> A -> object
```

## 5. 다형성 (Polymorphism)

### 5.1 덕 타이핑 (Duck Typing)
"오리처럼 걷고 오리처럼 운다면 그것은 오리다"

```python
class Dog:
    def speak(self):
        return "멍멍"

class Cat:
    def speak(self):
        return "야옹"

class Duck:
    def speak(self):
        return "꽥꽥"

def make_sound(animal):
    print(animal.speak())  # 어떤 클래스든 speak() 만 있으면 OK

make_sound(Dog())   # 멍멍
make_sound(Cat())   # 야옹
make_sound(Duck())  # 꽥꽥
```

### 5.2 isinstance() vs type()
```python
class Animal: pass
class Dog(Animal): pass

d = Dog()
print(type(d) == Dog)        # True
print(type(d) == Animal)     # False (정확히 같은 타입만)
print(isinstance(d, Dog))    # True
print(isinstance(d, Animal)) # True (부모도 인정)

# 권장: isinstance() 사용
```

## 6. 매직 메서드 (Dunder Methods)

`__이름__` 형태의 특수 메서드들. 연산자/내장 함수의 동작을 정의합니다.

### 6.1 객체 표현
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """str(obj), print(obj) 에서 호출"""
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        """repr(obj), 디버깅 시 호출"""
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(p)         # Point(3, 4)
print(repr(p))   # Point(x=3, y=4)
```

> 💡 `__str__` 는 사용자용, `__repr__` 는 개발자용

### 6.2 비교 연산자
```python
class Person:
    def __init__(self, age):
        self.age = age

    def __eq__(self, other):
        return self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

    def __le__(self, other):
        return self.age <= other.age

    # __gt__, __ge__, __ne__ 도 가능

a = Person(20)
b = Person(25)
print(a == b)    # False
print(a < b)     # True
print(sorted([b, a]))  # [a, b]
```

> 💡 `@functools.total_ordering` 데코레이터 사용 시 `__eq__`, `__lt__` 만 정의해도 모든 비교 동작!

### 6.3 산술 연산자
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)   # Vector(4, 6)
print(v2 - v1)   # Vector(2, 2)
print(v1 * 3)    # Vector(3, 6)
```

### 6.4 컨테이너 메서드
```python
class MyList:
    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def __contains__(self, item):
        return item in self._items

    def __iter__(self):
        return iter(self._items)

    def add(self, item):
        self._items.append(item)

ml = MyList()
ml.add(1); ml.add(2); ml.add(3)
print(len(ml))      # 3
print(ml[0])        # 1
print(2 in ml)      # True
for item in ml: print(item)
```

### 6.5 콜러블
```python
class Multiplier:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        """객체를 함수처럼 호출"""
        return x * self.n

times3 = Multiplier(3)
print(times3(10))   # 30
print(times3(5))    # 15
```

### 6.6 컨텍스트 매니저
```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.time() - self.start
        print(f"실행 시간: {self.elapsed:.4f}초")
        return False  # 예외를 다시 발생시킴

with Timer() as t:
    sum(range(1000000))
# 실행 시간: 0.0234초
```

## 7. 추상 클래스 (Abstract Class)

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        """반드시 자식이 구현해야 함"""
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def describe(self):
        return f"넓이: {self.area()}, 둘레: {self.perimeter()}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# s = Shape()           # TypeError: 추상 클래스
r = Rectangle(3, 4)
print(r.describe())     # 넓이: 12, 둘레: 14
```

## 8. dataclass (Python 3.7+)

데이터 클래스를 간단히 만드는 방법.

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Person:
    name: str
    age: int
    email: str = ""
    hobbies: List[str] = field(default_factory=list)

p = Person("Alice", 25, "a@example.com", ["reading"])
print(p)         # Person(name='Alice', age=25, email='a@example.com', hobbies=['reading'])
print(p.name)    # Alice

# 자동 생성되는 메서드:
# __init__, __repr__, __eq__
```

### dataclass 옵션
```python
@dataclass(frozen=True)   # 불변 객체
class Point:
    x: int
    y: int

p = Point(1, 2)
# p.x = 10   # FrozenInstanceError
```

## 9. 실전 예제

### 예제 1: 학생 관리 시스템
```python
class Student:
    school = "Python High School"  # 클래스 속성

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
        self._scores = {}

    def add_score(self, subject, score):
        if not 0 <= score <= 100:
            raise ValueError("점수는 0-100 사이여야 합니다")
        self._scores[subject] = score

    @property
    def average(self):
        if not self._scores:
            return 0
        return sum(self._scores.values()) / len(self._scores)

    def __str__(self):
        return f"{self.name}({self.grade}학년) - 평균: {self.average:.2f}"

    def __lt__(self, other):
        return self.average < other.average

students = [
    Student("Alice", 1),
    Student("Bob", 1),
    Student("Charlie", 1),
]

for s, scores in zip(students, [[85, 90, 78], [72, 80, 88], [95, 92, 89]]):
    for subject, score in zip(["수학", "영어", "과학"], scores):
        s.add_score(subject, score)

# 평균 점수 순으로 정렬
ranked = sorted(students, reverse=True)
for rank, student in enumerate(ranked, 1):
    print(f"{rank}등: {student}")
```

### 예제 2: 도형 계산기
```python
from abc import ABC, abstractmethod
from math import pi

class Shape(ABC):
    @abstractmethod
    def area(self): pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

shapes = [Circle(5), Square(4), Triangle(3, 6)]
total = sum(s.area() for s in shapes)
print(f"총 넓이: {total:.2f}")
```

## 📝 연습 문제

### 문제 1: BankAccount
입금, 출금, 잔액 확인이 가능한 BankAccount 클래스를 만드세요. 잔액보다 많이 출금하려 하면 예외를 발생시키세요.

### 문제 2: 사각형/원 다형성
Shape 부모 클래스를 만들고 Rectangle, Circle 자식을 만들어 면적/둘레를 계산하세요.

### 문제 3: Vector 클래스
2D 벡터 클래스를 만들어 덧셈, 뺄셈, 스칼라 곱, 내적, 크기 계산을 구현하세요.

### 문제 4: 도서관 시스템
Book, Library 클래스를 만들어 책 추가, 대출, 반납 기능을 구현하세요.

### 문제 5: dataclass 활용
@dataclass 를 사용해 Product 클래스를 만들고, 가격 순 정렬을 구현하세요.

## ✅ 체크리스트
- [ ] 클래스를 정의하고 객체를 생성할 수 있다
- [ ] `__init__` 으로 초기화한다
- [ ] 상속을 활용할 수 있다
- [ ] super() 로 부모 메서드를 호출한다
- [ ] property 로 getter/setter 를 만든다
- [ ] 매직 메서드를 활용한다
- [ ] 추상 클래스와 dataclass 를 안다

## 🔗 다음 챕터
👉 [03. 모듈과 패키지](./03-modules-packages.md)
