# Weaviate 학습 커리큘럼 🎓

## 전체 개요

이 커리큘럼은 **Python 초보자**가 **백엔드 전문가 수준**의 Weaviate 애플리케이션을 개발할 수 있도록 설계되었습니다.

### 학습 기간
- **초급**: 1-2주 (기초 다지기)
- **중급**: 2-3주 (실력 향상)
- **고급**: 3-4주 (전문가 되기)
- **프로젝트**: 2-3주 (실전 경험)

**총 예상 기간: 8-12주**

## 레벨별 상세 커리큘럼

### 🟢 레벨 1: 초급 (Basics)

**목표**: Weaviate의 기본 개념과 CRUD 작업 마스터

#### 1주차: 환경 설정 및 기본 개념
- [ ] Python 가상 환경 설정
- [ ] Docker 및 Weaviate 설치
- [ ] Weaviate 핵심 개념 학습
  - 벡터란 무엇인가?
  - 임베딩의 이해
  - 컬렉션과 객체
- [ ] 첫 Weaviate 클라이언트 연결

**학습 자료**:
- `docs/setup.md`
- `docs/concepts.md`
- `lessons/01-basics/01_connection.py`

#### 2주차: 스키마 및 CRUD
- [ ] 스키마(컬렉션) 생성
- [ ] 속성(Properties) 정의
- [ ] 벡터화 설정 이해
- [ ] Create: 객체 생성
- [ ] Read: 객체 조회
- [ ] Update: 객체 수정
- [ ] Delete: 객체 삭제
- [ ] 배치 작업으로 대량 데이터 처리

**학습 자료**:
- `lessons/01-basics/02_schema.py`
- `lessons/01-basics/03_crud.py`
- `lessons/01-basics/04_batch_operations.py`

**체크포인트**:
- ✅ Weaviate에 연결할 수 있다
- ✅ 컬렉션을 생성하고 관리할 수 있다
- ✅ 기본 CRUD 작업을 수행할 수 있다
- ✅ 배치 작업의 성능 이점을 이해한다

---

### 🟡 레벨 2: 중급 (Intermediate)

**목표**: 벡터 검색과 고급 쿼리 기법 습득

#### 3-4주차: 벡터 검색
- [ ] Near Text: 의미론적 검색
- [ ] Near Vector: 벡터 직접 사용
- [ ] Near Object: 유사 객체 찾기
- [ ] 거리 측정 및 확신도 이해
- [ ] 검색 결과 평가 및 튜닝

**학습 자료**:
- `lessons/02-intermediate/01_vector_search.py`

**실습 프로젝트**:
- 영화 추천 시스템 만들기
- 유사 문서 검색 엔진

#### 5주차: 하이브리드 검색 및 필터링
- [ ] BM25 키워드 검색
- [ ] 하이브리드 검색 (벡터 + 키워드)
- [ ] 알파 파라미터 조정
- [ ] Where 필터
- [ ] 복합 조건 (AND, OR, NOT)
- [ ] 범위 검색

**학습 자료** (작성 예정):
- `lessons/02-intermediate/02_hybrid_search.py` (예정)
- `lessons/02-intermediate/03_filters.py` (예정)

#### 6주차: 집계 및 분석
- [ ] 그룹화 (Group By)
- [ ] 집계 함수 (Count, Sum, Avg)
- [ ] 통계 추출
- [ ] 메타 분석

**학습 자료** (작성 예정):
- `lessons/02-intermediate/04_aggregations.py` (예정)

**체크포인트**:
- ✅ 의미론적 검색과 키워드 검색의 차이를 이해한다
- ✅ 하이브리드 검색으로 최적의 결과를 얻을 수 있다
- ✅ 복잡한 필터 쿼리를 작성할 수 있다
- ✅ 데이터 분석 쿼리를 실행할 수 있다

---

### 🔴 레벨 3: 고급 (Advanced)

**목표**: RAG 구현 및 프로덕션 패턴 학습

#### 7-8주차: RAG 구현
- [ ] RAG (Retrieval Augmented Generation) 개념
- [ ] 문서 검색 + LLM 통합
- [ ] 프롬프트 엔지니어링
- [ ] 컨텍스트 최적화
- [ ] 답변 품질 개선

**학습 자료**:
- `lessons/03-advanced/01_rag_implementation.py` (작성 예정)

**실습 프로젝트**:
- 문서 기반 Q&A 챗봇
- 지식베이스 검색 시스템

#### 9주차: 멀티테넌시 및 확장성
- [ ] 멀티테넌트 아키텍처
- [ ] 테넌트 관리
- [ ] 데이터 격리
- [ ] 수평 확장 (Sharding)
- [ ] 복제 (Replication)

**학습 자료**:
- `lessons/03-advanced/02_multi_tenancy.py` (작성 예정)

#### 10주차: 성능 최적화
- [ ] 인덱싱 전략
- [ ] 쿼리 최적화
- [ ] 캐싱 전략
- [ ] 벡터 압축
- [ ] 모니터링 및 로깅
- [ ] 에러 핸들링

**학습 자료**:
- `lessons/03-advanced/03_performance_optimization.py` (작성 예정)
- `lessons/03-advanced/04_monitoring.py` (작성 예정)

**체크포인트**:
- ✅ RAG 패턴을 구현하고 LLM과 통합할 수 있다
- ✅ 멀티테넌트 시스템을 설계할 수 있다
- ✅ 성능 병목을 찾고 최적화할 수 있다
- ✅ 프로덕션 레벨의 에러 핸들링을 구현할 수 있다

---

### 🏆 레벨 4: 실전 프로젝트

**목표**: 완전한 기능을 갖춘 백엔드 애플리케이션 개발

#### 11-12주차: 지능형 문서 검색 시스템 구축

**프로젝트 스펙**:
- ✅ FastAPI 기반 RESTful API
- ✅ 문서 업로드 및 자동 벡터화
- ✅ 다양한 검색 방식 (의미, 키워드, 하이브리드)
- ✅ RAG 기반 Q&A 시스템
- ✅ JWT 인증 및 권한 관리
- ✅ 입력 검증 및 에러 핸들링
- ✅ 구조화된 로깅
- ✅ 포괄적인 테스트
- ✅ Docker 배포
- ✅ API 문서화 (Swagger)

**프로젝트 구조**:
```
project/
├── app/
│   ├── main.py              # FastAPI 앱
│   ├── config.py            # 설정 관리
│   ├── models/              # Pydantic 모델
│   ├── services/            # 비즈니스 로직
│   ├── api/                 # API 라우터
│   └── utils/               # 유틸리티
├── tests/                   # 테스트
└── docker-compose.yml       # Docker 설정
```

**단계별 개발**:

1. **1-2일차: 프로젝트 설정**
   - [ ] FastAPI 프로젝트 초기화
   - [ ] Weaviate 연결 설정
   - [ ] 기본 구조 생성

2. **3-4일차: 문서 관리 API**
   - [ ] 문서 CRUD 엔드포인트
   - [ ] Pydantic 모델 정의
   - [ ] 입력 검증

3. **5-6일차: 검색 API**
   - [ ] 의미 검색 엔드포인트
   - [ ] 하이브리드 검색 엔드포인트
   - [ ] 필터링 지원

4. **7-8일차: RAG Q&A**
   - [ ] OpenAI LLM 통합
   - [ ] 컨텍스트 생성
   - [ ] 프롬프트 최적화

5. **9-10일차: 인증 및 보안**
   - [ ] JWT 토큰 발급
   - [ ] 엔드포인트 보호
   - [ ] 권한 관리

6. **11-12일차: 테스트 및 배포**
   - [ ] 단위 테스트
   - [ ] 통합 테스트
   - [ ] Docker 이미지 빌드
   - [ ] 배포 문서 작성

**학습 자료**:
- `project/README.md`
- `project/app/`
- `project/tests/`

**최종 체크포인트**:
- ✅ 프로덕션 레벨의 API를 개발할 수 있다
- ✅ 인증 및 권한을 관리할 수 있다
- ✅ 테스트를 작성하고 실행할 수 있다
- ✅ Docker로 애플리케이션을 배포할 수 있다
- ✅ API 문서를 작성할 수 있다

---

## 학습 방법론

### 1. 순차적 학습
- 반드시 **순서대로** 학습하세요
- 각 단계의 체크포인트를 완료한 후 다음으로 진행

### 2. 실습 중심
- 모든 예제 코드를 **직접 실행**
- 값을 바꿔가며 **실험**
- 에러를 만나면 **직접 해결** 시도

### 3. 프로젝트 기반
- 배운 내용을 **즉시 적용**
- 작은 프로젝트부터 시작
- 점진적으로 기능 확장

### 4. 문서화 습관
- 코드에 **주석** 작성
- README 파일 작성
- 학습 내용 **정리**

## 추가 리소스

### 공식 문서
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [Python Client](https://weaviate.io/developers/weaviate/client-libraries/python)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

### 커뮤니티
- [Weaviate Slack](https://weaviate.io/slack)
- [GitHub Discussions](https://github.com/weaviate/weaviate/discussions)

### 연습 프로젝트 아이디어
1. **블로그 검색 엔진**: 블로그 글 검색
2. **코드 검색 도구**: 코드 스니펫 검색
3. **레시피 추천**: 재료 기반 레시피 검색
4. **FAQ 챗봇**: 고객 지원 챗봇
5. **논문 검색**: 학술 논문 검색 및 요약

## 성공을 위한 팁

1. **꾸준함**: 매일 1-2시간씩 학습
2. **질문하기**: 막히면 커뮤니티에 질문
3. **코드 리뷰**: 다른 사람의 코드 읽기
4. **실전 경험**: 개인 프로젝트 진행
5. **최신 정보**: Weaviate 블로그 팔로우

## 수료 후 경로

### 주니어 백엔드 개발자
- Weaviate 활용 API 개발
- 검색 시스템 구축
- 데이터 파이프라인 설계

### AI 애플리케이션 개발자
- RAG 시스템 구축
- AI 에이전트 개발
- 지식 관리 시스템

### 데이터 엔지니어
- 벡터 DB 설계
- 성능 최적화
- 대규모 시스템 운영

---

**이제 시작하세요! 🚀**

👉 [환경 설정부터 시작](./setup.md)
