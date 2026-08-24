# 고급 학습: RAG와 프로덕션 패턴 🚀

## 학습 목표

1. RAG (Retrieval Augmented Generation) 패턴 구현
2. 멀티테넌시 아키텍처 이해와 활용
3. 성능 최적화 (인덱싱, HNSW, 쿼리 튜닝)
4. 모니터링과 백업 기초

## 필수 선행 학습

✅ 초급 모듈 (01-basics) 완료 필수
✅ 중급 모듈 (02-intermediate) 완료 권장

## 학습 순서

### 1️⃣ RAG 구현 (`01_rag_implementation.py`)
**학습 시간: 2시간**

- RAG 개념: 검색 증강 생성
- 지식베이스 구축 (문서 벡터화)
- 검색(Retrieval) 단계 분리
- 컨텍스트 빌드와 프롬프트 작성
- LLM 답변 생성 (OpenAI, API 키 없으면 모의 응답)

**핵심 개념:**
- 검색 품질이 곧 답변 품질
- 프롬프트 엔지니어링 기초
- 검색과 생성의 역할 분리

### 2️⃣ 멀티테넌시 (`02_multi_tenancy.py`)
**학습 시간: 1.5시간**

- 멀티테넌트 컬렉션 설정
- 테넌트 CRUD (생성/조회/수정/삭제)
- 테넌트별 데이터 격리 확인
- 자동 테넌트 생성/활성화
- SaaS 아키텍처 패턴

**핵심 개념:**
- 테넌트 격리와 데이터 안전
- 테넌트 생명주기 (ACTIVE/INACTIVE)
- 샤딩을 통한 수평 확장

### 3️⃣ 성능 최적화 (`03_performance_optimization.py`)
**학습 시간: 1.5시간**

- 배치 삽입 성능 측정 (dynamic vs fixed_size)
- HNSW 파라미터 이해 (max_connections, ef_construction)
- 쿼리 최적화 (limit, autocut, 프로젝션)
- 설정 동적 변경 (Reconfigure)
- 벡터 압축 (양자화) 소개

**핵심 개념:**
- 정확도 vs 속도 트레이드오프
- 인덱싱 전략
- 병목 지점 찾기

### 4️⃣ 모니터링 (`04_monitoring.py`)
**학습 시간: 1시간**

- 헬스 체크 (ready / live)
- REST 엔드포인트 직접 확인
- 클러스터 노드 통계 조회
- Prometheus 메트릭 연동
- 백업/복원 기초

**핵심 개념:**
- 서비스 상태 관찰 가능성(Observability)
- 메트릭 수집 전략
- 장애 대비 백업 습관

## 실습 방법

```bash
cd lessons/03-advanced

# 각 파일을 순서대로 실행
python 01_rag_implementation.py
python 02_multi_tenancy.py
python 03_performance_optimization.py
python 04_monitoring.py
```

> 💡 `01_rag_implementation.py`는 OpenAI API 키가 있으면 LLM 답변을 생성하고,
> 없어도 검색 결과 + 모의 응답으로 전체 흐름을 학습할 수 있습니다.

## 체크리스트

- [ ] RAG 파이프라인을 스스로 구현할 수 있다
- [ ] 멀티테넌트 컬렉션을 설계하고 운영할 수 있다
- [ ] 성능 병목을 측정하고 개선할 수 있다
- [ ] 헬스 체크와 메트릭으로 서비스 상태를 파악할 수 있다

## 다음 단계

고급 과정을 완료했다면 실전 프로젝트로!

👉 [실전 프로젝트: 지능형 문서 검색 시스템](../../project/README.md)

## 참고 자료

- [Weaviate RAG 가이드](https://weaviate.io/developers/weaviate/search/generative)
- [멀티테넌시 문서](https://weaviate.io/developers/weaviate/manage-data/collections/multi-tenancy-operator-guide)
- [성능 최적화 가이드](https://weaviate.io/developers/weaviate/concepts/storage)
- [모니터링 (Prometheus)](https://weaviate.io/developers/weaviate/configuration/monitoring)
