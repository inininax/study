"""
RAG 서비스
==========

Retrieval Augmented Generation 구현
"""

from typing import List, Dict, Tuple
from openai import OpenAI

from app.config import settings
from app.services.weaviate_service import weaviate_service
from app.utils.logger import logger


class RAGService:
    """RAG (Retrieval Augmented Generation) 서비스"""

    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def answer_question(
        self, question: str, max_docs: int = 5, temperature: float = 0.7
    ) -> Tuple[str, List[Dict]]:
        """
        질문에 대한 답변 생성

        Args:
            question: 질문
            max_docs: 검색할 최대 문서 수
            temperature: LLM 온도

        Returns:
            Tuple[str, List[Dict]]: (답변, 참고 문서 목록)
        """
        try:
            # 1. 관련 문서 검색
            logger.info(f"질문: {question}")
            documents = weaviate_service.semantic_search(
                query=question, limit=max_docs, min_certainty=0.7
            )

            if not documents:
                return "관련 문서를 찾을 수 없습니다.", []

            # 2. 컨텍스트 생성
            context = self._build_context(documents)

            # 3. 프롬프트 생성
            prompt = self._build_prompt(question, context)

            # 4. LLM으로 답변 생성
            answer = self._generate_answer(prompt, temperature)

            logger.info(f"답변 생성 완료 ({len(documents)}개 문서 참고)")

            return answer, documents

        except Exception as e:
            logger.error(f"RAG 처리 실패: {e}")
            raise

    def _build_context(self, documents: List[Dict]) -> str:
        """
        문서들로부터 컨텍스트 생성

        Args:
            documents: 검색된 문서 목록

        Returns:
            str: 컨텍스트 문자열
        """
        context_parts = []

        for i, doc in enumerate(documents, 1):
            title = doc.get("title", "제목 없음")
            content = doc.get("content", "")

            # 컨텐츠가 너무 길면 앞부분만 사용
            if len(content) > 1000:
                content = content[:1000] + "..."

            context_parts.append(f"[문서 {i}: {title}]\n{content}\n")

        return "\n".join(context_parts)

    def _build_prompt(self, question: str, context: str) -> str:
        """
        LLM 프롬프트 생성

        Args:
            question: 질문
            context: 컨텍스트

        Returns:
            str: 프롬프트
        """
        prompt = f"""다음 문서들을 참고하여 질문에 답변해주세요.

참고 문서:
{context}

질문: {question}

답변 작성 규칙:
1. 참고 문서의 정보만을 사용하여 답변하세요
2. 문서에 없는 정보는 추측하지 마세요
3. 명확하고 간결하게 답변하세요
4. 한국어로 답변하세요
5. 답변 끝에 "참고 문서: [문서 번호]"를 명시하세요

답변:"""

        return prompt

    def _generate_answer(self, prompt: str, temperature: float) -> str:
        """
        LLM으로 답변 생성

        Args:
            prompt: 프롬프트
            temperature: 온도 설정

        Returns:
            str: 생성된 답변
        """
        try:
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 문서 기반 질문 답변 전문가입니다. 제공된 문서의 정보만을 사용하여 정확하게 답변합니다.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=500,
            )

            answer = response.choices[0].message.content.strip()
            return answer

        except Exception as e:
            logger.error(f"LLM 답변 생성 실패: {e}")
            raise


# 전역 RAG 서비스 인스턴스
rag_service = RAGService()
