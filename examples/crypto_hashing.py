#!/usr/bin/env python3
"""
Crypto hashing examples for abs_utils
"""
import asyncio
from pathlib import Path
from abs_utils import crypto


async def main():
    # Create a test file
    test_file = Path("test_document.txt")
    test_file.write_text("This is a test document for hashing.")

    print("=== File Hashing Examples ===\n")

    # Synchronous file hashing
    file_hash = crypto.hash_file(test_file)
    print(f"Sync file hash: {file_hash}")

    # Asynchronous file hashing
    async_hash = await crypto.hash_file_async(test_file)
    print(f"Async file hash: {async_hash}")
    print(f"Hashes match: {file_hash == async_hash}\n")

    print("=== String Hashing Examples ===\n")

    # Hash a string
    text = "Hello, World!"
    text_hash = crypto.hash_string(text)
    print(f"String hash: {text_hash}")

    # Hash with different encoding
    utf16_hash = crypto.hash_string(text, encoding="utf-16")
    print(f"UTF-16 hash: {utf16_hash}")
    print(f"Different encoding produces different hash: {text_hash != utf16_hash}\n")

    print("=== Bytes Hashing Examples ===\n")

    # Hash bytes
    data = b"Binary data for hashing"
    bytes_hash = crypto.hash_bytes(data)
    print(f"Bytes hash: {bytes_hash}")

    # Async bytes hashing
    async_bytes_hash = await crypto.hash_bytes_async(data)
    print(f"Async bytes hash: {async_bytes_hash}")
    print(f"Hashes match: {bytes_hash == async_bytes_hash}\n")

    print("=== Hash Verification ===\n")

    # Verify hash
    is_valid = crypto.verify_hash(text, text_hash)
    print(f"Hash verification (valid): {is_valid}")

    # Try with wrong hash
    wrong_hash = "0x" + "0" * 64
    is_valid = crypto.verify_hash(text, wrong_hash)
    print(f"Hash verification (invalid): {is_valid}")

    # Cleanup
    test_file.unlink()
    print("\nTest file cleaned up.")


if __name__ == "__main__":
    asyncio.run(main())