## Elasticsearch Examples

Elasticsearch를 **전략적으로 활용**하기 위한 언어별 예제 모음입니다.  
단순한 CRUD 데모가 아니라, 실무 백엔드 엔지니어가 바로 참고할 수 있는 **검색, 로그 분석, 자동완성** 시나리오를 중심으로 구성합니다.

---

## 📋 목차

- [빠른 시작](#-빠른-시작)
- [리포지토리 구조](#-리포지토리-구조)
- [사용 시나리오 개요](#-사용-시나리오-개요)
- [실행 방법](#-실행-방법)
- [언어별 예제 추가 가이드](#-언어별-예제-추가-가이드)

---

## 🚀 빠른 시작

### Docker Compose로 한 번에 실행 (HTTP API 서버)

```bash
# 리포지토리 루트에서
docker compose up --build
```

이 명령으로 다음이 자동으로 실행됩니다:
- Elasticsearch 8.15.0 (단일 노드, `http://localhost:9200`)
- Kibana 8.15.0 (`http://localhost:5601`)
- Go 예제 앱 (Fiber 기반 HTTP API 서버, `http://localhost:8080`)

예시 요청:

```bash
# 헬스 체크
curl http://localhost:8080/health

# 상품 검색 시나리오 (인덱스 초기화 + 샘플 데이터 재적재)
curl -X POST http://localhost:8080/api/scenarios/product-search \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'

# 고급 인덱싱 시나리오 (esutil.BulkIndexer 사용)
curl -X POST http://localhost:8080/api/scenarios/advanced-indexing \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'
```

### 로컬 Go 환경에서 실행 (HTTP API 서버)

```bash
# Elasticsearch가 localhost:9200에서 실행 중이어야 합니다
cd go-elasticsearch-examples
go run ./cmd/es-examples
```

Fiber HTTP 서버가 `:8080` 포트에서 실행되며, 아래와 같은 HTTP API를 사용할 수 있습니다.

---

## 📁 리포지토리 구조

```
elasticsearch-examples/
├── docs/
│   ├── elasticsearch-prd.md          # 전체 예제의 PRD 문서
│   └── elasticsearch-indexing-guide.md  # Elasticsearch 인덱싱 기술 가이드
├── go-elasticsearch-examples/        # Go 예제 코드
│   ├── cmd/es-examples/              # 진입점 (internal/app.Run 호출)
│   ├── internal/
│   │   ├── app/                      # 부팅/종료, 설정, graceful shutdown
│   │   ├── esclient/                 # ES 클라이언트 래퍼
│   │   ├── scenario/                 # 시나리오별 구현
│   │   ├── httpapi/                  # HTTP 라우팅 및 핸들러
│   │   └── logging/                  # slog 기반 공통 로깅 레이어
│   ├── Dockerfile
│   └── README.md
├── docker-compose.yml                 # 개발 환경 구성
└── README.md                          # 본 문서
```

### 주요 디렉토리 설명

- **`docs/elasticsearch-prd.md`**  
  전체 예제의 목적, 시나리오(상품 검색, 로그 분석, 자동완성), 인덱스 설계, 쿼리 요구사항을 정의한 PRD 문서

- **`docs/elasticsearch-indexing-guide.md`**  
  Elasticsearch 인덱싱 최신 트렌드 및 베스트 프랙티스 가이드 (Bulk API, esutil.BulkIndexer, 성능 최적화 등)

- **`go-elasticsearch-examples/`**  
  Go 1.22 + 공식 `go-elasticsearch` 클라이언트를 사용한 예제 코드
  - `cmd/es-examples/` — CLI 엔트리 포인트
  - `internal/esclient/` — ES 클라이언트 래퍼, 헬스 체크
  - `internal/scenario/` — 시나리오별 구현
    - `product_search.go` — 상품 검색
    - `log_analytics.go` — 로그 분석
    - `autocomplete.go` — 자동완성
    - `advanced_indexing.go` — 고급 인덱싱 기법 (esutil.BulkIndexer, 동시성 제어 등)
    - `utils.go` — 공통 유틸

- **`docker-compose.yml`**  
  개발용 단일 노드 Elasticsearch + Kibana + Go 예제 앱 실행 환경

---

## 📖 사용 시나리오 개요

PRD(`docs/elasticsearch-prd.md`)에서 정의한 공통 시나리오와 추가 고급 시나리오는 다음과 같습니다.

### 1. 상품 검색 (Product Search)

**인덱스**: `products`

**주요 기능**:
- Full-text 검색 (`name`, `description` 필드)
- 카테고리/태그 필터링
- 가격 기준 정렬
- 카테고리별 집계 (Aggregation)

**실행 예시 (HTTP API)**:
```bash
curl -X POST http://localhost:8080/api/scenarios/product-search \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'
```

### 2. 로그 분석 (Log Analytics)

**인덱스**: `app-logs-demo`

**주요 기능**:
- 최근 시간 범위 로그 조회 (예: 최근 1시간)
- 서비스/레벨별 로그 수 집계
- ERROR 비율 계산

**실행 예시 (HTTP API)**:
```bash
curl -X POST http://localhost:8080/api/scenarios/log-analytics \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'
```

### 3. 자동완성 (Autocomplete & Suggest)

**인덱스**: `products-autocomplete`

**주요 기능**:
- `completion` suggester 기반 자동완성
- prefix(`"go"`)에 대한 추천 결과 조회

**실행 예시 (HTTP API)**:
```bash
curl -X POST http://localhost:8080/api/scenarios/autocomplete \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'
```

### 4. 고급 인덱싱 (Advanced Indexing)

**인덱스**: `advanced-indexing-demo`

**주요 기능**:
- `esutil.BulkIndexer`를 사용한 고성능 인덱싱
- 동시성 제어 (Worker 수 조정)
- Refresh interval 최적화
- 에러 처리 및 재시도 로직
- 성능 모니터링 및 통계 수집

**실행 예시 (HTTP API)**:
```bash
curl -X POST http://localhost:8080/api/scenarios/advanced-indexing \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'
```

**관련 문서**: [`docs/elasticsearch-indexing-guide.md`](./docs/elasticsearch-indexing-guide.md)

**주요 학습 포인트**:
- `esutil.BulkIndexer`를 사용한 고성능 인덱싱 패턴
- 동시성 제어 및 Worker 수 최적화 방법
- Refresh interval 조정을 통한 성능 향상
- 에러 처리 및 재시도 로직 구현
- 성능 모니터링 및 통계 수집

---

## 🛠 실행 방법

### 방법 1: Docker Compose (권장)

**사전 준비**:
- Docker / Docker Compose 설치

**실행**:
```bash
# 리포지토리 루트에서
docker compose up --build
```

**포함 서비스**:
- `elasticsearch`: `http://localhost:9200`
- `kibana`: `http://localhost:5601`
- `app` (Go 예제 HTTP API):
  - `go-elasticsearch-examples` 이미지를 빌드한 뒤
  - Fiber 기반 HTTP 서버(`:8080`) 실행

**특정 서비스만 실행**:
```bash
# Go 예제만 실행
docker compose up --build app

# Elasticsearch + Kibana만 실행 (앱 없이)
docker compose up elasticsearch kibana
```

**Kibana 접속**:
- 브라우저에서 `http://localhost:5601` 접속
- 인덱스 패턴을 등록하면 GUI로 데이터 확인 가능

### 방법 2: 로컬 Go 환경 (HTTP API 서버)

**사전 준비**:
- Go 1.22 이상
- 로컬에서 Elasticsearch 8.x 실행 중 (`http://localhost:9200`)

**환경 변수** (옵션):
- `ELASTICSEARCH_URL` (기본값: `http://localhost:9200`)
- `ELASTICSEARCH_USERNAME`, `ELASTICSEARCH_PASSWORD` (보안 활성화 시 사용)

**서버 실행 예시**:
```bash
cd go-elasticsearch-examples
go run ./cmd/es-examples
```

이후 HTTP API로 시나리오를 호출합니다:

```bash
# 헬스 체크 (Elasticsearch 연결 상태 확인)
curl http://localhost:8080/health

# 상품 검색
curl -X POST http://localhost:8080/api/scenarios/product-search \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'

# 로그 분석
curl -X POST http://localhost:8080/api/scenarios/log-analytics \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'

# 자동완성
curl -X POST http://localhost:8080/api/scenarios/autocomplete \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'

# 고급 인덱싱 (esutil.BulkIndexer 사용)
curl -X POST http://localhost:8080/api/scenarios/advanced-indexing \
  -H 'Content-Type: application/json' \
  -d '{"reset": true}'
```

---

## 🔧 언어별 예제 추가 가이드

다른 언어/프레임워크로 예제를 추가할 때는 다음 패턴을 권장합니다.

### 1. 폴더 생성
- 예: `python-elasticsearch-examples/`, `java-elasticsearch-examples/` 등
- 언어명을 포함한 명명 규칙 사용

### 2. 공유 PRD 재사용
- `docs/elasticsearch-prd.md`의 시나리오/인덱스 설계를 그대로 사용
- 언어별 README에서 "PRD 기준으로 어떻게 구현했는지" 설명

### 3. 독립적인 빌드/런타임 설정
- 각 언어/프레임워크의 표준 빌드 도구 사용
- 예: Python (poetry/pip), Java (Maven/Gradle), Node.js (npm/yarn)

### 4. Docker Compose 통합
- `docker-compose.yml`에 새로운 앱 서비스를 추가
- 예: `app-python` 서비스로 FastAPI 컨테이너를 올리고,
  `ELASTICSEARCH_URL=http://elasticsearch:9200` 환경 변수 주입

### 5. README 작성
- 실행 방법, 코드 리딩 포인트, 언어별 특성 설명

이렇게 하면 **데이터 모델과 시나리오는 공통**으로 유지하면서,  
언어별로 **클라이언트 사용법·아키텍처 스타일**을 비교 학습할 수 있습니다.

---

## ✅ 현재 구현된 예제

- ✅ **Go** (`go-elasticsearch-examples/`)
  - Go 1.22 + `github.com/elastic/go-elasticsearch/v8`
  - 상세 내용은 [`go-elasticsearch-examples/README.md`](./go-elasticsearch-examples/README.md) 참조

---

## 📚 추가 자료

- [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Go Elasticsearch 클라이언트 문서](https://github.com/elastic/go-elasticsearch)
- [PRD 문서](./docs/elasticsearch-prd.md)
- [인덱싱 기술 가이드](./docs/elasticsearch-indexing-guide.md) - Bulk API, esutil.BulkIndexer, 성능 최적화 등

---

## 🤝 기여

언어별 예제를 추가하거나 기존 예제를 개선하는 것을 환영합니다!  
PRD(`docs/elasticsearch-prd.md`)의 시나리오를 기준으로 구현해 주세요.
