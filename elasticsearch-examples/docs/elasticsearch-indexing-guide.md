# Elasticsearch 인덱싱 가이드 (2025)

## 목차
1. [개요](#개요)
2. [Bulk API 기초](#bulk-api-기초)
3. [고성능 인덱싱 전략](#고성능-인덱싱-전략)
4. [Go 클라이언트 활용](#go-클라이언트-활용)
5. [에러 처리 및 재시도](#에러-처리-및-재시도)
6. [인덱스 설정 최적화](#인덱스-설정-최적화)
7. [모니터링 및 성능 측정](#모니터링-및-성능-측정)

---

## 개요

Elasticsearch에 데이터를 효율적으로 인덱싱하는 것은 시스템 성능과 확장성에 직접적인 영향을 미칩니다. 본 가이드는 **Elasticsearch 8.x** 기준으로 최신 트렌드와 베스트 프랙티스를 다룹니다.

### 핵심 원칙

1. **단일 문서 인덱싱은 피하라**: Bulk API를 항상 사용
2. **동시성을 활용하라**: 단일 스레드로는 클러스터 용량을 최대화할 수 없음
3. **Refresh Interval을 조정하라**: 인덱싱 중에는 refresh 비용을 최소화
4. **적절한 Bulk Size를 찾아라**: 실험을 통해 최적값 도출
5. **에러를 모니터링하라**: 429 에러는 클러스터 과부하 신호

---

## Bulk API 기초

### Bulk API란?

Bulk API는 여러 인덱싱 작업(`index`, `create`, `update`, `delete`)을 단일 HTTP 요청으로 묶어서 처리하는 API입니다. 단일 문서 인덱싱 대비 **수십 배 빠른 성능**을 제공합니다.

### NDJSON 포맷

Bulk API는 **Newline-Delimited JSON (NDJSON)** 포맷을 사용합니다:

```json
{"index":{"_index":"products","_id":"1"}}
{"name":"Product 1","price":100}
{"index":{"_index":"products","_id":"2"}}
{"name":"Product 2","price":200}
```

각 작업은 두 줄로 구성됩니다:
- **메타 라인**: 작업 타입(`index`, `create`, `update`, `delete`)과 인덱스/ID 정보
- **소스 라인**: 실제 문서 데이터 (delete 작업의 경우 생략)

### 기본 사용 예제

```bash
POST /_bulk
{"index":{"_index":"products","_id":"1"}}
{"name":"Product 1","price":100}
{"index":{"_index":"products","_id":"2"}}
{"name":"Product 2","price":200}
```

---

## 고성능 인덱싱 전략

### 1. Bulk Size 최적화

**권장 접근법**:
- 시작: 100개 문서로 벤치마크
- 점진적 증가: 200, 400, 800, 1600... (2배씩 증가)
- 중지 조건: 인덱싱 속도가 정체되거나 클러스터 리소스가 포화될 때
- 상한선: **수십 MB를 초과하지 않도록** (메모리 압박 방지)

**실무 팁**:
- 문서 크기에 따라 최적 bulk size가 달라짐
- 작은 문서(1KB 이하): 1000~5000개
- 중간 문서(1~10KB): 500~2000개
- 큰 문서(10KB 이상): 100~500개

### 2. 동시성(Concurrency) 활용

**단일 스레드의 한계**:
- Elasticsearch 클러스터는 여러 샤드를 병렬 처리할 수 있음
- 단일 스레드는 클러스터 용량을 최대한 활용하지 못함

**최적 Worker 수 찾기**:
1. Worker 수를 점진적으로 증가 (2, 4, 8, 16...)
2. 클러스터의 CPU 또는 I/O가 포화될 때까지 테스트
3. `TOO_MANY_REQUESTS (429)` 응답이 발생하면 과부하 신호

**권장 설정**:
- CPU 코어 수의 1~2배
- 또는 클러스터 샤드 수와 유사한 수준
- 실험을 통해 최적값 도출

### 3. Refresh Interval 조정

**기본 동작**:
- Elasticsearch는 기본적으로 **1초마다** 인덱스를 refresh
- Refresh는 검색 가능한 상태로 만드는 비용이 큰 작업

**인덱싱 중 최적화**:
```json
PUT /products/_settings
{
  "index": {
    "refresh_interval": "30s"
  }
}
```

또는 인덱싱 완료 후에만 refresh:
```json
PUT /products/_settings
{
  "index": {
    "refresh_interval": "-1"
  }
}
```

**주의사항**:
- Refresh interval을 늘리면 검색 결과에 지연이 발생할 수 있음
- 인덱싱 완료 후 원래 값으로 복구 필요

### 4. 인덱싱 모드 선택

**`index` vs `create`**:
- `index`: 문서가 존재하면 업데이트, 없으면 생성
- `create`: 문서가 이미 존재하면 에러 반환 (중복 방지)

**`_id` 지정 여부**:
- ID 지정: `{"index":{"_index":"products","_id":"1"}}`
- ID 미지정: Elasticsearch가 자동 생성 (UUID)

**실무 권장**:
- 업데이트 가능성이 있으면 `index` + `_id` 지정
- 중복 방지가 필요하면 `create` + `_id` 지정
- 대량 로그 적재는 ID 미지정으로 자동 생성 활용

---

## Go 클라이언트 활용

### esutil.BulkIndexer 소개

`github.com/elastic/go-elasticsearch/v8/esutil` 패키지는 고수준 Bulk 인덱싱 유틸리티를 제공합니다.

**주요 기능**:
- 자동 Bulk 요청 구성 및 전송
- 동시성 제어 (Worker 수 설정)
- 에러 처리 및 재시도 로직
- 성능 모니터링 (통계 수집)

### 기본 사용법

```go
import (
    "github.com/elastic/go-elasticsearch/v8/esutil"
)

bi, err := esutil.NewBulkIndexer(esutil.BulkIndexerConfig{
    Client:        esClient,
    Index:         "products",
    NumWorkers:    4,              // 동시 worker 수
    FlushBytes:    5e6,            // 5MB마다 flush
    FlushInterval: 30 * time.Second,
})
if err != nil {
    log.Fatal(err)
}
defer bi.Close(context.Background())

// 문서 추가
for _, doc := range documents {
    err := bi.Add(context.Background(), esutil.BulkIndexerItem{
        Action:     "index",
        DocumentID: doc.ID,
        Body:       bytes.NewReader(docJSON),
        OnSuccess: func(ctx context.Context, item esutil.BulkIndexerItem, res esutil.BulkIndexerResponseItem) {
            // 성공 콜백
        },
        OnFailure: func(ctx context.Context, item esutil.BulkIndexerItem, res esutil.BulkIndexerResponseItem, err error) {
            // 실패 콜백
        },
    })
    if err != nil {
        log.Fatal(err)
    }
}

// 모든 작업 완료 대기
if err := bi.Close(context.Background()); err != nil {
    log.Fatal(err)
}

// 통계 확인
stats := bi.Stats()
log.Printf("Indexed: %d, Failed: %d", stats.NumAdded, stats.NumFailed)
```

### 설정 옵션

**BulkIndexerConfig 주요 필드**:

| 필드 | 타입 | 설명 | 기본값 |
|------|------|------|--------|
| `Client` | `*elasticsearch.Client` | ES 클라이언트 (필수) | - |
| `Index` | `string` | 기본 인덱스 이름 | - |
| `NumWorkers` | `int` | 동시 worker 수 | `runtime.NumCPU()` |
| `FlushBytes` | `int` | 이 크기마다 flush | `5MB` |
| `FlushInterval` | `time.Duration` | 이 시간마다 flush | `30s` |
| `Timeout` | `time.Duration` | 요청 타임아웃 | `0` (무한) |
| `OnFlushStart` | `func(context.Context) context.Context` | Flush 시작 콜백 | - |
| `OnFlushEnd` | `func(context.Context)` | Flush 완료 콜백 | - |

### 수동 Bulk API 사용

`esutil.BulkIndexer`가 부적합한 경우, 수동으로 Bulk API를 구성할 수 있습니다:

```go
var buf bytes.Buffer
for _, doc := range documents {
    meta := map[string]interface{}{
        "index": map[string]interface{}{
            "_index": "products",
            "_id":    doc.ID,
        },
    }
    metaJSON, _ := json.Marshal(meta)
    docJSON, _ := json.Marshal(doc)
    
    buf.Write(metaJSON)
    buf.WriteByte('\n')
    buf.Write(docJSON)
    buf.WriteByte('\n')
}

res, err := esClient.Bulk(bytes.NewReader(buf.Bytes()))
```

---

## 에러 처리 및 재시도

### Bulk API 응답 구조

Bulk API는 각 작업의 성공/실패를 개별적으로 반환합니다:

```json
{
  "took": 10,
  "errors": true,
  "items": [
    {
      "index": {
        "_index": "products",
        "_id": "1",
        "status": 201,
        "result": "created"
      }
    },
    {
      "index": {
        "_index": "products",
        "_id": "2",
        "status": 429,
        "error": {
          "type": "es_rejected_execution_exception",
          "reason": "rejected execution of..."
        }
      }
    }
  ]
}
```

### HTTP 상태 코드별 처리

**200 OK**: 전체 요청 성공 (개별 항목 실패 가능)
**429 Too Many Requests**: 클러스터 과부하 → **지수 백오프 재시도**
**400 Bad Request**: 매핑 오류 등 → 수정 후 재시도
**500 Internal Server Error**: 일시적 오류 → 재시도 가능

### 재시도 전략

**지수 백오프 (Exponential Backoff)**:
```go
func retryWithBackoff(ctx context.Context, fn func() error) error {
    maxRetries := 5
    baseDelay := 100 * time.Millisecond
    
    for i := 0; i < maxRetries; i++ {
        err := fn()
        if err == nil {
            return nil
        }
        
        // 429 에러인 경우에만 재시도
        if !isRetriableError(err) {
            return err
        }
        
        delay := baseDelay * time.Duration(1<<uint(i))
        select {
        case <-ctx.Done():
            return ctx.Err()
        case <-time.After(delay):
        }
    }
    return fmt.Errorf("max retries exceeded")
}
```

**Jitter 추가** (동시 재시도 방지):
```go
jitter := time.Duration(rand.Intn(100)) * time.Millisecond
delay := baseDelay + jitter
```

### esutil.BulkIndexer의 에러 처리

`OnFailure` 콜백에서 재시도 로직을 구현할 수 있습니다:

```go
bi.Add(ctx, esutil.BulkIndexerItem{
    Action:     "index",
    DocumentID: doc.ID,
    Body:       bytes.NewReader(docJSON),
    OnFailure: func(ctx context.Context, item esutil.BulkIndexerItem, res esutil.BulkIndexerResponseItem, err error) {
        if res.Status == 429 {
            // 재시도 큐에 추가
            retryQueue <- item
        } else {
            // 영구 실패로 기록
            log.Error("permanent failure", "id", item.DocumentID, "error", err)
        }
    },
})
```

---

## 인덱스 설정 최적화

### Refresh Interval

**인덱싱 중**:
```json
PUT /products/_settings
{
  "index": {
    "refresh_interval": "30s"
  }
}
```

**인덱싱 완료 후**:
```json
PUT /products/_settings
{
  "index": {
    "refresh_interval": "1s"
  }
}
```

### Number of Replicas

**인덱싱 중**: Replica를 0으로 설정하여 인덱싱 속도 향상
```json
PUT /products/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
```

**인덱싱 완료 후**: Replica 복구
```json
PUT /products/_settings
{
  "index": {
    "number_of_replicas": 1
  }
}
```

### Translog Durability

**인덱싱 중**: `async`로 설정하여 성능 향상 (데이터 손실 위험 있음)
```json
PUT /products/_settings
{
  "index": {
    "translog.durability": "async",
    "translog.sync_interval": "30s"
  }
}
```

**주의**: 운영 환경에서는 `request` (기본값) 권장

### Indexing Buffer

클러스터 레벨 설정 (elasticsearch.yml):
```yaml
indices.memory.index_buffer_size: 20%
```

---

## 모니터링 및 성능 측정

### 인덱싱 속도 측정

**초당 문서 수 (docs/sec)**:
```
인덱싱 속도 = 총 문서 수 / 소요 시간
```

**초당 MB 수 (MB/sec)**:
```
처리량 = 총 문서 크기(MB) / 소요 시간
```

### 클러스터 메트릭 확인

**인덱싱 통계**:
```bash
GET /products/_stats/indexing
```

**응답 예시**:
```json
{
  "_all": {
    "total": {
      "indexing": {
        "index_total": 10000,
        "index_time_in_millis": 5000,
        "index_current": 0,
        "index_failed": 0,
        "delete_total": 0,
        "delete_time_in_millis": 0,
        "delete_current": 0,
        "noop_update_total": 0,
        "is_throttled": false,
        "throttle_time_in_millis": 0
      }
    }
  }
}
```

**주요 지표**:
- `index_total`: 인덱싱된 문서 수
- `index_time_in_millis`: 총 인덱싱 시간 (ms)
- `index_failed`: 실패한 문서 수
- `is_throttled`: 쓰로틀링 발생 여부

### esutil.BulkIndexer 통계

```go
stats := bi.Stats()
log.Printf("Added: %d", stats.NumAdded)
log.Printf("Failed: %d", stats.NumFailed)
log.Printf("Flushed: %d", stats.NumFlushed)
log.Printf("Duration: %v", stats.Duration)
```

---

## 실무 체크리스트

### 인덱싱 전

- [ ] Bulk API 사용 계획 수립
- [ ] 최적 Bulk Size 실험 계획
- [ ] Worker 수 결정 (초기값: CPU 코어 수)
- [ ] Refresh Interval 조정 계획
- [ ] 에러 처리 및 재시도 로직 구현

### 인덱싱 중

- [ ] 429 에러 모니터링
- [ ] 클러스터 리소스 사용률 확인 (CPU, I/O, 메모리)
- [ ] 인덱싱 속도 추적
- [ ] 실패한 문서 수 모니터링

### 인덱싱 후

- [ ] Refresh Interval 원복
- [ ] Replica 수 복구 (필요시)
- [ ] 인덱싱 통계 확인
- [ ] 검색 가능 여부 확인

---

## 참고 자료

- [Elasticsearch 공식 문서 - Tune for indexing speed](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html)
- [Go Elasticsearch Client - esutil 패키지](https://pkg.go.dev/github.com/elastic/go-elasticsearch/v8/esutil)
- [Bulk API 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)

---

**작성일**: 2025-01-28  
**Elasticsearch 버전**: 8.x  
**Go 클라이언트 버전**: v8.15.0
