"""
Unit tests for crypto module
"""
import pytest
import asyncio
from pathlib import Path
import hashlib
from abs_utils import crypto


class TestHashFile:
    """Test file hashing functions"""

    def test_hash_file_sync(self, temp_file: Path):
        """Test synchronous file hashing"""
        result = crypto.hash_file(temp_file)
        assert result.startswith("0x")
        assert len(result) == 66  # "0x" + 64 hex chars

    @pytest.mark.asyncio
    async def test_hash_file_async(self, temp_file: Path):
        """Test asynchronous file hashing"""
        result = await crypto.hash_file_async(temp_file)
        assert result.startswith("0x")
        assert len(result) == 66

    @pytest.mark.asyncio
    async def test_hash_file_async_equals_sync(self, temp_file: Path):
        """Test that async and sync hashing produce same result"""
        sync_hash = crypto.hash_file(temp_file)
        async_hash = await crypto.hash_file_async(temp_file)
        assert sync_hash == async_hash

    def test_hash_file_with_custom_chunk_size(self, temp_file: Path):
        """Test file hashing with custom chunk size"""
        result1 = crypto.hash_file(temp_file, chunk_size=1024)
        result2 = crypto.hash_file(temp_file, chunk_size=4096)
        assert result1 == result2

    def test_hash_file_nonexistent(self):
        """Test hashing non-existent file raises error"""
        with pytest.raises(FileNotFoundError):
            crypto.hash_file("/nonexistent/file.txt")

    @pytest.mark.asyncio
    async def test_hash_file_async_nonexistent(self):
        """Test async hashing non-existent file raises error"""
        with pytest.raises(FileNotFoundError):
            await crypto.hash_file_async("/nonexistent/file.txt")

    def test_hash_empty_file(self, temp_dir: Path):
        """Test hashing empty file"""
        empty_file = temp_dir / "empty.txt"
        empty_file.touch()
        result = crypto.hash_file(empty_file)
        # SHA-256 of empty string
        expected = "0xe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert result == expected

    @pytest.mark.asyncio
    async def test_hash_large_file(self, large_file: Path):
        """Test hashing large file"""
        result = await crypto.hash_file_async(large_file)
        assert result.startswith("0x")
        assert len(result) == 66


class TestHashString:
    """Test string hashing functions"""

    def test_hash_string_basic(self):
        """Test basic string hashing"""
        result = crypto.hash_string("test")
        assert result.startswith("0x")
        assert len(result) == 66

    def test_hash_string_empty(self):
        """Test hashing empty string"""
        result = crypto.hash_string("")
        expected = "0xe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert result == expected

    def test_hash_string_unicode(self):
        """Test hashing unicode string"""
        result = crypto.hash_string("Hello 世界 🌍")
        assert result.startswith("0x")
        assert len(result) == 66

    def test_hash_string_custom_encoding(self):
        """Test hashing with custom encoding"""
        text = "Test string"
        utf8_hash = crypto.hash_string(text, encoding="utf-8")
        utf16_hash = crypto.hash_string(text, encoding="utf-16")
        assert utf8_hash != utf16_hash

    def test_hash_string_deterministic(self):
        """Test that hashing is deterministic"""
        text = "Deterministic test"
        hash1 = crypto.hash_string(text)
        hash2 = crypto.hash_string(text)
        assert hash1 == hash2


class TestHashBytes:
    """Test bytes hashing functions"""

    def test_hash_bytes_basic(self, sample_bytes: bytes):
        """Test basic bytes hashing"""
        result = crypto.hash_bytes(sample_bytes)
        assert result.startswith("0x")
        assert len(result) == 66

    def test_hash_bytes_empty(self):
        """Test hashing empty bytes"""
        result = crypto.hash_bytes(b"")
        expected = "0xe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert result == expected

    @pytest.mark.asyncio
    async def test_hash_bytes_async(self, sample_bytes: bytes):
        """Test async bytes hashing"""
        result = await crypto.hash_bytes_async(sample_bytes)
        assert result.startswith("0x")
        assert len(result) == 66

    @pytest.mark.asyncio
    async def test_hash_bytes_async_equals_sync(self, sample_bytes: bytes):
        """Test that async and sync bytes hashing produce same result"""
        sync_hash = crypto.hash_bytes(sample_bytes)
        async_hash = await crypto.hash_bytes_async(sample_bytes)
        assert sync_hash == async_hash


class TestVerifyHash:
    """Test hash verification functions"""

    def test_verify_hash_string_valid(self):
        """Test verifying valid string hash"""
        data = "test data"
        expected_hash = crypto.hash_string(data)
        assert crypto.verify_hash(data, expected_hash)

    def test_verify_hash_string_invalid(self):
        """Test verifying invalid string hash"""
        data = "test data"
        invalid_hash = "0x" + "a" * 64
        assert not crypto.verify_hash(data, invalid_hash)

    def test_verify_hash_bytes_valid(self, sample_bytes: bytes):
        """Test verifying valid bytes hash"""
        expected_hash = crypto.hash_bytes(sample_bytes)
        assert crypto.verify_hash(sample_bytes, expected_hash)

    def test_verify_hash_without_prefix(self):
        """Test verifying hash without 0x prefix"""
        data = "test"
        hash_with_prefix = crypto.hash_string(data)
        hash_without_prefix = hash_with_prefix[2:]  # Remove "0x"
        assert crypto.verify_hash(data, hash_without_prefix)

    def test_verify_hash_case_insensitive(self):
        """Test that hash verification is case-insensitive"""
        data = "test"
        hash_lower = crypto.hash_string(data).lower()
        hash_upper = hash_lower.upper()
        assert crypto.verify_hash(data, hash_upper)

    def test_verify_hash_custom_encoding(self):
        """Test verify hash with custom encoding"""
        data = "Test 世界"
        hash_utf8 = crypto.hash_string(data, encoding="utf-8")
        assert crypto.verify_hash(data, hash_utf8, encoding="utf-8")
        assert not crypto.verify_hash(data, hash_utf8, encoding="utf-16")


class TestGenerateApiKey:
    """Test API key generation"""

    def test_generate_api_key_default(self):
        """Test generating API key with default prefix"""
        full_key, key_hash, display_prefix = crypto.generate_api_key()
        assert full_key.startswith("sk_live_")
        assert key_hash.startswith("0x")
        assert len(key_hash) == 66
        assert display_prefix.startswith("sk_live_")
        assert len(display_prefix) == 16  # "sk_live_" + 8 chars

    def test_generate_api_key_custom_prefix(self, api_key_prefix: str):
        """Test generating API key with custom prefix"""
        full_key, key_hash, display_prefix = crypto.generate_api_key(api_key_prefix)
        assert full_key.startswith(f"{api_key_prefix}_")
        assert key_hash.startswith("0x")
        assert display_prefix.startswith(f"{api_key_prefix}_")

    def test_generate_api_key_unique(self):
        """Test that generated API keys are unique"""
        keys = set()
        hashes = set()
        for _ in range(100):
            full_key, key_hash, _ = crypto.generate_api_key()
            keys.add(full_key)
            hashes.add(key_hash)
        assert len(keys) == 100
        assert len(hashes) == 100

    def test_generate_api_key_verify(self):
        """Test that generated API key can be verified"""
        full_key, key_hash, _ = crypto.generate_api_key()
        # The hash of the full key should match the stored hash
        computed_hash = crypto.hash_string(full_key)
        assert computed_hash == key_hash

    def test_generate_api_key_length(self):
        """Test API key length"""
        full_key, _, _ = crypto.generate_api_key("test")
        # "test_" + 64 hex chars = 69 chars total
        assert len(full_key) == 69

    def test_generate_api_key_display_prefix_extraction(self):
        """Test that display prefix is properly extracted"""
        full_key, _, display_prefix = crypto.generate_api_key("api")
        # Display prefix should be first 8 chars of random part
        random_part = full_key.split("_", 1)[1]
        expected_prefix = f"api_{random_part[:8]}"
        assert display_prefix == expected_prefix