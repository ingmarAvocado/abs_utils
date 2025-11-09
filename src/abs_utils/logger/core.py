"""
Core logging functionality with JSON formatting and context injection
"""

import logging
import sys
from typing import Any

from pythonjsonlogger import jsonlogger


class ContextFilter(logging.Filter):
    """Add context fields to log records"""

    def __init__(self) -> None:
        super().__init__()
        self.context: dict[str, Any] = {}

    def filter(self, record: logging.LogRecord) -> bool:
        """Inject context into log record"""
        for key, value in self.context.items():
            setattr(record, key, value)
        return True

    def set_context(self, **kwargs: Any) -> None:
        """Set context fields"""
        self.context.update(kwargs)

    def clear_context(self) -> None:
        """Clear all context fields"""
        self.context.clear()


# Global context filter instance
_context_filter = ContextFilter()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with standard fields"""

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        """Add standard fields to log record"""
        super().add_fields(log_record, record, message_dict)

        # Ensure standard fields are present
        log_record["timestamp"] = self.formatTime(record, self.datefmt)
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["module"] = record.module
        log_record["function"] = record.funcName
        log_record["line"] = record.lineno

        # Add context fields if present
        for key in list(log_record.keys()):
            if key.startswith("context_"):
                # Keep context fields as-is
                continue


def setup_logging(
    level: str = "INFO",
    log_format: str = "json",
    service_name: str | None = None,
) -> None:
    """
    Setup logging configuration for the application

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Format type ('json' or 'text')
        service_name: Name of the service for identification
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Set formatter based on format type
    formatter: logging.Formatter
    if log_format == "json":
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(level)s %(logger)s %(module)s %(function)s %(line)d %(message)s"
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)

    # Configure root logger
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # Add context filter
    root_logger.addFilter(_context_filter)

    # Set service name if provided
    if service_name:
        set_log_context(service=service_name)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def set_log_context(**kwargs: Any) -> None:
    """
    Set context fields that will be included in all log records

    Example:
        set_log_context(request_id="123", user_id=456)
    """
    _context_filter.set_context(**kwargs)


def clear_log_context() -> None:
    """Clear all context fields"""
    _context_filter.clear_context()
