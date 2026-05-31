# 05. 베스트 프랙티스와 코드 스타일

## 🎯 학습 목표
- PEP 8 스타일 가이드를 따른다
- Pythonic 한 코드를 작성한다
- 좋은 함수와 클래스 설계를 한다
- 코드 리뷰 시 체크할 점을 안다

## 1. PEP 8 — 스타일 가이드

### 1.1 들여쓰기
```python
# ✅ 4 칸 공백
def function():
    if condition:
        do_something()

# ❌ 탭 또는 다른 칸 수
def function():
	if condition:  # 탭 X
		pass
```

### 1.2 줄 길이
```python
# ✅ 79자 (또는 프로젝트 표준 88, 100)
result = some_function(arg1, arg2, arg3, arg4)

# ✅ 긴 줄 분리
result = some_function(
    arg1,
    arg2,
    arg3,
)

# 또는 괄호 사용
total = (first_value
         + second_value
         + third_value)
```

### 1.3 빈 줄
```python
# 모듈 레벨: 2 줄 분리
import os

import requests


def function_one():
    pass


def function_two():
    pass


class MyClass:
    # 메서드는 1줄 분리
    def method_one(self):
        pass

    def method_two(self):
        pass
```

### 1.4 임포트 순서
```python
# 1. 표준 라이브러리
import os
import sys
from datetime import datetime

# 2. 서드파티
import requests
from flask import Flask

# 3. 로컬
from myapp.models import User
from myapp.utils import helper
```

> 💡 isort 도구로 자동 정렬!

### 1.5 명명 규칙
```python
# 변수, 함수: snake_case
user_name = "Alice"
def get_user_data():
    pass

# 상수: UPPER_SNAKE_CASE
MAX_RETRY = 3
PI = 3.14159

# 클래스: PascalCase
class UserAccount:
    pass

class HTTPError(Exception):  # 약어는 그대로
    pass

# 비공개: _underscore
class MyClass:
    def __init__(self):
        self._private = 0      # 약한 비공개
        self.__name_mangled = 0  # 강한 비공개

# 매직 메서드: __dunder__
def __init__(self): pass
def __str__(self): pass
```

### 1.6 공백
```python
# ✅
x = 1
y = 2
spam(ham[1], {eggs: 2})
if x == 4:
    pass

# ❌
x=1                          # 연산자 주위 공백
spam( ham[ 1 ], { eggs: 2 })  # 괄호 안 공백
if x == 4 :                  # : 앞 공백
    pass
```

### 1.7 주석
```python
# ✅ 좋은 주석: 왜?
# 캐시 만료 시간은 비즈니스 정책으로 고정
CACHE_TTL = 3600

# ❌ 나쁜 주석: 무엇을? (코드만 봐도 앎)
x = x + 1  # x를 1 증가시킴

# ✅ 복잡한 로직 설명
# Boyer-Moore 알고리즘 사용 (검색 효율 O(n/m))
def search(text, pattern):
    ...
```

## 2. Pythonic 코드

### 2.1 EAFP > LBYL
```python
# ❌ LBYL (Look Before You Leap)
if key in d:
    value = d[key]
else:
    value = None

# ✅ EAFP (Easier to Ask Forgiveness)
try:
    value = d[key]
except KeyError:
    value = None

# ✅ 더 Pythonic
value = d.get(key)
```

### 2.2 컴프리헨션 활용
```python
# ❌
result = []
for x in items:
    if x > 0:
        result.append(x ** 2)

# ✅
result = [x ** 2 for x in items if x > 0]

# ❌
result = []
for x in items:
    result.append(transform(x))
result_filtered = []
for r in result:
    if condition(r):
        result_filtered.append(r)

# ✅
result = [transform(x) for x in items if condition(transform(x))]
# 너무 복잡하면 분리
```

### 2.3 enumerate / zip 사용
```python
# ❌
for i in range(len(items)):
    print(i, items[i])

# ✅
for i, item in enumerate(items):
    print(i, item)

# ❌
for i in range(len(names)):
    print(names[i], ages[i])

# ✅
for name, age in zip(names, ages):
    print(name, age)
```

### 2.4 진리값 활용
```python
# ❌
if len(items) > 0:
    pass
if x == True:
    pass
if x != None:
    pass

# ✅
if items:
    pass
if x:
    pass
if x is not None:  # None 비교는 is/is not
    pass
```

### 2.5 with 문 사용
```python
# ❌
f = open("file.txt")
data = f.read()
f.close()  # 예외 시 안 닫힘!

# ✅
with open("file.txt") as f:
    data = f.read()
```

### 2.6 f-string 사용
```python
# ❌ 구식
name = "Alice"
greeting = "Hello, " + name + "!"
greeting = "Hello, %s!" % name
greeting = "Hello, {}!".format(name)

# ✅ Pythonic
greeting = f"Hello, {name}!"

# 표현식, 포맷 모두 가능
greeting = f"Hi, {name.upper()}! Age: {age:>5}"
```

### 2.7 unpacking
```python
# ✅ 튜플 언패킹
a, b = 1, 2
a, b = b, a  # 스왑

# ✅ 함수 다중 반환
def get_min_max(nums):
    return min(nums), max(nums)

low, high = get_min_max([3, 1, 4])

# ✅ 별표 unpacking
first, *rest = [1, 2, 3, 4]
*init, last = [1, 2, 3, 4]

# ✅ 딕셔너리 unpacking
combined = {**dict1, **dict2}
```

### 2.8 collections 활용
```python
# ❌
counts = {}
for word in words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1

# ✅
from collections import Counter
counts = Counter(words)
```

## 3. 함수 설계

### 3.1 작고 명확한 함수
```python
# ❌ 너무 많은 일
def process_user(user):
    # 검증
    if not user.name: raise ...
    if user.age < 0: raise ...
    # DB 저장
    db.save(user)
    # 이메일 발송
    send_welcome_email(user)
    # 로그
    logger.info(...)
    # 통계
    update_stats(...)

# ✅ 단일 책임
def validate_user(user): ...
def save_user(user): ...
def notify_user_creation(user): ...

def process_user(user):
    validate_user(user)
    save_user(user)
    notify_user_creation(user)
```

### 3.2 명확한 인터페이스
```python
# ❌ 무엇을 받는지 불분명
def process(data, flag, mode=1):
    pass

# ✅ 타입 힌트와 명확한 이름
def process_user_data(
    user: User,
    *,
    is_admin: bool = False,
    mode: ProcessMode = ProcessMode.NORMAL,
) -> ProcessResult:
    """사용자 데이터를 처리합니다."""
    pass
```

### 3.3 키워드 전용 인자
```python
# ✅ 헷갈리는 boolean 은 키워드로
def create_user(name, *, is_admin=False, send_email=True):
    pass

# create_user("Alice", True, False)  # 의도 불명
create_user("Alice", is_admin=True, send_email=False)  # 명확
```

### 3.4 기본값 주의
```python
# ❌ 가변 기본값
def add_item(item, items=[]):  # 공유됨!
    items.append(item)
    return items

# ✅ None 사용
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 3.5 빠른 반환 (Early Return)
```python
# ❌ 깊은 중첩
def process(user):
    if user is not None:
        if user.is_active:
            if user.verified:
                # 실제 로직
                return do_something()
            else:
                return None
        else:
            return None
    else:
        return None

# ✅ 가드 절
def process(user):
    if user is None:
        return None
    if not user.is_active:
        return None
    if not user.verified:
        return None

    return do_something()
```

## 4. 클래스 설계

### 4.1 SRP (단일 책임)
```python
# ❌
class User:
    def save(self): ...
    def send_email(self): ...
    def format_json(self): ...

# ✅
class User: ...
class UserRepository:
    def save(self, user): ...
class EmailService:
    def send(self, user): ...
class UserSerializer:
    def to_json(self, user): ...
```

### 4.2 dataclass 활용
```python
# ❌ boilerplate
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# ✅ dataclass
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

### 4.3 property 활용
```python
# ❌ getter/setter 메서드
class Circle:
    def __init__(self, radius):
        self._radius = radius

    def get_radius(self):
        return self._radius

    def set_radius(self, value):
        if value < 0:
            raise ValueError
        self._radius = value

# ✅ property
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
```

### 4.4 상속보다 합성
```python
# ❌ 깊은 상속 계층
class Animal: ...
class Mammal(Animal): ...
class Dog(Mammal): ...
class ServiceDog(Dog): ...

# ✅ 합성 (composition)
class Dog:
    def __init__(self, breed, service_type=None):
        self.breed = breed
        self.service = service_type  # 합성
```

## 5. 에러 처리

### 5.1 구체적 예외
```python
# ❌ 너무 광범위
try:
    process()
except Exception:
    pass

# ✅ 구체적
try:
    process()
except (ValueError, KeyError) as e:
    logger.error(f"처리 실패: {e}")
    raise
```

### 5.2 try 블록은 좁게
```python
# ❌
try:
    data = load_data()
    processed = process(data)
    save(processed)
    notify()
except Exception:
    pass

# ✅
try:
    data = load_data()
except FileNotFoundError:
    logger.error("파일 없음")
    return

processed = process(data)
save(processed)
notify()
```

### 5.3 침묵하지 마세요
```python
# ❌
try:
    risky()
except:
    pass

# ✅ 최소한 로깅
try:
    risky()
except Exception as e:
    logger.exception(f"실패: {e}")
    raise  # 또는 적절한 처리
```

### 5.4 사용자 정의 예외
```python
class AppError(Exception):
    """앱 기본 예외"""

class ValidationError(AppError):
    """검증 실패"""

class NotFoundError(AppError):
    """리소스 없음"""

# 사용
def find_user(id):
    user = db.get(id)
    if not user:
        raise NotFoundError(f"User {id} not found")
    return user
```

## 6. 로깅

### 6.1 print 대신 logging
```python
# ❌
print(f"Processing {user}")

# ✅
import logging
logger = logging.getLogger(__name__)
logger.info("Processing %s", user)  # %-formatting (지연 평가)
```

### 6.2 적절한 레벨
```python
logger.debug("디버그 정보")     # 개발 시
logger.info("일반 정보")        # 정상 동작
logger.warning("주의 필요")     # 잠재 문제
logger.error("에러 발생")       # 처리된 에러
logger.critical("치명적 에러")  # 시스템 멈춤
```

### 6.3 예외 로깅
```python
try:
    risky()
except Exception:
    logger.exception("실패")  # 자동으로 트레이스백 포함
```

## 7. 테스트

### 7.1 테스트 가능한 코드
```python
# ❌ 의존성 직접 사용 (테스트 어려움)
def send_notification(user):
    smtp = smtplib.SMTP("...")
    smtp.send(...)

# ✅ 의존성 주입
def send_notification(user, mailer):
    mailer.send(user.email, "...")

# 테스트
def test_send_notification():
    mock_mailer = Mock()
    send_notification(user, mock_mailer)
    mock_mailer.send.assert_called_once()
```

### 7.2 작은 단위로
```python
# ❌ 한 번에 너무 많이 테스트
def test_everything():
    pass

# ✅ 작은 단위
def test_validation_valid_input():
    pass

def test_validation_empty_input():
    pass

def test_validation_invalid_format():
    pass
```

## 8. 보안

### 8.1 비밀 키 관리
```python
# ❌ 코드에 하드코딩
API_KEY = "sk-1234567890"

# ✅ 환경 변수
import os
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY 환경 변수 필요")
```

### 8.2 SQL injection 방지
```python
# ❌ 문자열 포맷
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")

# ✅ 파라미터화
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))

# ORM (더 안전)
session.query(User).filter_by(name=name).first()
```

### 8.3 비밀번호 해싱
```python
# ❌ 평문 저장
user.password = "plain_text"

# ✅ 해시
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])
user.password_hash = pwd_context.hash("plain_text")
```

## 9. 도구 사용

### 9.1 추천 도구
| 도구 | 용도 |
|------|------|
| **black** | 코드 포매터 |
| **ruff** | 빠른 린터 (Black 대체 가능) |
| **isort** | import 정렬 |
| **mypy** | 정적 타입 체크 |
| **pylint** / **flake8** | 린터 |
| **bandit** | 보안 검사 |
| **pytest** | 테스트 |
| **coverage** | 커버리지 |

### 9.2 pre-commit 훅
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
```

```bash
pip install pre-commit
pre-commit install

# 이제 커밋 시 자동 실행
git commit -m "..."
```

## 10. 코드 리뷰 체크리스트

### 코드 품질
- [ ] 함수가 50줄 이하인가?
- [ ] 파일이 800줄 이하인가?
- [ ] 변수/함수 이름이 명확한가?
- [ ] 코드 중복이 없는가?
- [ ] 매직 넘버가 상수로 추출되었나?

### 가독성
- [ ] PEP 8 준수하는가?
- [ ] f-string 사용했는가?
- [ ] 컴프리헨션이 적절한가? (너무 복잡 X)
- [ ] 들여쓰기가 4 단계 이하인가?

### 안전성
- [ ] 입력이 검증되는가?
- [ ] 예외가 적절히 처리되는가?
- [ ] 자원이 with 문으로 관리되는가?
- [ ] 비밀 키가 코드에 없는가?
- [ ] SQL injection 방지하는가?

### 테스트
- [ ] 새 기능에 테스트가 있는가?
- [ ] 엣지 케이스가 다뤄지는가?
- [ ] 커버리지가 80% 이상인가?

### 성능
- [ ] 시간복잡도가 적절한가?
- [ ] 적절한 자료구조를 사용하는가?
- [ ] 불필요한 메모리 사용이 없는가?

### 유지보수
- [ ] 타입 힌트가 있는가?
- [ ] docstring 이 있는가?
- [ ] 의존성이 명시되어 있는가?
- [ ] 로깅이 있는가?

## 11. Zen of Python 적용

```python
import this
```

- **Beautiful is better than ugly** — 아름다움
- **Explicit is better than implicit** — 명시성
- **Simple is better than complex** — 단순함
- **Complex is better than complicated** — 복잡 < 난해
- **Flat is better than nested** — 평탄함
- **Sparse is better than dense** — 여백
- **Readability counts** — 가독성
- **Special cases aren't special enough to break the rules** — 일관성
- **Errors should never pass silently** — 명시적 에러
- **There should be one — and preferably only one — obvious way** — 단일 방법
- **Now is better than never** — 행동
- **If the implementation is hard to explain, it's a bad idea** — 설명 가능성

## 📝 연습 문제

### 문제 1: 리팩토링
다음 코드를 PEP 8 과 Pythonic 스타일로 리팩토링하세요.
```python
def func( data,flag ):
    res=[]
    for i in range(len(data)):
        if data[i]!=None:
            if flag==True:
                res.append(data[i]*2)
            else:
                res.append(data[i])
    return res
```

### 문제 2: 코드 리뷰
주변에 작성한 코드를 체크리스트에 따라 리뷰하세요.

### 문제 3: 타입 힌트 추가
타입 힌트가 없는 함수에 타입 힌트를 추가하세요.

### 문제 4: 도구 적용
프로젝트에 black, ruff, mypy 를 적용하세요.

### 문제 5: pre-commit
프로젝트에 pre-commit 훅을 설정하세요.

## ✅ 체크리스트
- [ ] PEP 8 을 따른다
- [ ] Pythonic 한 표현을 사용한다
- [ ] 함수와 클래스를 작고 명확하게 설계한다
- [ ] 예외를 적절히 처리한다
- [ ] 로깅을 사용한다
- [ ] 보안을 고려한다
- [ ] 자동화 도구를 사용한다

## 🔗 다음 챕터
👉 [06. 프로젝트 구조와 아키텍처](./06-project-structure.md)
