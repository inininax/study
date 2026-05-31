# Weaviate GUI 클라이언트 가이드 🖥️

## 추천 #1: Weaviate Console (공식, 가장 추천!)

**가장 많이 사용되고 공식 지원되는 GUI 도구**입니다.

### 설치 및 실행

#### 방법 1: Docker Compose에 추가 (권장)

`project/docker-compose.yml` 파일을 업데이트:

```yaml
version: '3.8'

services:
  weaviate:
    image: semitechnologies/weaviate:1.23.0
    container_name: weaviate
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "50051:50051"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'text2vec-openai'
      ENABLE_MODULES: 'text2vec-openai,generative-openai'
      OPENAI_APIKEY: ${OPENAI_API_KEY}
      CLUSTER_HOSTNAME: 'node1'
      LOG_LEVEL: 'info'
    volumes:
      - weaviate_data:/var/lib/weaviate
    networks:
      - weaviate_network

  # Weaviate Console 추가 ✨
  weaviate-console:
    image: semitechnologies/weaviate-console:latest
    container_name: weaviate-console
    restart: unless-stopped
    ports:
      - "8081:80"
    environment:
      - WEAVIATE_URL=http://weaviate:8080
    depends_on:
      - weaviate
    networks:
      - weaviate_network

volumes:
  weaviate_data:
    driver: local

networks:
  weaviate_network:
    driver: bridge
```

#### 실행

```bash
cd project
docker-compose down
docker-compose up -d

# 로그 확인
docker-compose logs -f weaviate-console
```

#### 접속

브라우저에서 **http://localhost:8081** 접속

### 주요 기능

✅ **스키마 탐색**: 모든 컬렉션과 속성 시각화
✅ **데이터 브라우징**: 객체 목록 및 상세 정보
✅ **쿼리 실행**: GraphQL 쿼리 실행 및 결과 확인
✅ **검색 테스트**: Near Text, Near Vector 등 검색 테스트
✅ **실시간 업데이트**: 데이터 변경 즉시 반영

---

## 추천 #2: Weaviate Cloud Console

**클라우드 기반, 설치 불필요**

### 접속 방법

1. https://console.weaviate.cloud/ 접속
2. 로컬 Weaviate에 연결:
   - Weaviate URL: `http://localhost:8080`
   - API Key: (없으면 비워두기)

### 특징

✅ 설치 불필요
✅ 깔끔한 UI
✅ 실시간 쿼리 테스트
❌ 로컬 환경에서 접근 제한 있을 수 있음

---

## 추천 #3: GraphiQL (GraphQL 쿼리 도구)

**Weaviate의 GraphQL API를 직접 탐색**

### Docker Compose에 추가

```yaml
  graphiql:
    image: graphql/graphiql:latest
    container_name: weaviate-graphiql
    restart: unless-stopped
    ports:
      - "8082:8080"
    environment:
      - GRAPHQL_ENDPOINT=http://weaviate:8080/v1/graphql
    depends_on:
      - weaviate
    networks:
      - weaviate_network
```

### 접속

**http://localhost:8082**

### 예제 쿼리

```graphql
# 모든 컬렉션 조회
{
  Get {
    Document(limit: 10) {
      title
      content
      tags
      created_at
    }
  }
}

# Near Text 검색
{
  Get {
    Document(
      nearText: {
        concepts: ["AI 기술"]
      }
      limit: 5
    ) {
      title
      content
      _additional {
        distance
        certainty
      }
    }
  }
}
```

---

## 비교표

| 도구 | 설치 | UI | 기능 | 추천도 |
|------|------|----|----|-------|
| **Weaviate Console** | Docker | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🏆 최고 |
| **Cloud Console** | 불필요 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **GraphiQL** | Docker | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Postman** | 앱 설치 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 💡 추천 조합

### 개발 환경

1. **Weaviate Console** (메인 GUI)
   - 데이터 탐색 및 디버깅
   - 스키마 확인

2. **FastAPI Swagger UI** (API 테스트)
   - http://localhost:8000/docs
   - REST API 테스트

3. **Python 스크립트** (자동화)
   - 대량 데이터 확인
   - 스크립트 기반 분석

---

## 🚀 빠른 시작: Weaviate Console 설정

### 1. docker-compose.yml 업데이트

```bash
cd project
```

기존 `docker-compose.yml`에 console 서비스 추가 (위 코드 참고)

### 2. 재시작

```bash
docker-compose down
docker-compose up -d
```

### 3. 접속 확인

```bash
# 콘솔 로그 확인
docker-compose logs weaviate-console

# 브라우저에서 접속
# http://localhost:8081
```

### 4. 사용 방법

1. 왼쪽 메뉴에서 **Schema** 클릭
   - 모든 컬렉션 확인
   - 속성 및 벡터 설정 확인

2. **Data** 탭 클릭
   - 저장된 객체 브라우징
   - 개별 객체 상세 정보

3. **Query** 탭 클릭
   - GraphQL 쿼리 작성 및 실행
   - 검색 테스트

4. **Monitoring** 탭 클릭
   - 성능 메트릭
   - 리소스 사용량

---

## 📱 모바일 대안

모바일에서는 **Weaviate Cloud Console** 웹 버전 사용 권장

---

## 🔧 문제 해결

### Console에 연결되지 않을 때

```bash
# 1. Weaviate가 실행 중인지 확인
docker ps | grep weaviate

# 2. 네트워크 확인
docker network ls | grep weaviate

# 3. Console 재시작
docker-compose restart weaviate-console

# 4. 로그 확인
docker-compose logs weaviate-console
```

### 데이터가 보이지 않을 때

```bash
# Weaviate 접속 테스트
curl http://localhost:8080/v1/meta

# 스키마 확인
curl http://localhost:8080/v1/schema
```

---

## 🎯 결론

### 최종 추천: Weaviate Console 🏆

**이유:**
1. ✅ 공식 지원 도구
2. ✅ 가장 많은 기능
3. ✅ 직관적인 UI
4. ✅ Docker로 쉬운 설치
5. ✅ 실시간 데이터 확인
6. ✅ GraphQL 쿼리 테스트
7. ✅ 무료

**설치 한 줄 요약:**
```bash
# docker-compose.yml에 console 추가 → docker-compose up -d → http://localhost:8081 접속
```

---

## 📚 참고 자료

- [Weaviate Console 문서](https://weaviate.io/developers/weaviate/tools/console)
- [GraphQL 쿼리 가이드](https://weaviate.io/developers/weaviate/api/graphql)
- [Weaviate Cloud Console](https://console.weaviate.cloud/)
