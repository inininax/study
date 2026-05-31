"""
예제 5: 에러 핸들링 및 재시도 로직

프로덕션 환경에서의 견고한 에러 처리 예제
"""

import sys
sys.path.append('..')

from core.operations import VectorOperations
from core.collections import CollectionManager
from core.exceptions import (
    QdrantConnectionError,
    QdrantTimeoutError,
    CollectionNotFoundError,
    VectorDimensionMismatchError,
    BatchOperationError
)
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import numpy as np
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RobustVectorInserter:
    """견고한 벡터 삽입 클래스"""

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.ops = None
        self._initialize()

    def _initialize(self):
        """초기화 (재시도 로직 포함)"""
        try:
            self.ops = VectorOperations(self.collection_name, auto_create=True)
        except CollectionNotFoundError:
            logger.error(f"컬렉션을 찾을 수 없음: {self.collection_name}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((QdrantTimeoutError, ConnectionError))
    )
    def insert_with_retry(
        self,
        vector: list,
        payload: dict,
        point_id: str = None
    ) -> str:
        """
        재시도 로직이 있는 벡터 삽입

        타임아웃이나 일시적 연결 오류 시 자동 재시도
        """
        try:
            logger.info(f"벡터 삽입 시도: {point_id or 'auto'}")

            point_id = self.ops.upsert_point(
                vector=vector,
                payload=payload,
                point_id=point_id
            )

            logger.info(f"✓ 벡터 삽입 성공: {point_id}")
            return point_id

        except VectorDimensionMismatchError as e:
            # 벡터 차원 오류는 재시도해도 소용없음
            logger.error(f"벡터 차원 오류 (재시도 불가): {e}")
            raise

        except Exception as e:
            logger.warning(f"삽입 실패, 재시도 중... 에러: {e}")
            raise

    def batch_insert_with_error_recovery(
        self,
        vectors: list,
        payloads: list,
        chunk_size: int = 100
    ) -> dict:
        """
        에러 복구 기능이 있는 배치 삽입

        실패한 청크를 추적하고 재시도
        """
        total_count = len(vectors)
        success_count = 0
        failed_chunks = []

        logger.info(f"배치 삽입 시작: {total_count}개 벡터")

        # 청크 단위로 처리
        for i in range(0, total_count, chunk_size):
            chunk_vectors = vectors[i:i+chunk_size]
            chunk_payloads = payloads[i:i+chunk_size]
            chunk_id = i // chunk_size

            try:
                result = self.ops.batch_upsert(
                    vectors=chunk_vectors,
                    payloads=chunk_payloads,
                    chunk_size=chunk_size
                )

                success_count += result.data['inserted']
                logger.info(
                    f"청크 {chunk_id} 성공: {result.data['inserted']}개 삽입"
                )

            except BatchOperationError as e:
                logger.error(f"청크 {chunk_id} 실패: {e}")
                failed_chunks.append({
                    "chunk_id": chunk_id,
                    "start_idx": i,
                    "end_idx": i + len(chunk_vectors),
                    "error": str(e)
                })

        # 실패한 청크 재시도
        if failed_chunks:
            logger.warning(f"{len(failed_chunks)}개 청크 재시도 중...")

            for chunk_info in failed_chunks:
                start = chunk_info['start_idx']
                end = chunk_info['end_idx']

                try:
                    # 더 작은 청크로 재시도
                    smaller_chunk_size = chunk_size // 2

                    result = self.ops.batch_upsert(
                        vectors=vectors[start:end],
                        payloads=payloads[start:end],
                        chunk_size=smaller_chunk_size
                    )

                    success_count += result.data['inserted']
                    logger.info(f"재시도 성공: 청크 {chunk_info['chunk_id']}")

                except Exception as e:
                    logger.error(f"재시도 실패: 청크 {chunk_info['chunk_id']} - {e}")

        return {
            "total": total_count,
            "success": success_count,
            "failed": total_count - success_count,
            "failed_chunks": failed_chunks
        }


def main():
    """메인 함수"""
    print("=" * 80)
    print("예제 5: 에러 핸들링 및 재시도 로직")
    print("=" * 80)

    collection_name = "error_handling_test"
    vector_size = 384

    try:
        # 1. 컬렉션 준비
        print("\n[1] 컬렉션 준비...")
        col_manager = CollectionManager()
        col_manager.recreate_collection(
            name=collection_name,
            vector_size=vector_size
        )
        print("  ✓ 컬렉션 준비 완료")

        # 2. 기본 에러 핸들링
        print("\n[2] 기본 에러 핸들링 예제...")

        ops = VectorOperations(collection_name)

        # 2-1. 벡터 차원 불일치 에러
        print("\n  (a) 벡터 차원 불일치 에러 테스트:")
        try:
            wrong_vector = [0.1, 0.2, 0.3]  # 잘못된 차원
            ops.upsert_point(vector=wrong_vector, payload={"test": "fail"})
        except VectorDimensionMismatchError as e:
            print(f"    ✓ 예상된 에러 캐치: {e.message}")
            print(f"      세부사항: {e.details}")

        # 2-2. 존재하지 않는 컬렉션
        print("\n  (b) 존재하지 않는 컬렉션 에러 테스트:")
        try:
            VectorOperations("non_existent_collection", auto_create=False)
        except CollectionNotFoundError as e:
            print(f"    ✓ 예상된 에러 캐치: {e.message}")

        # 2-3. 존재하지 않는 포인트 조회
        print("\n  (c) 존재하지 않는 포인트 조회:")
        result = ops.get_point("non_existent_id")
        if result is None:
            print("    ✓ None 반환 (에러 없음)")

        # 3. 재시도 로직
        print("\n[3] 재시도 로직 테스트...")

        inserter = RobustVectorInserter(collection_name)

        # 정상 삽입
        vector = np.random.rand(vector_size).tolist()
        payload = {"title": "테스트 문서", "retry_test": True}

        point_id = inserter.insert_with_retry(
            vector=vector,
            payload=payload,
            point_id="test_point_1"
        )

        print(f"  ✓ 재시도 로직으로 삽입 성공: {point_id}")

        # 4. 배치 에러 복구
        print("\n[4] 배치 작업 에러 복구 테스트...")

        # 테스트 데이터 생성 (일부 잘못된 데이터 포함)
        test_vectors = []
        test_payloads = []

        for i in range(500):
            # 99%는 정상, 1%는 에러 시뮬레이션용
            if i % 100 == 0:
                # 의도적으로 잘못된 차원 (에러 시뮬레이션)
                # 실제로는 VectorOperations가 검증하므로 정상 데이터만 사용
                test_vectors.append(np.random.rand(vector_size).tolist())
            else:
                test_vectors.append(np.random.rand(vector_size).tolist())

            test_payloads.append({
                "index": i,
                "category": f"cat_{i % 10}"
            })

        result = inserter.batch_insert_with_error_recovery(
            vectors=test_vectors,
            payloads=test_payloads,
            chunk_size=100
        )

        print(f"\n  배치 삽입 결과:")
        print(f"    - 총 벡터: {result['total']}")
        print(f"    - 성공: {result['success']}")
        print(f"    - 실패: {result['failed']}")

        if result['failed'] == 0:
            print(f"    ✓ 모든 벡터 삽입 성공!")
        else:
            print(f"    ⚠ 일부 벡터 삽입 실패")
            print(f"    실패한 청크: {len(result['failed_chunks'])}")

        # 5. 베스트 프랙티스
        print("\n" + "=" * 80)
        print("에러 핸들링 베스트 프랙티스")
        print("=" * 80)
        print("""
  1. 에러 타입별 처리 전략

     a) VectorDimensionMismatchError
        - 재시도 불필요 (데이터 문제)
        - 로깅 후 스킵 또는 중단
        - 데이터 검증 강화

     b) QdrantTimeoutError / ConnectionError
        - 재시도 권장 (일시적 문제)
        - Exponential backoff 사용
        - 최대 재시도 횟수 설정

     c) CollectionNotFoundError
        - auto_create 옵션 활용
        - 또는 사전 컬렉션 생성

     d) BatchOperationError
        - 청크 크기 줄여서 재시도
        - 실패한 항목만 별도 처리

  2. 재시도 전략

     - Exponential Backoff: 2초, 4초, 8초...
     - 최대 재시도: 3-5회
     - Jitter 추가로 동시 재시도 분산

  3. 로깅 및 모니터링

     - 모든 에러 로깅
     - 재시도 횟수 추적
     - 실패율 모니터링
     - 알림 설정 (실패율 임계값)

  4. 프로덕션 체크리스트

     ✓ 모든 API 호출에 timeout 설정
     ✓ 중요 작업은 재시도 로직 구현
     ✓ 에러 로그에 컨텍스트 포함
     ✓ 장애 시나리오 테스트
     ✓ 서킷 브레이커 패턴 고려
        """)

        # 6. 최종 검증
        print("\n[5] 최종 검증...")
        final_count = ops.count_points()
        print(f"  ✓ 총 {final_count}개 포인트 존재")

        print("\n" + "=" * 80)
        print("✓ 모든 에러 핸들링 테스트 완료!")
        print("=" * 80)

        # 정리
        cleanup = input("\n테스트 컬렉션을 삭제하시겠습니까? (y/N): ")
        if cleanup.lower() == 'y':
            col_manager.delete_collection(collection_name)
            print("  ✓ 컬렉션 삭제 완료")

    except Exception as e:
        logger.error(f"예상치 못한 에러: {e}", exc_info=True)
        print(f"\n✗ 실패: {e}")


if __name__ == "__main__":
    main()
