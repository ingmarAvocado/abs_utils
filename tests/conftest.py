"""
Test fixtures and configuration for abs_utils tests
"""
import pytest
import tempfile
import os
from pathlib import Path
import asyncio
from typing import Generator, AsyncGenerator


@pytest.fixture
def temp_file() -> Generator[Path, None, None]:
    """Create a temporary file for testing"""
    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
        f.write(b"Test content for hashing")
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_bytes() -> bytes:
    """Sample bytes for testing"""
    return b"Sample data for testing hash functions"


@pytest.fixture
def sample_string() -> str:
    """Sample string for testing"""
    return "Sample string for testing hash functions"


@pytest.fixture
def sample_hash() -> str:
    """Known hash for sample string"""
    # SHA-256 hash of "Sample string for testing hash functions"
    return "0x2a8b9c7d5e3f1a4b6c8d9e0f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b"


@pytest.fixture
def api_key_prefix() -> str:
    """API key prefix for testing"""
    return "sk_test"


@pytest.fixture
def sample_email() -> str:
    """Valid email for testing"""
    return "test@example.com"


@pytest.fixture
def invalid_email() -> str:
    """Invalid email for testing"""
    return "invalid-email"


@pytest.fixture
def ethereum_address() -> str:
    """Valid Ethereum address for testing"""
    return "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"


@pytest.fixture
def invalid_ethereum_address() -> str:
    """Invalid Ethereum address for testing"""
    return "0xinvalid"


@pytest.fixture
def large_file(temp_dir: Path) -> Path:
    """Create a large file for testing"""
    large_file_path = temp_dir / "large_file.bin"
    # Create a 10MB file
    with open(large_file_path, 'wb') as f:
        f.write(os.urandom(10 * 1024 * 1024))
    return large_file_path


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for config testing"""
    monkeypatch.setenv("MAX_FILE_SIZE", "200000000")
    monkeypatch.setenv("DEFAULT_GAS_LIMIT", "400000")
    monkeypatch.setenv("JWT_ALGORITHM", "HS512")
    return monkeypatch