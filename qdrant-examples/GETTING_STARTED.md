# 시작하기 가이드

> Qdrant 학습 프로젝트 빠른 시작

## 📋 사전 요구사항

### 필수 설치
- **Python 3.9 이상**
- **Docker & Docker Compose**
- **Git**

### 권장 사양
- RAM: 8GB 이상
- 디스크: 10GB 여유 공간
- OS: Linux, macOS, Windows (WSL2)

## 🚀 설치 및 실행

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd qdrant-examples
```

### 2. 가상환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 활성화 (Linux/macOS)
source venv/bin/activate

# 활성화 (Windows)
venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Qdrant 서버 실행

```bash
# Docker Compose로 모든 서비스 실행
docker-compose up -d

# 개별 서비스만 실행
docker-compose up -d qdrant      # Qdrant만
docker-compose up -d redis       # Redis만
```

### 5. 서버 확인

```bash
# Qdrant 헬스체크
curl http://localhost:6333/

# Qdrant 대시보드
# 브라우저에서 http://localhost:6333/dashboard 접속

# Redis 확인
docker-compose exec redis redis-cli ping
# 응답: PONG
```

### 6. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (필요한 API 키 설정)
nano .env  # 또는 원하는 에디터 사용
```

중요한 환경 변수:
```bash
# OpenAI API (RAG 프로젝트용)
OPENAI_API_KEY=sk-...

# Anthropic API (선택사항)
ANTHROPIC_API_KEY=sk-ant-...

# Qdrant 설정
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

## 📚 학습 순서

### 단계 1: 기초 학습 (2-3시간)

```bash
cd 01-fundamentals

# README 읽기
cat README.md

# 예제 1: 기본 연결
python examples/01_basic_connection.py

# 예제 2: 컬렉션 관리
python examples/02_collection_management.py

# 예제 3: CRUD 작업
python examples/03_vector_operations.py

# 예제 4: 배치 작업
python examples/04_batch_operations.py

# 예제 5: 에러 핸들링
python examples/05_error_handling.py
```

### 단계 2: 벡터 검색 (3-4시간)

```bash
cd 02-vector-search

cat README.md

# TODO: 예제 파일 실행
```

### 단계 3: API 서버 (4-5시간)

```bash
cd 03-production-api

# FastAPI 서버 실행
python app/main.py

# 또는 Uvicorn 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API 문서 확인
# http://localhost:8000/docs
```

### 단계 4: 최적화 (4-5시간)

```bash
cd 04-optimization

# 벤치마크 실행
python benchmarks/search_benchmark.py
```

### 단계 5: RAG 프로젝트 (6-8시간)

```bash
cd 05-real-project

# RAG 파이프라인 테스트
python rag/pipeline.py
```

## 🛠 문제 해결

### Qdrant 연결 실패

```bash
# Qdrant 컨테이너 로그 확인
docker-compose logs qdrant

# 포트 충돌 확인
lsof -i :6333  # Linux/macOS
netstat -ano | findstr :6333  # Windows

# Qdrant 재시작
docker-compose restart qdrant
```

### Python 패키지 오류

```bash
# pip 업그레이드
pip install --upgrade pip

# 의존성 재설치
pip install -r requirements.txt --force-reinstall

# 캐시 클리어
pip cache purge
```

### Docker 메모리 부족

```bash
# Docker 메모리 설정 확인
docker info | grep Memory

# Docker Desktop에서 메모리 증가 (8GB 권장)
# Settings > Resources > Memory
```

## 📖 추가 학습 자료

### 공식 문서
- [Qdrant 문서](https://qdrant.tech/documentation/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Pydantic 문서](https://docs.pydantic.dev/)

### 추천 블로그
- [Qdrant 블로그](https://qdrant.tech/blog/)
- [Vector Search 가이드](https://www.pinecone.io/learn/)

### 커뮤니티
- [Qdrant Discord](https://discord.gg/qdrant)
- [GitHub Issues](https://github.com/qdrant/qdrant/issues)

## 💡 팁

### 개발 환경 설정

```bash
# pre-commit 훅 설치 (선택사항)
pre-commit install

# 코드 포맷팅
black .

# 린팅
ruff check .

# 타입 체크
mypy .
```

### 효율적인 학습

1. **순차 학습**: 1단계부터 차례대로 진행
2. **코드 수정**: 예제를 자신의 상황에 맞게 변경
3. **테스트 작성**: 학습한 내용을 테스트로 검증
4. **문서 참조**: 막힐 때는 공식 문서 확인

### 실습 프로젝트 아이디어

- 개인 문서 검색 시스템
- 제품 추천 엔진
- 코드 검색 도구
- FAQ 챗봇

## 🔍 자주 묻는 질문

**Q: Qdrant vs Pinecone vs Weaviate?**
A: Qdrant는 오픈소스이며 셀프호스팅 가능. Pinecone은 관리형 서비스. Weaviate는 GraphQL 지원.

**Q: 무료로 사용 가능한가?**
A: Qdrant는 완전 오픈소스로 무료 사용 가능. Qdrant Cloud는 유료.

**Q: 프로덕션 배포는?**
A: Docker Compose, Kubernetes, Qdrant Cloud 등 다양한 옵션.

**Q: 벡터 차원은 어떻게 선택?**
A: 임베딩 모델에 따라 결정. sentence-transformers는 384/768, OpenAI는 1536.

## 📞 도움 받기

문제가 해결되지 않으면:

1. [GitHub Issues](https://github.com/<your-repo>/issues) 검색
2. 새 이슈 생성 (버그 리포트/기능 요청)
3. [Qdrant Discord](https://discord.gg/qdrant) 질문

---

즐거운 학습 되세요! 🚀
