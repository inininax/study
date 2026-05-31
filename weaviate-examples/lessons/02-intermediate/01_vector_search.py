"""
벡터 검색 (Semantic Search)
============================

이 모듈에서 배울 내용:
1. Near Text: 텍스트 기반 유사도 검색
2. Near Vector: 벡터 직접 사용
3. Near Object: 기존 객체와 유사한 객체 찾기
4. 검색 결과 평가 및 튜닝

난이도: ⭐⭐⭐ (중간)
소요 시간: 1.5시간
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
from typing import List, Dict, Any


# ====================
# 1. 준비: 샘플 데이터 생성
# ====================


def setup_movie_collection(client: weaviate.WeaviateClient):
    """영화 데이터로 벡터 검색 실습"""
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

    # 샘플 영화 데이터
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

    # 배치 삽입
    with collection.batch.dynamic() as batch:
        for movie in movies:
            batch.add_object(properties=movie)

    print(f"✅ {len(movies)}개의 영화 데이터 추가 완료\n")


# ====================
# 2. Near Text - 텍스트 기반 검색
# ====================


def search_near_text_basic(client: weaviate.WeaviateClient, query: str, limit: int = 3):
    """
    기본 텍스트 검색

    Args:
        query: 검색 쿼리
        limit: 결과 개수

    참고:
        - 쿼리 텍스트와 의미상 유사한 영화를 찾음
        - 정확한 키워드가 없어도 됨!
    """
    print(f"\n🔍 검색: '{query}'")
    print("=" * 60)

    collection = client.collections.get("Movie")

    # Near Text 검색
    response = collection.query.near_text(
        query=query,
        limit=limit,
        return_metadata=MetadataQuery(distance=True, certainty=True),
    )

    for i, movie in enumerate(response.objects, 1):
        props = movie.properties
        print(f"\n{i}. {props['title']} ({props['year']})")
        print(f"   장르: {', '.join(props['genre'])}")
        print(f"   줄거리: {props['description'][:80]}...")
        print(f"   평점: ⭐ {props['rating']}")

        # 메타데이터 (유사도 정보)
        if movie.metadata:
            # distance: 낮을수록 유사 (0에 가까울수록 완벽히 같음)
            # certainty: 높을수록 유사 (1에 가까울수록 완벽히 같음)
            print(f"   거리: {movie.metadata.distance:.4f}")
            print(f"   확신도: {movie.metadata.certainty:.4f}")


def search_near_text_advanced(client: weaviate.WeaviateClient):
    """
    다양한 검색 쿼리 예제

    참고:
        - 의미론적 검색의 힘을 체험!
        - 정확한 단어가 없어도 의미만 맞으면 찾아냄
    """
    print("\n" + "=" * 60)
    print("고급 벡터 검색 예제")
    print("=" * 60)

    # 예제 1: 감정/분위기로 검색
    search_near_text_basic(client, "희망과 자유에 대한 감동적인 이야기", limit=3)

    # 예제 2: 개념으로 검색
    search_near_text_basic(client, "우주를 배경으로 한 장대한 모험", limit=3)

    # 예제 3: 스타일로 검색
    search_near_text_basic(client, "철학적이고 생각할 거리가 많은 영화", limit=3)

    # 예제 4: 추상적 개념
    search_near_text_basic(client, "현실과 가상의 경계", limit=2)


# ====================
# 3. Near Vector - 벡터 직접 사용
# ====================


def search_near_vector(client: weaviate.WeaviateClient):
    """
    벡터를 직접 사용한 검색

    참고:
        - 텍스트를 벡터로 변환 후 검색
        - 더 세밀한 제어 가능
    """
    print("\n" + "=" * 60)
    print("벡터 직접 사용 검색")
    print("=" * 60)

    # OpenAI로 쿼리를 벡터로 변환
    from openai import OpenAI
    import os

    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    query_text = "로봇과 인공지능"
    response = openai_client.embeddings.create(
        model="text-embedding-3-small", input=query_text
    )
    query_vector = response.data[0].embedding

    print(f"검색: '{query_text}'")
    print(f"벡터 차원: {len(query_vector)}")

    # Near Vector 검색
    collection = client.collections.get("Movie")
    results = collection.query.near_vector(
        near_vector=query_vector,
        limit=3,
        return_metadata=MetadataQuery(distance=True),
    )

    print("\n검색 결과:")
    for i, movie in enumerate(results.objects, 1):
        props = movie.properties
        print(f"{i}. {props['title']} (거리: {movie.metadata.distance:.4f})")


# ====================
# 4. Near Object - 유사 객체 찾기
# ====================


def search_near_object(client: weaviate.WeaviateClient):
    """
    특정 영화와 유사한 영화 찾기

    참고:
        - "인셉션을 좋아한다면 이런 영화도..." 기능
        - 추천 시스템의 기초
    """
    print("\n" + "=" * 60)
    print("유사 영화 추천")
    print("=" * 60)

    collection = client.collections.get("Movie")

    # 먼저 "인셉션" 찾기
    inception = collection.query.fetch_objects(limit=100)
    inception_uuid = None

    for obj in inception.objects:
        if obj.properties["title"] == "인셉션":
            inception_uuid = obj.uuid
            break

    if not inception_uuid:
        print("❌ 인셉션을 찾을 수 없습니다")
        return

    print("📌 기준 영화: 인셉션")
    print("\n유사한 영화 추천:")

    # Near Object 검색
    results = collection.query.near_object(
        near_object=inception_uuid,
        limit=4,  # 자기 자신 포함되므로 4개 요청
        return_metadata=MetadataQuery(distance=True),
    )

    for i, movie in enumerate(results.objects):
        props = movie.properties
        # 자기 자신 제외
        if props["title"] == "인셉션":
            continue

        print(f"\n{i}. {props['title']} ({props['year']})")
        print(f"   장르: {', '.join(props['genre'])}")
        print(f"   유사도: {movie.metadata.distance:.4f}")


# ====================
# 5. 검색 결과 평가
# ====================


def evaluate_search_results(client: weaviate.WeaviateClient):
    """
    검색 결과의 품질 평가

    참고:
        - distance와 certainty 이해
        - 검색 품질 측정
    """
    print("\n" + "=" * 60)
    print("검색 결과 품질 평가")
    print("=" * 60)

    collection = client.collections.get("Movie")

    # 여러 쿼리로 테스트
    test_queries = [
        "우주 탐험",  # 명확한 쿼리
        "복잡한 스토리",  # 모호한 쿼리
        "감동적인",  # 추상적 쿼리
    ]

    for query in test_queries:
        print(f"\n🔍 쿼리: '{query}'")

        results = collection.query.near_text(
            query=query, limit=3, return_metadata=MetadataQuery(distance=True)
        )

        distances = [obj.metadata.distance for obj in results.objects]

        print(f"   평균 거리: {sum(distances) / len(distances):.4f}")
        print(f"   최소 거리: {min(distances):.4f}")
        print(f"   최대 거리: {max(distances):.4f}")

        # 거리 해석
        avg_dist = sum(distances) / len(distances)
        if avg_dist < 0.2:
            print("   ✅ 매우 관련성 높음")
        elif avg_dist < 0.4:
            print("   ✓ 관련성 있음")
        else:
            print("   ⚠️ 관련성 낮음 (쿼리 개선 필요)")


# ====================
# 6. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "🎬" * 25)
    print("벡터 검색 (Semantic Search) 학습")
    print("🎬" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 1. 준비
            setup_movie_collection(client)

            # 2. 기본 텍스트 검색
            print("\n" + "=" * 60)
            print("1️⃣ 기본 Near Text 검색")
            print("=" * 60)
            search_near_text_basic(client, "우주를 배경으로 한 SF 영화", limit=3)

            # 3. 고급 검색
            search_near_text_advanced(client)

            # 4. 벡터 직접 사용
            search_near_vector(client)

            # 5. 유사 객체 찾기
            search_near_object(client)

            # 6. 검색 품질 평가
            evaluate_search_results(client)

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n💡 핵심 정리:")
    print("   - Near Text: 텍스트로 의미 검색")
    print("   - Near Vector: 벡터로 직접 검색")
    print("   - Near Object: 유사 객체 찾기")
    print("   - Distance: 낮을수록 유사")

    print("\n📚 다음 학습:")
    print("   python 02_hybrid_search.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. 벡터 검색 유형
   - Near Text: 자연어 쿼리
   - Near Vector: 직접 벡터 제공
   - Near Object: 기존 객체 기준

2. 유사도 메트릭
   - Distance: 벡터 간 거리 (낮을수록 유사)
   - Certainty: 확신도 (높을수록 유사)
   - Cosine, Euclidean, Dot 등

3. 실전 활용
   - 추천 시스템
   - 유사 문서 찾기
   - 의미 기반 검색

💡 벡터 검색의 힘:
   - 정확한 키워드 없이도 의미만으로 검색
   - "우주 탐험" → "인터스텔라" 찾기
   - 동의어, 유사 개념 자동 처리

⚠️ 주의사항:
   - 벡터화 품질이 검색 품질 결정
   - 적절한 임베딩 모델 선택 중요
   - Distance threshold 조정 필요

🔧 연습 과제:
   1. 자신만의 데이터로 검색 실험
   2. 다양한 쿼리로 결과 비교
   3. Distance 값 분석
"""
