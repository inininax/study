# 단계 5: 실전 프로젝트 - RAG 시스템

> Retrieval-Augmented Generation 완전 구현

## 📚 학습 목표

- RAG 아키텍처 이해 및 설계
- 문서 처리 파이프라인 구축
- 임베딩 전략 및 최적화
- LLM 통합 (OpenAI, Anthropic)
- 답변 품질 평가 및 개선

## 🏗 프로젝트 구조

```
05-real-project/
├── rag/
│   ├── __init__.py
│   ├── pipeline.py          # RAG 파이프라인
│   ├── chunking.py          # 문서 청킹
│   ├── embeddings.py        # 임베딩 생성
│   ├── retrieval.py         # 검색 최적화
│   └── generation.py        # LLM 통합
│
├── api/
│   ├── main.py              # FastAPI 서버
│   ├── routers/
│   │   ├── qa.py            # Q&A 엔드포인트
│   │   └── documents.py     # 문서 관리
│   └── models/
│       └── schemas.py
│
├── data/
│   └── sample_docs/         # 샘플 문서들
│
└── tests/
    └── test_rag.py
```

## 🚀 RAG 파이프라인

### 1. 문서 처리

```python
from rag.chunking import DocumentChunker

chunker = DocumentChunker(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)

chunks = chunker.chunk_document(
    document=long_text,
    metadata={"source": "manual.pdf", "page": 1}
)
```

### 2. 임베딩 생성

```python
from rag.embeddings import EmbeddingGenerator

embedder = EmbeddingGenerator(
    model="text-embedding-3-small",  # OpenAI
    batch_size=32
)

embeddings = await embedder.generate_batch(
    texts=[chunk.content for chunk in chunks]
)
```

### 3. 벡터 저장

```python
from rag.pipeline import RAGPipeline

pipeline = RAGPipeline(collection_name="knowledge_base")

await pipeline.ingest_documents(
    documents=documents,
    source="product_docs"
)
```

### 4. 검색 및 생성

```python
# 질문 응답
response = await pipeline.query(
    question="Qdrant의 HNSW 파라미터는 어떻게 튜닝하나요?",
    top_k=5,
    llm_model="gpt-4"
)

print(f"답변: {response.answer}")
print(f"출처: {response.sources}")
print(f"신뢰도: {response.confidence}")
```

## 📖 고급 기능

### 1. 문서 청킹 전략

- **고정 크기**: 토큰 수 기반
- **의미 기반**: 문단/섹션 단위
- **하이브리드**: 크기 + 의미 조합
- **슬라이딩 윈도우**: 오버랩 처리

### 2. 하이브리드 검색

```python
# 벡터 + 키워드 + 메타데이터
results = await pipeline.hybrid_search(
    query="머신러닝",
    semantic_weight=0.7,
    keyword_weight=0.2,
    metadata_filter={
        "category": "AI",
        "year": {"$gte": 2023}
    }
)
```

### 3. 리랭킹

```python
from rag.retrieval import CrossEncoderReranker

reranker = CrossEncoderReranker(
    model="cross-encoder/ms-marco-MiniLM-L-12-v2"
)

reranked = await reranker.rerank(
    query=question,
    documents=initial_results,
    top_k=3
)
```

### 4. 답변 생성 옵션

```python
response = await pipeline.query(
    question="...",
    generation_config={
        "temperature": 0.1,
        "max_tokens": 500,
        "style": "concise",  # 또는 "detailed", "technical"
        "include_citations": True
    }
)
```

## 🎯 실전 활용 예시

### 1. 제품 문서 Q&A 시스템

```python
# 문서 업로드 API
@app.post("/api/documents/upload")
async def upload_document(file: UploadFile):
    # PDF/DOCX 파싱
    text = await parse_document(file)

    # RAG 파이프라인으로 처리
    await rag_pipeline.ingest_documents([text])

    return {"status": "success", "chunks": len(chunks)}

# Q&A API
@app.post("/api/qa")
async def ask_question(request: QuestionRequest):
    response = await rag_pipeline.query(
        question=request.question,
        top_k=5
    )

    return {
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence
    }
```

### 2. 대화형 챗봇

```python
# 대화 컨텍스트 유지
conversation = ConversationChain(
    rag_pipeline=pipeline,
    memory_window=5
)

# 연속 질문 처리
responses = []
for question in ["Qdrant란?", "설치 방법은?", "Python에서 사용하려면?"]:
    response = await conversation.ask(question)
    responses.append(response)
```

### 3. 문서 요약

```python
summary = await pipeline.summarize_document(
    document=long_document,
    style="executive",  # 또는 "technical", "simple"
    max_length=200
)
```

## 📊 성능 최적화

### 1. 캐싱 전략
- 임베딩 캐시 (Redis)
- LLM 응답 캐시
- 검색 결과 캐시

### 2. 배치 처리
- 문서 일괄 처리
- 임베딩 배치 생성
- 비동기 파이프라인

### 3. 비용 최적화
- 작은 임베딩 모델 사용
- 프롬프트 최적화
- 캐싱으로 API 호출 감소

## 🧪 평가 메트릭

### 1. 검색 품질
- Precision@K
- Recall@K
- MRR (Mean Reciprocal Rank)

### 2. 답변 품질
- ROUGE 점수
- 사용자 피드백
- 전문가 평가

### 3. 시스템 성능
- 응답 시간
- 처리량
- 비용 효율성

## 🎯 실습 과제

1. **개인 문서 Q&A**: PDF/Markdown 문서 업로드 및 질의응답
2. **기술 문서 챗봇**: 프로그래밍 문서 기반 도우미
3. **다국어 RAG**: 여러 언어 문서 처리

## 📚 참고 자료

- [RAG 논문](https://arxiv.org/abs/2005.11401)
- [LangChain RAG 가이드](https://python.langchain.com/docs/use_cases/question_answering/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

## ✅ 체크리스트

- [ ] 문서 청킹 파이프라인 구현
- [ ] 임베딩 생성 및 저장
- [ ] 하이브리드 검색 구현
- [ ] LLM 통합
- [ ] Q&A API 서버 구축
- [ ] 답변 품질 평가
- [ ] 프로덕션 배포

---

**난이도**: ⭐⭐⭐⭐⭐
**예상 시간**: 6-8시간
**선행 지식**: 단계 1-4 완료, LLM 기초, NLP 개념
