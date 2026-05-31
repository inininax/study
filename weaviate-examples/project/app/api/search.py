"""
검색 API 라우터
===============

벡터 검색, 하이브리드 검색, RAG Q&A 엔드포인트
"""

from fastapi import APIRouter, HTTPException
from typing import List

from app.models.document import (
    SemanticSearchRequest,
    HybridSearchRequest,
    QARequest,
    QAResponse,
)
from app.services.weaviate_service import weaviate_service
from app.services.rag_service import rag_service
from app.utils.logger import logger


router = APIRouter()


@router.post("/semantic", response_model=List[dict])
async def semantic_search(request: SemanticSearchRequest):
    """
    의미 검색 (Semantic Search)

    텍스트의 의미를 기반으로 유사한 문서를 찾습니다.

    - **query**: 검색 쿼리
    - **limit**: 결과 개수 (기본: 10)
    - **min_certainty**: 최소 확신도 (기본: 0.7)
    """
    try:
        results = weaviate_service.semantic_search(
            query=request.query, limit=request.limit, min_certainty=request.min_certainty
        )

        return results

    except Exception as e:
        logger.error(f"의미 검색 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/keyword", response_model=List[dict])
async def keyword_search(request: SemanticSearchRequest):
    """
    키워드 검색 (BM25)

    정확한 키워드 매칭으로 문서를 찾습니다.
    """
    try:
        # BM25 검색은 alpha=0으로 하이브리드 검색 사용
        results = weaviate_service.hybrid_search(
            query=request.query, limit=request.limit, alpha=0.0
        )

        return results

    except Exception as e:
        logger.error(f"키워드 검색 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hybrid", response_model=List[dict])
async def hybrid_search(request: HybridSearchRequest):
    """
    하이브리드 검색

    벡터 검색과 키워드 검색을 결합합니다.

    - **query**: 검색 쿼리
    - **limit**: 결과 개수
    - **alpha**: 검색 가중치
        - 0.0 = 키워드 검색만
        - 1.0 = 벡터 검색만
        - 0.5 = 균형 (기본값)
    """
    try:
        results = weaviate_service.hybrid_search(
            query=request.query, limit=request.limit, alpha=request.alpha
        )

        return results

    except Exception as e:
        logger.error(f"하이브리드 검색 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/qa", response_model=dict)
async def question_answering(request: QARequest):
    """
    Q&A (RAG - Retrieval Augmented Generation)

    문서를 검색하고 LLM을 사용하여 질문에 답변합니다.

    - **question**: 질문
    - **max_context_docs**: 컨텍스트로 사용할 문서 수 (기본: 5)
    - **temperature**: LLM 온도 설정 (기본: 0.7)
    """
    try:
        answer, sources = rag_service.answer_question(
            question=request.question,
            max_docs=request.max_context_docs,
            temperature=request.temperature,
        )

        return {
            "question": request.question,
            "answer": answer,
            "sources": sources,
        }

    except Exception as e:
        logger.error(f"Q&A 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))
