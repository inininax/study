"""
Level 2-4: Data Migration

데이터 마이그레이션 전략:
- Collection 백업 및 복구
- 스키마 변경 마이그레이션 (차원 축소 등)
- 데이터 정합성 검증
- Alias 기반 Zero-downtime 전환 및 롤백

Production 환경의 무중단 마이그레이션 패턴을 학습합니다.
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Callable, List, Optional

import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    utility,
)

from utils.connection import get_milvus_client
from utils.decorators import timing_decorator
from utils.logger import get_logger

logger = get_logger(__name__)


class DataMigrator:
    """Collection 데이터 마이그레이션 매니저."""

    def __init__(self, dim: int = 128):
        """
        Args:
            dim: 원본 벡터 차원
        """
        self.dim = dim
        self.pool = get_milvus_client()

    def _generate_random_vectors(self, count: int, seed: Optional[int] = None) -> np.ndarray:
        """L2 정규화된 랜덤 벡터 생성"""
        rng = np.random.default_rng(seed)
        vectors = rng.random((count, self.dim)).astype(np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms

    @timing_decorator
    def ensure_source_collection(
        self,
        collection_name: str = "migration_source",
        num_vectors: int = 500,
    ) -> Collection:
        """
        마이그레이션 원본 Collection 준비

        주의: 마이그레이션 시 id 를 보존해야 하므로 auto_id=False 로 생성한다.
        (auto_id 컬렉션은 id 재지정 삽입이 불가능하다)

        Args:
            collection_name: 원본 Collection 이름
            num_vectors: 초기 데이터 수
        """
        with self.pool.get_connection_context() as conn:
            if not utility.has_collection(collection_name, using=conn.alias):
                fields = [
                    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
                    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=128),
                    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
                ]
                schema = CollectionSchema(fields=fields, description="Migration source")
                collection = Collection(collection_name, schema=schema, using=conn.alias)

                collection.create_index(
                    field_name="embedding",
                    index_params={
                        "index_type": "HNSW",
                        "metric_type": "L2",
                        "params": {"M": 16, "efConstruction": 200},
                    },
                )

            collection = Collection(collection_name, using=conn.alias)

            if collection.num_entities == 0:
                vectors = self._generate_random_vectors(num_vectors, seed=7)
                # 컬럼(columnar) 형식 - 명시적 id 포함
                data = {
                    "id": list(range(1, num_vectors + 1)),
                    "title": [f"Doc {i}" for i in range(1, num_vectors + 1)],
                    "embedding": vectors.tolist(),
                }
                collection.insert(data)
                collection.flush()

            logger.info("source_collection_ready", name=collection_name, entities=collection.num_entities)
            return collection

    @timing_decorator
    def export_data(self, source_name: str, batch_size: int = 1000) -> List[dict]:
        """
        전체 데이터 내보내기 (백업의 기반)

        offset+limit 페이징으로 모든 행을 읽는다.
        대용량에서는 query_iterator 사용을 권장한다.

        Args:
            source_name: 읽어올 Collection 이름
            batch_size: 페이지 크기

        Returns:
            row dict 리스트 ({id, title, embedding})
        """
        all_rows: List[dict] = []
        offset = 0

        with self.pool.get_connection_context() as conn:
            collection = Collection(source_name, using=conn.alias)

            # query/search 는 로드된 컬렉션에서만 가능하다
            if not collection.is_loaded:
                collection.load()

            while True:
                rows = collection.query(
                    expr="id >= 0",
                    output_fields=["id", "title", "embedding"],
                    limit=batch_size,
                    offset=offset,
                )
                all_rows.extend(rows)

                if len(rows) < batch_size:
                    break
                offset += batch_size

        logger.info("data_exported", source=source_name, rows=len(all_rows))
        return all_rows

    def _create_like(self, target_name: str, source_name: str, dim: Optional[int] = None):
        """
        원본과 동일한 스키마로 새 Collection 생성

        Args:
            target_name: 생성할 Collection 이름
            source_name: 스키마 복제 대상
            dim: 지정하면 벡터 차원만 변경 (스키마 변경 마이그레이션용)
        """
        with self.pool.get_connection_context() as conn:
            if utility.has_collection(target_name, using=conn.alias):
                utility.drop_collection(target_name, using=conn.alias)

            source = Collection(source_name, using=conn.alias)

            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
                FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=128),
                FieldSchema(
                    name="embedding",
                    dtype=DataType.FLOAT_VECTOR,
                    dim=dim or self.dim,
                ),
            ]
            schema = CollectionSchema(
                fields=fields,
                description=f"Migrated from {source_name}",
            )
            collection = Collection(target_name, schema=schema, using=conn.alias)
            collection.create_index(
                field_name="embedding",
                index_params={
                    "index_type": "HNSW",
                    "metric_type": "L2",
                    "params": {"M": 16, "efConstruction": 200},
                },
            )
            return collection

    @timing_decorator
    def backup_collection(self, source_name: str, backup_name: str) -> int:
        """
        Collection 백업 (동일 스키마 + 전체 복사)

        Args:
            source_name: 원본
            backup_name: 백업 대상

        Returns:
            복사된 행 수
        """
        rows = self.export_data(source_name)

        if not rows:
            logger.warning("backup_empty_source", source=source_name)
            return 0

        self._create_like(backup_name, source_name)

        with self.pool.get_connection_context() as conn:
            backup = Collection(backup_name, using=conn.alias)

            # 컬럼(columnar) 형식으로 변환하여 복원
            data = {
                "id": [r["id"] for r in rows],
                "title": [r["title"] for r in rows],
                "embedding": [r["embedding"] for r in rows],
            }
            backup.insert(data)
            backup.flush()

        logger.info("backup_completed", source=source_name, backup=backup_name, rows=len(rows))
        return len(rows)

    @timing_decorator
    def restore_from_backup(self, backup_name: str, target_name: str) -> int:
        """
        백업으로부터 복구 (롤백 절차)

        Args:
            backup_name: 백업 Collection
            target_name: 복구 대상 Collection

        Returns:
            복구된 행 수
        """
        return self.backup_collection(backup_name, target_name)

    @timing_decorator
    def migrate_with_schema_change(
        self,
        source_name: str,
        target_name: str,
        transform_fn: Optional[Callable[[List[float]], List[float]]] = None,
    ):
        """
        스키마 변경 마이그레이션

        읽기 -> 변환(transform_fn) -> 쓰기 파이프라인.
        transform_fn 으로 차원 축소 등 임의 변환을 적용할 수 있다.

        Args:
            source_name: 원본
            target_name: 대상 (새 스키마)
            transform_fn: embedding 변환 함수 (None 이면 차원 축소 기본 적용)
        """

        def default_transform(vector: List[float]) -> List[float]:
            # 기본 변환: 앞 절반 차원 슬라이싱 후 L2 재정규화 (128D -> 64D)
            arr = np.asarray(vector[: len(vector) // 2], dtype=np.float32)
            norm = np.linalg.norm(arr)
            return (arr / norm).tolist() if norm > 0 else arr.tolist()

        transform_fn = transform_fn or default_transform

        # 새 차원 계산을 위해 첫 행 확인
        sample_rows = self.export_data(source_name, batch_size=1)
        if not sample_rows:
            raise ValueError(f"Source '{source_name}' is empty")

        new_dim = len(transform_fn(sample_rows[0]["embedding"]))
        self.dim = len(sample_rows[0]["embedding"])
        self._create_like(target_name, source_name, dim=new_dim)

        rows = self.export_data(source_name)
        self.dim = new_dim  # _create_like 이후 target 차원에 맞춤

        with self.pool.get_connection_context() as conn:
            target = Collection(target_name, using=conn.alias)

            # 배치 단위로 나누어 쓰기 - 메모리 피크 제어
            batch = 500
            for i in range(0, len(rows), batch):
                chunk = rows[i : i + batch]
                transformed = [transform_fn(r["embedding"]) for r in chunk]

                data = {
                    "id": [r["id"] for r in chunk],
                    "title": [r["title"] for r in chunk],
                    "embedding": transformed,
                }
                target.insert(data)

            target.flush()
            logger.info(
                "schema_migration_completed",
                source=source_name,
                target=target_name,
                rows=len(rows),
                new_dim=new_dim,
            )

    def verify_migration(
        self,
        source_name: str,
        target_name: str,
        sample_size: int = 10,
    ) -> bool:
        """
        마이그레이션 정합성 검증

        1) 행 수 일치 확인
        2) 샘플 쿼리 벡터를 양쪽에서 검색해 top-1 id 일치 확인
           (거리 값은 스키마 변경 시 달라질 수 있으므로 순위 비교 사용)

        Args:
            source_name: 원본
            target_name: 대상
            sample_size: 검증할 샘플 수

        Returns:
            검증 통과 여부
        """
        with self.pool.get_connection_context() as conn:
            source = Collection(source_name, using=conn.alias)
            target = Collection(target_name, using=conn.alias)

            if not source.is_loaded:
                source.load()
            if not target.is_loaded:
                target.load()

            # 대상 컬렉션의 벡터 차원 확인 (스키마 변경 시 원본과 다를 수 있음)
            embedding_field = next(
                f for f in target.schema.fields
                if f.dtype == DataType.FLOAT_VECTOR
            )
            target_dim = (embedding_field.params or {}).get("dim") or self.dim

            # 1. 행 수 비교
            if source.num_entities != target.num_entities:
                logger.error(
                    "verification_row_count_mismatch",
                    source=source.num_entities,
                    target=target.num_entities,
                )
                return False

            # 2. 샘플 NN(최근접 이웃) 일치 검증
            sample_rows = self.export_data(source_name, batch_size=sample_size)
            mismatches = 0

            for row in sample_rows:
                vector = np.asarray(row["embedding"], dtype=np.float32)

                src_hits = source.search(
                    data=[vector.tolist()],
                    anns_field="embedding",
                    param={"metric_type": "L2"},
                    limit=1,
                )[0]

                # 차원이 다르면 원본 벡터를 target 차원으로 절단 후 검색
                tgt_vector = vector[:target_dim]
                tgt_hits = target.search(
                    data=[tgt_vector.tolist()],
                    anns_field="embedding",
                    param={"metric_type": "L2"},
                    limit=1,
                )[0]

                if src_hits[0].id != tgt_hits[0].id:
                    mismatches += 1

            passed = mismatches == 0
            logger.info(
                "migration_verified",
                source=source_name,
                target=target_name,
                samples=len(sample_rows),
                mismatches=mismatches,
                passed=passed,
            )
            return passed

    @timing_decorator
    def switch_alias(self, alias: str, new_collection: str):
        """
        Alias 기반 Zero-downtime 전환

        애플리케이션은 항상 alias 로 접근하므로 컬렉션 교체 시
        alias 만 바꾸면 된다. 문제가 생기면 즉시 되돌릴 수 있다.

        Args:
            alias: 서비스가 사용하는 alias 이름
            new_collection: 전환 대상 Collection
        """
        with self.pool.get_connection_context() as conn:
            # 기존 alias 가 있으면 alter, 없으면 create
            try:
                utility.drop_alias(alias, using=conn.alias)
            except Exception:
                pass

            utility.create_alias(new_collection, alias, using=conn.alias)
            logger.info("alias_switched", alias=alias, collection=new_collection)

    @timing_decorator
    def rollback_migration(self, alias: str, previous_collection: str, failed_collection: str):
        """
        마이그레이션 롤백

        1) alias 를 이전 컬렉션으로 되돌린다 (다운타임 없음)
        2) 실패한 신규 컬렉션은 검토 후 삭제한다

        Args:
            alias: 서비스 alias
            previous_collection: 되돌아갈 기존 Collection
            failed_collection: 문제가 있는 신규 Collection
        """
        with self.pool.get_connection_context() as conn:
            utility.drop_alias(alias, using=conn.alias)
            utility.create_alias(previous_collection, alias, using=conn.alias)

            logger.info(
                "migration_rolled_back",
                alias=alias,
                restored=previous_collection,
                kept_for_review=failed_collection,
            )


def main():
    """메인 실행 함수 - 백업/복구, 스키마 변경, 검증, alias 전환 데모"""
    parser = argparse.ArgumentParser(description="Milvus Data Migration")
    parser.add_argument("--num-vectors", type=int, default=500, help="Source dataset size")
    args = parser.parse_args()

    migrator = DataMigrator(dim=128)

    source = "migration_source"
    backup = "migration_backup"
    migrated = "migration_target_v2"
    service_alias = "migration_service"

    try:
        print("\n" + "=" * 60)
        print("DATA MIGRATION DEMO")
        print("=" * 60)

        start_time = time.time()

        # 1. 원본 준비
        migrator.ensure_source_collection(source, num_vectors=args.num_vectors)

        # 2. 백업 및 복구 리허설
        count = migrator.backup_collection(source, backup)
        print(f"\nBackup created: {backup} ({count:,} rows)")

        # 3. 스키마 변경 마이그레이션 (128D -> 64D 차원 축소)
        migrator.migrate_with_schema_change(source, migrated)
        print(f"Schema-changed migration done: {migrated} (128D -> 64D)")

        # 4. 정합성 검증
        passed = migrator.verify_migration(source, migrated, sample_size=10)
        print(f"Verification: {'PASSED' if passed else 'FAILED'}")

        # 5. Alias 전환 (zero-downtime) 및 롤백 데모
        migrator.switch_alias(service_alias, migrated)
        print(f"Alias '{service_alias}' now points to '{migrated}'")

        migrator.rollback_migration(service_alias, source, migrated)
        print(f"Rollback rehearsed: '{service_alias}' -> '{source}' ('{migrated}' kept for review)")

        elapsed = time.time() - start_time
        print("\n" + "=" * 60)
        print("MIGRATION DEMO COMPLETED")
        print("=" * 60)
        print(f"Total time: {elapsed:.2f} seconds")
        return 0

    except Exception as e:
        logger.error(
            "migration_demo_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        print(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
