"""
메모리 프로파일링

tracemalloc 기반 클라이언트 메모리 측정과
양자화(Quantization) 설정에 따른 서버 메모리 절약 효과를 확인한다.

실행:
    python benchmarks/memory_profiling.py
"""

import os
import time
import tracemalloc
import logging
from typing import Dict, Optional

import numpy as np
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    ScalarQuantization,
    ScalarQuantizationConfig,
    ScalarType,
    VectorParams,
)

# 환경 변수 로드
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def format_bytes(num_bytes: int) -> str:
    """바이트를 사람이 읽기 쉬운 형태로 변환"""
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} TB"


class MemoryProfiler:
    """
    메모리 프로파일러

    Features:
    - 업서트/검색 시 클라이언트 메모리 사용량 측정 (tracemalloc)
    - INT8 스칼라 양자화 on/off 비교
    - 배치 크기별 메모리 피크 비교

    Example:
        >>> profiler = MemoryProfiler(collection_name="mem_profile")
        >>> stats = profiler.profile_upsert(num_vectors=2000)
        >>> print(format_bytes(stats["peak"]))
    """

    def __init__(
        self,
        collection_name: str = "memory_profiling",
        vector_size: int = 384,
        host: str = None,
        port: int = None,
    ):
        """
        Args:
            collection_name: 프로파일링 대상 컬렉션
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
        """테스트용 랜덤 벡터 생성"""
        rng = np.random.default_rng(seed)
        return rng.random((count, self.vector_size)).astype(np.float32)

    def _recreate_collection(self, quantize: bool = False):
        """
        컬렉션 재생성

        Args:
            quantize: True 면 INT8 스칼라 양자화(always_ram) 활성화
                - float32 대비 약 1/4 메모리로 벡터 저장 가능
                - always_ram=True 는 원본 포인터까지 RAM 에 유지해 정확도 보완
        """
        quantization_config = None
        if quantize:
            quantization_config = ScalarQuantization(
                scalar=ScalarQuantizationConfig(
                    type=ScalarType.INT8,
                    quantile=0.99,
                    always_ram=True,
                )
            )

        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
            quantization_config=quantization_config,
        )

    def profile_upsert(
        self,
        num_vectors: int = 2000,
        batch_size: int = 500,
    ) -> Dict[str, float]:
        """
        업서트 시 클라이언트 메모리 프로파일링

        Args:
            num_vectors: 업서트할 벡터 수
            batch_size: 배치 크기

        Returns:
            current / peak 메모리 통계 (바이트)
        """
        vectors = self._generate_vectors(num_vectors)

        # tracemalloc 시작 - 이후의 Python 할당을 추적한다
        tracemalloc.start()

        for i in range(0, num_vectors, batch_size):
            batch = vectors[i:i + batch_size]
            points = [
                PointStruct(id=i + j, vector=batch[j].tolist(), payload={"idx": i + j})
                for j in range(len(batch))
            ]
            self.client.upsert(collection_name=self.collection_name, points=points)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        stats = {"current": current, "peak": peak}
        logger.info(
            f"업서트 메모리: 현재 {format_bytes(current)}, "
            f"피크 {format_bytes(peak)} (batch={batch_size})"
        )
        return stats

    def profile_search(self, num_queries: int = 100) -> Dict[str, float]:
        """검색 시 클라이언트 메모리 프로파일링"""
        query_vector = self._generate_vectors(1)[0]

        tracemalloc.start()

        latencies_ms = []
        for _ in range(num_queries):
            start = time.time()
            self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector.tolist(),
                limit=10,
            )
            latencies_ms.append((time.time() - start) * 1000)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        stats = {
            "current": current,
            "peak": peak,
            "avg_latency_ms": round(float(np.mean(latencies_ms)), 3),
        }
        logger.info(
            f"검색 메모리: 현재 {format_bytes(current)}, "
            f"피크 {format_bytes(peak)}, 평균 지연 {stats['avg_latency_ms']}ms"
        )
        return stats

    def compare_batch_sizes(
        self,
        num_vectors: int = 2000,
        batch_sizes: Optional[list] = None,
    ) -> Dict[int, Dict[str, float]]:
        """
        배치 크기별 메모리 피크 비교

        큰 배치는 처리량은 좋지만 메모리 피크가 커진다.
        제한된 메모리 환경에서는 적절한 배치 크기를 선택해야 한다.

        Returns:
            배치 크기별 {current, peak} 딕셔너리
        """
        if batch_sizes is None:
            batch_sizes = [100, 500, 1000]

        results = {}
        for batch_size in batch_sizes:
            # 컬렉션 초기화 후 재측정 (공정 비교)
            self._recreate_collection()
            stats = self.profile_upsert(
                num_vectors=num_vectors,
                batch_size=batch_size,
            )
            results[batch_size] = stats
            print(f"  batch={batch_size:>5}: "
                  f"현재 {format_bytes(stats['current'])}, "
                  f"피크 {format_bytes(stats['peak'])}")

        return results


def main():
    """메인 함수"""
    print("=" * 60)
    print("메모리 프로파일링")
    print("=" * 60)

    profiler = MemoryProfiler()

    try:
        # 1. 배치 크기별 클라이언트 메모리 비교
        print("\n[1] 배치 크기별 업서트 메모리")
        profiler.compare_batch_sizes(num_vectors=2000)

        # 2. 검색 프로파일링
        print("\n[2] 검색 메모리 및 지연 시간")
        stats = profiler.profile_search(num_queries=100)
        print(f"  피크: {format_bytes(stats['peak'])}, "
              f"평균 지연: {stats['avg_latency_ms']}ms")

        print("\n" + "=" * 60)
        print("✓ 프로파일링 완료!")
        print("=" * 60)

    except Exception as e:
        logger.error(f"에러 발생: {e}")
        print(f"\n✗ 실패: {e}")
        print("\n해결 방법:")
        print("1. Docker Compose로 Qdrant 서버가 실행 중인지 확인:")
        print("   $ docker-compose up -d qdrant")


if __name__ == "__main__":
    main()
