"""
고급 필터링 (Where Filters)
============================

이 모듈에서 배울 내용:
1. 기본 필터: 같다/다르다 조건
2. 범위 필터: 숫자 비교 연산자
3. 배열/문자열 필터: contains_any, like
4. 복합 조건: AND, OR, NOT 조합
5. 벡터 검색 + 필터 결합

난이도: ⭐⭐⭐ (중간)
소요 시간: 1시간
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import Filter, MetadataQuery
from typing import List


# ====================
# 1. 준비: 샘플 데이터 생성
# ====================


def setup_movie_collection(client: weaviate.WeaviateClient):
    """영화 데이터로 필터링 실습"""
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
        {
            "title": "인셉션",
            "description": "꿈 속에서 생각을 훔치는 특수 요원의 이야기. 현실과 꿈의 경계가 모호해지는 SF 스릴러",
            "genre": ["SF", "액션", "스릴러"],
            "year": 2010,
            "rating": 8.8,
        },
        {
            "title": "인터스텔라",
            "description": "지구를 떠나 새로운 행성을 찾아 떠나는 우주 탐험가들의 여정. 시간과 공간을 초월한 감동",
            "genre": ["SF", "드라마"],
            "year": 2014,
            "rating": 8.6,
        },
        {
            "title": "매트릭스",
            "description": "가상현실에 갇힌 인류를 구하기 위한 선택받은 자의 싸움. 혁신적인 액션과 철학적 스토리",
            "genre": ["SF", "액션"],
            "year": 1999,
            "rating": 8.7,
        },
        {
            "title": "쇼생크 탈출",
            "description": "무고하게 감옥에 갇힌 은행가가 희망을 잃지 않고 자유를 찾아가는 감동적인 이야기",
            "genre": ["드라마"],
            "year": 1994,
            "rating": 9.3,
        },
        {
            "title": "다크 나이트",
            "description": "조커와 배트맨의 대결. 정의와 혼돈의 충돌을 그린 슈퍼히어로 영화의 걸작",
            "genre": ["액션", "범죄", "드라마"],
            "year": 2008,
            "rating": 9.0,
        },
        {
            "title": "기생충",
            "description": "가난한 가족이 부유한 가정에 들어가며 벌어지는 예측 불가능한 사건들",
            "genre": ["드라마", "스릴러"],
            "year": 2019,
            "rating": 8.6,
        },
        {
            "title": "어벤져스: 엔드게임",
            "description": "타노스에게 빼앗긴 세상을 되찾기 위한 마블 히어로들의 최후 전투",
            "genre": ["액션", "SF"],
            "year": 2019,
            "rating": 8.4,
        },
        {
            "title": "월-E",
            "description": "쓰레기로 뒤덮인 지구를 청소하는 로봇의 사랑 이야기. 감동적인 애니메이션",
            "genre": ["애니메이션", "SF"],
            "year": 2008,
            "rating": 8.4,
        },
    ]

    collection = client.collections.get("Movie")

    with collection.batch.dynamic() as batch:
        for movie in movies:
            batch.add_object(properties=movie)

    print(f"✅ {len(movies)}개의 영화 데이터 추가 완료\n")


def print_titles(objects: List, prefix: str = "   결과"):
    """검색 결과 제목 출력 헬퍼"""
    if not objects:
        print(f"{prefix}: (없음)")
        return
    titles = [f"{obj.properties['title']}" for obj in objects]
    print(f"{prefix} ({len(objects)}개): {', '.join(titles)}")


# ====================
# 2. 기본 필터 - 같다 / 다르다
# ====================


def basic_equality_filters(client: weaviate.WeaviateClient):
    """
    동등 비교 필터

    참고:
        - Filter.by_property("속성명")으로 필터 시작
        - .equal(): 같음 / .not_equal(): 다름
        - fetch_objects에 filters를 넣으면 SQL의 WHERE 절처럼 동작
    """
    print("\n" + "=" * 60)
    print("기본 필터: equal / not_equal")
    print("=" * 60)

    collection = client.collections.get("Movie")

    # 정확히 일치
    response = collection.query.fetch_objects(
        filters=Filter.by_property("title").equal("인셉션"),
        limit=10,
    )
    print("\n🔍 title == '인셉션'")
    print_titles(response.objects)

    # 일치하지 않음
    response = collection.query.fetch_objects(
        filters=Filter.by_property("genre").not_equal("SF"),
        limit=10,
    )
    print("\n🔍 genre != 'SF' (배열 속성에 특정 값이 없는 객체)")
    print_titles(response.objects)

    # UUID로 필터링: Filter.by_id()
    response = collection.query.fetch_objects(limit=1)
    first_uuid = response.objects[0].uuid
    response = collection.query.fetch_objects(
        filters=Filter.by_id().equal(first_uuid),
        limit=10,
    )
    print(f"\n🔍 id == {str(first_uuid)[:12]}...")
    print_titles(response.objects)


# ====================
# 3. 범위(비교) 필터
# ====================


def range_filters(client: weaviate.WeaviateClient):
    """
    범위 필터 (숫자 비교)

    참고:
        - greater_than (>), greater_or_equal (>=)
        - less_than (<), less_or_equal (<=)
        - INT, NUMBER, DATE 타입에 사용 가능
        - SQL의 WHERE year >= 2008 AND rating >= 8.5 와 동일한 개념
    """
    print("\n" + "=" * 60)
    print("범위 필터: >, >=, <, <=")
    print("=" * 60)

    collection = client.collections.get("Movie")

    # 2010년 이후
    response = collection.query.fetch_objects(
        filters=Filter.by_property("year").greater_than(2010),
        limit=10,
    )
    print("\n🔍 year > 2010")
    print_titles(response.objects)

    # 평점 8.7 이상
    response = collection.query.fetch_objects(
        filters=Filter.by_property("rating").greater_or_equal(8.7),
        limit=10,
    )
    print("\n🔍 rating >= 8.7")
    print_titles(response.objects)

    # 구간 검색: 1995 ~ 2012년 사이
    between_filter = Filter.by_property("year").greater_or_equal(1995) & (
        Filter.by_property("year").less_than(2013)
    )
    response = collection.query.fetch_objects(filters=between_filter, limit=10)
    print("\n🔍 1995 <= year < 2013")
    print_titles(response.objects)


# ====================
# 4. 배열 & 문자열 패턴 필터
# ====================


def array_and_pattern_filters(client: weaviate.WeaviateClient):
    """
    배열 필터와 문자열 패턴 필터

    참고:
        - TEXT_ARRAY에 .equal() → 배열 안에 값이 포함되면 매칭
        - .contains_any([...]): 여러 값 중 하나라도 포함
        - .like(): 와일드카드 패턴 (*: 임의 문자열, ?: 한 글자)
    """
    print("\n" + "=" * 60)
    print("배열 & 패턴 필터")
    print("=" * 60)

    collection = client.collections.get("Movie")

    # 배열에 '애니메이션' 포함
    response = collection.query.fetch_objects(
        filters=Filter.by_property("genre").equal("애니메이션"),
        limit=10,
    )
    print("\n🔍 genre에 '애니메이션' 포함")
    print_titles(response.objects)

    # SF 또는 범죄 장르 포함
    response = collection.query.fetch_objects(
        filters=Filter.by_property("genre").contains_any(["SF", "범죄"]),
        limit=10,
    )
    print("\n🔍 genre에 'SF' 또는 '범죄' 포함")
    print_titles(response.objects)

    # like 패턴: 제목이 '인'으로 시작
    response = collection.query.fetch_objects(
        filters=Filter.by_property("title").like("인*"),
        limit=10,
    )
    print("\n🔍 title LIKE '인*'")
    print_titles(response.objects)

    # like 패턴: 설명에 '감동' 포함
    response = collection.query.fetch_objects(
        filters=Filter.by_property("description").like("*감동*"),
        limit=10,
    )
    print("\n🔍 description LIKE '*감동*'")
    print_titles(response.objects)


# ====================
# 5. 복합 조건: AND / OR / NOT
# ====================


def compound_filters(client: weaviate.WeaviateClient):
    """
    복합 필터 조합

    참고:
        - &: AND / |: OR / ~: NOT (Python 비트 연산자 오버로딩)
        - Filter.all_of([...]): AND 목록 버전
        - Filter.any_of([...]): OR 목록 버전
        - 괄호로 묶어 원하는 대로 중첩 가능
    """
    print("\n" + "=" * 60)
    print("복합 조건: AND / OR / NOT")
    print("=" * 60)

    collection = client.collections.get("Movie")

    # AND: SF 장르 + 2008년 이후
    and_filter = Filter.by_property("genre").equal("SF") & (
        Filter.by_property("year").greater_or_equal(2008)
    )
    response = collection.query.fetch_objects(filters=and_filter, limit=10)
    print("\n🔍 genre='SF' AND year>=2008")
    print_titles(response.objects)

    # OR: 평점 9.0 이상 또는 애니메이션
    or_filter = Filter.by_property("rating").greater_or_equal(9.0) | (
        Filter.by_property("genre").equal("애니메이션")
    )
    response = collection.query.fetch_objects(filters=or_filter, limit=10)
    print("\n🔍 rating>=9.0 OR genre='애니메이션'")
    print_titles(response.objects)

    # NOT: 드라마 장르가 아닌 것
    not_filter = ~Filter.by_property("genre").equal("드라마")
    response = collection.query.fetch_objects(filters=not_filter, limit=10)
    print("\n🔍 NOT (genre='드라마')")
    print_titles(response.objects)

    # 중첩: (SF OR 액션) AND 평점 8.7 이상
    # any_of는 Filter 클래스의 클래스 메서드 (OR 목록)
    nested_filter = Filter.any_of(
        [
            Filter.by_property("genre").equal("SF"),
            Filter.by_property("genre").equal("액션"),
        ]
    ) & Filter.by_property("rating").greater_or_equal(8.7)

    response = collection.query.fetch_objects(filters=nested_filter, limit=10)
    print("\n🔍 (genre='SF' OR genre='액션') AND rating>=8.7")
    print_titles(response.objects)


# ====================
# 6. 벡터 검색 + 필터 결합
# ====================


def semantic_search_with_filters(client: weaviate.WeaviateClient):
    """
    의미 검색과 필터 결합 (실무에서 가장 많이 쓰는 패턴!)

    참고:
        - near_text에 filters를 전달하면
          "조건을 만족하는 객체들 안에서만" 의미 검색 수행
        - 예: "우주 영화 추천해줘" + "사용자가 좋아하는 장르만"
    """
    print("\n" + "=" * 60)
    print("벡터 검색 + 필터 결합")
    print("=" * 60)

    collection = client.collections.get("Movie")

    query = "우주를 배경으로 한 감동적인 이야기"

    # 필터 없이 의미 검색
    response = collection.query.near_text(query=query, limit=3)
    print(f"\n🔍 '{query}' (필터 없음)")
    print_titles(response.objects, prefix="   결과")

    # 2008년 이후 영화로 제한한 의미 검색
    filtered_response = collection.query.near_text(
        query=query,
        limit=3,
        filters=Filter.by_property("year").greater_or_equal(2008),
        return_metadata=MetadataQuery(distance=True),
    )
    print(f"\n🔍 '{query}' + year >= 2008")
    for i, obj in enumerate(filtered_response.objects, 1):
        dist = obj.metadata.distance if obj.metadata else None
        print(f"   {i}. {obj.properties['title']} (거리: {dist:.4f})")

    print("\n💡 필터가 의미 검색의 후보군을 좁혀준다!")
    print("   → RAG 시스템에서 권한/카테고리별 검색 분리에 필수")


# ====================
# 7. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "🔎" * 25)
    print("고급 필터링 (Where Filters) 학습")
    print("🔎" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 1. 준비
            setup_movie_collection(client)

            # 2. 기본 필터
            basic_equality_filters(client)

            # 3. 범위 필터
            range_filters(client)

            # 4. 배열 & 패턴 필터
            array_and_pattern_filters(client)

            # 5. 복합 조건
            compound_filters(client)

            # 6. 벡터 검색 + 필터
            semantic_search_with_filters(client)

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n💡 핵심 정리:")
    print("   - Filter.by_property(): 필터의 시작점")
    print("   - equal/not_equal/greater_than/less_than 등 비교 연산")
    print("   - & | ~ 로 AND/OR/NOT 조합, 괄호로 우선순위 제어")
    print("   - near_text/hybrid + filters = 실무 필수 조합")

    print("\n📚 다음 학습:")
    print("   python 04_aggregations.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. 필터 연산자
   - equal / not_equal: 동등 비교
   - greater_than / greater_or_equal: 초과 / 이상
   - less_than / less_or_equal: 미만 / 이하
   - contains_any / contains_all / contains_none: 배열 포함
   - like: 와일드카드 패턴 (*, ?)

2. 조합 방법
   - f1 & f2: AND
   - f1 | f2: OR
   - ~f1: NOT
   - Filter.all_of([...]) / Filter.any_of([...])

3. 활용 위치
   - fetch_objects(filters=...): 단순 조회
   - near_text/near_vector/hybrid/bm25(filters=...): 검색 제한
   - aggregate(filters=...): 조건부 집계

💡 성능 팁:
   - 필터 대상 속성은 자동으로 인덱싱됨 (index_filterable)
   - like '*단어*'처럼 앞쪽 와일드카드는 느릴 수 있음
   - 벡터 검색 + 필터는 Weaviate가 효율적으로 처리함

⚠️ 주의사항:
   - DATE 비교 시 ISO 8601 형식 문자열 필요 ("2024-01-01T00:00:00Z")
   - TEXT_ARRAY에 equal()은 '포함' 의미 (전체 일치가 아님)

🔧 연습 과제:
   1. 자신만의 데이터로 3중 중첩 필터 작성
   2. contains_all vs contains_any 차이 확인
   3. 하이브리드 검색 + 필터 조합 실습 (02_hybrid_search.py 참고)
"""
