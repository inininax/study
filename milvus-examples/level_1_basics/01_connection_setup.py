"""
Level 1-1: Milvus Connection Setup & Management

이 모듈은 Milvus 연결 관리의 모든 측면을 다룹니다:
- 기본 연결 설정
- Connection pooling
- Health checks
- Automatic reconnection
- Error handling

Production-ready 패턴을 사용하여 안정적인 연결 관리를 구현합니다.
"""

import argparse
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from pymilvus import connections, utility

from config.settings import settings
from utils.connection import MilvusConnectionManager, get_milvus_client
from utils.decorators import timing_decorator
from utils.logger import get_logger

logger = get_logger(__name__)


@timing_decorator
def test_single_connection():
    """
    테스트 1: 단일 연결 설정

    학습 포인트:
    - 기본 연결 파라미터
    - 연결 성공/실패 처리
    - 연결 상태 확인
    """
    logger.info("=== Test 1: Single Connection ===")

    try:
        # 연결 설정
        connections.connect(
            alias="default",
            host=settings.milvus_host,
            port=settings.milvus_port,
            user=settings.milvus_user or "",
            password=settings.milvus_password or "",
        )

        logger.info(
            "connection_established",
            host=settings.milvus_host,
            port=settings.milvus_port,
        )

        # 연결 확인 - 서버 버전 조회
        server_version = utility.get_server_version()
        logger.info("milvus_server_version", version=server_version)

        # Collection 리스트 조회로 연결 테스트
        collections = utility.list_collections()
        logger.info("existing_collections", count=len(collections), collections=collections)

        return True

    except Exception as e:
        logger.error(
            "connection_failed",
            error=str(e),
            error_type=type(e).__name__,
            host=settings.milvus_host,
            port=settings.milvus_port,
        )
        return False

    finally:
        # 연결 해제
        try:
            connections.disconnect("default")
            logger.info("connection_closed", alias="default")
        except:
            pass


@timing_decorator
def test_connection_pool():
    """
    테스트 2: Connection Pool 사용

    학습 포인트:
    - Connection pooling 이점
    - Pool 크기 설정
    - Connection 재사용
    - 동시성 처리
    """
    logger.info("=== Test 2: Connection Pool ===")

    try:
        # Global connection pool 사용
        pool = get_milvus_client()

        logger.info(
            "connection_pool_created",
            pool_size=settings.milvus_pool_size,
            host=settings.milvus_host,
        )

        # Pool에서 연결 가져오기 및 반환 테스트
        connections_tested = []

        for i in range(5):
            with pool.get_connection_context() as conn:
                # 연결 사용
                collections = utility.list_collections(using=conn.alias)

                logger.info(
                    "connection_acquired_from_pool",
                    iteration=i + 1,
                    alias=conn.alias,
                    collections_count=len(collections),
                )

                connections_tested.append(conn.alias)

                # 작업 시뮬레이션
                time.sleep(0.1)

            # Context manager가 자동으로 연결을 pool에 반환

        logger.info(
            "connection_pool_test_completed",
            total_connections_used=len(connections_tested),
        )

        return True

    except Exception as e:
        logger.error(
            "connection_pool_test_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        return False


@timing_decorator
def test_health_check():
    """
    테스트 3: Health Check & Monitoring

    학습 포인트:
    - 연결 상태 모니터링
    - Health check 구현
    - 장애 감지
    - Automatic recovery
    """
    logger.info("=== Test 3: Health Check ===")

    try:
        pool = get_milvus_client()

        # 여러 번 health check 수행
        for i in range(3):
            logger.info("health_check_iteration", iteration=i + 1)

            with pool.get_connection_context() as conn:
                # Health check 수행
                is_healthy = conn.check_health()

                logger.info(
                    "health_check_result",
                    iteration=i + 1,
                    alias=conn.alias,
                    is_healthy=is_healthy,
                    age_seconds=int(time.time() - conn.created_at),
                    idle_seconds=int(time.time() - conn.last_used),
                )

                if is_healthy:
                    # 추가 정보 수집
                    collections = utility.list_collections(using=conn.alias)
                    logger.info("health_check_details", collections_count=len(collections))

            time.sleep(1)

        return True

    except Exception as e:
        logger.error(
            "health_check_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        return False


@timing_decorator
def test_connection_manager():
    """
    테스트 4: High-level Connection Manager 사용

    학습 포인트:
    - 추상화된 연결 관리
    - Collection 접근 패턴
    - 자동 에러 처리
    """
    logger.info("=== Test 4: Connection Manager ===")

    try:
        manager = MilvusConnectionManager()

        # Collection 존재 여부 확인
        test_collection = "test_connection"
        exists = manager.collection_exists(test_collection)

        logger.info(
            "collection_exists_check",
            collection=test_collection,
            exists=exists,
        )

        # 모든 Collection 리스트
        all_collections = manager.list_collections()
        logger.info(
            "all_collections_listed",
            count=len(all_collections),
            collections=all_collections,
        )

        # 실제 collection이 있다면 접근 테스트
        if all_collections:
            collection_name = all_collections[0]

            with manager.get_collection(collection_name) as collection:
                logger.info(
                    "collection_accessed",
                    name=collection_name,
                    num_entities=collection.num_entities,
                )

        return True

    except Exception as e:
        logger.error(
            "connection_manager_test_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        return False


def test_error_scenarios():
    """
    테스트 5: 에러 시나리오 처리

    학습 포인트:
    - 잘못된 연결 정보 처리
    - Timeout 처리
    - Graceful degradation
    """
    logger.info("=== Test 5: Error Scenarios ===")

    # 1. 잘못된 호스트로 연결 시도
    logger.info("testing_invalid_host")

    try:
        connections.connect(
            alias="invalid",
            host="invalid-host-12345",
            port=19530,
            timeout=5,
        )
        logger.error("should_have_failed_but_didnt")
        return False

    except Exception as e:
        logger.info(
            "expected_connection_failure",
            error_type=type(e).__name__,
            message=str(e)[:100],
        )

    # 2. 연결 없이 작업 시도
    logger.info("testing_operation_without_connection")

    try:
        utility.list_collections(using="non_existent_alias")
        logger.error("should_have_failed_but_didnt")
        return False

    except Exception as e:
        logger.info(
            "expected_operation_failure",
            error_type=type(e).__name__,
            message=str(e)[:100],
        )

    logger.info("error_scenario_tests_passed")
    return True


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="Milvus Connection Setup Examples")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["single", "pool", "health", "manager", "error", "all"],
        default="all",
        help="Test mode to run",
    )

    args = parser.parse_args()

    logger.info(
        "starting_connection_tests",
        mode=args.mode,
        milvus_host=settings.milvus_host,
        milvus_port=settings.milvus_port,
    )

    results = {}

    try:
        if args.mode in ["single", "all"]:
            results["single"] = test_single_connection()

        if args.mode in ["pool", "all"]:
            results["pool"] = test_connection_pool()

        if args.mode in ["health", "all"]:
            results["health"] = test_health_check()

        if args.mode in ["manager", "all"]:
            results["manager"] = test_connection_manager()

        if args.mode in ["error", "all"]:
            results["error"] = test_error_scenarios()

        # 결과 요약
        logger.info("\n" + "="*50)
        logger.info("TEST RESULTS SUMMARY")
        logger.info("="*50)

        for test_name, passed in results.items():
            status = "✓ PASSED" if passed else "✗ FAILED"
            logger.info(f"{test_name:20s}: {status}")

        all_passed = all(results.values())
        logger.info("="*50)

        if all_passed:
            logger.info("🎉 All tests passed!")
            return 0
        else:
            logger.error("❌ Some tests failed")
            return 1

    except KeyboardInterrupt:
        logger.info("tests_interrupted_by_user")
        return 1

    except Exception as e:
        logger.error(
            "unexpected_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
