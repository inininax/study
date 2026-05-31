"""
예제 1: 기본 연결 및 헬스체크

Qdrant 서버에 연결하고 기본적인 헬스체크를 수행합니다.
"""

import sys
sys.path.append('..')

from core.client import QdrantClientManager
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """메인 함수"""
    print("=" * 60)
    print("예제 1: Qdrant 기본 연결 및 헬스체크")
    print("=" * 60)

    try:
        # 1. 클라이언트 생성
        print("\n[1] Qdrant 클라이언트 생성 중...")
        client_manager = QdrantClientManager(
            host="localhost",
            port=6333,
            timeout=30
        )
        print("✓ 클라이언트 생성 완료")

        # 2. 헬스체크
        print("\n[2] 서버 헬스체크...")
        if client_manager.health_check():
            print("✓ Qdrant 서버 정상 작동 중")
        else:
            print("✗ Qdrant 서버 응답 없음")
            return

        # 3. 컬렉션 목록 조회
        print("\n[3] 컬렉션 목록 조회...")
        collections = client_manager.list_collections()

        if collections:
            print(f"✓ 총 {len(collections)}개의 컬렉션 발견:")
            for i, coll in enumerate(collections, 1):
                print(f"   {i}. {coll}")
        else:
            print("  컬렉션이 없습니다.")

        # 4. 클라이언트 정보 출력
        print(f"\n[4] 클라이언트 정보:")
        print(f"  - 호스트: {client_manager.host}")
        print(f"  - 포트: {client_manager.port}")
        print(f"  - gRPC 포트: {client_manager.grpc_port}")
        print(f"  - 타임아웃: {client_manager.timeout}초")
        print(f"  - 상태: {client_manager}")

        print("\n" + "=" * 60)
        print("✓ 모든 테스트 통과!")
        print("=" * 60)

    except Exception as e:
        logger.error(f"에러 발생: {e}")
        print(f"\n✗ 실패: {e}")
        print("\n해결 방법:")
        print("1. Docker Compose로 Qdrant 서버가 실행 중인지 확인:")
        print("   $ docker-compose up -d qdrant")
        print("2. 서버가 응답하는지 확인:")
        print("   $ curl http://localhost:6333/")


if __name__ == "__main__":
    main()
