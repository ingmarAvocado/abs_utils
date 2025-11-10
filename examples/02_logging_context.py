#!/usr/bin/env python3
"""
Example 2: Logging with Global Context

This example shows:
- How to set global context that appears in ALL logs
- How to clear context
- Practical use case: Request ID tracking
"""

from abs_utils.logger import setup_logging, get_logger, set_log_context, clear_log_context
import uuid


def process_request(user_id: int, action: str):
    """Simulate processing a user request"""
    logger = get_logger(__name__)

    logger.info(f"Processing {action}", extra={"user_id": user_id, "action": action})

    # Simulate some work
    if action == "upload":
        logger.info("File uploaded successfully", extra={"file_count": 3})
    elif action == "delete":
        logger.warning("Delete operation requested")

    logger.info("Request completed", extra={"status": "success"})


def main():
    print("=" * 80)
    print("EXAMPLE 2: Logging Context")
    print("=" * 80)
    print()

    # Setup logging
    setup_logging(level="INFO", log_format="json", service_name="api_server")

    print("Scenario: Tracking requests with unique IDs\n")

    # Simulate Request 1
    print("📨 Request 1 arrives...")
    request_id_1 = str(uuid.uuid4())
    set_log_context(request_id=request_id_1, client_ip="192.168.1.100")
    process_request(user_id=123, action="upload")
    clear_log_context()
    print()

    # Simulate Request 2
    print("📨 Request 2 arrives...")
    request_id_2 = str(uuid.uuid4())
    set_log_context(request_id=request_id_2, client_ip="192.168.1.101")
    process_request(user_id=456, action="delete")
    clear_log_context()
    print()

    print("✅ Example complete!")
    print("\nKey Takeaways:")
    print("- set_log_context() adds fields to ALL subsequent logs")
    print("- Great for request IDs, user sessions, correlation IDs")
    print("- Always clear_log_context() when done (e.g., end of request)")
    print("- Context is thread-safe for async operations")
    print("\n💡 In production: Use FastAPI middleware to auto-manage context!")


if __name__ == "__main__":
    main()
