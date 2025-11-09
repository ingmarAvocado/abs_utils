"""
Async-compatible cryptographic utilities for hashing, API key generation, etc.
"""

import asyncio
import hashlib
import secrets
from pathlib import Path


async def hash_file_async(file_path: str | Path, chunk_size: int = 8192) -> str:
    """
    Calculate SHA-256 hash of a file asynchronously

    Args:
        file_path: Path to the file
        chunk_size: Size of chunks to read (default: 8KB)

    Returns:
        Hexadecimal hash string (0x-prefixed, 66 chars)
    """
    file_path = Path(file_path)

    def _hash_file() -> str:
        """Synchronous file hashing for thread executor"""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        return "0x" + sha256.hexdigest()

    # Run in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _hash_file)


def hash_file(file_path: str | Path, chunk_size: int = 8192) -> str:
    """
    Calculate SHA-256 hash of a file (synchronous version)

    Args:
        file_path: Path to the file
        chunk_size: Size of chunks to read (default: 8KB)

    Returns:
        Hexadecimal hash string (0x-prefixed, 66 chars)
    """
    file_path = Path(file_path)
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)

    return "0x" + sha256.hexdigest()


async def hash_bytes_async(data: bytes) -> str:
    """
    Calculate SHA-256 hash of bytes asynchronously

    Args:
        data: Bytes to hash

    Returns:
        Hexadecimal hash string (0x-prefixed, 66 chars)
    """

    def _hash() -> str:
        return "0x" + hashlib.sha256(data).hexdigest()

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _hash)


def hash_string(data: str, encoding: str = "utf-8") -> str:
    """
    Calculate SHA-256 hash of a string

    Args:
        data: String to hash
        encoding: Character encoding (default: utf-8)

    Returns:
        Hexadecimal hash string (0x-prefixed, 66 chars)
    """
    return "0x" + hashlib.sha256(data.encode(encoding)).hexdigest()


def hash_bytes(data: bytes) -> str:
    """
    Calculate SHA-256 hash of bytes

    Args:
        data: Bytes to hash

    Returns:
        Hexadecimal hash string (0x-prefixed, 66 chars)
    """
    return "0x" + hashlib.sha256(data).hexdigest()


def verify_hash(data: str | bytes, expected_hash: str, encoding: str = "utf-8") -> bool:
    """
    Verify that data matches expected hash

    Args:
        data: String or bytes to verify
        expected_hash: Expected hash (0x-prefixed or not)
        encoding: Character encoding if data is string

    Returns:
        True if hash matches, False otherwise
    """
    # Normalize expected hash (remove 0x prefix if present)
    expected = expected_hash.lower().removeprefix("0x")

    # Calculate actual hash
    if isinstance(data, str):
        actual = hash_string(data, encoding).removeprefix("0x")
    else:
        actual = hash_bytes(data).removeprefix("0x")

    return actual == expected


def generate_api_key(prefix: str = "sk_live") -> tuple[str, str, str]:
    """
    Generate a secure API key

    Args:
        prefix: API key prefix for identification

    Returns:
        Tuple of (full_key, key_hash, display_prefix)

    Example:
        >>> key, key_hash, prefix = generate_api_key("sk_live")
        >>> print(key)  # sk_live_a1b2c3d4e5f6...
        >>> print(prefix)  # sk_live_a1b2
    """
    # Generate random key (32 bytes = 64 hex chars)
    random_part = secrets.token_hex(32)
    full_key = f"{prefix}_{random_part}"

    # Hash the key for storage
    key_hash = hash_string(full_key)

    # Extract display prefix (first 4 chars of random part)
    display_prefix = f"{prefix}_{random_part[:8]}"

    return full_key, key_hash, display_prefix
