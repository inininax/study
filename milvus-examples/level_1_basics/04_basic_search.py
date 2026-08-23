"""
Level 1-4: Basic Vector Search

이 모듈은 Milvus의 기본 검색 기능을 다룹니다:
- Vector similarity search
- Top-K 검색
- 거리 메트릭 (L2, IP, COSINE)
- 검색 파라미터 튜닝
- 결과 분석

Production 환경에서의 검색 최적화 패턴을 학습합니다.
"""

import argparse
import sys
import time
from pathlib import Path
from typing import List, Optional

import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from pymilvus import Collection

from config.settings import settings
from utils.connection import get_milvus_client
from utils.decorators import timing_decorator
from utils.logger import get_logger

logger = get_logger(__name__)


class VectorSearcher:
    """Production-ready vector search manager."""

    def __init__(self, collection_name: str = "demo_simple"):
        """Initialize vector searcher."""
        self.collection_name = collection_name
        self.pool = get_milvus_client()
        self.dim = 128

    def _generate_query_vector(self, dim: int = None) -> np.ndarray:
        """
        쿼리 벡터 생성

        Args:
            dim: 벡터 차원

        Returns:
            정규화된 쿼리 벡터
        """
        if dim is None:
            dim = self.dim

        vector = np.random.rand(dim).astype(np.float32)
        vector = vector / np.linalg.norm(vector)

        return vector

    @timing_decorator
    def basic_search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        metric_type: str = "L2",
        search_params: Optional[dict] = None,
    ) -> List[dict]:
        """
        기본 벡터 검색

        Args:
            query_vector: 쿼리 벡터
            top_k: 반환할 결과 수
            metric_type: 거리 메트릭 (L2, IP, COSINE)
            search_params: 검색 파라미터

        Returns:
            검색 결과 리스트
        """
        logger.info(
            "performing_basic_search",
            collection=self.collection_name,
            top_k=top_k,
            metric=metric_type,
        )

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            # Collection 로드 확인
            if not collection.is_loaded:
                collection.load()
                logger.info("collection_loaded", name=self.collection_name)

            # 기본 검색 파라미터
            if search_params is None:
                search_params = {"metric_type": metric_type}

                # Index type에 따른 파라미터 설정
                try:
                    index_info = collection.index()
                    if index_info:
                        index_type = index_info.params.get("index_type", "")

                        if index_type == "HNSW":
                            search_params["params"] = {"ef": 64}
                        elif index_type in ["IVF_FLAT", "IVF_SQ8"]:
                            search_params["params"] = {"nprobe": 16}
                except Exception:
                    logger.debug("no_index_found_using_default_params")

            # 검색 수행
            results = collection.search(
                data=[query_vector.tolist()],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
            )

            # 결과 파싱
            parsed_results = []
            for hits in results:
                for hit in hits:
                    parsed_results.append({
                        "id": hit.id,
                        "distance": hit.distance,
                        "score": self._distance_to_score(hit.distance, metric_type),
                    })

            logger.info(
                "search_completed",
                results_count=len(parsed_results),
            )

            return parsed_results

    def _distance_to_score(self, distance: float, metric_type: str) -> float:
        """
        거리를 유사도 점수로 변환

        Args:
            distance: 거리 값
            metric_type: 메트릭 타입

        Returns:
            0-1 사이의 유사도 점수 (1이 가장 유사)
        """
        if metric_type == "L2":
            # L2 거리: 작을수록 유사
            return 1.0 / (1.0 + distance)
        elif metric_type in ["IP", "COSINE"]:
            # Inner Product / Cosine: 클수록 유사
            return distance
        else:
            return distance

    @timing_decorator
    def batch_search(
        self,
        query_vectors: np.ndarray,
        top_k: int = 10,
        metric_type: str = "L2",
    ) -> List[List[dict]]:
        """
        배치 검색

        Args:
            query_vectors: 쿼리 벡터들 (n, dim)
            top_k: 각 쿼리당 반환할 결과 수
            metric_type: 거리 메트릭

        Returns:
            각 쿼리별 검색 결과 리스트
        """
        logger.info(
            "performing_batch_search",
            num_queries=len(query_vectors),
            top_k=top_k,
        )

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            if not collection.is_loaded:
                collection.load()

            # 검색 파라미터 설정
            search_params = {"metric_type": metric_type}

            # 배치 검색
            results = collection.search(
                data=query_vectors.tolist(),
                anns_field="embedding",
                param=search_params,
                limit=top_k,
            )

            # 결과 파싱
            all_results = []
            for hits in results:
                query_results = []
                for hit in hits:
                    query_results.append({
                        "id": hit.id,
                        "distance": hit.distance,
                        "score": self._distance_to_score(hit.distance, metric_type),
                    })
                all_results.append(query_results)

            logger.info(
                "batch_search_completed",
                queries=len(all_results),
            )

            return all_results

    @timing_decorator
    def compare_metrics(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
    ) -> dict:
        """
        다양한 거리 메트릭 비교

        Args:
            query_vector: 쿼리 벡터
            top_k: 반환할 결과 수

        Returns:
            메트릭별 검색 결과
        """
        logger.info("comparing_distance_metrics", top_k=top_k)

        metrics = ["L2", "IP", "COSINE"]
        results = {}

        for metric in metrics:
            logger.info("testing_metric", metric=metric)

            try:
                search_results = self.basic_search(
                    query_vector,
                    top_k=top_k,
                    metric_type=metric,
                )

                results[metric] = {
                    "count": len(search_results),
                    "results": search_results,
                    "avg_distance": np.mean([r["distance"] for r in search_results]),
                    "avg_score": np.mean([r["score"] for r in search_results]),
                }

            except Exception as e:
                logger.error(
                    "metric_test_failed",
                    metric=metric,
                    error=str(e),
                )
                results[metric] = {"error": str(e)}

        logger.info("metric_comparison_completed")
        return results

    @timing_decorator
    def search_with_different_topk(
        self,
        query_vector: np.ndarray,
        topk_values: List[int] = None,
        metric_type: str = "L2",
    ) -> dict:
        """
        다양한 Top-K 값으로 검색

        Args:
            query_vector: 쿼리 벡터
            topk_values: 테스트할 Top-K 값 리스트
            metric_type: 거리 메트릭

        Returns:
            Top-K별 검색 결과
        """
        if topk_values is None:
            topk_values = [5, 10, 20, 50, 100]

        logger.info(
            "testing_different_topk",
            topk_values=topk_values,
            metric=metric_type,
        )

        results = {}

        for k in topk_values:
            start_time = time.time()

            search_results = self.basic_search(
                query_vector,
                top_k=k,
                metric_type=metric_type,
            )

            elapsed = time.time() - start_time

            results[k] = {
                "count": len(search_results),
                "elapsed_ms": elapsed * 1000,
                "top_result": search_results[0] if search_results else None,
            }

        logger.info("topk_comparison_completed")
        return results

    @timing_decorator
    def benchmark_search_performance(
        self,
        num_queries: int = 100,
        top_k: int = 10,
        metric_type: str = "L2",
    ) -> dict:
        """
        검색 성능 벤치마크

        Args:
            num_queries: 테스트 쿼리 수
            top_k: 반환할 결과 수
            metric_type: 거리 메트릭

        Returns:
            성능 통계
        """
        logger.info(
            "starting_search_benchmark",
            num_queries=num_queries,
            top_k=top_k,
        )

        # 쿼리 벡터 생성
        query_vectors = np.random.rand(num_queries, self.dim).astype(np.float32)
        query_vectors = query_vectors / np.linalg.norm(
            query_vectors, axis=1, keepdims=True
        )

        # 개별 검색 벤치마크
        individual_times = []
        for vector in query_vectors:
            start = time.time()
            self.basic_search(vector, top_k=top_k, metric_type=metric_type)
            individual_times.append(time.time() - start)

        # 배치 검색 벤치마크
        batch_start = time.time()
        self.batch_search(query_vectors, top_k=top_k, metric_type=metric_type)
        batch_elapsed = time.time() - batch_start

        # 통계 계산
        stats = {
            "num_queries": num_queries,
            "top_k": top_k,
            "individual_search": {
                "avg_latency_ms": np.mean(individual_times) * 1000,
                "p50_latency_ms": np.percentile(individual_times, 50) * 1000,
                "p95_latency_ms": np.percentile(individual_times, 95) * 1000,
                "p99_latency_ms": np.percentile(individual_times, 99) * 1000,
                "qps": 1.0 / np.mean(individual_times),
            },
            "batch_search": {
                "total_time_s": batch_elapsed,
                "avg_latency_ms": (batch_elapsed / num_queries) * 1000,
                "qps": num_queries / batch_elapsed,
            },
        }

        logger.info("benchmark_completed", **stats)
        return stats


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="Milvus Vector Search")
    parser.add_argument(
        "--collection",
        type=str,
        default="demo_simple",
        help="Collection name",
    )
    parser.add_argument(
        "--metric",
        type=str,
        choices=["L2", "IP", "COSINE", "all"],
        default="L2",
        help="Distance metric",
    )
    parser.add_argument(
        "--topk",
        type=str,
        default="10",
        help="Top K (comma-separated for multiple)",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run performance benchmark",
    )

    args = parser.parse_args()

    logger.info(
        "starting_vector_search",
        collection=args.collection,
        metric=args.metric,
    )

    searcher = VectorSearcher(args.collection)

    try:
        if args.benchmark:
            # 성능 벤치마크
            print("\n" + "="*60)
            print("SEARCH PERFORMANCE BENCHMARK")
            print("="*60 + "\n")

            stats = searcher.benchmark_search_performance(
                num_queries=100,
                top_k=10,
                metric_type="L2",
            )

            print("Individual Search:")
            print(f"  Avg Latency: {stats['individual_search']['avg_latency_ms']:.2f} ms")
            print(f"  P50 Latency: {stats['individual_search']['p50_latency_ms']:.2f} ms")
            print(f"  P95 Latency: {stats['individual_search']['p95_latency_ms']:.2f} ms")
            print(f"  P99 Latency: {stats['individual_search']['p99_latency_ms']:.2f} ms")
            print(f"  QPS: {stats['individual_search']['qps']:.2f}")

            print("\nBatch Search:")
            print(f"  Avg Latency: {stats['batch_search']['avg_latency_ms']:.2f} ms")
            print(f"  QPS: {stats['batch_search']['qps']:.2f}")
            print(f"  Total Time: {stats['batch_search']['total_time_s']:.2f} s")

        elif args.metric == "all":
            # 메트릭 비교
            print("\n" + "="*60)
            print("DISTANCE METRICS COMPARISON")
            print("="*60 + "\n")

            query_vector = searcher._generate_query_vector()
            topk = int(args.topk.split(",")[0])

            results = searcher.compare_metrics(query_vector, top_k=topk)

            for metric, data in results.items():
                if "error" in data:
                    print(f"{metric}: Error - {data['error']}")
                else:
                    print(f"\n{metric}:")
                    print(f"  Results: {data['count']}")
                    print(f"  Avg Distance: {data['avg_distance']:.4f}")
                    print(f"  Avg Score: {data['avg_score']:.4f}")
                    print(f"  Top 3 IDs: {[r['id'] for r in data['results'][:3]]}")

        else:
            # 기본 검색
            query_vector = searcher._generate_query_vector()

            # Top-K 값 파싱
            topk_values = [int(k.strip()) for k in args.topk.split(",")]

            if len(topk_values) > 1:
                # 여러 Top-K 값 테스트
                print("\n" + "="*60)
                print("TOP-K COMPARISON")
                print("="*60 + "\n")

                results = searcher.search_with_different_topk(
                    query_vector,
                    topk_values=topk_values,
                    metric_type=args.metric,
                )

                print(f"{'Top-K':>10} | {'Results':>10} | {'Latency (ms)':>15}")
                print("-" * 60)

                for k, data in results.items():
                    print(
                        f"{k:>10} | {data['count']:>10} | "
                        f"{data['elapsed_ms']:>15.2f}"
                    )

            else:
                # 단일 검색
                topk = topk_values[0]

                print(f"\nSearching for top {topk} results using {args.metric}...\n")

                results = searcher.basic_search(
                    query_vector,
                    top_k=topk,
                    metric_type=args.metric,
                )

                # 결과 출력
                print("="*60)
                print(f"SEARCH RESULTS (Top {topk})")
                print("="*60)
                print(f"{'Rank':>6} | {'ID':>12} | {'Distance':>12} | {'Score':>12}")
                print("-" * 60)

                for rank, result in enumerate(results, 1):
                    print(
                        f"{rank:>6} | {result['id']:>12} | "
                        f"{result['distance']:>12.6f} | {result['score']:>12.6f}"
                    )

        return 0

    except Exception as e:
        logger.error(
            "search_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        print(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
