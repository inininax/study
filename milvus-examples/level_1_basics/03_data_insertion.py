"""
Level 1-3: Data Insertion

이 모듈은 Milvus에 데이터를 삽입하는 다양한 방법을 다룹니다:
- 단건 삽입
- 배치 삽입
- 대용량 데이터 처리
- 삽입 성능 최적화
- 에러 처리 및 복구

Production 환경에서의 대용량 데이터 처리 패턴을 학습합니다.
"""

import argparse
import sys
import time
from pathlib import Path
from typing import List

import numpy as np
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))

from pymilvus import Collection

from config.settings import settings
from utils.connection import get_milvus_client
from utils.decorators import timing_decorator
from utils.logger import get_logger

logger = get_logger(__name__)


class DataInserter:
    """Production-ready data insertion manager."""

    def __init__(self, collection_name: str = "demo_simple"):
        """Initialize data inserter."""
        self.collection_name = collection_name
        self.pool = get_milvus_client()
        self.dim = 128  # Default dimension

    def _generate_random_vectors(self, count: int, dim: int = None) -> np.ndarray:
        """
        랜덤 벡터 생성

        Args:
            count: 생성할 벡터 수
            dim: 벡터 차원

        Returns:
            (count, dim) shape의 numpy array
        """
        if dim is None:
            dim = self.dim

        # 정규화된 랜덤 벡터 생성
        vectors = np.random.rand(count, dim).astype(np.float32)

        # L2 정규화
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        vectors = vectors / norms

        return vectors

    @timing_decorator
    def insert_single(self, vector: np.ndarray) -> int:
        """
        단건 삽입

        Args:
            vector: 삽입할 벡터

        Returns:
            삽입된 ID
        """
        logger.info("inserting_single_vector", dim=len(vector))

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            # 데이터 준비 - list 형식은 컬럼 단위이므로 벡터 리스트의 리스트여야 함
            data = [[vector.tolist()]]

            # 삽입
            mutation_result = collection.insert(data)

            # Flush to persist
            collection.flush()

            logger.info(
                "single_vector_inserted",
                insert_count=mutation_result.insert_count,
                primary_keys=mutation_result.primary_keys,
            )

            return mutation_result.primary_keys[0]

    @timing_decorator
    def insert_batch(
        self,
        vectors: np.ndarray,
        batch_size: int = None,
    ) -> List[int]:
        """
        배치 삽입

        Args:
            vectors: 삽입할 벡터들 (n, dim)
            batch_size: 배치 크기

        Returns:
            삽입된 ID 리스트
        """
        if batch_size is None:
            batch_size = settings.batch_size

        total_count = len(vectors)
        logger.info(
            "starting_batch_insert",
            total_vectors=total_count,
            batch_size=batch_size,
        )

        all_ids = []

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            # 배치로 분할하여 삽입
            for i in range(0, total_count, batch_size):
                batch_end = min(i + batch_size, total_count)
                batch_vectors = vectors[i:batch_end]

                # 데이터 준비
                data = [batch_vectors.tolist()]

                # 삽입
                mutation_result = collection.insert(data)
                all_ids.extend(mutation_result.primary_keys)

                logger.info(
                    "batch_inserted",
                    batch_num=i // batch_size + 1,
                    batch_size=len(batch_vectors),
                    total_inserted=len(all_ids),
                )

            # Flush
            collection.flush()

            logger.info(
                "batch_insert_completed",
                total_inserted=len(all_ids),
            )

        return all_ids

    @timing_decorator
    def insert_large_dataset(
        self,
        total_count: int,
        batch_size: int = None,
        show_progress: bool = True,
    ) -> dict:
        """
        대용량 데이터셋 삽입

        Args:
            total_count: 총 삽입할 벡터 수
            batch_size: 배치 크기
            show_progress: 진행바 표시 여부

        Returns:
            삽입 통계
        """
        if batch_size is None:
            batch_size = settings.batch_size

        logger.info(
            "starting_large_dataset_insert",
            total_count=total_count,
            batch_size=batch_size,
        )

        start_time = time.time()
        all_ids = []
        num_batches = (total_count + batch_size - 1) // batch_size

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            # 진행바 설정
            iterator = range(num_batches)
            if show_progress:
                iterator = tqdm(
                    iterator,
                    desc="Inserting batches",
                    unit="batch",
                )

            for batch_idx in iterator:
                # 현재 배치 크기 계산
                current_batch_size = min(
                    batch_size,
                    total_count - batch_idx * batch_size,
                )

                # 랜덤 벡터 생성
                vectors = self._generate_random_vectors(current_batch_size)

                # 데이터 준비 및 삽입
                data = [vectors.tolist()]

                try:
                    mutation_result = collection.insert(data)
                    all_ids.extend(mutation_result.primary_keys)

                    # 주기적으로 flush (메모리 관리)
                    if (batch_idx + 1) % 10 == 0:
                        collection.flush()

                except Exception as e:
                    logger.error(
                        "batch_insert_failed",
                        batch_idx=batch_idx,
                        error=str(e),
                    )
                    # 에러 발생 시 현재까지 데이터 flush
                    collection.flush()
                    raise

            # 최종 flush
            collection.flush()

        elapsed_time = time.time() - start_time

        # 통계 계산
        stats = {
            "total_inserted": len(all_ids),
            "elapsed_time_seconds": elapsed_time,
            "vectors_per_second": len(all_ids) / elapsed_time,
            "batch_size": batch_size,
            "num_batches": num_batches,
        }

        logger.info(
            "large_dataset_insert_completed",
            **stats,
        )

        return stats

    @timing_decorator
    def insert_with_metadata(
        self,
        count: int,
        include_scalars: bool = True,
    ) -> List[int]:
        """
        메타데이터와 함께 삽입 (advanced collection용)

        Args:
            count: 삽입할 데이터 수
            include_scalars: 스칼라 필드 포함 여부

        Returns:
            삽입된 ID 리스트
        """
        logger.info(
            "inserting_with_metadata",
            count=count,
            include_scalars=include_scalars,
        )

        # 데이터 생성
        vectors = self._generate_random_vectors(count, dim=256)

        data = {
            "embedding": vectors.tolist(),
        }

        if include_scalars:
            data.update({
                "title": [f"Product {i}" for i in range(count)],
                "category": [
                    np.random.choice(["Electronics", "Books", "Clothing", "Food"])
                    for _ in range(count)
                ],
                "price": np.random.uniform(10, 1000, count).tolist(),
                "stock": np.random.randint(0, 100, count).tolist(),
                "tags": [
                    [f"tag{j}" for j in range(np.random.randint(1, 4))]
                    for _ in range(count)
                ],
                "metadata": [
                    {"brand": f"Brand{i % 10}", "weight": float(np.random.rand())}
                    for i in range(count)
                ],
                "created_at": [int(time.time()) for _ in range(count)],
            })

        with self.pool.get_connection_context() as conn:
            collection = Collection("demo_advanced", using=conn.alias)

            # 삽입
            mutation_result = collection.insert(data)
            collection.flush()

            logger.info(
                "metadata_insert_completed",
                count=mutation_result.insert_count,
            )

            return mutation_result.primary_keys

    @timing_decorator
    def benchmark_insertion(
        self,
        sizes: List[int] = None,
        batch_sizes: List[int] = None,
    ) -> dict:
        """
        삽입 성능 벤치마크

        Args:
            sizes: 테스트할 데이터 크기 리스트
            batch_sizes: 테스트할 배치 크기 리스트

        Returns:
            벤치마크 결과
        """
        if sizes is None:
            sizes = [100, 1000, 10000]

        if batch_sizes is None:
            batch_sizes = [100, 500, 1000, 2000]

        logger.info(
            "starting_insertion_benchmark",
            sizes=sizes,
            batch_sizes=batch_sizes,
        )

        results = {}

        for size in sizes:
            results[size] = {}

            for batch_size in batch_sizes:
                logger.info(
                    "benchmark_iteration",
                    size=size,
                    batch_size=batch_size,
                )

                # 벡터 생성
                vectors = self._generate_random_vectors(size)

                # 삽입 벤치마크
                start_time = time.time()
                self.insert_batch(vectors, batch_size=batch_size)
                elapsed = time.time() - start_time

                results[size][batch_size] = {
                    "elapsed_seconds": elapsed,
                    "vectors_per_second": size / elapsed,
                }

        logger.info("benchmark_completed", results=results)
        return results


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="Milvus Data Insertion")
    parser.add_argument(
        "--size",
        type=str,
        choices=["small", "medium", "large", "xlarge"],
        default="small",
        help="Dataset size",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="demo_simple",
        help="Collection name",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Batch size",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run benchmark",
    )

    args = parser.parse_args()

    logger.info(
        "starting_data_insertion",
        size=args.size,
        collection=args.collection,
    )

    inserter = DataInserter(args.collection)

    try:
        if args.benchmark:
            # 벤치마크 실행
            print("\n" + "="*60)
            print("INSERTION BENCHMARK")
            print("="*60 + "\n")

            results = inserter.benchmark_insertion(
                sizes=[1000, 5000, 10000],
                batch_sizes=[500, 1000, 2000],
            )

            # 결과 출력
            print("\nResults:")
            print(f"{'Size':>10} | {'Batch':>10} | {'Time (s)':>12} | {'Vec/s':>12}")
            print("-" * 60)

            for size, batch_results in results.items():
                for batch_size, metrics in batch_results.items():
                    print(
                        f"{size:>10,} | {batch_size:>10,} | "
                        f"{metrics['elapsed_seconds']:>12.2f} | "
                        f"{metrics['vectors_per_second']:>12,.0f}"
                    )

        else:
            # 크기별 삽입
            size_map = {
                "small": 1_000,
                "medium": 10_000,
                "large": 100_000,
                "xlarge": 1_000_000,
            }

            count = size_map[args.size]

            print(f"\nInserting {count:,} vectors into '{args.collection}'...")
            print(f"Batch size: {args.batch_size:,}\n")

            stats = inserter.insert_large_dataset(
                total_count=count,
                batch_size=args.batch_size,
                show_progress=True,
            )

            # 결과 출력
            print("\n" + "="*60)
            print("INSERTION COMPLETED")
            print("="*60)
            print(f"Total vectors: {stats['total_inserted']:,}")
            print(f"Elapsed time: {stats['elapsed_time_seconds']:.2f} seconds")
            print(f"Throughput: {stats['vectors_per_second']:,.0f} vectors/second")
            print(f"Batch size: {stats['batch_size']:,}")
            print(f"Total batches: {stats['num_batches']:,}")
            print("="*60)

        return 0

    except Exception as e:
        logger.error(
            "insertion_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        print(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
