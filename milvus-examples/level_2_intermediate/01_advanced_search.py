"""
Level 2-1: Advanced Search

고급 검색 기능:
- Hybrid Search (Vector + Scalar Filtering)
- Range Search
- Boolean Expressions
- Result Re-ranking

Production-ready 하이브리드 검색 구현 패턴을 학습합니다.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from pymilvus import Collection

from config.settings import settings
from utils.connection import get_milvus_client
from utils.decorators import timing_decorator
from utils.logger import get_logger

logger = get_logger(__name__)


class AdvancedSearcher:
    """Advanced search functionality manager."""

    def __init__(self, collection_name: str = "demo_advanced"):
        self.collection_name = collection_name
        self.pool = get_milvus_client()

    @timing_decorator
    def hybrid_search(
        self,
        query_vector: np.ndarray,
        filters: str,
        top_k: int = 10,
    ):
        """
        Hybrid Search: Vector + Scalar Filtering

        Args:
            query_vector: 쿼리 벡터
            filters: Boolean expression (예: "price > 100 and category == 'Electronics'")
            top_k: 결과 수

        Example:
            filters = "price > 100.0 and stock > 10"
            filters = "category in ['Electronics', 'Books']"
            filters = "price between 50.0 and 200.0"
        """
        logger.info(
            "performing_hybrid_search",
            collection=self.collection_name,
            filters=filters,
            top_k=top_k,
        )

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            if not collection.is_loaded:
                collection.load()

            # Hybrid search with filtering
            results = collection.search(
                data=[query_vector.tolist()],
                anns_field="embedding",
                param={"metric_type": "L2"},
                limit=top_k,
                expr=filters,  # Boolean expression for filtering
                output_fields=["title", "category", "price", "stock"],
            )

            # 결과 파싱
            parsed_results = []
            for hits in results:
                for hit in hits:
                    parsed_results.append({
                        "id": hit.id,
                        "distance": hit.distance,
                        "title": hit.entity.get("title"),
                        "category": hit.entity.get("category"),
                        "price": hit.entity.get("price"),
                        "stock": hit.entity.get("stock"),
                    })

            logger.info("hybrid_search_completed", count=len(parsed_results))
            return parsed_results

    @timing_decorator
    def range_search(
        self,
        query_vector: np.ndarray,
        radius: float,
        range_filter: float = None,
    ):
        """
        Range Search: 특정 거리 범위 내의 결과 검색

        Args:
            query_vector: 쿼리 벡터
            radius: 검색 반경
            range_filter: 최소 거리 (optional)
        """
        logger.info(
            "performing_range_search",
            radius=radius,
            range_filter=range_filter,
        )

        with self.pool.get_connection_context() as conn:
            collection = Collection(self.collection_name, using=conn.alias)

            if not collection.is_loaded:
                collection.load()

            search_params = {
                "metric_type": "L2",
                "params": {"radius": radius}
            }

            if range_filter is not None:
                search_params["params"]["range_filter"] = range_filter

            results = collection.search(
                data=[query_vector.tolist()],
                anns_field="embedding",
                param=search_params,
                limit=1000,  # 최대 결과 수
                output_fields=["title", "price"],
            )

            parsed_results = []
            for hits in results:
                for hit in hits:
                    parsed_results.append({
                        "id": hit.id,
                        "distance": hit.distance,
                        "title": hit.entity.get("title"),
                    })

            logger.info("range_search_completed", count=len(parsed_results))
            return parsed_results


def main():
    """Example usage"""
    print("Advanced Search Examples")
    print("See source code for implementation details")


if __name__ == "__main__":
    main()
