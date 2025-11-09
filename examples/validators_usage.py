#!/usr/bin/env python3
"""
Validators usage example for abs_utils
"""
from abs_utils import validators
from abs_utils.exceptions import ValidationException
from abs_utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO", log_format="plain")
logger = get_logger(__name__)


def validate_emails():
    """Example of email validation"""
    print("=== Email Validation ===\n")

    test_emails = [
        "user@example.com",  # Valid
        "test.user+tag@company.co.uk",  # Valid
        "invalid-email",  # Invalid
        "@example.com",  # Invalid
    ]

    for email in test_emails:
        # Using raise_exception=False for demonstration
        is_valid = validators.validate_email(email, raise_exception=False)
        print(f"  {email:<30} {'✓ Valid' if is_valid else '✗ Invalid'}")

    print("\nWith exception handling:")
    try:
        validators.validate_email("bad@")  # Will raise
    except ValidationException as e:
        logger.error(f"Email validation failed: {e.message}")


def validate_files():
    """Example of file validation"""
    print("\n=== File Validation ===\n")

    test_files = [
        ("document.pdf", "application/pdf"),  # Valid
        ("image.jpg", "image/jpeg"),  # Valid
        ("script.exe", "application/x-executable"),  # Invalid
        ("data.xyz", None),  # Invalid extension
    ]

    for filename, mime_type in test_files:
        is_valid = validators.validate_file_type(
            filename, mime_type, raise_exception=False
        )
        print(f"  {filename:<20} {mime_type or 'no mime':<25} {'✓' if is_valid else '✗'}")

    # File size validation
    print("\n=== File Size Validation ===\n")

    test_sizes = [
        (1024, "1 KB"),  # Valid
        (50 * 1024 * 1024, "50 MB"),  # Valid
        (100 * 1024 * 1024, "100 MB"),  # Valid (at limit)
        (200 * 1024 * 1024, "200 MB"),  # Invalid
    ]

    for size, label in test_sizes:
        is_valid = validators.validate_file_size(size, raise_exception=False)
        print(f"  {label:<10} {'✓ Valid' if is_valid else '✗ Too large'}")


def validate_hashes():
    """Example of hash validation"""
    print("\n=== Hash Validation ===\n")

    test_hashes = [
        "0x" + "a" * 64,  # Valid
        "0x" + "0123456789abcdef" * 4,  # Valid
        "a" * 64,  # Valid (without 0x)
        "0x" + "z" * 64,  # Invalid (non-hex)
        "0x" + "a" * 63,  # Invalid (too short)
        "not-a-hash",  # Invalid
    ]

    for hash_value in test_hashes:
        is_valid = validators.validate_hash(hash_value, raise_exception=False)
        display = hash_value[:20] + "..." if len(hash_value) > 20 else hash_value
        print(f"  {display:<25} {'✓ Valid' if is_valid else '✗ Invalid'}")


def validate_addresses():
    """Example of Ethereum address validation"""
    print("\n=== Ethereum Address Validation ===\n")

    test_addresses = [
        "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",  # Valid
        "0x" + "0" * 40,  # Valid (zero address)
        "0x" + "a" * 40,  # Valid
        "not-an-address",  # Invalid
        "0x" + "g" * 40,  # Invalid (non-hex)
        "0x" + "a" * 39,  # Invalid (too short)
    ]

    for address in test_addresses:
        is_valid = validators.validate_ethereum_address(
            address, raise_exception=False
        )
        display = address[:20] + "..." if len(address) > 20 else address
        print(f"  {display:<25} {'✓ Valid' if is_valid else '✗ Invalid'}")


def validate_transaction_hashes():
    """Example of transaction hash validation"""
    print("\n=== Transaction Hash Validation ===\n")

    # Transaction hashes are same format as regular hashes
    tx_hash = "0x" + "deadbeef" * 8
    is_valid = validators.validate_transaction_hash(tx_hash, raise_exception=False)
    print(f"  Transaction hash: {tx_hash[:20]}...")
    print(f"  Valid: {is_valid}")


def combined_validation_example():
    """Example of validating multiple fields"""
    print("\n=== Combined Validation Example ===\n")

    # Simulate validating a document upload request
    class DocumentUploadRequest:
        def __init__(self, email, filename, file_size, network, tx_hash):
            self.email = email
            self.filename = filename
            self.file_size = file_size
            self.network = network
            self.tx_hash = tx_hash

    request = DocumentUploadRequest(
        email="user@example.com",
        filename="contract.pdf",
        file_size=5 * 1024 * 1024,  # 5MB
        network="polygon",
        tx_hash="0x" + "abc123" * 10 + "abcd",
    )

    errors = []

    # Validate all fields
    try:
        validators.validate_email(request.email)
        print("✓ Email valid")
    except ValidationException as e:
        errors.append(e)
        print(f"✗ Email: {e.message}")

    try:
        validators.validate_file_type(request.filename)
        print("✓ File type valid")
    except ValidationException as e:
        errors.append(e)
        print(f"✗ File type: {e.message}")

    try:
        validators.validate_file_size(request.file_size)
        print("✓ File size valid")
    except ValidationException as e:
        errors.append(e)
        print(f"✗ File size: {e.message}")

    try:
        validators.validate_transaction_hash(request.tx_hash)
        print("✓ Transaction hash valid")
    except ValidationException as e:
        errors.append(e)
        print(f"✗ Transaction hash: {e.message}")

    if errors:
        print(f"\n{len(errors)} validation error(s) found")
    else:
        print("\n✓ All validations passed!")


def main():
    """Run all validation examples"""
    validate_emails()
    validate_files()
    validate_hashes()
    validate_addresses()
    validate_transaction_hashes()
    combined_validation_example()


if __name__ == "__main__":
    main()