# Repository Guidelines

Polyglot study/examples mono-repo. Each top-level directory is a self-contained project with its own toolchain. There is no shared build system at the root — work inside the relevant sub-project directory.

## Project Structure

| Directory | Stack | Key Tech |
|-----------|-------|----------|
| `go-work-examples/` | Go | Go Workspace, microservices |
| `msa-saga-examples/` | Go | SAGA, Kafka, PostgreSQL, Redis, Temporal |
| `python-examples/` | Python 3.12+ | ruff, mypy, pytest |
| `springboot-rest-api/` | Java / Spring Boot | JPA, HATEOAS, REST Docs, OAuth2 |
| `airflow-study/` | Python / Airflow 2.9 | Docker Compose, DAGs |
| `design-system/` | Node.js | CSS tokens, SCSS — see `design-system/AGENTS.md` |
| `nextjs-study/` | TypeScript / Next.js | per-subfolder setup |
| `kotlin-*` | Kotlin | coroutines, advanced patterns |
| `langchain-basic-study/` | Python | LangChain, LLM integrations |
| `elasticsearch-examples/`, `elk-examples/` | — | ELK stack |
| `milvus-examples/`, `qdrant-examples/`, `weaviate-examples/` | — | vector databases |
| `k8s-study/`, `k8s-lecture-starter/` | — | Kubernetes |

## Build & Run Commands

### `go-work-examples/`

```bash
go work sync                          # sync workspace
./scripts/sync-all.sh                 # tidy all modules

cd examples/workspace-demo && go run main.go   # demo
cd services/user-service && go run main.go     # port 8080
cd services/order-service && go run main.go    # port 8081
cd services/notification-service && go run main.go  # port 8082

cd tools/cli && go run main.go user create --email "u@example.com" --name "Name"
cd tools/migration && go run main.go list

cd services/user-service && go mod tidy  # per-module tidy
```

### `msa-saga-examples/`

Requires Docker Compose (PostgreSQL ×4, Redis, Kafka, Temporal).

```bash
docker compose up -d
make check-volumes

go test ./...                        # unit tests
go test -cover ./...
go test ./tests/e2e/... -v           # integration (infra must be up)
```

Services: 8001–8004 · Kafka UI: http://localhost:8080 · Temporal UI: http://localhost:8088

### `python-examples/`

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cd 00-quick-start && python 01_syntax_comparison.py
python tools/validate_examples.py    # verify all examples compile
```

### `springboot-rest-api/`

Requires PostgreSQL (H2 used automatically in tests).

```bash
./gradlew build
./gradlew test
./gradlew bootRun

# Postgres for local dev
docker run --name test-postgres -p 5432:5432 -e POSTGRES_PASSWORD=pass -d postgres
```

See `springboot-rest-api/SCRIPTS.md` for `application.properties` datasource snippets.

### `airflow-study/`

```bash
cp .env.example .env
docker compose up airflow-init       # one-time initialisation
docker compose up -d
# Web UI: http://localhost:8080  (airflow / airflow)
```

### `design-system/`

```bash
npm run build    # regenerates dist/ from src/
open examples/index.html
```

Full details in `design-system/AGENTS.md` and `design-system/CLAUDE.md`.

## Architecture Notes

**`go-work-examples`** — Go workspace (no `replace` directives). All modules in `go.work` resolve locally. `shared/` is the cross-service library; changes there propagate immediately to all services and tools.

**`msa-saga-examples`** — Choreography SAGA over Kafka with Outbox pattern: business entity + outbox event saved in one DB transaction, then a background worker polls and publishes to Kafka. Each service follows `internal/{domain,repository,service,handler,worker}` layering. Idempotency checked at event-handler entry via Redis.

**`design-system`** — 5-layer token pipeline: primitive JSON → semantic JSON (`{token.path}` references) → 7 output formats (CSS, SCSS, JSON, DTCG, ESM, CJS, TypeScript). Never edit `dist/` by hand.

**`springboot-rest-api`** — HATEOAS-compliant REST API with hypermedia links; REST Docs generates API documentation from test assertions.

## Cross-project Rules

- Go: each sub-project has its own `go.mod`; run `go` commands from inside that directory, not the root.
- Spring Boot: use the Gradle wrapper (`./gradlew`) — no global Gradle installation required.
- Python: activate the project's `venv` before running scripts or installing packages.
- Infrastructure-dependent projects (`msa-saga-examples`, `airflow-study`, `springboot-rest-api`) require Docker Compose to be up before running the application or integration tests.
