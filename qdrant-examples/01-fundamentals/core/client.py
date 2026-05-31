"""
Qdrant 클라이언트 매니저

프로덕션 수준의 커넥션 풀링, 헬스체크, 에러 핸들링을 포함한
Qdrant 클라이언트 관리
"""

import os
import logging
from typing import Optional, List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

from .exceptions import QdrantConnectionError, QdrantTimeoutError
from .models import CollectionInfo

# 환경 변수 로드
load_dotenv()

# 로거 설정
logger = logging.getLogger(__name__)


class QdrantClientManager:
    """
    Qdrant 클라이언트 매니저 (싱글톤 패턴)

    Features:
    - 커넥션 풀링
    - 자동 재연결
    - 헬스체크
    - 타임아웃 관리

    Example:
        >>> manager = QdrantClientManager()
        >>> if manager.health_check():
        ...     print("Connected!")
    """

    _instance: Optional['QdrantClientManager'] = None
    _client: Optional[QdrantClient] = None

    def __new__(cls):
        """싱글톤 인스턴스 생성"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        grpc_port: Optional[int] = None,
        api_key: Optional[str] = None,
        timeout: int = 30,
        prefer_grpc: bool = False
    ):
        """
        Qdrant 클라이언트 초기화

        Args:
            host: Qdrant 서버 호스트 (기본값: 환경변수 QDRANT_HOST)
            port: REST API 포트 (기본값: 환경변수 QDRANT_PORT)
            grpc_port: gRPC 포트 (기본값: 환경변수 QDRANT_GRPC_PORT)
            api_key: API 키 (기본값: 환경변수 QDRANT_API_KEY)
            timeout: 타임아웃 (초)
            prefer_grpc: gRPC 사용 여부
        """
        # 이미 초기화된 경우 스킵
        if self._client is not None:
            return

        self.host = host or os.getenv("QDRANT_HOST", "localhost")
        self.port = port or int(os.getenv("QDRANT_PORT", "6333"))
        self.grpc_port = grpc_port or int(os.getenv("QDRANT_GRPC_PORT", "6334"))
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.timeout = timeout
        self.prefer_grpc = prefer_grpc

        self._initialize_client()

    def _initialize_client(self):
        """클라이언트 초기화"""
        try:
            logger.info(f"Qdrant 클라이언트 연결 중: {self.host}:{self.port}")

            self._client = QdrantClient(
                host=self.host,
                port=self.port,
                grpc_port=self.grpc_port,
                api_key=self.api_key,
                timeout=self.timeout,
                prefer_grpc=self.prefer_grpc
            )

            # 연결 테스트
            if not self.health_check():
                raise QdrantConnectionError(
                    "Qdrant 서버에 연결할 수 없습니다",
                    details={"host": self.host, "port": self.port}
                )

            logger.info("✓ Qdrant 클라이언트 연결 성공")

        except Exception as e:
            logger.error(f"Qdrant 연결 실패: {e}")
            raise QdrantConnectionError(
                f"클라이언트 초기화 실패: {str(e)}",
                details={"host": self.host, "port": self.port}
            )

    @property
    def client(self) -> QdrantClient:
        """클라이언트 인스턴스 반환"""
        if self._client is None:
            raise QdrantConnectionError("클라이언트가 초기화되지 않았습니다")
        return self._client

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def health_check(self) -> bool:
        """
        헬스체크

        Returns:
            서버 상태 정상 여부
        """
        try:
            # 간단한 API 호출로 연결 테스트
            self._client.get_collections()
            return True
        except Exception as e:
            logger.warning(f"헬스체크 실패: {e}")
            return False

    def list_collections(self) -> List[str]:
        """
        컬렉션 목록 조회

        Returns:
            컬렉션 이름 리스트
        """
        try:
            collections = self.client.get_collections()
            return [col.name for col in collections.collections]
        except Exception as e:
            logger.error(f"컬렉션 목록 조회 실패: {e}")
            raise QdrantConnectionError(f"컬렉션 목록 조회 실패: {str(e)}")

    def get_collection_info(self, collection_name: str) -> CollectionInfo:
        """
        컬렉션 정보 조회

        Args:
            collection_name: 컬렉션 이름

        Returns:
            CollectionInfo 객체
        """
        try:
            info = self.client.get_collection(collection_name)

            return CollectionInfo(
                name=collection_name,
                vector_size=info.config.params.vectors.size,
                distance=info.config.params.vectors.distance.name,
                points_count=info.points_count,
                indexed_vectors_count=info.indexed_vectors_count or 0,
                status=info.status.name
            )
        except Exception as e:
            logger.error(f"컬렉션 정보 조회 실패: {e}")
            raise

    def close(self):
        """클라이언트 연결 종료"""
        if self._client:
            logger.info("Qdrant 클라이언트 연결 종료")
            self._client.close()
            self._client = None

    def __enter__(self):
        """Context manager 진입"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager 종료"""
        self.close()

    def __repr__(self):
        status = "connected" if self._client else "disconnected"
        return f"QdrantClientManager(host={self.host}, port={self.port}, status={status})"
