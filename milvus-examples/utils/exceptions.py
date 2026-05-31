"""
Custom exceptions for Milvus operations.
Provides structured error handling with proper error codes and messages.
"""


class MilvusBaseException(Exception):
    """Base exception for all Milvus-related errors."""

    def __init__(self, message: str, error_code: str = "UNKNOWN", details: dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Convert exception to dictionary for JSON serialization."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class MilvusConnectionError(MilvusBaseException):
    """Raised when connection to Milvus fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, error_code="MILVUS_CONNECTION_ERROR", details=details)


class MilvusOperationError(MilvusBaseException):
    """Raised when a Milvus operation fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, error_code="MILVUS_OPERATION_ERROR", details=details)


class MilvusValidationError(MilvusBaseException):
    """Raised when validation fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, error_code="MILVUS_VALIDATION_ERROR", details=details)


class MilvusTimeoutError(MilvusBaseException):
    """Raised when an operation times out."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, error_code="MILVUS_TIMEOUT_ERROR", details=details)


class MilvusResourceExhaustedError(MilvusBaseException):
    """Raised when resources are exhausted."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, error_code="MILVUS_RESOURCE_EXHAUSTED", details=details)
