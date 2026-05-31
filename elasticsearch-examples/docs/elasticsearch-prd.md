## Elasticsearch Examples PRD

### 1. 목적

- **학습 목표**
  - 백엔드 엔지니어가 Elasticsearch를 단순 검색 엔진이 아니라 **전략적 인프라 컴포넌트**로 활용할 수 있도록 예제를 제공한다.
  - Go 언어 기반의 코드 예제를 통해 **실무 적용 가능 수준**의 패턴을 익힌다.
- **산출물**
  - `docs/elasticsearch-prd.md`: 본 문서
  - `cmd/` 및 `internal/` 디렉토리의 Go 예제 코드
  - `docker-compose.yml`, `Dockerfile` 기반 **로컬 단일 노드 학습 환경**

---

### 2. 대상 독자

- 주력 스택: Go / Kotlin / Java 백엔드 엔지니어
- 도메인: 마이크로서비스, 대규모 분산 시스템, 이벤트 드리븐 아키텍처
- 관심사:
  - 고성능 / 확장성
  - 운영 및 관측(Observability)
  - 데이터 모델링 및 인덱스 설계

---

### 3. 학습 시나리오 개요

본 예제들은 하나의 공통 Elasticsearch 클러스터를 기반으로 다음 세 가지 핵심 시나리오를 다룬다.

1. **상품 검색(Product Search)**
   - 전형적인 **전문 검색(Full-text Search)** 및 **필터링/정렬** 요구사항을 모델링한다.
   - 기능:
     - 상품 문서 인덱싱 (이름, 설명, 카테고리, 가격, 태그)
     - 키워드 검색 / 카테고리 필터 / 가격 범위 필터
     - 인기 카테고리/태그 집계 (Aggregation)
2. **로그 분석(Log Analytics, 초간단 Observability)**
   - 애플리케이션 로그를 Elasticsearch에 적재하고 **시간 기반 조회 + 집계**를 수행한다.
   - 기능:
     - 로그 인덱스 생성 (timestamp, level, service, message, metadata)
     - 특정 서비스/레벨/시간 범위 필터
     - 레벨별 로그 카운트 및 서비스별 에러 비율 집계
3. **자동완성(Auto-complete & Suggest)**
   - 검색창의 **타입어헤드(Autocomplete)** 기능을 단순한 prefix 검색과 비교하여 구현한다.
   - 기능:
     - 상품 이름 기반 `completion` suggester 설정
     - 키워드 prefix에 대한 추천 결과 반환

각 시나리오는 **단일 Go 바이너리** 안에서 별도 함수로 구성하며, `--scenario` CLI 플래그로 실행 시나리오를 선택할 수 있도록 한다.

---

### 4. 기술 스택 및 버전

- **언어**
  - Go **최신 안정 버전(예: 1.22 이상)** 을 기준으로 한다.
- **Elasticsearch**
  - 8.x 최신 안정 버전 단일 노드 구성 (학습/개발 용도)
- **Go Elasticsearch 클라이언트**
  - 공식 Go 클라이언트 (`github.com/elastic/go-elasticsearch/v8`) 사용을 기본 전제로 한다.
  - Context7 MCP를 활용해 최신 사용 예제 및 베스트 프랙티스를 참조하는 것을 목표로 하나,
    현재 MCP 인자 전달 제약으로 인해 문서/코드 조회가 불가능한 경우 공식 문서 기준으로 설계한다.
- **컨테이너/오케스트레이션**
  - `docker-compose` 기반 단일 노드 클러스터 + (옵션) Kibana
  - Go 예제 애플리케이션용 `Dockerfile`

---

### 5. 디렉토리 구조 (목표)

- `docs/`
  - `elasticsearch-prd.md` (본 문서)
- `cmd/`
  - `es-examples/`
    - `main.go` — CLI 엔트리 포인트
- `internal/`
  - `esclient/`
    - `client.go` — Elasticsearch 클라이언트 래퍼 및 공통 설정
  - `scenario/`
    - `product_search.go` — 상품 검색 시나리오 구현
    - `log_analytics.go` — 로그 분석 시나리오 구현
    - `autocomplete.go` — 자동완성 시나리오 구현
- 최상위
  - `go.mod`, `go.sum`
  - `docker-compose.yml`
  - `Dockerfile`

---

### 6. 기능 요구사항 상세

#### 6.1 공통 기능

- **환경 변수 기반 설정**
  - `ELASTICSEARCH_URL` (기본값: `http://localhost:9200`)
  - `ELASTICSEARCH_USERNAME` (옵션, 보안 비활성화 시 미사용)
  - `ELASTICSEARCH_PASSWORD` (옵션)
- **클라이언트 초기화**
  - 커넥션 풀, 타임아웃, 재시도 정책을 포함한 최소 설정
  - 요청 단위 `context.Context` 사용으로 타임아웃 및 취소 가능
- **기본 헬스 체크**
  - 애플리케이션 시작 시 `GET /` 또는 `GET /_cluster/health` 호출
  - 상태 출력 (green/yellow/red) 및 노드 정보 일부 로그 출력

#### 6.2 상품 검색 (Product Search)

1. **인덱스 설계**
   - 인덱스 이름: `products`
   - 필드 설계:
     - `id` (`keyword`)
     - `name` (`text` + `keyword` multi-field)
     - `description` (`text`)
     - `category` (`keyword`)
     - `tags` (`keyword`)
     - `price` (`double`)
     - `created_at` (`date`)
   - 요구 사항:
     - `name`, `description` 에 대해 full-text 검색 가능
     - `category`, `tags` 에 대해 필터링 및 집계 가능
     - `price` 기준 정렬 가능
2. **데이터 적재**
   - 샘플 데이터 10~20개 수준을 코드 내에 하드코딩하여 Bulk API로 인덱싱
3. **검색 기능**
   - 키워드 매치: `name` 또는 `description` 기준 `multi_match` 쿼리
   - 필터:
     - 카테고리 필터 (`term`)
     - 가격 범위 필터 (`range`)
   - 정렬:
     - 가격 오름차순/내림차순
   - 집계:
     - 카테고리별 상품 수 집계

#### 6.3 로그 분석 (Log Analytics)

1. **인덱스 설계**
   - 인덱스 이름: `app-logs-*` (시간 기반 패턴은 예제로만 소개)
   - 필드:
     - `timestamp` (`date`)
     - `level` (`keyword` — INFO, WARN, ERROR 등)
     - `service` (`keyword`)
     - `message` (`text`)
     - `meta.trace_id` (`keyword`)
     - `meta.user_id` (`keyword`)
2. **데이터 적재**
   - 샘플 로그 N개를 코드에서 생성하여 Bulk 인덱싱
3. **조회/집계**
   - 최근 15분 / 1시간 범위 로그 조회
   - 서비스/레벨별 로그 수 집계
   - 에러 비율 계산(예: 전체 대비 ERROR 비율)

#### 6.4 자동완성 (Autocomplete & Suggest)

1. **인덱스 설계**
   - 인덱스 이름: `products-autocomplete`
   - 필드:
     - `id` (`keyword`)
     - `name` (`text`)
     - `name_suggest` (`completion`)
2. **데이터 적재**
   - 상품명 기준으로 `name_suggest` 필드에 값 설정
3. **자동완성 쿼리**
   - `suggest` API를 사용하여 prefix 기반 추천 결과 반환
   - 단순 prefix match 쿼리와 결과 비교 예시 출력

---

### 7. 실행 방식 (CLI 설계)

- 바이너리 이름 (예시): `es-examples`
- 플래그:
  - `--scenario` (필수, string)
    - 허용값: `product-search`, `log-analytics`, `autocomplete`
  - `--reset` (옵션, bool)
    - 인덱스를 드롭 후 다시 생성하고 샘플 데이터를 재적재
- 사용 예:
  - `go run ./cmd/es-examples --scenario=product-search --reset`
  - `go run ./cmd/es-examples --scenario=log-analytics`

각 시나리오는 실행 로그를 통해 **요청된 쿼리 DSL** 과 **응답 결과 요약**을 함께 출력하여,
단순히 “동작 여부”뿐 아니라 “어떤 쿼리가 어떻게 동작하는지”를 학습할 수 있도록 한다.

---

### 8. Docker 기반 환경 구성 요구사항

- `docker-compose.yml`
  - 서비스:
    - `elasticsearch`
      - 이미지: 공식 Elasticsearch 8.x
      - 환경 변수:
        - `discovery.type=single-node`
        - `xpack.security.enabled=false` (학습용, 운영에서는 보안 필수)
      - 포트 매핑: `9200:9200`
    - `kibana` (옵션)
      - 이미지: 공식 Kibana 8.x
      - 포트 매핑: `5601:5601`
    - `app` (옵션)
      - `Dockerfile` 기반 Go 예제 애플리케이션
      - `ELASTICSEARCH_URL=http://elasticsearch:9200` 환경 변수 주입
- `Dockerfile`
  - 멀티 스테이지 빌드 (builder + runtime)
  - `cmd/es-examples` 바이너리를 빌드하여 경량 런타임 이미지에 포함

---

### 9. 비기능 요구사항

- **코드 품질**
  - SOLID, Clean Architecture를 과도하게 적용하기보다는,
    “예제로서 이해하기 쉬운 구조”를 우선한다.
  - 각 시나리오는 별도 함수로 분리하고, 최소한의 에러 처리 및 로깅을 포함한다.
- **성능/확장성 관점**
  - 샘플 규모는 작지만, 인덱스 설계/쿼리 패턴은
    실제 대용량 트래픽 환경에서도 그대로 적용 가능한 형태를 지향한다.
- **문서화**
  - `README.md` 및 본 PRD를 통해
    - 환경 구성 방법 (Docker)
    - 예제 실행 방법 (Go CLI)
    - 각 시나리오별 목적 및 주요 쿼리
    를 간단히 정리한다.

---

### 10. Git 커밋 전략

1. **PRD 추가**
   - 변경 내용: `docs/elasticsearch-prd.md` 추가
   - 예시 메시지: `docs: add Elasticsearch examples PRD`
2. **Go 예제 코드 추가**
   - 변경 내용: Go 모듈, CLI, 시나리오별 예제 코드 추가
   - 예시 메시지: `feat: add Go Elasticsearch example scenarios`
3. **Docker 환경 구성 추가**
   - 변경 내용: `docker-compose.yml`, `Dockerfile` 등 추가
   - 예시 메시지: `chore: add Docker environment for Elasticsearch examples`

