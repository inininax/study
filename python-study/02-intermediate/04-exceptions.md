# 04. 예외 처리 (Exception Handling)

## 🎯 학습 목표
- 예외의 개념과 예외 처리의 필요성을 이해한다
- try/except/else/finally 를 활용한다
- 사용자 정의 예외를 만들 수 있다
- 적절한 예외 처리 패턴을 안다

## 1. 예외(Exception)란?

프로그램 실행 중 발생하는 **비정상적인 상황**입니다.

```python
# 예외 발생 예
print(10 / 0)        # ZeroDivisionError
print(int("abc"))    # ValueError
print(list[10])      # TypeError
my_list = [1, 2, 3]
print(my_list[10])   # IndexError
```

### Python 내장 예외 계층
```
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 └── Exception          ← 일반 예외 (이걸 잡으세요)
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── ValueError
      ├── TypeError
      ├── FileNotFoundError
      ├── PermissionError
      └── ...
```

## 2. try-except 기본

### 2.1 기본 구조
```python
try:
    # 예외가 발생할 수 있는 코드
    result = 10 / 0
except ZeroDivisionError:
    # 예외가 발생하면 실행
    print("0으로 나눌 수 없습니다")
```

### 2.2 예외 객체 받기
```python
try:
    int("abc")
except ValueError as e:
    print(f"에러: {e}")
    print(f"타입: {type(e).__name__}")
```

### 2.3 여러 예외 처리
```python
try:
    value = int(input("숫자: "))
    result = 100 / value
except ValueError:
    print("숫자가 아닙니다")
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다")
except (TypeError, NameError) as e:  # 여러 개 묶기
    print(f"다른 에러: {e}")
```

### 2.4 모든 예외 잡기 (주의!)
```python
try:
    risky_operation()
except Exception as e:        # ✅ 권장
    print(f"오류: {e}")

# ❌ 비권장: 너무 광범위
try:
    risky_operation()
except:                       # bare except - 모든 것 잡음 (KeyboardInterrupt 포함)
    pass
```

## 3. else 와 finally

### 3.1 else — 예외가 없을 때만
```python
try:
    f = open("data.txt")
except FileNotFoundError:
    print("파일 없음")
else:
    print("파일 열기 성공")
    content = f.read()
    f.close()
```

### 3.2 finally — 항상 실행
```python
try:
    f = open("data.txt")
    content = f.read()
except FileNotFoundError:
    print("파일 없음")
finally:
    print("정리 작업")
    f.close()  # 예외 여부와 상관없이 실행
```

### 3.3 전체 구조
```python
try:
    # 시도할 코드
    pass
except SomeException as e:
    # 예외 처리
    pass
except AnotherException:
    pass
else:
    # 예외 없을 때
    pass
finally:
    # 항상 실행 (정리)
    pass
```

## 4. raise — 예외 발생시키기

### 4.1 명시적 예외 발생
```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다")
    return a / b

try:
    divide(10, 0)
except ZeroDivisionError as e:
    print(e)
```

### 4.2 입력 검증
```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("나이는 정수여야 합니다")
    if age < 0:
        raise ValueError("나이는 음수일 수 없습니다")
    if age > 150:
        raise ValueError("나이가 너무 큽니다")
    return age

# 사용
try:
    set_age(-5)
except ValueError as e:
    print(f"잘못된 값: {e}")
```

### 4.3 예외 재발생
```python
def process_data(data):
    try:
        result = parse(data)
    except ValueError as e:
        print(f"파싱 실패: {e}")
        raise  # 같은 예외 다시 발생

# 변환해서 재발생 (예외 체이닝)
def fetch_user(user_id):
    try:
        return db.query(user_id)
    except DatabaseError as e:
        raise RuntimeError("사용자 조회 실패") from e
```

## 5. 사용자 정의 예외

```python
class AppError(Exception):
    """애플리케이션 기본 예외"""
    pass

class ValidationError(AppError):
    """검증 실패"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    """리소스 없음"""
    pass

# 사용
def create_user(name, age):
    if not name:
        raise ValidationError("name", "이름이 필요합니다")
    if age < 0:
        raise ValidationError("age", "나이는 음수일 수 없습니다")

try:
    create_user("", -5)
except ValidationError as e:
    print(f"검증 실패 - 필드: {e.field}, 메시지: {e.message}")
except AppError as e:
    print(f"앱 에러: {e}")
```

## 6. 자주 발생하는 예외들

| 예외 | 원인 |
|------|------|
| `ValueError` | 잘못된 값 (예: `int("abc")`) |
| `TypeError` | 잘못된 타입 (예: `"a" + 1`) |
| `IndexError` | 리스트 인덱스 범위 초과 |
| `KeyError` | 딕셔너리 키 없음 |
| `AttributeError` | 속성 없음 |
| `FileNotFoundError` | 파일 없음 |
| `PermissionError` | 권한 없음 |
| `ZeroDivisionError` | 0으로 나눔 |
| `ImportError` / `ModuleNotFoundError` | 모듈 임포트 실패 |
| `NameError` | 정의되지 않은 이름 |
| `RecursionError` | 재귀 깊이 초과 |
| `StopIteration` | 이터레이터 종료 |
| `KeyboardInterrupt` | Ctrl+C |

## 7. EAFP vs LBYL

Python은 **EAFP** (Easier to Ask Forgiveness than Permission) 스타일을 선호합니다.

```python
# LBYL (Look Before You Leap) - 다른 언어 스타일
if key in my_dict:
    value = my_dict[key]
else:
    value = None

# EAFP (Python 스타일) ✅
try:
    value = my_dict[key]
except KeyError:
    value = None

# 또는
value = my_dict.get(key)  # 더 Pythonic
```

### 동시성 안전성
```python
import os

# ❌ LBYL: 두 작업 사이에 파일이 사라질 수 있음
if os.path.exists("file.txt"):
    with open("file.txt") as f:
        content = f.read()

# ✅ EAFP: 원자적
try:
    with open("file.txt") as f:
        content = f.read()
except FileNotFoundError:
    content = None
```

## 8. 컨텍스트 매니저로 자원 관리

### 8.1 with 문
```python
# 파일 - 자동으로 닫힘
with open("file.txt") as f:
    content = f.read()
# 여기서 f.close() 자동 호출됨

# 여러 컨텍스트
with open("in.txt") as fin, open("out.txt", "w") as fout:
    fout.write(fin.read().upper())
```

### 8.2 직접 만들기
```python
class DatabaseConnection:
    def __enter__(self):
        print("연결 시작")
        self.conn = "DB_CONN"
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("연결 종료")
        # exc_type: 예외 타입, exc_val: 예외 값, exc_tb: 트레이스백
        # True 반환 시 예외 억제

with DatabaseConnection() as db:
    print(f"DB 사용: {db}")
# 연결 시작
# DB 사용: DB_CONN
# 연결 종료
```

### 8.3 contextlib 활용
```python
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    try:
        yield
    finally:
        print(f"실행 시간: {time.time() - start:.4f}초")

with timer():
    sum(range(1000000))
```

## 9. 로깅과 예외

```python
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

logger = logging.getLogger(__name__)

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logger.error("0으로 나누기 시도", exc_info=True)
        # exc_info=True 로 트레이스백 포함
        raise
    except Exception:
        logger.exception("예상치 못한 에러")  # 자동으로 exc_info=True
        raise

try:
    divide(10, 0)
except ZeroDivisionError:
    pass
```

## 10. 좋은 예외 처리 패턴

### 10.1 구체적인 예외 잡기
```python
# ❌ 너무 광범위
try:
    process()
except Exception:
    pass

# ✅ 구체적
try:
    process()
except (FileNotFoundError, PermissionError) as e:
    logger.error(f"파일 에러: {e}")
```

### 10.2 침묵하지 마세요
```python
# ❌ 에러를 숨김
try:
    risky()
except:
    pass

# ✅ 최소한 로깅
try:
    risky()
except Exception as e:
    logger.warning(f"실패: {e}")
```

### 10.3 try 블록은 좁게
```python
# ❌ 너무 넓음
try:
    data = load_data()
    processed = process(data)
    save(processed)
    notify_user()
    update_stats()
except Exception:
    pass

# ✅ 예외가 발생할 수 있는 곳만
try:
    data = load_data()
except FileNotFoundError:
    logger.error("데이터 파일 없음")
    return

processed = process(data)
# ...
```

### 10.4 finally 에서 raise 하지 마세요
```python
# ❌ finally 에서 발생한 예외가 원래 예외를 덮어씀
try:
    raise ValueError("원래 예외")
finally:
    raise RuntimeError("덮어쓰기")  # 원래 예외 잃음

# ✅ 정리만 하기
try:
    something()
finally:
    cleanup()  # 예외 발생시키지 않음
```

## 11. assert 문

디버깅용 검증. **프로덕션에서는 -O 옵션으로 비활성화됨!**

```python
def get_age(birth_year):
    age = 2026 - birth_year
    assert age >= 0, f"잘못된 나이: {age}"
    return age

get_age(2000)   # 26
get_age(2030)   # AssertionError: 잘못된 나이: -4
```

⚠️ **검증에는 assert 사용 X! raise 사용:**
```python
# ❌ 외부 입력 검증에 assert
def divide(a, b):
    assert b != 0  # python -O 로 실행하면 사라짐!
    return a / b

# ✅ raise 사용
def divide(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없음")
    return a / b
```

## 12. 실전 예제

### 예제 1: 안전한 입력
```python
def get_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"{min_val} 이상이어야 합니다")
                continue
            if max_val is not None and value > max_val:
                print(f"{max_val} 이하여야 합니다")
                continue
            return value
        except ValueError:
            print("정수를 입력하세요")

age = get_int("나이: ", min_val=0, max_val=150)
```

### 예제 2: 재시도 로직
```python
import time

def retry(func, max_attempts=3, delay=1):
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as e:
            print(f"시도 {attempt} 실패: {e}")
            if attempt < max_attempts:
                time.sleep(delay)
            else:
                raise

def unreliable_api():
    import random
    if random.random() < 0.7:
        raise ConnectionError("네트워크 에러")
    return "성공!"

try:
    result = retry(unreliable_api)
    print(result)
except ConnectionError:
    print("최종 실패")
```

### 예제 3: 사용자 입력 검증
```python
class User:
    def __init__(self, name, email, age):
        self.name = self._validate_name(name)
        self.email = self._validate_email(email)
        self.age = self._validate_age(age)

    @staticmethod
    def _validate_name(name):
        if not isinstance(name, str):
            raise TypeError("이름은 문자열이어야 합니다")
        if not name.strip():
            raise ValueError("이름이 비어있습니다")
        return name.strip()

    @staticmethod
    def _validate_email(email):
        if "@" not in email or "." not in email:
            raise ValueError(f"잘못된 이메일: {email}")
        return email.lower()

    @staticmethod
    def _validate_age(age):
        if not isinstance(age, int):
            raise TypeError("나이는 정수여야 합니다")
        if not 0 <= age <= 150:
            raise ValueError(f"잘못된 나이: {age}")
        return age

try:
    u = User("Alice", "alice@example.com", 25)
    print(u.name)
except (TypeError, ValueError) as e:
    print(f"사용자 생성 실패: {e}")
```

## 📝 연습 문제

### 문제 1: 안전한 나눗셈
두 숫자를 입력받아 나눗셈하되, 0으로 나누거나 잘못된 입력에 대해 적절히 처리하세요.

### 문제 2: 파일 안전 읽기
파일을 읽되, 파일이 없으면 "파일 없음", 권한이 없으면 "권한 없음"을 출력하세요.

### 문제 3: 사용자 정의 예외
`InsufficientFundsError` 를 만들고 BankAccount 클래스의 출금 시 사용하세요.

### 문제 4: 재시도 데코레이터
함수가 실패하면 최대 3번까지 재시도하는 데코레이터를 작성하세요.

### 문제 5: 검증 함수
이메일, 비밀번호, 전화번호 형식을 검증하는 함수들을 작성하세요.

## ✅ 체크리스트
- [ ] try/except 의 기본 구조를 안다
- [ ] 여러 예외를 적절히 처리한다
- [ ] finally 의 용도를 안다
- [ ] raise 로 예외를 발생시킨다
- [ ] 사용자 정의 예외를 만들 수 있다
- [ ] EAFP 스타일을 이해한다
- [ ] with 문으로 자원을 관리한다

## 🔗 다음 챕터
👉 [05. 파일 I/O와 컨텍스트 매니저](./05-file-io.md)
