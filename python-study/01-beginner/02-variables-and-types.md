# 02. 변수와 데이터 타입

## 🎯 학습 목표
- 변수의 개념과 사용법을 이해한다
- Python의 기본 데이터 타입을 안다
- 타입 변환을 할 수 있다

## 1. 변수란?

**변수(variable)** 는 데이터를 저장하는 메모리 공간의 이름입니다.

```python
name = "홍길동"
age = 25
height = 175.5
is_student = True
```

### 변수 명명 규칙
✅ **가능한 이름**
```python
name = "Alice"
user_name = "Bob"        # snake_case (권장)
age2 = 30
_private = "private"
```

❌ **불가능한 이름** (다음은 모두 SyntaxError 가 발생합니다)
```python
# 2age = 30          # 숫자로 시작 불가
# user-name = "x"    # 하이픈 불가
# class = "A"        # 예약어 사용 불가
# my var = 10        # 공백 불가
```

### PEP 8 권장 명명 규칙
- 변수/함수: `snake_case`
- 상수: `UPPER_SNAKE_CASE`
- 클래스: `PascalCase`
- 비공개: `_underscore_prefix`

```python
# 좋은 예
user_name = "Alice"
MAX_RETRY_COUNT = 3
class UserAccount:
    pass
```

## 2. 기본 데이터 타입

### 2.1 숫자형 (Numeric)

#### 정수 (int)
```python
age = 25
year = 2026
negative = -10
big_number = 1_000_000  # 가독성을 위한 언더스코어
```

#### 실수 (float)
```python
pi = 3.14159
temperature = -2.5
scientific = 1.5e3  # 1500.0
```

#### 복소수 (complex)
```python
z = 3 + 4j
print(z.real)  # 3.0
print(z.imag)  # 4.0
```

### 2.2 문자열 (str)

```python
single = 'Hello'
double = "World"
triple = """여러 줄
문자열"""

# 이스케이프 문자
text = "He said \"Hello\""
path = "C:\\Users\\Alice"

# Raw 문자열
raw = r"C:\Users\Alice"  # 백슬래시 그대로

# f-string (Python 3.6+, 권장)
name = "Alice"
greeting = f"Hello, {name}!"
```

### 2.3 불리언 (bool)

```python
is_active = True
is_admin = False

# 0과 빈 값은 False
print(bool(0))      # False
print(bool(""))     # False
print(bool([]))     # False
print(bool(None))   # False

# 그 외는 True
print(bool(1))      # True
print(bool("a"))    # True
print(bool([0]))    # True
```

### 2.4 None
값이 없음을 나타내는 특별한 객체입니다.

```python
result = None
print(result)        # None
print(result is None)  # True
```

## 3. type() 함수로 타입 확인

```python
print(type(25))           # <class 'int'>
print(type(3.14))         # <class 'float'>
print(type("Hello"))      # <class 'str'>
print(type(True))         # <class 'bool'>
print(type(None))         # <class 'NoneType'>
print(type([1, 2, 3]))    # <class 'list'>
```

## 4. 타입 변환 (Type Conversion)

### 명시적 변환
```python
# 문자열 → 정수
num_str = "100"
num_int = int(num_str)
print(num_int + 1)  # 101

# 정수 → 문자열
age = 25
text = "I am " + str(age) + " years old"

# 문자열 → 실수
price = float("19.99")

# 실수 → 정수 (소수점 버림)
print(int(3.9))   # 3
print(int(-3.9))  # -3

# 다양한 타입 → 불리언
print(bool(1))     # True
print(bool(0))     # False
print(bool("a"))   # True
print(bool(""))    # False
```

### 변환 에러 처리
```python
try:
    num = int("abc")
except ValueError as e:
    print(f"변환 실패: {e}")
```

## 5. 동적 타이핑

Python은 **동적 타입(dynamically typed)** 언어입니다. 변수의 타입은 실행 중에 결정되며 변경할 수 있습니다.

```python
x = 10           # int
print(type(x))   # <class 'int'>

x = "Hello"      # str로 변경
print(type(x))   # <class 'str'>

x = [1, 2, 3]    # list로 변경
print(type(x))   # <class 'list'>
```

## 6. 변수 할당 패턴

### 다중 할당
```python
# 같은 값을 여러 변수에
x = y = z = 0

# 여러 값을 한 번에
name, age, height = "Alice", 25, 165.5

# 교환 (Swap)
a, b = 1, 2
a, b = b, a
print(a, b)  # 2 1
```

### 언패킹 (Unpacking)
```python
point = (10, 20)
x, y = point
print(x, y)  # 10 20

# 별표(*) 사용
first, *rest = [1, 2, 3, 4, 5]
print(first)  # 1
print(rest)   # [2, 3, 4, 5]
```

## 7. 상수 (관습)

Python은 진정한 상수가 없지만, **대문자**로 작성하여 상수임을 표현합니다.

```python
PI = 3.14159
MAX_USERS = 1000
DEFAULT_TIMEOUT = 30

# 변경하지 않는 것이 관습
```

## 8. 메모리와 객체

Python의 모든 값은 **객체**입니다. `id()` 로 메모리 주소를 확인할 수 있습니다.

```python
a = 100
b = 100
print(id(a) == id(b))  # True (작은 정수는 캐싱됨)

x = [1, 2, 3]
y = [1, 2, 3]
print(id(x) == id(y))  # False (서로 다른 객체)
print(x == y)          # True (값은 같음)
```

## 9. 실전 예제

### 예제 1: BMI 계산기
```python
# bmi.py
weight = float(input("체중(kg)을 입력하세요: "))
height = float(input("키(m)를 입력하세요: "))

bmi = weight / (height ** 2)
print(f"당신의 BMI는 {bmi:.2f} 입니다.")
```

### 예제 2: 온도 변환기
```python
# temperature.py
celsius = float(input("섭씨 온도: "))
fahrenheit = celsius * 9 / 5 + 32
kelvin = celsius + 273.15

print(f"섭씨 {celsius}°C")
print(f"화씨 {fahrenheit}°F")
print(f"켈빈 {kelvin}K")
```

## 📝 연습 문제

### 문제 1: 변수 타입 맞추기
다음 각 변수의 타입을 예측하고 `type()` 으로 확인하세요.
```python
a = 10
b = 10.0
c = "10"
d = True
e = None
f = 10 + 0j
```

### 문제 2: 타입 변환
사용자에게 두 개의 숫자를 입력받아 합을 출력하는 프로그램을 작성하세요. (input()은 항상 문자열을 반환합니다.)

### 문제 3: 변수 교환
세 개의 변수 `a=1, b=2, c=3` 을 `a=3, b=1, c=2` 로 교환하세요.

### 문제 4: 사각형의 넓이와 둘레
가로와 세로를 입력받아 사각형의 넓이와 둘레를 계산하는 프로그램을 작성하세요.

## ✅ 체크리스트
- [ ] 변수 명명 규칙을 안다
- [ ] int, float, str, bool 타입을 안다
- [ ] type() 으로 타입을 확인할 수 있다
- [ ] int(), str(), float() 으로 타입 변환을 할 수 있다
- [ ] f-string으로 문자열을 포맷할 수 있다

## 🔗 다음 챕터
👉 [03. 연산자](./03-operators.md)
