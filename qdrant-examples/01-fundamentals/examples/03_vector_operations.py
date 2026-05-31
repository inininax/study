"""
예제 3: 벡터 CRUD 작업

기본적인 벡터 삽입, 조회, 업데이트, 삭제 작업
"""

import sys
sys.path.append('..')

from core.operations import VectorOperations
from core.collections import CollectionManager
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """메인 함수"""
    print("=" * 60)
    print("예제 3: 벡터 CRUD 작업")
    print("=" * 60)

    collection_name = "crud_test"
    vector_size = 384

    try:
        # 1. 컬렉션 준비
        print("\n[1] 컬렉션 준비...")
        col_manager = CollectionManager()

        # 기존 컬렉션 재생성
        col_manager.recreate_collection(
            name=collection_name,
            vector_size=vector_size
        )
        print(f"  ✓ 컬렉션 '{collection_name}' 준비 완료")

        # 2. VectorOperations 인스턴스 생성
        ops = VectorOperations(collection_name)
        print(f"  ✓ 벡터 작업 클래스 초기화 (벡터 크기: {ops.vector_size})")

        # 3. 단일 벡터 삽입 (CREATE)
        print("\n[2] 단일 벡터 삽입...")

        # 랜덤 벡터 생성
        vector1 = np.random.rand(vector_size).tolist()

        point_id_1 = ops.upsert_point(
            vector=vector1,
            payload={
                "title": "Python 프로그래밍 완벽 가이드",
                "author": "홍길동",
                "category": "programming",
                "year": 2024,
                "rating": 4.5,
                "created_at": datetime.now().isoformat()
            }
        )

        print(f"  ✓ 포인트 삽입 완료: ID = {point_id_1}")

        # 4. 벡터 조회 (READ)
        print("\n[3] 벡터 조회...")

        point = ops.get_point(
            point_id=point_id_1,
            with_payload=True,
            with_vectors=False  # 벡터는 크므로 제외
        )

        if point:
            print(f"  ✓ 포인트 조회 성공:")
            print(f"    - ID: {point.id}")
            print(f"    - 페이로드:")
            for key, value in point.payload.items():
                print(f"      • {key}: {value}")

        # 5. 페이로드 업데이트 (UPDATE)
        print("\n[4] 페이로드 업데이트...")

        # 기존 페이로드에 필드 추가
        ops.update_payload(
            point_id=point_id_1,
            payload={
                "views": 1000,
                "likes": 150,
                "updated_at": datetime.now().isoformat()
            }
        )

        print("  ✓ 페이로드 업데이트 완료 (기존 데이터 + 새 데이터)")

        # 업데이트 확인
        updated_point = ops.get_point(point_id_1, with_vectors=False)
        print(f"  업데이트된 페이로드:")
        for key, value in updated_point.payload.items():
            print(f"    • {key}: {value}")

        # 6. 페이로드 덮어쓰기
        print("\n[5] 페이로드 덮어쓰기...")

        vector2 = np.random.rand(vector_size).tolist()
        point_id_2 = ops.upsert_point(
            vector=vector2,
            payload={"temp": "임시 데이터"}
        )

        print(f"  임시 포인트 생성: {point_id_2}")

        # 전체 페이로드 교체
        ops.overwrite_payload(
            point_id=point_id_2,
            payload={
                "title": "새로운 제목",
                "description": "완전히 새로운 데이터"
            }
        )

        overwritten_point = ops.get_point(point_id_2, with_vectors=False)
        print(f"  ✓ 페이로드 덮어쓰기 완료:")
        print(f"    {overwritten_point.payload}")

        # 7. 여러 벡터 삽입
        print("\n[6] 여러 벡터 삽입...")

        sample_docs = [
            {"title": "머신러닝 기초", "category": "AI", "year": 2023},
            {"title": "딥러닝 심화", "category": "AI", "year": 2024},
            {"title": "웹 개발 입문", "category": "web", "year": 2022},
            {"title": "데이터베이스 설계", "category": "database", "year": 2023},
        ]

        vectors = [np.random.rand(vector_size).tolist() for _ in sample_docs]

        result = ops.batch_upsert(
            vectors=vectors,
            payloads=sample_docs,
            chunk_size=2
        )

        print(f"  ✓ {result.data['inserted']}개 포인트 삽입 완료")
        print(f"  소요 시간: {result.elapsed_time:.3f}초")
        print(f"  처리량: {result.data['throughput']:.0f} ops/s")

        # 8. 전체 포인트 수 확인
        print("\n[7] 컬렉션 통계...")
        total_points = ops.count_points()
        print(f"  ✓ 총 포인트 수: {total_points}")

        # 9. 벡터 삭제 (DELETE)
        print("\n[8] 벡터 삭제...")

        ops.delete_point(point_id_2)
        print(f"  ✓ 포인트 삭제 완료: {point_id_2}")

        # 삭제 확인
        deleted_point = ops.get_point(point_id_2)
        if deleted_point is None:
            print("  ✓ 포인트가 정상적으로 삭제되었습니다")

        # 10. 필터로 삭제
        print("\n[9] 필터 조건으로 삭제...")

        # year=2023인 모든 포인트 삭제
        delete_result = ops.delete_by_filter(
            filter_conditions={"year": 2023}
        )

        print(f"  ✓ 필터 삭제 완료: {delete_result.message}")
        print(f"  조건: {delete_result.data['filter']}")

        # 11. 최종 통계
        print("\n[10] 최종 통계...")
        final_count = ops.count_points()
        print(f"  ✓ 남은 포인트 수: {final_count}")

        print("\n" + "=" * 60)
        print("✓ 모든 CRUD 작업 완료!")
        print("=" * 60)

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
