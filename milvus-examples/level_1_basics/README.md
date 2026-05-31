# Level 1: Milvus 기초 (Basics)

## 학습 목표

Milvus의 핵심 개념을 이해하고 기본적인 CRUD 작업을 production-ready 수준으로 구현할 수 있다.

## 예상 학습 시간

1-2주 (하루 2-3시간 기준)

---

## 📚 학습 내용

### 1. Connection Setup & Management
**파일**: `01_connection_setup.py`

**학습 내용**:
- Milvus 연결 설정
- Connection pooling 구현
- Health check 및 재연결 로직
- 환경별 설정 관리

**핵심 개념**:
- Connection lifecycle
- Pool management
- Error handling
- Retry patterns

**실습**:
```python
# 단일 연결
python 01_connection_setup.py --mode single

# Connection pool 테스트
python 01_connection_setup.py --mode pool

# Health check
python 01_connection_setup.py --mode health
```

---

### 2. Collection Management
**파일**: `02_collection_management.py`

**학습 내용**:
- Collection 스키마 설계
- 다양한 필드 타입 (vector, scalar)
- 인덱스 생성 및 관리
- Collection CRUD 작업

**핵심 개념**:
- Schema design best practices
- Field types and constraints
- Primary key management
- Index types (FLAT, IVF_FLAT, HNSW)

**실습**:
```python
# Collection 생성
python 02_collection_management.py --action create

# 스키마 조회
python 02_collection_management.py --action describe

# Collection 리스트
python 02_collection_management.py --action list

# Collection 삭제
python 02_collection_management.py --action drop
```

---

### 3. Data Insertion
**파일**: `03_data_insertion.py`

**학습 내용**:
- 단건 및 배치 삽입
- 대용량 데이터 처리 (100K+ vectors)
- 트랜잭션 처리
- 삽입 성능 최적화

**핵심 개념**:
- Batch processing
- Memory management
- Async insertion
- Error recovery

**실습**:
```python
# 소량 데이터 삽입 (1K vectors)
python 03_data_insertion.py --size small

# 중량 데이터 삽입 (10K vectors)
python 03_data_insertion.py --size medium

# 대량 데이터 삽입 (100K vectors)
python 03_data_insertion.py --size large

# 성능 벤치마크
python 03_data_insertion.py --benchmark
```

---

### 4. Basic Search
**파일**: `04_basic_search.py`

**학습 내용**:
- Vector similarity search
- Top-K 검색
- 거리 메트릭 (L2, IP, COSINE)
- 검색 결과 처리

**핵심 개념**:
- Similarity metrics
- Search parameters
- Result ranking
- Query optimization

**실습**:
```python
# L2 거리 기반 검색
python 04_basic_search.py --metric L2

# Inner Product 검색
python 04_basic_search.py --metric IP

# Cosine 유사도 검색
python 04_basic_search.py --metric COSINE

# 다양한 Top-K 값 테스트
python 04_basic_search.py --topk 5,10,50,100
```

---

## 🎯 실습 프로젝트

### 프로젝트 1: 간단한 문서 검색 시스템

**요구사항**:
1. 문서 텍스트를 벡터로 변환 (TF-IDF 또는 간단한 임베딩)
2. Milvus에 저장
3. 쿼리 문서와 유사한 문서 검색
4. 결과를 유사도 점수와 함께 반환

**구현 파일**: `projects/simple_doc_search.py`

---

## 📊 진도 체크리스트

- [ ] Milvus 로컬 환경 구축 완료 (Docker)
- [ ] Connection pool 구현 및 테스트
- [ ] 3가지 이상의 스키마로 Collection 생성
- [ ] 100K 이상의 벡터 삽입 성공
- [ ] 3가지 거리 메트릭으로 검색 수행
- [ ] 간단한 문서 검색 시스템 구현

---

## 🔧 문제 해결 (Troubleshooting)

### 연결 실패
```bash
# Milvus 상태 확인
docker-compose ps

# Milvus 로그 확인
docker-compose logs milvus

# 재시작
docker-compose restart milvus
```

### 성능 이슈
- Batch size 조정 (기본 1000)
- Connection pool size 증가
- Index 파라미터 튜닝

### 메모리 부족
- Docker 메모리 할당 증가
- Batch size 감소
- 데이터 분할 처리

---

## 📖 참고 자료

- [Milvus Schema Design](https://milvus.io/docs/schema.md)
- [Milvus Index Types](https://milvus.io/docs/index.md)
- [PyMilvus API Reference](https://milvus.io/api-reference/pymilvus/v2.3.x/About.md)

---

## ⏭️ 다음 단계

Level 1을 완료하면 [Level 2: 중급](../level_2_intermediate/README.md)으로 진행하세요.

**Level 2 미리보기**:
- Advanced search (hybrid, range, filtered)
- Partition management
- Index optimization
- Performance tuning
