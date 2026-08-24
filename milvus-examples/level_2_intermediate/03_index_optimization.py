"""
Level 2-3: Index Optimization

다양한 Index 타입 비교 및 튜닝:
- FLAT / IVF_FLAT / IVF_SQ8 / HNSW 비교
- Index 파라미터 튜닝 (nprobe, ef)
- 정확도(Recall) vs 속도(Latency) 트레이드오프 측정
- Index 재생성 전략

Production 환경의 인덱스 선택 기준을 학습합니다.
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

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


class IndexOptimizer:
    """Index 타입 비교 및 벤치마크 매니저."""

    # Index 타입별 기본 빌드 파라미터
    INDEX_CONFIGS: Dict[str, dict] = {
        "FLAT": {},  # 전수조사 - 100% recall, 느림
        "IVF_FLAT": {"nlist": 128},  # 클러스터링 - 균형형
        "IVF_SQ8": {"nlist": 128},  # 양자화 - 메모리 절약, 약간 낮은 recall
        "HNSW": {"M": 16, "efConstruction": 200},  # 그래프 기반 - 빠르고 정확, 메모리 많이 사용
    }

    # 검색 시 사용할 파라미터 (Index 타입별)
    SEARCH_PARAMS: Dict[str, dict] = {
        "FLAT": {},
        "IVF_FLAT": {"nprobe": 16},
        "IVF_SQ8": {"nprobe": 16},
        "HNSW": {"ef": 64},
    }

    def __init__(self, collection_name: str = "index_benchmark_demo", dim: int = 128):
        """
        Args:
            collection_name: 벤치마크용 Collection 이름
            dim: 벡터 차원
        """
        self.collection_name = collection_name
        self.dim = dim
        self.pool = get_milvus_client()

    def _generate_random_vectors(self, count: int, seed: Optional[int] = None) -> np.ndarray:
        """L2 정규화된 랜덤 벡터 생성"""
        rng = np.random.default_rng(seed)
        vectors = rng.random((count, self.dim)).astype(np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms

    def ensure_collection_with_data(
        self,
        num_vectors: int = 5000,
        batch_size: int = 1000,
    ) -> Collection:
        """
        벤치마크 데이터셋 준비

        Args:
            num_vectors: 삽입할 벡터 수
            batch_size: 배치 크기

        Returns:
            데이터가 채워진 Collection
        """
        with self.pool.get_connection_context() as conn:
            if utility.has_collection(self.collection_name, using=conn.alias):
                utility.drop_collection(self.collection_name, using=conn.alias)

            fields = [
                FieldSchema(
                    name="id",
                    dtype=DataType.INT64,
                    is_primary=True,
                    auto_id=True,
                ),
                FieldSchema(
                    name="embedding",
                    dtype=DataType.FLOAT_VECTOR,
                    dim=self.dim,
                ),
            ]
            schema = CollectionSchema(fields=fields, description="Index benchmark dataset")
            collection = Collection(
                name=self.collection_name,
                schema=schema,
                using=conn.alias,
            )

            # 컬럼(columnar) 형식으로 배치 삽입: [벡터 리스트] 한 개의 컬럼
            for i in range(0, num_vectors, batch_size):
                end = min(i + batch_size, num_vectors)
                vectors = self._generate_random_vectors(end - i, seed=i)
                data = [vectors.tolist()]
                collection.insert(data)

            collection.flush()
            logger.info(
                "benchmark_dataset_ready",
                collection=self.collection_name,
                num_vectors=num_vectors,
            )
            return collection

    @timing_decorator
    def build_index(self, index_type: str, index_params: Optional[dict] = None):
        """
        Index 재생성 (기존 index 제거 후 새로 구축)

        Milvus는 필드당 하나의 index 만 허용하므로 교체 시
        release -> drop -> create -> load 순서를 지켜야 한다.

        Args:
            index_type: FLAT / IVF_FLAT / IVF_SQ8 / HNSW
            index_params: 빌드 파라미터 (None 이면 기본값 사용)

        Returns:
            빌드 소요 시간(초)
        """
        if index_params is None:
            index_params = self.INDEX_CONFIGS[index_type]

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            # 로드 상태에서는 index 변경이 불가하므로 먼저 release
            collection.release()

            try:
                collection.drop_index()
            except Exception as e:
                logger.debug("no_existing_index", error=str(e))

            start_time = time.time()
            collection.create_index(
                field_name="embedding",
                index_params={
                    "index_type": index_type,
                    "metric_type": "L2",
                    "params": index_params,
                },
            )

            # index 빌드 완료 대기
            utility.wait_for_index_build_complete(
                collection_name=self.collection_name,
                using=conn.alias,
            )
            build_time = time.time() - start_time

            collection.load()
            utility.wait_for_loading_complete(self.collection_name, using=conn.alias)

            logger.info(
                "index_built",
                index_type=index_type,
                params=index_params,
                build_time_seconds=round(build_time, 3),
            )
            return build_time

    def compute_ground_truth(
        self,
        query_vectors: np.ndarray,
        top_k: int = 10,
    ) -> List[List[int]]:
        """
        FLAT(전수조사) 검색으로 ground truth 계산

        Args:
            query_vectors: 쿼리 벡터들 (q, dim)
            top_k: 결과 수

        Returns:
            각 쿼리의 정답 id 리스트
        """
        results = []
        for query_vector in query_vectors:
            hits = self._search_single(query_vector, top_k=top_k, search_params={})
            results.append([hit.id for hit in hits])
        return results

    def _search_single(
        self,
        query_vector: np.ndarray,
        top_k: int,
        search_params: dict,
    ):
        """단일 벡터 검색 (내부 헬퍼)"""
        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            param = {"metric_type": "L2"}
            if search_params:
                param["params"] = search_params

            return collection.search(
                data=[query_vector.tolist()],
                anns_field="embedding",
                param=param,
                limit=top_k,
            )[0]

    @timing_decorator
    def benchmark_search(
        self,
        index_type: str,
        query_vectors: np.ndarray,
        ground_truth: List[List[int]],
        top_k: int = 10,
    ) -> dict:
        """
        단일 Index 타입 성능 측정 (Latency + Recall@K)

        Args:
            index_type: 측정 대상 index
            query_vectors: 쿼리 벡터들
            ground_truth: FLAT 기준 정답
            top_k: 결과 수

        Returns:
            latency 통계와 recall 지표
        """
        latencies_ms = []
        recalls = []

        for i, query_vector in enumerate(query_vectors):
            start_time = time.time()
            hits = self._search_single(
                query_vector,
                top_k=top_k,
                search_params=self.SEARCH_PARAMS[index_type],
            )
            elapsed_ms = (time.time() - start_time) * 1000
            latencies_ms.append(elapsed_ms)

            # Recall@K: 검색 결과와 ground truth 의 교집합 비율
            retrieved_ids = {hit.id for hit in hits}
            relevant_ids = set(ground_truth[i])
            recalls.append(len(retrieved_ids & relevant_ids) / top_k)

        result = {
            "index_type": index_type,
            "avg_latency_ms": round(float(np.mean(latencies_ms)), 3),
            "p95_latency_ms": round(float(np.percentile(latencies_ms, 95)), 3),
            "qps": round(len(query_vectors) / (sum(latencies_ms) / 1000), 1),
            "recall_at_k": round(float(np.mean(recalls)), 4),
            "top_k": top_k,
        }

        logger.info("index_benchmark_completed", **result)
        return result

    def run_comparison(
        self,
        index_types: Optional[List[str]] = None,
        num_vectors: int = 5000,
        num_queries: int = 20,
        top_k: int = 10,
    ) -> List[dict]:
        """
        여러 Index 타입 일괄 비교

        Args:
            index_types: 비교할 index 목록 (None 이면 전체)
            num_vectors: 데이터셋 크기
            num_queries: 쿼리 수
            top_k: 결과 수

        Returns:
            index 별 성능 결과 리스트
        """
        if index_types is None:
            index_types = list(self.INDEX_CONFIGS.keys())

        print(f"\nPreparing benchmark dataset ({num_vectors:,} vectors, dim={self.dim})...")
        self.ensure_collection_with_data(num_vectors=num_vectors)

        query_vectors = self._generate_random_vectors(num_queries, seed=12345)

        # Ground truth 를 위해 FLAT 를 먼저 구축하고 정답을 확보한다
        print("Building FLAT index for ground truth...")
        self.build_index("FLAT")
        ground_truth = self.compute_ground_truth(query_vectors, top_k=top_k)

        results = []
        for index_type in index_types:
            print(f"\n--- Benchmarking {index_type} ---")
            build_time = self.build_index(index_type)
            metrics = self.benchmark_search(
                index_type=index_type,
                query_vectors=query_vectors,
                ground_truth=ground_truth,
                top_k=top_k,
            )
            metrics["build_time_seconds"] = round(build_time, 3)
            results.append(metrics)

        self._print_results(results)
        return results

    @staticmethod
    def _print_results(results: List[dict]):
        """비교 결과 테이블 출력"""
        print("\n" + "=" * 80)
        print("INDEX COMPARISON RESULTS")
        print("=" * 80)
        print(
            f"{'Index':<10} | {'Build (s)':>10} | {'Avg Lat(ms)':>12} | "
            f"{'P95 Lat(ms)':>12} | {'QPS':>8} | {'Recall@K':>9}"
        )
        print("-" * 80)

        for r in results:
            print(
                f"{r['index_type']:<10} | {r['build_time_seconds']:>10.3f} | "
                f"{r['avg_latency_ms']:>12.3f} | {r['p95_latency_ms']:>12.3f} | "
                f"{r['qps']:>8,.1f} | {r['recall_at_k']:>9.4f}"
            )
        print("=" * 80)


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="Milvus Index Optimization Benchmark")
    parser.add_argument(
        "--collection",
        type=str,
        default="index_benchmark_demo",
        help="Benchmark collection name",
    )
    parser.add_argument("--dim", type=int, default=128, help="Vector dimension")
    parser.add_argument(
        "--num-vectors",
        type=int,
        default=5000,
        help="Number of vectors in the dataset",
    )
    parser.add_argument("--queries", type=int, default=20, help="Number of queries")
    parser.add_argument("--top-k", type=int, default=10, help="Top K results")
    parser.add_argument(
        "--types",
        type=str,
        default="FLAT,IVF_FLAT,IVF_SQ8,HNSW",
        help="Comma-separated index types to compare",
    )

    args = parser.parse_args()

    optimizer = IndexOptimizer(args.collection, dim=args.dim)
    index_types = [t.strip().upper() for t in args.types.split(",")]

    try:
        optimizer.run_comparison(
            index_types=index_types,
            num_vectors=args.num_vectors,
            num_queries=args.queries,
            top_k=args.top_k,
        )
        return 0

    except Exception as e:
        logger.error(
            "index_benchmark_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        print(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
