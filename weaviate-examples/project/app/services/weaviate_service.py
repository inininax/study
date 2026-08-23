"""
Weaviate 서비스
================

Weaviate 클라이언트 관리 및 데이터 작업
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.init import Auth
from weaviate.classes.query import Filter, MetadataQuery
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from uuid import UUID
from datetime import datetime

from app.config import settings
from app.utils.logger import logger
from app.utils.exceptions import WeaviateException


class WeaviateService:
    """
    Weaviate 서비스 클래스

    싱글톤 패턴으로 구현하여 전역에서 하나의 인스턴스만 사용
    """

    _instance = None
    _client: Optional[weaviate.WeaviateClient] = None
    COLLECTION_NAME = "Document"

    def __new__(cls):
        """싱글톤 패턴 구현"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self):
        """Weaviate 클라이언트 초기화"""
        try:
            logger.info(f"Weaviate 연결 중: {settings.WEAVIATE_URL}")

            parsed = urlparse(settings.WEAVIATE_URL)
            host = parsed.hostname or "localhost"
            port = parsed.port or 8080
            auth = (
                Auth.api_key(settings.WEAVIATE_API_KEY)
                if settings.WEAVIATE_API_KEY
                else None
            )

            # 클라이언트 생성
            self._client = weaviate.connect_to_local(
                host=host,
                port=port,
                auth_credentials=auth,
            )

            # 헬스 체크
            if not self._client.is_ready():
                raise WeaviateException("Weaviate가 준비되지 않았습니다")

            # 컬렉션 생성
            self._setup_collection()

            logger.info("✅ Weaviate 초기화 완료")

        except Exception as e:
            logger.error(f"Weaviate 초기화 실패: {e}")
            raise WeaviateException(f"Weaviate 연결 실패: {e}")

    def _setup_collection(self):
        """문서 컬렉션 생성"""
        if self._client.collections.exists(self.COLLECTION_NAME):
            logger.info(f"컬렉션 '{self.COLLECTION_NAME}' 이미 존재")
            return

        logger.info(f"컬렉션 '{self.COLLECTION_NAME}' 생성 중...")

        self._client.collections.create(
            name=self.COLLECTION_NAME,
            description="문서 검색 컬렉션",
            properties=[
                Property(name="title", data_type=DataType.TEXT, description="제목"),
                Property(name="content", data_type=DataType.TEXT, description="내용"),
                Property(
                    name="tags", data_type=DataType.TEXT_ARRAY, description="태그"
                ),
                Property(
                    name="created_at", data_type=DataType.DATE, description="생성일"
                ),
                Property(
                    name="updated_at", data_type=DataType.DATE, description="수정일"
                ),
                Property(
                    name="view_count", data_type=DataType.INT, description="조회수"
                ),
            ],
            vectorizer_config=Configure.Vectorizer.text2vec_openai(
                model=settings.OPENAI_EMBEDDING_MODEL
            ),
        )

        logger.info(f"✅ 컬렉션 '{self.COLLECTION_NAME}' 생성 완료")

    @property
    def client(self) -> weaviate.WeaviateClient:
        """클라이언트 반환"""
        if self._client is None:
            raise WeaviateException("Weaviate가 초기화되지 않았습니다")
        return self._client

    @property
    def collection(self):
        """컬렉션 반환"""
        return self.client.collections.get(self.COLLECTION_NAME)

    def health_check(self) -> bool:
        """헬스 체크"""
        try:
            return self.client.is_ready()
        except:
            return False

    # ====================
    # CRUD 작업
    # ====================

    def create_document(
        self, title: str, content: str, tags: List[str] = None, metadata: Dict = None
    ) -> UUID:
        """문서 생성"""
        try:
            now = datetime.utcnow().isoformat() + "Z"

            properties = {
                "title": title,
                "content": content,
                "tags": tags or [],
                "created_at": now,
                "updated_at": now,
                "view_count": 0,
            }

            uuid = self.collection.data.insert(properties=properties)

            logger.info(f"문서 생성: {uuid}")
            return uuid

        except Exception as e:
            logger.error(f"문서 생성 실패: {e}")
            raise WeaviateException(f"문서 생성 실패: {e}")

    def get_document(self, doc_id: UUID) -> Optional[Dict[str, Any]]:
        """문서 조회"""
        try:
            obj = self.collection.query.fetch_object_by_id(uuid=doc_id)

            if not obj:
                return None

            # 조회수 증가
            self.collection.data.update(
                uuid=doc_id,
                properties={"view_count": obj.properties.get("view_count", 0) + 1},
            )

            return {"id": obj.uuid, **obj.properties}

        except Exception as e:
            logger.error(f"문서 조회 실패: {e}")
            raise WeaviateException(f"문서 조회 실패: {e}")

    def update_document(
        self, doc_id: UUID, title: str = None, content: str = None, tags: List[str] = None
    ):
        """문서 수정"""
        try:
            properties = {}

            if title is not None:
                properties["title"] = title
            if content is not None:
                properties["content"] = content
            if tags is not None:
                properties["tags"] = tags

            properties["updated_at"] = datetime.utcnow().isoformat() + "Z"

            self.collection.data.update(uuid=doc_id, properties=properties)

            logger.info(f"문서 수정: {doc_id}")

        except Exception as e:
            logger.error(f"문서 수정 실패: {e}")
            raise WeaviateException(f"문서 수정 실패: {e}")

    def delete_document(self, doc_id: UUID):
        """문서 삭제"""
        try:
            self.collection.data.delete_by_id(uuid=doc_id)
            logger.info(f"문서 삭제: {doc_id}")

        except Exception as e:
            logger.error(f"문서 삭제 실패: {e}")
            raise WeaviateException(f"문서 삭제 실패: {e}")

    def list_documents(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """문서 목록 조회"""
        try:
            response = self.collection.query.fetch_objects(limit=limit, offset=offset)

            return [{"id": obj.uuid, **obj.properties} for obj in response.objects]

        except Exception as e:
            logger.error(f"문서 목록 조회 실패: {e}")
            raise WeaviateException(f"문서 목록 조회 실패: {e}")

    # ====================
    # 검색 작업
    # ====================

    def semantic_search(
        self, query: str, limit: int = 10, min_certainty: float = 0.7
    ) -> List[Dict[str, Any]]:
        """의미 검색"""
        try:
            response = self.collection.query.near_text(
                query=query,
                limit=limit,
                return_metadata=MetadataQuery(distance=True, certainty=True),
            )

            results = []
            for obj in response.objects:
                if obj.metadata.certainty >= min_certainty:
                    results.append(
                        {
                            "id": obj.uuid,
                            **obj.properties,
                            "distance": obj.metadata.distance,
                            "certainty": obj.metadata.certainty,
                        }
                    )

            logger.info(f"의미 검색: '{query}' - {len(results)}개 결과")
            return results

        except Exception as e:
            logger.error(f"의미 검색 실패: {e}")
            raise WeaviateException(f"의미 검색 실패: {e}")

    def hybrid_search(
        self, query: str, limit: int = 10, alpha: float = 0.5
    ) -> List[Dict[str, Any]]:
        """하이브리드 검색"""
        try:
            response = self.collection.query.hybrid(
                query=query,
                alpha=alpha,
                limit=limit,
                return_metadata=MetadataQuery(score=True),
            )

            results = []
            for obj in response.objects:
                results.append(
                    {"id": obj.uuid, **obj.properties, "score": obj.metadata.score}
                )

            logger.info(f"하이브리드 검색: '{query}' - {len(results)}개 결과")
            return results

        except Exception as e:
            logger.error(f"하이브리드 검색 실패: {e}")
            raise WeaviateException(f"하이브리드 검색 실패: {e}")

    def close(self):
        """연결 종료"""
        if self._client:
            self._client.close()
            logger.info("Weaviate 연결 종료")


# 전역 서비스 인스턴스
weaviate_service = WeaviateService()
