# 03. 연산자

## 🎯 학습 목표
- Python의 다양한 연산자를 안다
- 연산자 우선순위를 이해한다
- 연산자를 활용한 표현식을 작성할 수 있다

## 1. 산술 연산자 (Arithmetic Operators)

| 연산자 | 설명 | 예시 | 결과 |
|--------|------|------|------|
| `+` | 덧셈 | `5 + 3` | `8` |
| `-` | 뺄셈 | `5 - 3` | `2` |
| `*` | 곱셈 | `5 * 3` | `15` |
| `/` | 나눗셈 (실수) | `5 / 3` | `1.666...` |
| `//` | 몫 (정수 나눗셈) | `5 // 3` | `1` |
| `%` | 나머지 | `5 % 3` | `2` |
| `**` | 거듭제곱 | `5 ** 3` | `125` |

```python
print(10 + 3)   # 13
print(10 - 3)   # 7
print(10 * 3)   # 30
print(10 / 3)   # 3.3333333333333335
print(10 // 3)  # 3
print(10 % 3)   # 1
print(10 ** 3)  # 1000

# 음수의 나눗셈 주의
print(-7 // 2)  # -4 (수학적으로 -3.5의 내림)
print(-7 % 2)   # 1
```

### 실용 예시
```python
# 짝수/홀수 판별
num = 7
if num % 2 == 0:
    print("짝수")
else:
    print("홀수")

# 시간 변환 (초 → 분, 초)
seconds = 125
minutes = seconds // 60
remaining_seconds = seconds % 60
print(f"{minutes}분 {remaining_seconds}초")
```

## 2. 비교 연산자 (Comparison Operators)

| 연산자 | 설명 |
|--------|------|
| `==` | 같다 |
| `!=` | 다르다 |
| `>` | 크다 |
| `<` | 작다 |
| `>=` | 크거나 같다 |
| `<=` | 작거나 같다 |

```python
print(5 == 5)    # True
print(5 != 3)    # True
print(5 > 3)     # True
print(5 < 3)     # False
print(5 >= 5)    # True
print(5 <= 4)    # False

# 문자열 비교 (사전순)
print("apple" < "banana")  # True
print("abc" == "abc")      # True
```

### 체인 비교 (Python의 강점!)
```python
age = 25

# 일반적인 방법
if age >= 18 and age <= 65:
    print("성인")

# Python의 체인 비교 (권장)
if 18 <= age <= 65:
    print("성인")
```

## 3. 논리 연산자 (Logical Operators)

| 연산자 | 설명 |
|--------|------|
| `and` | 모두 참이면 참 |
| `or` | 하나라도 참이면 참 |
| `not` | 부정 |

```python
print(True and True)    # True
print(True and False)   # False
print(True or False)    # True
print(False or False)   # False
print(not True)         # False

# 실용 예시
age = 25
has_license = True
if age >= 18 and has_license:
    print("운전 가능")
```

### Short-Circuit Evaluation (단축 평가)
Python은 결과가 확정되면 나머지를 평가하지 않습니다.

```python
def expensive_check():
    print("호출됨!")
    return True

# False and X → X 평가 안 함
result = False and expensive_check()  # "호출됨!" 출력 안 됨
print(result)  # False

# True or X → X 평가 안 함
result = True or expensive_check()    # "호출됨!" 출력 안 됨
print(result)  # True
```

### 논리 연산자의 반환값
Python의 `and`, `or` 는 불리언이 아닌 **값**을 반환합니다.

```python
print(0 or "Hello")      # "Hello"  (첫 truthy 값)
print("a" or "b")        # "a"
print(0 and "Hello")     # 0  (첫 falsy 값)
print("a" and "b")       # "b"

# 기본값 설정 패턴
name = input("이름: ") or "익명"
```

## 4. 할당 연산자 (Assignment Operators)

| 연산자 | 의미 | 예시 |
|--------|------|------|
| `=` | 할당 | `x = 5` |
| `+=` | 더하고 할당 | `x += 3` |
| `-=` | 빼고 할당 | `x -= 3` |
| `*=` | 곱하고 할당 | `x *= 3` |
| `/=` | 나누고 할당 | `x /= 3` |
| `//=` | 몫 할당 | `x //= 3` |
| `%=` | 나머지 할당 | `x %= 3` |
| `**=` | 거듭제곱 할당 | `x **= 3` |

```python
x = 10
x += 5   # x = x + 5 → 15
x -= 3   # x = x - 3 → 12
x *= 2   # x = x * 2 → 24
x //= 5  # x = x // 5 → 4
print(x) # 4
```

### Walrus 연산자 (`:=`, Python 3.8+)
표현식 안에서 할당이 가능합니다.

```python
# 기존 방식
data = input("입력: ")
if len(data) > 10:
    print(f"길이: {len(data)}")

# Walrus 연산자
if (n := len(data := input("입력: "))) > 10:
    print(f"길이: {n}")

# 반복문 활용
while (line := input("> ")) != "quit":
    print(f"입력값: {line}")
```

## 5. 멤버십 연산자 (Membership Operators)

| 연산자 | 설명 |
|--------|------|
| `in` | 포함되어 있다 |
| `not in` | 포함되지 않는다 |

```python
fruits = ["apple", "banana", "cherry"]
print("apple" in fruits)       # True
print("grape" in fruits)       # False
print("grape" not in fruits)   # True

# 문자열에서도 사용 가능
print("Py" in "Python")        # True
print("a" in "Python")         # False

# 딕셔너리는 키를 검사
ages = {"Alice": 25, "Bob": 30}
print("Alice" in ages)         # True
print(25 in ages)              # False (값이 아닌 키)
```

## 6. 동일성 연산자 (Identity Operators)

| 연산자 | 설명 |
|--------|------|
| `is` | 같은 객체인가 |
| `is not` | 다른 객체인가 |

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)      # True  (값이 같다)
print(a is b)      # False (서로 다른 객체)
print(a is c)      # True  (같은 객체)

# None 비교는 반드시 is 사용 (PEP 8)
x = None
if x is None:      # ✅ 권장
    pass
if x == None:      # ❌ 비권장
    pass
```

## 7. 비트 연산자 (Bitwise Operators)

| 연산자 | 설명 |
|--------|------|
| `&` | AND |
| `\|` | OR |
| `^` | XOR |
| `~` | NOT |
| `<<` | 왼쪽 시프트 |
| `>>` | 오른쪽 시프트 |

```python
a = 0b1100  # 12
b = 0b1010  # 10

print(bin(a & b))   # 0b1000 (8)
print(bin(a | b))   # 0b1110 (14)
print(bin(a ^ b))   # 0b110  (6)
print(bin(~a))      # -0b1101 (-13)
print(bin(a << 1))  # 0b11000 (24)
print(bin(a >> 1))  # 0b110   (6)
```

## 8. 연산자 우선순위

높은 우선순위부터 낮은 우선순위 순서:

| 우선순위 | 연산자 | 설명 |
|---------|--------|------|
| 1 | `()` | 괄호 |
| 2 | `**` | 거듭제곱 |
| 3 | `+x`, `-x`, `~x` | 단항 |
| 4 | `*`, `/`, `//`, `%` | 곱셈/나눗셈 |
| 5 | `+`, `-` | 덧셈/뺄셈 |
| 6 | `<<`, `>>` | 시프트 |
| 7 | `&` | 비트 AND |
| 8 | `^` | 비트 XOR |
| 9 | `\|` | 비트 OR |
| 10 | 비교 연산자 | `<`, `>`, `==` 등 |
| 11 | `not` | 논리 NOT |
| 12 | `and` | 논리 AND |
| 13 | `or` | 논리 OR |

```python
# 우선순위 예시
result = 2 + 3 * 4         # 14 (곱셈 먼저)
result = (2 + 3) * 4       # 20 (괄호 먼저)
result = 2 ** 3 ** 2       # 512 (오른쪽부터: 2^(3^2) = 2^9)

# 헷갈리면 괄호 사용 (가독성)
if (a > 0) and (b > 0):
    pass
```

## 9. 실전 예제

### 예제 1: 윤년 판별
```python
year = int(input("연도: "))
is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
print(f"{year}년은 윤년{'입니다' if is_leap else '이 아닙니다'}")
```

### 예제 2: 계산기
```python
a = float(input("첫 번째 숫자: "))
op = input("연산자 (+, -, *, /): ")
b = float(input("두 번째 숫자: "))

if op == '+':
    result = a + b
elif op == '-':
    result = a - b
elif op == '*':
    result = a * b
elif op == '/':
    result = a / b if b != 0 else "0으로 나눌 수 없음"
else:
    result = "잘못된 연산자"

print(f"결과: {result}")
```

## 📝 연습 문제

### 문제 1: 거스름돈 계산
1000원에서 입력받은 금액을 뺀 거스름돈을 500원, 100원, 50원, 10원 동전으로 환산하세요.

### 문제 2: 짝/홀수 카운트
1부터 100까지의 숫자 중 짝수의 개수와 홀수의 개수를 출력하세요. (힌트: `%` 사용)

### 문제 3: 비교 연산자 활용
세 숫자 중 가장 큰 수를 찾는 프로그램을 작성하세요. (`if/elif/else` 또는 `max()` 사용)

### 문제 4: 비밀번호 강도 체크
비밀번호를 입력받아 다음 조건을 모두 만족하는지 체크하세요.
- 8자 이상
- 숫자 포함
- 대문자 포함

## ✅ 체크리스트
- [ ] 산술 연산자를 사용할 수 있다
- [ ] `//` 와 `/` 의 차이를 안다
- [ ] 비교 연산자와 논리 연산자를 안다
- [ ] `in` 으로 멤버십을 확인할 수 있다
- [ ] `is` 와 `==` 의 차이를 안다
- [ ] 연산자 우선순위를 이해한다

## 🔗 다음 챕터
👉 [04. 제어문 (조건문/반복문)](./04-control-flow.md)
