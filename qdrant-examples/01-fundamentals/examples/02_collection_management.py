"""
예제 2: 컬렉션 생성 및 관리

다양한 거리 메트릭을 사용한 컬렉션 생성 및 관리
"""

import sys
sys.path.append('..')

from core.collections import CollectionManager
from qdrant_client.models import Distance
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """메인 함수"""
    print("=" * 60)
    print("예제 2: 컬렉션 생성 및 관리")
    print("=" * 60)

    manager = CollectionManager()

    # 테스트용 컬렉션 이름
    collections_to_create = [
        {
            "name": "documents_cosine",
            "vector_size": 384,
            "distance": Distance.COSINE,
            "description": "텍스트 임베딩용 (Cosine 유사도)"
        },
        {
            "name": "images_dot",
            "vector_size": 512,
            "distance": Distance.DOT,
            "description": "이미지 임베딩용 (Dot Product)"
        },
        {
            "name": "locations_euclid",
            "vector_size": 2,
            "distance": Distance.EUCLID,
            "description": "좌표 데이터용 (Euclidean 거리)"
        }
    ]

    try:
        # 1. 컬렉션 생성
        print("\n[1] 컬렉션 생성...")
        for config in collections_to_create:
            print(f"\n  생성 중: {config['name']}")
            print(f"  설명: {config['description']}")
            print(f"  벡터 크기: {config['vector_size']}")
            print(f"  거리 메트릭: {config['distance']}")

            # 기존 컬렉션 삭제 (있다면)
            if manager.collection_exists(config['name']):
                print(f"  → 기존 컬렉션 삭제 중...")
                manager.delete_collection(config['name'])

            # 새 컬렉션 생성
            info = manager.create_collection(
                name=config['name'],
                vector_size=config['vector_size'],
                distance=config['distance'],
                hnsw_config={
                    "m": 16,  # 각 노드의 최대 연결 수
                    "ef_construct": 100  # 인덱스 구성 시 탐색 깊이
                }
            )

            print(f"  ✓ 생성 완료: {info.name}")

        # 2. 컬렉션 목록 확인
        print("\n[2] 생성된 컬렉션 확인...")
        all_collections = manager.client.get_collections().collections

        print(f"\n  총 {len(all_collections)}개의 컬렉션:")
        for coll in all_collections:
            print(f"  - {coll.name}")

        # 3. 각 컬렉션 상세 정보 조회
        print("\n[3] 컬렉션 상세 정보...")
        for config in collections_to_create:
            info = manager.get_collection_info(config['name'])
            print(f"\n  컬렉션: {info.name}")
            print(f"  - 벡터 크기: {info.vector_size}")
            print(f"  - 거리 메트릭: {info.distance}")
            print(f"  - 포인트 수: {info.points_count}")
            print(f"  - 인덱싱된 벡터 수: {info.indexed_vectors_count}")
            print(f"  - 상태: {info.status}")

        # 4. HNSW 파라미터 최적화 예제
        print("\n[4] HNSW 파라미터 업데이트 예제...")
        print("  documents_cosine 컬렉션의 HNSW 파라미터 최적화 중...")

        manager.update_collection_params(
            name="documents_cosine",
            hnsw_config={
                "m": 32,  # 연결 수 증가 (더 정확하지만 메모리 사용 증가)
                "ef_construct": 200  # 구성 품질 향상
            }
        )
        print("  ✓ 파라미터 업데이트 완료")

        # 5. 거리 메트릭 선택 가이드
        print("\n" + "=" * 60)
        print("거리 메트릭 선택 가이드")
        print("=" * 60)
        print("""
  1. Cosine Similarity (코사인 유사도)
     - 사용처: 텍스트 임베딩, 문서 유사도
     - 특징: 방향만 고려, 크기 무시
     - 범위: -1 ~ 1 (1에 가까울수록 유사)
     - 추천: sentence-transformers 등

  2. Dot Product (내적)
     - 사용처: 정규화된 벡터, 추천 시스템
     - 특징: 방향과 크기 모두 고려
     - 범위: -∞ ~ ∞
     - 추천: 사전 정규화된 임베딩

  3. Euclidean Distance (유클리드 거리)
     - 사용처: 좌표 데이터, 이미지 특징
     - 특징: 실제 거리 계산
     - 범위: 0 ~ ∞ (0에 가까울수록 유사)
     - 추천: 공간 데이터, 클러스터링

  4. Manhattan Distance (맨해튼 거리)
     - 사용처: 격자 기반 데이터
     - 특징: 축 방향 거리의 합
     - 범위: 0 ~ ∞
     - 추천: 특수한 경우
        """)

        print("\n✓ 모든 작업 완료!")

        # 6. 정리 (선택사항)
        print("\n[5] 생성된 컬렉션 정리 (삭제)...")
        cleanup = input("테스트 컬렉션을 삭제하시겠습니까? (y/N): ")

        if cleanup.lower() == 'y':
            for config in collections_to_create:
                print(f"  삭제 중: {config['name']}")
                manager.delete_collection(config['name'])
            print("  ✓ 모든 테스트 컬렉션 삭제 완료")
        else:
            print("  컬렉션 유지 (나중에 수동 삭제 필요)")

    except Exception as e:
        logger.error(f"에러 발생: {e}", exc_info=True)
        print(f"\n✗ 실패: {e}")


if __name__ == "__main__":
    main()
