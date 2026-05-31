"""
Level 1-2: Collection Management

이 모듈은 Milvus Collection의 전체 라이프사이클을 다룹니다:
- Schema 설계 및 생성
- Field types (vector, scalar)
- Index 생성 및 관리
- Collection CRUD 작업

Production-ready 스키마 설계 패턴을 학습합니다.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

sys.path.append(str(Path(__file__).parent.parent))

from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    utility,
)

from config.settings import settings
from utils.connection import get_milvus_client
from utils.decorators import timing_decorator
from utils.exceptions import MilvusOperationError
from utils.logger import get_logger

logger = get_logger(__name__)


class CollectionManager:
    """Production-ready Collection management class."""

    def __init__(self):
        """Initialize collection manager with connection pool."""
        self.pool = get_milvus_client()

    @timing_decorator
    def create_simple_collection(
        self,
        collection_name: str,
        dim: int = 128,
        description: str = "",
    ) -> Collection:
        """
        간단한 Collection 생성 (기본 스키마)

        Args:
            collection_name: Collection 이름
            dim: 벡터 차원
            description: Collection 설명

        Returns:
            생성된 Collection 객체

        Schema:
        - id: INT64 (primary key, auto_id)
        - embedding: FLOAT_VECTOR (dim)
        """
        logger.info("creating_simple_collection", name=collection_name, dim=dim)

        with self.pool.get_connection_context() as conn:
            # 이미 존재하는지 확인
            if utility.has_collection(collection_name, using=conn.alias):
                logger.warning("collection_already_exists", name=collection_name)
                return Collection(collection_name, using=conn.alias)

            # Field 정의
            fields = [
                FieldSchema(
                    name="id",
                    dtype=DataType.INT64,
                    is_primary=True,
                    auto_id=True,
                    description="Primary key",
                ),
                FieldSchema(
                    name="embedding",
                    dtype=DataType.FLOAT_VECTOR,
                    dim=dim,
                    description=f"{dim}-dimensional embedding vector",
                ),
            ]

            # Schema 생성
            schema = CollectionSchema(
                fields=fields,
                description=description or f"Simple collection with {dim}D vectors",
            )

            # Collection 생성
            collection = Collection(
                name=collection_name,
                schema=schema,
                using=conn.alias,
            )

            logger.info(
                "collection_created",
                name=collection_name,
                fields=len(fields),
            )

            return collection

    @timing_decorator
    def create_advanced_collection(
        self,
        collection_name: str,
        dim: int = 256,
        description: str = "",
    ) -> Collection:
        """
        고급 Collection 생성 (스칼라 필드 포함)

        Schema:
        - id: INT64 (primary key, auto_id)
        - title: VARCHAR (256)
        - category: VARCHAR (64)
        - price: FLOAT
        - stock: INT32
        - tags: ARRAY<VARCHAR>
        - metadata: JSON
        - embedding: FLOAT_VECTOR (dim)
        - created_at: INT64 (timestamp)
        """
        logger.info("creating_advanced_collection", name=collection_name, dim=dim)

        with self.pool.get_connection_context() as conn:
            if utility.has_collection(collection_name, using=conn.alias):
                logger.warning("collection_already_exists", name=collection_name)
                return Collection(collection_name, using=conn.alias)

            # 풍부한 스키마 정의
            fields = [
                # Primary key
                FieldSchema(
                    name="id",
                    dtype=DataType.INT64,
                    is_primary=True,
                    auto_id=True,
                ),
                # Text fields
                FieldSchema(
                    name="title",
                    dtype=DataType.VARCHAR,
                    max_length=256,
                    description="Item title",
                ),
                FieldSchema(
                    name="category",
                    dtype=DataType.VARCHAR,
                    max_length=64,
                    description="Item category",
                ),
                # Numeric fields
                FieldSchema(
                    name="price",
                    dtype=DataType.FLOAT,
                    description="Item price",
                ),
                FieldSchema(
                    name="stock",
                    dtype=DataType.INT32,
                    description="Stock quantity",
                ),
                # Array field
                FieldSchema(
                    name="tags",
                    dtype=DataType.ARRAY,
                    element_type=DataType.VARCHAR,
                    max_capacity=10,
                    max_length=32,
                    description="Item tags",
                ),
                # JSON field for flexible metadata
                FieldSchema(
                    name="metadata",
                    dtype=DataType.JSON,
                    description="Additional metadata",
                ),
                # Vector field
                FieldSchema(
                    name="embedding",
                    dtype=DataType.FLOAT_VECTOR,
                    dim=dim,
                    description="Product embedding vector",
                ),
                # Timestamp
                FieldSchema(
                    name="created_at",
                    dtype=DataType.INT64,
                    description="Creation timestamp",
                ),
            ]

            schema = CollectionSchema(
                fields=fields,
                description=description or "Advanced e-commerce product collection",
                enable_dynamic_field=True,  # 동적 필드 지원
            )

            collection = Collection(
                name=collection_name,
                schema=schema,
                using=conn.alias,
            )

            logger.info(
                "advanced_collection_created",
                name=collection_name,
                fields=len(fields),
            )

            return collection

    @timing_decorator
    def create_index(
        self,
        collection_name: str,
        field_name: str = "embedding",
        index_type: str = "HNSW",
        metric_type: str = "L2",
        index_params: Optional[dict] = None,
    ):
        """
        Collection에 Index 생성

        Args:
            collection_name: Collection 이름
            field_name: Index를 생성할 필드
            index_type: Index 타입 (FLAT, IVF_FLAT, HNSW 등)
            metric_type: 거리 메트릭 (L2, IP, COSINE)
            index_params: Index 파라미터

        Index Types:
        - FLAT: 전수조사, 100% 정확도, 느림
        - IVF_FLAT: 중간 속도, 높은 정확도
        - IVF_SQ8: 빠름, 메모리 절약, 약간 낮은 정확도
        - HNSW: 매우 빠름, 높은 정확도, 메모리 많이 사용
        """
        logger.info(
            "creating_index",
            collection=collection_name,
            field=field_name,
            index_type=index_type,
            metric=metric_type,
        )

        with self.pool.get_connection_context() as conn:
            collection = Collection(collection_name, using=conn.alias)

            # 기본 index 파라미터
            if index_params is None:
                if index_type == "HNSW":
                    index_params = {
                        "M": 16,  # 연결 수
                        "efConstruction": 200,  # 구축 시 탐색 깊이
                    }
                elif index_type == "IVF_FLAT":
                    index_params = {
                        "nlist": 128,  # 클러스터 수
                    }
                elif index_type == "IVF_SQ8":
                    index_params = {
                        "nlist": 128,
                    }
                else:  # FLAT
                    index_params = {}

            # Index 파라미터 구성
            index_config = {
                "index_type": index_type,
                "metric_type": metric_type,
                "params": index_params,
            }

            # Index 생성
            collection.create_index(
                field_name=field_name,
                index_params=index_config,
            )

            logger.info(
                "index_created",
                collection=collection_name,
                field=field_name,
                params=index_config,
            )

            # Index 로드 대기
            collection.load()
            logger.info("collection_loaded", collection=collection_name)

    @timing_decorator
    def describe_collection(self, collection_name: str) -> dict:
        """
        Collection 정보 조회

        Returns:
            Collection 상세 정보
        """
        with self.pool.get_connection_context() as conn:
            if not utility.has_collection(collection_name, using=conn.alias):
                raise MilvusOperationError(f"Collection '{collection_name}' does not exist")

            collection = Collection(collection_name, using=conn.alias)

            # 상세 정보 수집
            info = {
                "name": collection_name,
                "description": collection.description,
                "num_entities": collection.num_entities,
                "schema": {
                    "fields": [
                        {
                            "name": field.name,
                            "type": field.dtype.name,
                            "is_primary": field.is_primary,
                            "auto_id": field.auto_id if hasattr(field, "auto_id") else False,
                            "description": field.description,
                        }
                        for field in collection.schema.fields
                    ],
                    "enable_dynamic_field": collection.schema.enable_dynamic_field,
                },
                "indexes": [],
            }

            # Index 정보 (있다면)
            try:
                for field in collection.schema.fields:
                    if field.dtype in [DataType.FLOAT_VECTOR, DataType.BINARY_VECTOR]:
                        index_info = collection.index(field.name)
                        if index_info:
                            info["indexes"].append({
                                "field": field.name,
                                "params": index_info.params,
                            })
            except:
                pass

            logger.info(
                "collection_described",
                name=collection_name,
                entities=info["num_entities"],
                fields=len(info["schema"]["fields"]),
            )

            return info

    @timing_decorator
    def list_collections(self) -> List[str]:
        """모든 Collection 리스트 조회"""
        with self.pool.get_connection_context() as conn:
            collections = utility.list_collections(using=conn.alias)
            logger.info("collections_listed", count=len(collections))
            return collections

    @timing_decorator
    def drop_collection(self, collection_name: str):
        """Collection 삭제"""
        with self.pool.get_connection_context() as conn:
            if utility.has_collection(collection_name, using=conn.alias):
                utility.drop_collection(collection_name, using=conn.alias)
                logger.info("collection_dropped", name=collection_name)
            else:
                logger.warning("collection_not_found", name=collection_name)


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="Milvus Collection Management")
    parser.add_argument(
        "--action",
        type=str,
        choices=["create", "describe", "list", "drop", "demo"],
        default="demo",
        help="Action to perform",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="demo_collection",
        help="Collection name",
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["simple", "advanced"],
        default="simple",
        help="Collection type",
    )
    parser.add_argument(
        "--dim",
        type=int,
        default=128,
        help="Vector dimension",
    )

    args = parser.parse_args()

    logger.info(
        "starting_collection_management",
        action=args.action,
        name=args.name,
    )

    manager = CollectionManager()

    try:
        if args.action == "create":
            # Collection 생성
            if args.type == "simple":
                collection = manager.create_simple_collection(args.name, args.dim)
            else:
                collection = manager.create_advanced_collection(args.name, args.dim)

            # Index 생성
            manager.create_index(
                args.name,
                index_type=settings.index_type,
                metric_type=settings.metric_type,
            )

            print(f"✓ Collection '{args.name}' created successfully")

        elif args.action == "describe":
            # Collection 정보 조회
            info = manager.describe_collection(args.name)

            print(f"\n{'='*60}")
            print(f"Collection: {info['name']}")
            print(f"{'='*60}")
            print(f"Description: {info['description']}")
            print(f"Entities: {info['num_entities']:,}")
            print(f"\nFields:")
            for field in info['schema']['fields']:
                pk = " (PRIMARY KEY)" if field['is_primary'] else ""
                auto = " [AUTO_ID]" if field.get('auto_id') else ""
                print(f"  - {field['name']}: {field['type']}{pk}{auto}")

            if info['indexes']:
                print(f"\nIndexes:")
                for idx in info['indexes']:
                    print(f"  - {idx['field']}: {idx['params']}")

        elif args.action == "list":
            # 모든 Collection 리스트
            collections = manager.list_collections()

            print(f"\n{'='*60}")
            print(f"Total Collections: {len(collections)}")
            print(f"{'='*60}")

            for i, name in enumerate(collections, 1):
                try:
                    info = manager.describe_collection(name)
                    print(f"{i}. {name}")
                    print(f"   Entities: {info['num_entities']:,}")
                    print(f"   Fields: {len(info['schema']['fields'])}")
                except:
                    print(f"{i}. {name} (details unavailable)")

        elif args.action == "drop":
            # Collection 삭제
            manager.drop_collection(args.name)
            print(f"✓ Collection '{args.name}' dropped successfully")

        elif args.action == "demo":
            # 데모: 두 가지 타입의 Collection 생성
            print("\n" + "="*60)
            print("DEMO: Creating Sample Collections")
            print("="*60 + "\n")

            # 1. Simple collection
            print("1. Creating simple collection...")
            simple_name = "demo_simple"
            manager.create_simple_collection(simple_name, dim=128)
            manager.create_index(simple_name, index_type="HNSW")
            print(f"   ✓ Created: {simple_name}")

            # 2. Advanced collection
            print("\n2. Creating advanced collection...")
            advanced_name = "demo_advanced"
            manager.create_advanced_collection(advanced_name, dim=256)
            manager.create_index(advanced_name, index_type="IVF_FLAT")
            print(f"   ✓ Created: {advanced_name}")

            # 3. 정보 출력
            print("\n3. Collection Details:")
            for name in [simple_name, advanced_name]:
                info = manager.describe_collection(name)
                print(f"\n   {name}:")
                print(f"   - Fields: {len(info['schema']['fields'])}")
                print(f"   - Indexes: {len(info['indexes'])}")

            print("\n" + "="*60)
            print("Demo completed! Collections created:")
            print(f"  - {simple_name}")
            print(f"  - {advanced_name}")
            print("\nCleanup: Run with --action drop --name <collection_name>")
            print("="*60)

        return 0

    except Exception as e:
        logger.error(
            "operation_failed",
            action=args.action,
            error=str(e),
            error_type=type(e).__name__,
        )
        print(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
