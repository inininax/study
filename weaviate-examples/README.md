# Weaviate 학습 프로젝트 🚀

> Python 초보자를 위한 체계적인 Weaviate 학습 커리큘럼과 실무 수준의 프로젝트

## 📚 프로젝트 개요

이 프로젝트는 벡터 데이터베이스 **Weaviate**를 처음부터 배워 실무 수준의 백엔드 애플리케이션을 개발할 수 있도록 설계된 종합 학습 자료입니다.

### 🎯 학습 목표

- Weaviate의 핵심 개념과 벡터 데이터베이스 이해
- Python을 통한 Weaviate 클라이언트 조작
- 벡터 검색, 하이브리드 검색 등 고급 검색 기술 습득
- RAG (Retrieval Augmented Generation) 패턴 구현
- 실무 환경에서 바로 사용 가능한 백엔드 애플리케이션 개발

## 🗂️ 프로젝트 구조

```
weaviate-examples/
├── README.md                    # 프로젝트 개요
├── requirements.txt             # Python 의존성
├── .env.example                 # 환경 변수 템플릿
├── docs/                        # 학습 문서
│   ├── curriculum.md            # 전체 커리큘럼
│   ├── setup.md                 # 환경 설정 가이드
│   └── concepts.md              # Weaviate 핵심 개념
├── lessons/                     # 단계별 학습 모듈
│   ├── 01-basics/              # 초급: 기본 개념과 CRUD
│   ├── 02-intermediate/        # 중급: 벡터 검색과 필터링
│   └── 03-advanced/            # 고급: RAG, 멀티테넌시, 최적화
├── project/                     # 실전 프로젝트
│   ├── app/                    # FastAPI 백엔드 애플리케이션
│   ├── tests/                  # 테스트 코드
│   └── docker-compose.yml      # Docker 설정
└── utils/                       # 공통 유틸리티
```

## 🚀 빠른 시작

### 1. 환경 설정

#### 방법 1: pip 사용

```bash
# 저장소 클론
git clone <repository-url>
cd weaviate-examples

# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 필요한 API 키 입력
```

#### 방법 2: uv 사용 (권장 - 빠른 속도)

```bash
# 저장소 클론
git clone <repository-url>
cd weaviate-examples

# uv 설치 (아직 설치하지 않은 경우)
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows:
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 가상 환경 생성 및 의존성 설치
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 필요한 API 키 입력
```

### 2. Weaviate 실행 (Docker 사용)

```bash
cd project
docker-compose up -d

# Weaviate와 GUI Console이 모두 시작됩니다
# - Weaviate: http://localhost:8080
# - Weaviate Console (GUI): http://localhost:8081
```

### 3. GUI로 데이터 확인 🎨

**Weaviate Console**에서 데이터를 시각적으로 확인할 수 있습니다:

```
브라우저에서 접속: http://localhost:8081

주요 기능:
✅ 스키마(컬렉션) 탐색
✅ 저장된 데이터 브라우징
✅ GraphQL 쿼리 테스트
✅ 벡터 검색 실험
```

> 📝 GUI 클라이언트 자세한 가이드: [docs/gui-clients.md](docs/gui-clients.md)

### 4. 학습 시작

```bash
# 초급 모듈부터 시작
cd lessons/01-basics
python 01_connection.py
```

## 📖 학습 커리큘럼

### 🟢 초급 (Basics) - 1-2주

1. **Weaviate 연결** (`lessons/01-basics/01_connection.py`)
   - 클라이언트 설정 및 연결
   - 헬스 체크 및 메타데이터 조회

2. **스키마 정의** (`lessons/01-basics/02_schema.py`)
   - 컬렉션(클래스) 생성
   - 속성(Properties) 정의
   - 벡터화(Vectorization) 설정

3. **CRUD 작업** (`lessons/01-basics/03_crud.py`)
   - 데이터 생성 (Create)
   - 데이터 읽기 (Read)
   - 데이터 수정 (Update)
   - 데이터 삭제 (Delete)

4. **배치 작업** (`lessons/01-basics/04_batch_operations.py`)
   - 대량 데이터 삽입
   - 성능 최적화

### 🟡 중급 (Intermediate) - 2-3주

1. **벡터 검색** (`lessons/02-intermediate/01_vector_search.py`)
   - Semantic Search (의미론적 검색)
   - Near Text / Near Vector 쿼리
   - 유사도 측정

2. **하이브리드 검색** (`lessons/02-intermediate/02_hybrid_search.py`)
   - BM25 + 벡터 검색 결합
   - 알파 파라미터 조정

3. **필터링** (`lessons/02-intermediate/03_filters.py`)
   - Where 필터
   - 복합 조건
   - 범위 검색

4. **집계 쿼리** (`lessons/02-intermediate/04_aggregations.py`)
   - 그룹화 및 집계
   - 통계 정보 추출

### 🔴 고급 (Advanced) - 3-4주

1. **RAG 구현** (`lessons/03-advanced/01_rag_implementation.py`)
   - LLM과 벡터 DB 통합
   - 컨텍스트 기반 응답 생성
   - 프롬프트 엔지니어링

2. **멀티테넌시** (`lessons/03-advanced/02_multi_tenancy.py`)
   - 테넌트 관리
   - 데이터 격리
   - 확장성 패턴

3. **성능 최적화** (`lessons/03-advanced/03_performance_optimization.py`)
   - 인덱싱 전략
   - 쿼리 최적화
   - 캐싱 전략

4. **모니터링** (`lessons/03-advanced/04_monitoring.py`)
   - 메트릭 수집
   - 로깅 전략
   - 에러 핸들링

### 🏆 실전 프로젝트 - 2-3주

**지능형 문서 검색 시스템**

완전한 기능을 갖춘 백엔드 애플리케이션:
- FastAPI 기반 RESTful API
- 문서 업로드 및 벡터화
- 고급 검색 기능
- RAG 기반 Q&A
- 사용자 인증 및 권한 관리
- 프로덕션 레벨 에러 핸들링
- 포괄적인 테스트
- Docker 배포

## 🛠️ 사용 기술

- **Weaviate**: 벡터 데이터베이스
- **Python 3.10+**: 프로그래밍 언어
- **FastAPI**: 웹 프레임워크
- **OpenAI**: 임베딩 생성
- **Docker**: 컨테이너화
- **Pytest**: 테스트 프레임워크

## 📝 학습 방법

1. **순차적 학습**: 초급 → 중급 → 고급 순서로 진행
2. **실습 중심**: 각 예제 코드를 직접 실행하고 수정해보기
3. **주석 읽기**: 코드 내 상세한 한글 주석으로 개념 이해
4. **프로젝트 적용**: 배운 내용을 실전 프로젝트에 적용

## 🤝 기여하기

이슈나 개선 사항이 있다면 언제든 Pull Request를 보내주세요!

## 📄 라이선스

MIT License

## 📞 문의

질문이나 피드백은 이슈를 통해 남겨주세요.

---

**Happy Learning! 🎓**
