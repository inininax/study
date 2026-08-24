"""
RAG 구현 (Retrieval Augmented Generation)
==========================================

이 모듈에서 배울 내용:
1. RAG 개념: 검색(Retrieval) + 증강(Augmentation) + 생성(Generation)
2. 지식베이스 구축: 문서 벡터화
3. 검색 단계: 질문과 유사한 문서 찾기
4. 프롬프트 작성: 컨텍스트 + 질문 결합
5. LLM 답변 생성: OpenAI 사용 (키가 없으면 모의 응답)

난이도: ⭐⭐⭐⭐ (높음)
소요 시간: 2시간

💡 API 키 없이 실행 가능!
   - OPENAI_API_KEY 환경 변수가 있으면 실제 LLM 답변 생성
   - 없으면 검색 결과를 요약하는 '모의 응답'으로 전체 흐름 학습
"""

import os
from typing import List, Dict, Optional

from dotenv import load_dotenv
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery


# ====================
# 0. 환경 변수 로드
# ====================

# .env 파일에서 환경 변수 로드 (OPENAI_API_KEY 등)
load_dotenv()


# ====================
# 1. 준비: 지식베이스 구축
# ====================


def setup_knowledge_base(client: weaviate.WeaviateClient):
    """
    RAG용 지식베이스 컬렉션 생성 및 문서 삽입

    참고:
        - 실제 서비스라면 사내 위키, 매뉴얼, FAQ 등이 될 것
        - 여기선 Weaviate 관련 지식 문서 몇 개를 사용
        - text2vec-openai로 문서가 자동 벡터화됨 (서버 측에서 처리)
    """
    print("📚 지식베이스 컬렉션 설정...")

    if client.collections.exists("KBDoc"):
        client.collections.delete("KBDoc")

    client.collections.create(
        name="KBDoc",
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="content", data_type=DataType.TEXT),
            Property(name="category", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_openai(
            model="text-embedding-3-small"
        ),
    )

    docs = [
        {
            "title": "Weaviate란 무엇인가?",
            "content": (
                "Weaviate는 오픈소스 벡터 데이터베이스입니다. 텍스트, 이미지 등을 "
                "벡터(임베딩)로 저장하고 유사도 기반 검색을 제공합니다. "
                "모듈 시스템을 통해 다양한 벡터화 모델을 사용할 수 있으며, "
                "GraphQL과 gRPC API를 지원합니다."
            ),
            "category": "기초",
        },
        {
            "title": "하이브리드 검색의 이해",
            "content": (
                "하이브리드 검색은 BM25 키워드 검색과 벡터 의미 검색을 결합한 방식입니다. "
                "알파 파라미터로 두 방식의 비중을 조절할 수 있습니다. "
                "alpha가 0에 가까울수록 키워드, 1에 가까울수록 벡터 검색의 영향이 커집니다. "
                "기본값은 0.5이며 상대 점수 융합 방식을 사용합니다."
            ),
            "category": "검색",
        },
        {
            "title": "멀티테넌시 아키텍처",
            "content": (
                "멀티테넌시는 하나의 Weaviate 인스턴스에서 여러 고객(테넌트)의 데이터를 "
                "격리해서 관리하는 기능입니다. 각 테넌트는 독립된 샤드로 저장되며 "
                "테넌트 단위 활성화/비활성화로 리소스를 절약할 수 있습니다. "
                "SaaS 서비스 설계에 필수적인 패턴입니다."
            ),
            "category": "아키텍처",
        },
        {
            "title": "HNSW 알고리즘 소개",
            "content": (
                "HNSW(Hierarchical Navigable Small World)는 Weaviate의 기본 벡터 인덱스입니다. "
                "계층적 그래프 구조로 근사 최근접 이웃 검색을 수행합니다. "
                "ef_construction은 색인 품질, max_connections는 그래프 연결 밀도를 결정합니다. "
                "파라미터가 클수록 정확하지만 느려지고 메모리를 더 사용합니다."
            ),
            "category": "성능",
        },
        {
            "title": "RAG 패턴의 핵심",
            "content": (
                "RAG(Retrieval Augmented Generation)는 LLM에게 답변 전에 관련 문서를 검색해 "
                "컨텍스트로 제공하는 패턴입니다. 환각(hallucination)을 줄이고 최신 정보를 "
                "반영할 수 있습니다. 검색 품질이 답변 품질을 좌우하므로 하이브리드 검색과 "
                "필터링을 함께 사용하는 것이 좋습니다."
            ),
            "category": "AI",
        },
        {
            "title": "백업과 복구 전략",
            "content": (
                "Weaviate는 백업 모듈(filesystem, s3, gcs, azure)을 제공합니다. "
                "백업은 컬렉션 단위로 수행되며 backup_id로 관리됩니다. "
                "복원 시에는 같은 이름의 컬렉션이 존재하면 안 됩니다. "
                "정기적인 백업 스케줄과 복원 리허설이 운영의 기본입니다."
            ),
            "category": "운영",
        },
    ]

    collection = client.collections.get("KBDoc")

    # generate_uuid5로 결정적 UUID 사용 → 재실행해도 동일한 ID
    from weaviate.util import generate_uuid5

    with collection.batch.dynamic() as batch:
        for doc in docs:
            batch.add_object(
                properties=doc,
                uuid=generate_uuid5(doc["title"]),
            )

    print(f"✅ {len(docs)}개의 지식 문서 추가 완료\n")
    return len(docs)


# ====================
# 2. 검색 단계 (Retrieval)
# ====================


def retrieve_documents(
    client: weaviate.WeaviateClient, question: str, top_k: int = 3
) -> List[Dict]:
    """
    질문과 관련된 문서를 검색한다 (RAG의 첫 단계!)

    Args:
        question: 사용자 질문
        top_k: 가져올 문서 개수

    Returns:
        List[Dict]: [{"title", "content", "category", "distance"}] 형태의 문서 목록

    참고:
        - 검색 품질이 곧 RAG 품질! near_text 대신 hybrid를 쓰면 더 견고해짐
        - category 필터를 추가하면 특정 주제 안에서만 검색 가능
    """
    print(f"\n🔍 [검색 단계] '{question}' 관련 문서 조회...")

    collection = client.collections.get("KBDoc")

    response = collection.query.near_text(
        query=question,
        limit=top_k,
        return_metadata=MetadataQuery(distance=True),
    )

    results = []
    for obj in response.objects:
        distance = obj.metadata.distance if obj.metadata else 1.0
        results.append(
            {
                "title": obj.properties["title"],
                "content": obj.properties["content"],
                "category": obj.properties["category"],
                "distance": distance,
            }
        )

    for i, doc in enumerate(results, 1):
        print(f"   {i}. [{doc['category']}] {doc['title']} (거리: {doc['distance']:.4f})")

    return results


def build_context(docs: List[Dict]) -> str:
    """
    검색된 문서들을 LLM 프롬프트에 넣을 컨텍스트 문자열로 변환

    참고:
        - 문서 경계가 명확하도록 번호와 출처(제목)를 붙임
        - 너무 긴 컨텍스트는 비용/성능 문제 → top_k 조절 필요
    """
    context_parts = []
    for i, doc in enumerate(docs, 1):
        context_parts.append(f"[문서 {i}] ({doc['category']}) {doc['title']}\n{doc['content']}")

    return "\n\n".join(context_parts)


# ====================
# 3. 생성 단계 (Generation)
# ====================


def build_prompt(question: str, context: str) -> str:
    """컨텍스트와 질문을 결합한 프롬프트 작성"""
    return f"""당신은 Weaviate 벡터 데이터베이스 전문 상담 AI입니다.
아래 제공된 문서 내용만 근거로 한국어로 답변하세요.
문서에 없는 내용은 추측하지 말고 "제공된 문서에는 해당 정보가 없습니다"라고 답하세요.

<문서>
{context}
</문서>

<질문>
{question}
</질문>

<답변 형식>
- 핵심을 먼저 한 문장으로 요약
- 필요하면 항목별 설명
"""



def generate_answer_with_openai(prompt: str) -> Optional[str]:
    """
    OpenAI API로 답변 생성 (API 키가 있을 때만 호출)

    Returns:
        성공 시 답변 문자열, 실패/미설정 시 None
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("your_"):
        return None

    try:
        # lazy import: openai 미설치/키 미설정 환경에서도 모듈 임포트 가능
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # 사실 기반 답변이므로 낮게
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ OpenAI 호출 실패: {e}")
        return None


def generate_answer_mock(question: str, docs: List[Dict]) -> str:
    """
    모의 응답 생성 (API 키가 없을 때)

    참고:
        - 검색된 문서의 앞부분을 추출해 답변처럼 조립 (추출적 요약)
        - RAG 파이프라인의 '구조'를 학습하기 위한 용도
    """
    lines = ["🧪 [모의 응답 모드 - OPENAI_API_KEY 미설정]", ""]
    lines.append(f"질문 '{question}'에 대해 검색된 문서 근거:")
    for i, doc in enumerate(docs[:2], 1):
        summary = doc["content"][:80].replace("\n", " ")
        lines.append(f"  {i}. [{doc['title']}] {summary}...")
    lines.append("")
    lines.append("💡 OPENAI_API_KEY를 설정하면 이 자리에 LLM 답변이 생성됩니다.")
    return "\n".join(lines)


# ====================
# 4. 전체 RAG 파이프라인
# ====================


def rag_pipeline(client: weaviate.WeaviateClient, question: str):
    """
    RAG 전체 흐름 실행

        질문 → 검색(Retrieval) → 컨텍스트 증강(Augmentation) → 답변 생성(Generation)

    참고:
        - 검색과 생성이 분리되어 있어 각 단계를 독립적으로 개선/테스트 가능
        - 프로덕션에서는 각 단계에 로깅·평가를 붙임
    """
    print("\n" + "=" * 60)
    print(f"💬 질문: {question}")
    print("=" * 60)

    # 1단계: 검색
    docs = retrieve_documents(client, question, top_k=2)

    # 2단계: 컨텍스트 빌드 + 프롬프트 작성
    context = build_context(docs)
    prompt = build_prompt(question, context)

    # 3단계: 생성
    answer = generate_answer_with_openai(prompt)
    if answer is None:
        answer = generate_answer_mock(question, docs)

    print("\n🤖 [생성 단계] 답변:")
    print("-" * 60)
    print(answer)
    print("-" * 60)


# ====================
# 5. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "🤖" * 25)
    print("RAG 구현 (Retrieval Augmented Generation) 학습")
    print("🤖" * 25)

    has_key = bool(os.getenv("OPENAI_API_KEY")) and not os.getenv(
        "OPENAI_API_KEY", ""
    ).startswith("your_")
    mode = "실제 LLM 모드" if has_key else "모의 응답 모드 (API 키 없음)"
    print(f"\n📌 현재 모드: {mode}")

    try:
        with weaviate.connect_to_local() as client:
            # 1. 지식베이스 구축
            setup_knowledge_base(client)

            # 2. RAG 파이프라인 실행
            questions = [
                "하이브리드 검색에서 알파 값은 무엇을 조절하나요?",
                "멀티테넌시는 왜 필요한가요?",
                "HNSW 파라미터를 올리면 어떻게 되나요?",
            ]
            for q in questions:
                rag_pipeline(client, q)

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n💡 핵심 정리:")
    print("   - RAG = 검색 + 컨텍스트 증강 + 생성")
    print("   - 검색 품질이 답변 품질을 결정 (hybrid/filters 활용)")
    print("   - 검색 단계와 생성 단계를 분리해 테스트 가능하게!")
    print("   - 프롬프트에서 '문서 근거만 답하라'고 제한하면 환각 감소")

    print("\n📚 다음 학습:")
    print("   python 02_multi_tenancy.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. RAG 파이프라인 구성요소
   - Retrieval: near_text/hybrid/bm25로 관련 문서 검색
   - Augmentation: 검색 결과를 프롬프트 컨텍스트로 조립
   - Generation: LLM이 컨텍스트 근거로 답변 생성

2. 검색 품질 개선 포인트
   - near_text → hybrid 전환 (키워드+의미)
   - filters로 검색 범위 제한 (카테고리/권한)
   - top_k 조절 (너무 많으면 노이즈, 적으면 부족)
   - metadata.distance로 관련도 낮으면 '모른다'고 답하게 처리

3. 프로덕션 확장 아이디어
   - Weaviate 네이티브 생성: collection.generate.near_text(single_prompt=...)
     (generative-openai 모듈이 서버에서 활성화되어 있어야 함)
   - 스트리밍 응답, 대화 히스토리 관리
   - Reranker 모듈로 검색 후 재정렬

⚠️ 주의사항:
   - 컨텍스트가 길수록 비용 증가 → 문서 청크 크기 설계 중요
   - temperature를 낮게(0~0.3): 사실 기반 답변에 적합
   - API 키는 절대 코드에 하드코딩 금지 (환경 변수 사용)

🔧 연습 과제:
   1. hybrid 검색으로 retrieve_documents 개선해보기
   2. category 필터를 파라미터로 받아보기
   3. 자신의 도메인 문서로 지식베이스 교체하기
"""
