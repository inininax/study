"""
검색 성능 벤치마크

QPS(초당 쿼리 수)와 지연 시간 분포(P50/P95/P99)를 측정한다.

실행:
    python benchmarks/search_benchmark.py
"""

import os
import time
import logging
from typing import Dict, List

import numpy as np
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

# 환경 변수 로드
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def percentile(values: List[float], percent: float) -> float:
    """
    백분위수 계산 (의존성 없이 직접 구현)

    Args:
        values: 값 목록
        percent: 백분위 (예: 95 -> P95)
    """
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = int(len(sorted_values) * percent / 100)
    index = min(index, len(sorted_values) - 1)
    return sorted_values[index]


class SearchBenchmark:
    """
    검색 성능 벤치마크

    Example:
        >>> benchmark = SearchBenchmark(collection_name="products")
        >>> results = benchmark.run(num_queries=1000, vector_size=384, top_k=10)
        >>> print(f"평균 응답 시간: {results['avg_latency_ms']}ms")
        >>> print(f"처리량: {results['throughput_qps']} QPS")
        >>> print(f"P95 latency: {results['p95_latency_ms']}ms")
        >>> print(f"P99 latency: {results['p99_latency_ms']}ms")
    """

    def __init__(
        self,
        collection_name: str,
        host: str = None,
        port: int = None,
    ):
        """
        Args:
            collection_name: 벤치마크 대상 컬렉션 이름
            host: Qdrant 호스트 (기본값: 환경변수 QDRANT_HOST)
            port: Qdrant 포트 (기본값: 환경변수 QDRANT_PORT)
        """
        self.collection_name = collection_name
        self.client = QdrantClient(
            host=host or os.getenv("QDRANT_HOST", "localhost"),
            port=port or int(os.getenv("QDRANT_PORT", "6333")),
        )

    def ensure_collection(
        self,
        vector_size: int = 384,
        num_points: int = 10000,
        seed: int = 42,
    ) -> bool:
        """
        컬렉션 확인 및 샘플 데이터 준비

        컬렉션이 없거나 비어 있으면 랜덤 샘플 데이터를 적재한다.

        Args:
            vector_size: 벡터 차원
            num_points: 생성할 샘플 포인트 수
            seed: 난수 시드

        Returns:
            새로 데이터를 적재했는지 여부
        """
        collections = {c.name for c in self.client.get_collections().collections}

        if self.collection_name not in collections:
            logger.info(f"컬렉션 생성: {self.collection_name}")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

        info = self.client.get_collection(self.collection_name)
        if info.points_count and info.points_count > 0:
            # 이미 데이터가 있으면 기존 데이터로 진행
            return False

        rng = np.random.default_rng(seed)
        batch_size = 500

        for i in range(0, num_points, batch_size):
            end = min(i + batch_size, num_points)
            batch = rng.random((end - i, vector_size)).astype(np.float32)

            points = [
                PointStruct(id=i + j, vector=batch[j].tolist(), payload={"idx": i + j})
                for j in range(len(batch))
            ]
            self.client.upsert(collection_name=self.collection_name, points=points)

        return True

    def run(
        self,
        num_queries: int = 1000,
        vector_size: int = 384,
        top_k: int = 10,
        warmup: int = 50,
    ) -> Dict[str, float]:
        """
        벤치마크 실행

        Args:
            num_queries: 실행할 쿼리 수
            vector_size: 쿼리 벡터 차원
            top_k: 검색 결과 수
            warmup: 워밍업 쿼리 수 (컴파일/커넥션 워밍 - 측정 제외)

        Returns:
            지연 시간 통계 딕셔너리
        """
        rng = np.random.default_rng(1234)

        # 워밍업 - 첫 요청은 컴파일/연결 비용이 커서 측정에서 제외한다
        for _ in range(warmup):
            self.client.search(
                collection_name=self.collection_name,
                query_vector=rng.random(vector_size).tolist(),
                limit=top_k,
            )

        latencies_ms: List[float] = []
        start_total = time.time()

        for _ in range(num_queries):
            query_vector = rng.random(vector_size).astype(np.float32)

            start = time.time()
            self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector.tolist(),
                limit=top_k,
            )
            latencies_ms.append((time.time() - start) * 1000)

        total_seconds = time.time() - start_total

        results = {
            "num_queries": num_queries,
            "top_k": top_k,
            "avg_latency_ms": round(float(np.mean(latencies_ms)), 3),
            "p50_latency_ms": round(percentile(latencies_ms, 50), 3),
            "p95_latency_ms": round(percentile(latencies_ms, 95), 3),
            "p99_latency_ms": round(percentile(latencies_ms, 99), 3),
            "throughput_qps": round(num_queries / total_seconds, 1),
        }

        logger.info("검색 벤치마크 완료", extra={"results": results})
        return results


def main():
    """메인 함수"""
    print("=" * 60)
    print("Qdrant 검색 성능 벤치마크")
    print("=" * 60)

    benchmark = SearchBenchmark(
        collection_name=os.getenv("BENCH_COLLECTION_NAME", "search_benchmark")
    )

    try:
        loaded = benchmark.ensure_collection(vector_size=384, num_points=10000)
        if loaded:
            print("샘플 데이터 10,000건 적재 완료")

        results = benchmark.run(num_queries=500, vector_size=384, top_k=10)

        print("\n" + "=" * 60)
        print("결과")
        print("=" * 60)
        print(f"평균 응답 시간: {results['avg_latency_ms']}ms")
        print(f"처리량: {results['throughput_qps']} QPS")
        print(f"P50 latency: {results['p50_latency_ms']}ms")
        print(f"P95 latency: {results['p95_latency_ms']}ms")
        print(f"P99 latency: {results['p99_latency_ms']}ms")

    except Exception as e:
        logger.error(f"벤치마크 실패: {e}")
        print(f"\n✗ 실패: {e}")
        print("\n해결 방법:")
        print("1. Docker Compose로 Qdrant 서버가 실행 중인지 확인:")
        print("   $ docker-compose up -d qdrant")


if __name__ == "__main__":
    main()
