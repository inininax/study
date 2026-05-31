# 단계 1: Qdrant 기초 - 설정 및 기본 CRUD

> 프로덕션 수준의 Qdrant 클라이언트 설정 및 기본 벡터 작업

## 📚 학습 목표

이 단계에서는 Qdrant의 핵심 개념을 이해하고, 프로덕션 환경에서 사용할 수 있는 견고한 클라이언트를 구축합니다.

### 핵심 개념
1. **벡터 데이터베이스 기초**
   - 벡터란 무엇인가?
   - 유사도 측정 방법 (Cosine, Dot Product, Euclidean)
   - 벡터 검색의 장점

2. **Qdrant 아키텍처**
   - 컬렉션(Collection) 구조
   - 페이로드(Payload)와 메타데이터
   - 인덱싱 전략 (HNSW)

3. **프로덕션 베스트 프랙티스**
   - 커넥션 풀링
   - 에러 핸들링
   - 재시도 로직
   - 로깅 및 모니터링

## 🏗 프로젝트 구조

```
01-fundamentals/
├── core/
│   ├── __init__.py
│   ├── client.py           # Qdrant 클라이언트 (커넥션 풀링, 헬스체크)
│   ├── collections.py      # 컬렉션 관리 (생성, 삭제, 업데이트)
│   ├── operations.py       # CRUD 작업 (insert, update, delete, retrieve)
│   ├── models.py           # Pydantic 데이터 모델
│   └── exceptions.py       # 커스텀 예외 클래스
│
├── examples/
│   ├── 01_basic_connection.py
│   ├── 02_collection_management.py
│   ├── 03_vector_operations.py
│   ├── 04_batch_operations.py
│   └── 05_error_handling.py
│
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_collections.py
│   └── test_operations.py
│
└── README.md
```

## 🚀 빠른 시작

### 1. Qdrant 서버 실행

```bash
# 프로젝트 루트에서
docker-compose up -d qdrant

# 헬스체크
curl http://localhost:6333/
```

### 2. 기본 연결 테스트

```bash
cd 01-fundamentals
python examples/01_basic_connection.py
```

## 📖 학습 가이드

### 예제 1: 기본 연결 및 헬스체크

**파일**: `examples/01_basic_connection.py`

```python
from core.client import QdrantClientManager

# 클라이언트 생성 (커넥션 풀링 포함)
client_manager = QdrantClientManager()

# 헬스체크
if client_manager.health_check():
    print("✓ Qdrant 서버 정상 작동")

# 컬렉션 목록 조회
collections = client_manager.list_collections()
print(f"컬렉션 목록: {collections}")
```

**학습 포인트**:
- 싱글톤 패턴을 사용한 클라이언트 관리
- 커넥션 풀링의 중요성
- 헬스체크 구현

---

### 예제 2: 컬렉션 생성 및 관리

**파일**: `examples/02_collection_management.py`

다양한 거리 메트릭을 사용한 컬렉션 생성:

```python
from core.collections import CollectionManager
from qdrant_client.models import Distance, VectorParams

manager = CollectionManager()

# Cosine 유사도 (추천: 텍스트 임베딩)
manager.create_collection(
    name="documents",
    vector_size=384,
    distance=Distance.COSINE
)

# Dot Product (추천: 정규화된 벡터)
manager.create_collection(
    name="images",
    vector_size=512,
    distance=Distance.DOT
)

# Euclidean 거리 (추천: 좌표 데이터)
manager.create_collection(
    name="locations",
    vector_size=2,
    distance=Distance.EUCLID
)
```

**학습 포인트**:
- 거리 메트릭 선택 기준
- 벡터 차원 설정
- 컬렉션 최적화 파라미터

---

### 예제 3: 벡터 CRUD 작업

**파일**: `examples/03_vector_operations.py`

```python
from core.operations import VectorOperations
import numpy as np

ops = VectorOperations("documents")

# 1. 단일 벡터 삽입
vector = np.random.rand(384).tolist()
point_id = ops.upsert_point(
    vector=vector,
    payload={
        "title": "Python 프로그래밍 가이드",
        "author": "홍길동",
        "category": "programming",
        "year": 2024
    }
)

# 2. 벡터 조회
point = ops.get_point(point_id)
print(f"조회된 포인트: {point}")

# 3. 페이로드 업데이트
ops.update_payload(
    point_id=point_id,
    payload={"views": 1000, "rating": 4.5}
)

# 4. 벡터 삭제
ops.delete_point(point_id)
```

**학습 포인트**:
- 벡터와 페이로드의 관계
- Upsert vs Insert
- 페이로드 부분 업데이트

---

### 예제 4: 배치 작업 최적화

**파일**: `examples/04_batch_operations.py`

프로덕션에서는 배치 작업이 필수:

```python
from core.operations import VectorOperations
import numpy as np

ops = VectorOperations("documents")

# 1000개의 벡터 생성
vectors = np.random.rand(1000, 384).tolist()
payloads = [
    {
        "title": f"Document {i}",
        "category": np.random.choice(["tech", "science", "art"]),
        "year": np.random.randint(2020, 2025)
    }
    for i in range(1000)
]

# 배치 삽입 (청크 단위로 나눠서 처리)
result = ops.batch_upsert(
    vectors=vectors,
    payloads=payloads,
    chunk_size=100  # 100개씩 나눠서 처리
)

print(f"삽입 완료: {result['inserted']} 개")
print(f"소요 시간: {result['elapsed_time']:.2f}초")
```

**학습 포인트**:
- 배치 크기 최적화
- 메모리 관리
- 성능 측정

---

### 예제 5: 에러 핸들링 및 재시도

**파일**: `examples/05_error_handling.py`

프로덕션에서는 견고한 에러 핸들링이 필수:

```python
from core.operations import VectorOperations
from core.exceptions import (
    QdrantConnectionError,
    QdrantTimeoutError,
    CollectionNotFoundError
)
from tenacity import retry, stop_after_attempt, wait_exponential

ops = VectorOperations("documents")

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def insert_with_retry(vector, payload):
    try:
        return ops.upsert_point(vector, payload)
    except QdrantTimeoutError:
        print("타임아웃 발생, 재시도 중...")
        raise
    except CollectionNotFoundError as e:
        print(f"컬렉션을 찾을 수 없음: {e}")
        # 컬렉션 자동 생성
        ops.create_collection_if_not_exists()
        raise
    except Exception as e:
        print(f"예상치 못한 에러: {e}")
        raise
```

**학습 포인트**:
- 재시도 전략 (exponential backoff)
- 에러 타입별 처리
- 로깅 및 알림

## 🎯 실습 과제

### 과제 1: 다국어 문서 시스템
간단한 다국어 문서 저장 시스템을 구현하세요:
- 컬렉션: `multilingual_docs`
- 페이로드: `{language, title, content, created_at}`
- 100개의 샘플 문서 삽입
- 언어별 통계 조회

### 과제 2: 배치 처리 성능 테스트
배치 크기에 따른 성능을 측정하세요:
- 배치 크기: [10, 50, 100, 500, 1000]
- 총 10,000개의 벡터 삽입
- 소요 시간 및 메모리 사용량 측정

### 과제 3: 장애 복구 시스템
네트워크 장애 시 자동 복구 로직을 구현하세요:
- 연결 실패 시 재연결
- 타임아웃 시 재시도
- 실패한 작업 로깅

## 🧪 테스트 실행

```bash
# 전체 테스트
pytest tests/ -v

# 특정 테스트만
pytest tests/test_client.py -v

# 커버리지 포함
pytest tests/ --cov=core --cov-report=html
```

## 📊 성능 벤치마크

### 단일 삽입 vs 배치 삽입 (10,000개 벡터)

| 방법 | 소요 시간 | 초당 처리량 |
|------|-----------|-------------|
| 단일 삽입 | ~30초 | ~333 ops/s |
| 배치(100) | ~5초 | ~2000 ops/s |
| 배치(500) | ~3초 | ~3333 ops/s |
| 배치(1000) | ~2.5초 | ~4000 ops/s |

**권장 배치 크기**: 100-500 (메모리와 성능의 균형)

## 🔍 디버깅 팁

### 1. 로깅 활성화
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Qdrant UI 사용
브라우저에서 `http://localhost:6333/dashboard` 접속

### 3. 성능 프로파일링
```python
import cProfile
cProfile.run('ops.batch_upsert(vectors, payloads)')
```

## 📚 추가 학습 자료

- [Qdrant 공식 문서](https://qdrant.tech/documentation/)
- [벡터 임베딩 가이드](https://www.pinecone.io/learn/vector-embeddings/)
- [HNSW 알고리즘 설명](https://arxiv.org/abs/1603.09320)

## ✅ 체크리스트

학습을 완료한 후 다음 항목을 확인하세요:

- [ ] Qdrant 클라이언트 연결 성공
- [ ] 다양한 거리 메트릭으로 컬렉션 생성
- [ ] 벡터 CRUD 작업 이해
- [ ] 배치 작업 구현 및 최적화
- [ ] 에러 핸들링 및 재시도 로직 구현
- [ ] 테스트 코드 작성 및 실행
- [ ] 성능 벤치마크 측정

## 🎓 다음 단계

기초를 마스터했다면 [단계 2: 벡터 검색 및 필터링](../02-vector-search/README.md)으로 진행하세요.

---

**난이도**: ⭐⭐☆☆☆
**예상 시간**: 2-3시간
**선행 지식**: Python 기초, REST API 개념
