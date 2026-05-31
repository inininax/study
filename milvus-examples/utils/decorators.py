"""
Decorator utilities for retry logic, timing, and circuit breakers.
Production-ready patterns for robust Milvus operations.
"""

import functools
import time
from typing import Any, Callable, Optional, Type, Union

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .exceptions import (
    MilvusConnectionError,
    MilvusOperationError,
    MilvusTimeoutError,
)
from .logger import get_logger

logger = get_logger(__name__)


def retry_on_failure(
    max_attempts: int = 3,
    wait_min: float = 1.0,
    wait_max: float = 10.0,
    exceptions: tuple = (MilvusConnectionError, MilvusOperationError),
):
    """
    Retry decorator with exponential backoff for Milvus operations.

    Args:
        max_attempts: Maximum number of retry attempts
        wait_min: Minimum wait time between retries (seconds)
        wait_max: Maximum wait time between retries (seconds)
        exceptions: Tuple of exception types to retry on

    Example:
        @retry_on_failure(max_attempts=5)
        def insert_data(collection, data):
            return collection.insert(data)
    """

    def decorator(func: Callable) -> Callable:
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(min=wait_min, max=wait_max),
            retry=retry_if_exception_type(exceptions),
            reraise=True,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                logger.warning(
                    "operation_failed_retrying",
                    function=func.__name__,
                    error=str(e),
                    error_type=type(e).__name__,
                )
                raise

        return wrapper

    return decorator


def timing_decorator(func: Callable) -> Callable:
    """
    Decorator to measure and log execution time.

    Args:
        func: Function to decorate

    Example:
        @timing_decorator
        def search_vectors(collection, query):
            return collection.search(query)
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(
                "operation_completed",
                function=func.__name__,
                duration_ms=round(elapsed_time * 1000, 2),
            )
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "operation_failed",
                function=func.__name__,
                duration_ms=round(elapsed_time * 1000, 2),
                error=str(e),
                error_type=type(e).__name__,
            )
            raise

    return wrapper


def timeout_decorator(seconds: float):
    """
    Decorator to enforce timeout on operations.

    Args:
        seconds: Timeout in seconds

    Example:
        @timeout_decorator(30.0)
        def long_running_operation():
            # ... operation ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import signal

            def timeout_handler(signum, frame):
                raise MilvusTimeoutError(
                    f"Operation timed out after {seconds} seconds",
                    details={"function": func.__name__, "timeout": seconds},
                )

            # Set the timeout handler
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(seconds))

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

            return result

        return wrapper

    return decorator


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for fault tolerance.

    States:
    - CLOSED: Normal operation
    - OPEN: Failures exceed threshold, reject requests
    - HALF_OPEN: Test if service recovered

    Example:
        breaker = CircuitBreaker(failure_threshold=5, timeout=60)

        @breaker.call
        def call_external_service():
            # ... service call ...
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        expected_exception: Type[Exception] = Exception,
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "CLOSED"

    def call(self, func: Callable) -> Callable:
        """Decorator to wrap function with circuit breaker."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "HALF_OPEN"
                    logger.info("circuit_breaker_half_open", function=func.__name__)
                else:
                    logger.warning("circuit_breaker_open", function=func.__name__)
                    raise MilvusOperationError(
                        "Circuit breaker is OPEN",
                        details={
                            "function": func.__name__,
                            "state": self.state,
                            "failure_count": self.failure_count,
                        },
                    )

            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except self.expected_exception as e:
                self._on_failure()
                raise

        return wrapper

    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            logger.info("circuit_breaker_closed")

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.error(
                "circuit_breaker_opened",
                failure_count=self.failure_count,
                threshold=self.failure_threshold,
            )


def cache_result(ttl: int = 300):
    """
    Simple in-memory cache decorator with TTL.

    Args:
        ttl: Time to live in seconds

    Example:
        @cache_result(ttl=600)
        def get_collection_info(collection_name):
            # ... expensive operation ...
    """
    cache = {}

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            current_time = time.time()

            # Check if cached and not expired
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if current_time - timestamp < ttl:
                    logger.debug("cache_hit", function=func.__name__, key=cache_key)
                    return result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache[cache_key] = (result, current_time)
            logger.debug("cache_miss", function=func.__name__, key=cache_key)

            # Simple cache cleanup: remove expired entries
            expired_keys = [
                k for k, (_, ts) in cache.items() if current_time - ts >= ttl
            ]
            for k in expired_keys:
                del cache[k]

            return result

        return wrapper

    return decorator
