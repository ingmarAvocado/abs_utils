"""
Input validation utilities
"""

import re
from pathlib import Path
from typing import Any

from abs_utils.exceptions import ValidationException
from abs_utils.constants import SUPPORTED_FILE_TYPES, MAX_FILE_SIZE


def validate_email(email: str, raise_exception: bool = True) -> bool:
    """
    Validate email format

    Args:
        email: Email address to validate
        raise_exception: If True, raise ValidationException on invalid email

    Returns:
        True if valid

    Raises:
        ValidationException: If email is invalid and raise_exception=True
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    is_valid = bool(re.match(pattern, email))

    if not is_valid and raise_exception:
        raise ValidationException("email", f"Invalid email format: {email}")

    return is_valid


def validate_file_type(
    file_name: str, mime_type: str | None = None, raise_exception: bool = True
) -> bool:
    """
    Validate file type based on extension or MIME type

    Args:
        file_name: Name of the file
        mime_type: MIME type (optional)
        raise_exception: If True, raise ValidationException on invalid type

    Returns:
        True if valid

    Raises:
        ValidationException: If file type is invalid and raise_exception=True
    """
    # Check MIME type if provided
    if mime_type:
        is_valid = mime_type in SUPPORTED_FILE_TYPES
        if not is_valid and raise_exception:
            raise ValidationException(
                "file_type",
                f"Unsupported MIME type: {mime_type}. Supported: {SUPPORTED_FILE_TYPES}",
            )
        return is_valid

    # Check file extension
    extension = Path(file_name).suffix.lower()
    # Map extensions to MIME types (simplified)
    extension_map = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".json": "application/json",
        ".txt": "text/plain",
    }

    mime = extension_map.get(extension)
    is_valid = mime in SUPPORTED_FILE_TYPES if mime else False

    if not is_valid and raise_exception:
        raise ValidationException(
            "file_type",
            f"Unsupported file extension: {extension}. Supported: {list(extension_map.keys())}",
        )

    return is_valid


def validate_file_size(file_size: int, raise_exception: bool = True) -> bool:
    """
    Validate file size

    Args:
        file_size: File size in bytes
        raise_exception: If True, raise ValidationException if too large

    Returns:
        True if valid

    Raises:
        ValidationException: If file is too large and raise_exception=True
    """
    is_valid = file_size <= MAX_FILE_SIZE

    if not is_valid and raise_exception:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        actual_mb = file_size / (1024 * 1024)
        raise ValidationException(
            "file_size",
            f"File too large: {actual_mb:.2f} MB (max: {max_mb:.2f} MB)",
        )

    return is_valid


def validate_hash(hash_string: str, raise_exception: bool = True) -> bool:
    """
    Validate hash format (0x-prefixed 64 hex characters)

    Args:
        hash_string: Hash string to validate
        raise_exception: If True, raise ValidationException on invalid hash

    Returns:
        True if valid

    Raises:
        ValidationException: If hash is invalid and raise_exception=True
    """
    # Pattern: 0x followed by 64 hex characters
    pattern = r"^0x[a-fA-F0-9]{64}$"
    is_valid = bool(re.match(pattern, hash_string))

    if not is_valid and raise_exception:
        raise ValidationException(
            "hash",
            f"Invalid hash format. Expected: 0x + 64 hex chars, got: {hash_string}",
        )

    return is_valid


def validate_ethereum_address(address: str, raise_exception: bool = True) -> bool:
    """
    Validate Ethereum address format

    Args:
        address: Ethereum address to validate
        raise_exception: If True, raise ValidationException on invalid address

    Returns:
        True if valid

    Raises:
        ValidationException: If address is invalid and raise_exception=True
    """
    # Pattern: 0x followed by 40 hex characters
    pattern = r"^0x[a-fA-F0-9]{40}$"
    is_valid = bool(re.match(pattern, address))

    if not is_valid and raise_exception:
        raise ValidationException(
            "ethereum_address",
            f"Invalid Ethereum address format. Expected: 0x + 40 hex chars, got: {address}",
        )

    return is_valid


def validate_transaction_hash(tx_hash: str, raise_exception: bool = True) -> bool:
    """
    Validate Ethereum transaction hash format

    Args:
        tx_hash: Transaction hash to validate
        raise_exception: If True, raise ValidationException on invalid hash

    Returns:
        True if valid

    Raises:
        ValidationException: If hash is invalid and raise_exception=True
    """
    # Same format as file hash
    return validate_hash(tx_hash, raise_exception)


def validate_required_fields(data: dict[str, Any], required: list[str]) -> None:
    """
    Validate that required fields are present in data

    Args:
        data: Dictionary to validate
        required: List of required field names

    Raises:
        ValidationException: If any required field is missing
    """
    missing = [field for field in required if field not in data or data[field] is None]

    if missing:
        raise ValidationException(
            "required_fields",
            f"Missing required fields: {', '.join(missing)}",
        )


def validate_positive_integer(value: int, field_name: str) -> None:
    """
    Validate that value is a positive integer

    Args:
        value: Value to validate
        field_name: Name of the field (for error messages)

    Raises:
        ValidationException: If value is not a positive integer
    """
    if not isinstance(value, int) or value <= 0:
        raise ValidationException(
            field_name,
            f"Must be a positive integer, got: {value}",
        )


def validate_string_length(
    value: str, field_name: str, min_length: int = 0, max_length: int | None = None
) -> None:
    """
    Validate string length

    Args:
        value: String to validate
        field_name: Name of the field (for error messages)
        min_length: Minimum length (default: 0)
        max_length: Maximum length (default: None = no limit)

    Raises:
        ValidationException: If string length is invalid
    """
    length = len(value)

    if length < min_length:
        raise ValidationException(
            field_name,
            f"Must be at least {min_length} characters, got {length}",
        )

    if max_length is not None and length > max_length:
        raise ValidationException(
            field_name,
            f"Must be at most {max_length} characters, got {length}",
        )
