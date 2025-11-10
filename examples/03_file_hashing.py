#!/usr/bin/env python3
"""
Example 3: File Hashing (Sync and Async)

This example shows:
- How to hash files synchronously
- How to hash files asynchronously
- How to hash strings and bytes
- How to verify hashes
"""

import asyncio
import tempfile
from pathlib import Path
from abs_utils.crypto import (
    hash_file,
    hash_file_async,
    hash_string,
    hash_bytes,
    verify_hash,
)


def create_sample_file(content: str) -> Path:
    """Create a temporary file with content"""
    temp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
    temp.write(content)
    temp.close()
    return Path(temp.name)


async def async_example():
    """Async hashing example"""
    print("\n2️⃣ ASYNC FILE HASHING")
    print("-" * 50)

    # Create multiple test files
    files = {
        "file1.txt": "Hello, World!",
        "file2.txt": "This is a test file",
        "file3.txt": "Another test file",
    }

    file_paths = []
    for name, content in files.items():
        path = create_sample_file(content)
        file_paths.append((name, path))

    print(f"Created {len(file_paths)} test files\n")

    # Hash all files concurrently
    print("Hashing files concurrently...")
    tasks = [hash_file_async(path) for _, path in file_paths]
    hashes = await asyncio.gather(*tasks)

    for (name, path), file_hash in zip(file_paths, hashes):
        print(f"  {name:15} -> {file_hash}")
        path.unlink()  # Clean up

    print("\n✅ All files hashed concurrently!")


def sync_example():
    """Sync hashing example"""
    print("1️⃣ SYNCHRONOUS FILE HASHING")
    print("-" * 50)

    # Create a test file
    content = "The quick brown fox jumps over the lazy dog"
    file_path = create_sample_file(content)

    print(f"Created file: {file_path}")
    print(f"Content: '{content}'\n")

    # Hash the file
    file_hash = hash_file(file_path)
    print(f"File hash: {file_hash}")

    # Hash the same content as string
    string_hash = hash_string(content)
    print(f"String hash: {string_hash}")

    # Verify they match
    if file_hash == string_hash:
        print("✅ File hash matches string hash!")
    else:
        print("❌ Hashes don't match (this shouldn't happen)")

    # Clean up
    file_path.unlink()


def string_and_bytes_example():
    """String and bytes hashing"""
    print("\n3️⃣ STRING AND BYTES HASHING")
    print("-" * 50)

    # Hash a string
    text = "Hello, Blockchain!"
    text_hash = hash_string(text)
    print(f"String: '{text}'")
    print(f"Hash:   {text_hash}\n")

    # Hash bytes
    data = b"Binary data: \x00\x01\x02\x03"
    bytes_hash = hash_bytes(data)
    print(f"Bytes:  {data}")
    print(f"Hash:   {bytes_hash}\n")

    # Verify hash
    print("Verifying hash...")
    is_valid = verify_hash(text, text_hash)
    print(f"✅ Hash verification: {is_valid}")

    # Try wrong data
    is_valid_wrong = verify_hash("Wrong data", text_hash)
    print(f"❌ Wrong data verification: {is_valid_wrong}")


def hash_properties():
    """Demonstrate hash properties"""
    print("\n4️⃣ HASH PROPERTIES")
    print("-" * 50)

    # Same input = same output
    hash1 = hash_string("test")
    hash2 = hash_string("test")
    print(f"Hash('test') = {hash1}")
    print(f"Hash('test') = {hash2}")
    print(f"✅ Deterministic: {hash1 == hash2}\n")

    # Small change = completely different hash
    hash_a = hash_string("Hello")
    hash_b = hash_string("hello")  # Just lowercase 'h'
    print(f"Hash('Hello') = {hash_a}")
    print(f"Hash('hello') = {hash_b}")
    print(f"✅ Avalanche effect: Hashes are completely different\n")

    # Fixed length output
    short_hash = hash_string("a")
    long_hash = hash_string("a" * 10000)
    print(f"Hash of 1 char:      {len(short_hash)} characters")
    print(f"Hash of 10000 chars: {len(long_hash)} characters")
    print(f"✅ Fixed length: Both are 66 characters (0x + 64 hex)")


def main():
    print("=" * 80)
    print("EXAMPLE 3: FILE HASHING")
    print("=" * 80)
    print()

    # Run sync example
    sync_example()

    # Run async example
    asyncio.run(async_example())

    # String and bytes
    string_and_bytes_example()

    # Hash properties
    hash_properties()

    print("\n" + "=" * 80)
    print("✅ Example complete!")
    print("\nKey Takeaways:")
    print("- Use hash_file() for sync, hash_file_async() for async")
    print("- All hashes are SHA-256 (0x-prefixed, 66 chars)")
    print("- Hashes are deterministic and irreversible")
    print("- Use hash_file_async() for large files to avoid blocking")
    print("=" * 80)


if __name__ == "__main__":
    main()
