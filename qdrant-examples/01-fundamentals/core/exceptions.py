"""
커스텀 예외 클래스

프로덕션 환경에서의 세밀한 에러 핸들링을 위한 예외 정의
"""


class QdrantBaseException(Exception):
    """모든 Qdrant 관련 예외의 베이스 클래스"""

    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self):
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class QdrantConnectionError(QdrantBaseException):
    """Qdrant 서버 연결 실패"""
    pass


class QdrantTimeoutError(QdrantBaseException):
    """요청 타임아웃"""
    pass


class CollectionNotFoundError(QdrantBaseException):
    """컬렉션을 찾을 수 없음"""
    pass


class CollectionAlreadyExistsError(QdrantBaseException):
    """컬렉션이 이미 존재함"""
    pass


class VectorDimensionMismatchError(QdrantBaseException):
    """벡터 차원 불일치"""
    pass


class InvalidPayloadError(QdrantBaseException):
    """잘못된 페이로드"""
    pass


class PointNotFoundError(QdrantBaseException):
    """포인트를 찾을 수 없음"""
    pass


class BatchOperationError(QdrantBaseException):
    """배치 작업 실패"""
    pass
