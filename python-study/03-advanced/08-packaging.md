# 08. 패키징과 배포

## 🎯 학습 목표
- 현대적인 Python 프로젝트 구조를 안다
- pyproject.toml 을 작성한다
- PyPI 에 패키지를 배포한다
- 종합적인 도구 체인을 익힌다

## 1. 프로젝트 구조

### 권장 구조 (src layout)
```
my-package/
├── pyproject.toml          # 프로젝트 메타데이터
├── README.md
├── LICENSE
├── .gitignore
├── .python-version
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── __main__.py     # python -m mypackage 진입점
│       ├── cli.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_core.py
│   └── test_cli.py
└── docs/
    └── index.md
```

### src layout 의 장점
- 설치된 패키지로만 import (실수 방지)
- 테스트가 실제 설치된 코드를 사용
- 명확한 분리

## 2. pyproject.toml — 핵심 메타데이터

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
description = "패키지 설명"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
keywords = ["awesome", "tool", "cli"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "requests>=2.28",
    "click>=8.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "black",
    "ruff",
    "mypy",
]
docs = [
    "sphinx",
    "sphinx-rtd-theme",
]

[project.urls]
Homepage = "https://github.com/you/mypackage"
Documentation = "https://mypackage.readthedocs.io"
Repository = "https://github.com/you/mypackage"
Issues = "https://github.com/you/mypackage/issues"
Changelog = "https://github.com/you/mypackage/blob/main/CHANGELOG.md"

[project.scripts]
mycli = "mypackage.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
mypackage = ["py.typed", "data/*.json"]
```

## 3. 빌드 백엔드 선택

### 3.1 setuptools (가장 일반적)
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

### 3.2 hatchling (현대적)
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 3.3 poetry-core
```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### 3.4 flit (간단한 패키지)
```toml
[build-system]
requires = ["flit_core>=3.4"]
build-backend = "flit_core.buildapi"
```

## 4. 빌드 도구 비교

| 도구 | 설치 | 의존성 | 빌드 | 배포 | 특징 |
|------|------|--------|------|------|------|
| **pip + venv** | ✅ | ✅ | ❌ | ❌ | 기본 |
| **build + twine** | - | - | ✅ | ✅ | 표준 빌드/배포 |
| **poetry** | ✅ | ✅ | ✅ | ✅ | 올인원 |
| **uv** | ✅ | ✅ | ✅ | ❌ | 매우 빠름 (Rust 기반) |
| **pipenv** | ✅ | ✅ | ❌ | ❌ | Pipfile 사용 |
| **pdm** | ✅ | ✅ | ✅ | ✅ | PEP 표준 준수 |

## 5. 빌드와 배포 (표준 방식)

### 5.1 빌드 도구 설치
```bash
pip install build twine
```

### 5.2 빌드
```bash
python -m build

# 결과:
# dist/
#   mypackage-0.1.0-py3-none-any.whl    # 휠 (배포용)
#   mypackage-0.1.0.tar.gz              # 소스 배포본
```

### 5.3 로컬 설치 테스트
```bash
# 새 가상 환경에서
pip install dist/mypackage-0.1.0-py3-none-any.whl

# 또는 개발 모드 (코드 변경 즉시 반영)
pip install -e .
pip install -e ".[dev]"  # 개발 의존성 포함
```

### 5.4 TestPyPI 에 업로드 (테스트)
```bash
# TestPyPI 계정 만들기: https://test.pypi.org/

twine upload --repository testpypi dist/*

# 설치 테스트
pip install --index-url https://test.pypi.org/simple/ mypackage
```

### 5.5 PyPI 에 배포
```bash
# PyPI 계정: https://pypi.org/
# API 토큰 발급 권장

twine upload dist/*
```

### 5.6 ~/.pypirc (인증 저장)
```ini
[pypi]
username = __token__
password = pypi-...

[testpypi]
username = __token__
password = pypi-...
```

## 6. Poetry 사용

### 6.1 설치
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 6.2 프로젝트 생성
```bash
poetry new mypackage
cd mypackage

# 또는 기존 디렉토리에
poetry init
```

### 6.3 의존성 관리
```bash
poetry add requests
poetry add pytest --group dev
poetry remove requests
poetry update
```

### 6.4 가상 환경
```bash
poetry shell           # 가상 환경 진입
poetry run pytest      # 가상 환경에서 명령 실행
poetry install         # pyproject.toml 기반 설치
```

### 6.5 빌드/배포
```bash
poetry build
poetry publish
poetry publish --repository testpypi
```

## 7. uv — 최신 빠른 도구 (2024+)

Rust 로 작성된 매우 빠른 도구.

### 설치
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 또는 pip
pip install uv
```

### 사용
```bash
# 가상 환경 + 의존성 (매우 빠름!)
uv venv
source .venv/bin/activate
uv pip install requests pytest

# 또는 pip-tools 호환
uv pip compile pyproject.toml -o requirements.txt
uv pip sync requirements.txt

# 프로젝트 (2024+)
uv init
uv add requests
uv run python script.py
uv build
```

## 8. 버전 관리

### 8.1 시멘틱 버저닝 (SemVer)
```
MAJOR.MINOR.PATCH
1.2.3
```
- **MAJOR**: 호환되지 않는 API 변경
- **MINOR**: 하위 호환 기능 추가
- **PATCH**: 하위 호환 버그 수정

### 8.2 버전 자동 관리
```toml
# pyproject.toml
[project]
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "mypackage.__version__"}
```

```python
# src/mypackage/__init__.py
__version__ = "0.1.0"
```

### 8.3 git tag 기반
```toml
[build-system]
requires = ["setuptools>=64", "setuptools_scm>=8"]

[tool.setuptools_scm]
write_to = "src/mypackage/_version.py"
```

```bash
git tag v0.1.0
python -m build  # 자동으로 버전 적용
```

## 9. 코드 품질 도구

### 9.1 Black — 포매터
```bash
pip install black

black src/ tests/
black --check .   # 검사만
```

```toml
[tool.black]
line-length = 100
target-version = ["py39", "py310", "py311"]
```

### 9.2 Ruff — 빠른 린터 (Black 도 대체 가능)
```bash
pip install ruff

ruff check .
ruff check --fix .
ruff format .   # Black 호환 포매터
```

```toml
[tool.ruff]
line-length = 100
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "B", "UP"]
# E: pycodestyle 에러, F: pyflakes, I: isort
# N: pep8-naming, W: warnings
# B: bugbear, UP: pyupgrade
```

### 9.3 mypy — 타입 체커
```bash
pip install mypy

mypy src/
```

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
disallow_untyped_defs = true
```

### 9.4 pytest 설정
```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
addopts = [
    "-v",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
]
markers = [
    "slow: 느린 테스트",
    "integration: 통합 테스트",
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__init__.py"]
```

## 10. CLI 도구 만들기

### 10.1 click 사용
```python
# src/mypackage/cli.py
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, help="횟수")
@click.option("--upper", is_flag=True, help="대문자")
def main(name, count, upper):
    """안녕하세요 인사를 출력합니다."""
    greeting = f"Hello, {name}!"
    if upper:
        greeting = greeting.upper()
    for _ in range(count):
        click.echo(greeting)

if __name__ == "__main__":
    main()
```

```toml
# pyproject.toml
[project.scripts]
mygreet = "mypackage.cli:main"
```

설치 후:
```bash
mygreet Alice --count 3 --upper
```

### 10.2 typer (현대적)
```python
import typer

app = typer.Typer()

@app.command()
def greet(name: str, count: int = 1, upper: bool = False):
    """안녕하세요 인사를 출력합니다."""
    greeting = f"Hello, {name}!"
    if upper:
        greeting = greeting.upper()
    for _ in range(count):
        print(greeting)

if __name__ == "__main__":
    app()
```

## 11. 문서화

### 11.1 docstring
```python
def calculate_tax(price: float, rate: float = 0.1) -> float:
    """가격에 세금을 더한 값을 계산합니다.

    Args:
        price: 원가
        rate: 세율 (기본 10%)

    Returns:
        세금이 포함된 가격

    Raises:
        ValueError: 가격이 음수일 때

    Example:
        >>> calculate_tax(100)
        110.0
    """
    if price < 0:
        raise ValueError("음수 불가")
    return price * (1 + rate)
```

### 11.2 Sphinx — 문서 생성
```bash
pip install sphinx sphinx-rtd-theme

sphinx-quickstart docs/
cd docs && make html
```

### 11.3 MkDocs — 더 간단
```bash
pip install mkdocs mkdocs-material

mkdocs new my-docs
mkdocs serve
mkdocs build
```

## 12. CI/CD (GitHub Actions)

### `.github/workflows/test.yml`
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}

      - name: Install
        run: |
          pip install -e ".[dev]"

      - name: Lint
        run: |
          ruff check .
          mypy src/

      - name: Test
        run: pytest
```

### `.github/workflows/publish.yml`
```yaml
name: Publish

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Build
        run: |
          pip install build
          python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

## 13. .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# 가상 환경
venv/
.venv/
env/
ENV/

# 빌드
build/
dist/
*.egg-info/
*.egg

# 테스트/커버리지
.pytest_cache/
.coverage
htmlcov/
.tox/

# 타입 체크
.mypy_cache/
.ruff_cache/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# 환경 변수
.env
.env.local

# 로컬 빌드
*.log
```

## 14. 체크리스트: 완전한 패키지

배포 전 확인:
- [ ] `pyproject.toml` 작성됨
- [ ] `README.md` 와 `LICENSE` 있음
- [ ] 버전 번호 올림
- [ ] 모든 테스트 통과
- [ ] 코드 커버리지 충분 (80%+)
- [ ] 린터/포매터/타입체커 통과
- [ ] CHANGELOG 업데이트
- [ ] 문서 업데이트
- [ ] git tag 생성
- [ ] TestPyPI 에서 테스트
- [ ] PyPI 에 배포

## 15. 실전 예제: 처음부터 끝까지

```bash
# 1. 프로젝트 생성
mkdir my-cli && cd my-cli

# 2. 가상 환경
python -m venv venv
source venv/bin/activate

# 3. 도구 설치
pip install build twine pytest ruff mypy

# 4. 구조 만들기
mkdir -p src/mycli tests
touch src/mycli/__init__.py
touch src/mycli/cli.py
touch tests/test_cli.py

# 5. 코드 작성 (생략)

# 6. pyproject.toml 작성
cat > pyproject.toml <<'EOF'
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "mycli"
version = "0.1.0"
description = "내 첫 CLI 도구"
authors = [{name = "Me", email = "me@example.com"}]
readme = "README.md"
requires-python = ">=3.9"
dependencies = ["click"]

[project.scripts]
mycli = "mycli.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
EOF

# 7. 로컬 설치 테스트
pip install -e .
mycli --help

# 8. 테스트
pytest

# 9. 빌드
python -m build

# 10. 배포 (실제로는 TestPyPI 먼저)
twine upload dist/*
```

## 📝 연습 문제

### 문제 1: 최소 패키지
"hello-world" 만 출력하는 함수가 있는 최소한의 패키지를 만드세요.

### 문제 2: CLI 도구
파일을 받아 줄 수를 세는 CLI 도구를 만들고 `pip install -e .` 로 설치하세요.

### 문제 3: 의존성
requests 를 의존성으로 추가한 패키지를 만드세요.

### 문제 4: 빌드
`python -m build` 로 빌드해 `dist/` 에 wheel 파일을 생성하세요.

### 문제 5: TestPyPI 배포
TestPyPI 에 패키지를 업로드하고 다른 가상 환경에서 설치해 사용해보세요.

## ✅ 체크리스트
- [ ] src layout 의 장점을 안다
- [ ] pyproject.toml 의 주요 섹션을 안다
- [ ] python -m build 로 빌드한다
- [ ] twine upload 로 배포한다
- [ ] pip install -e . 로 개발 설치한다
- [ ] CI/CD 의 기본을 안다

## 🎉 고급 완료!

축하합니다! Python 고급 과정을 모두 마쳤습니다.
이제 [전문가 단계](../04-expert/)로 진행하세요.

## 🔗 다음 단계
👉 [전문가 시작 - 01. 디자인 패턴](../04-expert/01-design-patterns.md)
