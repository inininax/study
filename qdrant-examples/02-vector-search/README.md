# 단계 2: 벡터 검색 및 필터링

> 고급 벡터 검색 및 하이브리드 필터링 구현

## 📚 학습 목표

- 유사도 검색 알고리즘 이해 (HNSW, IVF)
- 복잡한 필터 쿼리 작성
- 하이브리드 검색 (벡터 + 메타데이터)
- 커스텀 스코어링 및 리랭킹
- 검색 성능 최적화

## 🏗 프로젝트 구조

```
02-vector-search/
├── search/
│   ├── __init__.py
│   ├── semantic.py         # 의미론적 검색
│   ├── filters.py          # 고급 필터링
│   ├── hybrid.py           # 하이브리드 검색
│   └── scoring.py          # 스코어링 함수
│
├── examples/
│   ├── 01_semantic_search.py
│   ├── 02_filter_queries.py
│   ├── 03_hybrid_search.py
│   └── 04_custom_scoring.py
│
└── tests/
    └── test_search.py
```

## 🚀 주요 기능

### 1. 의미론적 검색 (Semantic Search)

텍스트 임베딩을 사용한 의미 기반 검색:

```python
from search.semantic import SemanticSearchEngine

# 검색 엔진 초기화
engine = SemanticSearchEngine("documents")

# 자연어 쿼리로 검색
results = engine.search(
    query="Python 머신러닝 튜토리얼",
    limit=10,
    score_threshold=0.7
)
```

### 2. 고급 필터링

복잡한 조건을 사용한 필터링:

```python
from search.filters import FilterBuilder

# 필터 구성
filter_query = FilterBuilder() \
    .must("category", "AI") \
    .must_not("status", "draft") \
    .should("year", [2023, 2024]) \
    .range("rating", gte=4.0) \
    .build()

# 필터 + 벡터 검색
results = engine.search_with_filter(
    query_vector=query_vector,
    filter_query=filter_query
)
```

### 3. 하이브리드 검색

벡터 검색과 전통적 필터링의 결합:

```python
from search.hybrid import HybridSearch

hybrid = HybridSearch("products")

results = hybrid.search(
    text_query="편안한 운동화",
    filters={
        "price": {"$lt": 100000},
        "brand": {"$in": ["Nike", "Adidas"]},
        "rating": {"$gte": 4.5}
    },
    limit=20
)
```

### 4. 커스텀 스코어링

검색 결과 재점수화:

```python
from search.scoring import CustomScorer

scorer = CustomScorer()

# 가중치 기반 스코어링
reranked = scorer.rerank(
    results=search_results,
    weights={
        "vector_similarity": 0.7,
        "recency": 0.2,
        "popularity": 0.1
    }
)
```

## 📖 실습 예제

### 예제 1: 의미론적 검색 구현
실제 텍스트 데이터로 의미 기반 검색 시스템 구축

### 예제 2: 복합 필터 쿼리
AND, OR, NOT, 범위 쿼리 등 복잡한 필터링

### 예제 3: 하이브리드 검색
벡터 유사도 + 메타데이터 필터링 조합

### 예제 4: 검색 결과 최적화
리랭킹, 다양성 증대, 개인화

## 🎯 실습 과제

1. **전자상거래 검색**: 제품 검색 시스템 (가격, 카테고리, 평점 필터)
2. **뉴스 검색**: 시간 범위, 카테고리, 키워드 기반 검색
3. **추천 시스템**: 사용자 선호도 + 유사도 기반 추천

## ✅ 체크리스트

- [ ] 기본 벡터 검색 구현
- [ ] 필터 쿼리 작성
- [ ] 하이브리드 검색 구현
- [ ] 커스텀 스코어링 적용
- [ ] 검색 성능 측정

---

**난이도**: ⭐⭐⭐☆☆
**예상 시간**: 3-4시간
**선행 지식**: 단계 1 완료, 벡터 임베딩 개념
