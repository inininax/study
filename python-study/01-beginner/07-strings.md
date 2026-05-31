# 07. 문자열 처리

## 🎯 학습 목표
- 문자열의 다양한 메서드를 활용할 수 있다
- 문자열 포맷팅을 자유롭게 한다
- 문자열을 분리하고 합칠 수 있다

## 1. 문자열 기본

### 1.1 생성
```python
# 작은따옴표, 큰따옴표 (동일)
s1 = 'Hello'
s2 = "World"

# 여러 줄
s3 = """첫 번째 줄
두 번째 줄
세 번째 줄"""

# 이스케이프
s4 = "She said \"Hi\""
s5 = 'She said \'Hi\''
s6 = "C:\\Users\\Alice"
s7 = "Line1\nLine2"     # 줄바꿈
s8 = "Tab\there"        # 탭

# Raw 문자열 (이스케이프 무시)
path = r"C:\Users\Alice\new_folder"
regex = r"\d+"
```

### 1.2 문자열은 불변 (Immutable)
```python
s = "Hello"
# s[0] = "h"    # TypeError!

# 새 문자열을 만들어야 함
s = "h" + s[1:]
print(s)  # hello
```

### 1.3 인덱싱과 슬라이싱
```python
s = "Python"

# 인덱싱
print(s[0])     # P
print(s[-1])    # n
print(s[2])     # t

# 슬라이싱
print(s[0:3])   # Pyt
print(s[2:])    # thon
print(s[:4])    # Pyth
print(s[::2])   # Pto
print(s[::-1])  # nohtyP (역순)
```

## 2. 문자열 메서드

### 2.1 대소문자 변환
```python
s = "Hello, World!"

print(s.upper())        # HELLO, WORLD!
print(s.lower())        # hello, world!
print(s.title())        # Hello, World!
print(s.capitalize())   # Hello, world!
print(s.swapcase())     # hELLO, wORLD!
```

### 2.2 검색과 카운트
```python
s = "Python is fun, Python is powerful"

# find/rfind (못 찾으면 -1)
print(s.find("Python"))     # 0 (첫 위치)
print(s.find("Java"))       # -1
print(s.rfind("Python"))    # 15 (오른쪽부터)

# index/rindex (못 찾으면 ValueError)
print(s.index("is"))        # 7

# count
print(s.count("Python"))    # 2

# startswith/endswith
print(s.startswith("Py"))   # True
print(s.endswith("!"))      # False
print(s.endswith(("ful", "!")))  # 튜플로 여러 개
```

### 2.3 검증
```python
print("abc".isalpha())      # True (알파벳만)
print("123".isdigit())      # True (숫자만)
print("abc123".isalnum())   # True (알파벳+숫자)
print("   ".isspace())      # True (공백만)
print("Hello".istitle())    # True (제목 형식)
print("HELLO".isupper())    # True
print("hello".islower())    # True
print("123".isnumeric())    # True
print("hello_world".isidentifier())  # True (변수명 가능)
```

### 2.4 공백 제거
```python
s = "   Hello, World!   "

print(s.strip())            # "Hello, World!"
print(s.lstrip())           # "Hello, World!   "
print(s.rstrip())           # "   Hello, World!"

# 특정 문자 제거
print("###Hello###".strip("#"))  # "Hello"
print("www.example.com".strip("cmow."))  # "example"
```

### 2.5 분리와 결합
```python
# split
s = "apple,banana,cherry"
print(s.split(","))             # ['apple', 'banana', 'cherry']

s = "Hello World Python"
print(s.split())                # ['Hello', 'World', 'Python']
print(s.split(" ", 1))          # ['Hello', 'World Python'] (1회만)

# splitlines (줄 단위 분리)
text = "Line1\nLine2\nLine3"
print(text.splitlines())        # ['Line1', 'Line2', 'Line3']

# rsplit (오른쪽부터)
print("a-b-c-d".rsplit("-", 1)) # ['a-b-c', 'd']

# join
words = ["Hello", "World", "Python"]
print(" ".join(words))          # "Hello World Python"
print("-".join(words))          # "Hello-World-Python"
print("".join(words))           # "HelloWorldPython"
```

### 2.6 치환
```python
s = "Hello, World!"
print(s.replace("World", "Python"))      # Hello, Python!
print("aaa".replace("a", "b"))           # bbb
print("aaa".replace("a", "b", 2))        # bba (2회만)

# 여러 문자 치환 (str.translate)
table = str.maketrans("aeiou", "AEIOU")
print("hello world".translate(table))    # hEllO wOrld
```

### 2.7 정렬과 패딩
```python
s = "Hello"
print(s.center(11, "*"))    # ***Hello***
print(s.ljust(10, "-"))     # Hello-----
print(s.rjust(10, "-"))     # -----Hello

# zfill (0으로 채우기)
print("42".zfill(5))        # 00042
print("-42".zfill(5))       # -0042
```

## 3. 문자열 포맷팅

### 3.1 f-string (Python 3.6+, 권장 ✅)
```python
name = "Alice"
age = 25

# 기본
print(f"이름: {name}, 나이: {age}")

# 표현식
print(f"내년: {age + 1}")
print(f"대문자: {name.upper()}")

# 너비/정렬
print(f"{name:>10}")    # 오른쪽 정렬, 폭 10
print(f"{name:<10}")    # 왼쪽 정렬
print(f"{name:^10}")    # 가운데 정렬
print(f"{name:*^10}")   # *로 채우기

# 숫자 포맷
pi = 3.14159
print(f"{pi:.2f}")      # 3.14 (소수점 2자리)
print(f"{pi:10.2f}")    # "      3.14" (폭 10)
print(f"{1000000:,}")   # 1,000,000 (천 단위 콤마)
print(f"{0.5:.0%}")     # 50% (퍼센트)
print(f"{255:b}")       # 11111111 (2진수)
print(f"{255:o}")       # 377 (8진수)
print(f"{255:x}")       # ff (16진수)
print(f"{255:X}")       # FF

# 디버깅 (Python 3.8+)
x = 42
print(f"{x=}")          # x=42

# 중첩
width = 10
precision = 2
value = 3.14159
print(f"{value:{width}.{precision}f}")
```

### 3.2 format() 메서드
```python
print("{} {}".format("Hello", "World"))
print("{0} {1} {0}".format("Hi", "there"))
print("{name} is {age}".format(name="Alice", age=25))
print("{:.2f}".format(3.14159))
```

### 3.3 % 포맷팅 (구식)
```python
# 사용 비권장 (f-string 사용)
print("Hello, %s! You are %d years old." % ("Alice", 25))
print("%.2f" % 3.14159)
```

## 4. 인코딩과 디코딩

### 4.1 문자열과 바이트
```python
# 문자열 → 바이트
s = "Python 한글"
b = s.encode("utf-8")
print(b)  # b'Python \xed\x95\x9c\xea\xb8\x80'

# 바이트 → 문자열
decoded = b.decode("utf-8")
print(decoded)  # Python 한글
```

### 4.2 다양한 인코딩
```python
text = "한글"
print(text.encode("utf-8"))     # 3바이트씩
print(text.encode("euc-kr"))    # 2바이트씩
print(text.encode("cp949"))     # Windows 한글
```

## 5. 정규표현식 미리보기

```python
import re

text = "전화번호는 010-1234-5678 입니다"

# 패턴 검색
match = re.search(r"\d{3}-\d{4}-\d{4}", text)
if match:
    print(match.group())  # 010-1234-5678

# 모든 매치
phones = re.findall(r"\d+", text)
print(phones)  # ['010', '1234', '5678']
```

> 📚 정규표현식은 [중급/06-regex.md](../02-intermediate/06-regex.md) 에서 자세히 다룹니다.

## 6. 자주 쓰는 문자열 작업

### 6.1 회문 판별
```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(is_palindrome("level"))           # True
print(is_palindrome("A man a plan"))    # False
```

### 6.2 단어 카운트
```python
text = "Python is great and Python is powerful"
words = text.split()
word_count = len(words)
print(f"단어 수: {word_count}")
```

### 6.3 첫 글자 대문자
```python
# title()의 문제: 아포스트로피 뒤도 대문자
print("it's nice".title())     # "It'S Nice" (이상함)

# 개선
def proper_title(s):
    return " ".join(w.capitalize() for w in s.split())

print(proper_title("it's nice"))  # "It's Nice"
```

### 6.4 문자열에서 숫자 추출
```python
text = "abc123def456"

# 방법 1: 정규표현식
import re
numbers = re.findall(r"\d+", text)
print(numbers)  # ['123', '456']

# 방법 2: 컴프리헨션
digits = "".join(c for c in text if c.isdigit())
print(digits)  # "123456"
```

### 6.5 문자열 뒤집기
```python
s = "Hello"
print(s[::-1])              # olleH
print("".join(reversed(s))) # olleH
```

## 7. 문자열 비교

```python
# 정확한 비교
print("hello" == "hello")           # True
print("hello" == "Hello")           # False

# 대소문자 무시 비교
print("hello".lower() == "Hello".lower())  # True
print("hello".casefold() == "HELLO".casefold())  # True (더 강력)

# 사전순 비교
print("apple" < "banana")           # True
print("Banana" < "apple")           # True (대문자가 작음)
```

## 8. 멀티라인 문자열 처리

```python
text = """첫 번째 줄
두 번째 줄
세 번째 줄"""

# 줄 단위로 분리
lines = text.splitlines()
print(lines)  # ['첫 번째 줄', '두 번째 줄', '세 번째 줄']

# 각 줄의 앞 공백 제거 (들여쓰기 제거)
import textwrap
indented = """
    Hello
    World
"""
print(textwrap.dedent(indented))
```

## 9. 실전 예제

### 예제 1: 이메일 유효성 검사 (간단 버전)
```python
def is_valid_email(email):
    if "@" not in email:
        return False
    local, domain = email.rsplit("@", 1)
    if not local or not domain:
        return False
    if "." not in domain:
        return False
    return True

print(is_valid_email("user@example.com"))  # True
print(is_valid_email("invalid"))           # False
```

### 예제 2: 비밀번호 강도 체크
```python
def check_password(password):
    if len(password) < 8:
        return "약함: 8자 이상이어야 합니다"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if score == 4:
        return "강함"
    elif score == 3:
        return "보통"
    return "약함"

print(check_password("password"))         # 약함
print(check_password("Password1"))        # 보통
print(check_password("P@ssword1!"))       # 강함
```

### 예제 3: CSV 파싱
```python
csv_line = "Alice,25,Seoul,Developer"
fields = csv_line.split(",")
name, age, city, job = fields
print(f"이름: {name}, 나이: {age}")
```

## 📝 연습 문제

### 문제 1: 단어 뒤집기
"Hello World" → "World Hello" 로 변환하세요.

### 문제 2: 모음 개수 세기
문자열에서 모음(a, e, i, o, u)의 개수를 세는 함수를 작성하세요.

### 문제 3: 대소문자 변환
문자열의 대소문자를 서로 바꾸세요. (swapcase 사용 금지)

### 문제 4: 압축
"aaabbbccd" → "a3b3c2d1" 로 압축하세요.

### 문제 5: 문장 첫 글자 대문자
"hello world. python is fun." → "Hello world. Python is fun."

## ✅ 체크리스트
- [ ] 문자열 슬라이싱을 자유롭게 한다
- [ ] split() 과 join() 을 활용할 수 있다
- [ ] f-string 으로 문자열을 포맷할 수 있다
- [ ] 문자열 검색/치환을 할 수 있다
- [ ] strip(), upper(), lower() 등 자주 쓰는 메서드를 안다

## 🔗 다음 챕터
👉 [08. 입출력 (I/O)](./08-io.md)
