# 06. 테스팅 (pytest, TDD)

## 🎯 학습 목표
- 단위 테스트의 중요성을 이해한다
- pytest 의 핵심 기능을 활용한다
- TDD 워크플로우를 따른다
- 모킹과 테스트 더블을 사용한다
- 코드 커버리지를 측정한다

## 1. 왜 테스트?

- 🐛 **버그 조기 발견**: 변경이 다른 부분을 깨뜨리는지 확인
- 🔄 **안전한 리팩토링**: 테스트가 있으면 자신 있게 변경
- 📖 **살아있는 문서**: 코드 사용법을 보여주는 예시
- 🚀 **CI/CD**: 자동화된 품질 게이트

## 2. unittest (표준 라이브러리)

```python
# test_math.py
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def setUp(self):
        # 각 테스트 전 실행
        self.x = 10

    def tearDown(self):
        # 각 테스트 후 실행
        pass

    def test_add_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-1, -1), -2)

    def test_add_zero(self):
        self.assertEqual(add(0, 0), 0)

if __name__ == "__main__":
    unittest.main()
```

실행:
```bash
python -m unittest test_math.py
```

## 3. pytest (권장 ✅)

더 간단하고 강력한 테스트 프레임워크.

### 3.1 설치
```bash
pip install pytest
```

### 3.2 기본 사용
```python
# test_math.py
def add(a, b):
    return a + b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 0) == 0
```

실행:
```bash
pytest                    # 모든 테스트
pytest test_math.py       # 특정 파일
pytest -v                 # verbose
pytest -k "positive"      # 이름으로 필터
pytest -x                 # 첫 실패 시 중단
pytest --lf               # 마지막 실패한 것만
```

### 3.3 명명 규칙
- 파일: `test_*.py` 또는 `*_test.py`
- 함수: `test_*`
- 클래스: `Test*` (생성자 없어야 함)

## 4. assert 와 비교

pytest 는 일반 `assert` 를 사용하면서도 풍부한 정보 제공.

```python
def test_examples():
    # 동등성
    assert 1 + 1 == 2

    # 부등호
    assert 5 > 3

    # 포함
    assert "py" in "python"
    assert 1 in [1, 2, 3]

    # 부동소수
    assert 0.1 + 0.2 == pytest.approx(0.3)

    # 타입
    assert isinstance("hello", str)

    # 진리값
    assert []  # AssertionError (빈 리스트)
```

### 예외 테스트
```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없음")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="0으로"):
        divide(10, 0)

def test_divide_by_zero_capture():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "0으로" in str(exc_info.value)
```

## 5. Fixture — 테스트 준비

테스트에 필요한 데이터/리소스를 제공.

### 5.1 기본 fixture
```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Alice", "age": 25}

def test_user_name(sample_user):
    assert sample_user["name"] == "Alice"

def test_user_age(sample_user):
    assert sample_user["age"] == 25
```

### 5.2 setup/teardown
```python
@pytest.fixture
def temp_file(tmp_path):  # tmp_path 는 pytest 내장 fixture
    file = tmp_path / "test.txt"
    file.write_text("hello")
    yield file
    # teardown (자동 정리되지만 명시적으로 가능)
```

### 5.3 fixture 스코프
```python
@pytest.fixture(scope="function")  # 기본 (각 테스트마다)
def f1(): ...

@pytest.fixture(scope="class")     # 클래스마다
def f2(): ...

@pytest.fixture(scope="module")    # 모듈마다
def f3(): ...

@pytest.fixture(scope="session")   # 전체 세션
def f4(): ...

# 예: DB 연결은 session 스코프
@pytest.fixture(scope="session")
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

### 5.4 conftest.py — 공유 fixture
```python
# conftest.py (자동으로 로드됨)
import pytest

@pytest.fixture
def app():
    from myapp import create_app
    return create_app(testing=True)

@pytest.fixture
def client(app):
    return app.test_client()
```

이제 모든 테스트에서 `app`, `client` fixture 사용 가능.

### 5.5 내장 fixture
```python
def test_tmp(tmp_path):
    """임시 디렉토리"""
    (tmp_path / "file.txt").write_text("data")

def test_capsys(capsys):
    """stdout/stderr 캡처"""
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"

def test_monkeypatch(monkeypatch):
    """환경 패치"""
    monkeypatch.setenv("MY_VAR", "test")
    monkeypatch.setattr("os.getcwd", lambda: "/fake/path")
```

## 6. 파라미터화 (Parametrize)

같은 테스트를 여러 데이터로.

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, -50, 50),
])
def test_add(a, b, expected):
    assert add(a, b) == expected

# 다중 파라미터화
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_combinations(x, y):
    # 6번 실행 (3 x 2)
    assert x * y > 0

# id 지정
@pytest.mark.parametrize("input, expected", [
    pytest.param("", 0, id="empty"),
    pytest.param("a", 1, id="one_char"),
    pytest.param("hello", 5, id="word"),
])
def test_len(input, expected):
    assert len(input) == expected
```

## 7. 마커 (Markers)

```python
import pytest

@pytest.mark.slow
def test_heavy():
    # 느린 테스트
    pass

@pytest.mark.skip(reason="아직 미구현")
def test_future():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Windows 미지원")
def test_unix_only():
    pass

@pytest.mark.xfail(reason="알려진 버그")
def test_known_bug():
    assert False
```

실행:
```bash
pytest -m slow         # slow 마커만
pytest -m "not slow"   # slow 제외
```

## 8. 모킹 (Mocking)

### 8.1 unittest.mock
```python
from unittest.mock import Mock, MagicMock, patch

# Mock 객체
mock = Mock()
mock.method.return_value = 42
result = mock.method()
assert result == 42
mock.method.assert_called_once()
mock.method.assert_called_with()  # 인자도 확인
```

### 8.2 patch 데코레이터
```python
# code.py
import requests

def fetch_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()
```

```python
# test_code.py
from unittest.mock import patch

@patch("code.requests.get")
def test_fetch_user(mock_get):
    # 응답 모킹
    mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}

    result = fetch_user(1)

    assert result == {"id": 1, "name": "Alice"}
    mock_get.assert_called_with("https://api.example.com/users/1")
```

### 8.3 patch 컨텍스트 매니저
```python
def test_with_patch():
    with patch("code.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"id": 1}
        result = fetch_user(1)
        assert result["id"] == 1
```

### 8.4 사이드 이펙트
```python
@patch("code.requests.get")
def test_retry(mock_get):
    # 처음에는 실패, 두 번째에 성공
    mock_get.side_effect = [
        ConnectionError("fail"),
        Mock(json=lambda: {"id": 1}),
    ]

    result = fetch_with_retry(1)
    assert result["id"] == 1
    assert mock_get.call_count == 2
```

### 8.5 pytest-mock (편리)
```bash
pip install pytest-mock
```

```python
def test_fetch(mocker):
    mock_get = mocker.patch("code.requests.get")
    mock_get.return_value.json.return_value = {"id": 1}

    assert fetch_user(1) == {"id": 1}
```

## 9. 코드 커버리지

```bash
pip install pytest-cov

# 실행
pytest --cov=mymodule
pytest --cov=mymodule --cov-report=html  # HTML 리포트
pytest --cov=mymodule --cov-report=term-missing  # 빠진 라인 표시
```

### 설정 (pyproject.toml)
```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing --cov-fail-under=80"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
]
```

## 10. TDD (Test-Driven Development)

### Red - Green - Refactor 사이클

```
1. Red:     실패하는 테스트 작성
2. Green:   테스트 통과하는 최소한의 코드
3. Refactor: 코드 개선 (테스트는 계속 통과)
```

### 예시: 회문 판별

#### 1단계: Red — 실패하는 테스트
```python
# test_palindrome.py
from palindrome import is_palindrome

def test_simple_palindrome():
    assert is_palindrome("level") == True

# 실행 → ImportError (구현 없음)
```

#### 2단계: Green — 최소 구현
```python
# palindrome.py
def is_palindrome(s):
    return s == s[::-1]
```
테스트 실행 → 통과!

#### 3단계: 다음 테스트 추가
```python
def test_not_palindrome():
    assert is_palindrome("hello") == False

def test_case_insensitive():
    assert is_palindrome("Level") == True  # 실패!
```

#### 4단계: 구현 개선
```python
def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]
```

#### 5단계: 더 많은 케이스
```python
def test_with_spaces():
    assert is_palindrome("A man a plan") == True
```

#### 6단계: 구현
```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]
```

## 11. 좋은 테스트의 특성 (FIRST)

- **F**ast: 빠르게 실행
- **I**solated: 다른 테스트와 독립
- **R**epeatable: 같은 결과 반복
- **S**elf-validating: 자동 판별 (assert)
- **T**imely: 코드와 함께 작성

### AAA 패턴
```python
def test_user_creation():
    # Arrange (준비)
    name = "Alice"
    age = 25

    # Act (실행)
    user = User(name, age)

    # Assert (검증)
    assert user.name == name
    assert user.age == age
```

## 12. 테스트 구조

```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── models.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_models.py
│   │   └── test_utils.py
│   └── integration/
│       └── test_api.py
└── pyproject.toml
```

### 단위 vs 통합 vs E2E
| 종류 | 범위 | 속도 | 안정성 |
|------|------|------|--------|
| Unit | 단일 함수/클래스 | 빠름 | 높음 |
| Integration | 여러 컴포넌트 | 보통 | 보통 |
| E2E | 전체 시스템 | 느림 | 낮음 |

## 13. 실전 예제

### 예제 1: 계산기 TDD
```python
# test_calculator.py
import pytest
from calculator import Calculator

@pytest.fixture
def calc():
    return Calculator()

class TestCalculator:
    def test_add(self, calc):
        assert calc.add(2, 3) == 5

    def test_subtract(self, calc):
        assert calc.subtract(5, 3) == 2

    def test_divide(self, calc):
        assert calc.divide(10, 2) == 5

    def test_divide_by_zero(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)

    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 6),
        (-1, 5, -5),
        (0, 100, 0),
    ])
    def test_multiply(self, calc, a, b, expected):
        assert calc.multiply(a, b) == expected
```

### 예제 2: API 모킹
```python
# user_service.py
import requests

def get_user(user_id):
    r = requests.get(f"https://api.example.com/users/{user_id}")
    r.raise_for_status()
    return r.json()
```

```python
# test_user_service.py
from unittest.mock import patch, Mock

def test_get_user_success(mocker):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "Alice"}
    mock_response.raise_for_status = Mock()

    mocker.patch("user_service.requests.get", return_value=mock_response)

    result = get_user(1)
    assert result["name"] == "Alice"

def test_get_user_error(mocker):
    import requests
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    mocker.patch("user_service.requests.get", return_value=mock_response)

    with pytest.raises(requests.HTTPError):
        get_user(1)
```

### 예제 3: 파일 작업 테스트
```python
def test_save_user(tmp_path):
    file = tmp_path / "users.json"

    save_user(file, {"name": "Alice"})

    assert file.exists()
    import json
    data = json.loads(file.read_text())
    assert data["name"] == "Alice"
```

## 14. 추가 도구

| 도구 | 용도 |
|------|------|
| **pytest-cov** | 커버리지 |
| **pytest-mock** | 모킹 편의 |
| **pytest-xdist** | 병렬 실행 |
| **pytest-asyncio** | asyncio 테스트 |
| **pytest-django** | Django 통합 |
| **pytest-bdd** | BDD 스타일 |
| **hypothesis** | property-based testing |
| **faker** | 가짜 데이터 생성 |
| **freezegun** | 시간 조작 |

### hypothesis 예시
```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    assert add(a, b) == add(b, a)

@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    assert sorted(sorted(lst)) == sorted(lst)
```

## 📝 연습 문제

### 문제 1: 기본 테스트
사칙연산 함수 4개를 만들고 각각 테스트하세요.

### 문제 2: 예외 테스트
음수 입력 시 ValueError 를 던지는 factorial 함수를 만들고 예외를 테스트하세요.

### 문제 3: Parametrize
회문 판별 함수에 대해 5가지 케이스를 parametrize 로 테스트하세요.

### 문제 4: Fixture
임시 파일을 생성하는 fixture 를 만들고 파일 읽기 함수를 테스트하세요.

### 문제 5: 모킹
외부 API 를 호출하는 함수를 mock 으로 테스트하세요.

### 문제 6: TDD
완전히 처음부터 TDD 로 BankAccount 클래스를 구현하세요. (입금, 출금, 잔액)

## ✅ 체크리스트
- [ ] pytest 의 기본 사용법을 안다
- [ ] assert 와 예외 테스트를 한다
- [ ] fixture 를 정의하고 사용한다
- [ ] parametrize 로 여러 케이스를 테스트한다
- [ ] mock 으로 외부 의존성을 격리한다
- [ ] 커버리지를 측정한다
- [ ] TDD 사이클을 따른다

## 🔗 다음 챕터
👉 [07. 성능 최적화와 프로파일링](./07-performance.md)
