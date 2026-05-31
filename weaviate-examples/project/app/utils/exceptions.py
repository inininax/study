"""
커스텀 예외
===========

애플리케이션 전용 예외 클래스
"""

from fastapi import HTTPException


class AppException(HTTPException):
    """기본 애플리케이션 예외"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or "APP_ERROR"


class WeaviateException(AppException):
    """Weaviate 관련 예외"""

    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail, error_code="WEAVIATE_ERROR")


class DocumentNotFoundException(AppException):
    """문서를 찾을 수 없는 경우"""

    def __init__(self, doc_id: str):
        super().__init__(
            status_code=404,
            detail=f"문서를 찾을 수 없습니다: {doc_id}",
            error_code="DOCUMENT_NOT_FOUND",
        )


class ValidationException(AppException):
    """데이터 검증 실패"""

    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail, error_code="VALIDATION_ERROR")
