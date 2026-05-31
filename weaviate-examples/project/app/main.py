"""
FastAPI 메인 애플리케이션
=========================

프로덕션 레벨의 Weaviate 기반 문서 검색 API
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from app.config import settings, validate_settings, print_settings
from app.utils.logger import setup_logger, logger
from app.utils.exceptions import AppException


# ====================
# 애플리케이션 라이프사이클
# ====================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 시작/종료 시 실행되는 로직

    참고:
        - startup: 애플리케이션 시작 시
        - shutdown: 애플리케이션 종료 시
    """
    # Startup
    logger.info("🚀 애플리케이션 시작")

    try:
        # 설정 검증
        validate_settings()
        print_settings()

        # 로거 설정
        setup_logger()

        # Weaviate 연결 테스트
        from app.services.weaviate_service import weaviate_service

        weaviate_service.initialize()
        logger.info("✅ Weaviate 연결 성공")

    except Exception as e:
        logger.error(f"❌ 초기화 실패: {e}")
        raise

    yield  # 애플리케이션 실행

    # Shutdown
    logger.info("👋 애플리케이션 종료")


# ====================
# FastAPI 앱 생성
# ====================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Weaviate 기반 지능형 문서 검색 시스템",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    lifespan=lifespan,
)


# ====================
# 미들웨어 설정
# ====================

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ====================
# 예외 핸들러
# ====================


@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    """커스텀 예외 핸들러"""
    logger.error(f"AppException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": exc.error_code},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """전역 예외 핸들러"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500, content={"detail": "내부 서버 오류가 발생했습니다."}
    )


# ====================
# 기본 라우트
# ====================


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    from app.services.weaviate_service import weaviate_service

    try:
        is_ready = weaviate_service.health_check()
        return {"status": "healthy" if is_ready else "unhealthy", "weaviate": is_ready}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.get("/info")
async def app_info():
    """애플리케이션 정보"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG,
        "weaviate_url": settings.WEAVIATE_URL,
    }


# ====================
# API 라우터 등록
# ====================

# 라우터를 동적으로 import하여 순환 참조 방지
from app.api import documents, search

app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])


# ====================
# 개발 서버 실행
# ====================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
