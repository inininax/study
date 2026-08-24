"""
캐싱 전략

상황별 캐싱 전략 구현:
- Cache-Aside: 조회 시 먼저 캐시 확인, 미스 시 원본 조회 후 캐시 저장 (가장 일반적)
- Write-Through: 데이터 변경 시 항상 캐시와 원본에 동시 기록 (정합성 우선)
- TTL Refresh: 접근이 잦은 키의 만료 시간을 연장 (핫 데이터 유지)

실행:
    python caching/strategies.py
"""

import time
import logging
from typing import Any, Callable, Optional

from redis import Redis
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseCacheStrategy:
    """캐싱 전략 공통 베이스 클래스"""

    def __init__(self, redis_client: Redis, ttl: int = 3600, prefix: str = "strategy"):
        """
        Args:
            redis_client: Redis 클라이언트
            ttl: 기본 만료 시간(초)
            prefix: 키 네임스페이스
        """
        self.redis = redis_client
        self.ttl = ttl
        self.prefix = prefix

    def _key(self, name: str) -> str:
        """네임스페이스가 적용된 키 생성"""
        return f"{self.prefix}:{name}"


class CacheAsideStrategy(BaseCacheStrategy):
    """
    Cache-Aside (Lazy Loading) 전략

    흐름: 요청 -> 캐시 확인 -> HIT 이면 반환 / MISS 이면 DB 조회 -> 캐시 저장 -> 반환

    장점: 필요한 데이터만 캐시됨, 장애 격리(Redis 다운 시에도 서비스 가능)
    단점: 첫 요청은 느림, 원본 갱신과 캐시 사이에 짧은 불일치 가능
    """

    def get_or_load(self, key: str, loader: Callable[[], Any]) -> Any:
        """
        캐시에서 조회하거나, 없으면 loader 로 로드 후 캐시

        Args:
            key: 캐시 키
            loader: 캐시 미스 시 실행할 원본 조회 함수

        Returns:
            조회 결과
        """
        cache_key = self._key(key)

        # 1. 캐시 확인
        cached = self.redis.get(cache_key)
        if cached is not None:
            logger.info(f"[cache-aside] HIT: {key}")
            return cached

        # 2. MISS - 원본에서 로드
        logger.info(f"[cache-aside] MISS: {key}")
        value = str(loader())

        # 3. 캐시 저장
        self.redis.setex(cache_key, self.ttl, value)
        return value

    def invalidate(self, key: str):
        """원본 데이터 변경 시 캐시 무효화"""
        self.redis.delete(self._key(key))
        logger.info(f"[cache-aside] 무효화: {key}")


class WriteThroughStrategy(BaseCacheStrategy):
    """
    Write-Through 전략

    흐름: 쓰기 요청 -> 캐시 기록 -> 원본 기록 (동시)

    장점: 캐시와 원본이 항상 일치 (강한 정합성)
    단점: 쓰기 지연 증가, 사용되지 않을 데이터도 캐시됨
    """

    def write(self, key: str, compute_value: Callable[[], Any], persist: Callable[[str], None]) -> Any:
        """
        캐시와 원본에 동시 기록

        Args:
            key: 캐시 키
            compute_value: 저장할 값 계산 함수
            persist: 원본 저장소에 기록하는 함수

        Returns:
            저장된 값
        """
        cache_key = self._key(key)
        value = str(compute_value())

        # 1. 원본 저장소 기록 (실제로는 캐시보다 먼저/동시에)
        persist(value)
        # 2. 캐시 기록
        self.redis.setex(cache_key, self.ttl, value)

        logger.info(f"[write-through] 캐시+원본 동시 기록: {key}")
        return value

    def read(self, key: str) -> Optional[str]:
        """읽기는 항상 캐시 우선 (write-through 덕분에 항상 최신)"""
        cached = self.redis.get(self._key(key))
        if cached is not None:
            logger.info(f"[write-through] HIT: {key}")
        else:
            logger.info(f"[write-through] MISS: {key} (쓰기 경유 데이터만 캐시됨)")
        return cached


class TTLRefreshStrategy(BaseCacheStrategy):
    """
    TTL Refresh 전략

    자주 조회되는 키는 만료 시간을 연장해 핫 데이터를 캐시에 유지한다.
    인기 상품/인기 문서 검색처럼 접근 편중이 있는 경우에 유효하다.
    """

    def __init__(self, *args, refresh_threshold_ratio: float = 0.5, **kwargs):
        """
        Args:
            refresh_threshold_ratio: 남은 TTL 비율이 이 값 이하면 만료 연장
        """
        super().__init__(*args, **kwargs)
        self.refresh_threshold_ratio = refresh_threshold_ratio

    def get_with_refresh(self, key: str) -> Optional[str]:
        """
        조회 + 필요 시 TTL 연장

        Args:
            key: 캐시 키
        """
        cache_key = self._key(key)
        value = self.redis.get(cache_key)

        if value is None:
            logger.info(f"[ttl-refresh] MISS: {key}")
            return None

        # 남은 수명 확인 후 임계값 이하면 연장
        remaining_ttl = self.redis.ttl(cache_key)
        if 0 < remaining_ttl < self.ttl * self.refresh_threshold_ratio:
            self.redis.expire(cache_key, self.ttl)
            logger.info(
                f"[ttl-refresh] TTL 연장: {key} "
                f"(남은 {remaining_ttl}s -> {self.ttl}s)"
            )

        logger.info(f"[ttl-refresh] HIT: {key}")
        return value


def main():
    """메인 함수 - 세 가지 전략 데모"""
    print("=" * 60)
    print("캐싱 전략 데모")
    print("=" * 60)

    try:
        redis_client = Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            password=os.getenv("REDIS_PASSWORD") or None,
            decode_responses=True,
        )
        redis_client.ping()
        print("✓ Redis 연결 성공\n")

        # 1. Cache-Aside: 첫 호출은 MISS, 이후 HIT
        print("[1] Cache-Aside")
        counter = {"n": 0}

        def expensive_loader():
            counter["n"] += 1  # 원본 조회 비용 흉내
            return f"db-value-{counter['n']}"

        aside = CacheAsideStrategy(redis_client, ttl=60, prefix="demo_aside")
        redis_client.flushdb()

        for i in range(3):
            value = aside.get_or_load("popular_query", expensive_loader)
            print(f"  조회 {i + 1}: {value}")

        # 2. Write-Through: 쓰기 시 캐시+원본 동시 기록
        print("\n[2] Write-Through")
        persisted = {}

        through = WriteThroughStrategy(redis_client, ttl=60, prefix="demo_through")
        through.write("product:42", lambda: "product-data-v2", persisted.__setitem__)
        result = through.read("product:42")  # 캐시 HIT 보장
        print(f"  읽은 값: {result}, 원본 저장: {persisted}")

        # 3. TTL Refresh: 짧은 TTL 로 설정 후 반복 조회로 만료 연장 확인
        print("\n[3] TTL Refresh")
        refresh = TTLRefreshStrategy(
            redis_client, ttl=5, prefix="demo_ttl", refresh_threshold_ratio=0.8
        )
        redis_client.setex(refresh._key("hot_item"), 5, "hot-value")

        for i in range(3):
            value = refresh.get_with_refresh("hot_item")
            remaining = redis_client.ttl(refresh._key("hot_item"))
            print(f"  조회 {i + 1}: {value} (남은 TTL: {remaining}s)")
            time.sleep(0.5)

        print("\n" + "=" * 60)
        print("✓ 데모 완료!")
        print("=" * 60)

    except Exception as e:
        logger.error(f"에러 발생: {e}")
        print(f"\n✗ 실패: {e}")
        print("\n해결 방법:")
        print("1. Docker Compose로 Redis가 실행 중인지 확인:")
        print("   $ docker-compose up -d redis")


if __name__ == "__main__":
    main()
