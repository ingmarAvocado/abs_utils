#!/usr/bin/env python3
"""
Example 1: Basic Logging Setup and Usage

This example shows:
- How to setup logging with JSON format
- How to use different log levels
- How to add context to logs
- How to use both text and JSON formats
"""

from abs_utils.logger import setup_logging, get_logger


def main():
    print("=" * 80)
    print("EXAMPLE 1: Basic Logging")
    print("=" * 80)
    print()

    # Setup logging with JSON format
    print("1. Setting up JSON logging...")
    setup_logging(level="INFO", log_format="json", service_name="example_service")

    # Get a logger
    logger = get_logger(__name__)

    # Basic logging
    print("\n2. Basic log messages:")
    logger.debug("This is a debug message (won't show because level=INFO)")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Logging with extra context
    print("\n3. Logging with context:")
    logger.info("User logged in", extra={"user_id": 123, "username": "john_doe"})
    logger.info(
        "Document uploaded",
        extra={"doc_id": 456, "file_name": "contract.pdf", "file_size": 1024000},
    )

    # Logging errors with exception info
    print("\n4. Logging exceptions:")
    try:
        result = 10 / 0
    except Exception as e:
        logger.error("Division by zero error", extra={"error": str(e)}, exc_info=True)

    print("\n" + "=" * 80)
    print("Now let's try TEXT format for comparison...")
    print("=" * 80)
    print()

    # Switch to text format
    setup_logging(level="INFO", log_format="text", service_name="example_service")
    logger_text = get_logger("text_logger")

    logger_text.info("This is text format")
    logger_text.info("User logged in", extra={"user_id": 123, "username": "john_doe"})

    print("\n✅ Example complete!")
    print("\nKey Takeaways:")
    print("- JSON format: Machine-readable, great for log aggregation")
    print("- Text format: Human-readable, great for development")
    print("- Use 'extra' parameter to add structured context")
    print("- Call setup_logging() once at application startup")


if __name__ == "__main__":
    main()
