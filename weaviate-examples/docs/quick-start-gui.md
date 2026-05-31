# Weaviate Console 빠른 시작 가이드 🎨

## 5분 안에 GUI로 Weaviate 탐색하기

### 1단계: Weaviate와 Console 실행 (1분)

```bash
cd project
docker-compose up -d
```

**실행 확인:**
```bash
docker ps

# 다음 2개의 컨테이너가 실행 중이어야 합니다:
# - weaviate
# - weaviate-console
```

### 2단계: Console 접속 (10초)

브라우저에서 **http://localhost:8081** 접속

### 3단계: 첫 화면 이해 (1분)

Console에 접속하면 다음과 같은 메뉴가 보입니다:

```
┌─────────────────────────────────────┐
│ Weaviate Console                    │
├─────────────────────────────────────┤
│ 📋 Schema      - 스키마 확인         │
│ 📊 Data        - 데이터 탐색         │
│ 🔍 Query       - 쿼리 실행           │
│ 📈 Monitoring  - 성능 모니터링       │
└─────────────────────────────────────┘
```

### 4단계: 샘플 데이터 생성 (2분)

**터미널에서 실행:**
```bash
cd ../lessons/01-basics
python 01_connection.py
python 02_schema.py
python 03_crud.py
```

이제 Console에 데이터가 보입니다! 🎉

---

## 주요 기능 사용법

### 📋 Schema 탭 - 스키마 확인

**무엇을 할 수 있나요?**
- ✅ 모든 컬렉션(클래스) 목록 보기
- ✅ 각 컬렉션의 속성(Properties) 확인
- ✅ 벡터 설정 확인
- ✅ 인덱스 구성 확인

**사용 예시:**

1. 왼쪽 메뉴에서 **Schema** 클릭
2. `Article` 컬렉션 클릭
3. 다음 정보 확인:
   ```
   Collection: Article

   Properties:
   - title (TEXT)
   - content (TEXT)
   - author (TEXT)
   - published_date (DATE)
   - views (INT)
   - tags (TEXT_ARRAY)

   Vectorizer: text2vec-openai
   Model: text-embedding-3-small
   ```

---

### 📊 Data 탭 - 데이터 탐색

**무엇을 할 수 있나요?**
- ✅ 저장된 모든 객체 브라우징
- ✅ 개별 객체 상세 정보 확인
- ✅ UUID 및 메타데이터 확인
- ✅ 벡터 값 확인

**사용 예시:**

1. **Data** 탭 클릭
2. 컬렉션 선택: `Article`
3. 객체 목록이 표시됨:
   ```
   [1] Weaviate 벡터 데이터베이스 소개
       Author: 홍길동
       Views: 0
       UUID: abc123...

   [2] Python으로 시작하는 AI 개발
       Author: 김개발
       Views: 150
       UUID: def456...
   ```
4. 객체 클릭하면 상세 정보 표시:
   ```json
   {
     "id": "abc123...",
     "properties": {
       "title": "Weaviate 벡터 데이터베이스 소개",
       "content": "Weaviate는 오픈소스...",
       "author": "홍길동",
       "published_date": "2024-01-15T10:00:00Z",
       "views": 0,
       "tags": ["AI", "데이터베이스", "벡터검색"]
     },
     "vector": [0.123, -0.456, 0.789, ...]
   }
   ```

---

### 🔍 Query 탭 - GraphQL 쿼리

**무엇을 할 수 있나요?**
- ✅ GraphQL 쿼리 작성 및 실행
- ✅ Near Text 검색 테스트
- ✅ 필터 조건 실험
- ✅ 결과 실시간 확인

**기본 쿼리 예시:**

#### 1. 모든 문서 조회
```graphql
{
  Get {
    Article(limit: 10) {
      title
      author
      views
    }
  }
}
```

**결과:**
```json
{
  "data": {
    "Get": {
      "Article": [
        {
          "title": "Weaviate 벡터 데이터베이스 소개",
          "author": "홍길동",
          "views": 0
        }
      ]
    }
  }
}
```

#### 2. 의미 검색 (Near Text)
```graphql
{
  Get {
    Article(
      nearText: {
        concepts: ["AI 기술"]
      }
      limit: 5
    ) {
      title
      author
      _additional {
        distance
        certainty
      }
    }
  }
}
```

**결과:**
```json
{
  "data": {
    "Get": {
      "Article": [
        {
          "title": "Python으로 시작하는 AI 개발",
          "author": "김개발",
          "_additional": {
            "distance": 0.123,
            "certainty": 0.877
          }
        }
      ]
    }
  }
}
```

#### 3. 필터 검색
```graphql
{
  Get {
    Article(
      where: {
        path: ["views"]
        operator: GreaterThan
        valueInt: 100
      }
      limit: 10
    ) {
      title
      views
    }
  }
}
```

#### 4. 하이브리드 검색
```graphql
{
  Get {
    Article(
      hybrid: {
        query: "벡터 데이터베이스"
        alpha: 0.5
      }
      limit: 5
    ) {
      title
      _additional {
        score
      }
    }
  }
}
```

---

### 📈 Monitoring 탭 - 성능 모니터링

**무엇을 할 수 있나요?**
- ✅ 쿼리 성능 확인
- ✅ 메모리 사용량 모니터링
- ✅ 벡터 인덱스 상태 확인
- ✅ 처리량(Throughput) 측정

**주요 메트릭:**
```
Objects: 15
Collections: 3
Vector Dimensions: 1536
Memory Usage: 245 MB
Query Latency: 23ms (avg)
```

---

## 실전 워크플로우

### 시나리오: 새 문서 추가 후 확인

**1. Python으로 문서 추가**
```python
# lessons/01-basics/03_crud.py 실행
python 03_crud.py
```

**2. Console에서 즉시 확인**
- **Data** 탭 → `Article` 선택
- 새로 추가된 문서 확인
- UUID 복사

**3. 검색 테스트**
- **Query** 탭으로 이동
- Near Text 쿼리 실행
- 새 문서가 검색되는지 확인

**4. 벡터 확인**
- 문서 클릭
- `vector` 필드에서 1536차원 벡터 확인

---

## 유용한 팁 💡

### 팁 1: 실시간 새로고침
Console은 자동으로 데이터를 새로고침하지 않습니다.
- 브라우저 새로고침(F5) 또는
- 탭 재클릭으로 업데이트

### 팁 2: 쿼리 저장
자주 사용하는 쿼리는 별도 파일에 저장:
```bash
# queries.graphql
query GetAllArticles {
  Get {
    Article(limit: 10) {
      title
    }
  }
}
```

### 팁 3: 에러 디버깅
쿼리 실패시 Console에 에러 메시지 표시:
```json
{
  "errors": [
    {
      "message": "Collection 'Article' does not exist"
    }
  ]
}
```

### 팁 4: 벡터 검색 실험
다양한 쿼리로 검색 품질 테스트:
```graphql
# 테스트 1: 정확한 키워드
nearText: { concepts: ["Weaviate"] }

# 테스트 2: 의미론적 쿼리
nearText: { concepts: ["벡터 데이터베이스란 무엇인가"] }

# 테스트 3: 관련 개념
nearText: { concepts: ["AI", "머신러닝", "검색"] }
```

---

## 문제 해결 🔧

### Console이 접속되지 않을 때

**1. 컨테이너 상태 확인**
```bash
docker ps | grep console

# 없다면 재시작
docker-compose restart weaviate-console
```

**2. 로그 확인**
```bash
docker-compose logs weaviate-console

# "ready" 또는 "started" 메시지 확인
```

**3. 포트 충돌 확인**
```bash
# 8081 포트가 이미 사용 중인지 확인
lsof -i :8081  # macOS/Linux
netstat -an | findstr 8081  # Windows
```

**해결:** docker-compose.yml에서 포트 변경
```yaml
ports:
  - "8082:80"  # 8081 → 8082로 변경
```

### 데이터가 보이지 않을 때

**1. Weaviate 연결 확인**
```bash
curl http://localhost:8080/v1/meta
```

**2. 스키마 확인**
```bash
curl http://localhost:8080/v1/schema
```

**3. Python 스크립트 재실행**
```bash
cd lessons/01-basics
python 02_schema.py
python 03_crud.py
```

### 쿼리 실패시

**일반적인 원인:**
- ❌ 컬렉션 이름 오타 (`Article` vs `Articles`)
- ❌ 속성 이름 오타 (`title` vs `Title`)
- ❌ 잘못된 필터 연산자
- ❌ 데이터 타입 불일치

**해결:** Schema 탭에서 정확한 이름 확인

---

## 다음 단계

Console 사용법을 익혔다면:

1. **학습 모듈 진행**: `lessons/`의 예제 실행하며 Console에서 결과 확인
2. **쿼리 실험**: 다양한 GraphQL 쿼리 작성 및 테스트
3. **성능 분석**: Monitoring 탭으로 쿼리 성능 측정
4. **API 개발**: Console에서 테스트한 쿼리를 Python 코드로 구현

---

## 참고 자료

- [Weaviate Console 공식 문서](https://weaviate.io/developers/weaviate/tools/console)
- [GraphQL 쿼리 가이드](https://weaviate.io/developers/weaviate/api/graphql)
- [GUI 클라이언트 비교](./gui-clients.md)

---

**이제 Console로 Weaviate를 시각적으로 탐색해보세요! 🚀**
