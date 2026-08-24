"""
집계 쿼리 (Aggregations)
=========================

이 모듈에서 배울 내용:
1. 전체 개수 집계 (total_count)
2. 숫자 속성 통계 (평균, 최대, 최소, 합계)
3. 텍스트 속성 분석 (최빈값 top_occurrences)
4. 그룹화 집계 (Group By)
5. 필터 결합 집계와 메타 분석

난이도: ⭐⭐ (중하)
소요 시간: 45분
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.aggregate import Metrics, GroupByAggregate
from weaviate.classes.query import Filter
from typing import Any, Optional


# ====================
# 0. 버전 호환 헬퍼
# ====================


def get_stat(stats: Any, name: str) -> Optional[Any]:
    """
    집계 결과 속성을 클라이언트 버전에 관계없이 읽는 헬퍼

    참고:
        - weaviate-client v4 버전에 따라 집계 결과 속성 이름이
          mean / mean_ 처럼 trailing underscore가 다를 수 있음
        - 이 헬퍼는 두 가지 이름을 모두 시도한다
    """
    value = getattr(stats, name, None)
    if value is None:
        value = getattr(stats, f"{name}_", None)
    return value


# ====================
# 1. 준비: 샘플 데이터 생성
# ====================


def setup_movie_collection(client: weaviate.WeaviateClient):
    """영화 데이터로 집계 실습"""
    print("🎬 영화 컬렉션 설정...")

    if client.collections.exists("Movie"):
        client.collections.delete("Movie")

    client.collections.create(
        name="Movie",
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="description", data_type=DataType.TEXT),
            Property(name="genre", data_type=DataType.TEXT_ARRAY),
            Property(name="year", data_type=DataType.INT),
            Property(name="rating", data_type=DataType.NUMBER),
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_openai(
            model="text-embedding-3-small"
        ),
    )

    movies = [
        {"title": "인셉션", "genre": ["SF", "액션"], "year": 2010, "rating": 8.8,
         "description": "꿈 속에서 생각을 훔치는 특수 요원의 이야기"},
        {"title": "인터스텔라", "genre": ["SF", "드라마"], "year": 2014, "rating": 8.6,
         "description": "지구를 떠나 새로운 행성을 찾아 떠나는 우주 탐험가들의 여정"},
        {"title": "매트릭스", "genre": ["SF", "액션"], "year": 1999, "rating": 8.7,
         "description": "가상현실에 갇힌 인류를 구하기 위한 선택받은 자의 싸움"},
        {"title": "쇼생크 탈출", "genre": ["드라마"], "year": 1994, "rating": 9.3,
         "description": "무고하게 감옥에 갇힌 은행가가 희망을 잃지 않고 자유를 찾아가는 이야기"},
        {"title": "다크 나이트", "genre": ["액션", "범죄"], "year": 2008, "rating": 9.0,
         "description": "조커와 배트맨의 대결. 정의와 혼돈의 충돌"},
        {"title": "기생충", "genre": ["드라마", "스릴러"], "year": 2019, "rating": 8.6,
         "description": "가난한 가족이 부유한 가정에 들어가며 벌어지는 사건들"},
        {"title": "어벤져스: 엔드게임", "genre": ["액션", "SF"], "year": 2019, "rating": 8.4,
         "description": "타노스에게 빼앗긴 세상을 되찾기 위한 히어로들의 최후 전투"},
        {"title": "월-E", "genre": ["애니메이션", "SF"], "year": 2008, "rating": 8.4,
         "description": "쓰레기로 뒤덮인 지구를 청소하는 로봇의 사랑 이야기"},
    ]

    collection = client.collections.get("Movie")

    with collection.batch.dynamic() as batch:
        for movie in movies:
            batch.add_object(properties=movie)

    print(f"✅ {len(movies)}개의 영화 데이터 추가 완료\n")


# ====================
# 2. 전체 개수 집계
# ====================


def count_all_objects(client: weaviate.WeaviateClient):
    """
    전체 객체 수 집계

    참고:
        - aggregate.over_all(total_count=True): 컬렉션 전체 개수
        - 대량 컬렉션에서 fetch_objects로 셀 필요 없이 서버가 한 번에 계산
    """
    print("\n" + "=" * 60)
    print("전체 개수 집계")
    print("=" * 60)

    collection = client.collections.get("Movie")

    response = collection.aggregate.over_all(total_count=True)

    print(f"\n📊 Movie 전체 객체 수: {response.total_count}개")


# ====================
# 3. 숫자 속성 통계
# ====================


def numeric_statistics(client: weaviate.WeaviateClient):
    """
    숫자(INT/NUMBER) 속성 통계

    참고:
        - Metrics("속성명").number(...)로 NUMBER 타입 메트릭 정의
          (INT 속성은 .integer(...) 사용)
        - count / maximum / minimum / mean / median / sum_ 지원
        - sum_이 underscore인 이유: Python 내장 함수 sum과의 충돌 방지
    """
    print("\n" + "=" * 60)
    print("숫자 속성 통계 (평점)")
    print("=" * 60)

    collection = client.collections.get("Movie")

    response = collection.aggregate.over_all(
        total_count=True,
        return_metrics=[
            Metrics("rating").number(
                count=True, minimum=True, maximum=True, mean=True, median=True, sum_=True
            ),
            Metrics("year").integer(minimum=True, maximum=True),
        ],
    )

    rating_stats = response.properties["rating"]
    year_stats = response.properties["year"]

    print("\n📈 평점(rating) 통계:")
    print(f"   개수:   {get_stat(rating_stats, 'count')}")
    print(f"   최소:   {get_stat(rating_stats, 'minimum')}")
    print(f"   최대:   {get_stat(rating_stats, 'maximum')}")
    print(f"   평균:   {get_stat(rating_stats, 'mean')}")
    print(f"   중간값: {get_stat(rating_stats, 'median')}")
    print(f"   합계:   {get_stat(rating_stats, 'sum')}")

    print("\n📈 연도(year) 통계:")
    print(f"   가장 오래된 영화: {get_stat(year_stats, 'minimum')}")
    print(f"   가장 최신 영화:   {get_stat(year_stats, 'maximum')}")


# ====================
# 4. 텍스트 속성 분석
# ====================


def text_statistics(client: weaviate.WeaviateClient):
    """
    텍스트(TEXT_ARRAY) 속성 분석

    참고:
        - Metrics("속성명").text(...):
          count: 값이 채워진 객체 수
          top_occurrences_value/count: 최빈 값과 빈도
        - 태그/카테고리 분포를 볼 때 유용 (대시보드의 '인기 태그' 위젯!)
    """
    print("\n" + "=" * 60)
    print("텍스트 속성 분석 (장르 분포)")
    print("=" * 60)

    collection = client.collections.get("Movie")

    response = collection.aggregate.over_all(
        return_metrics=[
            Metrics("genre").text(
                count=True,
                top_occurrences_value=True,
                top_occurrences_count=True,
                limit=5,
            ),
        ]
    )

    genre_stats = response.properties["genre"]

    print("\n🏷️ 장르별 출현 빈도 TOP 5:")
    for occ in genre_stats.top_occurrences:
        print(f"   {occ.value}: {occ.count}회")


# ====================
# 5. 그룹화 집계 (Group By)
# ====================


def group_by_aggregation(client: weaviate.WeaviateClient):
    """
    그룹화 집계

    참고:
        - group_by=GroupByAggregate(prop="속성명")
        - SQL의 GROUP BY처럼 그룹별로 total_count와 메트릭 계산
        - 결과는 response.groups 리스트로 반환됨
    """
    print("\n" + "=" * 60)
    print("그룹화 집계: 연도별 영화 수")
    print("=" * 60)

    collection = client.collections.get("Movie")

    response = collection.aggregate.over_all(
        group_by=GroupByAggregate(prop="year"),
        total_count=True,
    )

    # 연도순으로 정렬해서 출력
    groups = sorted(response.groups, key=lambda g: g.grouped_by.value or 0)

    print("\n📊 연도별 영화 수:")
    for group in groups:
        print(f"   {group.grouped_by.value}년: {group.total_count}편")


# ====================
# 6. 필터 결합 집계
# ====================


def filtered_aggregation(client: weaviate.WeaviateClient):
    """
    조건부 집계 (필터 + 집계)

    참고:
        - over_all(filters=...)로 집계 대상 제한 가능
        - "평점 8.7 이상인 영화만" 통계 낼 때 사용
    """
    print("\n" + "=" * 60)
    print("조건부 집계: 고평점 영화만")
    print("=" * 60)

    collection = client.collections.get("Movie")

    high_rated_filter = Filter.by_property("rating").greater_or_equal(8.7)

    response = collection.aggregate.over_all(
        filters=high_rated_filter,
        total_count=True,
        return_metrics=[Metrics("rating").number(mean=True)],
    )

    rating_stats = response.properties.get("rating")

    print("\n🏆 평점 8.7 이상 영화:")
    print(f"   개수: {response.total_count}편")
    if rating_stats is not None:
        print(f"   평균 평점: {get_stat(rating_stats, 'mean')}")


# ====================
# 7. 메타 분석
# ====================


def meta_analysis(client: weaviate.WeaviateClient):
    """
    Weaviate 인스턴스/컬렉션 메타 정보 분석

    참고:
        - client.get_meta(): 서버 버전, 모듈 목록 등 인스턴스 정보
        - collection.config: 컬렉션 설정 조회
        - 운영 대시보드의 '시스템 정보' 화면 구현에 활용
    """
    print("\n" + "=" * 60)
    print("메타 분석 (인스턴스 & 컬렉션)")
    print("=" * 60)

    meta = client.get_meta()
    print("\n🛠️ Weaviate 인스턴스 정보:")
    print(f"   버전: {meta.get('version', 'Unknown')}")
    modules = meta.get("modules", {})
    print(f"   활성 모듈: {', '.join(modules.keys()) if modules else '(없음)'}")

    collection = client.collections.get("Movie")
    config = collection.config.get()

    print("\n📦 Movie 컬렉션 설정:")
    print(f"   설명: {config.description or '(없음)'}")
    print(f"   속성 수: {len(config.properties)}개")
    for prop in config.properties:
        print(f"     - {prop.name} ({prop.data_type})")


# ====================
# 8. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "📊" * 25)
    print("집계 쿼리 (Aggregations) 학습")
    print("📊" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 1. 준비
            setup_movie_collection(client)

            # 2. 전체 개수
            count_all_objects(client)

            # 3. 숫자 통계
            numeric_statistics(client)

            # 4. 텍스트 분석
            text_statistics(client)

            # 5. 그룹화 집계
            group_by_aggregation(client)

            # 6. 필터 결합 집계
            filtered_aggregation(client)

            # 7. 메타 분석
            meta_analysis(client)

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n💡 핵심 정리:")
    print("   - over_all(total_count=True): 전체 개수")
    print('   - Metrics("속성").number/text(...): 통계 메트릭 정의')
    print("   - GroupByAggregate(prop=...): SQL GROUP BY와 유사")
    print("   - filters로 조건부 집계 가능")

    print("\n📚 다음 학습:")
    print("   lessons/03-advanced/01_rag_implementation.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. 집계 API 구조
   - collection.aggregate.over_all(...)
   - total_count: 객체 수
   - return_metrics: 속성별 통계 지정
   - group_by: 그룹화
   - filters: 집계 대상 제한

2. 메트릭 종류
   - number/int: count, min, max, mean, median, sum
   - text: count, top_occurrences(최빈값)
   - boolean: true/false 비율
   - date: count, min, max, median

3. 실전 활용
   - 대시보드: 카테고리 분포, 평균 평점 추이
   - 검색 품질 점검: 필드 채워짐 비율(count)
   - 운영: 인스턴스 버전/모듈 확인

⚠️ 주의사항:
   - TEXT vs TEXT_ARRAY 집계 동작 차이 이해 필요
   - 그룹화 속성의 카디널리티가 높으면(limit 기본 100)
     그룹 수가 잘릴 수 있음 → GroupByAggregate(prop=..., limit=N)

🔧 연습 과제:
   1. 장르 그룹별 평균 평점 집계하기
   2. boolean 속성 추가 후 true 비율 집계해보기
   3. get_meta()로 모듈 목록 출력해보기
"""
