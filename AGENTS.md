# Repository Guidelines

Polyglot study/examples mono-repo. Each top-level directory is a self-contained project with its own toolchain. There is no shared build system at the root — work inside the relevant sub-project directory.

## Project Structure

| Directory | Stack | Key Tech |
|-----------|-------|----------|
| `go-work-examples/` | Go | Go Workspace, microservices |
| `msa-saga-examples/` | Go | SAGA, Kafka, PostgreSQL, Redis, Temporal |
| `go-tuckersGo-goWeb/` | Go | 3 independent web tutorial modules |
| `python-examples/`, `python-study/` | Python 3.12+ | ruff, mypy, pytest / stdlib-only exercises |
| `airflow-study/` | Python / Airflow 2.9 | Docker Compose, DAGs |
| `langchain-basic-study/` | Python | LangChain notebooks, uv venv, `.env` required |
| `springboot-rest-api/` | Java / Spring Boot | JPA, HATEOAS, REST Docs, OAuth2 |
| `springboot-*/`, `spring-boot-webflux-mongodb-examples/`, `jpa-orm-study/`, `java-reactive-study/` | Java / Kotlin | per-folder Spring/Hibernate studies |
| `kotlin-study/`, `kotlin-advanced-study/`, `kotlin-coroutine-study/` | Kotlin | coroutines, advanced patterns |
| `design-system/` | Node.js | CSS tokens, SCSS — see its own `AGENTS.md` |
| `nextjs-study/`, `react-study/`, `node-study/` | TypeScript / Node.js | per-subfolder setup |
| `typescript-study/`, `es6-study/`, `extjs-study/` | JS/TS | es6/extjs are pure static HTML+JS |
| `webpack-example/`, `webpack-study/`, `webpack-gulp-study/` | Node.js | era-pinned bundler tutorials |
| `flutter-study/`, `dart-study/` | Dart | Flutter app + standalone scripts |
| `elasticsearch-examples/`, `elk-examples/` | — | ELK stack (Docker Compose) |
| `milvus-examples/`, `qdrant-examples/`, `weaviate-examples/` | — | vector databases (Docker Compose) |
| `k8s-study/`, `k8s-lecture-starter/` | — | Kubernetes manifests, lecture notes |
| `docker-study/`, `docker-examples/`, `jenkins-examples/`, `git-examples/`, `shell-study/` | — | DevOps/scripting studies |

## Build & Run Commands

### `go-work-examples/`

```bash
go work sync                          # sync workspace
./scripts/sync-all.sh                 # tidy all modules
go build ./...                        # verify all modules compile

cd examples/workspace-demo && go run main.go   # demo
cd services/user-service && go run main.go     # port 8080
cd services/order-service && go run main.go    # port 8081
cd services/notification-service && go run main.go  # port 8082

cd tools/cli && go run main.go user create --email "u@example.com" --name "Name"
cd tools/migration && go run main.go list
```

### `msa-saga-examples/`

Running services needs Docker Compose (PostgreSQL ×4, Redis, Kafka, Temporal). No automated tests exist yet — verify with `go build ./...`.

```bash
docker compose up -d                  # before running services
make check-volumes

go build ./...                        # compile check
```

Services: 8001–8004 · Kafka UI: http://localhost:8080 · Temporal UI: http://localhost:8088

### `python-examples/`

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python tools/validate_examples.py    # verify all examples compile
```

### JVM projects (`springboot-*`, `jpa-orm-study`, `java-reactive-study`, `kotlin-*`)

**No Gradle wrapper exists and `.gitignore` excludes `gradlew`/`gradle/` — use a locally installed `gradle`.**

```bash
gradle build                          # from inside the sub-project
gradle test                           # springboot-rest-api uses H2 automatically in tests

# Postgres for springboot-rest-api local dev
docker run --name test-postgres -p 5432:5432 -e POSTGRES_PASSWORD=pass -d postgres
```

See `springboot-rest-api/SCRIPTS.md` for datasource snippets.

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

Full details in `design-system/AGENTS.md`.

## Architecture Notes

**`go-work-examples`** — Go workspace. Consumer `go.mod`s pin a pseudo-version of `shared/` but each also carries a `replace ... => ../../shared` directive, so builds work both inside the workspace (`go.work`) and per-module standalone. `shared/` is the cross-service library; changes propagate immediately to all services and tools.

**`msa-saga-examples`** — Choreography SAGA over Kafka with Outbox pattern: business entity + outbox event saved in one DB transaction, then a background worker polls and publishes to Kafka. Each service follows `internal/{domain,repository,service,handler,worker}` layering. Idempotency checked at event-handler entry via Redis. Temporal containers exist in compose but no Go code uses Temporal yet.

**`design-system`** — 5-layer token pipeline: primitive JSON → semantic JSON (`{token.path}` references) → 7 output formats. Never edit `dist/` by hand.

**`springboot-rest-api`** — HATEOAS-compliant REST API; REST Docs generates API documentation from test assertions (`@ActiveProfiles("test")` switches to H2).

## Gotchas & Conventions

- **Intentionally broken code — do not "fix"**: `k8s-study/examples/09-troubleshooting/*` are broken-on-purpose teaching fixtures.
- **Era-pinned legacy toolchains**: `webpack-gulp-study/` (gulp 3 / Babel 6 / webpack 1) and `webpack-study/` (`node-sass@5`) fail on modern Node. They are historical tutorial snapshots — do not modernize unless asked, and don't debug install failures as if they were bugs.
- **Committed build artifacts**: `webpack-example/dist/` and `webpack-study/dist/` are tracked in git on purpose; `design-system/dist/` is generated (untracked). Don't confuse the two policies.
- **`extjs-study/` requires manual SDK download**: HTML demos reference `libs/ext-5.1.4/`, `libs/ext-6.2.0-gpl/`, which are gitignored. Missing-lib errors are expected until downloaded (see its README).
- **Hardcoded local credentials** (MariaDB `root/1234`, Postgres `pass`, dev JWT secrets) across study configs are intentional for local study use — don't refactor them into env vars unprompted.
- **`go-tuckersGo-goWeb/`**: all 3 modules declare the same module path (`github.com/kyungseok-lee/learn-go-web`). Keep them independent; never combine under one `go.work`.
- Python: activate the project's `venv` before running scripts or installing packages. `langchain-basic-study/` additionally needs a `.env` (see its README).
- Infrastructure-dependent projects (`msa-saga-examples`, `airflow-study`, ELK/vector-db examples, `springboot-rest-api` for runtime) require Docker Compose to be up first.

## Nested Instruction Files

- `design-system/AGENTS.md` (+ `CLAUDE.md`) — token pipeline details
- `python-study/CLAUDE.md`, `jenkins-examples/AGENTS.md` — sub-project specifics
