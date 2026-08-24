"""
하이브리드 검색 (Hybrid Search)
================================

이 모듈에서 배울 내용:
1. BM25: 전통적인 키워드(BM25) 검색
2. 하이브리드 검색: 벡터 + 키워드 결합
3. 알파(alpha) 파라미터: 벡터/키워드 비중 조절
4. 퓨전(Fusion) 방식과 실전 튜닝 팁

난이도: ⭐⭐⭐ (중간)
소요 시간: 1시간
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery, HybridFusion
from typing import Dict, List


# ====================
# 1. 준비: 샘플 데이터 생성
# ====================


def setup_movie_collection(client: weaviate.WeaviateClient):
    """영화 데이터로 하이브리드 검색 실습 (01_vector_search.py와 동일한 데이터)"""
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


def print_results(objects: List, show_score: bool = True):
    """검색 결과 출력 헬퍼"""
    for i, obj in enumerate(objects, 1):
        props = obj.properties
        line = f"{i}. {props['title']} ({props['year']})"
        if show_score and obj.metadata and obj.metadata.score is not None:
            line += f" | score: {obj.metadata.score:.4f}"
        print(f"   {line}")


# ====================
# 2. BM25 - 키워드 검색
# ====================


def search_bm25(client: weaviate.WeaviateClient):
    """
    BM25 키워드 검색

    참고:
        - BM25: TF-IDF를 개량한 랭킹 알고리즘 (Elasticsearch 등에서도 사용)
        - 정확한 키워드가 있을 때 강력하지만, 동의어는 못 찾음
        - query_properties로 검색 대상 속성을 좁힐 수 있음
    """
    print("\n" + "=" * 60)
    print("BM25 키워드 검색")
    print("=" * 60)

    collection = client.collections.get("Movie")

    # 쿼리에 포함된 단어가 '문서에 그대로' 있어야 매칭됨
    response = collection.query.bm25(
        query="우주 행성",
        query_properties=["description"],  # description에서만 검색
        limit=3,
        return_metadata=MetadataQuery(score=True),
    )

    print("\n🔍 BM25 검색: '우주 행성'")
    print_results(response.objects)

    # 벡터 검색이라면 "우주 탐험" 같은 의미적 확장도 가능하지만,
    # BM25는 '우주', '행성' 단어가 실제로 들어간 문서만 찾는다!
    response = collection.query.bm25(
        query="감옥 희망",
        limit=3,
        return_metadata=MetadataQuery(score=True),
    )

    print("\n🔍 BM25 검색: '감옥 희망'")
    print_results(response.objects)


# ====================
# 3. 하이브리드 검색 기본
# ====================


def search_hybrid_basic(client: weaviate.WeaviateClient):
    """
    하이브리드 검색 기본

    참고:
        - BM25(키워드) + 벡터(의미) 결과를 융합해서 랭킹
        - alpha=0.5 (기본값): 두 방식의 균형
        - 키워드의 정확함 + 의미 검색의 유연함을 동시에 얻음
    """
    print("\n" + "=" * 60)
    print("하이브리드 검색 기본 (alpha=0.5)")
    print("=" * 60)

    collection = client.collections.get("Movie")

    response = collection.query.hybrid(
        query="로봇이 나오는 감동적인 영화",
        alpha=0.5,
        limit=3,
        return_metadata=MetadataQuery(score=True, explain_score=True),
    )

    print("\n🔍 하이브리드 검색: '로봇이 나오는 감동적인 영화'")
    for i, obj in enumerate(response.objects, 1):
        props = obj.properties
        score = obj.metadata.score if obj.metadata else None
        print(f"\n{i}. {props['title']} ({props['year']}) | score: {score}")
        print(f"   {props['description'][:60]}...")


# ====================
# 4. 알파 파라미터 튜닝
# ====================


def tune_alpha_parameter(client: weaviate.WeaviateClient):
    """
    알파(alpha) 파라미터 비교 실험

    참고:
        - alpha=0.0: 100% BM25 (순수 키워드 검색)
        - alpha=1.0: 100% 벡터 (순수 의미 검색)
        - alpha=0.5: 절반씩 혼합 (기본값)
        - 같은 쿼리라도 alpha에 따라 랭킹이 달라짐을 눈으로 확인!
    """
    print("\n" + "=" * 60)
    print("알파 파라미터 튜닝: 같은 쿼리, 다른 결과")
    print("=" * 60)

    collection = client.collections.get("Movie")

    # 의도: '가상현실'이라는 키워드가 정확히 있는 매트릭스가
    #       키워드 가중(낮은 alpha)에서 상위로 올라와야 함
    query = "가상현실"

    rankings: Dict[str, List[str]] = {}

    for alpha in [0.0, 0.3, 0.7, 1.0]:
        response = collection.query.hybrid(
            query=query,
            alpha=alpha,
            limit=3,
            return_metadata=MetadataQuery(score=True),
        )

        titles = [obj.properties["title"] for obj in response.objects]
        rankings[f"alpha={alpha}"] = titles

        print(f"\n🎯 alpha={alpha:.1f} {'(순수 BM25)' if alpha == 0.0 else '(순수 벡터)' if alpha == 1.0 else '(혼합)'}")
        print_results(response.objects)

    print("\n📊 랭킹 변화 요약:")
    for label, titles in rankings.items():
        print(f"   {label}: {' > '.join(titles)}")


# ====================
# 5. 퓨전(Fusion) 방식 비교
# ====================


def compare_fusion_types(client: weaviate.WeaviateClient):
    """
    퓨전 방식 비교

    참고:
        - RELATIVE_SCORE (기본): 점수의 상대적 크기를 정규화해 합산
          → 점수 차이까지 반영하므로 더 정밀한 랭킹
        - RANKED: 순위(rank)만 사용해 합산 (Reciprocal Rank Fusion 계열)
          → 점수 스케일이 서로 다를 때 안정적
    """
    print("\n" + "=" * 60)
    print("퓨전 방식 비교: RELATIVE_SCORE vs RANKED")
    print("=" * 60)

    collection = client.collections.get("Movie")

    query = "시간을 초월한 감동"

    for fusion_type, label in [
        (HybridFusion.RELATIVE_SCORE, "RELATIVE_SCORE (점수 기반, 기본값)"),
        (HybridFusion.RANKED, "RANKED (순위 기반)"),
    ]:
        response = collection.query.hybrid(
            query=query,
            alpha=0.5,
            fusion_type=fusion_type,
            limit=3,
            return_metadata=MetadataQuery(score=True),
        )

        print(f"\n🔧 fusion_type={label}")
        print_results(response.objects)


# ====================
# 6. 실전: 필터 + 오토틀림 조합
# ====================


def practical_hybrid_usage(client: weaviate.WeaviateClient):
    """
    실전 하이브리드 검색 활용

    참고:
        - filters와 결합하면 "조건을 만족하는 것 중에서" 의미+키워드 검색 가능
        - auto_limit(autocut): 점수가 급격히 떨어지는 지점에서 결과를
          자동으로 잘라내 노이즈를 줄임
    """
    print("\n" + "=" * 60)
    print("실전 활용: 필터 + autocut")
    print("=" * 60)

    collection = client.collections.get("Movie")

    from weaviate.classes.query import Filter

    # 1) 필터 결합: 2010년 이후 영화 중에서만 하이브리드 검색
    response = collection.query.hybrid(
        query="우주 탐험",
        alpha=0.6,
        filters=Filter.by_property("year").greater_or_equal(2010),
        limit=3,
        return_metadata=MetadataQuery(score=True),
    )

    print("\n🔍 '우주 탐험' + year >= 2010")
    print_results(response.objects)

    # 2) 특정 속성에서만 검색 (query_properties)
    response = collection.query.hybrid(
        query="슈퍼히어로",
        query_properties=["description"],  # 제목이 아니라 줄거리에서 찾기
        alpha=0.5,
        limit=3,
        return_metadata=MetadataQuery(score=True),
    )

    print("\n🔍 '슈퍼히어로' (description에서만 검색)")
    print_results(response.objects)

    # 3) autocut: 노이즈 자동 제거
    response = collection.query.hybrid(
        query="감옥",
        alpha=0.4,
        auto_limit=1,  # 점수 급락 지점에서 자르기
        limit=5,
        return_metadata=MetadataQuery(score=True),
    )

    print(f"\n🔍 '감옥' + auto_limit=1 → 실제 반환: {len(response.objects)}개")
    print_results(response.objects)


# ====================
# 7. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "🔀" * 25)
    print("하이브리드 검색 (Hybrid Search) 학습")
    print("🔀" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 1. 준비
            setup_movie_collection(client)

            # 2. BM25 키워드 검색
            search_bm25(client)

            # 3. 하이브리드 검색 기본
            search_hybrid_basic(client)

            # 4. 알파 파라미터 튜닝
            tune_alpha_parameter(client)

            # 5. 퓨전 방식 비교
            compare_fusion_types(client)

            # 6. 실전 활용
            practical_hybrid_usage(client)

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n💡 핵심 정리:")
    print("   - BM25: 키워드 정확 매칭 (동의어는 못 찾음)")
    print("   - Hybrid: 키워드 + 의미 결합 (alpha로 비중 조절)")
    print("   - alpha=0 키워드, alpha=1 벡터, alpha=0.5 균형")
    print("   - RELATIVE_SCORE: 점수 기반 / RANKED: 순위 기반")

    print("\n📚 다음 학습:")
    print("   python 03_filters.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. 검색 방식 3종
   - BM25: 키워드 기반 (query.bm25)
   - 벡터: 의미 기반 (query.near_text)
   - Hybrid: 둘의 결합 (query.hybrid)

2. 알파 파라미터 선택 가이드
   - 고유명사/코드/ID 검색 → 낮은 alpha (0.2~0.4)
   - 추상적/자연어 질문 → 높은 alpha (0.6~0.8)
   - 잘 모르겠으면 → 0.5에서 시작해 실험

3. 퓨전 방식
   - RELATIVE_SCORE: 점수 정규화 후 합산 (기본, 권장)
   - RANKED: 순위 기반 (Reciprocal Rank Fusion 계열)

💡 실전 팁:
   - query_properties로 검색 범위를 좁히면 품질 향상
   - filters와 결합해 "조건부 의미 검색" 구현
   - auto_limit로 관련 없는 꼬리 결과 제거

⚠️ 주의사항:
   - 하이브리드 검색에는 벡터화 모듈 필요 (여기선 text2vec-openai)
   - 한글 BM25는 토크나이저 설정에 따라 결과가 달라짐
     (Property의 tokenization 옵션 참고)

🔧 연습 과제:
   1. alpha를 0.0~1.0 사이 10단계로 바꿔가며 랭킹 변화 기록
   2. 자신의 도메인 데이터에서 최적 alpha 찾기
   3. query_properties를 바꿔보며 결과 비교
"""
