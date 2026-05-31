"""
고급 필터 쿼리 빌더

복잡한 필터 조건을 쉽게 구성하기 위한 빌더 패턴
"""

from typing import List, Dict, Any, Optional, Union
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    MatchAny,
    Range
)
import logging

logger = logging.getLogger(__name__)


class FilterBuilder:
    """
    필터 쿼리 빌더

    Fluent API 스타일로 복잡한 필터 조건을 쉽게 구성

    Example:
        >>> filter_query = FilterBuilder() \\
        ...     .must("category", "AI") \\
        ...     .must_not("status", "draft") \\
        ...     .should("year", [2023, 2024]) \\
        ...     .range("rating", gte=4.0) \\
        ...     .build()
    """

    def __init__(self):
        self._must: List[FieldCondition] = []
        self._must_not: List[FieldCondition] = []
        self._should: List[FieldCondition] = []

    def must(self, key: str, value: Any) -> 'FilterBuilder':
        """
        반드시 만족해야 하는 조건 (AND)

        Args:
            key: 필드명
            value: 값

        Returns:
            FilterBuilder (체이닝용)
        """
        condition = FieldCondition(
            key=key,
            match=MatchValue(value=value)
        )
        self._must.append(condition)
        return self

    def must_not(self, key: str, value: Any) -> 'FilterBuilder':
        """
        만족하지 않아야 하는 조건 (NOT)

        Args:
            key: 필드명
            value: 값

        Returns:
            FilterBuilder
        """
        condition = FieldCondition(
            key=key,
            match=MatchValue(value=value)
        )
        self._must_not.append(condition)
        return self

    def should(self, key: str, values: List[Any]) -> 'FilterBuilder':
        """
        하나 이상 만족하면 되는 조건 (OR)

        Args:
            key: 필드명
            values: 값 리스트

        Returns:
            FilterBuilder
        """
        condition = FieldCondition(
            key=key,
            match=MatchAny(any=values)
        )
        self._should.append(condition)
        return self

    def range(
        self,
        key: str,
        gt: Optional[float] = None,
        gte: Optional[float] = None,
        lt: Optional[float] = None,
        lte: Optional[float] = None
    ) -> 'FilterBuilder':
        """
        범위 조건

        Args:
            key: 필드명
            gt: 초과 (greater than)
            gte: 이상 (greater than or equal)
            lt: 미만 (less than)
            lte: 이하 (less than or equal)

        Returns:
            FilterBuilder

        Example:
            >>> .range("price", gte=10000, lte=50000)  # 10,000 ~ 50,000
        """
        condition = FieldCondition(
            key=key,
            range=Range(
                gt=gt,
                gte=gte,
                lt=lt,
                lte=lte
            )
        )
        self._must.append(condition)
        return self

    def build(self) -> Filter:
        """
        필터 객체 생성

        Returns:
            Qdrant Filter 객체
        """
        return Filter(
            must=self._must if self._must else None,
            must_not=self._must_not if self._must_not else None,
            should=self._should if self._should else None
        )

    def reset(self) -> 'FilterBuilder':
        """필터 초기화"""
        self._must = []
        self._must_not = []
        self._should = []
        return self


# 편의 함수들
def create_category_filter(categories: List[str]) -> Filter:
    """카테고리 필터 생성"""
    return FilterBuilder().should("category", categories).build()


def create_date_range_filter(
    start_date: str,
    end_date: str,
    date_field: str = "created_at"
) -> Filter:
    """날짜 범위 필터 생성"""
    return FilterBuilder().range(
        date_field,
        gte=start_date,
        lte=end_date
    ).build()


def create_rating_filter(min_rating: float = 4.0) -> Filter:
    """최소 평점 필터 생성"""
    return FilterBuilder().range("rating", gte=min_rating).build()
