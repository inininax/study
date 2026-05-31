"""
컬렉션 관리

컬렉션의 생성, 삭제, 업데이트 및 설정 관리
"""

import logging
from typing import Optional, Dict, Any
from qdrant_client.models import Distance, VectorParams, HnswConfigDiff, OptimizersConfigDiff

from .client import QdrantClientManager
from .models import CollectionConfig, DistanceMetric, CollectionInfo
from .exceptions import (
    CollectionNotFoundError,
    CollectionAlreadyExistsError,
    QdrantBaseException
)

logger = logging.getLogger(__name__)


class CollectionManager:
    """
    컬렉션 관리 클래스

    Features:
    - 컬렉션 생성 (다양한 설정 옵션)
    - 컬렉션 삭제
    - 컬렉션 존재 확인
    - HNSW 파라미터 최적화

    Example:
        >>> manager = CollectionManager()
        >>> manager.create_collection(
        ...     name="documents",
        ...     vector_size=384,
        ...     distance=Distance.COSINE
        ... )
    """

    def __init__(self, client_manager: Optional[QdrantClientManager] = None):
        """
        Args:
            client_manager: QdrantClientManager 인스턴스 (없으면 자동 생성)
        """
        self.client_manager = client_manager or QdrantClientManager()
        self.client = self.client_manager.client

    def create_collection(
        self,
        name: str,
        vector_size: int,
        distance: Distance = Distance.COSINE,
        hnsw_config: Optional[Dict[str, Any]] = None,
        optimizers_config: Optional[Dict[str, Any]] = None,
        on_disk: bool = False,
        replication_factor: int = 1,
        write_consistency_factor: int = 1
    ) -> CollectionInfo:
        """
        컬렉션 생성

        Args:
            name: 컬렉션 이름
            vector_size: 벡터 차원
            distance: 거리 메트릭 (Cosine, Dot, Euclid)
            hnsw_config: HNSW 인덱스 설정
                - m: 각 노드의 최대 연결 수 (기본값: 16)
                - ef_construct: 인덱스 구성 시 탐색 깊이 (기본값: 100)
            optimizers_config: 옵티마이저 설정
            on_disk: 디스크 저장 여부
            replication_factor: 복제 팩터
            write_consistency_factor: 쓰기 일관성 팩터

        Returns:
            CollectionInfo 객체

        Raises:
            CollectionAlreadyExistsError: 컬렉션이 이미 존재하는 경우
        """
        try:
            # 컬렉션 존재 확인
            if self.collection_exists(name):
                raise CollectionAlreadyExistsError(
                    f"컬렉션 '{name}'이 이미 존재합니다",
                    details={"collection_name": name}
                )

            # HNSW 설정
            hnsw_config_diff = None
            if hnsw_config:
                hnsw_config_diff = HnswConfigDiff(
                    m=hnsw_config.get("m", 16),
                    ef_construct=hnsw_config.get("ef_construct", 100),
                    full_scan_threshold=hnsw_config.get("full_scan_threshold", 10000)
                )

            # Optimizers 설정
            optimizers_config_diff = None
            if optimizers_config:
                optimizers_config_diff = OptimizersConfigDiff(
                    deleted_threshold=optimizers_config.get("deleted_threshold", 0.2),
                    vacuum_min_vector_number=optimizers_config.get("vacuum_min_vector_number", 1000),
                    default_segment_number=optimizers_config.get("default_segment_number", 0)
                )

            logger.info(f"컬렉션 생성 중: {name} (벡터 크기: {vector_size}, 거리: {distance})")

            # 컬렉션 생성
            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=distance,
                    on_disk=on_disk
                ),
                hnsw_config=hnsw_config_diff,
                optimizers_config=optimizers_config_diff,
                replication_factor=replication_factor,
                write_consistency_factor=write_consistency_factor
            )

            logger.info(f"✓ 컬렉션 '{name}' 생성 완료")

            return self.get_collection_info(name)

        except CollectionAlreadyExistsError:
            raise
        except Exception as e:
            logger.error(f"컬렉션 생성 실패: {e}")
            raise QdrantBaseException(f"컬렉션 생성 실패: {str(e)}")

    def create_collection_from_config(self, config: CollectionConfig) -> CollectionInfo:
        """
        CollectionConfig 객체로부터 컬렉션 생성

        Args:
            config: CollectionConfig 객체

        Returns:
            CollectionInfo 객체
        """
        distance_map = {
            DistanceMetric.COSINE: Distance.COSINE,
            DistanceMetric.DOT: Distance.DOT,
            DistanceMetric.EUCLID: Distance.EUCLID,
            DistanceMetric.MANHATTAN: Distance.MANHATTAN
        }

        return self.create_collection(
            name=config.name,
            vector_size=config.vector_size,
            distance=distance_map[config.distance],
            hnsw_config=config.hnsw_config
        )

    def delete_collection(self, name: str, timeout: int = 60) -> bool:
        """
        컬렉션 삭제

        Args:
            name: 컬렉션 이름
            timeout: 타임아웃 (초)

        Returns:
            삭제 성공 여부

        Raises:
            CollectionNotFoundError: 컬렉션이 존재하지 않는 경우
        """
        try:
            if not self.collection_exists(name):
                raise CollectionNotFoundError(
                    f"컬렉션 '{name}'을 찾을 수 없습니다",
                    details={"collection_name": name}
                )

            logger.info(f"컬렉션 삭제 중: {name}")
            self.client.delete_collection(collection_name=name, timeout=timeout)
            logger.info(f"✓ 컬렉션 '{name}' 삭제 완료")

            return True

        except CollectionNotFoundError:
            raise
        except Exception as e:
            logger.error(f"컬렉션 삭제 실패: {e}")
            raise QdrantBaseException(f"컬렉션 삭제 실패: {str(e)}")

    def collection_exists(self, name: str) -> bool:
        """
        컬렉션 존재 확인

        Args:
            name: 컬렉션 이름

        Returns:
            존재 여부
        """
        try:
            collections = self.client.get_collections().collections
            return any(col.name == name for col in collections)
        except Exception as e:
            logger.error(f"컬렉션 존재 확인 실패: {e}")
            return False

    def get_collection_info(self, name: str) -> CollectionInfo:
        """
        컬렉션 정보 조회

        Args:
            name: 컬렉션 이름

        Returns:
            CollectionInfo 객체

        Raises:
            CollectionNotFoundError: 컬렉션이 존재하지 않는 경우
        """
        try:
            if not self.collection_exists(name):
                raise CollectionNotFoundError(
                    f"컬렉션 '{name}'을 찾을 수 없습니다",
                    details={"collection_name": name}
                )

            return self.client_manager.get_collection_info(name)

        except CollectionNotFoundError:
            raise
        except Exception as e:
            logger.error(f"컬렉션 정보 조회 실패: {e}")
            raise QdrantBaseException(f"컬렉션 정보 조회 실패: {str(e)}")

    def recreate_collection(
        self,
        name: str,
        vector_size: int,
        distance: Distance = Distance.COSINE,
        **kwargs
    ) -> CollectionInfo:
        """
        컬렉션 재생성 (기존 컬렉션 삭제 후 새로 생성)

        Args:
            name: 컬렉션 이름
            vector_size: 벡터 차원
            distance: 거리 메트릭
            **kwargs: 추가 설정

        Returns:
            CollectionInfo 객체
        """
        if self.collection_exists(name):
            logger.warning(f"기존 컬렉션 '{name}' 삭제 중...")
            self.delete_collection(name)

        return self.create_collection(
            name=name,
            vector_size=vector_size,
            distance=distance,
            **kwargs
        )

    def update_collection_params(
        self,
        name: str,
        optimizers_config: Optional[Dict[str, Any]] = None,
        hnsw_config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        컬렉션 파라미터 업데이트

        Args:
            name: 컬렉션 이름
            optimizers_config: 옵티마이저 설정
            hnsw_config: HNSW 설정

        Returns:
            업데이트 성공 여부
        """
        try:
            if not self.collection_exists(name):
                raise CollectionNotFoundError(
                    f"컬렉션 '{name}'을 찾을 수 없습니다",
                    details={"collection_name": name}
                )

            if optimizers_config:
                self.client.update_collection(
                    collection_name=name,
                    optimizers_config=OptimizersConfigDiff(**optimizers_config)
                )

            if hnsw_config:
                self.client.update_collection(
                    collection_name=name,
                    hnsw_config=HnswConfigDiff(**hnsw_config)
                )

            logger.info(f"✓ 컬렉션 '{name}' 파라미터 업데이트 완료")
            return True

        except Exception as e:
            logger.error(f"컬렉션 파라미터 업데이트 실패: {e}")
            raise QdrantBaseException(f"컬렉션 파라미터 업데이트 실패: {str(e)}")
