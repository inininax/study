"""
Structured logging utility with support for JSON and text formats.
Provides context-aware logging for production environments.
"""

import logging
import logging.config
import sys
from pathlib import Path
from typing import Optional

import structlog
import yaml

from config.settings import settings


def setup_logging(log_file: Optional[str] = None) -> None:
    """
    Setup logging configuration.

    Args:
        log_file: Optional log file path override
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_file or settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Load logging configuration from YAML
    config_path = Path(__file__).parent.parent / "config" / "logging.yaml"

    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            # Override log file path
            if log_file:
                config["handlers"]["file"]["filename"] = log_file
            logging.config.dictConfig(config)
    else:
        # Fallback to basic configuration
        logging.basicConfig(
            level=getattr(logging, settings.log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer() if settings.log_format == "json"
            else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


# Initialize logging on module import
setup_logging()
