"""
프로덕션 수준의 FastAPI 애플리케이션

벡터 검색 REST API 서버
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import time
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="Qdrant Vector Search API",
    description="프로덕션 수준의 벡터 검색 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 미들웨어: 요청 로깅
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """모든 요청 로깅"""
    start_time = time.time()

    # 요청 처리
    response = await call_next(request)

    # 소요 시간 계산
    process_time = time.time() - start_time

    # 로그
    logger.info(
        f"{request.method} {request.url.path} "
        f"- {response.status_code} "
        f"- {process_time:.3f}s"
    )

    # 응답 헤더에 소요 시간 추가
    response.headers["X-Process-Time"] = str(process_time)

    return response


# 헬스체크 엔드포인트
@app.get("/health", tags=["monitoring"])
async def health_check():
    """
    서버 헬스체크

    Returns:
        서버 상태
    """
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


# Prometheus 메트릭
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# 루트 엔드포인트
@app.get("/", tags=["general"])
async def root():
    """
    API 정보

    Returns:
        API 기본 정보
    """
    return {
        "name": "Qdrant Vector Search API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }


# 에러 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 에러 핸들러"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "detail": str(exc) if app.debug else None
        }
    )


# TODO: 라우터 추가
# from .routers import collections, vectors, search
# app.include_router(collections.router, prefix="/api/v1")
# app.include_router(vectors.router, prefix="/api/v1")
# app.include_router(search.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
