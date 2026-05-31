# 06. 정규표현식 (Regular Expression)

## 🎯 학습 목표
- 정규표현식의 기본 문법을 안다
- re 모듈을 활용한다
- 문자열 패턴을 검색/추출/치환한다

## 1. 정규표현식이란?

**문자열의 패턴**을 표현하는 형식 언어입니다.

### 기본 사용
```python
import re

text = "전화번호: 010-1234-5678"
pattern = r"\d{3}-\d{4}-\d{4}"

match = re.search(pattern, text)
if match:
    print(match.group())  # 010-1234-5678
```

> 💡 `r"..."` (raw string) 을 사용하면 백슬래시 이스케이프 헷갈림이 없어집니다.

## 2. 메타 문자

### 2.1 문자 클래스
| 패턴 | 의미 |
|------|------|
| `.` | 모든 문자 (줄바꿈 제외) |
| `\d` | 숫자 [0-9] |
| `\D` | 숫자 아님 |
| `\w` | 단어 문자 [a-zA-Z0-9_] |
| `\W` | 단어 문자 아님 |
| `\s` | 공백 (스페이스, 탭, 줄바꿈) |
| `\S` | 공백 아님 |
| `[abc]` | a, b, c 중 하나 |
| `[a-z]` | a-z 중 하나 |
| `[^abc]` | a, b, c 가 아닌 |

```python
re.search(r"\d", "abc123")        # '1'
re.search(r"[a-z]+", "Hello World") # 'ello'
re.search(r"[^0-9]+", "abc123")    # 'abc'
```

### 2.2 수량자
| 패턴 | 의미 |
|------|------|
| `*` | 0개 이상 |
| `+` | 1개 이상 |
| `?` | 0개 또는 1개 |
| `{n}` | 정확히 n개 |
| `{n,}` | n개 이상 |
| `{n,m}` | n개 이상 m개 이하 |
| `*?`, `+?` | 비탐욕적 (최소 매칭) |

```python
re.search(r"a*", "aaab")          # 'aaa'
re.search(r"\d{3}", "abc1234")    # '123'
re.search(r"\d{3,5}", "12345678") # '12345'

# 탐욕적 vs 비탐욕적
re.search(r"<.*>", "<b>text</b>")   # '<b>text</b>'
re.search(r"<.*?>", "<b>text</b>")  # '<b>'
```

### 2.3 위치 (앵커)
| 패턴 | 의미 |
|------|------|
| `^` | 문자열/줄의 시작 |
| `$` | 문자열/줄의 끝 |
| `\b` | 단어 경계 |
| `\B` | 단어 경계 아님 |

```python
re.search(r"^Hello", "Hello World")  # 'Hello'
re.search(r"World$", "Hello World")  # 'World'
re.search(r"\bcat\b", "concat cat")  # 'cat' (두 번째)
```

### 2.4 그룹화와 선택
```python
# 그룹화 ()
re.search(r"(ab)+", "ababab")  # 'ababab'

# 선택 |
re.search(r"cat|dog", "I love dogs")  # 'dog'

# 비캡처 그룹 (?:...)
re.search(r"(?:ab)+", "ababab")  # 그룹 캡처 안 함
```

## 3. re 모듈 함수

### 3.1 re.search() — 첫 매치
```python
text = "이메일: alice@example.com"
m = re.search(r"\w+@\w+\.\w+", text)
if m:
    print(m.group())     # alice@example.com
    print(m.start())     # 4
    print(m.end())       # 22
    print(m.span())      # (4, 22)
```

### 3.2 re.match() — 시작만 매치
```python
re.match(r"\d+", "123abc")    # 매치: '123'
re.match(r"\d+", "abc123")    # 매치 없음 (시작에 없음)
```

### 3.3 re.fullmatch() — 전체 매치
```python
re.fullmatch(r"\d+", "12345")    # 매치
re.fullmatch(r"\d+", "123abc")   # 매치 없음
```

### 3.4 re.findall() — 모든 매치 (리스트)
```python
text = "010-1234-5678, 02-987-6543"
phones = re.findall(r"\d+-\d+-\d+", text)
print(phones)  # ['010-1234-5678', '02-987-6543']

# 그룹 사용 시 그룹만 반환
emails = re.findall(r"(\w+)@(\w+)", "alice@gmail, bob@naver")
print(emails)  # [('alice', 'gmail'), ('bob', 'naver')]
```

### 3.5 re.finditer() — 매치 객체 이터레이터
```python
text = "Tel: 010-1111-2222, 02-333-4444"
for m in re.finditer(r"\d+-\d+-\d+", text):
    print(f"{m.group()} at {m.start()}-{m.end()}")
```

### 3.6 re.sub() — 치환
```python
# 기본 치환
re.sub(r"\d+", "###", "abc123def456")  # 'abc###def###'

# 횟수 제한
re.sub(r"\d+", "#", "1 2 3 4", count=2)  # '# # 3 4'

# 함수로 치환
def double(m):
    return str(int(m.group()) * 2)

re.sub(r"\d+", double, "a1 b2 c3")  # 'a2 b4 c6'

# 그룹 참조
re.sub(r"(\w+) (\w+)", r"\2 \1", "Hello World")  # 'World Hello'
```

### 3.7 re.split() — 분할
```python
re.split(r"[\s,;]+", "a,b;c d  e")
# ['a', 'b', 'c', 'd', 'e']

re.split(r"\d+", "abc1def22ghi333")
# ['abc', 'def', 'ghi', '']
```

### 3.8 re.compile() — 패턴 컴파일
반복 사용할 패턴은 미리 컴파일하면 빠릅니다.

```python
phone_pattern = re.compile(r"\d{3}-\d{4}-\d{4}")

phone_pattern.search("010-1234-5678")
phone_pattern.findall("...")
phone_pattern.sub("###", "...")
```

## 4. 그룹 (Groups)

### 4.1 위치 그룹
```python
text = "이름: 홍길동, 나이: 25"
m = re.search(r"이름: (\w+), 나이: (\d+)", text)
print(m.group())   # 전체: '이름: 홍길동, 나이: 25'
print(m.group(0))  # 전체
print(m.group(1))  # 홍길동
print(m.group(2))  # 25
print(m.groups())  # ('홍길동', '25')
```

### 4.2 이름 그룹 (?P<name>...)
```python
m = re.search(r"(?P<name>\w+) (?P<age>\d+)", "Alice 25")
print(m.group("name"))   # Alice
print(m.group("age"))    # 25
print(m.groupdict())     # {'name': 'Alice', 'age': '25'}

# 그룹 참조
re.sub(r"(?P<word>\w+)", r"\g<word>!", "hello world")
# 'hello! world!'
```

## 5. 플래그 (Flags)

```python
# re.IGNORECASE / re.I — 대소문자 무시
re.findall(r"python", "Python PYTHON python", re.I)
# ['Python', 'PYTHON', 'python']

# re.MULTILINE / re.M — ^, $ 가 각 줄에 적용
text = "line1\nline2\nline3"
re.findall(r"^line\d", text, re.M)
# ['line1', 'line2', 'line3']

# re.DOTALL / re.S — . 이 줄바꿈도 매치
re.search(r"a.b", "a\nb")          # None
re.search(r"a.b", "a\nb", re.S)    # 매치

# re.VERBOSE / re.X — 가독성을 위한 공백/주석 허용
pattern = re.compile(r"""
    \d{3}    # 지역번호
    -
    \d{4}    # 국번
    -
    \d{4}    # 끝번호
""", re.X)

# 여러 플래그 조합
re.findall(r"python", text, re.I | re.M)
```

## 6. 자주 쓰이는 패턴

### 6.1 이메일
```python
EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")

emails = EMAIL_RE.findall(text)
```

> 💡 완벽한 이메일 정규식은 매우 복잡합니다. 검증은 라이브러리(`email-validator`) 사용을 권장.

### 6.2 URL
```python
URL_RE = re.compile(r"https?://[\w\.-]+(?:/[\w\.-/?%&=]*)?")
```

### 6.3 한국 전화번호
```python
PHONE_RE = re.compile(r"01[016789]-\d{3,4}-\d{4}")

# 또는 더 일반적으로
PHONE_RE = re.compile(r"\d{2,3}-\d{3,4}-\d{4}")
```

### 6.4 IP 주소
```python
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

# 더 엄격하게
IP_RE = re.compile(
    r"\b(?:25[0-5]|2[0-4]\d|1?\d?\d)"
    r"(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b"
)
```

### 6.5 날짜
```python
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")  # 2026-05-12
DATE_RE_KR = re.compile(r"\d{4}년 \d{1,2}월 \d{1,2}일")
```

### 6.6 한글
```python
KOR_RE = re.compile(r"[가-힣]+")

re.findall(KOR_RE, "Hello 안녕하세요 World 반갑습니다")
# ['안녕하세요', '반갑습니다']
```

### 6.7 비밀번호 강도
```python
# 8자 이상, 대소문자 + 숫자
PWD_RE = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")

PWD_RE.fullmatch("Password1")    # 매치
PWD_RE.fullmatch("password")     # None
```

## 7. 룩어라운드 (Lookaround)

### 7.1 전방 탐색
```python
# 긍정 전방 ?= : 뒤에 ~이 있는
re.findall(r"\d+(?=원)", "100원 200달러 300원")
# ['100', '300']

# 부정 전방 ?! : 뒤에 ~이 없는
re.findall(r"\d+(?!원)", "100원 200달러 300원")
# ['200']
```

### 7.2 후방 탐색
```python
# 긍정 후방 ?<= : 앞에 ~이 있는
re.findall(r"(?<=\$)\d+", "$100 200 $300")
# ['100', '300']

# 부정 후방 ?<! : 앞에 ~이 없는
re.findall(r"(?<!\$)\d+", "$100 200 $300")
# ['00', '200', '00']  (주의: 일치하는 부분 다 찾음)
```

## 8. 매치 객체 (Match Object)

```python
m = re.search(r"(\w+) (\w+)", "Hello World")

m.group()       # 'Hello World'
m.group(0)      # 'Hello World'
m.group(1)      # 'Hello'
m.group(2)      # 'World'
m.groups()      # ('Hello', 'World')

m.start()       # 0
m.end()         # 11
m.span()        # (0, 11)
m.start(1)      # 첫 그룹의 시작

m.string        # 원본 문자열
m.re.pattern    # 사용한 패턴
```

## 9. 실전 예제

### 예제 1: 텍스트에서 정보 추출
```python
import re

text = """
사용자 정보:
- 이름: Alice
- 이메일: alice@example.com
- 전화: 010-1234-5678
- 생년월일: 2000-01-15

사용자 정보:
- 이름: Bob
- 이메일: bob@test.org
- 전화: 010-9876-5432
- 생년월일: 1995-05-20
"""

pattern = re.compile(
    r"이름: (?P<name>\w+).*?"
    r"이메일: (?P<email>\S+).*?"
    r"전화: (?P<phone>[\d-]+).*?"
    r"생년월일: (?P<dob>\d{4}-\d{2}-\d{2})",
    re.S
)

for m in pattern.finditer(text):
    print(m.groupdict())
```

### 예제 2: 로그 파싱
```python
log = """
2026-05-12 10:00:01 [INFO] Server started
2026-05-12 10:00:05 [WARNING] High memory: 85%
2026-05-12 10:00:10 [ERROR] Connection failed
"""

LOG_RE = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) "
    r"(?P<time>\d{2}:\d{2}:\d{2}) "
    r"\[(?P<level>\w+)\] "
    r"(?P<msg>.+)"
)

errors = []
for line in log.strip().split("\n"):
    m = LOG_RE.match(line)
    if m and m.group("level") == "ERROR":
        errors.append(m.groupdict())

print(errors)
```

### 예제 3: HTML 태그 제거
```python
def strip_html(html):
    return re.sub(r"<[^>]+>", "", html)

html = "<p>안녕하세요, <b>홍길동</b>님!</p>"
print(strip_html(html))  # 안녕하세요, 홍길동님!
```

> ⚠️ 실제 HTML 파싱은 BeautifulSoup, lxml 등 라이브러리 사용 권장!

### 예제 4: 변수명 검증
```python
def is_valid_identifier(name):
    return bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name))

print(is_valid_identifier("user_name"))  # True
print(is_valid_identifier("2nd_user"))   # False (숫자로 시작)
print(is_valid_identifier("my-var"))     # False (- 포함)
```

### 예제 5: URL slug 생성
```python
def slugify(text):
    # 영숫자, 한글, 공백, 하이픈만 남김
    text = re.sub(r"[^\w\s-가-힣]", "", text.lower())
    # 공백을 하이픈으로
    text = re.sub(r"[\s]+", "-", text.strip())
    return text

print(slugify("Hello World! 안녕하세요?"))
# 'hello-world-안녕하세요'
```

## 10. 성능과 주의사항

### 컴파일 활용
```python
# ❌ 매번 컴파일
for line in lines:
    if re.search(r"\d+", line):
        process(line)

# ✅ 한 번만 컴파일
pattern = re.compile(r"\d+")
for line in lines:
    if pattern.search(line):
        process(line)
```

### 비탐욕 매칭 활용
```python
# ❌ 탐욕적 (느릴 수 있음)
re.findall(r"<.*>", html)

# ✅ 비탐욕적
re.findall(r"<.*?>", html)
```

### 너무 복잡하면 코드로
정규식이 너무 길고 복잡하면 가독성이 떨어집니다. 코드로 분리하는 것을 고려하세요.

## 📝 연습 문제

### 문제 1: 전화번호 추출
텍스트에서 모든 전화번호(010-XXXX-XXXX)를 추출하세요.

### 문제 2: 이메일 마스킹
이메일의 @ 앞부분 첫 글자만 남기고 나머지는 * 로 치환하세요.
예: `alice@example.com` → `a****@example.com`

### 문제 3: 날짜 형식 변환
`2026/05/12` → `2026-05-12` 로 변환하세요.

### 문제 4: 숫자만 추출
문자열에서 모든 정수를 추출해 리스트로 반환하세요.
예: `"abc 123 def 456"` → `[123, 456]`

### 문제 5: 비밀번호 검증
다음 조건을 모두 만족하는지 정규식으로 검증하세요.
- 8-20자
- 대문자, 소문자, 숫자, 특수문자 모두 포함

## ✅ 체크리스트
- [ ] 기본 메타문자(`\d`, `\w`, `.` 등)를 안다
- [ ] 수량자(`*`, `+`, `?`, `{n,m}`)를 안다
- [ ] re.search, findall, sub 를 사용한다
- [ ] 그룹과 이름 그룹을 활용한다
- [ ] 자주 쓰는 패턴을 작성할 수 있다

## 🔗 다음 챕터
👉 [07. 컴프리헨션과 제너레이터](./07-comprehensions-generators.md)
