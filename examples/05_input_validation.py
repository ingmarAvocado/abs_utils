#!/usr/bin/env python3
"""
Example 5: Input Validation

This example shows:
- How to validate emails
- How to validate file types and sizes
- How to validate hashes and Ethereum addresses
- Error handling with ValidationException
"""

from abs_utils.validators import (
    validate_email,
    validate_file_type,
    validate_file_size,
    validate_hash,
    validate_ethereum_address,
    validate_required_fields,
    validate_positive_integer,
    validate_string_length,
)
from abs_utils.exceptions import ValidationException


def email_validation_example():
    """Email validation examples"""
    print("\n1️⃣ EMAIL VALIDATION")
    print("-" * 50)

    valid_emails = [
        "user@example.com",
        "john.doe@company.co.uk",
        "admin+test@subdomain.example.com",
    ]

    invalid_emails = [
        "not-an-email",
        "@example.com",
        "user@",
        "user name@example.com",
    ]

    print("Valid emails:")
    for email in valid_emails:
        try:
            validate_email(email)
            print(f"  ✅ {email}")
        except ValidationException as e:
            print(f"  ❌ {email}: {e.message}")

    print("\nInvalid emails:")
    for email in invalid_emails:
        try:
            validate_email(email)
            print(f"  ✅ {email} (unexpected!)")
        except ValidationException as e:
            print(f"  ❌ {email}: {e.details['reason']}")


def file_validation_example():
    """File type and size validation"""
    print("\n2️⃣ FILE VALIDATION")
    print("-" * 50)

    # File type validation
    print("File types:")
    files = [
        ("document.pdf", "application/pdf"),
        ("image.png", "image/png"),
        ("script.exe", "application/x-msdownload"),  # Not supported
    ]

    for filename, mime_type in files:
        try:
            validate_file_type(filename, mime_type)
            print(f"  ✅ {filename} ({mime_type})")
        except ValidationException as e:
            print(f"  ❌ {filename}: {e.details['reason']}")

    # File size validation
    print("\nFile sizes:")
    MB = 1024 * 1024
    sizes = [
        (5 * MB, "5 MB"),
        (50 * MB, "50 MB"),
        (150 * MB, "150 MB"),  # Too large (max 100 MB)
    ]

    for size, description in sizes:
        try:
            validate_file_size(size)
            print(f"  ✅ {description}")
        except ValidationException as e:
            print(f"  ❌ {description}: {e.details['reason']}")


def hash_validation_example():
    """Hash format validation"""
    print("\n3️⃣ HASH VALIDATION")
    print("-" * 50)

    hashes = [
        ("0x" + "a" * 64, "Valid hash"),
        ("0x" + "1234" * 16, "Valid hash (numbers)"),
        ("0x" + "A" * 64, "Valid hash (uppercase)"),
        ("0x123", "Too short"),
        ("abc" * 22, "Missing 0x prefix"),
        ("0x" + "g" * 64, "Invalid character (g)"),
    ]

    for hash_value, description in hashes:
        try:
            validate_hash(hash_value)
            print(f"  ✅ {description}: {hash_value[:20]}...")
        except ValidationException as e:
            print(f"  ❌ {description}: {e.details['reason'][:50]}")


def ethereum_address_example():
    """Ethereum address validation"""
    print("\n4️⃣ ETHEREUM ADDRESS VALIDATION")
    print("-" * 50)

    addresses = [
        ("0x" + "a" * 40, "Valid address"),
        ("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "Valid address (mixed case)"),
        ("0x" + "1234" * 10, "Valid address (numbers)"),
        ("0x" + "a" * 39, "Too short"),
        ("0x" + "g" * 40, "Invalid character"),
    ]

    for address, description in addresses:
        try:
            validate_ethereum_address(address)
            print(f"  ✅ {description}: {address[:20]}...")
        except ValidationException as e:
            print(f"  ❌ {description}: {e.details['reason'][:50]}")


def advanced_validation_example():
    """Advanced validation examples"""
    print("\n5️⃣ ADVANCED VALIDATION")
    print("-" * 50)

    # Required fields
    print("Required fields validation:")
    data = {"user_id": 123, "email": "user@example.com"}

    try:
        validate_required_fields(data, ["user_id", "email", "password"])
    except ValidationException as e:
        print(f"  ❌ Missing fields: {e.details['reason']}")

    # Positive integer
    print("\nPositive integer validation:")
    values = [42, 0, -5]
    for val in values:
        try:
            validate_positive_integer(val, "amount")
            print(f"  ✅ {val} is valid")
        except ValidationException as e:
            print(f"  ❌ {val}: {e.details['reason']}")

    # String length
    print("\nString length validation:")
    passwords = ["abc", "securepass123", "a" * 150]
    for pwd in passwords:
        try:
            validate_string_length(pwd, "password", min_length=8, max_length=128)
            print(f"  ✅ Password length {len(pwd)} is valid")
        except ValidationException as e:
            print(f"  ❌ Password length {len(pwd)}: {e.details['reason']}")


def error_handling_example():
    """How to handle validation errors"""
    print("\n6️⃣ ERROR HANDLING")
    print("-" * 50)

    def process_user_input(email: str, file_size: int):
        """Process user input with validation"""
        try:
            # Validate email
            validate_email(email)
            print(f"  ✅ Email validated: {email}")

            # Validate file size
            validate_file_size(file_size)
            print(f"  ✅ File size validated: {file_size} bytes")

            # If we get here, all validation passed
            return {"success": True, "message": "Input validated"}

        except ValidationException as e:
            # ValidationException has structured error info
            print(f"  ❌ Validation failed: {e.message}")
            print(f"     Field: {e.details.get('field', 'unknown')}")
            print(f"     Reason: {e.details.get('reason', 'unknown')}")

            # Return error info (perfect for API responses)
            return e.to_dict()

    # Test with valid input
    print("Valid input:")
    result = process_user_input("user@example.com", 5 * 1024 * 1024)

    # Test with invalid email
    print("\nInvalid email:")
    result = process_user_input("not-an-email", 5 * 1024 * 1024)

    # Test with too large file
    print("\nToo large file:")
    result = process_user_input("user@example.com", 200 * 1024 * 1024)


def main():
    print("=" * 80)
    print("EXAMPLE 5: INPUT VALIDATION")
    print("=" * 80)

    email_validation_example()
    file_validation_example()
    hash_validation_example()
    ethereum_address_example()
    advanced_validation_example()
    error_handling_example()

    print("\n" + "=" * 80)
    print("✅ Example complete!")
    print("\nKey Takeaways:")
    print("- All validators raise ValidationException on failure")
    print("- Use raise_exception=False to get boolean instead")
    print("- ValidationException.to_dict() is perfect for API responses")
    print("- Validators check format, not actual validity (e.g., email exists)")
    print("- Combine validators for complete input validation")
    print("=" * 80)


if __name__ == "__main__":
    main()
