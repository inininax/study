"""
Pydantic 데이터 모델

타입 안정성과 검증을 위한 데이터 모델 정의
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class DistanceMetric(str, Enum):
    """벡터 거리 측정 메트릭"""
    COSINE = "Cosine"
    DOT = "Dot"
    EUCLID = "Euclid"
    MANHATTAN = "Manhattan"


class VectorPoint(BaseModel):
    """벡터 포인트 모델"""
    id: Union[int, str] = Field(..., description="포인트 고유 ID")
    vector: List[float] = Field(..., description="벡터 데이터")
    payload: Dict[str, Any] = Field(default_factory=dict, description="메타데이터")

    @validator('vector')
    def validate_vector(cls, v):
        if not v:
            raise ValueError("벡터는 비어있을 수 없습니다")
        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError("벡터는 숫자만 포함해야 합니다")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "vector": [0.1, 0.2, 0.3],
                "payload": {"title": "Example", "category": "test"}
            }
        }


class CollectionConfig(BaseModel):
    """컬렉션 설정"""
    name: str = Field(..., description="컬렉션 이름")
    vector_size: int = Field(..., gt=0, description="벡터 차원")
    distance: DistanceMetric = Field(default=DistanceMetric.COSINE, description="거리 메트릭")
    hnsw_config: Optional[Dict[str, Any]] = Field(default=None, description="HNSW 인덱스 설정")

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("컬렉션 이름은 비어있을 수 없습니다")
        # 컬렉션 이름 규칙: 소문자, 숫자, 언더스코어, 하이픈만 허용
        import re
        if not re.match(r'^[a-z0-9_-]+$', v):
            raise ValueError(
                "컬렉션 이름은 소문자, 숫자, 언더스코어, 하이픈만 사용 가능합니다"
            )
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "my_collection",
                "vector_size": 384,
                "distance": "Cosine",
                "hnsw_config": {"m": 16, "ef_construct": 100}
            }
        }


class CollectionInfo(BaseModel):
    """컬렉션 정보"""
    name: str
    vector_size: int
    distance: str
    points_count: int = 0
    indexed_vectors_count: int = 0
    status: str = "green"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "documents",
                "vector_size": 384,
                "distance": "Cosine",
                "points_count": 1000,
                "indexed_vectors_count": 1000,
                "status": "green"
            }
        }


class OperationResult(BaseModel):
    """작업 결과"""
    success: bool = Field(..., description="작업 성공 여부")
    message: str = Field(default="", description="결과 메시지")
    data: Optional[Dict[str, Any]] = Field(default=None, description="결과 데이터")
    elapsed_time: float = Field(default=0.0, description="소요 시간(초)")
    timestamp: datetime = Field(default_factory=datetime.now, description="작업 시간")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "작업 완료",
                "data": {"inserted": 100},
                "elapsed_time": 1.23,
                "timestamp": "2024-01-01T00:00:00"
            }
        }


class BatchUpsertRequest(BaseModel):
    """배치 삽입 요청"""
    vectors: List[List[float]] = Field(..., description="벡터 리스트")
    payloads: Optional[List[Dict[str, Any]]] = Field(default=None, description="페이로드 리스트")
    ids: Optional[List[Union[int, str]]] = Field(default=None, description="ID 리스트")
    chunk_size: int = Field(default=100, gt=0, le=1000, description="청크 크기")

    @validator('payloads')
    def validate_payloads(cls, v, values):
        if v is not None:
            vectors = values.get('vectors', [])
            if len(v) != len(vectors):
                raise ValueError("페이로드 개수와 벡터 개수가 일치해야 합니다")
        return v

    @validator('ids')
    def validate_ids(cls, v, values):
        if v is not None:
            vectors = values.get('vectors', [])
            if len(v) != len(vectors):
                raise ValueError("ID 개수와 벡터 개수가 일치해야 합니다")
            if len(set(v)) != len(v):
                raise ValueError("ID는 중복될 수 없습니다")
        return v


class SearchRequest(BaseModel):
    """검색 요청"""
    query_vector: List[float] = Field(..., description="쿼리 벡터")
    limit: int = Field(default=10, gt=0, le=100, description="결과 개수")
    score_threshold: Optional[float] = Field(default=None, ge=0, le=1, description="최소 점수")
    with_payload: bool = Field(default=True, description="페이로드 포함 여부")
    with_vectors: bool = Field(default=False, description="벡터 포함 여부")


class SearchResult(BaseModel):
    """검색 결과"""
    id: Union[int, str]
    score: float
    payload: Optional[Dict[str, Any]] = None
    vector: Optional[List[float]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "score": 0.95,
                "payload": {"title": "Example"},
                "vector": None
            }
        }
