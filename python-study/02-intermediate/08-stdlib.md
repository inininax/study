# 08. 유용한 표준 라이브러리

## 🎯 학습 목표
- Python 표준 라이브러리의 핵심 모듈을 안다
- 실무에서 자주 쓰는 도구들을 익힌다

> 💡 Python은 "Batteries included" 철학으로 풍부한 표준 라이브러리를 제공합니다.

## 1. collections — 특수 컬렉션

### 1.1 Counter — 빈도 카운트
```python
from collections import Counter

# 기본
c = Counter("mississippi")
print(c)                # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
print(c.most_common(3)) # [('i', 4), ('s', 4), ('p', 2)]

# 리스트
votes = ["A", "B", "A", "C", "B", "A"]
print(Counter(votes))   # Counter({'A': 3, 'B': 2, 'C': 1})

# 연산
c1 = Counter("aab")     # {a: 2, b: 1}
c2 = Counter("abc")     # {a: 1, b: 1, c: 1}
print(c1 + c2)          # {a: 3, b: 2, c: 1}
print(c1 - c2)          # {a: 1}
print(c1 & c2)          # 교집합: {a: 1, b: 1}
print(c1 | c2)          # 합집합 (max): {a: 2, b: 1, c: 1}
```

### 1.2 defaultdict — 기본값 딕셔너리
```python
from collections import defaultdict

# 키가 없으면 자동 생성
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
print(dd["fruits"])     # ['apple', 'banana']
print(dd["nothing"])    # [] (자동 생성)

# 그룹핑
words = ["apple", "bat", "banana", "cherry", "ant"]
by_letter = defaultdict(list)
for word in words:
    by_letter[word[0]].append(word)
# {'a': ['apple', 'ant'], 'b': ['bat', 'banana'], 'c': ['cherry']}

# 다른 타입
dd_int = defaultdict(int)   # 기본 0
dd_int["count"] += 1        # KeyError 없음
```

### 1.3 deque — 양방향 큐
```python
from collections import deque

dq = deque([1, 2, 3])
dq.append(4)             # [1, 2, 3, 4]
dq.appendleft(0)         # [0, 1, 2, 3, 4]
dq.pop()                 # 4
dq.popleft()             # 0

# 최대 크기 (오래된 것부터 제거)
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
print(recent)            # deque([2, 3, 4], maxlen=3)

# 회전
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)             # [4, 5, 1, 2, 3]
dq.rotate(-1)            # [5, 1, 2, 3, 4]
```

### 1.4 namedtuple — 이름 있는 튜플
```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)          # 3 4
print(p[0], p[1])        # 인덱스도 가능

# dataclass 가 더 권장되지만 가볍게 쓸 때 좋음
Person = namedtuple("Person", "name age city")
alice = Person("Alice", 25, "Seoul")
print(alice.name)
print(alice._asdict())   # {'name': 'Alice', ...}
```

### 1.5 OrderedDict / ChainMap
```python
from collections import ChainMap

# 여러 딕셔너리를 하나처럼
defaults = {"color": "red", "size": "M"}
user_pref = {"color": "blue"}
config = ChainMap(user_pref, defaults)

print(config["color"])   # blue (앞쪽 우선)
print(config["size"])    # M (defaults 에서)
```

## 2. datetime — 날짜와 시간

```python
from datetime import datetime, date, time, timedelta, timezone

# 현재
now = datetime.now()
today = date.today()

# 생성
d = date(2026, 5, 12)
t = time(14, 30, 0)
dt = datetime(2026, 5, 12, 14, 30, 0)

# 포맷 (strftime)
print(dt.strftime("%Y-%m-%d %H:%M:%S"))    # 2026-05-12 14:30:00
print(dt.strftime("%Y년 %m월 %d일"))        # 2026년 05월 12일
print(dt.strftime("%A"))                    # Tuesday

# 파싱 (strptime)
d = datetime.strptime("2026-05-12", "%Y-%m-%d")

# ISO 형식
print(now.isoformat())                      # 2026-05-12T14:30:00.123456
parsed = datetime.fromisoformat("2026-05-12T14:30:00")

# 계산
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)
in_1h_30m = now + timedelta(hours=1, minutes=30)

# 차이
diff = tomorrow - now
print(diff.days)
print(diff.total_seconds())

# 타임존
utc_now = datetime.now(timezone.utc)
kst = timezone(timedelta(hours=9))
seoul_now = datetime.now(kst)
```

### strftime 형식 코드
| 코드 | 의미 | 예 |
|------|------|----|
| `%Y` | 연도 (4자리) | 2026 |
| `%m` | 월 (01-12) | 05 |
| `%d` | 일 (01-31) | 12 |
| `%H` | 시 (00-23) | 14 |
| `%M` | 분 (00-59) | 30 |
| `%S` | 초 (00-59) | 00 |
| `%A` | 요일 (전체) | Tuesday |
| `%a` | 요일 (축약) | Tue |
| `%B` | 월 (전체) | May |
| `%b` | 월 (축약) | May |

## 3. time — 시간 측정

```python
import time

# 현재 timestamp
print(time.time())              # 1715000000.123

# 잠시 대기
time.sleep(1.5)

# 실행 시간 측정
start = time.perf_counter()
sum(range(1_000_000))
elapsed = time.perf_counter() - start
print(f"{elapsed:.4f}초")

# struct_time
t = time.localtime()
print(t.tm_year, t.tm_mon, t.tm_mday)
```

## 4. random — 난수

```python
import random

# 기본
random.random()                 # 0.0 ~ 1.0
random.uniform(1.5, 10.5)       # 실수 범위
random.randint(1, 100)          # 정수 범위 (양 끝 포함)
random.randrange(0, 100, 2)     # 0, 2, 4, ..., 98

# 선택
random.choice(["a", "b", "c"])           # 1개
random.choices(["a", "b"], k=5)          # 중복 허용 5개
random.choices(["a", "b"], weights=[1, 9], k=10)  # 가중치
random.sample([1, 2, 3, 4, 5], 3)        # 중복 없이 3개

# 섞기
items = [1, 2, 3, 4, 5]
random.shuffle(items)
print(items)

# 시드 (재현 가능)
random.seed(42)

# 가우시안 분포
random.gauss(0, 1)              # 평균 0, 표준편차 1
```

## 5. math — 수학

```python
import math

# 상수
math.pi                         # 3.141592653589793
math.e                          # 2.718281828459045
math.inf                        # 무한대
math.nan                        # Not a Number

# 함수
math.sqrt(16)                   # 4.0
math.pow(2, 10)                 # 1024.0
math.log(100)                   # 자연로그
math.log(100, 10)               # 밑이 10인 로그
math.log2(8)                    # 3.0
math.log10(1000)                # 3.0

math.sin(math.pi / 2)           # 1.0
math.cos(0)                     # 1.0
math.tan(math.pi / 4)           # 0.9999...
math.radians(180)               # math.pi
math.degrees(math.pi)           # 180.0

math.floor(3.7)                 # 3
math.ceil(3.2)                  # 4
math.trunc(3.7)                 # 3 (소수부 버림)

math.gcd(12, 18)                # 6
math.lcm(4, 6)                  # 12 (Python 3.9+)
math.factorial(5)               # 120
math.comb(5, 2)                 # 10 (조합)
math.perm(5, 2)                 # 20 (순열)
```

## 6. statistics — 통계

```python
import statistics as stats

data = [10, 20, 30, 40, 50]

stats.mean(data)                # 30.0 (평균)
stats.median(data)              # 30 (중앙값)
stats.median_low(data)          # 30
stats.median_high(data)         # 30
stats.mode([1, 1, 2, 3])        # 1 (최빈값)
stats.stdev(data)               # 표준편차
stats.variance(data)            # 분산
stats.quantiles(data, n=4)      # 사분위수
```

## 7. itertools — 이터레이터 도구

```python
from itertools import (
    count, cycle, repeat,
    chain, combinations, permutations, product,
    accumulate, groupby, takewhile, dropwhile,
    islice, zip_longest, starmap, compress
)

# 무한
list(islice(count(10, 2), 5))           # [10, 12, 14, 16, 18]
list(islice(cycle("ABC"), 7))           # ['A','B','C','A','B','C','A']

# 결합
list(chain([1, 2], [3, 4]))             # [1, 2, 3, 4]

# 조합/순열
list(combinations([1, 2, 3], 2))        # [(1,2),(1,3),(2,3)]
list(permutations([1, 2, 3], 2))        # [(1,2),(1,3),(2,1),...]
list(product([1, 2], ["a", "b"]))       # [(1,'a'),(1,'b'),(2,'a'),(2,'b')]

# 누적
list(accumulate([1, 2, 3, 4]))          # [1, 3, 6, 10]
list(accumulate([1, 2, 3, 4], max))     # [1, 2, 3, 4]

# 그룹화 (먼저 정렬 필요)
data = sorted([("a", 1), ("a", 2), ("b", 3)])
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))
```

## 8. functools — 함수형 도구

```python
from functools import partial, reduce, lru_cache, wraps, cache, total_ordering

# partial - 부분 적용
def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
print(square(5))                # 25

# reduce - 누적
from functools import reduce
total = reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])

# lru_cache - 메모이제이션
@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

# cache (Python 3.9+) - 무제한 캐시
@cache
def slow_func(x):
    return x ** 2

# total_ordering - 비교 메서드 자동 생성
@total_ordering
class Item:
    def __init__(self, val):
        self.val = val
    def __eq__(self, other):
        return self.val == other.val
    def __lt__(self, other):
        return self.val < other.val
    # >, >=, <=, != 자동 생성

# wraps - 데코레이터 메타데이터 보존
def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper
```

## 9. os & sys — 시스템

```python
import os
import sys

# 환경 변수
os.environ["MY_VAR"] = "value"
os.environ.get("PATH")
os.getenv("HOME", "/tmp")       # 기본값 지원

# 경로
os.path.join("a", "b", "c")
os.path.abspath("file.txt")
os.path.dirname(__file__)

# 디렉토리
os.getcwd()
os.chdir("/tmp")
os.listdir(".")
os.makedirs("a/b/c", exist_ok=True)

# 시스템 명령 (subprocess 권장)
os.system("ls")                 # 결과 코드만
output = os.popen("ls").read()  # 출력 캡처

# sys
sys.argv                        # 명령줄 인자
sys.exit(0)                     # 종료
sys.path                        # 모듈 검색 경로
sys.platform                    # 'linux', 'darwin', 'win32'
sys.version_info                # Python 버전
sys.stdin, sys.stdout, sys.stderr
```

## 10. subprocess — 외부 프로세스

```python
import subprocess

# 간단한 실행
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.returncode)

# 에러 발생 시 예외
subprocess.run(["false"], check=True)   # CalledProcessError

# 셸 명령
subprocess.run("ls -la | grep py", shell=True, capture_output=True)

# 파이프
result = subprocess.run(
    ["grep", "python"],
    input="hello python world",
    text=True,
    capture_output=True,
)
print(result.stdout)
```

## 11. pathlib — 경로

```python
from pathlib import Path

p = Path("data/users.txt")

# 정보
p.name              # users.txt
p.stem              # users
p.suffix            # .txt
p.parent            # data
p.absolute()        # 절대 경로

# 검사
p.exists()
p.is_file()
p.is_dir()

# 작업
p.read_text(encoding="utf-8")
p.write_text("Hello!", encoding="utf-8")
p.read_bytes()
p.write_bytes(b"...")
p.unlink()
p.rename("new.txt")

# 디렉토리
Path("dir").mkdir(parents=True, exist_ok=True)
for f in Path(".").rglob("*.py"):
    print(f)
```

## 12. logging — 로깅

```python
import logging

# 기본 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

logger.debug("디버그 메시지")
logger.info("정보 메시지")
logger.warning("경고 메시지")
logger.error("에러 메시지")
logger.critical("치명적")

# 예외와 함께
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("나눗셈 오류")

# 파일에 기록
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)
```

### 로깅 레벨
| 레벨 | 값 | 용도 |
|------|-----|------|
| DEBUG | 10 | 상세 디버깅 |
| INFO | 20 | 일반 정보 |
| WARNING | 30 | 경고 (기본) |
| ERROR | 40 | 에러 |
| CRITICAL | 50 | 치명적 |

## 13. argparse — 명령줄 인자

```python
import argparse

parser = argparse.ArgumentParser(description="파일 처리 도구")

parser.add_argument("input", help="입력 파일")
parser.add_argument("-o", "--output", default="out.txt", help="출력 파일")
parser.add_argument("-v", "--verbose", action="store_true", help="자세히 출력")
parser.add_argument("-n", "--count", type=int, default=10, help="개수")
parser.add_argument("--mode", choices=["a", "b", "c"], default="a")

args = parser.parse_args()
print(args.input, args.output, args.verbose)
```

## 14. urllib & http — 네트워크

```python
from urllib.parse import urlparse, urlencode, urljoin, quote
from urllib.request import urlopen

# URL 파싱
url = urlparse("https://example.com/path?key=value")
print(url.scheme, url.netloc, url.path)

# 쿼리 인코딩
params = {"name": "Alice", "age": 25}
print(urlencode(params))        # name=Alice&age=25

# URL 결합
print(urljoin("https://example.com/a/", "b/c"))

# URL 안전 인코딩
print(quote("한글 텍스트"))

# HTTP 요청 (간단)
with urlopen("https://example.com") as resp:
    html = resp.read().decode()
```

> 💡 실무에서는 `requests` 라이브러리 사용을 권장합니다.

## 15. hashlib — 해시

```python
import hashlib

# SHA-256
h = hashlib.sha256()
h.update(b"hello")
h.update(b" world")
print(h.hexdigest())

# 한 번에
print(hashlib.md5(b"password").hexdigest())
print(hashlib.sha256("hello".encode()).hexdigest())

# 파일 해시
def file_hash(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
```

## 16. uuid — 고유 ID

```python
import uuid

# UUID4 (랜덤, 가장 많이 사용)
print(uuid.uuid4())             # 550e8400-e29b-41d4-a716-446655440000

# UUID1 (MAC + 타임스탬프)
print(uuid.uuid1())

# 문자열 비교
print(uuid.uuid4().hex)         # 하이픈 없는 형태
print(str(uuid.uuid4()))
```

## 17. enum — 열거형

```python
from enum import Enum, auto, IntEnum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# auto 사용
class Status(Enum):
    PENDING = auto()
    ACTIVE = auto()
    CLOSED = auto()

# 정수처럼 비교 가능
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

print(Color.RED)                # Color.RED
print(Color.RED.name)           # RED
print(Color.RED.value)          # 1

if Priority.HIGH > Priority.LOW:
    print("True")
```

## 18. typing — 타입 힌트

```python
from typing import List, Dict, Tuple, Set, Optional, Union, Any, Callable

def greet(name: str) -> str:
    return f"Hello, {name}!"

def get_items() -> List[int]:
    return [1, 2, 3]

def find_user(id: int) -> Optional[Dict[str, Any]]:
    return None

def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

# Python 3.9+ 부터는 내장 타입 사용 가능
def get_items() -> list[int]:
    return [1, 2, 3]

def get_user() -> dict[str, str | int]:
    return {"name": "Alice", "age": 25}
```

## 19. 실전 예제

### 예제 1: 빈도 분석
```python
from collections import Counter
import re

def top_words(text, n=10):
    words = re.findall(r"\w+", text.lower())
    return Counter(words).most_common(n)
```

### 예제 2: 로그 분석기
```python
from collections import defaultdict, Counter
from datetime import datetime
import re

LOG_RE = re.compile(r"(\d{4}-\d{2}-\d{2}) \[(\w+)\] (.+)")

def analyze_log(path):
    by_level = Counter()
    by_date = defaultdict(int)

    with open(path, encoding="utf-8") as f:
        for line in f:
            if m := LOG_RE.match(line):
                date, level, msg = m.groups()
                by_level[level] += 1
                by_date[date] += 1

    return dict(by_level), dict(by_date)
```

### 예제 3: 캐시 데코레이터
```python
import functools
from datetime import datetime, timedelta

def timed_cache(seconds=60):
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args):
            now = datetime.now()
            if args in cache:
                value, expires = cache[args]
                if now < expires:
                    return value

            value = func(*args)
            cache[args] = (value, now + timedelta(seconds=seconds))
            return value

        return wrapper
    return decorator

@timed_cache(seconds=60)
def expensive_query(user_id):
    print(f"실제 쿼리: {user_id}")
    return {"id": user_id, "name": "..."}
```

## 📝 연습 문제

### 문제 1: 가장 흔한 단어 5개
파일에서 가장 자주 등장하는 단어 5개를 출력하세요. (Counter 사용)

### 문제 2: 디렉토리 통계
디렉토리 안 파일들을 확장자별로 그룹화해서 개수를 출력하세요.

### 문제 3: 명령줄 도구
argparse 를 사용해 파일 경로와 키워드를 받아 grep 처럼 동작하는 도구를 만드세요.

### 문제 4: 파일 해시
디렉토리 내 모든 파일의 SHA-256 해시를 계산해 JSON 으로 저장하세요.

### 문제 5: 만년 달력
calendar 모듈을 활용해 특정 년/월의 달력을 출력하세요.

## ✅ 체크리스트
- [ ] collections 의 주요 클래스를 안다
- [ ] datetime 으로 날짜 계산을 한다
- [ ] itertools 와 functools 를 활용한다
- [ ] pathlib 으로 경로를 다룬다
- [ ] logging 으로 로그를 남긴다
- [ ] argparse 로 CLI 를 만든다

## 🎉 중급 완료!

축하합니다! Python 중급 과정을 모두 마쳤습니다.
이제 [고급 단계](../03-advanced/)로 진행할 준비가 되었습니다.

## 🔗 다음 단계
👉 [고급 시작 - 01. 데코레이터 심화](../03-advanced/01-decorators.md)
