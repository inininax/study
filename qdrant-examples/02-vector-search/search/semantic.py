"""
의미론적 검색 엔진

텍스트 임베딩 기반 의미론적 유사도 검색
"""

import sys
sys.path.append('../../01-fundamentals')

from typing import List, Dict, Any, Optional
from core.client import QdrantClientManager
from core.operations import VectorOperations
from qdrant_client.models import ScoredPoint
import logging

logger = logging.getLogger(__name__)


class SemanticSearchEngine:
    """
    의미론적 검색 엔진

    Features:
    - 벡터 기반 유사도 검색
    - 점수 임계값 필터링
    - 페이로드 포함/제외 옵션
    - 검색 결과 후처리

    Example:
        >>> engine = SemanticSearchEngine("documents")
        >>> results = engine.search(
        ...     query_vector=[0.1, 0.2, ...],
        ...     limit=10
        ... )
    """

    def __init__(
        self,
        collection_name: str,
        client_manager: Optional[QdrantClientManager] = None
    ):
        """
        Args:
            collection_name: 검색할 컬렉션 이름
            client_manager: QdrantClientManager 인스턴스
        """
        self.collection_name = collection_name
        self.client_manager = client_manager or QdrantClientManager()
        self.client = self.client_manager.client
        self.ops = VectorOperations(collection_name, client_manager)

    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: Optional[float] = None,
        with_payload: bool = True,
        with_vectors: bool = False,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        벡터 유사도 검색

        Args:
            query_vector: 쿼리 벡터
            limit: 결과 개수
            score_threshold: 최소 점수 (0.0 ~ 1.0)
            with_payload: 페이로드 포함 여부
            with_vectors: 벡터 포함 여부
            offset: 결과 오프셋 (페이지네이션)

        Returns:
            검색 결과 리스트
        """
        try:
            # Qdrant 검색
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=with_payload,
                with_vectors=with_vectors,
                offset=offset
            )

            # 결과 포맷팅
            formatted_results = [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload if with_payload else None,
                    "vector": result.vector if with_vectors else None
                }
                for result in results
            ]

            logger.info(
                f"검색 완료: {len(formatted_results)}개 결과 "
                f"(임계값: {score_threshold or 'None'})"
            )

            return formatted_results

        except Exception as e:
            logger.error(f"검색 실패: {e}")
            raise

    def search_batch(
        self,
        query_vectors: List[List[float]],
        limit: int = 10,
        score_threshold: Optional[float] = None
    ) -> List[List[Dict[str, Any]]]:
        """
        여러 쿼리 벡터 동시 검색

        Args:
            query_vectors: 쿼리 벡터 리스트
            limit: 각 쿼리당 결과 개수
            score_threshold: 최소 점수

        Returns:
            검색 결과 리스트의 리스트
        """
        try:
            results = self.client.search_batch(
                collection_name=self.collection_name,
                requests=[
                    {
                        "vector": qv,
                        "limit": limit,
                        "score_threshold": score_threshold
                    }
                    for qv in query_vectors
                ]
            )

            return [
                [
                    {
                        "id": r.id,
                        "score": r.score,
                        "payload": r.payload
                    }
                    for r in batch_results
                ]
                for batch_results in results
            ]

        except Exception as e:
            logger.error(f"배치 검색 실패: {e}")
            raise

    def recommend(
        self,
        positive_ids: List[str],
        negative_ids: Optional[List[str]] = None,
        limit: int = 10,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        추천 검색 (긍정/부정 예시 기반)

        Args:
            positive_ids: 좋아하는 항목 ID들
            negative_ids: 싫어하는 항목 ID들
            limit: 결과 개수
            score_threshold: 최소 점수

        Returns:
            추천 결과 리스트
        """
        try:
            results = self.client.recommend(
                collection_name=self.collection_name,
                positive=positive_ids,
                negative=negative_ids or [],
                limit=limit,
                score_threshold=score_threshold
            )

            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                }
                for result in results
            ]

        except Exception as e:
            logger.error(f"추천 실패: {e}")
            raise
