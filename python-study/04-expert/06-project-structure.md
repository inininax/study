# 06. 프로젝트 구조와 아키텍처

## 🎯 학습 목표
- 다양한 프로젝트 구조를 안다
- Clean Architecture 를 이해한다
- 의존성 관리 전략을 안다
- 큰 프로젝트를 조직하는 방법을 안다

## 1. 프로젝트 구조의 중요성

좋은 구조는:
- 📖 **이해 용이**: 새 개발자도 빠르게 적응
- 🔧 **변경 용이**: 한 곳 변경이 다른 곳에 영향 적음
- 🧪 **테스트 가능**: 컴포넌트 격리
- ♻️ **재사용 가능**: 모듈 단위로 분리
- 📈 **확장 가능**: 큰 규모로 성장 가능

## 2. 단순한 프로젝트 구조

### 2.1 작은 스크립트
```
my_script/
├── script.py
├── requirements.txt
└── README.md
```

### 2.2 작은 패키지
```
mypackage/
├── pyproject.toml
├── README.md
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
└── tests/
    ├── __init__.py
    └── test_core.py
```

## 3. 중간 규모 프로젝트

### 모듈 분리
```
mypackage/
├── pyproject.toml
├── README.md
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── __main__.py      # CLI 진입점
│       ├── cli.py
│       ├── config.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── services.py
│       │   └── exceptions.py
│       ├── data/
│       │   ├── __init__.py
│       │   ├── repository.py
│       │   └── database.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── logging.py
│       │   └── helpers.py
│       └── py.typed         # 타입 힌트 제공 표시
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── docs/
└── scripts/
```

## 4. 웹 애플리케이션 구조

### 4.1 Flask/FastAPI 작은 앱
```
myapp/
├── pyproject.toml
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py          # app 인스턴스
│       ├── config.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py       # Pydantic
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── users.py
│       │   └── posts.py
│       └── services/
│           └── auth.py
└── tests/
```

### 4.2 큰 웹 앱 (도메인별)
```
myapp/
├── pyproject.toml
├── alembic/                 # DB 마이그레이션
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── auth/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── service.py
│       │   ├── router.py
│       │   └── dependencies.py
│       ├── users/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── service.py
│       │   └── router.py
│       ├── posts/
│       │   └── (같은 구조)
│       └── core/
│           ├── exceptions.py
│           └── middleware.py
└── tests/
    ├── auth/
    ├── users/
    └── posts/
```

## 5. Clean Architecture

### 5.1 핵심 아이디어
의존성은 **안쪽 (도메인)** 으로만 향함.

```
┌──────────────────────────────┐
│  Interfaces (UI, API, CLI)   │  ← 외부
├──────────────────────────────┤
│  Application (Use Cases)     │
├──────────────────────────────┤
│  Domain (Entities, Rules)    │  ← 핵심 (의존성 없음)
└──────────────────────────────┘
       의존성은 안쪽으로만!
```

### 5.2 구조
```
myapp/
├── domain/                  # 비즈니스 로직 (의존성 없음)
│   ├── entities/
│   │   └── user.py
│   ├── value_objects/
│   │   └── email.py
│   └── exceptions.py
├── application/             # 유스케이스
│   ├── use_cases/
│   │   ├── create_user.py
│   │   └── delete_user.py
│   ├── ports/               # 인터페이스
│   │   ├── user_repository.py
│   │   └── email_sender.py
│   └── dtos.py
├── infrastructure/          # 외부 시스템 구현
│   ├── persistence/
│   │   └── sql_user_repository.py
│   ├── email/
│   │   └── smtp_sender.py
│   └── config.py
└── interfaces/              # 진입점
    ├── api/                 # FastAPI
    ├── cli/                 # CLI
    └── workers/             # 백그라운드
```

### 5.3 예시 코드

#### Domain
```python
# domain/entities/user.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int | None
    name: str
    email: str
    created_at: datetime

    def __post_init__(self):
        if not self.name:
            raise ValueError("이름 필수")
        if "@" not in self.email:
            raise ValueError("잘못된 이메일")
```

#### Application (Port)
```python
# application/ports/user_repository.py
from abc import ABC, abstractmethod
from domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        ...
```

#### Application (Use Case)
```python
# application/use_cases/create_user.py
from dataclasses import dataclass
from domain.entities.user import User
from application.ports.user_repository import UserRepository
from application.ports.email_sender import EmailSender

@dataclass
class CreateUserUseCase:
    repo: UserRepository
    mailer: EmailSender

    def execute(self, name: str, email: str) -> User:
        if self.repo.find_by_email(email):
            raise ValueError("이미 가입된 이메일")

        user = User(id=None, name=name, email=email, created_at=datetime.now())
        saved = self.repo.save(user)
        self.mailer.send_welcome(saved)
        return saved
```

#### Infrastructure
```python
# infrastructure/persistence/sql_user_repository.py
from sqlalchemy.orm import Session
from application.ports.user_repository import UserRepository
from domain.entities.user import User

class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        # SQL 구현
        ...

    def find_by_email(self, email: str) -> User | None:
        # SQL 구현
        ...
```

#### Interface
```python
# interfaces/api/users.py
from fastapi import APIRouter, Depends
from application.use_cases.create_user import CreateUserUseCase

router = APIRouter()

@router.post("/users")
def create_user(
    data: UserCreateDTO,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    return use_case.execute(data.name, data.email)
```

## 6. Hexagonal Architecture (Ports & Adapters)

### 핵심
- **Application Core**: 비즈니스 로직 (포트만 정의)
- **Adapters**: 외부 시스템 (포트 구현)

```
       ┌──── Adapter (REST API) ────┐
       │                            │
Adapter (CLI) ── Application ── Adapter (DB)
       │           Core             │
       └──── Adapter (Worker) ──────┘
```

장점:
- 인프라 교체 쉬움 (DB → MongoDB, REST → GraphQL)
- 테스트 용이 (mock adapter)

## 7. 의존성 주입 (DI)

### 7.1 수동 주입
```python
# 인터페이스
class Logger(Protocol):
    def log(self, msg: str): ...

class EmailService(Protocol):
    def send(self, to: str, msg: str): ...

# 구현
class ConsoleLogger:
    def log(self, msg: str):
        print(f"[LOG] {msg}")

class GmailService:
    def send(self, to: str, msg: str):
        # SMTP 호출
        pass

# 서비스
class UserService:
    def __init__(self, logger: Logger, mailer: EmailService):
        self.logger = logger
        self.mailer = mailer

    def create_user(self, name, email):
        self.logger.log(f"Creating user {name}")
        # ...
        self.mailer.send(email, "환영합니다")

# 사용 (조립)
service = UserService(
    logger=ConsoleLogger(),
    mailer=GmailService(),
)
service.create_user("Alice", "a@example.com")
```

### 7.2 DI 컨테이너 (dependency-injector)
```bash
pip install dependency-injector
```

```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(ConsoleLogger)
    mailer = providers.Factory(
        GmailService,
        smtp_host=config.smtp_host,
    )

    user_service = providers.Factory(
        UserService,
        logger=logger,
        mailer=mailer,
    )

# 사용
container = Container()
container.config.smtp_host.from_env("SMTP_HOST")

service = container.user_service()
```

## 8. 설정 관리

### 8.1 pydantic-settings (권장)
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # 데이터베이스
    database_url: str
    db_echo: bool = False

    # 인증
    secret_key: str
    token_expire_minutes: int = 60

    # 외부 API
    api_key: str
    api_timeout: int = 30

    # 환경
    debug: bool = False
    log_level: str = "INFO"

settings = Settings()
```

### 8.2 환경별 설정
```python
import os

class BaseSettings:
    DATABASE_URL: str = "sqlite:///./app.db"
    LOG_LEVEL: str = "INFO"

class DevelopmentSettings(BaseSettings):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

class ProductionSettings(BaseSettings):
    DEBUG: bool = False
    DATABASE_URL: str = os.environ["DATABASE_URL"]

class TestSettings(BaseSettings):
    DATABASE_URL: str = "sqlite:///:memory:"

def get_settings():
    env = os.environ.get("ENV", "development")
    return {
        "development": DevelopmentSettings(),
        "production": ProductionSettings(),
        "test": TestSettings(),
    }[env]
```

## 9. 데이터베이스 마이그레이션 (Alembic)

```bash
pip install alembic
alembic init alembic
```

```python
# alembic/env.py
from myapp.models import Base
target_metadata = Base.metadata
```

```bash
# 새 마이그레이션 생성
alembic revision --autogenerate -m "Create users table"

# 적용
alembic upgrade head

# 되돌리기
alembic downgrade -1
```

## 10. CI/CD 파이프라인

### 10.1 GitHub Actions
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy src/

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.9", "3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install -e ".[dev]"
      - run: pytest --cov

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install bandit safety
      - run: bandit -r src/
      - run: safety check
```

## 11. Docker 화

### Dockerfile
```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app

# 의존성 설치
COPY pyproject.toml .
RUN pip install --no-cache-dir build && \
    python -m build --wheel

# 런타임 이미지
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl

# non-root 사용자
RUN useradd -m -u 1000 app
USER app

EXPOSE 8000

CMD ["uvicorn", "myapp.main:app", "--host", "0.0.0.0"]
```

### docker-compose
```yaml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db/myapp
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  pgdata:
```

## 12. 모노레포 vs 마이크로레포

### 모노레포 (한 저장소)
```
my-monorepo/
├── packages/
│   ├── core/
│   │   ├── pyproject.toml
│   │   └── src/core/
│   ├── api/
│   │   ├── pyproject.toml
│   │   └── src/api/
│   └── worker/
│       ├── pyproject.toml
│       └── src/worker/
├── apps/
│   ├── web/
│   └── cli/
└── pyproject.toml          # 작업영역
```

장점: 변경 추적 쉬움, 공유 의존성, 일관된 도구
단점: 큰 저장소, 빌드 시간

### 마이크로레포 (저장소 별)
- 독립 배포
- 팀별 분리
- 의존성 관리 복잡

## 13. 좋은 README 구조

```markdown
# 프로젝트 이름

배지 (CI 상태, 커버리지, 버전 등)

## 소개
프로젝트가 무엇인지 1-2 문단

## 주요 기능
- 핵심 기능 1
- 핵심 기능 2

## 빠른 시작
\```bash
pip install mypackage
mypackage --help
\```

## 설치
상세 설치 방법

## 사용법
코드 예시

## 개발
\```bash
git clone ...
cd ...
pip install -e ".[dev]"
pytest
\```

## 기여
기여 가이드

## 라이센스
MIT
```

## 14. 실전 체크리스트

새 프로젝트 시작 시:
- [ ] pyproject.toml 설정
- [ ] src 레이아웃 선택
- [ ] 가상 환경 (venv/poetry/uv)
- [ ] .gitignore 작성
- [ ] README 작성
- [ ] LICENSE 추가
- [ ] 린터/포매터 설정 (ruff)
- [ ] 타입 체커 (mypy)
- [ ] 테스트 프레임워크 (pytest)
- [ ] pre-commit 훅
- [ ] CI/CD 파이프라인
- [ ] 환경 변수 (.env.example)
- [ ] 도커파일 (필요시)
- [ ] CONTRIBUTING.md (오픈소스)

## 15. 학습 자료

### 책
- "Architecture Patterns with Python" (Harry Percival)
- "Clean Architecture" (Robert C. Martin)
- "Domain-Driven Design" (Eric Evans)

### 온라인
- [Cosmic Python](https://www.cosmicpython.com/)
- [Real Python](https://realpython.com/)
- [Python 공식 문서](https://docs.python.org/3/)

## 📝 연습 문제

### 문제 1: 기본 구조
src layout 으로 새 패키지를 시작해보세요.

### 문제 2: 도메인 분리
간단한 ToDo 앱을 도메인/애플리케이션/인프라/인터페이스로 분리해보세요.

### 문제 3: 의존성 주입
서비스 클래스에 의존성을 주입하도록 리팩토링하세요.

### 문제 4: 설정
pydantic-settings 로 환경별 설정을 구현하세요.

### 문제 5: CI/CD
GitHub Actions 로 린트, 테스트, 빌드 파이프라인을 만드세요.

## ✅ 체크리스트
- [ ] 프로젝트 규모에 맞는 구조를 선택한다
- [ ] Clean Architecture 의 원칙을 안다
- [ ] 의존성 주입을 활용한다
- [ ] 환경 설정을 안전하게 관리한다
- [ ] CI/CD 파이프라인을 구축한다
- [ ] Docker 화한다

## 🎉 전문가 과정 완료!

축하합니다! Python 학습 로드맵의 모든 단계를 완료했습니다.

이제 당신은:
- ✅ Python 의 모든 기본 문법을 마스터함
- ✅ OOP, 함수형, 비동기 패러다임을 활용함
- ✅ 실전 프로젝트를 설계하고 구축할 수 있음
- ✅ 데이터 분석, 웹 개발, 자동화를 수행함
- ✅ 코드 품질과 베스트 프랙티스를 안다

## 🚀 다음 단계

### 더 깊이 파고들기
- **머신러닝/AI**: scikit-learn, TensorFlow, PyTorch
- **데이터 엔지니어링**: Airflow, Spark, Kafka
- **DevOps**: Kubernetes, Terraform
- **시스템 프로그래밍**: Cython, ctypes, FFI

### 실전 프로젝트
- 오픈소스에 기여
- 자신만의 패키지 PyPI 배포
- 개인 프로젝트 (블로그, 봇, 게임 등)

### 커뮤니티
- PyCon 참가
- 지역 Python 모임
- Python 공식 문서 번역 기여

## 🔗 추가 자료
👉 [메인 README 로 돌아가기](../README.md)
👉 [예제 코드](../examples/)
👉 [연습 문제](../exercises/)

---

**Happy Pythoning! 🐍**
