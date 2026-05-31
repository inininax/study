# 단계 4: 성능 최적화 및 모니터링

> 프로덕션 환경에서의 성능 최적화 및 모니터링

## 📚 학습 목표

- 벡터 인덱스 튜닝 (HNSW 파라미터)
- 쿼리 최적화 기법
- 캐싱 전략 (Redis)
- 메모리 관리 및 샤딩
- 모니터링 및 알림 시스템

## 🏗 프로젝트 구조

```
04-optimization/
├── benchmarks/
│   ├── __init__.py
│   ├── indexing_benchmark.py      # 인덱싱 벤치마크
│   ├── search_benchmark.py        # 검색 성능 측정
│   └── memory_profiling.py        # 메모리 프로파일링
│
├── caching/
│   ├── __init__.py
│   ├── redis_cache.py             # Redis 캐싱
│   └── strategies.py              # 캐싱 전략
│
└── monitoring/
    ├── __init__.py
    ├── metrics.py                 # Prometheus 메트릭
    └── dashboards/
        └── grafana_dashboard.json
```

## 🚀 핵심 최적화 기법

### 1. HNSW 파라미터 튜닝

```python
# 정확도 우선 (느리지만 정확)
hnsw_config = {
    "m": 64,              # 연결 수 증가
    "ef_construct": 200   # 구성 품질 향상
}

# 속도 우선 (빠르지만 덜 정확)
hnsw_config = {
    "m": 16,              # 연결 수 감소
    "ef_construct": 100   # 구성 속도 향상
}

# 균형 (추천)
hnsw_config = {
    "m": 32,
    "ef_construct": 128
}
```

### 2. Redis 캐싱

```python
from caching.redis_cache import VectorCache

cache = VectorCache(
    redis_host="localhost",
    ttl=3600  # 1시간
)

# 검색 결과 캐싱
@cache.cache_search_results
async def search(query_vector):
    return await qdrant_client.search(...)
```

### 3. 성능 벤치마킹

```python
from benchmarks.search_benchmark import SearchBenchmark

benchmark = SearchBenchmark(collection_name="products")

results = benchmark.run(
    num_queries=1000,
    vector_size=384,
    top_k=10
)

print(f"평균 응답 시간: {results['avg_latency_ms']}ms")
print(f"처리량: {results['throughput_qps']} QPS")
print(f"P95 latency: {results['p95_latency_ms']}ms")
print(f"P99 latency: {results['p99_latency_ms']}ms")
```

### 4. Prometheus 메트릭

```python
from monitoring.metrics import setup_metrics

metrics = setup_metrics()

# 커스텀 메트릭
with metrics.search_duration.time():
    results = await search(query)

metrics.search_total.inc()
metrics.results_count.observe(len(results))
```

## 📊 최적화 체크리스트

### 인덱스 최적화
- [ ] HNSW 파라미터 벤치마크
- [ ] 적절한 벡터 차원 선택
- [ ] 세그먼트 수 조정
- [ ] 온디스크 vs 인메모리 결정

### 쿼리 최적화
- [ ] 배치 쿼리 사용
- [ ] 불필요한 페이로드 제외
- [ ] 스코어 임계값 활용
- [ ] 캐싱 전략 적용

### 시스템 최적화
- [ ] 커넥션 풀링 설정
- [ ] 타임아웃 적절히 설정
- [ ] 메모리 제한 설정
- [ ] 로그 레벨 조정

### 모니터링
- [ ] Prometheus 메트릭 수집
- [ ] Grafana 대시보드 구성
- [ ] 알림 규칙 설정
- [ ] 로그 집계 (ELK)

## 🎯 성능 목표

### 응답 시간
- P50: < 10ms
- P95: < 50ms
- P99: < 100ms

### 처리량
- 검색: > 1000 QPS
- 삽입: > 5000 ops/s

### 리소스
- 메모리: < 8GB (100만 벡터 기준)
- CPU: < 50% (정상 부하)

## 📚 참고 자료

- [HNSW 논문](https://arxiv.org/abs/1603.09320)
- [Qdrant 성능 가이드](https://qdrant.tech/documentation/guides/optimize/)
- [Redis 캐싱 패턴](https://redis.io/docs/manual/patterns/)

---

**난이도**: ⭐⭐⭐⭐☆
**예상 시간**: 4-5시간
**선행 지식**: 단계 1-3 완료, 시스템 성능 측정 경험
