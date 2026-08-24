"""
인덱싱 벤치마크

HNSW 파라미터(m, ef_construct) 조합별 인덱싱 소요 시간과
검색 지연 시간을 측정해 최적 파라미터를 찾는다.

실행:
    python benchmarks/indexing_benchmark.py
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
    HnswConfigDiff,
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


class IndexingBenchmark:
    """
    인덱싱 벤치마크

    HNSW 파라미터 조합별로 컬렉션을 재구성하고,
    업서트(색인) 시간과 검색 지연을 측정한다.

    Example:
        >>> benchmark = IndexingBenchmark(collection_name="index_bench")
        >>> results = benchmark.run(num_vectors=2000)
        >>> for r in results:
        ...     print(r)
    """

    def __init__(
        self,
        collection_name: str = "index_benchmark",
        vector_size: int = 384,
        host: str = None,
        port: int = None,
    ):
        """
        Args:
            collection_name: 벤치마크용 컬렉션 이름
            vector_size: 벡터 차원
            host: Qdrant 호스트 (기본값: 환경변수 QDRANT_HOST)
            port: Qdrant 포트 (기본값: 환경변수 QDRANT_PORT)
        """
        self.collection_name = collection_name
        self.vector_size = vector_size

        self.client = QdrantClient(
            host=host or os.getenv("QDRANT_HOST", "localhost"),
            port=port or int(os.getenv("QDRANT_PORT", "6333")),
        )

    def _generate_vectors(self, count: int, seed: int = 42) -> np.ndarray:
        """테스트용 랜덤 벡터 생성 (L2 정규화)"""
        rng = np.random.default_rng(seed)
        vectors = rng.random((count, self.vector_size)).astype(np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms

    def _recreate_collection(self, m: int, ef_construct: int):
        """
        HNSW 설정을 바꿔 컬렉션 재생성

        Args:
            m: 그래프 노드당 최대 연결 수 (높을수록 정확/메모리 증가)
            ef_construct: 구축 시 탐색 폭 (높을수록 정확/느림)
        """
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
            hnsw_config=HnswConfigDiff(m=m, ef_construct=ef_construct),
        )

    def _upsert_and_wait_indexed(self, vectors: np.ndarray, batch_size: int = 500) -> float:
        """
        벡터 업서트 후 색인 완료까지 대기하며 소요 시간 측정

        Returns:
            업서트 + 색인 완료까지의 총 시간(초)
        """
        start = time.time()
        total = len(vectors)

        # 배치 단위 업서트 - 한 번에 올리면 메모리 피크가 커진다
        for i in range(0, total, batch_size):
            batch = vectors[i:i + batch_size]
            points = [
                PointStruct(id=i + j, vector=batch[j].tolist(), payload={"idx": i + j})
                for j in range(len(batch))
            ]
            self.client.upsert(collection_name=self.collection_name, points=points)

        # 색인은 비동기로 수행되므로 optimizer 가 완료될 때까지 폴링한다
        deadline = start + 120
        while True:
            info = self.client.get_collection(self.collection_name)
            if info.status == "green" and info.optimizer_status == "ok":
                break
            if time.time() > deadline:
                logger.warning("색인 대기 시간 초과 (120초)")
                break
            time.sleep(0.5)

        return time.time() - start

    def _measure_search_latency(self, queries: np.ndarray, top_k: int = 10) -> Dict[str, float]:
        """검색 지연 시간 측정"""
        latencies_ms = []

        for query_vector in queries:
            start = time.time()
            self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector.tolist(),
                limit=top_k,
            )
            latencies_ms.append((time.time() - start) * 1000)

        return {
            "avg_latency_ms": round(float(np.mean(latencies_ms)), 3),
            "p95_latency_ms": round(float(np.percentile(latencies_ms, 95)), 3),
        }

    def run(
        self,
        configs: List[Dict[str, int]] = None,
        num_vectors: int = 2000,
        num_queries: int = 20,
        top_k: int = 10,
    ) -> List[dict]:
        """
        벤치마크 실행

        Args:
            configs: 테스트할 HNSW 설정 목록 (None 이면 기본 3종)
            num_vectors: 업서트할 벡터 수
            num_queries: 검색 측정용 쿼리 수
            top_k: 검색 결과 수

        Returns:
            설정별 성능 결과 리스트
        """
        if configs is None:
            # 속도 우선 / 균형 / 정확도 우선
            configs = [
                {"m": 16, "ef_construct": 100},
                {"m": 32, "ef_construct": 128},
                {"m": 64, "ef_construct": 200},
            ]

        dataset = self._generate_vectors(num_vectors)
        queries = self._generate_vectors(num_queries, seed=999)

        results = []
        for config in configs:
            m, ef_construct = config["m"], config["ef_construct"]
            print(f"\n--- m={m}, ef_construct={ef_construct} ---")

            try:
                self._recreate_collection(m=m, ef_construct=ef_construct)

                indexing_time = self._upsert_and_wait_indexed(dataset)
                latency = self._measure_search_latency(queries, top_k=top_k)

                result = {
                    "m": m,
                    "ef_construct": ef_construct,
                    "indexing_seconds": round(indexing_time, 2),
                    **latency,
                }
                results.append(result)
                print(f"  색인: {result['indexing_seconds']}초 | "
                      f"평균 지연: {result['avg_latency_ms']}ms | "
                      f"P95: {result['p95_latency_ms']}ms")

            except Exception as e:
                logger.error(f"벤치마크 실패 (m={m}, ef_construct={ef_construct}): {e}")

        return results


def main():
    """메인 함수"""
    print("=" * 60)
    print("HNSW 인덱싱 벤치마크")
    print("=" * 60)

    benchmark = IndexingBenchmark()

    results = benchmark.run(num_vectors=2000, num_queries=20)

    print("\n" + "=" * 60)
    print("결과 요약")
    print("=" * 60)
    print(f"{'m':>5} | {'ef_construct':>12} | {'색인(s)':>10} | {'평균(ms)':>10} | {'P95(ms)':>10}")
    print("-" * 60)

    for r in results:
        print(f"{r['m']:>5} | {r['ef_construct']:>12} | "
              f"{r['indexing_seconds']:>10.2f} | "
              f"{r['avg_latency_ms']:>10.3f} | {r['p95_latency_ms']:>10.3f}")


if __name__ == "__main__":
    main()
