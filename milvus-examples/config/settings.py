"""
Global settings and configuration management.
Uses pydantic-settings for type-safe configuration with environment variable support.
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable override support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Milvus Configuration
    milvus_host: str = Field(default="localhost", description="Milvus host address")
    milvus_port: int = Field(default=19530, description="Milvus port")
    milvus_user: Optional[str] = Field(default=None, description="Milvus username")
    milvus_password: Optional[str] = Field(default=None, description="Milvus password")
    milvus_db_name: str = Field(default="default", description="Milvus database name")
    milvus_secure: bool = Field(default=False, description="Use TLS connection")

    # Connection Pool
    milvus_pool_size: int = Field(default=10, ge=1, le=100, description="Connection pool size")
    milvus_max_idle_time: int = Field(default=300, ge=60, description="Max idle time in seconds")
    milvus_connection_timeout: int = Field(default=30, ge=5, description="Connection timeout in seconds")

    # Redis Configuration
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, ge=0, le=15, description="Redis database number")
    redis_password: Optional[str] = Field(default=None, description="Redis password")
    redis_cache_ttl: int = Field(default=3600, ge=60, description="Cache TTL in seconds")

    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="text-embedding-3-small", description="OpenAI embedding model")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")
    log_file: str = Field(default="logs/milvus-app.log", description="Log file path")

    # Performance
    batch_size: int = Field(default=1000, ge=1, le=10000, description="Batch insert size")
    search_topk: int = Field(default=10, ge=1, le=1000, description="Top K search results")
    index_type: str = Field(default="HNSW", description="Default index type")
    metric_type: str = Field(default="L2", description="Distance metric type")

    # Monitoring
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_port: int = Field(default=8000, description="Metrics server port")
    prometheus_enabled: bool = Field(default=True, description="Enable Prometheus integration")

    # Development
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment: development, staging, production")

    @validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of {valid_levels}")
        return v_upper

    @validator("index_type")
    def validate_index_type(cls, v: str) -> str:
        """Validate index type."""
        valid_types = {"FLAT", "IVF_FLAT", "IVF_SQ8", "IVF_PQ", "HNSW", "ANNOY", "DISKANN"}
        v_upper = v.upper()
        if v_upper not in valid_types:
            raise ValueError(f"Invalid index type. Must be one of {valid_types}")
        return v_upper

    @validator("metric_type")
    def validate_metric_type(cls, v: str) -> str:
        """Validate metric type."""
        valid_types = {"L2", "IP", "COSINE", "HAMMING", "JACCARD"}
        v_upper = v.upper()
        if v_upper not in valid_types:
            raise ValueError(f"Invalid metric type. Must be one of {valid_types}")
        return v_upper

    @property
    def milvus_uri(self) -> str:
        """Get Milvus connection URI."""
        protocol = "https" if self.milvus_secure else "http"
        return f"{protocol}://{self.milvus_host}:{self.milvus_port}"

    @property
    def redis_url(self) -> str:
        """Get Redis connection URL."""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure singleton pattern.
    """
    return Settings()


# Global settings instance
settings = get_settings()
