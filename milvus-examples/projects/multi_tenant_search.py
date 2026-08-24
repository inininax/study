"""
실습 프로젝트: 멀티테넌트 검색 시스템

Level 2 학습 내용을 종합한 실전 프로젝트:
- 파티션 기반 테넌트 격리
- 하이브리드 검색 (벡터 + 스칼라 필터)
- Index 전략 비교 (FLAT vs HNSW)
- 성능 모니터링 (latency 통계 수집)

실행:
    python projects/multi_tenant_search.py --tenants 3 --docs-per-tenant 300
"""

import argparse
import sys
import time
from pathlib import Path
from typing import List, Optional

import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    utility,
)

from utils.connection import get_milvus_client
from utils.decorators import timing_decorator
from utils.logger import get_logger

logger = get_logger(__name__)


class MultiTenantSearchService:
    """파티션 기반 멀티테넌트 검색 서비스."""

    CATEGORIES = ["Electronics", "Books", "Clothing", "Food"]

    def __init__(self, collection_name: str = "multi_tenant_demo", dim: int = 128):
        """
        Args:
            collection_name: 서비스 Collection 이름
            dim: 임베딩 차원
        """
        self.collection_name = collection_name
        self.dim = dim
        self.pool = get_milvus_client()

        # 성능 모니터링용 검색 latency 기록
        self._search_latencies_ms: List[float] = []

    def _generate_random_vectors(self, count: int, seed: Optional[int] = None) -> np.ndarray:
        """L2 정규화된 랜덤 벡터 생성"""
        rng = np.random.default_rng(seed)
        vectors = rng.random((count, self.dim)).astype(np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms

    @timing_decorator
    def setup(self, num_tenants: int = 3, docs_per_tenant: int = 500) -> Collection:
        """
        멀티테넌트 환경 구축

        - 컬렉션 생성 (테넌트/카테고리/가격 스칼라 필드 포함)
        - 테넌트별 파티션 생성 (데이터 격리)
        - HNSW index 구축 후 샘플 데이터 적재

        Args:
            num_tenants: 테넌트 수
            docs_per_tenant: 테넌트당 문서 수
        """
        tenant_ids = [f"tenant_{chr(ord('a') + i)}" for i in range(num_tenants)]

        with self.pool.get_connection_context() as conn:
            # 기존 데모 데이터가 있으면 초기화 (재실행 가능하도록)
            if utility.has_collection(self.collection_name, using=conn.alias):
                utility.drop_collection(self.collection_name, using=conn.alias)

            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="tenant", dtype=DataType.VARCHAR, max_length=64),
                FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=64),
                FieldSchema(name="price", dtype=DataType.FLOAT),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
            ]
            schema = CollectionSchema(
                fields=fields,
                description="Multi-tenant search service",
            )
            collection = Collection(self.collection_name, schema=schema, using=conn.alias)

            collection.create_index(
                field_name="embedding",
                index_params={
                    "index_type": "HNSW",
                    "metric_type": "L2",
                    "params": {"M": 16, "efConstruction": 200},
                },
            )

            # 테넌트별 파티션 생성
            for tenant_id in tenant_ids:
                collection.create_partition(partition_name=tenant_id)

            rng = np.random.default_rng(42)

            # 테넌트별로 자기 파티션에만 데이터 삽입 (컬럼 형식)
            for seed_offset, tenant_id in enumerate(tenant_ids):
                vectors = self._generate_random_vectors(docs_per_tenant, seed=seed_offset)
                data = {
                    "tenant": [tenant_id] * docs_per_tenant,
                    "category": rng.choice(self.CATEGORIES, docs_per_tenant).tolist(),
                    "price": np.round(rng.uniform(10, 1000, docs_per_tenant), 2).tolist(),
                    "embedding": vectors.tolist(),
                }
                collection.insert(data, partition_name=tenant_id)
                logger.info("tenant_data_inserted", tenant=tenant_id, count=docs_per_tenant)

            collection.flush()
            return collection

    @timing_decorator
    def hybrid_search(
        self,
        tenant_id: str,
        query_vector: np.ndarray,
        filter_expr: Optional[str] = None,
        top_k: int = 5,
    ) -> List[dict]:
        """
        하이브리드 검색: 벡터 유사도 + 스칼라 필터 + 파티션 격리

        partition_names 로 테넌트를 격리하고,
        expr 로 카테고리/가격 조건을 필터링한다.

        Args:
            tenant_id: 조회할 테넌트 (파티션 이름)
            query_vector: 쿼리 벡터
            filter_expr: Boolean expression
                예: "category == 'Electronics' and price < 100"
            top_k: 결과 수

        Returns:
            검색 결과 리스트
        """
        start_time = time.time()

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            if not collection.is_loaded:
                collection.load()

            results = collection.search(
                data=[query_vector.tolist()],
                anns_field="embedding",
                param={"metric_type": "L2"},
                limit=top_k,
                partition_names=[tenant_id],
                expr=filter_expr,
                output_fields=["tenant", "category", "price"],
            )

            parsed_results = []
            for hits in results:
                for hit in hits:
                    parsed_results.append({
                        "id": hit.id,
                        "distance": hit.distance,
                        "tenant": hit.entity.get("tenant"),
                        "category": hit.entity.get("category"),
                        "price": hit.entity.get("price"),
                    })

        elapsed_ms = (time.time() - start_time) * 1000
        self._search_latencies_ms.append(elapsed_ms)

        logger.info(
            "hybrid_search_completed",
            tenant=tenant_id,
            expr=filter_expr,
            count=len(parsed_results),
            latency_ms=round(elapsed_ms, 3),
        )
        return parsed_results

    @timing_decorator
    def compare_index_strategies(self, num_queries: int = 10, top_k: int = 5) -> List[dict]:
        """
        Index 전략 비교: FLAT(정확도 기준선) vs HNSW(운영 전략)

        동일 데이터에서 두 index 를 번갈아 구축해 latency 와 recall 을 측정한다.

        Args:
            num_queries: 쿼리 수
            top_k: 결과 수

        Returns:
            index 별 비교 결과
        """
        strategies = [
            ("FLAT", {}),
            ("HNSW", {"M": 16, "efConstruction": 200}),
        ]
        search_param_map = {"FLAT": {}, "HNSW": {"ef": 64}}

        results = []

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)
            if not collection.is_loaded:
                collection.load()

            query_vectors = self._generate_random_vectors(num_queries, seed=2024)

            for index_type, build_params in strategies:
                # Index 교체: release -> drop -> create -> load
                collection.release()
                try:
                    collection.drop_index()
                except Exception:
                    pass

                start_build = time.time()
                collection.create_index(
                    field_name="embedding",
                    index_params={
                        "index_type": index_type,
                        "metric_type": "L2",
                        "params": build_params,
                    },
                )
                build_time = time.time() - start_build
                collection.load()

                latencies = []

                # FLAT 결과를 기준선으로 먼저 확보
                if index_type == "FLAT":
                    baseline_ids = []
                    for qv in query_vectors:
                        hits = collection.search(
                            data=[qv.tolist()],
                            anns_field="embedding",
                            param={"metric_type": "L2"},
                            limit=top_k,
                            partition_names=["tenant_a"],
                        )[0]
                        baseline_ids.append({h.id for h in hits})

                else:
                    recalls = []
                    for i, qv in enumerate(query_vectors):
                        start_time = time.time()
                        param = {"metric_type": "L2"}
                        if search_param_map[index_type]:
                            param["params"] = search_param_map[index_type]

                        hits = collection.search(
                            data=[qv.tolist()],
                            anns_field="embedding",
                            param=param,
                            limit=top_k,
                            partition_names=["tenant_a"],
                        )[0]
                        latencies.append((time.time() - start_time) * 1000)

                        retrieved = {h.id for h in hits}
                        recalls.append(len(retrieved & baseline_ids[i]) / top_k)

                result = {
                    "index_type": index_type,
                    "build_time_seconds": round(build_time, 3),
                    "avg_latency_ms": round(float(np.mean(latencies)), 3) if latencies else None,
                    "recall_vs_flat": round(float(np.mean(recalls)), 4) if recalls else 1.0,
                }
                results.append(result)
                logger.info("strategy_compared", **result)

        return results

    def get_performance_report(self) -> dict:
        """
        누적된 검색 성능 리포트 생성

        Returns:
            요청 수 / 평균 / P95 latency 등의 통계
        """
        latencies = self._search_latencies_ms

        if not latencies:
            return {"total_searches": 0}

        report = {
            "total_searches": len(latencies),
            "avg_latency_ms": round(float(np.mean(latencies)), 3),
            "p95_latency_ms": round(float(np.percentile(latencies, 95)), 3),
            "max_latency_ms": round(float(np.max(latencies)), 3),
        }

        logger.info("performance_report_generated", **report)
        return report


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="Multi-tenant Search Service Demo")
    parser.add_argument("--collection", type=str, default="multi_tenant_demo")
    parser.add_argument("--tenants", type=int, default=3, help="Number of tenants")
    parser.add_argument("--docs-per-tenant", type=int, default=300, help="Docs per tenant")

    args = parser.parse_args()

    service = MultiTenantSearchService(args.collection)

    try:
        print("\n" + "=" * 60)
        print("MULTI-TENANT SEARCH SERVICE DEMO")
        print("=" * 60)

        # 1. 환경 구축
        service.setup(num_tenants=args.tenants, docs_per_tenant=args.docs_per_tenant)
        print(f"\nSetup done: {args.tenants} tenants x {args.docs_per_tenant:,} docs")

        # 2. 테넌트별 격리 확인 - 같은 쿼리로 각 테넌트 검색
        rng = np.random.default_rng(7)
        query_vector = service._generate_random_vectors(1, seed=99)[0]

        for i in range(args.tenants):
            tenant_id = f"tenant_{chr(ord('a') + i)}"
            results = service.hybrid_search(tenant_id, query_vector, top_k=3)
            tenants_seen = {r["tenant"] for r in results}
            print(f"[{tenant_id}] top-3 tenants seen: {tenants_seen}")

        # 3. 하이브리드 검색 (필터 조합)
        print("\nHybrid search: category == 'Electronics' and price < 100")
        results = service.hybrid_search(
            "tenant_a",
            query_vector,
            filter_expr="category == 'Electronics' and price < 100",
            top_k=5,
        )
        for r in results:
            print(f"  {r['category']:<12} ${r['price']:<8} dist={r['distance']:.4f}")

        # 4. Index 전략 비교
        print("\nComparing index strategies...")
        comparison = service.compare_index_strategies(num_queries=10)
        for c in comparison:
            print(f"  {c}")

        # 5. 성능 모니터링 리포트
        report = service.get_performance_report()
        print("\nPerformance report:")
        for key, value in report.items():
            print(f"  {key}: {value}")

        print("\n" + "=" * 60)
        print("DEMO COMPLETED")
        print("=" * 60)
        return 0

    except Exception as e:
        logger.error(
            "multi_tenant_demo_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        print(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
