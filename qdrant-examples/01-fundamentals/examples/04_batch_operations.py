"""
예제 4: 배치 작업 최적화

대량 벡터 삽입 시 배치 크기에 따른 성능 비교
"""

import sys
sys.path.append('..')

from core.operations import VectorOperations
from core.collections import CollectionManager
import numpy as np
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def benchmark_batch_insert(
    ops: VectorOperations,
    total_vectors: int,
    chunk_size: int,
    vector_size: int
) -> dict:
    """
    배치 삽입 벤치마크

    Args:
        ops: VectorOperations 인스턴스
        total_vectors: 총 벡터 개수
        chunk_size: 청크 크기
        vector_size: 벡터 차원

    Returns:
        벤치마크 결과
    """
    # 랜덤 벡터 생성
    vectors = np.random.rand(total_vectors, vector_size).tolist()

    # 페이로드 생성
    payloads = [
        {
            "doc_id": i,
            "category": f"cat_{i % 10}",
            "score": np.random.rand()
        }
        for i in range(total_vectors)
    ]

    # 배치 삽입
    result = ops.batch_upsert(
        vectors=vectors,
        payloads=payloads,
        chunk_size=chunk_size,
        wait=True
    )

    return {
        "chunk_size": chunk_size,
        "total_vectors": total_vectors,
        "elapsed_time": result.elapsed_time,
        "throughput": result.data['throughput']
    }


def main():
    """메인 함수"""
    print("=" * 80)
    print("예제 4: 배치 작업 성능 최적화")
    print("=" * 80)

    collection_name = "batch_benchmark"
    vector_size = 384
    total_vectors = 1000  # 테스트할 총 벡터 수

    # 테스트할 청크 크기들
    chunk_sizes = [10, 50, 100, 200, 500]

    try:
        # 1. 컬렉션 준비
        print("\n[1] 컬렉션 준비...")
        col_manager = CollectionManager()
        col_manager.recreate_collection(
            name=collection_name,
            vector_size=vector_size
        )
        print(f"  ✓ 컬렉션 '{collection_name}' 준비 완료")

        # 2. 배치 크기별 성능 벤치마크
        print(f"\n[2] 배치 크기별 성능 측정 (총 {total_vectors}개 벡터)...")
        print("  이 작업은 몇 분 정도 소요될 수 있습니다...\n")

        results = []

        for i, chunk_size in enumerate(chunk_sizes, 1):
            print(f"  [{i}/{len(chunk_sizes)}] 청크 크기: {chunk_size} 테스트 중...")

            # 컬렉션 재생성 (이전 데이터 제거)
            if i > 1:
                col_manager.recreate_collection(
                    name=collection_name,
                    vector_size=vector_size
                )

            ops = VectorOperations(collection_name)

            # 벤치마크 실행
            result = benchmark_batch_insert(
                ops=ops,
                total_vectors=total_vectors,
                chunk_size=chunk_size,
                vector_size=vector_size
            )

            results.append(result)

            print(f"    소요 시간: {result['elapsed_time']:.2f}초")
            print(f"    처리량: {result['throughput']:.0f} ops/s\n")

            # CPU 쿨다운
            time.sleep(1)

        # 3. 결과 분석
        print("\n[3] 성능 비교 결과")
        print("=" * 80)
        print(f"{'청크 크기':<15} {'소요 시간 (초)':<20} {'처리량 (ops/s)':<20} {'상대 성능':<15}")
        print("-" * 80)

        # 기준 성능 (첫 번째 결과)
        baseline_throughput = results[0]['throughput']

        for result in results:
            relative_perf = result['throughput'] / baseline_throughput
            print(
                f"{result['chunk_size']:<15} "
                f"{result['elapsed_time']:<20.2f} "
                f"{result['throughput']:<20.0f} "
                f"{relative_perf:<15.2f}x"
            )

        # 4. 최적 청크 크기 추천
        print("\n" + "=" * 80)
        best_result = max(results, key=lambda x: x['throughput'])
        print(f"✓ 최고 성능: 청크 크기 {best_result['chunk_size']}")
        print(f"  - 소요 시간: {best_result['elapsed_time']:.2f}초")
        print(f"  - 처리량: {best_result['throughput']:.0f} ops/s")

        # 5. 베스트 프랙티스
        print("\n" + "=" * 80)
        print("배치 작업 베스트 프랙티스")
        print("=" * 80)
        print("""
  1. 청크 크기 선택
     - 일반적 권장: 100-500
     - 메모리 제한 있을 때: 50-100
     - 대용량 처리: 500-1000

  2. 성능 vs 메모리 트레이드오프
     - 큰 청크: 빠르지만 메모리 많이 사용
     - 작은 청크: 느리지만 메모리 안정적

  3. 프로덕션 권장사항
     - wait=True: 데이터 무결성 중요
     - wait=False: 처리량 중요 (주의 필요)
     - 에러 핸들링 필수
     - 프로그레스 로깅

  4. 대용량 데이터 처리
     - 파일에서 스트리밍으로 읽기
     - 제너레이터 사용으로 메모리 절약
     - 실패한 청크 재시도 로직
        """)

        # 6. 실전 예제: 대용량 데이터 처리
        print("\n[4] 실전 예제: 대용량 데이터 스트리밍 처리")
        print("=" * 80)

        def generate_vectors(total: int, vector_size: int, batch_size: int):
            """벡터 제너레이터 (메모리 효율적)"""
            for i in range(0, total, batch_size):
                batch_count = min(batch_size, total - i)
                vectors = np.random.rand(batch_count, vector_size).tolist()
                payloads = [
                    {"batch": i // batch_size, "index": j}
                    for j in range(batch_count)
                ]
                yield vectors, payloads

        # 컬렉션 재생성
        col_manager.recreate_collection(
            name=collection_name,
            vector_size=vector_size
        )
        ops = VectorOperations(collection_name)

        # 스트리밍 삽입
        total_to_insert = 5000
        batch_size = 200
        total_inserted = 0
        start_time = time.time()

        print(f"  {total_to_insert}개 벡터를 {batch_size}개씩 스트리밍 삽입 중...\n")

        for i, (vectors, payloads) in enumerate(
            generate_vectors(total_to_insert, vector_size, batch_size)
        ):
            ops.batch_upsert(
                vectors=vectors,
                payloads=payloads,
                chunk_size=100,
                wait=True
            )

            total_inserted += len(vectors)
            progress = (total_inserted / total_to_insert) * 100

            print(f"  진행률: {progress:.1f}% ({total_inserted}/{total_to_insert})", end='\r')

        elapsed = time.time() - start_time
        final_throughput = total_inserted / elapsed

        print(f"\n\n  ✓ 스트리밍 삽입 완료!")
        print(f"    - 총 삽입: {total_inserted}개")
        print(f"    - 소요 시간: {elapsed:.2f}초")
        print(f"    - 평균 처리량: {final_throughput:.0f} ops/s")

        # 최종 확인
        final_count = ops.count_points()
        print(f"    - 검증: {final_count}개 포인트 존재")

        print("\n" + "=" * 80)
        print("✓ 모든 벤치마크 완료!")
        print("=" * 80)

        # 정리
        cleanup = input("\n테스트 컬렉션을 삭제하시겠습니까? (y/N): ")
        if cleanup.lower() == 'y':
            col_manager.delete_collection(collection_name)
            print("  ✓ 컬렉션 삭제 완료")

    except Exception as e:
        logger.error(f"에러 발생: {e}", exc_info=True)
        print(f"\n✗ 실패: {e}")


if __name__ == "__main__":
    main()
