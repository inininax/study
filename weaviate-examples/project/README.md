# 실전 프로젝트: 지능형 문서 검색 시스템 🚀

## 프로젝트 개요

Weaviate를 활용한 **프로덕션 레벨**의 백엔드 애플리케이션입니다.

### 주요 기능

- 📄 문서 업로드 및 자동 벡터화
- 🔍 고급 검색 (벡터, 키워드, 하이브리드)
- 🤖 RAG 기반 Q&A 시스템
- 👥 다중 사용자 지원
- 🔐 JWT 인증 및 권한 관리
- 📊 검색 분석 및 로깅
- 🧪 포괄적인 테스트

### 기술 스택

- **Backend**: FastAPI
- **Database**: Weaviate (벡터 DB)
- **Auth**: JWT
- **AI**: OpenAI (임베딩, LLM)
- **Testing**: Pytest
- **Deployment**: Docker

## 프로젝트 구조

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 애플리케이션
│   ├── config.py               # 설정 관리
│   ├── models/                 # 데이터 모델
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── document.py
│   ├── services/               # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── weaviate_service.py
│   │   ├── auth_service.py
│   │   └── rag_service.py
│   ├── api/                    # API 라우터
│   │   ├── __init__.py
│   │   ├── documents.py
│   │   ├── search.py
│   │   └── auth.py
│   └── utils/                  # 유틸리티
│       ├── __init__.py
│       ├── logger.py
│       └── exceptions.py
├── tests/                      # 테스트
│   ├── __init__.py
│   ├── test_documents.py
│   └── test_search.py
├── docker-compose.yml          # Docker 설정
├── requirements.txt
└── README.md
```

## 빠른 시작

### 1. 환경 설정

```bash
cd project

# 환경 변수 설정
cp ../.env.example .env
# .env 파일 편집하여 API 키 입력
```

### 2. Docker로 실행

```bash
# Weaviate와 GUI Console 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

**접속 URL:**
- 🗄️ Weaviate API: http://localhost:8080
- 🎨 Weaviate Console (GUI): http://localhost:8081
- 📊 FastAPI Docs: http://localhost:8000/docs (다음 단계 후)

### 3. 애플리케이션 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 개발 서버 시작
uvicorn app.main:app --reload

# 브라우저에서 열기
# http://localhost:8000/docs (Swagger UI)
```

## API 엔드포인트

### 인증 (Auth)

```http
POST /api/auth/register       # 회원가입
POST /api/auth/login          # 로그인
GET  /api/auth/me             # 내 정보
```

### 문서 (Documents)

```http
POST   /api/documents              # 문서 업로드
GET    /api/documents              # 문서 목록
GET    /api/documents/{id}         # 문서 조회
PUT    /api/documents/{id}         # 문서 수정
DELETE /api/documents/{id}         # 문서 삭제
```

### 검색 (Search)

```http
POST /api/search/semantic          # 의미 검색
POST /api/search/keyword           # 키워드 검색
POST /api/search/hybrid            # 하이브리드 검색
POST /api/search/qa                # RAG 기반 Q&A
```

## 사용 예제

### 1. 문서 업로드

```bash
curl -X POST "http://localhost:8000/api/documents" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weaviate 소개",
    "content": "Weaviate는 오픈소스 벡터 데이터베이스입니다...",
    "tags": ["AI", "Database"]
  }'
```

### 2. 의미 검색

```bash
curl -X POST "http://localhost:8000/api/search/semantic" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "벡터 데이터베이스란?",
    "limit": 5
  }'
```

### 3. RAG Q&A

```bash
curl -X POST "http://localhost:8000/api/search/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Weaviate의 주요 특징은?"
  }'
```

## 테스트

```bash
# 모든 테스트 실행
pytest

# 커버리지 포함
pytest --cov=app

# 특정 테스트만
pytest tests/test_search.py
```

## 배포

### Docker로 배포

```bash
# 이미지 빌드
docker build -t weaviate-app .

# 컨테이너 실행
docker run -p 8000:8000 weaviate-app
```

### 프로덕션 체크리스트

- [ ] 환경 변수 보안
- [ ] HTTPS 설정
- [ ] 로깅 설정
- [ ] 에러 모니터링
- [ ] 성능 최적화
- [ ] 백업 전략
- [ ] CI/CD 파이프라인

## 학습 목표

이 프로젝트를 완료하면:

✅ FastAPI로 RESTful API 개발
✅ Weaviate 실무 활용
✅ RAG 패턴 구현
✅ 인증/권한 관리
✅ 테스트 작성
✅ Docker 배포

## 다음 단계

1. 코드 분석 및 이해
2. 기능 추가 및 커스터마이징
3. 자신만의 프로젝트로 확장

## 참고 자료

- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Weaviate 문서](https://weaviate.io/developers/weaviate)
- [OpenAI API](https://platform.openai.com/docs/)
