"""Unit tests that run without a Milvus server."""

import pytest

from config.settings import Settings
from utils.decorators import cache_result
from utils.exceptions import MilvusConnectionError, MilvusOperationError


def test_settings_defaults():
    settings = Settings()
    assert settings.milvus_host == "localhost"
    assert settings.milvus_port == 19530
    assert settings.index_type == "HNSW"
    assert settings.metric_type == "L2"


def test_settings_milvus_uri():
    settings = Settings(milvus_host="milvus", milvus_port=19530, milvus_secure=False)
    assert settings.milvus_uri == "http://milvus:19530"

    tls = Settings(milvus_host="milvus", milvus_secure=True)
    assert tls.milvus_uri.startswith("https://")


def test_settings_redis_url_with_auth():
    settings = Settings(redis_host="redis", redis_port=6379, redis_db=2, redis_password="pw")
    assert settings.redis_url == "redis://:pw@redis:6379/2"

    no_auth = Settings(redis_host="localhost")
    assert no_auth.redis_url == "redis://localhost:6379/0"


def test_settings_invalid_log_level_rejected():
    with pytest.raises(ValueError):
        Settings(log_level="VERBOSE")


def test_settings_log_level_uppercased():
    assert Settings(log_level="debug").log_level == "DEBUG"


def test_connection_error_details():
    err = MilvusConnectionError("boom", details={"host": "h"})
    assert err.error_code == "MILVUS_CONNECTION_ERROR"
    assert err.to_dict() == {
        "error_code": "MILVUS_CONNECTION_ERROR",
        "message": "boom",
        "details": {"host": "h"},
    }


def test_operation_error_is_base_exception():
    assert isinstance(MilvusOperationError("x"), Exception)


def test_cache_result_decorator_hits_cache():
    calls = []

    @cache_result(ttl=60)
    def add(a, b=0):
        calls.append((a, b))
        return a + b

    assert add(1, b=2) == 3
    assert add(1, b=2) == 3
    assert len(calls) == 1
