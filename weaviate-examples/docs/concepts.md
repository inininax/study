# Weaviate 핵심 개념 📖

## 1. Weaviate란?

Weaviate는 **벡터 데이터베이스(Vector Database)**입니다. 일반적인 데이터베이스와 달리, 데이터를 숫자 벡터로 저장하고 **의미(semantic)** 기반으로 검색할 수 있습니다.

### 1.1 왜 벡터 데이터베이스가 필요한가?

**전통적인 데이터베이스 검색의 한계:**
```python
# 전통적인 키워드 검색
query = "강아지 사료"
# 결과: "강아지 사료"라는 정확한 단어가 포함된 문서만 찾음
# 문제: "반려견 먹이", "개 음식" 등은 찾지 못함
```

**벡터 데이터베이스의 장점:**
```python
# 의미 기반 검색
query = "강아지 사료"
# 결과: "반려견 먹이", "개 음식", "애완동물 영양" 등
#       의미가 유사한 모든 문서를 찾음
```

## 2. 핵심 개념

### 2.1 벡터(Vector)란?

벡터는 **숫자의 배열**입니다. 텍스트, 이미지, 오디오 등을 숫자로 변환한 것입니다.

```python
# 예시: 문장을 벡터로 변환
text = "안녕하세요"
vector = [0.23, -0.45, 0.67, ...]  # 실제로는 768차원 또는 1536차원

# 유사한 문장은 유사한 벡터를 가짐
text1 = "안녕하세요"     # [0.23, -0.45, 0.67, ...]
text2 = "반갑습니다"     # [0.25, -0.43, 0.69, ...]  <- 비슷함!
text3 = "사과는 맛있다"  # [-0.89, 0.12, -0.34, ...] <- 다름!
```

### 2.2 임베딩(Embedding)

**임베딩**은 데이터를 벡터로 변환하는 과정입니다.

```python
# OpenAI의 임베딩 모델 사용 예시
from openai import OpenAI

client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Weaviate는 벡터 데이터베이스입니다"
)

# 결과: 1536개의 숫자로 이루어진 벡터
embedding = response.data[0].embedding
print(f"벡터 차원: {len(embedding)}")  # 1536
```

### 2.3 컬렉션(Collection) / 클래스(Class)

컬렉션은 **데이터의 그룹**입니다. SQL의 테이블과 유사합니다.

```python
# 예시: Article 컬렉션
{
    "class": "Article",          # 컬렉션 이름
    "description": "뉴스 기사",
    "properties": [              # 속성들 (SQL의 컬럼과 유사)
        {
            "name": "title",     # 제목
            "dataType": ["text"]
        },
        {
            "name": "content",   # 내용
            "dataType": ["text"]
        },
        {
            "name": "published", # 발행일
            "dataType": ["date"]
        }
    ]
}
```

### 2.4 객체(Object)

객체는 **컬렉션 안의 개별 데이터**입니다. SQL의 행(row)과 유사합니다.

```python
# 예시: Article 객체
{
    "title": "AI 기술의 발전",
    "content": "인공지능 기술이 빠르게 발전하고 있습니다...",
    "published": "2024-01-15T10:00:00Z"
}
```

### 2.5 벡터화(Vectorization)

Weaviate가 자동으로 텍스트를 벡터로 변환하는 기능입니다.

**수동 벡터화:**
```python
# 직접 벡터를 생성하고 저장
vector = create_embedding("텍스트")
weaviate.data.insert(properties={...}, vector=vector)
```

**자동 벡터화 (권장):**
```python
# Weaviate가 자동으로 벡터 생성
weaviate.data.insert(properties={
    "title": "AI 기술의 발전"  # <- 이 텍스트가 자동으로 벡터화됨
})
```

## 3. 검색 방법

### 3.1 벡터 검색 (Semantic Search)

**의미 기반으로 유사한 데이터**를 찾습니다.

```python
# "AI 기술"을 검색하면 "인공지능", "머신러닝" 등도 찾음
results = collection.query.near_text(
    query="AI 기술",
    limit=10
)
```

### 3.2 키워드 검색 (BM25)

**정확한 키워드 매칭**으로 검색합니다. (전통적인 방식)

```python
# "AI"라는 단어가 포함된 문서만 찾음
results = collection.query.bm25(
    query="AI",
    limit=10
)
```

### 3.3 하이브리드 검색

**벡터 검색 + 키워드 검색**을 결합합니다.

```python
# 의미도 맞고, 키워드도 포함된 최상의 결과
results = collection.query.hybrid(
    query="AI 기술",
    alpha=0.5,  # 0=키워드만, 1=벡터만, 0.5=균형
    limit=10
)
```

## 4. 필터링

검색 결과를 특정 조건으로 **필터링**할 수 있습니다.

```python
from weaviate.classes.query import Filter

# 2024년 이후 발행된 기사만 검색
results = collection.query.near_text(
    query="AI 기술",
    filters=Filter.by_property("published").greater_than("2024-01-01"),
    limit=10
)
```

## 5. 주요 용어 정리

| 용어 | 설명 | SQL 비유 |
|------|------|----------|
| **Collection** | 데이터 그룹 | Table |
| **Object** | 개별 데이터 | Row |
| **Property** | 객체의 속성 | Column |
| **Vector** | 숫자 배열 (임베딩) | - |
| **Embedding** | 데이터를 벡터로 변환 | - |
| **Near Text** | 의미 기반 검색 | - |
| **BM25** | 키워드 검색 | LIKE '%keyword%' |
| **Hybrid** | 벡터 + 키워드 검색 | - |
| **Filter** | 조건 필터링 | WHERE |

## 6. Weaviate의 장점

### 6.1 빠른 속도
- 수백만 개의 벡터에서 밀리초 안에 검색

### 6.2 확장성
- 수평 확장 가능 (Sharding)
- 멀티테넌시 지원

### 6.3 유연성
- 다양한 벡터화 모델 지원 (OpenAI, Cohere, Hugging Face 등)
- RESTful API 및 GraphQL 지원

### 6.4 실시간 업데이트
- 데이터 추가/수정/삭제가 즉시 검색에 반영

## 7. 실제 사용 사례

### 7.1 의미론적 검색
```
사용자: "배가 고파요"
결과: "음식점 추천", "레시피", "간단한 요리" 등
```

### 7.2 추천 시스템
```
사용자가 본 영화: "인셉션"
추천: "인터스텔라", "메멘토", "프레스티지" (유사한 스타일)
```

### 7.3 RAG (Retrieval Augmented Generation)
```
질문: "회사의 휴가 정책은?"
1. Weaviate에서 관련 문서 검색
2. 검색된 문서를 LLM에 전달
3. LLM이 정확한 답변 생성
```

### 7.4 중복 탐지
```
신규 문서가 기존 문서와 얼마나 유사한지 확인
```

## 8. Python 초보자를 위한 팁

### 8.1 클라이언트 연결 패턴
```python
import weaviate
from weaviate.classes.init import Auth

# 항상 이 패턴으로 시작
client = weaviate.connect_to_local()
try:
    # 여기에 작업 코드
    pass
finally:
    client.close()  # 항상 연결 종료!
```

### 8.2 에러 처리
```python
try:
    result = collection.query.near_text(query="AI")
except Exception as e:
    print(f"에러 발생: {e}")
    # 에러를 무시하지 말고 항상 처리하세요!
```

### 8.3 타입 힌트 사용
```python
from typing import List, Dict, Any

def search_articles(query: str) -> List[Dict[str, Any]]:
    """
    타입 힌트를 사용하면 코드가 더 명확해집니다.

    Args:
        query: 검색 쿼리 문자열

    Returns:
        검색 결과 리스트
    """
    pass
```

## 다음 단계

이제 기본 개념을 이해했으니, 실제 코드로 Weaviate를 사용해봅시다!

👉 [초급 학습 시작하기](../lessons/01-basics/README.md)
