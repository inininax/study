# 단계 3: 프로덕션 수준의 API 서버

> FastAPI를 활용한 프로덕션 벡터 검색 API 구축

## 📚 학습 목표

- RESTful API 설계 베스트 프랙티스
- 비동기 처리 및 성능 최적화
- 인증 및 보안
- API 문서화 및 테스팅
- 에러 핸들링 및 로깅

## 🏗 프로젝트 구조

```
03-production-api/
├── app/
│   ├── main.py              # FastAPI 앱
│   ├── config.py            # 설정
│   ├── dependencies.py      # 의존성 주입
│   │
│   ├── routers/
│   │   ├── collections.py   # 컬렉션 API
│   │   ├── vectors.py       # 벡터 CRUD API
│   │   └── search.py        # 검색 API
│   │
│   ├── middleware/
│   │   ├── auth.py          # 인증
│   │   ├── logging.py       # 로깅
│   │   └── rate_limit.py    # 레이트 리미팅
│   │
│   └── models/
│       ├── requests.py      # 요청 모델
│       └── responses.py     # 응답 모델
│
└── tests/
    └── test_api.py
```

## 🚀 API 엔드포인트

### 컬렉션 관리
```
POST   /api/v1/collections              # 컬렉션 생성
GET    /api/v1/collections              # 컬렉션 목록
GET    /api/v1/collections/{name}       # 컬렉션 상세
DELETE /api/v1/collections/{name}       # 컬렉션 삭제
```

### 벡터 작업
```
POST   /api/v1/vectors                  # 벡터 삽입
GET    /api/v1/vectors/{id}             # 벡터 조회
PUT    /api/v1/vectors/{id}             # 벡터 업데이트
DELETE /api/v1/vectors/{id}             # 벡터 삭제
POST   /api/v1/vectors/batch            # 배치 삽입
```

### 검색
```
POST   /api/v1/search                   # 벡터 검색
POST   /api/v1/search/hybrid            # 하이브리드 검색
POST   /api/v1/search/recommend         # 추천
```

### 모니터링
```
GET    /health                          # 헬스체크
GET    /metrics                         # Prometheus 메트릭
GET    /docs                            # API 문서 (Swagger)
```

## 📖 주요 기능

### 1. 비동기 처리

```python
@app.post("/api/v1/search")
async def search_vectors(
    request: SearchRequest,
    ops: VectorOperations = Depends(get_vector_ops)
) -> SearchResponse:
    results = await ops.async_search(
        query_vector=request.vector,
        limit=request.limit
    )
    return SearchResponse(results=results)
```

### 2. 인증 및 보안

```python
# API Key 인증
@app.post("/api/v1/vectors")
async def insert_vector(
    request: VectorInsertRequest,
    api_key: str = Depends(verify_api_key)
):
    # ...
```

### 3. 레이트 리미팅

```python
@app.post("/api/v1/search")
@limiter.limit("100/minute")
async def search(request: Request):
    # ...
```

### 4. 에러 핸들링

```python
@app.exception_handler(VectorDimensionMismatchError)
async def dimension_mismatch_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "error": "DIMENSION_MISMATCH",
            "message": str(exc),
            "details": exc.details
        }
    )
```

## 🧪 API 테스트

### cURL 예제
```bash
# 벡터 삽입
curl -X POST http://localhost:8000/api/v1/vectors \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "collection": "documents",
    "vector": [0.1, 0.2, ...],
    "payload": {"title": "Example"}
  }'

# 검색
curl -X POST http://localhost:8000/api/v1/search \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "collection": "documents",
    "query_vector": [0.1, 0.2, ...],
    "limit": 10
  }'
```

## 🎯 실습 과제

1. **완전한 REST API 구현**: 모든 CRUD 엔드포인트
2. **인증 시스템**: JWT 기반 인증
3. **API 문서화**: OpenAPI/Swagger
4. **통합 테스트**: pytest + httpx

## ✅ 체크리스트

- [ ] FastAPI 앱 구조 설계
- [ ] 비동기 엔드포인트 구현
- [ ] 인증 및 권한 관리
- [ ] 에러 핸들링 표준화
- [ ] API 문서 자동 생성
- [ ] 통합 테스트 작성

---

**난이도**: ⭐⭐⭐⭐☆
**예상 시간**: 4-5시간
**선행 지식**: 단계 1-2 완료, FastAPI 기초
