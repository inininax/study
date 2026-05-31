"""
문서 API 라우터
===============

문서 CRUD 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from uuid import UUID

from app.models.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
)
from app.services.weaviate_service import weaviate_service
from app.utils.logger import logger


router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def create_document(document: DocumentCreate):
    """
    문서 생성

    - **title**: 문서 제목
    - **content**: 문서 내용
    - **tags**: 태그 목록 (선택)
    """
    try:
        doc_id = weaviate_service.create_document(
            title=document.title,
            content=document.content,
            tags=document.tags,
            metadata=document.metadata,
        )

        return {"id": str(doc_id), "message": "문서가 생성되었습니다"}

    except Exception as e:
        logger.error(f"문서 생성 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[dict])
async def list_documents(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    문서 목록 조회

    - **limit**: 조회할 문서 수 (기본: 20)
    - **offset**: 시작 위치 (기본: 0)
    """
    try:
        documents = weaviate_service.list_documents(limit=limit, offset=offset)
        return documents

    except Exception as e:
        logger.error(f"문서 목록 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{doc_id}", response_model=dict)
async def get_document(doc_id: UUID):
    """
    문서 조회

    - **doc_id**: 문서 UUID
    """
    try:
        document = weaviate_service.get_document(doc_id)

        if not document:
            raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")

        return document

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"문서 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{doc_id}", response_model=dict)
async def update_document(doc_id: UUID, document: DocumentUpdate):
    """
    문서 수정

    - **doc_id**: 문서 UUID
    - **title**: 새 제목 (선택)
    - **content**: 새 내용 (선택)
    - **tags**: 새 태그 (선택)
    """
    try:
        # 문서 존재 확인
        existing = weaviate_service.get_document(doc_id)
        if not existing:
            raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")

        # 수정
        weaviate_service.update_document(
            doc_id=doc_id,
            title=document.title,
            content=document.content,
            tags=document.tags,
        )

        return {"id": str(doc_id), "message": "문서가 수정되었습니다"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"문서 수정 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{doc_id}", response_model=dict)
async def delete_document(doc_id: UUID):
    """
    문서 삭제

    - **doc_id**: 문서 UUID
    """
    try:
        # 문서 존재 확인
        existing = weaviate_service.get_document(doc_id)
        if not existing:
            raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")

        # 삭제
        weaviate_service.delete_document(doc_id)

        return {"id": str(doc_id), "message": "문서가 삭제되었습니다"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"문서 삭제 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))
