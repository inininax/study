"""
Weaviate 배치 작업
==================

이 모듈에서 배울 내용:
1. 배치 삽입 (Batch Insert)
2. 성능 최적화
3. 에러 처리 및 재시도
4. 진행 상황 모니터링

난이도: ⭐⭐⭐ (중간)
소요 시간: 1시간
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.util import generate_uuid5
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random
import time


# ====================
# 1. 준비: 테스트 데이터 생성
# ====================


def generate_sample_articles(count: int = 100) -> List[Dict[str, Any]]:
    """
    테스트용 샘플 기사 데이터 생성

    Args:
        count: 생성할 기사 개수

    Returns:
        List[Dict]: 기사 데이터 리스트
    """
    print(f"📝 {count}개의 샘플 데이터 생성 중...")

    titles = [
        "AI의 미래와 전망",
        "Python 프로그래밍 기초",
        "데이터베이스 최적화 기법",
        "클라우드 컴퓨팅 트렌드",
        "머신러닝 실전 가이드",
        "웹 개발 베스트 프랙티스",
        "사이버 보안 핵심 개념",
        "DevOps 문화와 도구",
        "빅데이터 분석 방법론",
        "블록체인 기술 이해",
    ]

    authors = ["홍길동", "김개발", "이데이터", "박클라우드", "최AI"]

    tags_pool = [
        ["AI", "기술"],
        ["Python", "프로그래밍"],
        ["데이터베이스", "최적화"],
        ["클라우드", "AWS"],
        ["머신러닝", "딥러닝"],
    ]

    articles = []
    base_date = datetime.now()

    for i in range(count):
        article = {
            "title": f"{random.choice(titles)} - Part {i+1}",
            "content": f"이것은 {i+1}번째 기사의 내용입니다. " * 10,
            "author": random.choice(authors),
            "published_date": (
                base_date - timedelta(days=random.randint(0, 365))
            ).isoformat()
            + "Z",
            "views": random.randint(0, 10000),
            "tags": random.choice(tags_pool),
        }
        articles.append(article)

    print(f"✅ {count}개의 샘플 데이터 생성 완료")
    return articles


# ====================
# 2. 배치 삽입 - 기본
# ====================


def batch_insert_basic(client: weaviate.WeaviateClient, articles: List[Dict]):
    """
    기본 배치 삽입

    Args:
        client: Weaviate 클라이언트
        articles: 삽입할 기사 리스트

    참고:
        - 배치 작업은 단일 삽입보다 훨씬 빠릅니다
        - 네트워크 왕복 횟수를 줄여 성능 향상
    """
    print(f"\n📦 기본 배치 삽입 ({len(articles)}개)...")

    collection = client.collections.get("Article")

    start_time = time.time()

    # with 문으로 배치 컨텍스트 시작
    # 배치가 끝나면 자동으로 전송됨
    with collection.batch.dynamic() as batch:
        for article in articles:
            # 배치에 객체 추가
            batch.add_object(properties=article)

    elapsed = time.time() - start_time

    print(f"✅ 배치 삽입 완료!")
    print(f"   소요 시간: {elapsed:.2f}초")
    print(f"   초당 처리: {len(articles) / elapsed:.2f}개/초")


# ====================
# 3. 배치 삽입 - 성능 최적화
# ====================


def batch_insert_optimized(client: weaviate.WeaviateClient, articles: List[Dict]):
    """
    최적화된 배치 삽입

    참고:
        - batch_size: 한 번에 보낼 객체 수
        - num_workers: 병렬 워커 수
        - 크기와 워커를 조정하여 성능 최적화
    """
    print(f"\n⚡ 최적화된 배치 삽입 ({len(articles)}개)...")

    collection = client.collections.get("Article")

    start_time = time.time()

    # 최적화된 배치 설정
    with collection.batch.dynamic() as batch:
        for i, article in enumerate(articles):
            # UUID를 결정론적으로 생성
            article_uuid = generate_uuid5(f"article-{i}")

            # 배치에 추가
            batch.add_object(properties=article, uuid=article_uuid)

            # 진행 상황 표시 (100개마다)
            if (i + 1) % 100 == 0:
                print(f"   진행: {i + 1}/{len(articles)}")

    elapsed = time.time() - start_time

    print(f"✅ 최적화된 배치 삽입 완료!")
    print(f"   소요 시간: {elapsed:.2f}초")
    print(f"   초당 처리: {len(articles) / elapsed:.2f}개/초")


# ====================
# 4. 배치 삽입 - 에러 처리
# ====================


def batch_insert_with_error_handling(
    client: weaviate.WeaviateClient, articles: List[Dict]
):
    """
    에러 처리가 포함된 배치 삽입

    참고:
        - 일부 객체 실패시에도 계속 진행
        - 실패한 객체 추적 및 재시도 가능
    """
    print(f"\n🛡️ 에러 처리가 포함된 배치 삽입...")

    collection = client.collections.get("Article")

    successful = 0
    failed = 0
    failed_objects = []

    start_time = time.time()

    # 배치 컨텍스트 시작
    with collection.batch.dynamic() as batch:
        for i, article in enumerate(articles):
            try:
                batch.add_object(properties=article)
                successful += 1

            except Exception as e:
                failed += 1
                failed_objects.append({"index": i, "error": str(e), "data": article})
                print(f"   ⚠️ 객체 {i} 실패: {e}")

    elapsed = time.time() - start_time

    print(f"\n📊 배치 삽입 결과:")
    print(f"   성공: {successful}개")
    print(f"   실패: {failed}개")
    print(f"   소요 시간: {elapsed:.2f}초")

    # 실패한 객체 정보 반환
    return failed_objects


# ====================
# 5. 배치 업데이트
# ====================


def batch_update_objects(client: weaviate.WeaviateClient):
    """
    배치로 여러 객체 업데이트

    참고:
        - 조회수 증가 등 대량 업데이트에 유용
    """
    print(f"\n🔄 배치 업데이트...")

    from weaviate.classes.query import Filter

    collection = client.collections.get("Article")

    # 업데이트할 객체들 조회
    response = collection.query.fetch_objects(
        filters=Filter.by_property("author").equal("홍길동"), limit=50
    )

    print(f"   업데이트 대상: {len(response.objects)}개")

    # 배치 업데이트
    updated_count = 0
    for obj in response.objects:
        try:
            # 조회수 2배로 증가
            new_views = obj.properties["views"] * 2
            collection.data.update(
                uuid=obj.uuid, properties={"views": new_views}
            )
            updated_count += 1
        except Exception as e:
            print(f"   ⚠️ 업데이트 실패: {e}")

    print(f"✅ {updated_count}개 객체 업데이트 완료")


# ====================
# 6. 배치 삭제
# ====================


def batch_delete_objects(client: weaviate.WeaviateClient):
    """
    배치로 여러 객체 삭제

    참고:
        - 조건에 맞는 객체들을 한 번에 삭제
        - 주의: 복구 불가능!
    """
    print(f"\n🗑️ 배치 삭제...")

    from weaviate.classes.query import Filter

    collection = client.collections.get("Article")

    # 조회수가 100 미만인 기사 삭제
    result = collection.data.delete_many(
        where=Filter.by_property("views").less_than(100)
    )

    print(f"✅ 삭제 완료:")
    print(f"   성공: {result.successful}개")
    print(f"   실패: {result.failed}개")


# ====================
# 7. 성능 비교
# ====================


def compare_single_vs_batch(client: weaviate.WeaviateClient):
    """
    단일 삽입 vs 배치 삽입 성능 비교
    """
    print("\n" + "=" * 50)
    print("성능 비교: 단일 삽입 vs 배치 삽입")
    print("=" * 50)

    collection = client.collections.get("Article")

    # 테스트 데이터 (50개)
    test_articles = generate_sample_articles(50)

    # 1. 단일 삽입
    print("\n1️⃣ 단일 삽입 (50개)...")
    start = time.time()
    for article in test_articles:
        collection.data.insert(properties=article)
    single_time = time.time() - start
    print(f"   소요 시간: {single_time:.2f}초")

    # 데이터 정리
    collection.data.delete_many(where=Filter())

    # 2. 배치 삽입
    print("\n2️⃣ 배치 삽입 (50개)...")
    start = time.time()
    with collection.batch.dynamic() as batch:
        for article in test_articles:
            batch.add_object(properties=article)
    batch_time = time.time() - start
    print(f"   소요 시간: {batch_time:.2f}초")

    # 결과 비교
    print("\n📊 결과:")
    print(f"   단일 삽입: {single_time:.2f}초")
    print(f"   배치 삽입: {batch_time:.2f}초")
    print(f"   성능 향상: {single_time / batch_time:.1f}배 빠름")


# ====================
# 8. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "🚀" * 25)
    print("Weaviate 배치 작업 학습")
    print("🚀" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 0. 준비: 컬렉션 생성
            print("\n📦 Article 컬렉션 설정...")
            if client.collections.exists("Article"):
                client.collections.delete("Article")

            client.collections.create(
                name="Article",
                properties=[
                    Property(name="title", data_type=DataType.TEXT),
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="author", data_type=DataType.TEXT),
                    Property(name="published_date", data_type=DataType.DATE),
                    Property(name="views", data_type=DataType.INT),
                    Property(name="tags", data_type=DataType.TEXT_ARRAY),
                ],
                vectorizer_config=Configure.Vectorizer.text2vec_openai(
                    model="text-embedding-3-small"
                ),
            )
            print("✅ 컬렉션 생성 완료\n")

            # 1. 샘플 데이터 생성
            articles = generate_sample_articles(200)

            # 2. 기본 배치 삽입
            batch_insert_basic(client, articles[:100])

            # 3. 최적화된 배치 삽입
            batch_insert_optimized(client, articles[100:])

            # 4. 에러 처리
            print("\n" + "=" * 50)
            print("에러 처리 데모")
            print("=" * 50)
            # (정상 데이터라 에러 없음)

            # 5. 배치 업데이트
            batch_update_objects(client)

            # 6. 배치 삭제
            batch_delete_objects(client)

            # 7. 성능 비교
            # compare_single_vs_batch(client)  # 시간이 걸리므로 필요시 활성화

            # 최종 통계
            print("\n" + "=" * 50)
            print("최종 통계")
            print("=" * 50)
            collection = client.collections.get("Article")
            response = collection.query.fetch_objects(limit=1)
            # 총 객체 수는 aggregate로 확인 가능
            print(f"   현재 객체 수: 확인 중...")

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "🎉" * 25)
    print("초급 학습 완료!")
    print("🎉" * 25)

    print("\n📚 다음 학습:")
    print("   cd ../02-intermediate")
    print("   python 01_vector_search.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. 배치 삽입
   - batch.dynamic(): 자동 최적화 배치
   - 단일 삽입보다 훨씬 빠름
   - with 문으로 자동 전송

2. 성능 최적화
   - 배치 크기 조정
   - 병렬 워커 활용
   - 진행 상황 모니터링

3. 에러 처리
   - try-except로 개별 에러 처리
   - 실패한 객체 추적
   - 재시도 로직 구현 가능

4. 배치 작업 종류
   - 삽입 (insert)
   - 업데이트 (update)
   - 삭제 (delete)

💡 실무 팁:
   - 대량 데이터는 반드시 배치 사용
   - 10배 이상 성능 향상 가능
   - UUID를 결정론적으로 생성하면 중복 방지
   - 진행 상황 로깅으로 모니터링

⚠️ 주의사항:
   - 너무 큰 배치는 메모리 부족 유발
   - 네트워크 타임아웃 고려
   - 에러 처리 필수

🔧 연습 과제:
   1. 더 많은 데이터 (1000개+) 삽입해보기
   2. 에러 재시도 로직 구현
   3. 배치 크기별 성능 측정

🎓 초급 과정 완료!
   다음은 중급 과정으로 이동하세요.
   벡터 검색의 진정한 힘을 경험할 것입니다!
"""
