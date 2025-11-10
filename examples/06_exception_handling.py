#!/usr/bin/env python3
"""
Example 6: Exception Handling

This example shows:
- How to use custom exceptions
- How exceptions convert to API responses
- Exception hierarchy and catching
- Best practices for error handling
"""

from abs_utils.exceptions import (
    NotaryException,
    DocumentNotFoundException,
    DocumentAlreadyExistsException,
    ValidationException,
    BlockchainException,
    InsufficientGasException,
    TransactionFailedException,
    AuthenticationException,
    AuthorizationException,
    ApiKeyNotFoundException,
    RateLimitException,
)


def basic_exception_example():
    """Basic exception usage"""
    print("\n1️⃣ BASIC EXCEPTION USAGE")
    print("-" * 50)

    try:
        # Raise a custom exception
        raise DocumentNotFoundException(document_id=123)
    except DocumentNotFoundException as e:
        print(f"❌ Exception caught: {e.message}")
        print(f"   Error code: {e.code}")
        print(f"   Details: {e.details}")
        print(f"   As dict: {e.to_dict()}")


def api_response_example():
    """How to use exceptions in API responses"""
    print("\n2️⃣ API RESPONSE FORMAT")
    print("-" * 50)

    def get_document(doc_id: int):
        """Simulate fetching a document"""
        # Simulate document not found
        if doc_id != 1:
            raise DocumentNotFoundException(document_id=doc_id)
        return {"id": doc_id, "name": "contract.pdf"}

    # Try valid ID
    print("Request: GET /documents/1")
    try:
        doc = get_document(1)
        print(f"✅ 200 OK: {doc}")
    except NotaryException as e:
        print(f"❌ 404 Not Found: {e.to_dict()}")

    # Try invalid ID
    print("\nRequest: GET /documents/999")
    try:
        doc = get_document(999)
        print(f"✅ 200 OK: {doc}")
    except NotaryException as e:
        error_response = e.to_dict()
        print(f"❌ 404 Not Found:")
        print(f"   {error_response}")


def exception_hierarchy_example():
    """Exception hierarchy and catching"""
    print("\n3️⃣ EXCEPTION HIERARCHY")
    print("-" * 50)

    exceptions_to_raise = [
        DocumentNotFoundException(123),
        ValidationException("email", "Invalid format"),
        InsufficientGasException(required_gas=300000, available_gas=100000),
        AuthenticationException("Invalid credentials"),
    ]

    for exc in exceptions_to_raise:
        try:
            raise exc
        except BlockchainException as e:
            # Catch all blockchain-related errors
            print(f"🔗 Blockchain error: {e.code}")
        except ValidationException as e:
            # Catch validation errors
            print(f"📝 Validation error: {e.code}")
        except NotaryException as e:
            # Catch all other notary errors
            print(f"❌ General error: {e.code}")


def blockchain_exceptions_example():
    """Blockchain-specific exceptions"""
    print("\n4️⃣ BLOCKCHAIN EXCEPTIONS")
    print("-" * 50)

    # Insufficient gas
    try:
        raise InsufficientGasException(required_gas=300000, available_gas=50000)
    except InsufficientGasException as e:
        print(f"❌ {e.message}")
        print(f"   Required: {e.details['required_gas']} gas")
        print(f"   Available: {e.details['available_gas']} gas")

    # Transaction failed
    try:
        tx_hash = "0x" + "a" * 64
        raise TransactionFailedException(tx_hash, reason="Out of gas")
    except TransactionFailedException as e:
        print(f"\n❌ {e.message}")
        print(f"   TX Hash: {e.details['transaction_hash'][:20]}...")
        print(f"   Reason: {e.details['reason']}")


def authentication_exceptions_example():
    """Authentication and authorization exceptions"""
    print("\n5️⃣ AUTHENTICATION & AUTHORIZATION")
    print("-" * 50)

    # Authentication failure
    try:
        raise AuthenticationException("Invalid password")
    except AuthenticationException as e:
        print(f"❌ {e.message} (401 Unauthorized)")
        print(f"   Response: {e.to_dict()}")

    # Authorization failure
    try:
        raise AuthorizationException(action="delete", resource="document/123")
    except AuthorizationException as e:
        print(f"\n❌ {e.message} (403 Forbidden)")
        print(f"   Action: {e.details['action']}")
        print(f"   Resource: {e.details['resource']}")

    # API key not found
    try:
        raise ApiKeyNotFoundException(key_prefix="sk_live_abc1")
    except ApiKeyNotFoundException as e:
        print(f"\n❌ {e.message} (401 Unauthorized)")
        print(f"   Prefix: {e.details['key_prefix']}")


def rate_limiting_example():
    """Rate limiting exception"""
    print("\n6️⃣ RATE LIMITING")
    print("-" * 50)

    try:
        raise RateLimitException(retry_after=60)
    except RateLimitException as e:
        print(f"❌ {e.message} (429 Too Many Requests)")
        print(f"   Retry after: {e.details['retry_after_seconds']} seconds")
        print(f"   Response headers:")
        print(f"     Retry-After: {e.details['retry_after_seconds']}")


def complete_error_handling_example():
    """Complete error handling pattern"""
    print("\n7️⃣ COMPLETE ERROR HANDLING PATTERN")
    print("-" * 50)

    def process_document_upload(doc_id: int, file_hash: str, gas_available: int):
        """Simulate document processing with multiple potential errors"""

        # Check if document exists
        existing_doc_id = 123
        if doc_id == existing_doc_id:
            raise DocumentAlreadyExistsException(file_hash)

        # Validate hash format
        if not file_hash.startswith("0x") or len(file_hash) != 66:
            raise ValidationException("file_hash", "Invalid hash format")

        # Check gas
        required_gas = 300000
        if gas_available < required_gas:
            raise InsufficientGasException(required_gas, gas_available)

        # Simulate success
        return {"status": "success", "doc_id": doc_id}

    # Test scenarios
    scenarios = [
        (100, "0x" + "a" * 64, 400000, "Should succeed"),
        (123, "0x" + "b" * 64, 400000, "Document exists"),
        (200, "invalid_hash", 400000, "Invalid hash"),
        (300, "0x" + "c" * 64, 100000, "Insufficient gas"),
    ]

    for doc_id, file_hash, gas, description in scenarios:
        print(f"\nScenario: {description}")
        try:
            result = process_document_upload(doc_id, file_hash, gas)
            print(f"  ✅ Success: {result}")
        except NotaryException as e:
            print(f"  ❌ Error ({e.code}): {e.message}")
            if e.details:
                for key, value in e.details.items():
                    print(f"     {key}: {value}")


def main():
    print("=" * 80)
    print("EXAMPLE 6: EXCEPTION HANDLING")
    print("=" * 80)

    basic_exception_example()
    api_response_example()
    exception_hierarchy_example()
    blockchain_exceptions_example()
    authentication_exceptions_example()
    rate_limiting_example()
    complete_error_handling_example()

    print("\n" + "=" * 80)
    print("✅ Example complete!")
    print("\nKey Takeaways:")
    print("- All custom exceptions inherit from NotaryException")
    print("- Use exc.to_dict() for clean API error responses")
    print("- Exceptions include structured error codes and details")
    print("- Catch specific exceptions for different error handling")
    print("- BlockchainException is base for all blockchain errors")
    print("=" * 80)


if __name__ == "__main__":
    main()
