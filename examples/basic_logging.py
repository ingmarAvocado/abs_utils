#!/usr/bin/env python3
"""
Basic logging setup example for abs_utils
"""
from abs_utils.logger import setup_logging, get_logger


def main():
    # Setup logging once at application startup
    setup_logging(
        level="INFO",
        log_format="json",  # or "plain" for human-readable
        service_name="example-service"
    )

    # Get logger anywhere in your code
    logger = get_logger(__name__)

    # Log at different levels
    logger.debug("Debug message - won't show with INFO level")
    logger.info("Application started")
    logger.warning("This is a warning")
    logger.error("An error occurred", extra={"error_code": "ERR_001"})

    # Log with extra context
    logger.info(
        "Processing request",
        extra={
            "request_id": "req-123",
            "user_id": "user-456",
            "endpoint": "/api/documents"
        }
    )

    # Log exceptions
    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception("Failed to calculate result")


if __name__ == "__main__":
    main()