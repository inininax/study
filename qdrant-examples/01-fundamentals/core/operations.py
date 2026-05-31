"""
벡터 작업 관리

CRUD 작업 및 배치 처리를 담당하는 핵심 모듈
"""

import logging
import time
import uuid
from typing import List, Dict, Any, Optional, Union
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue

from .client import QdrantClientManager
from .collections import CollectionManager
from .models import VectorPoint, OperationResult, BatchUpsertRequest
from .exceptions import (
    CollectionNotFoundError,
    VectorDimensionMismatchError,
    PointNotFoundError,
    BatchOperationError
)

logger = logging.getLogger(__name__)


class VectorOperations:
    """
    벡터 CRUD 작업 관리

    Features:
    - 단일/배치 삽입 (Upsert)
    - 벡터 조회
    - 페이로드 업데이트
    - 벡터 삭제
    - 배치 작업 최적화

    Example:
        >>> ops = VectorOperations("my_collection")
        >>> point_id = ops.upsert_point(
        ...     vector=[0.1, 0.2, 0.3],
        ...     payload={"title": "Example"}
        ... )
    """

    def __init__(
        self,
        collection_name: str,
        client_manager: Optional[QdrantClientManager] = None,
        auto_create: bool = False,
        vector_size: int = 384
    ):
        """
        Args:
            collection_name: 컬렉션 이름
            client_manager: QdrantClientManager 인스턴스
            auto_create: 컬렉션이 없을 때 자동 생성 여부
            vector_size: 자동 생성 시 벡터 크기
        """
        self.collection_name = collection_name
        self.client_manager = client_manager or QdrantClientManager()
        self.client = self.client_manager.client
        self.collection_manager = CollectionManager(self.client_manager)

        # 컬렉션 존재 확인
        if not self.collection_manager.collection_exists(collection_name):
            if auto_create:
                logger.info(f"컬렉션 '{collection_name}' 자동 생성 중...")
                self.collection_manager.create_collection(
                    name=collection_name,
                    vector_size=vector_size
                )
            else:
                raise CollectionNotFoundError(
                    f"컬렉션 '{collection_name}'을 찾을 수 없습니다",
                    details={"collection_name": collection_name}
                )

        # 컬렉션 정보 캐싱
        self._collection_info = self.collection_manager.get_collection_info(collection_name)

    @property
    def vector_size(self) -> int:
        """컬렉션의 벡터 크기"""
        return self._collection_info.vector_size

    def _validate_vector(self, vector: List[float]) -> None:
        """벡터 유효성 검사"""
        if len(vector) != self.vector_size:
            raise VectorDimensionMismatchError(
                f"벡터 크기 불일치: 예상 {self.vector_size}, 실제 {len(vector)}",
                details={
                    "expected": self.vector_size,
                    "actual": len(vector),
                    "collection": self.collection_name
                }
            )

    def _generate_id(self) -> str:
        """고유 ID 생성"""
        return str(uuid.uuid4())

    def upsert_point(
        self,
        vector: List[float],
        payload: Optional[Dict[str, Any]] = None,
        point_id: Optional[Union[int, str]] = None,
        wait: bool = True
    ) -> Union[int, str]:
        """
        단일 벡터 삽입/업데이트

        Args:
            vector: 벡터 데이터
            payload: 메타데이터
            point_id: 포인트 ID (없으면 자동 생성)
            wait: 작업 완료 대기 여부

        Returns:
            포인트 ID

        Raises:
            VectorDimensionMismatchError: 벡터 크기 불일치
        """
        try:
            self._validate_vector(vector)

            if point_id is None:
                point_id = self._generate_id()

            point = PointStruct(
                id=point_id,
                vector=vector,
                payload=payload or {}
            )

            self.client.upsert(
                collection_name=self.collection_name,
                points=[point],
                wait=wait
            )

            logger.debug(f"포인트 삽입 완료: {point_id}")
            return point_id

        except VectorDimensionMismatchError:
            raise
        except Exception as e:
            logger.error(f"포인트 삽입 실패: {e}")
            raise

    def batch_upsert(
        self,
        vectors: List[List[float]],
        payloads: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[Union[int, str]]] = None,
        chunk_size: int = 100,
        wait: bool = True
    ) -> OperationResult:
        """
        배치 벡터 삽입/업데이트

        Args:
            vectors: 벡터 리스트
            payloads: 페이로드 리스트
            ids: ID 리스트 (없으면 자동 생성)
            chunk_size: 청크 크기 (한 번에 처리할 개수)
            wait: 작업 완료 대기 여부

        Returns:
            OperationResult 객체

        Raises:
            BatchOperationError: 배치 작업 실패
        """
        try:
            start_time = time.time()

            # 벡터 유효성 검사
            for i, vector in enumerate(vectors):
                try:
                    self._validate_vector(vector)
                except VectorDimensionMismatchError as e:
                    raise BatchOperationError(
                        f"벡터 {i} 검증 실패: {str(e)}",
                        details={"index": i, "error": str(e)}
                    )

            # ID 생성
            if ids is None:
                ids = [self._generate_id() for _ in range(len(vectors))]

            # 페이로드 기본값
            if payloads is None:
                payloads = [{} for _ in range(len(vectors))]

            # PointStruct 생성
            points = [
                PointStruct(id=point_id, vector=vector, payload=payload)
                for point_id, vector, payload in zip(ids, vectors, payloads)
            ]

            # 청크 단위로 삽입
            total_inserted = 0
            for i in range(0, len(points), chunk_size):
                chunk = points[i:i + chunk_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=chunk,
                    wait=wait
                )
                total_inserted += len(chunk)
                logger.debug(f"청크 삽입: {total_inserted}/{len(points)}")

            elapsed_time = time.time() - start_time

            logger.info(
                f"배치 삽입 완료: {total_inserted}개, "
                f"소요 시간: {elapsed_time:.2f}초, "
                f"처리량: {total_inserted/elapsed_time:.0f} ops/s"
            )

            return OperationResult(
                success=True,
                message=f"{total_inserted}개 포인트 삽입 완료",
                data={
                    "inserted": total_inserted,
                    "chunk_size": chunk_size,
                    "throughput": total_inserted / elapsed_time
                },
                elapsed_time=elapsed_time
            )

        except BatchOperationError:
            raise
        except Exception as e:
            logger.error(f"배치 삽입 실패: {e}")
            raise BatchOperationError(f"배치 작업 실패: {str(e)}")

    def get_point(
        self,
        point_id: Union[int, str],
        with_payload: bool = True,
        with_vectors: bool = True
    ) -> Optional[VectorPoint]:
        """
        포인트 조회

        Args:
            point_id: 포인트 ID
            with_payload: 페이로드 포함 여부
            with_vectors: 벡터 포함 여부

        Returns:
            VectorPoint 객체 (없으면 None)
        """
        try:
            points = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[point_id],
                with_payload=with_payload,
                with_vectors=with_vectors
            )

            if not points:
                logger.warning(f"포인트를 찾을 수 없음: {point_id}")
                return None

            point = points[0]
            return VectorPoint(
                id=point.id,
                vector=point.vector if with_vectors else [],
                payload=point.payload if with_payload else {}
            )

        except Exception as e:
            logger.error(f"포인트 조회 실패: {e}")
            raise

    def update_payload(
        self,
        point_id: Union[int, str],
        payload: Dict[str, Any],
        wait: bool = True
    ) -> bool:
        """
        페이로드 업데이트 (기존 데이터에 병합)

        Args:
            point_id: 포인트 ID
            payload: 업데이트할 페이로드
            wait: 작업 완료 대기 여부

        Returns:
            업데이트 성공 여부
        """
        try:
            self.client.set_payload(
                collection_name=self.collection_name,
                points=[point_id],
                payload=payload,
                wait=wait
            )

            logger.debug(f"페이로드 업데이트 완료: {point_id}")
            return True

        except Exception as e:
            logger.error(f"페이로드 업데이트 실패: {e}")
            raise

    def overwrite_payload(
        self,
        point_id: Union[int, str],
        payload: Dict[str, Any],
        wait: bool = True
    ) -> bool:
        """
        페이로드 덮어쓰기 (기존 데이터 대체)

        Args:
            point_id: 포인트 ID
            payload: 새 페이로드
            wait: 작업 완료 대기 여부

        Returns:
            업데이트 성공 여부
        """
        try:
            self.client.overwrite_payload(
                collection_name=self.collection_name,
                points=[point_id],
                payload=payload,
                wait=wait
            )

            logger.debug(f"페이로드 덮어쓰기 완료: {point_id}")
            return True

        except Exception as e:
            logger.error(f"페이로드 덮어쓰기 실패: {e}")
            raise

    def delete_point(
        self,
        point_id: Union[int, str],
        wait: bool = True
    ) -> bool:
        """
        포인트 삭제

        Args:
            point_id: 포인트 ID
            wait: 작업 완료 대기 여부

        Returns:
            삭제 성공 여부
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[point_id],
                wait=wait
            )

            logger.debug(f"포인트 삭제 완료: {point_id}")
            return True

        except Exception as e:
            logger.error(f"포인트 삭제 실패: {e}")
            raise

    def delete_by_filter(
        self,
        filter_conditions: Dict[str, Any],
        wait: bool = True
    ) -> OperationResult:
        """
        필터 조건으로 포인트 삭제

        Args:
            filter_conditions: 필터 조건 (예: {"category": "spam"})
            wait: 작업 완료 대기 여부

        Returns:
            OperationResult 객체
        """
        try:
            start_time = time.time()

            # 필터 구성
            conditions = [
                FieldCondition(
                    key=key,
                    match=MatchValue(value=value)
                )
                for key, value in filter_conditions.items()
            ]

            filter_obj = Filter(must=conditions)

            self.client.delete(
                collection_name=self.collection_name,
                points_selector=filter_obj,
                wait=wait
            )

            elapsed_time = time.time() - start_time

            logger.info(f"필터 삭제 완료: {filter_conditions}")

            return OperationResult(
                success=True,
                message=f"필터 조건으로 포인트 삭제 완료",
                data={"filter": filter_conditions},
                elapsed_time=elapsed_time
            )

        except Exception as e:
            logger.error(f"필터 삭제 실패: {e}")
            raise

    def count_points(self) -> int:
        """
        컬렉션의 총 포인트 수 조회

        Returns:
            포인트 개수
        """
        try:
            info = self.collection_manager.get_collection_info(self.collection_name)
            return info.points_count
        except Exception as e:
            logger.error(f"포인트 카운트 실패: {e}")
            raise
