"""
문서 모델
=========

Pydantic 모델로 요청/응답 데이터 검증
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class DocumentBase(BaseModel):
    """문서 기본 모델"""

    title: str = Field(..., min_length=1, max_length=500, description="문서 제목")
    content: str = Field(..., min_length=1, description="문서 내용")
    tags: List[str] = Field(default_factory=list, description="태그 목록")
    metadata: Optional[dict] = Field(default_factory=dict, description="추가 메타데이터")

    @field_validator("tags")
    def validate_tags(cls, v):
        """태그 검증"""
        if len(v) > 20:
            raise ValueError("태그는 최대 20개까지 가능합니다")
        return [tag.strip() for tag in v if tag.strip()]


class DocumentCreate(DocumentBase):
    """문서 생성 요청"""

    pass


class DocumentUpdate(BaseModel):
    """문서 수정 요청"""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = Field(None, min_length=1)
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None


class DocumentResponse(DocumentBase):
    """문서 응답"""

    id: UUID = Field(..., description="문서 UUID")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")
    view_count: int = Field(default=0, description="조회수")

    class Config:
        from_attributes = True  # ORM 모드 활성화


class DocumentSearchResult(DocumentResponse):
    """검색 결과 모델"""

    score: Optional[float] = Field(None, description="검색 점수")
    distance: Optional[float] = Field(None, description="벡터 거리")
    highlight: Optional[str] = Field(None, description="하이라이트된 내용")


class SearchRequest(BaseModel):
    """검색 요청"""

    query: str = Field(..., min_length=1, max_length=1000, description="검색 쿼리")
    limit: int = Field(default=10, ge=1, le=100, description="결과 개수")
    offset: int = Field(default=0, ge=0, description="오프셋")
    filters: Optional[dict] = Field(default=None, description="필터 조건")


class SemanticSearchRequest(SearchRequest):
    """의미 검색 요청"""

    min_certainty: Optional[float] = Field(
        default=0.7, ge=0.0, le=1.0, description="최소 확신도"
    )


class HybridSearchRequest(SearchRequest):
    """하이브리드 검색 요청"""

    alpha: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="검색 가중치 (0=키워드, 1=벡터, 0.5=균형)",
    )


class QARequest(BaseModel):
    """Q&A 요청 (RAG)"""

    question: str = Field(..., min_length=1, max_length=1000, description="질문")
    max_context_docs: int = Field(
        default=5, ge=1, le=10, description="컨텍스트 문서 수"
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="온도 설정")


class QAResponse(BaseModel):
    """Q&A 응답"""

    question: str = Field(..., description="질문")
    answer: str = Field(..., description="답변")
    sources: List[DocumentResponse] = Field(..., description="참고 문서")
    confidence: Optional[float] = Field(None, description="신뢰도")
