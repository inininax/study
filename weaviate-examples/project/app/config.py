"""
애플리케이션 설정
==================

환경 변수를 안전하게 관리하고 설정을 중앙화합니다.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스

    참고:
        - .env 파일에서 자동으로 값을 로드합니다
        - 타입 검증 자동 수행
        - 환경별 설정 관리 가능
    """

    # 애플리케이션 기본 설정
    APP_NAME: str = "Weaviate Document Search API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = Field(default="development", env="APP_ENV")
    DEBUG: bool = Field(default=True, env="DEBUG")

    # 서버 설정
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")

    # Weaviate 설정
    WEAVIATE_URL: str = Field(default="http://localhost:8080", env="WEAVIATE_URL")
    WEAVIATE_API_KEY: Optional[str] = Field(default=None, env="WEAVIATE_API_KEY")

    # OpenAI 설정
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")  # 필수 값
    OPENAI_EMBEDDING_MODEL: str = Field(
        default="text-embedding-3-small", env="OPENAI_EMBEDDING_MODEL"
    )
    OPENAI_LLM_MODEL: str = Field(default="gpt-4o-mini", env="OPENAI_LLM_MODEL")

    # JWT 인증 설정
    JWT_SECRET_KEY: str = Field(
        default="your-super-secret-key-change-in-production",
        env="JWT_SECRET_KEY",
    )
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # 로깅 설정
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: Optional[str] = Field(default="app.log", env="LOG_FILE")

    # CORS 설정
    CORS_ORIGINS: list = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ORIGINS",
    )

    # 페이지네이션 설정
    DEFAULT_PAGE_SIZE: int = Field(default=20, env="DEFAULT_PAGE_SIZE")
    MAX_PAGE_SIZE: int = Field(default=100, env="MAX_PAGE_SIZE")

    # RAG 설정
    RAG_MAX_CONTEXT_DOCUMENTS: int = Field(default=5, env="RAG_MAX_CONTEXT_DOCUMENTS")
    RAG_TEMPERATURE: float = Field(default=0.7, env="RAG_TEMPERATURE")

    class Config:
        """Pydantic 설정"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 전역 설정 인스턴스
settings = Settings()


def get_settings() -> Settings:
    """
    설정 객체 반환 (Dependency Injection용)

    Returns:
        Settings: 설정 객체

    사용 예:
        @app.get("/")
        def root(settings: Settings = Depends(get_settings)):
            return {"app": settings.APP_NAME}
    """
    return settings


# 개발 환경 확인
def is_development() -> bool:
    """개발 환경 여부 반환"""
    return settings.APP_ENV == "development"


def is_production() -> bool:
    """프로덕션 환경 여부 반환"""
    return settings.APP_ENV == "production"


# 설정 검증
def validate_settings():
    """
    필수 설정 검증

    Raises:
        ValueError: 필수 설정이 누락된 경우
    """
    # OpenAI API 키 검증
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
        raise ValueError(
            "OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."
        )

    # 프로덕션 환경에서 보안 설정 검증
    if is_production():
        if settings.JWT_SECRET_KEY == "your-super-secret-key-change-in-production":
            raise ValueError("프로덕션 환경에서는 JWT_SECRET_KEY를 변경해야 합니다.")

        if settings.DEBUG:
            raise ValueError("프로덕션 환경에서는 DEBUG를 False로 설정해야 합니다.")

    print("✅ 설정 검증 완료")


# 설정 정보 출력 (디버깅용)
def print_settings():
    """현재 설정 정보 출력 (민감한 정보는 마스킹)"""
    print("\n" + "=" * 60)
    print("애플리케이션 설정")
    print("=" * 60)
    print(f"앱 이름: {settings.APP_NAME}")
    print(f"버전: {settings.APP_VERSION}")
    print(f"환경: {settings.APP_ENV}")
    print(f"디버그 모드: {settings.DEBUG}")
    print(f"\nWeaviate URL: {settings.WEAVIATE_URL}")
    print(f"OpenAI 모델: {settings.OPENAI_LLM_MODEL}")
    print(f"임베딩 모델: {settings.OPENAI_EMBEDDING_MODEL}")
    print(f"\nJWT 만료 시간: {settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES}분")
    print(f"로그 레벨: {settings.LOG_LEVEL}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # 설정 테스트
    try:
        validate_settings()
        print_settings()
    except ValueError as e:
        print(f"❌ 설정 에러: {e}")
