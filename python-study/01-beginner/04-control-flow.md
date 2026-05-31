# 04. 제어문 (조건문과 반복문)

## 🎯 학습 목표
- if/elif/else 조건문을 사용할 수 있다
- for 반복문과 while 반복문의 차이를 안다
- break, continue, else를 활용할 수 있다

## 1. 조건문 (if)

### 기본 구조
```python
if 조건:
    # 조건이 참일 때 실행
    pass
```

⚠️ **Python은 들여쓰기(indentation)로 블록을 구분합니다!** (4칸 권장)

### 1.1 단순 if
```python
age = 20

if age >= 18:
    print("성인입니다")
```

### 1.2 if-else
```python
score = 75

if score >= 60:
    print("합격")
else:
    print("불합격")
```

### 1.3 if-elif-else
```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"등급: {grade}")
```

### 1.4 중첩 if
```python
age = 25
has_license = True

if age >= 18:
    if has_license:
        print("운전 가능")
    else:
        print("면허 필요")
else:
    print("미성년자")
```

> 💡 **팁**: 중첩이 깊어지면 가독성이 떨어집니다. 가능하면 `and`/`or` 로 합치거나 함수로 분리하세요.

### 1.5 삼항 연산자 (Conditional Expression)
```python
# 일반 if-else
if score >= 60:
    result = "합격"
else:
    result = "불합격"

# 삼항 연산자
result = "합격" if score >= 60 else "불합격"

# 활용
max_value = a if a > b else b
status = "성인" if age >= 18 else "미성년"
```

### 1.6 Truthy / Falsy
조건문에서 자동으로 불리언으로 변환되는 값들:

**Falsy (False로 평가)**
- `False`, `None`
- `0`, `0.0`, `0j`
- `""` (빈 문자열)
- `[]` (빈 리스트)
- `()` (빈 튜플)
- `{}` (빈 딕셔너리)
- `set()` (빈 셋)

```python
name = ""
if not name:
    print("이름을 입력하세요")

items = []
if items:        # ✅ Pythonic
    print("아이템 있음")
else:
    print("비어 있음")

# ❌ 덜 Pythonic
if len(items) > 0:
    print("아이템 있음")
```

### 1.7 match-case 문 (Python 3.10+)
```python
def describe_status(status):
    match status:
        case 200:
            return "성공"
        case 404:
            return "찾을 수 없음"
        case 500 | 502 | 503:  # 여러 값 매칭
            return "서버 오류"
        case code if code >= 400:  # 가드
            return f"클라이언트 오류: {code}"
        case _:  # 기본값 (와일드카드)
            return "알 수 없음"

print(describe_status(200))  # 성공
print(describe_status(404))  # 찾을 수 없음
print(describe_status(503))  # 서버 오류
```

## 2. for 반복문

`for` 는 **시퀀스(sequence)** 의 각 요소를 순회합니다.

### 2.1 기본 구조
```python
for 변수 in 시퀀스:
    # 반복 실행할 코드
    pass
```

### 2.2 리스트 순회
```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

### 2.3 range() 함수
```python
# range(stop)
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop)
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# 역순
for i in range(10, 0, -1):
    print(i)  # 10, 9, ..., 1
```

### 2.4 문자열 순회
```python
for char in "Python":
    print(char)
# P, y, t, h, o, n
```

### 2.5 enumerate() — 인덱스와 함께
```python
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# 시작 인덱스 지정
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
```

### 2.6 zip() — 여러 시퀀스 동시 순회
```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

for name, age in zip(names, ages):
    print(f"{name}: {age}살")
```

### 2.7 딕셔너리 순회
```python
scores = {"Alice": 90, "Bob": 85, "Charlie": 92}

# 키 순회 (기본)
for name in scores:
    print(name)

# 값 순회
for score in scores.values():
    print(score)

# 키-값 모두 순회
for name, score in scores.items():
    print(f"{name}: {score}")
```

### 2.8 reversed() — 역순 순회
```python
for i in reversed(range(5)):
    print(i)  # 4, 3, 2, 1, 0

for fruit in reversed(["a", "b", "c"]):
    print(fruit)  # c, b, a
```

## 3. while 반복문

조건이 참인 동안 반복합니다.

```python
count = 0
while count < 5:
    print(count)
    count += 1  # 잊지 말기! 무한루프 방지
```

### 활용 예시: 사용자 입력 검증
```python
while True:
    age = input("나이를 입력하세요: ")
    if age.isdigit():
        age = int(age)
        break
    print("숫자만 입력해주세요!")

print(f"입력한 나이: {age}")
```

## 4. break와 continue

### break — 반복문 즉시 종료
```python
for i in range(10):
    if i == 5:
        break
    print(i)
# 0, 1, 2, 3, 4
```

### continue — 다음 반복으로 건너뛰기
```python
for i in range(10):
    if i % 2 == 0:
        continue  # 짝수 건너뛰기
    print(i)
# 1, 3, 5, 7, 9
```

### 실용 예시
```python
# 첫 번째 짝수 찾기
numbers = [1, 3, 5, 7, 8, 9]
for num in numbers:
    if num % 2 == 0:
        print(f"첫 짝수: {num}")
        break

# 음수 제외하고 합 계산
numbers = [1, -2, 3, -4, 5]
total = 0
for num in numbers:
    if num < 0:
        continue
    total += num
print(f"양수의 합: {total}")  # 9
```

## 5. for/while-else 절

반복문이 **정상 종료** 되었을 때 실행됩니다. (`break` 로 종료되지 않은 경우)

```python
# 소수 판별
n = 7
for i in range(2, n):
    if n % i == 0:
        print(f"{n}은 소수가 아닙니다")
        break
else:
    print(f"{n}은 소수입니다")
```

```python
# while-else
count = 0
while count < 3:
    print(count)
    count += 1
else:
    print("정상 종료")
```

## 6. 중첩 반복문

```python
# 구구단
for i in range(2, 10):
    for j in range(1, 10):
        print(f"{i} x {j} = {i*j}")
    print()  # 단마다 빈 줄
```

### 별 찍기
```python
n = 5
for i in range(1, n + 1):
    print("*" * i)
# *
# **
# ***
# ****
# *****
```

## 7. 패스 (pass) 문

아무 동작도 하지 않는 자리표시자입니다.

```python
if True:
    pass  # 나중에 구현
else:
    pass

def my_function():
    pass  # 빈 함수
```

## 8. 실전 예제

### 예제 1: 숫자 맞추기 게임
```python
import random

target = random.randint(1, 100)
attempts = 0

while True:
    guess = int(input("1-100 사이 숫자: "))
    attempts += 1

    if guess == target:
        print(f"정답! {attempts}번 만에 맞췄어요")
        break
    elif guess < target:
        print("더 크게")
    else:
        print("더 작게")
```

### 예제 2: 피보나치 수열
```python
n = 10
a, b = 0, 1
for _ in range(n):
    print(a, end=" ")
    a, b = b, a + b
# 0 1 1 2 3 5 8 13 21 34
```

### 예제 3: 평균 점수 계산
```python
scores = []
print("점수를 입력하세요 (종료: -1):")
while True:
    score = int(input("> "))
    if score == -1:
        break
    scores.append(score)

if scores:
    avg = sum(scores) / len(scores)
    print(f"평균: {avg:.2f}")
else:
    print("입력된 점수가 없습니다")
```

## 📝 연습 문제

### 문제 1: FizzBuzz
1부터 100까지 출력하되:
- 3의 배수는 "Fizz"
- 5의 배수는 "Buzz"
- 15의 배수는 "FizzBuzz"
- 나머지는 숫자

### 문제 2: 누적 합
1부터 n까지 입력받아 누적 합을 계산하세요.

### 문제 3: 별 찍기 (피라미드)
```
    *
   ***
  *****
 *******
*********
```

### 문제 4: 약수 구하기
숫자를 입력받아 그 숫자의 모든 약수를 출력하세요.

### 문제 5: 소수 찾기
2부터 100까지의 소수를 모두 출력하세요.

## ✅ 체크리스트
- [ ] if/elif/else 를 사용할 수 있다
- [ ] for 와 range() 를 활용할 수 있다
- [ ] while 반복문을 작성할 수 있다
- [ ] break, continue 의 차이를 안다
- [ ] enumerate, zip 을 활용할 수 있다
- [ ] 들여쓰기를 정확히 한다 (4칸)

## 🔗 다음 챕터
👉 [05. 함수 기초](./05-functions-basics.md)
