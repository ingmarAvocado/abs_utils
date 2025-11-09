"""
Integration tests for async crypto operations
"""
import pytest
import asyncio
import tempfile
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from abs_utils import crypto


class TestAsyncCryptoOperations:
    """Test async crypto operations under load"""

    @pytest.mark.asyncio
    async def test_concurrent_file_hashing(self, temp_dir):
        """Test hashing multiple files concurrently"""
        # Create multiple test files
        files = []
        for i in range(10):
            file_path = temp_dir / f"test_file_{i}.txt"
            file_path.write_text(f"Content for file {i}" * 100)
            files.append(file_path)

        # Hash all files concurrently
        tasks = [crypto.hash_file_async(f) for f in files]
        results = await asyncio.gather(*tasks)

        # Verify all hashes are unique (different content)
        assert len(set(results)) == 10
        assert all(r.startswith("0x") for r in results)

    @pytest.mark.asyncio
    async def test_same_file_concurrent_hashing(self, temp_file):
        """Test hashing same file multiple times concurrently"""
        # Hash same file 20 times concurrently
        tasks = [crypto.hash_file_async(temp_file) for _ in range(20)]
        results = await asyncio.gather(*tasks)

        # All hashes should be identical
        assert len(set(results)) == 1
        assert results[0].startswith("0x")

    @pytest.mark.asyncio
    async def test_mixed_sync_async_operations(self, temp_file):
        """Test mixing sync and async operations"""
        # Get sync hash first
        sync_hash = crypto.hash_file(temp_file)

        # Run async operations
        async_tasks = [
            crypto.hash_file_async(temp_file),
            crypto.hash_bytes_async(b"test data"),
            crypto.hash_file_async(temp_file)
        ]
        async_results = await asyncio.gather(*async_tasks)

        # Verify file hashes match
        assert async_results[0] == sync_hash
        assert async_results[2] == sync_hash

    @pytest.mark.asyncio
    async def test_large_file_async_performance(self, temp_dir):
        """Test async hashing performance with large files"""
        # Create a large file (5MB)
        large_file = temp_dir / "large_file.bin"
        large_file.write_bytes(os.urandom(5 * 1024 * 1024))

        # Time the async operation
        import time
        start = time.time()
        hash_result = await crypto.hash_file_async(large_file)
        async_time = time.time() - start

        assert hash_result.startswith("0x")
        assert len(hash_result) == 66

        # Compare with sync version
        start = time.time()
        sync_result = crypto.hash_file(large_file)
        sync_time = time.time() - start

        assert hash_result == sync_result
        # Async shouldn't be significantly slower
        assert async_time < sync_time * 2

    @pytest.mark.asyncio
    async def test_async_bytes_hashing_concurrent(self):
        """Test concurrent bytes hashing"""
        # Create different byte sequences
        data_list = [
            b"data_" + str(i).encode() * 100
            for i in range(20)
        ]

        # Hash all concurrently
        tasks = [crypto.hash_bytes_async(data) for data in data_list]
        results = await asyncio.gather(*tasks)

        # All should be different (different data)
        assert len(set(results)) == 20
        assert all(r.startswith("0x") for r in results)

    @pytest.mark.asyncio
    async def test_async_with_exceptions(self, temp_dir):
        """Test async operations with error handling"""
        valid_file = temp_dir / "valid.txt"
        valid_file.write_text("valid content")

        tasks = [
            crypto.hash_file_async(valid_file),
            crypto.hash_file_async("/nonexistent/file.txt"),  # Will fail
            crypto.hash_bytes_async(b"test"),
        ]

        # Gather with return_exceptions=True to handle errors
        results = await asyncio.gather(*tasks, return_exceptions=True)

        assert results[0].startswith("0x")  # Valid file hash
        assert isinstance(results[1], Exception)  # FileNotFoundError
        assert results[2].startswith("0x")  # Valid bytes hash

    @pytest.mark.asyncio
    async def test_async_api_key_generation_uniqueness(self):
        """Test that API keys generated concurrently are unique"""
        # Generate 100 API keys concurrently
        async def generate_key():
            # Run in executor since generate_api_key is sync
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, crypto.generate_api_key, "test")

        tasks = [generate_key() for _ in range(100)]
        results = await asyncio.gather(*tasks)

        # Extract full keys and hashes
        full_keys = [r[0] for r in results]
        key_hashes = [r[1] for r in results]

        # All should be unique
        assert len(set(full_keys)) == 100
        assert len(set(key_hashes)) == 100

    @pytest.mark.asyncio
    async def test_async_hash_verification(self, temp_file):
        """Test hash verification with async operations"""
        # Get hash asynchronously
        file_hash = await crypto.hash_file_async(temp_file)

        # Read file content and verify
        content = temp_file.read_bytes()

        # Verify using sync function (since verify_hash is sync)
        assert crypto.verify_hash(content, file_hash)

        # Test with wrong hash
        wrong_hash = "0x" + "0" * 64
        assert not crypto.verify_hash(content, wrong_hash)

    @pytest.mark.asyncio
    async def test_async_with_different_chunk_sizes(self, temp_dir):
        """Test async hashing with different chunk sizes"""
        # Create a medium file
        test_file = temp_dir / "chunk_test.bin"
        test_file.write_bytes(os.urandom(1024 * 1024))  # 1MB

        # Hash with different chunk sizes
        tasks = [
            crypto.hash_file_async(test_file, chunk_size=1024),
            crypto.hash_file_async(test_file, chunk_size=4096),
            crypto.hash_file_async(test_file, chunk_size=8192),
            crypto.hash_file_async(test_file, chunk_size=16384),
        ]
        results = await asyncio.gather(*tasks)

        # All should produce same hash
        assert len(set(results)) == 1

    @pytest.mark.asyncio
    async def test_async_empty_data_edge_cases(self):
        """Test async operations with empty data"""
        # Empty bytes
        empty_hash = await crypto.hash_bytes_async(b"")
        expected = "0xe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert empty_hash == expected

        # Empty file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = Path(f.name)

        try:
            file_hash = await crypto.hash_file_async(temp_path)
            assert file_hash == expected
        finally:
            temp_path.unlink()

    @pytest.mark.asyncio
    async def test_cancellation_handling(self, temp_dir):
        """Test handling of cancelled async operations"""
        # Create a large file
        large_file = temp_dir / "large.bin"
        large_file.write_bytes(os.urandom(10 * 1024 * 1024))  # 10MB

        # Start hashing and cancel
        task = asyncio.create_task(crypto.hash_file_async(large_file))

        # Give it a moment to start
        await asyncio.sleep(0.01)

        # Cancel the task
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task