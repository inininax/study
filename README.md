# study

다양한 기술 스택을 학습하기 위한 폴리글랏 스터디 모노레포입니다. 각 최상위 디렉터리는 독립적인 프로젝트로, 자체 툴체인과 실행 방법을 가집니다. 루트에는 공통 빌드 시스템이 없으므로 반드시 해당 하위 프로젝트 디렉터리 안에서 작업하세요.

> 🤖 **AI 에이전트 협업 가이드**: [AGENTS.md](./AGENTS.md)가 단일 진실 공급원(single source of truth)입니다. Codex·OpenCode·Cursor는 이 파일을 자동으로 읽고, Claude Code는 [CLAUDE.md](./CLAUDE.md) → AGENTS.md, GitHub Copilot은 [.github/copilot-instructions.md](./.github/copilot-instructions.md), Gemini CLI는 [.gemini/settings.json](./.gemini/settings.json), OpenCode는 [opencode.json](./opencode.json)으로 하위 프로젝트 규칙까지 자동 로드합니다. 규칙 추가 절차는 AGENTS.md의 "Agent Instruction Files" 섹션을 참고하세요.

## 저장소 지도

### Go / MSA

| 디렉터리 | 설명 |
|---|---|
| `go-work-examples/` | Go Workspace 기반 마이크로서비스 예제 (user/order/notification 서비스, CLI 도구) |
| `msa-saga-examples/` | Kafka + Outbox 패턴 Choreography SAGA 구현 (PostgreSQL ×4, Redis, Temporal) |
| `go-tuckersGo-goWeb/` | Go 웹 프로그래밍 튜토리얼 3개 독립 모듈 |

### Python

| 디렉터리 | 설명 |
|---|---|
| `python-examples/` | Python 3.12+ 문법·동시성 예제 (`python tools/validate_examples.py`로 전체 검증) |
| `python-study/` | 외부 의존성 없는 순수 stdlib 연습문제 |
| `airflow-study/` | Airflow 2.9 Docker Compose 실습 (LocalExecutor, DAG 4개) |
| `langchain-basic-study/` | LangChain 입문 노트북 (`.env` 필요, `.env.example` 참고) |

### Java / Spring / Kotlin

| 디렉터리 | 설명 |
|---|---|
| `springboot-rest-api/` | HATEOAS REST API (JPA, REST Docs, OAuth2) — 테스트는 H2 자동 사용 |
| `springboot-data-jpa/`, `springboot-advanced/`, `jpa-orm-study/` | JPA/Hibernate 단계별 학습 |
| `springboot-jwt-example/` | JWT 인증 구현 예제 |
| `spring-boot-webflux-mongodb-examples/` | WebFlux + Reactive MongoDB |
| `java-reactive-study/` | Reactor 기반 리액티브 학습 |
| `kotlin-study/`, `kotlin-advanced-study/`, `kotlin-coroutine-study/` | Kotlin 문법 → 고급 패턴 → 코루틴 |

> ⚠️ JVM 프로젝트에는 Gradle 래퍼가 커밋되어 있지 않습니다(`.gitignore` 정책). 로컬에 설치된 `gradle`을 사용하세요.

### 웹 / 프론트엔드

| 디렉터리 | 설명 |
|---|---|
| `design-system/` | 디자인 토큰 파이프라인 (JSON → CSS/SCSS/TS 등 7종 출력) — 상세: [design-system/AGENTS.md](./design-system/AGENTS.md) |
| `nextjs-study/`, `react-study/`, `node-study/` | Next.js / React / Node 학습 |
| `typescript-study/`, `es6-study/` | TypeScript / ES6+ 문법 |
| `webpack-example/`, `webpack-study/` | Webpack 번들러 학습 (`dist/`가 git에 커밋됨) |
| `webpack-gulp-study/`, `webpack-study/` | ⚠️ 구버전 Node 전용 시대 고정 스냅샷 — 모던 Node에서 설치 실패는 버그가 아님 |
| `extjs-study/` | Ext JS 데모 — `libs/` SDK 수동 다운로드 필요 (README 참고) |
| `flutter-study/`, `dart-study/` | Flutter 앱 + Dart 스크립트 |

### 데이터 / 인프라

| 디렉터리 | 설명 |
|---|---|
| `elasticsearch-examples/`, `elk-examples/` | Elasticsearch 및 ELK 스택 (Docker Compose) |
| `milvus-examples/`, `qdrant-examples/`, `weaviate-examples/` | 벡터 DB 실습 (Docker Compose) |
| `k8s-study/`, `k8s-lecture-starter/` | Kubernetes 매니페스트·강의 노트 (`09-troubleshooting`은 고의로 깨진 교육용 예제) |
| `docker-study/`, `docker-examples/` | Docker 기초 및 응용 |
| `jenkins-examples/` | Jenkins Pipeline 예제 8종 (`scripts/validate-jenkinsfiles.sh` 검증 스크립트) |
| `git-examples/`, `shell-study/` | Git / 셸 스크립트 연습 |
| `hello-world/` | JS/Go/Py 미니 데모 모음 (fibonacci, bouncing balls 등) |
| `prompt-engineering-study/` | 프롬프트 엔지니어링 학습 |

## 시작하기

각 프로젝트의 자세한 실행 명령은 [AGENTS.md](./AGENTS.md)의 "Build & Run Commands" 섹션 또는 각 디렉터리의 README를 참고하세요. 요약:

```bash
# Go 워크스페이스 전체 빌드 (모듈 디렉터리 안에서 실행)
cd go-work-examples && go work sync
for d in shared examples/* services/* tools/*; do (cd "$d" && go build ./...) || echo "FAIL: $d"; done

# MSA SAGA 컴파일 검증 (아직 자동화 테스트 없음)
cd msa-saga-examples && go build ./...

# Python 예제 전체 검증
cd python-examples && python tools/validate_examples.py

# Spring Boot 테스트 (H2 자동)
cd springboot-rest-api && gradle test

# Airflow 스택 기동
cd airflow-study && cp .env.example .env && docker compose up airflow-init && docker compose up -d
```

## 주의사항

- 인프라 의존 프로젝트(`msa-saga-examples`, `airflow-study`, ELK/벡터 DB 예제 등)는 먼저 `docker compose up -d`가 필요합니다.
- 설정 파일의 로컬 개발용 자격증명(MariaDB `root/1234` 등)은 학습 목적으로 의도된 것이며, 실제 서비스 용도가 아닙니다.
- 일부 폴더는 학습 당시의 레거시 툴체인 그대로 보존된 역사적 스냅샷입니다.
