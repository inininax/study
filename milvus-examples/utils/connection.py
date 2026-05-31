"""
Milvus connection management with pooling and health checks.
Production-ready connection handling with automatic reconnection.
"""

import threading
import time
from contextlib import contextmanager
from queue import Empty, Queue
from typing import Optional

from pymilvus import Collection, connections, utility

from config.settings import settings
from .decorators import retry_on_failure
from .exceptions import MilvusConnectionError, MilvusOperationError
from .logger import get_logger

logger = get_logger(__name__)


class MilvusConnection:
    """
    Wrapper for a single Milvus connection with health tracking.
    """

    def __init__(self, alias: str):
        self.alias = alias
        self.created_at = time.time()
        self.last_used = time.time()
        self.is_healthy = True

    def check_health(self) -> bool:
        """Check if connection is healthy."""
        try:
            # Simple health check using list_collections
            utility.list_collections(using=self.alias)
            self.is_healthy = True
            return True
        except Exception as e:
            logger.warning(
                "connection_health_check_failed",
                alias=self.alias,
                error=str(e),
            )
            self.is_healthy = False
            return False

    def disconnect(self):
        """Disconnect from Milvus."""
        try:
            connections.disconnect(self.alias)
            logger.info("connection_disconnected", alias=self.alias)
        except Exception as e:
            logger.error(
                "connection_disconnect_failed",
                alias=self.alias,
                error=str(e),
            )


class MilvusConnectionPool:
    """
    Connection pool for Milvus with automatic health checks and reconnection.

    Features:
    - Connection pooling for reuse
    - Automatic health checks
    - Connection timeout handling
    - Thread-safe operations
    """

    def __init__(
        self,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        pool_size: int = None,
        max_idle_time: int = None,
        connection_timeout: int = None,
    ):
        """
        Initialize connection pool.

        Args:
            host: Milvus host (default from settings)
            port: Milvus port (default from settings)
            user: Milvus user (default from settings)
            password: Milvus password (default from settings)
            pool_size: Pool size (default from settings)
            max_idle_time: Max idle time in seconds (default from settings)
            connection_timeout: Connection timeout (default from settings)
        """
        self.host = host or settings.milvus_host
        self.port = port or settings.milvus_port
        self.user = user or settings.milvus_user
        self.password = password or settings.milvus_password
        self.pool_size = pool_size or settings.milvus_pool_size
        self.max_idle_time = max_idle_time or settings.milvus_max_idle_time
        self.connection_timeout = connection_timeout or settings.milvus_connection_timeout

        self._pool: Queue[MilvusConnection] = Queue(maxsize=self.pool_size)
        self._lock = threading.Lock()
        self._connection_counter = 0
        self._initialized = False

        logger.info(
            "connection_pool_initialized",
            host=self.host,
            port=self.port,
            pool_size=self.pool_size,
        )

    def _create_connection(self) -> MilvusConnection:
        """Create a new Milvus connection."""
        with self._lock:
            self._connection_counter += 1
            alias = f"milvus_conn_{self._connection_counter}_{int(time.time())}"

        try:
            connections.connect(
                alias=alias,
                host=self.host,
                port=self.port,
                user=self.user or "",
                password=self.password or "",
                timeout=self.connection_timeout,
            )

            conn = MilvusConnection(alias)
            logger.info("connection_created", alias=alias)
            return conn

        except Exception as e:
            logger.error(
                "connection_creation_failed",
                alias=alias,
                error=str(e),
                error_type=type(e).__name__,
            )
            raise MilvusConnectionError(
                f"Failed to create connection: {str(e)}",
                details={"host": self.host, "port": self.port},
            )

    def _initialize_pool(self):
        """Initialize the connection pool with connections."""
        if self._initialized:
            return

        with self._lock:
            if self._initialized:
                return

            logger.info("initializing_connection_pool", size=self.pool_size)

            for _ in range(self.pool_size):
                try:
                    conn = self._create_connection()
                    self._pool.put(conn)
                except MilvusConnectionError as e:
                    logger.error("pool_initialization_partial_failure", error=str(e))
                    # Continue initializing remaining connections

            self._initialized = True
            logger.info(
                "connection_pool_ready",
                available_connections=self._pool.qsize(),
            )

    @retry_on_failure(max_attempts=3)
    def get_connection(self, timeout: Optional[float] = None) -> MilvusConnection:
        """
        Get a connection from the pool.

        Args:
            timeout: Timeout for getting connection (seconds)

        Returns:
            MilvusConnection instance

        Raises:
            MilvusConnectionError: If unable to get connection
        """
        if not self._initialized:
            self._initialize_pool()

        timeout = timeout or self.connection_timeout

        try:
            conn = self._pool.get(timeout=timeout)

            # Check if connection is still healthy
            if not conn.check_health():
                logger.warning("unhealthy_connection_detected", alias=conn.alias)
                conn.disconnect()
                conn = self._create_connection()

            # Check if connection has been idle too long
            idle_time = time.time() - conn.last_used
            if idle_time > self.max_idle_time:
                logger.info(
                    "connection_idle_too_long",
                    alias=conn.alias,
                    idle_time=idle_time,
                )
                conn.disconnect()
                conn = self._create_connection()

            conn.last_used = time.time()
            return conn

        except Empty:
            raise MilvusConnectionError(
                f"Timeout waiting for connection (timeout={timeout}s)",
                details={"pool_size": self.pool_size, "timeout": timeout},
            )

    def return_connection(self, conn: MilvusConnection):
        """
        Return a connection to the pool.

        Args:
            conn: Connection to return
        """
        try:
            self._pool.put(conn, block=False)
        except Exception as e:
            logger.error(
                "connection_return_failed",
                alias=conn.alias,
                error=str(e),
            )
            conn.disconnect()

    @contextmanager
    def get_connection_context(self):
        """
        Context manager for getting and returning connections.

        Example:
            with pool.get_connection_context() as conn:
                # Use conn.alias for Milvus operations
                collection = Collection("my_collection", using=conn.alias)
        """
        conn = self.get_connection()
        try:
            yield conn
        finally:
            self.return_connection(conn)

    def close_all(self):
        """Close all connections in the pool."""
        logger.info("closing_connection_pool")

        while not self._pool.empty():
            try:
                conn = self._pool.get(block=False)
                conn.disconnect()
            except Empty:
                break

        logger.info("connection_pool_closed")


# Global connection pool instance
_connection_pool: Optional[MilvusConnectionPool] = None
_pool_lock = threading.Lock()


def get_milvus_client() -> MilvusConnectionPool:
    """
    Get the global Milvus connection pool instance (singleton).

    Returns:
        MilvusConnectionPool instance
    """
    global _connection_pool

    if _connection_pool is None:
        with _pool_lock:
            if _connection_pool is None:
                _connection_pool = MilvusConnectionPool()

    return _connection_pool


class MilvusConnectionManager:
    """
    High-level connection manager with additional utilities.

    Example:
        manager = MilvusConnectionManager()

        # Get a collection
        collection = manager.get_collection("my_collection")

        # Check if collection exists
        if manager.collection_exists("my_collection"):
            # Do something
    """

    def __init__(self, pool: Optional[MilvusConnectionPool] = None):
        """
        Initialize connection manager.

        Args:
            pool: Optional connection pool (uses global pool if None)
        """
        self.pool = pool or get_milvus_client()

    @contextmanager
    def get_collection(self, name: str) -> Collection:
        """
        Get a collection with automatic connection management.

        Args:
            name: Collection name

        Yields:
            Collection instance

        Example:
            with manager.get_collection("my_collection") as collection:
                results = collection.search(...)
        """
        with self.pool.get_connection_context() as conn:
            try:
                collection = Collection(name, using=conn.alias)
                yield collection
            except Exception as e:
                logger.error(
                    "collection_access_failed",
                    collection=name,
                    error=str(e),
                )
                raise MilvusOperationError(
                    f"Failed to access collection '{name}': {str(e)}",
                    details={"collection": name},
                )

    def collection_exists(self, name: str) -> bool:
        """
        Check if a collection exists.

        Args:
            name: Collection name

        Returns:
            True if collection exists, False otherwise
        """
        with self.pool.get_connection_context() as conn:
            try:
                return utility.has_collection(name, using=conn.alias)
            except Exception as e:
                logger.error(
                    "collection_exists_check_failed",
                    collection=name,
                    error=str(e),
                )
                return False

    def list_collections(self) -> list[str]:
        """
        List all collections.

        Returns:
            List of collection names
        """
        with self.pool.get_connection_context() as conn:
            try:
                return utility.list_collections(using=conn.alias)
            except Exception as e:
                logger.error("list_collections_failed", error=str(e))
                raise MilvusOperationError(f"Failed to list collections: {str(e)}")

    def close(self):
        """Close all connections."""
        self.pool.close_all()
