# Qdrant 백엔드 전문가 학습 커리큘럼

> 실무 환경에서 즉시 사용 가능한 수준의 Qdrant 벡터 데이터베이스 학습 프로젝트

## 📚 커리큘럼 개요

이 프로젝트는 백엔드 전문가를 위한 체계적인 Qdrant 학습 과정을 제공합니다. 각 단계는 실무에서 바로 적용 가능한 프로덕션 수준의 코드와 베스트 프랙티스를 포함합니다.

### 학습 목표
- Qdrant 벡터 데이터베이스의 핵심 개념 이해
- 프로덕션 환경에서의 벡터 검색 시스템 구축 능력
- 성능 최적화 및 스케일링 전략 습득
- RAG(Retrieval-Augmented Generation) 시스템 구현 능력

## 🎯 커리큘럼 구조

### [단계 1: Qdrant 기초 - 설정 및 기본 CRUD](./01-fundamentals/README.md)
**예상 학습 시간: 2-3시간**

#### 학습 내용
- Qdrant 아키텍처 및 핵심 개념
- Docker를 이용한 Qdrant 서버 설정
- 컬렉션 생성 및 관리
- 벡터 데이터 CRUD 작업
- 페이로드(메타데이터) 관리

#### 실습 프로젝트
- 기본 벡터 DB 연결 및 헬스체크
- 다양한 거리 메트릭을 사용한 컬렉션 생성
- 배치 인서트 구현
- 에러 핸들링 및 재시도 로직

#### 핵심 코드
```python
# 01-fundamentals/core/client.py - 프로덕션 수준의 클라이언트
# 01-fundamentals/core/collections.py - 컬렉션 관리
# 01-fundamentals/core/operations.py - CRUD 작업
```

---

### [단계 2: 벡터 검색 및 필터링](./02-vector-search/README.md)
**예상 학습 시간: 3-4시간**

#### 학습 내용
- 유사도 검색 알고리즘 (HNSW, IVF)
- 복잡한 필터 쿼리 작성
- 하이브리드 검색 (벡터 + 필터)
- 점수 함수 및 리랭킹
- 벡터 임베딩 전략

#### 실습 프로젝트
- 의미론적 검색 엔진 구현
- 다단계 필터링 시스템
- 커스텀 스코어링 함수
- 벡터 인덱스 최적화

#### 핵심 코드
```python
# 02-vector-search/search/semantic.py - 의미론적 검색
# 02-vector-search/search/filters.py - 고급 필터링
# 02-vector-search/search/hybrid.py - 하이브리드 검색
```

---

### [단계 3: 프로덕션 수준의 API 서버](./03-production-api/README.md)
**예상 학습 시간: 4-5시간**

#### 학습 내용
- FastAPI를 활용한 RESTful API 설계
- 비동기 처리 및 커넥션 풀링
- 입력 검증 및 에러 처리
- API 문서화 (OpenAPI/Swagger)
- 보안 및 인증 (API Key, JWT)
- 레이트 리미팅

#### 실습 프로젝트
- 완전한 벡터 검색 API 서버
- 헬스체크 및 메트릭 엔드포인트
- 미들웨어 구현 (로깅, CORS, 인증)
- Pydantic을 활용한 데이터 검증

#### 핵심 코드
```python
# 03-production-api/app/main.py - FastAPI 애플리케이션
# 03-production-api/app/routers/ - API 라우터들
# 03-production-api/app/middleware/ - 커스텀 미들웨어
# 03-production-api/app/models/ - Pydantic 모델들
```

---

### [단계 4: 성능 최적화 및 모니터링](./04-optimization/README.md)
**예상 학습 시간: 4-5시간**

#### 학습 내용
- 벡터 인덱스 튜닝 (HNSW 파라미터)
- 쿼리 최적화 기법
- 캐싱 전략 (Redis 통합)
- 메모리 관리 및 샤딩
- 프로메테우스 메트릭 수집
- 분산 추적 (OpenTelemetry)

#### 실습 프로젝트
- 벤치마킹 도구 개발
- 성능 프로파일링 시스템
- Redis 캐싱 레이어 구현
- Prometheus + Grafana 대시보드

#### 핵심 코드
```python
# 04-optimization/benchmarks/ - 벤치마크 스크립트
# 04-optimization/caching/ - 캐싱 전략
# 04-optimization/monitoring/ - 모니터링 설정
```

---

### [단계 5: 실전 프로젝트 - RAG 시스템](./05-real-project/README.md)
**예상 학습 시간: 6-8시간**

#### 학습 내용
- RAG 아키텍처 설계
- 문서 청킹 전략
- 임베딩 모델 선택 및 최적화
- LLM 통합 (OpenAI, Anthropic)
- 컨텍스트 윈도우 관리
- 답변 품질 평가

#### 실습 프로젝트
- 완전한 RAG 시스템 구현
- PDF/Markdown 문서 처리 파이프라인
- 대화형 Q&A 시스템
- 벡터 저장소 업데이트 자동화
- A/B 테스트 프레임워크

#### 핵심 코드
```python
# 05-real-project/rag/pipeline.py - RAG 파이프라인
# 05-real-project/rag/chunking.py - 문서 청킹
# 05-real-project/rag/embeddings.py - 임베딩 생성
# 05-real-project/rag/retrieval.py - 검색 최적화
# 05-real-project/rag/generation.py - LLM 통합
```

---

## 🚀 빠른 시작

### 사전 요구사항
- Python 3.9+
- Docker & Docker Compose
- 8GB+ RAM 권장

### 설치

```bash
# 1. 레포지토리 클론
git clone <repository-url>
cd qdrant-examples

# 2. 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. Qdrant 서버 실행
docker-compose up -d

# 5. 환경 변수 설정
cp .env.example .env
# .env 파일을 수정하여 필요한 API 키 등을 설정
```

### 단계별 학습 시작

각 단계별로 독립적인 README와 실습 자료가 제공됩니다:

```bash
# 단계 1부터 시작
cd 01-fundamentals
python examples/basic_operations.py

# 각 단계의 README를 따라 진행
cat README.md
```

## 📁 프로젝트 구조

```
qdrant-examples/
├── 01-fundamentals/          # 기초 개념 및 기본 작업
│   ├── core/                 # 핵심 라이브러리
│   ├── examples/             # 실습 예제
│   ├── tests/                # 단위 테스트
│   └── README.md
│
├── 02-vector-search/         # 벡터 검색 및 필터링
│   ├── search/               # 검색 알고리즘
│   ├── examples/             # 실습 예제
│   ├── tests/
│   └── README.md
│
├── 03-production-api/        # 프로덕션 API 서버
│   ├── app/                  # FastAPI 애플리케이션
│   ├── tests/
│   └── README.md
│
├── 04-optimization/          # 성능 최적화
│   ├── benchmarks/           # 벤치마크 도구
│   ├── caching/              # 캐싱 전략
│   ├── monitoring/           # 모니터링
│   └── README.md
│
├── 05-real-project/          # RAG 시스템 구현
│   ├── rag/                  # RAG 파이프라인
│   ├── api/                  # API 서버
│   ├── tests/
│   └── README.md
│
├── docker-compose.yml        # Qdrant 서버 설정
├── requirements.txt          # Python 의존성
└── README.md                 # 이 파일
```

## 🛠 기술 스택

### 핵심 기술
- **Qdrant**: 벡터 데이터베이스
- **Python 3.9+**: 주 개발 언어
- **FastAPI**: 고성능 웹 프레임워크
- **Pydantic**: 데이터 검증
- **Docker**: 컨테이너화

### 임베딩 및 ML
- **sentence-transformers**: 문장 임베딩
- **OpenAI API**: 고품질 임베딩 및 LLM
- **tiktoken**: 토큰 카운팅

### 프로덕션 도구
- **Redis**: 캐싱
- **Prometheus**: 메트릭 수집
- **Grafana**: 모니터링 대시보드
- **pytest**: 테스트 프레임워크
- **black/ruff**: 코드 포맷팅

## 🎓 학습 방법

### 추천 학습 순서
1. **순차 학습**: 1단계부터 5단계까지 순서대로 진행
2. **실습 중심**: 각 단계의 코드를 직접 실행하고 수정
3. **테스트 작성**: 학습한 내용을 테스트 코드로 검증
4. **문서 참조**: 각 단계의 README에서 상세 설명 확인

### 각 단계별 학습 팁
- ✅ 코드 실행 전 README 숙독
- ✅ 제공된 테스트 코드 분석
- ✅ 예제를 자신의 유스케이스에 맞게 수정
- ✅ 성능 메트릭 측정 및 비교
- ✅ 프로덕션 체크리스트 확인

## 📊 실무 활용 예시

### 유스케이스별 가이드
- **의미론적 검색**: 2단계 + 3단계
- **추천 시스템**: 2단계 + 4단계
- **챗봇/Q&A**: 5단계 전체
- **이미지 검색**: 1단계 + 2단계 (벡터 수정)
- **중복 탐지**: 2단계

## 🔍 베스트 프랙티스

### 프로덕션 체크리스트
- [ ] 적절한 벡터 차원 선택 (384, 768, 1536 등)
- [ ] HNSW 파라미터 튜닝 (m, ef_construct)
- [ ] 커넥션 풀링 설정
- [ ] 에러 핸들링 및 재시도 로직
- [ ] 로깅 및 모니터링 구현
- [ ] 백업 및 복구 전략
- [ ] 보안 설정 (API 키, 네트워크 격리)
- [ ] 부하 테스트 실행
- [ ] 문서화 (API docs, runbook)

## 🤝 기여 및 피드백

이 프로젝트는 지속적으로 업데이트됩니다. 개선 사항이나 버그는 이슈로 제보해주세요.

## 📝 라이센스

MIT License

## 🔗 참고 자료

- [Qdrant 공식 문서](https://qdrant.tech/documentation/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Vector Search 가이드](https://www.pinecone.io/learn/vector-search/)
- [RAG 패턴](https://arxiv.org/abs/2005.11401)

---

**마지막 업데이트**: 2025-12-01
**난이도**: 중급 ~ 고급
**추천 대상**: 백엔드 개발 경험 1년 이상, Python 숙련자
