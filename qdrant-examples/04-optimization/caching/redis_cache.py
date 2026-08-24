"""
Redis 벡터 검색 캐시

동일한(또는 유사한) 쿼리 벡터에 대한 검색 결과를 Redis 에 캐싱해
Qdrant 부하를 줄이고 응답 시간을 단축한다.

필요 서비스:
    docker-compose up -d redis

실행:
    python caching/redis_cache.py
"""

import os
import json
import hashlib
import logging
import functools
import inspect
from typing import Any, Callable, List, Optional

import numpy as np
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from redis import Redis

# 환경 변수 로드
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VectorCache:
    """
    벡터 검색 결과 캐시

    Features:
    - 쿼리 벡터 기반 캐시 키 생성 (벡터 해시)
    - 동기/비동기 함수 모두 지원하는 데코레이터
    - TTL 만료 관리
    - 히트/미스 통계 수집

    Example:
        >>> cache = VectorCache(redis_host="localhost", ttl=3600)  # 1시간
        >>>
        >>> @cache.cache_search_results
        ... def search(query_vector):
        ...     return client.search(collection_name="products", query_vector=query_vector)

        # 비동기 함수에도 그대로 적용 가능하다
        >>> @cache.cache_search_results
        ... async def async_search(query_vector):
        ...     return await async_client.search(...)
    """

    def __init__(
        self,
        redis_host: Optional[str] = None,
        redis_port: int = None,
        redis_db: int = None,
        redis_password: Optional[str] = None,
        ttl: int = None,
        prefix: str = "vsearch",
    ):
        """
        Args:
            redis_host: Redis 호스트 (기본값: 환경변수 REDIS_HOST)
            redis_port: Redis 포트 (기본값: 환경변수 REDIS_PORT)
            redis_db: Redis DB 번호 (기본값: 환경변수 REDIS_DB)
            redis_password: Redis 비밀번호 (기본값: 환경변수 REDIS_PASSWORD)
            ttl: 캐시 만료 시간 초 (기본값: 환경변수 REDIS_CACHE_TTL)
            prefix: 캐시 키 접두사 (네임스페이스 격리용)
        """
        self.redis_client = Redis(
            host=redis_host or os.getenv("REDIS_HOST", "localhost"),
            port=redis_port or int(os.getenv("REDIS_PORT", "6379")),
            db=redis_db if redis_db is not None else int(os.getenv("REDIS_DB", "0")),
            password=redis_password or os.getenv("REDIS_PASSWORD") or None,
            decode_responses=True,
        )
        self.ttl = ttl or int(os.getenv("REDIS_CACHE_TTL", "3600"))
        self.prefix = prefix

        # 통계
        self.hits = 0
        self.misses = 0

    def _make_key(self, query_vector: List[float], top_k: int = 10) -> str:
        """
        쿼리 벡터로부터 캐시 키 생성

        float32 로 반올림 후 해시 - 미세한 부동소수점 오차로 인한
        캐시 미스를 방지한다.

        Args:
            query_vector: 쿼리 벡터
            top_k: 결과 수 (키에 포함)

        Returns:
            MD5 해시 기반 캐시 키
        """
        rounded = np.round(np.asarray(query_vector), decimals=6).tobytes()
        vector_hash = hashlib.md5(rounded).hexdigest()
        return f"{self.prefix}:{vector_hash}:k{top_k}"

    def get(self, key: str) -> Optional[Any]:
        """캐시 조회"""
        try:
            cached = self.redis_client.get(key)
        except Exception as e:
            logger.warning(f"Redis 조회 실패 (캐시 비활성화로 계속): {e}")
            return None

        if cached is not None:
            self.hits += 1
            logger.info("캐시 HIT")
            return json.loads(cached)

        self.misses += 1
        logger.info("캐시 MISS")
        return None

    def set(self, key: str, value: Any) -> bool:
        """캐시 저장 (TTL 적용)"""
        try:
            self.redis_client.setex(key, self.ttl, json.dumps(value))
            return True
        except Exception as e:
            logger.warning(f"Redis 저장 실패 (캐시 비활성화로 계속): {e}")
            return False

    def invalidate(self, key_prefix: str = None) -> int:
        """
        패턴 매칭으로 캐시 무효화

        Args:
            key_prefix: 무효화할 키 접두사 (None 이면 자신의 네임스페이스 전체)

        Returns:
            삭제된 키 수
        """
        pattern = f"{key_prefix or self.prefix}:*"
        deleted = 0

        for key in self.redis_client.scan_iter(match=pattern):
            self.redis_client.delete(key)
            deleted += 1

        logger.info(f"캐시 {deleted}건 무효화")
        return deleted

    @property
    def hit_rate(self) -> float:
        """캐시 히트율"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def cache_search_results(self, func: Callable) -> Callable:
        """
        검색 결과 캐싱 데코레이터

        첫 번째 인자를 쿼리 벡터로 간주해 캐시 키를 만든다.
        동기/비동기 함수를 모두 지원한다.

        Example:
            @cache.cache_search_results
            def search(query_vector):
                ...
        """

        # 비동기 함수 지원
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(query_vector, *args, **kwargs):
                top_k = kwargs.get("limit", args[1] if len(args) > 1 else 10)
                key = self._make_key(query_vector, top_k=top_k)

                cached = self.get(key)
                if cached is not None:
                    return cached

                result = await func(query_vector, *args, **kwargs)
                self.set(key, [
                    {"id": r.id, "score": r.score} for r in result
                ] if hasattr(result[0] if result else None, "id") else result)
                return result

            return async_wrapper

        # 동기 함수
        @functools.wraps(func)
        def wrapper(query_vector, *args, **kwargs):
            top_k = kwargs.get("limit", args[1] if len(args) > 1 else 10)
            key = self._make_key(query_vector, top_k=top_k)

            cached = self.get(key)
            if cached is not None:
                return cached

            result = func(query_vector, *args, **kwargs)
            self.set(key, [
                {"id": r.id, "score": r.score} for r in result
            ] if hasattr(result[0] if result else None, "id") else result)
            return result

        return wrapper


def main():
    """메인 함수 - 데모 실행"""
    print("=" * 60)
    print("Redis 벡터 검색 캐시 데모")
    print("=" * 60)

    try:
        # 1. Qdrant 및 샘플 컬렉션 준비
        print("\n[1] Qdrant 연결 및 샘플 데이터 준비...")
        client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", "6333")),
        )

        collection_name = "redis_cache_demo"
        rng = np.random.default_rng(42)

        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        vectors = rng.random((1000, 384)).astype(np.float32)
        points = [PointStruct(id=i, vector=vectors[i].tolist()) for i in range(1000)]
        client.upsert(collection_name=collection_name, points=points)
        print("✓ 샘플 데이터 1,000건 적재 완료")

        # 2. 캐시 생성
        print("\n[2] Redis 캐시 생성...")
        cache = VectorCache(ttl=3600)
        cache.redis_client.ping()
        print("✓ Redis 연결 성공")

        # 3. 캐시가 적용된 검색 함수 정의
        @cache.cache_search_results
        def search_with_cache(query_vector, limit=10):
            return client.search(
                collection_name=collection_name,
                query_vector=query_vector.tolist(),
                limit=limit,
            )

        # 4. 동일 쿼리 반복 실행 - 두 번째부터 캐시 HIT
        print("\n[3] 동일 쿼리 3회 실행")
        import time

        for i in range(3):
            start = time.time()
            results = search_with_cache(vectors[0], limit=10)
            elapsed_ms = (time.time() - start) * 1000
            print(f"  [{i + 1}] 결과 {len(results)}건 | "
                  f"{elapsed_ms:.2f}ms | hits={cache.hits}, misses={cache.misses}")

        print(f"\n캐시 히트율: {cache.hit_rate:.1%}")
        print("\n" + "=" * 60)
        print("✓ 데모 완료!")
        print("=" * 60)

    except Exception as e:
        logger.error(f"에러 발생: {e}")
        print(f"\n✗ 실패: {e}")
        print("\n해결 방법:")
        print("1. Qdrant와 Redis가 실행 중인지 확인:")
        print("   $ docker-compose up -d qdrant redis")


if __name__ == "__main__":
    main()
