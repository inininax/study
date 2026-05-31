"""
Weaviate CRUD 작업
==================

이 모듈에서 배울 내용:
1. Create: 객체 생성
2. Read: 객체 조회
3. Update: 객체 수정
4. Delete: 객체 삭제

난이도: ⭐⭐ (쉬움)
소요 시간: 1.5시간
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.data import DataObject
from weaviate.util import generate_uuid5
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid


# ====================
# 1. 준비: 컬렉션 생성
# ====================


def setup_collection(client: weaviate.WeaviateClient):
    """테스트용 Article 컬렉션 생성"""
    print("📦 Article 컬렉션 설정...")

    # 기존 컬렉션 삭제
    if client.collections.exists("Article"):
        client.collections.delete("Article")

    # 컬렉션 생성
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

    print("✅ Article 컬렉션 생성 완료\n")


# ====================
# 2. CREATE - 객체 생성
# ====================


def create_single_object(client: weaviate.WeaviateClient) -> str:
    """
    단일 객체 생성

    Returns:
        str: 생성된 객체의 UUID
    """
    print("➕ 단일 객체 생성...")

    # 컬렉션 가져오기
    articles = client.collections.get("Article")

    # 데이터 준비
    article_data = {
        "title": "Weaviate 벡터 데이터베이스 소개",
        "content": "Weaviate는 오픈소스 벡터 데이터베이스입니다...",
        "author": "홍길동",
        "published_date": datetime.now().isoformat() + "Z",
        "views": 0,
        "tags": ["AI", "데이터베이스", "벡터검색"],
    }

    # 객체 생성
    # insert()는 자동으로 UUID를 생성하고 데이터를 삽입합니다
    uuid_generated = articles.data.insert(properties=article_data)

    print(f"✅ 객체 생성 완료!")
    print(f"   UUID: {uuid_generated}")
    print(f"   제목: {article_data['title']}")

    return str(uuid_generated)


def create_object_with_custom_uuid(client: weaviate.WeaviateClient) -> str:
    """
    커스텀 UUID로 객체 생성

    참고:
        - UUID를 직접 지정할 수 있음
        - 중복 방지 또는 외부 시스템과 동기화에 유용
    """
    print("\n🎯 커스텀 UUID로 객체 생성...")

    articles = client.collections.get("Article")

    # 결정론적 UUID 생성 (같은 입력이면 같은 UUID)
    # generate_uuid5: 이름 기반 UUID 생성
    article_id = "article-001"  # 고유 식별자
    custom_uuid = generate_uuid5(article_id)

    article_data = {
        "title": "Python으로 시작하는 AI 개발",
        "content": "Python은 AI 개발의 표준 언어입니다...",
        "author": "김개발",
        "published_date": "2024-01-15T10:00:00Z",
        "views": 150,
        "tags": ["Python", "AI", "개발"],
    }

    # UUID를 명시적으로 지정
    articles.data.insert(properties=article_data, uuid=custom_uuid)

    print(f"✅ 객체 생성 완료!")
    print(f"   UUID: {custom_uuid}")
    print(f"   제목: {article_data['title']}")

    return str(custom_uuid)


def create_object_with_vector(client: weaviate.WeaviateClient) -> str:
    """
    수동 벡터를 포함한 객체 생성

    참고:
        - 자동 벡터화 대신 직접 벡터를 제공
        - 벡터 차원은 모델에 따라 다름 (OpenAI: 1536)
    """
    print("\n🔢 수동 벡터로 객체 생성...")

    articles = client.collections.get("Article")

    # 간단한 예시 벡터 (실제로는 임베딩 모델 사용)
    # 주의: 실제 프로덕션에서는 올바른 차원의 벡터 필요!
    custom_vector = [0.1] * 1536  # OpenAI 벡터 차원

    article_data = {
        "title": "벡터 데이터베이스의 원리",
        "content": "벡터 데이터베이스는 고차원 벡터를 저장합니다...",
        "author": "이연구",
        "published_date": "2024-01-16T10:00:00Z",
        "views": 89,
        "tags": ["벡터", "데이터베이스", "이론"],
    }

    # 벡터와 함께 삽입
    uuid_generated = articles.data.insert(
        properties=article_data,
        vector=custom_vector,  # 수동 벡터 제공
    )

    print(f"✅ 객체 생성 완료!")
    print(f"   UUID: {uuid_generated}")
    print(f"   벡터 차원: {len(custom_vector)}")

    return str(uuid_generated)


# ====================
# 3. READ - 객체 조회
# ====================


def read_object_by_uuid(client: weaviate.WeaviateClient, object_uuid: str):
    """
    UUID로 객체 조회

    Args:
        client: Weaviate 클라이언트
        object_uuid: 조회할 객체의 UUID
    """
    print(f"\n🔍 UUID로 객체 조회: {object_uuid}")

    articles = client.collections.get("Article")

    try:
        # UUID로 객체 가져오기
        article = articles.query.fetch_object_by_id(uuid=object_uuid)

        if article:
            print("✅ 객체 찾음!")
            print(f"   제목: {article.properties['title']}")
            print(f"   작성자: {article.properties['author']}")
            print(f"   조회수: {article.properties['views']}")
            print(f"   태그: {', '.join(article.properties['tags'])}")

            return article.properties
        else:
            print("❌ 객체를 찾을 수 없습니다")

    except Exception as e:
        print(f"❌ 조회 실패: {e}")


def read_all_objects(client: weaviate.WeaviateClient, limit: int = 10):
    """
    모든 객체 조회

    Args:
        client: Weaviate 클라이언트
        limit: 조회할 최대 객체 수
    """
    print(f"\n📋 모든 객체 조회 (최대 {limit}개)...")

    articles = client.collections.get("Article")

    # 모든 객체 가져오기
    response = articles.query.fetch_objects(limit=limit)

    print(f"✅ 총 {len(response.objects)} 개의 객체 발견")

    for i, obj in enumerate(response.objects, 1):
        print(f"\n{i}. {obj.properties['title']}")
        print(f"   작성자: {obj.properties['author']}")
        print(f"   UUID: {obj.uuid}")


def read_objects_with_filter(client: weaviate.WeaviateClient):
    """
    조건 필터링으로 객체 조회

    참고:
        - Where 필터로 특정 조건의 객체만 조회
        - SQL의 WHERE 절과 유사
    """
    print("\n🔎 필터링으로 객체 조회...")

    from weaviate.classes.query import Filter

    articles = client.collections.get("Article")

    # 조회수가 100 이상인 기사만 조회
    response = articles.query.fetch_objects(
        filters=Filter.by_property("views").greater_than(100), limit=10
    )

    print(f"✅ 조회수 100 이상: {len(response.objects)}개")

    for obj in response.objects:
        print(f"   - {obj.properties['title']} (조회수: {obj.properties['views']})")


# ====================
# 4. UPDATE - 객체 수정
# ====================


def update_object_properties(client: weaviate.WeaviateClient, object_uuid: str):
    """
    객체의 속성 수정

    Args:
        client: Weaviate 클라이언트
        object_uuid: 수정할 객체의 UUID
    """
    print(f"\n✏️ 객체 수정: {object_uuid}")

    articles = client.collections.get("Article")

    # 수정 전 데이터 확인
    original = articles.query.fetch_object_by_id(uuid=object_uuid)
    print(f"   수정 전 조회수: {original.properties['views']}")

    # 속성 업데이트
    # update()는 지정한 속성만 수정 (나머지는 유지)
    articles.data.update(
        uuid=object_uuid,
        properties={
            "views": original.properties["views"] + 1,  # 조회수 증가
        },
    )

    # 수정 후 확인
    updated = articles.query.fetch_object_by_id(uuid=object_uuid)
    print(f"   수정 후 조회수: {updated.properties['views']}")
    print("✅ 수정 완료!")


def replace_object(client: weaviate.WeaviateClient, object_uuid: str):
    """
    객체 전체 교체

    Args:
        client: Weaviate 클라이언트
        object_uuid: 교체할 객체의 UUID

    참고:
        - replace()는 모든 속성을 새 값으로 교체
        - 지정하지 않은 속성은 삭제됨!
    """
    print(f"\n🔄 객체 전체 교체: {object_uuid}")

    articles = client.collections.get("Article")

    # 새 데이터 (모든 필드 지정 필요!)
    new_data = {
        "title": "업데이트된 제목",
        "content": "완전히 새로운 내용입니다.",
        "author": "새로운작성자",
        "published_date": datetime.now().isoformat() + "Z",
        "views": 0,
        "tags": ["업데이트", "새로운"],
    }

    # 객체 교체
    articles.data.replace(uuid=object_uuid, properties=new_data)

    print("✅ 객체 교체 완료!")
    print(f"   새 제목: {new_data['title']}")


# ====================
# 5. DELETE - 객체 삭제
# ====================


def delete_single_object(client: weaviate.WeaviateClient, object_uuid: str):
    """
    단일 객체 삭제

    Args:
        client: Weaviate 클라이언트
        object_uuid: 삭제할 객체의 UUID
    """
    print(f"\n🗑️ 객체 삭제: {object_uuid}")

    articles = client.collections.get("Article")

    try:
        # 객체 삭제
        articles.data.delete_by_id(uuid=object_uuid)
        print("✅ 삭제 완료!")

    except Exception as e:
        print(f"❌ 삭제 실패: {e}")


def delete_multiple_objects(client: weaviate.WeaviateClient):
    """
    여러 객체 삭제 (조건부)

    참고:
        - Where 필터로 조건에 맞는 객체들을 삭제
        - 주의: 복구 불가능!
    """
    print("\n🗑️ 조건부 여러 객체 삭제...")

    from weaviate.classes.query import Filter

    articles = client.collections.get("Article")

    # 조회수가 0인 기사 삭제
    result = articles.data.delete_many(
        where=Filter.by_property("views").equal(0)
    )

    print(f"✅ {result.successful} 개의 객체 삭제 완료")
    if result.failed > 0:
        print(f"⚠️ {result.failed} 개 삭제 실패")


# ====================
# 6. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "🚀" * 25)
    print("Weaviate CRUD 작업 학습")
    print("🚀" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 0. 준비: 컬렉션 생성
            setup_collection(client)

            # 1. CREATE - 객체 생성
            print("\n" + "=" * 50)
            print("CREATE - 객체 생성")
            print("=" * 50)

            uuid1 = create_single_object(client)
            uuid2 = create_object_with_custom_uuid(client)
            uuid3 = create_object_with_vector(client)

            # 2. READ - 객체 조회
            print("\n" + "=" * 50)
            print("READ - 객체 조회")
            print("=" * 50)

            read_object_by_uuid(client, uuid1)
            read_all_objects(client, limit=5)
            read_objects_with_filter(client)

            # 3. UPDATE - 객체 수정
            print("\n" + "=" * 50)
            print("UPDATE - 객체 수정")
            print("=" * 50)

            update_object_properties(client, uuid1)
            # replace_object(client, uuid2)  # 주석 해제하면 전체 교체

            # 4. DELETE - 객체 삭제
            print("\n" + "=" * 50)
            print("DELETE - 객체 삭제")
            print("=" * 50)

            delete_single_object(client, uuid3)
            delete_multiple_objects(client)

            # 최종 확인
            print("\n" + "=" * 50)
            print("최종 객체 목록")
            print("=" * 50)
            read_all_objects(client)

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n📚 다음 학습:")
    print("   python 04_batch_operations.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. CREATE (생성)
   - insert(): 새 객체 생성
   - UUID 자동 생성 또는 수동 지정
   - 벡터 자동 또는 수동 제공

2. READ (조회)
   - fetch_object_by_id(): UUID로 조회
   - fetch_objects(): 여러 객체 조회
   - 필터링으로 조건부 조회

3. UPDATE (수정)
   - update(): 특정 속성만 수정
   - replace(): 객체 전체 교체

4. DELETE (삭제)
   - delete_by_id(): 단일 객체 삭제
   - delete_many(): 조건부 여러 객체 삭제

💡 실무 팁:
   - UUID는 generate_uuid5로 결정론적 생성
   - update() vs replace() 차이 이해
   - 삭제 전 항상 확인 (복구 불가!)
   - 배치 작업은 성능상 유리

⚠️ 주의사항:
   - replace()는 모든 속성 덮어씀
   - delete는 복구 불가능
   - UUID는 문자열로 변환 필요할 수 있음

🔧 연습 과제:
   1. 자신만의 데이터로 CRUD 수행
   2. 다양한 필터 조건 실험
   3. 에러 핸들링 추가
"""
