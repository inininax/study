"""
Weaviate 스키마 관리
===================

이 모듈에서 배울 내용:
1. 컬렉션(클래스) 생성
2. 속성(Properties) 정의
3. 벡터화 설정
4. 스키마 조회 및 삭제

난이도: ⭐⭐ (쉬움)
소요 시간: 1시간
"""

import weaviate
from weaviate.classes.config import (
    Configure,
    Property,
    DataType,
    VectorDistances,
)
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()


# ====================
# 1. 스키마의 개념
# ====================

"""
스키마란?
- 데이터의 구조를 정의하는 청사진
- SQL의 CREATE TABLE과 유사
- 어떤 속성(필드)을 가질지 정의

예시:
    Article 스키마
    - title (문자열)
    - content (문자열)
    - published (날짜)
    - views (숫자)
"""


# ====================
# 2. 기본 컬렉션 생성
# ====================


def create_simple_collection(client: weaviate.WeaviateClient):
    """
    가장 간단한 컬렉션 생성

    Args:
        client: Weaviate 클라이언트

    참고:
        - 최소한의 설정으로 컬렉션 생성
        - 자동 벡터화 비활성화 (수동 벡터 제공 필요)
    """
    print("\n📦 간단한 컬렉션 생성...")

    # 기존 컬렉션이 있다면 삭제
    if client.collections.exists("SimpleArticle"):
        client.collections.delete("SimpleArticle")
        print("   기존 컬렉션 삭제됨")

    # 컬렉션 생성
    collection = client.collections.create(
        name="SimpleArticle",  # 컬렉션 이름 (대문자로 시작 권장)
        # 속성 정의
        properties=[
            # Property: 각 속성(필드)을 정의
            Property(
                name="title",  # 속성 이름
                data_type=DataType.TEXT,  # 데이터 타입
                description="기사 제목",  # 설명 (선택사항)
            ),
            Property(
                name="content",
                data_type=DataType.TEXT,
                description="기사 본문",
            ),
        ],
    )

    print("✅ SimpleArticle 컬렉션 생성 완료")
    return collection


def create_collection_with_vectorizer(client: weaviate.WeaviateClient):
    """
    벡터화 설정이 포함된 컬렉션 생성

    참고:
        - OpenAI를 사용하여 자동으로 텍스트를 벡터로 변환
        - OPENAI_API_KEY 환경 변수 필요
    """
    print("\n🤖 자동 벡터화 컬렉션 생성...")

    # 기존 컬렉션 삭제
    if client.collections.exists("Article"):
        client.collections.delete("Article")
        print("   기존 컬렉션 삭제됨")

    # OpenAI 벡터화 설정
    collection = client.collections.create(
        name="Article",
        description="뉴스 기사 컬렉션",
        # 속성 정의
        properties=[
            Property(
                name="title",
                data_type=DataType.TEXT,
                description="기사 제목",
                # 이 필드는 벡터화에 포함됨 (기본값)
            ),
            Property(
                name="content",
                data_type=DataType.TEXT,
                description="기사 본문",
            ),
            Property(
                name="author",
                data_type=DataType.TEXT,
                description="작성자",
                # skip_vectorization=True,  # 벡터화에서 제외하고 싶다면
            ),
            Property(
                name="published_date",
                data_type=DataType.DATE,
                description="발행일",
            ),
            Property(
                name="views",
                data_type=DataType.INT,
                description="조회수",
            ),
            Property(
                name="is_featured",
                data_type=DataType.BOOL,
                description="추천 기사 여부",
            ),
        ],
        # 벡터화 설정
        vectorizer_config=Configure.Vectorizer.text2vec_openai(
            model="text-embedding-3-small",  # OpenAI 임베딩 모델
            # vectorize_collection_name=False,  # 컬렉션 이름 벡터화 제외
        ),
        # 벡터 인덱스 설정
        vector_index_config=Configure.VectorIndex.hnsw(
            distance_metric=VectorDistances.COSINE,  # 유사도 측정 방식
            # ef: 검색 품질 (높을수록 정확하지만 느림)
            # max_connections: 각 노드의 최대 연결 수
        ),
    )

    print("✅ Article 컬렉션 생성 완료")
    print("   - 자동 벡터화: OpenAI text-embedding-3-small")
    print("   - 유사도 측정: Cosine")
    return collection


def create_collection_with_multiple_vectors(client: weaviate.WeaviateClient):
    """
    다중 벡터 설정 (고급)

    참고:
        - 하나의 객체가 여러 벡터를 가질 수 있음
        - 예: 제목 벡터, 본문 벡터를 따로 관리
    """
    print("\n🔀 다중 벡터 컬렉션 생성...")

    if client.collections.exists("MultiVectorArticle"):
        client.collections.delete("MultiVectorArticle")

    collection = client.collections.create(
        name="MultiVectorArticle",
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="content", data_type=DataType.TEXT),
        ],
        # 다중 벡터 설정
        vectorizer_config=[
            # 제목용 벡터
            Configure.NamedVectors.text2vec_openai(
                name="title_vector",
                source_properties=["title"],  # title만 벡터화
                model="text-embedding-3-small",
            ),
            # 본문용 벡터
            Configure.NamedVectors.text2vec_openai(
                name="content_vector",
                source_properties=["content"],  # content만 벡터화
                model="text-embedding-3-small",
            ),
        ],
    )

    print("✅ MultiVectorArticle 컬렉션 생성 완료")
    print("   - title_vector: 제목 벡터화")
    print("   - content_vector: 본문 벡터화")
    return collection


# ====================
# 3. 스키마 조회
# ====================


def list_all_collections(client: weaviate.WeaviateClient):
    """
    모든 컬렉션 목록 조회

    Returns:
        List[str]: 컬렉션 이름 리스트
    """
    print("\n📋 모든 컬렉션 조회...")

    # 모든 컬렉션 가져오기
    collections = client.collections.list_all()

    print(f"   총 {len(collections)} 개의 컬렉션:")
    for name in collections:
        print(f"   - {name}")

    return collections


def get_collection_schema(client: weaviate.WeaviateClient, collection_name: str):
    """
    특정 컬렉션의 스키마 상세 조회

    Args:
        client: Weaviate 클라이언트
        collection_name: 조회할 컬렉션 이름
    """
    print(f"\n🔍 {collection_name} 스키마 조회...")

    # 컬렉션 가져오기
    collection = client.collections.get(collection_name)

    # 설정 정보 조회
    config = collection.config.get()

    print(f"\n📦 컬렉션: {config.name}")
    print(f"   설명: {config.description or 'N/A'}")

    print("\n📋 속성 목록:")
    for prop in config.properties:
        print(f"   - {prop.name}")
        print(f"     타입: {prop.data_type}")
        print(f"     설명: {prop.description or 'N/A'}")

    # 벡터화 설정 확인
    if config.vectorizer_config:
        print(f"\n🤖 벡터화: {config.vectorizer_config}")

    return config


# ====================
# 4. 스키마 수정 및 삭제
# ====================


def update_collection_description(
    client: weaviate.WeaviateClient, collection_name: str, new_description: str
):
    """
    컬렉션 설명 수정

    Args:
        client: Weaviate 클라이언트
        collection_name: 수정할 컬렉션 이름
        new_description: 새로운 설명
    """
    print(f"\n✏️ {collection_name} 설명 수정...")

    collection = client.collections.get(collection_name)

    # 설명 업데이트
    collection.config.update(description=new_description)

    print(f"✅ 설명 업데이트 완료: {new_description}")


def delete_collection(client: weaviate.WeaviateClient, collection_name: str):
    """
    컬렉션 삭제

    Args:
        client: Weaviate 클라이언트
        collection_name: 삭제할 컬렉션 이름

    주의:
        - 컬렉션을 삭제하면 모든 데이터도 삭제됩니다!
        - 복구 불가능하므로 주의해서 사용하세요
    """
    print(f"\n🗑️ {collection_name} 삭제...")

    if client.collections.exists(collection_name):
        client.collections.delete(collection_name)
        print(f"✅ {collection_name} 삭제 완료")
    else:
        print(f"⚠️ {collection_name}이(가) 존재하지 않습니다")


# ====================
# 5. 실전 예제: 복합 스키마
# ====================


def create_ecommerce_schema(client: weaviate.WeaviateClient):
    """
    실전 예제: 이커머스 제품 스키마

    참고:
        - 실무에서 사용할 만한 복잡한 스키마
        - 다양한 데이터 타입 활용
    """
    print("\n🛍️ 이커머스 제품 스키마 생성...")

    # 기존 컬렉션 삭제
    if client.collections.exists("Product"):
        client.collections.delete("Product")

    collection = client.collections.create(
        name="Product",
        description="이커머스 제품 정보",
        properties=[
            # 기본 정보
            Property(name="name", data_type=DataType.TEXT, description="제품명"),
            Property(
                name="description", data_type=DataType.TEXT, description="제품 설명"
            ),
            Property(name="sku", data_type=DataType.TEXT, description="제품 코드"),
            # 가격 정보
            Property(name="price", data_type=DataType.NUMBER, description="가격"),
            Property(name="currency", data_type=DataType.TEXT, description="통화"),
            Property(
                name="discount_rate", data_type=DataType.NUMBER, description="할인율"
            ),
            # 재고 정보
            Property(name="stock_quantity", data_type=DataType.INT, description="재고"),
            Property(
                name="in_stock", data_type=DataType.BOOL, description="재고 여부"
            ),
            # 카테고리
            Property(
                name="category",
                data_type=DataType.TEXT_ARRAY,  # 여러 카테고리 가능
                description="카테고리",
            ),
            Property(name="brand", data_type=DataType.TEXT, description="브랜드"),
            # 메타데이터
            Property(
                name="created_at", data_type=DataType.DATE, description="생성일"
            ),
            Property(
                name="updated_at", data_type=DataType.DATE, description="수정일"
            ),
            # 통계
            Property(name="views", data_type=DataType.INT, description="조회수"),
            Property(name="sales", data_type=DataType.INT, description="판매량"),
            Property(
                name="rating", data_type=DataType.NUMBER, description="평점 (0-5)"
            ),
        ],
        # 자동 벡터화: 이름과 설명만 벡터화
        vectorizer_config=Configure.Vectorizer.text2vec_openai(
            model="text-embedding-3-small",
            vectorize_collection_name=False,
        ),
    )

    print("✅ Product 컬렉션 생성 완료")
    print("   속성: 이름, 설명, SKU, 가격, 재고, 카테고리 등")
    return collection


# ====================
# 6. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "🚀" * 25)
    print("Weaviate 스키마 관리 학습")
    print("🚀" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 1. 간단한 컬렉션
            create_simple_collection(client)

            # 2. 자동 벡터화 컬렉션
            create_collection_with_vectorizer(client)

            # 3. 다중 벡터 컬렉션
            create_collection_with_multiple_vectors(client)

            # 4. 모든 컬렉션 조회
            list_all_collections(client)

            # 5. 특정 컬렉션 스키마 조회
            get_collection_schema(client, "Article")

            # 6. 설명 수정
            update_collection_description(
                client, "Article", "AI 및 기술 관련 뉴스 기사"
            )

            # 7. 실전 예제: 이커머스 스키마
            create_ecommerce_schema(client)

            # 8. 최종 컬렉션 목록
            print("\n" + "=" * 50)
            list_all_collections(client)

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        print("\n💡 해결 방법:")
        print("   1. OPENAI_API_KEY 환경 변수 확인")
        print("   2. Weaviate가 실행 중인지 확인")

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n📚 다음 학습:")
    print("   python 03_crud.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. 컬렉션 생성
   - collections.create(): 새 컬렉션 생성
   - Property: 속성 정의
   - DataType: 데이터 타입 지정

2. 데이터 타입
   - TEXT: 문자열
   - TEXT_ARRAY: 문자열 배열
   - INT: 정수
   - NUMBER: 실수
   - BOOL: 불리언
   - DATE: 날짜/시간

3. 벡터화 설정
   - text2vec_openai: OpenAI 임베딩
   - NamedVectors: 다중 벡터 설정
   - source_properties: 벡터화할 속성 지정

4. 스키마 관리
   - list_all(): 모든 컬렉션 조회
   - get(): 특정 컬렉션 조회
   - update(): 스키마 수정
   - delete(): 컬렉션 삭제

💡 실무 팁:
   - 컬렉션 이름은 대문자로 시작 (PascalCase)
   - 속성 이름은 소문자로 시작 (snake_case)
   - 설명(description) 작성으로 문서화
   - 벡터화가 필요한 필드만 선택

⚠️ 주의사항:
   - 컬렉션 삭제시 데이터도 모두 삭제됨
   - 스키마 변경시 기존 데이터 영향 고려
   - OPENAI_API_KEY 필요 (자동 벡터화)

🔧 연습 과제:
   1. 자신만의 컬렉션 만들어보기
   2. 다양한 데이터 타입 실험
   3. 벡터화 설정 변경해보기
"""
