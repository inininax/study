"""
Level 2-2: Partition Management

Partition 생성 및 관리:
- Partition 생성 및 조회
- 파티션 기반 멀티테넌시 (테넌트별 데이터 격리)
- 파티션 범위 검색 (Query Scoping)
- 파티션 간 데이터 이동 및 정리

Production 환경에서의 데이터 격리 전략을 학습합니다.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    Partition,
    utility,
)

from config.settings import settings
from utils.connection import get_milvus_client
from utils.decorators import timing_decorator
from utils.logger import get_logger

logger = get_logger(__name__)


class PartitionManager:
    """Partition 기반 테넌트 격리 매니저."""

    def __init__(self, collection_name: str = "demo_partitions", dim: int = 128):
        """
        Args:
            collection_name: 관리 대상 Collection 이름
            dim: 벡터 차원
        """
        self.collection_name = collection_name
        self.dim = dim
        self.pool = get_milvus_client()

    def _generate_random_vectors(self, count: int, seed: Optional[int] = None) -> np.ndarray:
        """
        랜덤 벡터 생성 (L2 정규화)

        Args:
            count: 생성할 벡터 수
            seed: 재현성을 위한 시드

        Returns:
            (count, dim) shape의 numpy array
        """
        rng = np.random.default_rng(seed)
        vectors = rng.random((count, self.dim)).astype(np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms

    def ensure_collection(self) -> Collection:
        """
        데모용 Collection 확보 (없으면 생성)

        Schema:
        - id: INT64 (primary key, auto_id)
        - tenant: VARCHAR (테넌트 식별자)
        - embedding: FLOAT_VECTOR (dim)
        """
        with self.pool.get_connection_context() as conn:
            if utility.has_collection(self.collection_name, using=conn.alias):
                return Collection(self.collection_name, using=conn.alias)

            fields = [
                FieldSchema(
                    name="id",
                    dtype=DataType.INT64,
                    is_primary=True,
                    auto_id=True,
                    description="Primary key",
                ),
                FieldSchema(
                    name="tenant",
                    dtype=DataType.VARCHAR,
                    max_length=64,
                    description="Tenant identifier",
                ),
                FieldSchema(
                    name="embedding",
                    dtype=DataType.FLOAT_VECTOR,
                    dim=self.dim,
                    description=f"{self.dim}-dimensional embedding vector",
                ),
            ]

            schema = CollectionSchema(
                fields=fields,
                description="Partition management demo collection",
            )

            collection = Collection(
                name=self.collection_name,
                schema=schema,
                using=conn.alias,
            )

            # 검색 성능을 위한 기본 Index
            collection.create_index(
                field_name="embedding",
                index_params={
                    "index_type": "HNSW",
                    "metric_type": "L2",
                    "params": {"M": 16, "efConstruction": 200},
                },
            )

            logger.info("collection_created", name=self.collection_name)
            return collection

    @timing_decorator
    def create_partition(self, partition_name: str) -> bool:
        """
        Partition 생성

        Args:
            partition_name: Partition 이름 (예: 테넌트 ID)

        Returns:
            생성 여부 (이미 존재하면 False)
        """
        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            if collection.has_partition(partition_name):
                logger.warning("partition_already_exists", partition=partition_name)
                return False

            collection.create_partition(partition_name=partition_name)
            logger.info("partition_created", partition=partition_name)
            return True

    def list_partitions(self) -> List[str]:
        """모든 Partition 이름 조회 (_default 포함)"""
        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)
            names = [p.name for p in collection.partitions]
            logger.info("partitions_listed", count=len(names))
            return names

    def has_partition(self, partition_name: str) -> bool:
        """Partition 존재 여부 확인"""
        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)
            return collection.has_partition(partition_name)

    @timing_decorator
    def insert_to_partition(
        self,
        vectors: np.ndarray,
        partition_name: str,
        tenant: str,
    ) -> List[int]:
        """
        특정 Partition으로 직접 삽입 (테넌트 격리 핵심)

        컬럼(columnar) 형식으로 데이터를 구성한다.
        auto_id PK 이므로 id 필드는 제외하고 나머지 필드만 컬럼 단위로 전달.

        Args:
            vectors: 삽입할 벡터들 (n, dim)
            partition_name: 삽입 대상 Partition
            tenant: tenant 필드 값

        Returns:
            생성된 primary key 리스트
        """
        count = len(vectors)

        # 컬럼(columnar) 단위 데이터 구성
        data = {
            "tenant": [tenant] * count,
            "embedding": vectors.tolist(),
        }

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            mutation_result = collection.insert(
                data,
                partition_name=partition_name,
            )
            collection.flush()

            logger.info(
                "partition_insert_completed",
                partition=partition_name,
                count=mutation_result.insert_count,
            )
            return mutation_result.primary_keys

    @timing_decorator
    def search_in_partition(
        self,
        query_vector: np.ndarray,
        partition_names: List[str],
        top_k: int = None,
    ) -> List[dict]:
        """
        Partition 범위 검색 (Query Scoping)

        partition_names 를 지정하면 해당 파티션에서만 검색하므로
        테넌트 간 데이터 누출이 원천적으로 차단된다.

        Args:
            query_vector: 쿼리 벡터
            partition_names: 검색 대상 Partition 목록
            top_k: 결과 수
        """
        if top_k is None:
            top_k = settings.search_topk

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            if not collection.is_loaded:
                collection.load()

            results = collection.search(
                data=[query_vector.tolist()],
                anns_field="embedding",
                param={"metric_type": "L2"},
                limit=top_k,
                partition_names=partition_names,
                output_fields=["tenant"],
            )

            parsed_results = []
            for hits in results:
                for hit in hits:
                    parsed_results.append({
                        "id": hit.id,
                        "distance": hit.distance,
                        "tenant": hit.entity.get("tenant"),
                        "partition": hits.partition_name if hasattr(hits, "partition_name") else partition_names[0],
                    })

            logger.info(
                "partition_scoped_search_completed",
                partitions=partition_names,
                count=len(parsed_results),
            )
            return parsed_results

    def get_partition_stats(self, partition_name: str) -> dict:
        """
        Partition 통계 조회 (데이터 격리 상태 점검)

        Args:
            partition_name: Partition 이름

        Returns:
            행 수 등 통계 정보
        """
        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)
            partition = Partition(collection, partition_name, using=conn.alias)

            stats = {
                "name": partition.name,
                "num_entities": partition.num_entities,
            }
            logger.info("partition_stats_retrieved", **stats)
            return stats

    @timing_decorator
    def move_data_between_partitions(
        self,
        source_partition: str,
        target_partition: str,
        limit: int = 100,
    ) -> dict:
        """
        Partition 간 데이터 이동 (copy + delete 패턴)

        Milvus는 파티션 간 직접 이동 API 가 없으므로
        1) source 에서 데이터 읽기 -> 2) target 에 삽입 -> 3) source 에서 삭제
        순서로 처리한다. 장애 시 재수행 가능하도록 delete 를 마지막에 실행.

        Args:
            source_partition: 원본 Partition
            target_partition: 대상 Partition
            limit: 이동할 최대 행 수

        Returns:
            이동 통계
        """
        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            # 1. source 파티션에서 id + tenant + embedding 읽기
            rows = collection.query(
                expr="id >= 0",
                partition_names=[source_partition],
                output_fields=["tenant", "embedding"],
                limit=limit,
            )

            if not rows:
                logger.warning(
                    "partition_move_nothing_to_move",
                    source=source_partition,
                )
                return {"moved": 0}

            moved_ids = [row["id"] for row in rows]
            tenants = [row["tenant"] for row in rows]
            embeddings = [row["embedding"] for row in rows]

            # 2. target 파티션에 삽입 (컬럼 형식 유지)
            data = {
                "tenant": tenants,
                "embedding": embeddings,
            }
            collection.insert(data, partition_name=target_partition)
            collection.flush()

            # 3. source 파티션에서 삭제 (id in [...]) - 실패해도 target 에 데이터가 있으므로 재시도 가능
            delete_expr = f"id in {moved_ids}"
            collection.delete(expr=delete_expr, partition_name=source_partition)
            collection.flush()

            logger.info(
                "partition_move_completed",
                source=source_partition,
                target=target_partition,
                moved=len(moved_ids),
            )
            return {"moved": len(moved_ids)}

    @timing_decorator
    def drop_partition(self, partition_name: str):
        """
        Partition 삭제 (대량 데이터 정리에 유용 - row 단위 삭제보다 훨씬 빠름)

        Args:
            partition_name: 삭제할 Partition 이름
        """
        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            if not collection.has_partition(partition_name):
                logger.warning("partition_not_found", partition=partition_name)
                return

            collection.drop_partition(partition_name)
            logger.info("partition_dropped", partition=partition_name)


def main():
    """메인 실행 함수 - 전체 파티션 라이프사이클 데모"""
    parser = argparse.ArgumentParser(description="Milvus Partition Management")
    parser.add_argument(
        "--collection",
        type=str,
        default="demo_partitions",
        help="Collection name",
    )
    parser.add_argument(
        "--per-partition",
        type=int,
        default=100,
        help="Vectors to insert per partition",
    )
    args = parser.parse_args()

    manager = PartitionManager(args.collection)

    try:
        print("\n" + "=" * 60)
        print("PARTITION MANAGEMENT DEMO")
        print("=" * 60)

        # 1. Collection 및 파티션 준비
        manager.ensure_collection()
        for tenant in ["tenant_a", "tenant_b"]:
            manager.create_partition(tenant)
        print(f"\nPartitions: {manager.list_partitions()}")

        # 2. 파티션별 데이터 삽입 (테넌트 격리)
        for i, tenant in enumerate(["tenant_a", "tenant_b"]):
            vectors = manager._generate_random_vectors(args.per_partition, seed=i)
            manager.insert_to_partition(vectors, partition_name=tenant, tenant=tenant)

        # 3. 파티션 통계 확인
        for tenant in ["tenant_a", "tenant_b"]:
            stats = manager.get_partition_stats(tenant)
            print(f"Stats [{stats['name']}]: {stats['num_entities']} entities")

        # 4. 파티션 범위 검색 - tenant_a 파티션에서만 검색
        query_vector = manager._generate_random_vectors(1, seed=99)[0]
        results = manager.search_in_partition(
            query_vector,
            partition_names=["tenant_a"],
            top_k=5,
        )
        print(f"\nScoped search in 'tenant_a' (top 5):")
        for r in results:
            print(f"  id={r['id']} distance={r['distance']:.4f} tenant={r['tenant']}")

        # 5. 파티션 간 데이터 이동 (tenant_a -> tenant_b 일부 이동 후 되돌리기)
        moved = manager.move_data_between_partitions("tenant_a", "tenant_b", limit=10)
        print(f"\nMoved {moved['moved']} rows: tenant_a -> tenant_b")
        manager.move_data_between_partitions("tenant_b", "tenant_a", limit=moved["moved"])

        # 6. 정리 - 파티션 삭제는 row 삭제보다 훨씬 빠르다
        # manager.drop_partition("tenant_b")

        print("\n" + "=" * 60)
        print("PARTITION MANAGEMENT DEMO COMPLETED")
        print("=" * 60)
        return 0

    except Exception as e:
        logger.error(
            "partition_demo_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        print(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
