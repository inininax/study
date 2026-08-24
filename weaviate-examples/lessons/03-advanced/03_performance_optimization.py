"""
성능 최적화 (Performance Optimization)
=======================================

이 모듈에서 배울 내용:
1. 배치 삽입 성능: dynamic vs fixed_size 비교
2. HNSW 파라미터: 인덱스 품질과 속도의 트레이드오프
3. 쿼리 최적화: limit, autocut, 프로젝션
4. 실행 중 설정 변경 (Reconfigure)
5. 벡터 압축(양자화) 소개

난이도: ⭐⭐⭐⭐ (높음)
소요 시간: 1.5시간

💡 이 레슨은 Vectorizer.none() + 무작위 벡터를 사용합니다!
   - OpenAI API 키/비용 없이 순수 DB 성능만 측정하기 위함
   - 실제 서비스에서는 임베딩 생성 시간도 함께 고려해야 합니다
"""

import random
import time
from typing import List

import weaviate
from weaviate.classes.config import (
    Configure,
    Property,
    DataType,
    Reconfigure,
    VectorDistances,
)


# 벡터 차원 (실제 임베딩 모델은 1536 등을 사용하지만 데모는 가볍게)
VECTOR_DIM = 128


# ====================
# 1. 벤치마크 데이터 생성
# ====================


def make_random_vector() -> List[float]:
    """무작위 벡터 생성 (데모용)"""
    return [random.random() for _ in range(VECTOR_DIM)]


def make_docs(count: int) -> List[dict]:
    """벤치마크용 문서 목록 생성"""
    docs = []
    for i in range(count):
        docs.append(
            {
                "properties": {
                    "title": f"문서-{i:05d}",
                    "content": f"성능 테스트용 문서 {i}번입니다.",
                    "category": f"cat-{i % 5}",
                },
                "vector": make_random_vector(),
            }
        )
    return docs


# ====================
# 2. 배치 삽입 성능 비교
# ====================


def benchmark_batch_strategies(client: weaviate.WeaviateClient, doc_count: int = 2000):
    """
    배치 전략별 삽입 속도 비교

    참고:
        - dynamic(): 클라이언트가 배치 크기를 자동 조절 (간편, 기본값 권장)
        - fixed_size(batch_size=N): 크기 고정 (트래픽 예측 가능, 대량 마이그레이션에 유리)
        - concurrent_requests: 동시 전송 스레드 수
    """
    print("\n" + "=" * 60)
    print(f"배치 삽입 성능 비교 ({doc_count}개 문서)")
    print("=" * 60)

    docs = make_docs(doc_count)

    strategies = [
        ("dynamic", lambda c: c.batch.dynamic()),
        ("fixed_size(batch=100)", lambda c: c.batch.fixed_size(batch_size=100, concurrent_requests=2)),
    ]

    for label, get_batch in strategies:
        name = f"Bench_{label.split('(')[0].capitalize()}"

        if client.collections.exists(name):
            client.collections.delete(name)

        client.collections.create(
            name=name,
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="content", data_type=DataType.TEXT),
                Property(name="category", data_type=DataType.TEXT),
            ],
            vectorizer_config=Configure.Vectorizer.none(),  # 벡터 직접 제공
        )

        collection = client.collections.get(name)

        start = time.perf_counter()
        with get_batch(collection) as batch:
            for doc in docs:
                batch.add_object(properties=doc["properties"], vector=doc["vector"])
        elapsed = time.perf_counter() - start

        failed = len(collection.batch.failed_objects)
        speed = doc_count / elapsed if elapsed > 0 else 0
        print(f"\n🚀 {label}: {elapsed:.2f}초 ({speed:,.0f} obj/s) | 실패: {failed}개")


# ====================
# 3. HNSW 파라미터 비교
# ====================


def benchmark_hsnw_parameters(client: weaviate.WeaviateClient, doc_count: int = 800):
    """
    HNSW 파라미터에 따른 색인 속도 / 검색 지연 비교

    참고:
        - max_connections(M): 그래프 노드당 최대 연결 수 → 클수록 정확, 메모리↑
        - ef_construction: 색인 시 탐색 폭 → 클수록 인덱스 품질↑, 색인 느림
        - ef(동적): 검색 시 탐색 폭 → 클수록 정확, 느림 (dynamic_ef_min/max로 자동 조절)
    """
    print("\n" + "=" * 60)
    print(f"HNSW 파라미터 비교 ({doc_count}개 문서)")
    print("=" * 60)

    docs = make_docs(doc_count)
    query_vector = docs[0]["vector"]  # 첫 문서를 질의 벡터로 재사용

    configs = [
        ("PerfHnswSmall", dict(max_connections=8, ef_construction=32)),
        ("PerfHnswLarge", dict(max_connections=32, ef_construction=128)),
    ]

    results = {}

    for name, params in configs:
        if client.collections.exists(name):
            client.collections.delete(name)

        client.collections.create(
            name=name,
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="content", data_type=DataType.TEXT),
                Property(name="category", data_type=DataType.TEXT),
            ],
            vectorizer_config=Configure.Vectorizer.none(),
            vector_index_config=Configure.VectorIndex.hnsw(
                distance_metric=VectorDistances.COSINE,
                **params,
            ),
        )

        collection = client.collections.get(name)

        # 색인 시간 측정
        start = time.perf_counter()
        with collection.batch.fixed_size(batch_size=200) as batch:
            for doc in docs:
                batch.add_object(properties=doc["properties"], vector=doc["vector"])
        index_time = time.perf_counter() - start

        # 검색 지연 측정 (20회 평균)
        latencies = []
        for _ in range(20):
            q_start = time.perf_counter()
            collection.query.near_vector(
                near_vector=query_vector, limit=5, include_vector=False
            )
            latencies.append((time.perf_counter() - q_start) * 1000)

        avg_latency = sum(latencies) / len(latencies)
        results[name] = {"index": index_time, "latency": avg_latency}

        print(
            f"\n🔧 {name} (max_connections={params['max_connections']}, "
            f"ef_construction={params['ef_construction']})"
        )
        print(f"   색인 시간:   {index_time:.2f}초")
        print(f"   평균 검색:   {avg_latency:.2f}ms")

    print("\n📊 요약:")
    small, large = results.values()
    print("   작은 파라미터 → 색인 빠름, 검색 다소 부정확할 수 있음")
    print("   큰 파라미터   → 색인 느림/메모리↑, 검색 정확도↑")

    # 정리
    for name, _ in configs:
        client.collections.delete(name)


# ====================
# 4. 쿼리 최적화
# ====================


def optimize_queries(client: weaviate.WeaviateClient):
    """
    쿼리 레벨 최적화 기법

    참고:
        - return_properties: 필요한 속성만 조회 (네트워크/직렬화 절감)
        - auto_limit(autocut): 관련 없는 꼬리 결과 자동 제거
        - limit 최소화: limit이 클수록 탐색량 증가
    """
    print("\n" + "=" * 60)
    print("쿼리 최적화 기법")
    print("=" * 60)

    # 실습용 컬렉션 준비
    if client.collections.exists("PerfQuery"):
        client.collections.delete("PerfQuery")

    client.collections.create(
        name="PerfQuery",
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="content", data_type=DataType.TEXT),
            Property(name="category", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )

    collection = client.collections.get("PerfQuery")
    docs = make_docs(500)

    with collection.batch.dynamic() as batch:
        for doc in docs:
            batch.add_object(properties=doc["properties"], vector=doc["vector"])

    query_vector = docs[0]["vector"]

    # 1) 프로젝션: 전체 속성 vs 필요한 속성만
    start = time.perf_counter()
    for _ in range(20):
        collection.query.near_vector(near_vector=query_vector, limit=10)
    full_ms = (time.perf_counter() - start) / 20 * 1000

    start = time.perf_counter()
    for _ in range(20):
        collection.query.near_vector(
            near_vector=query_vector,
            limit=10,
            return_properties=["title"],  # title만!
        )
    projected_ms = (time.perf_counter() - start) / 20 * 1000

    print(f"\n🎯 프로젝션 효과 (20회 평균):")
    print(f"   전체 속성 조회: {full_ms:.2f}ms")
    print(f"   title만 조회:   {projected_ms:.2f}ms  ← 데이터가 클수록 차이 커짐")

    # 2) autocut: 점수 급락 지점에서 결과 절단
    response = collection.query.near_vector(near_vector=query_vector, limit=50)
    response_cut = collection.query.near_vector(
        near_vector=query_vector, limit=50, auto_limit=1
    )
    print(f"\n✂️ autocut 효과:")
    print(f"   limit=50 그대로:     {len(response.objects)}개 반환")
    print(f"   auto_limit=1 적용:   {len(response_cut.objects)}개 반환 (노이즈 제거)")

    # 정리
    client.collections.delete("PerfQuery")


# ====================
# 5. 실행 중 설정 변경 (Reconfigure)
# ====================


def reconfigure_runtime_settings(client: weaviate.WeaviateClient):
    """
    컬렉션 설정 동적 변경

    참고:
        - Reconfigure.*는 '재색인 없이' 변경 가능한 항목만 허용
        - hnsw.ef, dynamic_ef_min/max: 검색 시 탐색 폭 → 즉시 반영
        - max_connections/ef_construction은 변경 불가 (재생성 필요)
        - inverted_index bm25 파라미터(b/k1)도 동적으로 조절 가능
    """
    print("\n" + "=" * 60)
    print("실행 중 설정 변경 (Reconfigure)")
    print("=" * 60)

    if client.collections.exists("PerfReconfig"):
        client.collections.delete("PerfReconfig")

    from weaviate.classes.config import StopwordsPreset

    client.collections.create(
        name="PerfReconfig",
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="content", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
        vector_index_config=Configure.VectorIndex.hnsw(
            dynamic_ef_min=50, dynamic_ef_max=200
        ),
        inverted_index_config=Configure.inverted_index(
            bm25_b=0.75, bm25_k1=1.2, stopwords_preset=StopwordsPreset.EN
        ),
    )

    collection = client.collections.get("PerfReconfig")

    before = collection.config.get()
    print("\n📖 변경 전:")
    print(f"   dynamic_ef_min={before.vector_index_config.dynamic_ef_min}")
    print(f"   dynamic_ef_max={before.vector_index_config.dynamic_ef_max}")

    # 검색 정확도를 높이기 위해 탐색 폭 상향
    collection.config.update(
        vector_index_config=Reconfigure.VectorIndex.hnsw(
            dynamic_ef_min=100, dynamic_ef_max=500
        )
    )

    after = collection.config.get()
    print("\n🔧 변경 후 (더 넓은 탐색 → 더 정확, 다소 느림):")
    print(f"   dynamic_ef_min={after.vector_index_config.dynamic_ef_min}")
    print(f"   dynamic_ef_max={after.vector_index_config.dynamic_ef_max}")
    print(f"   bm25_k1={after.inverted_index_config.bm25_k1}, "
          f"bm25_b={after.inverted_index_config.bm25_b}")

    # 정리
    client.collections.delete("PerfReconfig")


# ====================
# 6. 벡터 압축 (양자화)
# ====================


def quantization_demo(client: weaviate.WeaviateClient):
    """
    벡터 압축(양자화) 소개

    참고:
        - BQ(Binary): float32 → 1bit, 메모리 ~1/32, 리스코어링으로 정확도 보완
        - SQ(Scalar): float32 → int8, 메모리 ~1/4
        - PQ(Product): 세그먼트별 양자화, 대규모에 적합
        - quantizer를 제외한 나머지는 일반 컬렉션과 동일하게 동작
    """
    print("\n" + "=" * 60)
    print("벡터 압축 데모 (Binary Quantization)")
    print("=" * 60)

    if client.collections.exists("PerfQuantized"):
        client.collections.delete("PerfQuantized")

    client.collections.create(
        name="PerfQuantized",
        properties=[Property(name="title", data_type=DataType.TEXT)],
        vectorizer_config=Configure.Vectorizer.none(),
        vector_index_config=Configure.VectorIndex.hnsw(
            distance_metric=VectorDistances.COSINE,
            # ★ BQ 적용: rescore_limit개 원본 후보로 재채점해 정확도 보완
            quantizer=Configure.VectorIndex.Quantizer.bq(rescore_limit=200),
        ),
    )

    collection = client.collections.get("PerfQuantized")
    docs = make_docs(300)

    start = time.perf_counter()
    with collection.batch.dynamic() as batch:
        for doc in docs:
            batch.add_object(properties=doc["properties"], vector=doc["vector"])
    print(f"\n💾 BQ 적용 컬렉션 삽입: {time.perf_counter() - start:.2f}초")

    response = collection.query.near_vector(near_vector=docs[0]["vector"], limit=3)
    print(f"🔍 BQ 컬렉션에서 검색: {len(response.objects)}개 결과 정상 반환 ✅")
    print("\n💡 운영 팁: 메모리가 병목일 때 양자화가 강력한 해결책!")
    print("   단, 도입 전 반드시 자신의 데이터로 리콜(recall) 검증부터!")

    # 정리
    client.collections.delete("PerfQuantized")


# ====================
# 7. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "⚡" * 25)
    print("성능 최적화 (Performance Optimization) 학습")
    print("⚡" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 1. 배치 삽입 성능 비교
            benchmark_batch_strategies(client, doc_count=2000)

            # 2. HNSW 파라미터 비교
            benchmark_hsnw_parameters(client, doc_count=800)

            # 3. 쿼리 최적화
            optimize_queries(client)

            # 4. 실행 중 설정 변경
            reconfigure_runtime_settings(client)

            # 5. 양자화 데모
            quantization_demo(client)

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n💡 핵심 정리:")
    print("   - 배치: dynamic 간편 / fixed_size 예측 가능")
    print("   - HNSW: max_connections·ef_construction ↑ → 정확하지만 무거움")
    print("   - 쿼리: return_properties로 필요한 것만, auto_limit로 노이즈 제거")
    print("   - Reconfigure로 재색인 없이 ef/bm25 파라미터 조정")
    print("   - 메모리 병목엔 양자화(BQ/SQ/PQ), 단 리콜 검증 필수!")

    print("\n📚 다음 학습:")
    print("   python 04_monitoring.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. 최적화 레이어
   - 데이터 삽입: 배치 크기/동시성 튜닝
   - 인덱스: HNSW 파라미터, 양자화
   - 쿼리: limit/autocut/프로젝션/필터 전략

2. 트레이드오프 사고방식
   - 정확도 ↔ 속도 ↔ 메모리: 세 가지를 동시에 다 잡을 순 없다
   - 워크로드 측정 먼저, 변경은 한 번에 하나씩!

3. 운영 체크포인트
   - 색인 지연(vector_indexing_status) 모니터링
   - vector_cache_max_objects로 캐시 메모리 제한
   - 속성별 index_filterable/index_searchable로 불필요한 인덱스 제거

⚠️ 주의사항:
   - 벤치마크는 실제 데이터 분포와 유사하게 해야 의미 있음
   - 무작위 벡터는 실제 임베딩보다 클러스터링이 없어 결과가 다를 수 있음
   - 양자화는 리콜 손실이 있으므로 A/B 검증 후 도입

🔧 연습 과제:
   1. VECTOR_DIM을 768/1536으로 바꿔 성능 변화 측정
   2. ef_construction을 바꿔가며 리콜@5 측정해보기
      (근사 검색 결과 vs 완전 탐색 결과 비교)
   3. Property(index_filterable=False) 효과 확인해보기
"""
