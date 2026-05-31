## Go Elasticsearch Examples

Go 1.22와 공식 `go-elasticsearch` 클라이언트를 사용해  
Elasticsearch를 **검색 / 로그 분석 / 자동완성** 용도로 활용하는 예제입니다.

루트 PRD(`../docs/elasticsearch-prd.md`)에 정의된 공통 시나리오를  
Go로 어떻게 구현했는지에 집중합니다.

---

## 📋 목차

- [폴더 구조](#-폴더-구조)
- [실행 방법](#-실행-방법)
- [코드 리딩 포인트](#-코드-리딩-포인트)
- [시나리오별 상세 설명](#-시나리오별-상세-설명)

---

## 📁 폴더 구조

```
go-elasticsearch-examples/
├── go.mod, go.sum              # Go 모듈 및 의존성 관리
├── cmd/es-examples/
│   └── main.go                 # 진입점 (app.Run 호출)
├── internal/
│   ├── app/
│   │   └── app.go              # 애플리케이션 부팅/종료, 설정 로드, graceful shutdown
│   ├── esclient/
│   │   └── client.go           # Elasticsearch 클라이언트 래퍼
│   ├── httpapi/
│   │   └── server.go           # HTTP 라우팅 및 핸들러 (Fiber)
│   ├── logging/
│   │   └── logging.go          # slog 기반 공통 로깅 레이어
│   └── scenario/
│       ├── product_search.go   # 상품 검색 시나리오
│       ├── log_analytics.go    # 로그 분석 시나리오
│       ├── autocomplete.go     # 자동완성 시나리오
│       ├── advanced_indexing.go  # 고급 인덱싱 시나리오 (esutil.BulkIndexer)
│       └── utils.go            # 공통 유틸 함수
├── Dockerfile                   # 멀티 스테이지 빌드용 Dockerfile
└── README.md                   # 본 문서
```

### 주요 파일 설명

- **`go.mod`, `go.sum`**  
  Go 모듈 및 의존성 관리
  - `github.com/elastic/go-elasticsearch/v8` (Elasticsearch 공식 클라이언트)

- **`cmd/es-examples/main.go`**  
  CLI 엔트리 포인트
  - `--scenario` 플래그로 시나리오 선택
  - `--reset` 플래그로 인덱스 초기화 및 샘플 데이터 재적재

- **`internal/esclient/client.go`**  
  Elasticsearch 클라이언트 래퍼
  - 환경 변수 기반 설정 (`ELASTICSEARCH_URL`, `ELASTICSEARCH_USERNAME`, `ELASTICSEARCH_PASSWORD`)
  - 기본 헬스 체크(`Cluster.Health`) 기능

- **`internal/scenario/`**  
  시나리오별 구현
  - `product_search.go`: `products` 인덱스 생성, 샘플 데이터 Bulk 인덱싱, Full-text 검색 + 필터 + 정렬 + 집계 쿼리
  - `log_analytics.go`: `app-logs-demo` 인덱스 생성, 샘플 로그 Bulk 인덱싱, 최근 1시간 로그에 대해 서비스/레벨별 집계 및 ERROR 비율 계산
  - `autocomplete.go`: `products-autocomplete` 인덱스 생성 (`completion` 필드), 샘플 자동완성 데이터 인덱싱, `"go"` prefix에 대한 자동완성 쿼리
  - `advanced_indexing.go`: `esutil.BulkIndexer`를 사용한 고성능 인덱싱, 동시성 제어, refresh interval 최적화, 에러 처리 및 성능 모니터링
  - `utils.go`: 공통 유틸 함수 (예: 인덱스 삭제)

- **`Dockerfile`**  
  이 디렉토리 기준으로 Go 바이너리를 빌드하는 멀티 스테이지 Dockerfile

---

## 🚀 실행 방법

### 방법 1: 로컬 Go + Fiber HTTP 서버

**사전 준비**:
- Go 1.22 이상
- 로컬 Elasticsearch 8.x 실행 중 (기본 `http://localhost:9200`)

**환경 변수** (옵션):
- `ELASTICSEARCH_URL` (기본값: `http://localhost:9200`)
- `ELASTICSEARCH_USERNAME`, `ELASTICSEARCH_PASSWORD` (보안 활성화 시)
- `APP_LISTEN_ADDR` (기본 `:8080`)
- `APP_REQUEST_TIMEOUT` (기본 `30s`)

**서버 실행 예시**:
```bash
cd go-elasticsearch-examples

go run ./cmd/es-examples
```

Fiber HTTP 서버가 기본적으로 `:8080` 포트에서 실행됩니다.

**시나리오 실행 예시 (HTTP 요청)**:

```bash
# 헬스 체크 (Elasticsearch 연결 상태 확인)
curl http://localhost:8080/health

# 상품 검색 시나리오 (인덱스 초기화 + 샘플 데이터 재적재)
curl -X POST http://localhost:8080/api/scenarios/product-search \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'

# 로그 분석 시나리오
curl -X POST http://localhost:8080/api/scenarios/log-analytics \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'

# 자동완성 시나리오
curl -X POST http://localhost:8080/api/scenarios/autocomplete \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'

# 고급 인덱싱 시나리오 (esutil.BulkIndexer 사용)
curl -X POST http://localhost:8080/api/scenarios/advanced-indexing \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'
```

### 방법 2: Docker로 실행하기

이 디렉터리의 `Dockerfile`은 **Go 바이너리만을 위한 Dockerfile**입니다.  
실제 로컬 개발 환경 전체(Elasticsearch, Kibana, 앱)는 루트의 `docker-compose.yml`에서 정의합니다.

#### 2.1 단독 이미지 빌드 및 실행

```bash
cd go-elasticsearch-examples

# Docker 이미지 빌드
docker build -t go-elasticsearch-examples .

# Elasticsearch가 localhost:9200에서 떠 있다고 가정
docker run --rm \
  -e ELASTICSEARCH_URL=http://host.docker.internal:9200 \
  go-elasticsearch-examples \
  --scenario=product-search --reset
```

#### 2.2 루트 `docker-compose.yml`과 함께 사용

루트에서:
```bash
cd ..
docker compose up --build app
```

- `docker-compose.yml`의 `app` 서비스가
  - `build.context: ./go-elasticsearch-examples`
  - `dockerfile: Dockerfile`
  로 이 디렉토리를 이용해 이미지를 빌드합니다.

---

## 🔍 코드 리딩 포인트

### 클라이언트 설정 패턴
**파일**: `internal/esclient/client.go`

- 환경 변수 기반 설정 (`NewFromEnv()`)
- 헬스 체크 패턴 (`HealthCheck()`)
- Context 기반 타임아웃 처리

### 인덱스 설계와 매핑
**파일**: `internal/scenario/product_search.go`, `log_analytics.go`, `autocomplete.go`

각 시나리오별로 인덱스 매핑을 정의하고 있습니다:
- 필드 타입 선택 (`text`, `keyword`, `date`, `double`, `completion` 등)
- Multi-field 설정 (예: `name.text` + `name.keyword`)
- Nested 객체 구조 (예: `meta.trace_id`, `meta.user_id`)

### Bulk 인덱싱 패턴
**파일**: `internal/scenario/*.go`의 `indexSample*()` 함수들

**기본 패턴** (`product_search.go`, `log_analytics.go`, `autocomplete.go`):
- 메타 + 소스 JSON을 번갈아 쓰는 전형적인 Bulk 포맷 구현
- `bytes.Buffer`를 사용한 효율적인 문자열 조합
- 에러 처리 및 로깅

**고급 패턴** (`advanced_indexing.go`):
- `esutil.BulkIndexer`를 사용한 고성능 인덱싱
- 동시성 제어 (NumWorkers 설정)
- FlushBytes, FlushInterval 설정으로 자동 flush
- OnSuccess/OnFailure 콜백을 통한 에러 처리
- 성능 통계 수집 (Stats())

### 쿼리 DSL 구성
**파일**: `internal/scenario/*.go`의 `runSample*Queries()` 함수들

- Go의 `map[string]interface{}`로 쿼리 빌드
- `json.MarshalIndent`로 로깅 (디버깅/학습용)
- 실제 요청은 `Search` API에 `WithBody`로 전달
- 응답 파싱 및 결과 출력

이 예제를 기반으로,  
실제 서비스 코드에서는 **구조체 기반 DSL 래퍼, 에러 핸들링/로깅/리트라이, Context 전파** 등을 확장하는 용도로 활용할 수 있습니다.

---

## 📖 시나리오별 상세 설명

### 1. 상품 검색 (Product Search)

**인덱스**: `products`

**인덱스 매핑**:
- `id` (keyword)
- `name` (text + keyword multi-field)
- `description` (text)
- `category` (keyword)
- `tags` (keyword 배열)
- `price` (double)
- `created_at` (date)

**주요 쿼리**:
- `multi_match`: `name`, `description` 필드에서 키워드 검색
- `bool` 쿼리: `must` (검색) + `filter` (카테고리 필터)
- `sort`: 가격 기준 정렬
- `terms` aggregation: 카테고리별 상품 수 집계

**실행 예시**:
```bash
go run ./cmd/es-examples --scenario=product-search --reset
```

### 2. 로그 분석 (Log Analytics)

**인덱스**: `app-logs-demo`

**인덱스 매핑**:
- `timestamp` (date)
- `level` (keyword: INFO, WARN, ERROR 등)
- `service` (keyword)
- `message` (text)
- `meta.trace_id` (keyword)
- `meta.user_id` (keyword)

**주요 쿼리**:
- `range` 쿼리: 최근 1시간 범위 필터
- `terms` aggregation: 서비스별 로그 수 집계
- Nested aggregation: 서비스 내 레벨별 로그 수 집계
- ERROR 비율 계산 (전체 대비 ERROR 개수)

**실행 예시**:
```bash
go run ./cmd/es-examples --scenario=log-analytics --reset
```

### 3. 자동완성 (Autocomplete & Suggest)

**인덱스**: `products-autocomplete`

**인덱스 매핑**:
- `id` (keyword)
- `name` (text)
- `name_suggest` (completion)

**주요 쿼리**:
- `suggest` API 사용
- `completion` suggester: prefix 기반 자동완성
- 입력 예시: `"go"` → `"go 마이크로서비스 입문"`, `"go 고성능 서버 튜닝"` 등 추천

**실행 예시**:
```bash
go run ./cmd/es-examples --scenario=autocomplete --reset
```

### 4. 고급 인덱싱 (Advanced Indexing)

**인덱스**: `advanced-indexing-demo`

**주요 기능**:
- `esutil.BulkIndexer`를 사용한 고성능 인덱싱 (1000개 문서)
- 동시성 제어 (4개 worker)
- Refresh interval 최적화 (인덱싱 중 30초, 완료 후 1초로 복구)
- Replica 설정 최적화 (인덱싱 중 0, 완료 후 1)
- 에러 처리 및 성능 통계 수집

**실행 예시**:
```bash
curl -X POST http://localhost:8080/api/scenarios/advanced-indexing \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'
```

**관련 문서**: [`../docs/elasticsearch-indexing-guide.md`](../docs/elasticsearch-indexing-guide.md)

**주요 학습 포인트**:
- `esutil.BulkIndexer`를 사용한 고성능 인덱싱 패턴
- 동시성 제어 및 Worker 수 최적화 방법
- Refresh interval 조정을 통한 성능 향상
- 에러 처리 및 재시도 로직 구현
- 성능 모니터링 및 통계 수집 (docs/sec, 성공/실패 수 등)

---

## 🔗 관련 링크

- [루트 README](../README.md)
- [PRD 문서](../docs/elasticsearch-prd.md)
- [인덱싱 기술 가이드](../docs/elasticsearch-indexing-guide.md) - Bulk API, esutil.BulkIndexer, 성능 최적화 등
- [Elasticsearch Go 클라이언트 문서](https://github.com/elastic/go-elasticsearch)
