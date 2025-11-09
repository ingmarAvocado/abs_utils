#!/usr/bin/env python3
"""
Custom exceptions usage example for abs_utils
"""
from abs_utils.exceptions import (
    NotaryException,
    DocumentNotFoundException,
    DocumentAlreadyExistsException,
    ValidationException,
    AuthenticationException,
    AuthorizationException,
    BlockchainException,
    TransactionFailedException,
    InvalidNetworkException,
    RateLimitException,
)
from abs_utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO", log_format="plain")
logger = get_logger(__name__)


def handle_document_operations():
    """Example of document-related exceptions"""
    print("=== Document Exceptions ===\n")

    try:
        # Simulate document not found
        raise DocumentNotFoundException(document_id=123)
    except DocumentNotFoundException as e:
        logger.error(f"Document error: {e.message}")
        print(f"Error dict: {e.to_dict()}\n")

    try:
        # Simulate duplicate document
        raise DocumentAlreadyExistsException(
            file_hash="0xabc123def456"
        )
    except DocumentAlreadyExistsException as e:
        logger.error(f"Duplicate document: {e.message}")
        print(f"Error dict: {e.to_dict()}\n")


def handle_validation():
    """Example of validation exceptions"""
    print("=== Validation Exceptions ===\n")

    try:
        # Simulate validation failure
        email = "invalid-email"
        if "@" not in email:
            raise ValidationException("email", "Invalid email format")
    except ValidationException as e:
        logger.error(f"Validation failed: {e.message}")
        print(f"Error dict: {e.to_dict()}\n")


def handle_authentication():
    """Example of auth exceptions"""
    print("=== Authentication/Authorization ===\n")

    try:
        # Simulate auth failure
        raise AuthenticationException("Invalid API key")
    except AuthenticationException as e:
        logger.error(f"Auth failed: {e.message}")
        print(f"Error dict: {e.to_dict()}\n")

    try:
        # Simulate authorization failure
        raise AuthorizationException(
            action="delete",
            resource="document_123"
        )
    except AuthorizationException as e:
        logger.error(f"Not authorized: {e.message}")
        print(f"Error dict: {e.to_dict()}\n")


def handle_blockchain():
    """Example of blockchain exceptions"""
    print("=== Blockchain Exceptions ===\n")

    try:
        # Simulate transaction failure
        raise TransactionFailedException(
            transaction_hash="0xtx123",
            reason="Out of gas"
        )
    except TransactionFailedException as e:
        logger.error(f"Transaction failed: {e.message}")
        print(f"Error dict: {e.to_dict()}\n")

    try:
        # Simulate invalid network
        supported = ["polygon", "ethereum", "sepolia"]
        raise InvalidNetworkException("bsc", supported)
    except InvalidNetworkException as e:
        logger.error(f"Invalid network: {e.message}")
        print(f"Error dict: {e.to_dict()}\n")


def handle_rate_limiting():
    """Example of rate limit exception"""
    print("=== Rate Limiting ===\n")

    try:
        # Simulate rate limit exceeded
        raise RateLimitException(retry_after=60)
    except RateLimitException as e:
        logger.error(f"Rate limited: {e.message}")
        print(f"Error dict: {e.to_dict()}\n")


def handle_generic_exception():
    """Example of catching all NotaryExceptions"""
    print("=== Generic Exception Handling ===\n")

    exceptions_to_test = [
        DocumentNotFoundException(456),
        ValidationException("field", "error"),
        AuthenticationException("Token expired"),
    ]

    for exc in exceptions_to_test:
        try:
            raise exc
        except NotaryException as e:
            # All custom exceptions inherit from NotaryException
            print(f"Caught {e.__class__.__name__}: {e.code}")
            print(f"  Message: {e.message}")
            print(f"  Details: {e.details}\n")


def main():
    """Run all examples"""
    handle_document_operations()
    handle_validation()
    handle_authentication()
    handle_blockchain()
    handle_rate_limiting()
    handle_generic_exception()

    print("=== API Response Example ===\n")

    # Example of using to_dict() for API responses
    exc = ValidationException("password", "Password too short")
    api_response = {
        "status": "error",
        **exc.to_dict()
    }
    print(f"API Response: {api_response}")


if __name__ == "__main__":
    main()