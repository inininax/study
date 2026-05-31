# Level 2: Milvus 중급 (Intermediate)

## 학습 목표

고급 검색 기능과 인덱스 최적화를 통해 실전 프로젝트를 위한 기술을 습득한다.

## 예상 학습 시간

2-3주 (하루 2-3시간 기준)

---

## 📚 학습 내용

### 1. Advanced Search
**파일**: `01_advanced_search.py`

**학습 내용**:
- Hybrid Search (Vector + Scalar Filtering)
- Range Search
- Multi-vector Search
- Search Result Re-ranking

**핵심 개념**:
- Boolean expressions
- Filter optimization
- Query planning
- Result fusion

---

### 2. Partition Management
**파일**: `02_partition_management.py`

**학습 내용**:
- Partition 생성 및 관리
- 파티션 기반 멀티테넌시
- 파티션별 데이터 격리
- 파티션 간 데이터 이동

**핵심 개념**:
- Partition key design
- Data isolation
- Query scoping
- Maintenance strategies

---

### 3. Index Optimization
**파일**: `03_index_optimization.py`

**학습 내용**:
- 다양한 Index 타입 비교 (FLAT, IVF_FLAT, IVF_SQ8, HNSW)
- Index 파라미터 튜닝
- Index 재생성 전략
- Index 성능 벤치마킹

**핵심 개념**:
- Index selection criteria
- Accuracy vs Speed tradeoffs
- Memory optimization
- Build time optimization

---

### 4. Data Migration
**파일**: `04_data_migration.py`

**학습 내용**:
- 버전 간 마이그레이션
- Collection 백업 및 복구
- 스키마 변경 전략
- Zero-downtime migration

**핵심 개념**:
- Migration planning
- Data consistency
- Rollback strategies
- Testing procedures

---

## 🎯 실습 프로젝트

### 프로젝트 1: 멀티테넌트 검색 시스템

**요구사항**:
1. 파티션 기반 테넌트 격리
2. 하이브리드 검색 (벡터 + 필터)
3. 다양한 Index 전략 비교
4. 성능 모니터링

**구현 파일**: `projects/multi_tenant_search.py`

---

## 📊 진도 체크리스트

- [ ] 하이브리드 검색 구현 (벡터 + 3가지 이상 필터 조합)
- [ ] 파티션 기반 멀티테넌시 시스템 구축
- [ ] 3가지 이상 Index 타입 성능 비교
- [ ] 데이터 마이그레이션 스크립트 작성
- [ ] 멀티테넌트 검색 시스템 프로젝트 완성

---

## ⏭️ 다음 단계

Level 2를 완료하면 [Level 3: 고급](../level_3_advanced/README.md)으로 진행하세요.
