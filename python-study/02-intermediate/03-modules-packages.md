# 03. 모듈과 패키지

## 🎯 학습 목표
- 모듈과 패키지의 차이를 안다
- 모듈을 임포트하고 사용한다
- 패키지를 만들고 배포할 수 있다
- 가상 환경과 pip 를 다룬다

## 1. 모듈 (Module)

**모듈**은 Python 코드를 담은 `.py` 파일입니다.

### 1.1 모듈 만들기
```python
# mymath.py
PI = 3.14159

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class Calculator:
    def __init__(self):
        self.result = 0
```

### 1.2 모듈 사용하기
```python
# main.py
import mymath

print(mymath.PI)              # 3.14159
print(mymath.add(2, 3))       # 5
calc = mymath.Calculator()
```

## 2. import 의 다양한 방법

```python
# 1. 모듈 전체 임포트
import math
math.sqrt(16)

# 2. 별명(alias) 사용
import numpy as np
np.array([1, 2, 3])

# 3. 특정 항목만 임포트
from math import sqrt, pi
sqrt(16)
print(pi)

# 4. 별명과 함께
from math import sqrt as square_root
square_root(16)

# 5. 모든 것 임포트 (비권장 ❌)
from math import *  # 네임스페이스 오염!
```

### 2.1 자주 쓰는 별명 관례
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
```

## 3. 모듈 검색 경로

Python이 모듈을 찾는 순서:
1. 내장 모듈
2. `sys.path` 의 디렉토리들 (현재 디렉토리 포함)

```python
import sys
print(sys.path)

# 경로 추가
sys.path.append("/my/custom/path")
```

### 3.1 PYTHONPATH 환경 변수
```bash
export PYTHONPATH="/path/to/modules:$PYTHONPATH"
```

## 4. __name__ 과 __main__

```python
# mymodule.py
def hello():
    print("Hello!")

# 모듈로 임포트되면 __name__ == 'mymodule'
# 직접 실행하면 __name__ == '__main__'

if __name__ == "__main__":
    # 직접 실행 시에만 동작
    print("이 파일이 직접 실행되었습니다")
    hello()
```

```bash
# 직접 실행
python3 mymodule.py    # "이 파일이..." 출력

# 임포트 시 출력 없음
python3 -c "import mymodule"  # 아무것도 출력 안 됨
```

## 5. 패키지 (Package)

**패키지**는 모듈들을 담은 디렉토리입니다.

### 5.1 패키지 구조
```
mypackage/
├── __init__.py          # 패키지임을 표시
├── module1.py
├── module2.py
└── subpackage/
    ├── __init__.py
    └── module3.py
```

### 5.2 __init__.py
```python
# mypackage/__init__.py
print("패키지가 로드됨")

# 패키지 레벨에서 항목 노출
from .module1 import important_function
from .module2 import MyClass

__version__ = "1.0.0"
__all__ = ["important_function", "MyClass"]
```

### 5.3 패키지 사용
```python
# 전체 임포트
import mypackage
mypackage.important_function()

# 모듈 임포트
from mypackage import module1
module1.some_function()

# 깊은 임포트
from mypackage.subpackage.module3 import deep_function

# 상대 임포트 (패키지 내부에서)
# mypackage/module1.py 안에서:
from . import module2          # 같은 패키지
from .subpackage import module3 # 하위 패키지
from .. import other_module     # 상위 패키지
```

## 6. 표준 라이브러리 핵심

### 6.1 os — 운영체제 인터페이스
```python
import os

print(os.getcwd())               # 현재 디렉토리
os.chdir("/tmp")                 # 디렉토리 변경
print(os.listdir("."))           # 파일 목록
os.makedirs("a/b/c", exist_ok=True)
os.remove("file.txt")
os.rename("old.txt", "new.txt")

# 환경 변수
print(os.environ.get("HOME"))
print(os.environ.get("MY_VAR", "default"))

# 경로 (pathlib 권장)
print(os.path.join("a", "b", "c.txt"))  # a/b/c.txt
print(os.path.exists("file.txt"))
print(os.path.isfile("file.txt"))
print(os.path.basename("/a/b/c.txt"))   # c.txt
print(os.path.dirname("/a/b/c.txt"))    # /a/b
```

### 6.2 sys — 시스템
```python
import sys

print(sys.version)         # Python 버전
print(sys.platform)        # 운영체제
print(sys.argv)            # 명령줄 인자
sys.exit(0)                # 종료
```

### 6.3 datetime — 날짜와 시간
```python
from datetime import datetime, date, timedelta

# 현재 시간
now = datetime.now()
print(now)                                  # 2026-05-12 10:30:45.123456
print(now.year, now.month, now.day)
print(now.hour, now.minute, now.second)

# 포맷팅
print(now.strftime("%Y-%m-%d %H:%M:%S"))    # 2026-05-12 10:30:45
print(now.strftime("%A, %B %d"))            # Tuesday, May 12

# 파싱
d = datetime.strptime("2026-05-12", "%Y-%m-%d")

# 날짜 계산
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)

# 차이
delta = tomorrow - now
print(delta.days)
print(delta.total_seconds())

# 날짜만
today = date.today()
birthday = date(2000, 1, 1)
age_days = (today - birthday).days
```

### 6.4 collections — 특수 컬렉션
```python
from collections import Counter, defaultdict, deque, namedtuple, OrderedDict

# Counter - 빈도 계산
c = Counter("hello world")
print(c)                       # Counter({'l': 3, 'o': 2, ...})
print(c.most_common(3))        # [('l', 3), ('o', 2), ('h', 1)]

# defaultdict - 기본값 딕셔너리
dd = defaultdict(list)
dd["fruits"].append("apple")   # 키 없어도 에러 X
dd["fruits"].append("banana")

# deque - 양방향 큐 (빠른 양쪽 추가/제거)
dq = deque([1, 2, 3])
dq.appendleft(0)               # [0, 1, 2, 3]
dq.append(4)                   # [0, 1, 2, 3, 4]
dq.popleft()                   # 0 반환

# namedtuple - 이름 있는 튜플
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)                # 3 4

# OrderedDict - 순서 유지 (Python 3.7+ 에선 일반 dict 도 순서 유지)
```

### 6.5 random — 난수
```python
import random

print(random.random())            # 0.0 ~ 1.0
print(random.randint(1, 10))      # 1 ~ 10 정수
print(random.uniform(1.0, 10.0))  # 1.0 ~ 10.0 실수

# 선택
colors = ["red", "green", "blue"]
print(random.choice(colors))      # 1개 선택
print(random.choices(colors, k=3))     # 중복 허용 3개
print(random.sample(colors, 2))   # 중복 없이 2개

# 섞기
deck = list(range(1, 11))
random.shuffle(deck)
print(deck)

# 시드 (재현 가능)
random.seed(42)
print(random.random())  # 항상 같은 값
```

### 6.6 json — JSON 처리
```python
import json

# Python → JSON
data = {"name": "Alice", "age": 25, "active": True}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# JSON → Python
parsed = json.loads(json_str)
print(parsed["name"])

# 파일로
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 6.7 math — 수학 함수
```python
import math

print(math.pi)              # 3.141592653589793
print(math.e)               # 2.718281828459045
print(math.sqrt(16))        # 4.0
print(math.pow(2, 10))      # 1024.0
print(math.log(100, 10))    # 2.0
print(math.sin(math.pi/2))  # 1.0
print(math.floor(3.7))      # 3
print(math.ceil(3.2))       # 4
print(math.gcd(12, 18))     # 6
print(math.factorial(5))    # 120
```

## 7. 외부 패키지 설치 (pip)

### 7.1 기본 명령
```bash
# 설치
pip install requests
pip install numpy pandas matplotlib

# 특정 버전
pip install django==4.2.0
pip install "django>=4.0,<5.0"

# 업그레이드
pip install --upgrade requests

# 제거
pip uninstall requests

# 설치된 패키지 목록
pip list
pip freeze              # requirements.txt 형식

# 패키지 정보
pip show requests
```

### 7.2 requirements.txt
```text
# requirements.txt
requests==2.31.0
numpy>=1.24.0
pandas
django>=4.0,<5.0
```

```bash
# 일괄 설치
pip install -r requirements.txt

# 현재 패키지 저장
pip freeze > requirements.txt
```

## 8. 가상 환경 (venv)

프로젝트별로 독립된 Python 환경을 만듭니다.

```bash
# 생성
python3 -m venv myenv

# 활성화 (macOS/Linux)
source myenv/bin/activate

# 활성화 (Windows)
myenv\Scripts\activate

# 비활성화
deactivate

# 삭제
rm -rf myenv
```

### 다른 가상 환경 도구
- **virtualenv**: venv 의 이전 버전
- **pipenv**: pip + venv 통합
- **poetry**: 의존성/패키징 관리 (권장)
- **conda**: 데이터 과학용
- **uv**: 빠른 최신 도구 (2024+ 인기)

## 9. 패키지 만들기 (배포)

### 9.1 프로젝트 구조 (현대적)
```
mypackage/
├── pyproject.toml          # 메타데이터 + 빌드 설정
├── README.md
├── LICENSE
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
└── tests/
    └── test_module.py
```

### 9.2 pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
description = "My awesome package"
authors = [{name = "Your Name", email = "you@example.com"}]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
dependencies = [
    "requests>=2.28",
    "click>=8.0",
]

[project.optional-dependencies]
dev = ["pytest", "black", "mypy"]

[project.scripts]
mycommand = "mypackage.cli:main"
```

### 9.3 빌드 & 배포
```bash
# 빌드 도구 설치
pip install build twine

# 빌드
python -m build
# → dist/mypackage-0.1.0.tar.gz, dist/mypackage-0.1.0-py3-none-any.whl

# PyPI 업로드 (실제 배포)
python -m twine upload dist/*

# TestPyPI 업로드 (테스트)
python -m twine upload --repository testpypi dist/*

# 로컬 설치 (개발 중)
pip install -e .
```

## 10. 실전 예제

### 예제: 유틸리티 패키지 만들기
```
myutils/
├── __init__.py
├── string_utils.py
├── number_utils.py
└── file_utils.py
```

```python
# myutils/__init__.py
from .string_utils import reverse_string, is_palindrome
from .number_utils import is_prime, gcd
from .file_utils import read_lines, write_lines

__version__ = "0.1.0"
__all__ = [
    "reverse_string", "is_palindrome",
    "is_prime", "gcd",
    "read_lines", "write_lines",
]
```

```python
# myutils/string_utils.py
def reverse_string(s):
    return s[::-1]

def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]
```

```python
# main.py
from myutils import reverse_string, is_prime

print(reverse_string("Hello"))  # olleH
print(is_prime(7))              # True
```

## 📝 연습 문제

### 문제 1: 모듈 만들기
사칙연산을 하는 `calculator.py` 모듈을 만들고 다른 파일에서 사용하세요.

### 문제 2: 패키지 만들기
`shapes` 패키지를 만들고 `circle.py`, `rectangle.py` 를 포함시키세요.

### 문제 3: 가상 환경
가상 환경을 만들어 `requests` 와 `beautifulsoup4` 를 설치하세요. requirements.txt 를 생성하세요.

### 문제 4: 날짜 계산기
datetime 을 사용해 두 날짜 사이의 일수를 계산하는 프로그램을 작성하세요.

### 문제 5: 단어 빈도
Counter 를 사용해 텍스트 파일의 단어 빈도 top 10을 출력하세요.

## ✅ 체크리스트
- [ ] import 의 다양한 방법을 안다
- [ ] `if __name__ == "__main__":` 패턴을 이해한다
- [ ] 패키지 구조를 만들 수 있다
- [ ] pip 으로 패키지를 설치한다
- [ ] 가상 환경을 사용한다
- [ ] 표준 라이브러리 핵심 모듈을 안다

## 🔗 다음 챕터
👉 [04. 예외 처리](./04-exceptions.md)
