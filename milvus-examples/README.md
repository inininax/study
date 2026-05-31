# Milvus 학습 커리큘럼 - Backend Expert Level

실무 환경에서 즉시 사용 가능한 Milvus 벡터 데이터베이스 학습 커리큘럼입니다.

## 📚 커리큘럼 개요

이 커리큘럼은 Milvus를 실무 수준에서 활용하기 위한 체계적인 학습 경로를 제공합니다.
모든 코드는 production-ready 수준으로 작성되었으며, 에러 처리, 로깅, 모니터링, 테스트를 포함합니다.

### 학습 로드맵

```
Level 1 (기초) → Level 2 (중급) → Level 3 (고급) → Level 4 (실전)
   1-2주           2-3주           2-3주          3-4주
```

## 🎯 Level 1: 기초 (Basics)
**목표**: Milvus 핵심 개념과 기본 CRUD 작업 마스터

### 학습 내용
- ✅ Connection Management & Pool
- ✅ Collection Schema Design
- ✅ Data Insertion & Batch Processing
- ✅ Basic Vector Search
- ✅ Error Handling & Retry Logic

### 실습 프로젝트
1. **연결 관리 시스템**: Connection pooling, health check
2. **컬렉션 CRUD**: Schema 설계, 생성, 삭제, 인덱싱
3. **대용량 데이터 삽입**: Batch processing, 트랜잭션 처리
4. **기본 검색 시스템**: Vector similarity search

📖 [Level 1 상세 가이드](./level_1_basics/README.md)

---

## 🚀 Level 2: 중급 (Intermediate)
**목표**: 고급 검색 기능 및 최적화 기법 학습

### 학습 내용
- ✅ Advanced Search (Hybrid, Range, Filtered)
- ✅ Partition Management
- ✅ Index Optimization (HNSW, IVF_FLAT, IVF_SQ8)
- ✅ Query Performance Tuning
- ✅ Data Migration & Backup

### 실습 프로젝트
1. **하이브리드 검색 엔진**: 벡터 + 스칼라 필터링
2. **파티션 기반 멀티테넌시**: 테넌트별 데이터 격리
3. **인덱스 벤치마킹**: 성능 비교 및 최적 인덱스 선택
4. **데이터 마이그레이션 도구**: 버전 업그레이드, 백업/복구

📖 [Level 2 상세 가이드](./level_2_intermediate/README.md)

---

## 💪 Level 3: 고급 (Advanced)
**목표**: 대규모 운영 환경 구축 및 성능 튜닝

### 학습 내용
- ✅ Performance Monitoring & Metrics
- ✅ High Availability & Failover
- ✅ Scalability Patterns
- ✅ Resource Management
- ✅ Security & Access Control

### 실습 프로젝트
1. **모니터링 대시보드**: Prometheus + Grafana 연동
2. **고가용성 구성**: 클러스터링, failover 전략
3. **Auto-scaling**: 부하 기반 자동 확장
4. **보안 강화**: TLS, RBAC, 암호화

📖 [Level 3 상세 가이드](./level_3_advanced/README.md)

---

## 🏆 Level 4: 실전 프로젝트 (Production)
**목표**: 실무 시나리오 기반 end-to-end 프로젝트 구현

### 프로젝트 목록

#### 1. **Semantic Search Service**
- OpenAI/HuggingFace 임베딩 연동
- RESTful API (FastAPI)
- Redis 캐싱
- Rate limiting & Authentication

#### 2. **E-commerce Recommendation Engine**
- 협업 필터링 + 벡터 검색
- Real-time personalization
- A/B 테스팅 프레임워크
- 성능 최적화 (sub-100ms latency)

#### 3. **Image Similarity Search**
- CLIP/ResNet 임베딩
- 대용량 이미지 처리 (1M+ images)
- Distributed processing
- CDN 연동

📖 [Level 4 프로젝트 가이드](./level_4_production/README.md)

---

## 🛠️ 환경 설정

### 요구사항
- Python 3.9+
- Docker & Docker Compose
- 8GB+ RAM
- Milvus 2.3+

### 빠른 시작

```bash
# 1. 저장소 클론 (이미 완료)
cd milvus-examples

# 2. 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. Milvus 시작 (Docker)
docker-compose up -d

# 5. 환경변수 설정
cp .env.example .env

# 6. 설치 확인
python -m pytest tests/

# 7. Level 1부터 시작
cd level_1_basics
python 01_connection_setup.py
```

---

## 📁 프로젝트 구조

```
milvus-examples/
├── README.md                    # 메인 가이드
├── requirements.txt             # Python 패키지
├── setup.py                     # 프로젝트 설정
├── docker-compose.yml           # Milvus + 부가 서비스
├── .env.example                 # 환경변수 템플릿
├── pytest.ini                   # 테스트 설정
│
├── config/                      # 설정 파일
│   ├── __init__.py
│   ├── settings.py             # 전역 설정
│   └── logging.yaml            # 로깅 설정
│
├── utils/                       # 공통 유틸리티
│   ├── __init__.py
│   ├── connection.py           # 연결 관리 (Pool, Retry)
│   ├── logger.py               # 구조화된 로깅
│   ├── decorators.py           # 재시도, 타이밍 등
│   └── exceptions.py           # 커스텀 예외
│
├── level_1_basics/              # Level 1: 기초
│   ├── README.md
│   ├── 01_connection_setup.py
│   ├── 02_collection_management.py
│   ├── 03_data_insertion.py
│   ├── 04_basic_search.py
│   └── tests/
│
├── level_2_intermediate/        # Level 2: 중급
│   ├── README.md
│   ├── 01_advanced_search.py
│   ├── 02_partition_management.py
│   ├── 03_index_optimization.py
│   ├── 04_data_migration.py
│   └── tests/
│
├── level_3_advanced/            # Level 3: 고급
│   ├── README.md
│   ├── 01_performance_tuning.py
│   ├── 02_monitoring_metrics.py
│   ├── 03_high_availability.py
│   ├── 04_scalability_patterns.py
│   └── tests/
│
└── level_4_production/          # Level 4: 실전
    ├── README.md
    ├── semantic_search_service/
    │   ├── api/
    │   ├── core/
    │   ├── tests/
    │   └── docker-compose.yml
    ├── recommendation_engine/
    │   └── ...
    └── image_similarity_search/
        └── ...
```

---

## 🧪 테스트

```bash
# 전체 테스트 실행
pytest

# 특정 레벨 테스트
pytest level_1_basics/tests/

# 커버리지 리포트
pytest --cov=. --cov-report=html
```

---

## 📊 학습 진도 체크리스트

### Level 1: 기초
- [ ] Milvus 연결 및 Connection Pool 구현
- [ ] Collection 생성 및 스키마 설계
- [ ] Batch 데이터 삽입 (10K+ vectors)
- [ ] 기본 벡터 검색 구현
- [ ] 에러 처리 및 로깅 적용

### Level 2: 중급
- [ ] 하이브리드 검색 (벡터 + 필터) 구현
- [ ] Partition 기반 멀티테넌시 구축
- [ ] 다양한 인덱스 타입 성능 비교
- [ ] 데이터 마이그레이션 스크립트 작성

### Level 3: 고급
- [ ] Prometheus 메트릭 수집
- [ ] 고가용성 클러스터 구성
- [ ] 부하 테스트 및 성능 튜닝
- [ ] TLS 및 RBAC 설정

### Level 4: 실전
- [ ] Semantic Search API 구축 (FastAPI)
- [ ] Recommendation Engine 구현
- [ ] Image Similarity Search 시스템

---

## 🔗 참고 자료

- [Milvus 공식 문서](https://milvus.io/docs)
- [PyMilvus SDK](https://github.com/milvus-io/pymilvus)
- [Milvus 아키텍처](https://milvus.io/docs/architecture_overview.md)
- [벡터 데이터베이스 Best Practices](https://milvus.io/docs/performance_faq.md)

---

## 📝 라이선스

MIT License

---

## 💡 기여

이슈 및 개선 제안은 언제든 환영합니다!

**제작**: Backend Expert Curriculum for Milvus
**버전**: 1.0.0
**최종 업데이트**: 2025-11-30
