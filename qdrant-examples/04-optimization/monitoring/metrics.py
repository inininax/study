"""
Prometheus 메트릭 수집

Qdrant 애플리케이션의 검색/업서트/캐시 지표를 Prometheus 형식으로 수집한다.
Grafana 대시보드(../monitoring/grafana/)와 연동해 시각화할 수 있다.

실행:
    python monitoring/metrics.py
    # 메트릭 엔드포인트: http://localhost:8001/metrics
"""

import os
import time
import random
import logging

from dotenv import load_dotenv
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    start_http_server,
)

# 환경 변수 로드
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Qdrant 애플리케이션 메트릭 컬렉터

    Features:
    - 검색 요청 수/지연 시간 히스토그램
    - 결과 개수 분포
    - 캐시 히트율
    - 컬렉션 포인트 수 게이지

    Example:
        >>> metrics = setup_metrics()
        >>>
        >>> with metrics.search_duration.time():
        ...     results = search(query)
        >>>
        >>> metrics.search_total.inc()
        >>> metrics.results_count.observe(len(results))
    """

    def __init__(self, namespace: str = None, port: int = None):
        """
        Args:
            namespace: 메트릭 네임스페이스 (기본값: 환경변수 METRICS_NAMESPACE)
            port: 메트릭 서버 포트 (기본값: 환경변수 PROMETHEUS_PORT)
        """
        self.namespace = namespace or os.getenv("METRICS_NAMESPACE", "qdrant_app")
        self.port = port or int(os.getenv("PROMETHEUS_PORT", "8001"))

        # 카운터: 누적 발생 건수
        self.search_total = Counter(
            "search_total",
            "총 검색 요청 수",
            namespace=self.namespace,
        )
        self.search_errors_total = Counter(
            "search_errors_total",
            "검색 실패 수",
            namespace=self.namespace,
        )
        self.upsert_total = Counter(
            "upsert_total",
            "총 업서트 배치 수",
            namespace=self.namespace,
        )

        # 캐시 히트/미스 - 히트율은 두 카운터의 비율로 계산한다
        self.cache_hits = Counter(
            "cache_hits_total",
            "캐시 히트 수",
            namespace=self.namespace,
        )
        self.cache_misses = Counter(
            "cache_misses_total",
            "캐시 미스 수",
            namespace=self.namespace,
        )

        # 히스토그램: 값의 분포 (버킷별 카운트 -> P50/P95/P99 계산 가능)
        self.search_duration = Histogram(
            "search_duration_seconds",
            "검색 소요 시간(초)",
            buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0),
            namespace=self.namespace,
        )
        self.results_count = Histogram(
            "search_results_count",
            "검색 결과 개수 분포",
            buckets=(1, 5, 10, 20, 50, 100),
            namespace=self.namespace,
        )

        # 게이지: 현재 시점의 값
        self.collection_points = Gauge(
            "collection_points",
            "컬렉션 내 포인트 수",
            ["collection"],
            namespace=self.namespace,
        )
        self.active_connections = Gauge(
            "active_connections",
            "현재 활성 커넥션 수",
            namespace=self.namespace,
        )

        logger.info(f"메트릭 초기화 완료 (namespace={self.namespace})")

    @property
    def hit_rate(self) -> float:
        """현재까지의 캐시 히트율"""
        hits = self.cache_hits._value.get()
        misses = self.cache_misses._value.get()
        total = hits + misses
        return hits / total if total > 0 else 0.0

    def observe_search(self, duration_seconds: float, result_count: int):
        """
        한 번의 검색을 기록하는 편의 메서드

        Args:
            duration_seconds: 소요 시간(초)
            result_count: 결과 개수
        """
        self.search_duration.observe(duration_seconds)
        self.results_count.observe(result_count)
        self.search_total.inc()


def setup_metrics(
    start_server: bool = True,
    namespace: str = None,
    port: int = None,
) -> MetricsCollector:
    """
    메트릭 설정 및 컬렉터 반환

    Args:
        start_server: /metrics HTTP 서버 시작 여부
        namespace: 메트릭 네임스페이스
        port: 메트릭 서버 포트

    Returns:
        MetricsCollector 인스턴스

    Example:
        >>> metrics = setup_metrics()
        >>> with metrics.search_duration.time():
        ...     results = await search(query)
        >>> metrics.results_count.observe(len(results))
    """
    collector = MetricsCollector(namespace=namespace, port=port)

    if start_server and os.getenv("PROMETHEUS_ENABLED", "true").lower() == "true":
        start_http_server(collector.port)
        logger.info(f"메트릭 서버 시작: http://localhost:{collector.port}/metrics")

    return collector


def main():
    """메인 함수 - 메트릭 수집 데모"""
    print("=" * 60)
    print("Prometheus 메트릭 데모")
    print("=" * 60)

    try:
        # 1. 메트릭 서버 시작
        metrics = setup_metrics(start_server=True)
        print(f"✓ 메트릭 서버 시작: http://localhost:{metrics.port}/metrics\n")

        # 2. 가상의 검색 트래픽 발생
        print("가상 검색 트래픽 생성 중... (Ctrl+C 로 종료)")
        for i in range(30):
            # 가상의 지연 시간과 결과 수 생성
            fake_latency = random.uniform(0.002, 0.08)
            fake_results = random.randint(1, 50)

            metrics.search_duration.observe(fake_latency)
            metrics.results_count.observe(fake_results)
            metrics.search_total.inc()

            # 10% 확률로 캐시 히트/미스 기록
            if random.random() < 0.7:
                metrics.cache_hits.inc()
            else:
                metrics.cache_misses.inc()

            # 게이지 갱신 흉내
            metrics.collection_points.labels(collection="demo").set(10_000 + i * 100)

            if (i + 1) % 10 == 0:
                print(f"  {i + 1}회 처리 | 히트율: {metrics.hit_rate:.1%}")

            time.sleep(0.2)

        print("\n✓ 데모 완료! 브라우저에서 확인:")
        print(f"   http://localhost:{metrics.port}/metrics")

    except KeyboardInterrupt:
        print("\n사용자 중지")
    except Exception as e:
        logger.error(f"에러 발생: {e}")
        print(f"\n✗ 실패: {e}")


if __name__ == "__main__":
    main()
