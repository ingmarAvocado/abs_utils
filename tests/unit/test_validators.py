"""
Unit tests for validators module
"""
import pytest
from abs_utils import validators
from abs_utils.exceptions import ValidationException
from abs_utils.constants import MAX_FILE_SIZE


class TestValidateEmail:
    """Test email validation"""

    def test_valid_emails(self):
        """Test valid email addresses"""
        valid_emails = [
            "user@example.com",
            "test.user@example.com",
            "user+tag@example.co.uk",
            "123@example.org",
            "user_name@example-domain.com",
            "FirstName.LastName@company.io"
        ]
        for email in valid_emails:
            assert validators.validate_email(email, raise_exception=False)

    def test_invalid_emails(self):
        """Test invalid email addresses"""
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user@.com",
            "user@@example.com",
            "user@example",
            "user example@test.com",
            "",
            "user@",
            "@",
            "user..name@example.com"
        ]
        for email in invalid_emails:
            assert not validators.validate_email(email, raise_exception=False)

    def test_raise_exception_on_invalid(self):
        """Test that exception is raised for invalid email when requested"""
        with pytest.raises(ValidationException) as exc_info:
            validators.validate_email("invalid-email")

        assert exc_info.value.code == "VALIDATION_ERROR"
        assert "email" in exc_info.value.details["field"]

    def test_no_exception_when_disabled(self):
        """Test that no exception is raised when raise_exception=False"""
        result = validators.validate_email("invalid", raise_exception=False)
        assert result is False


class TestValidateFileType:
    """Test file type validation"""

    def test_valid_file_types(self):
        """Test valid file types based on extension"""
        valid_files = [
            "document.pdf",
            "image.jpg",
            "photo.jpeg",
            "picture.png",
            "file.txt",
            "Document.PDF",  # Test case insensitive
            "IMAGE.JPG"
        ]
        for file_name in valid_files:
            assert validators.validate_file_type(file_name, raise_exception=False)

    def test_invalid_file_types(self):
        """Test invalid file types"""
        invalid_files = [
            "script.exe",
            "program.bat",
            "archive.zip",
            "spreadsheet.xlsx",
            "noextension",
            "",
            ".hidden"
        ]
        for file_name in invalid_files:
            assert not validators.validate_file_type(file_name, raise_exception=False)

    def test_with_mime_type(self):
        """Test validation with MIME type"""
        # Valid MIME type should pass
        assert validators.validate_file_type(
            "document.pdf",
            mime_type="application/pdf",
            raise_exception=False
        )
        # Even if extension doesn't match, valid MIME type should pass
        assert validators.validate_file_type(
            "wrongext.xyz",
            mime_type="image/jpeg",
            raise_exception=False
        )

    def test_invalid_mime_type(self):
        """Test with invalid MIME type"""
        assert not validators.validate_file_type(
            "file.xyz",
            mime_type="application/x-executable",
            raise_exception=False
        )

    def test_raise_exception_on_invalid_type(self):
        """Test exception raised for invalid file type"""
        with pytest.raises(ValidationException) as exc_info:
            validators.validate_file_type("file.exe")

        assert "file_type" in str(exc_info.value.details)


class TestValidateFileSize:
    """Test file size validation"""

    def test_valid_file_sizes(self):
        """Test valid file sizes"""
        valid_sizes = [
            0,
            1,
            1024,
            1024 * 1024,  # 1MB
            MAX_FILE_SIZE - 1,
            MAX_FILE_SIZE
        ]
        for size in valid_sizes:
            assert validators.validate_file_size(size, raise_exception=False)

    def test_invalid_file_sizes(self):
        """Test invalid file sizes"""
        invalid_sizes = [
            -1,
            -1000,
            MAX_FILE_SIZE + 1,
            MAX_FILE_SIZE * 2,
            10 * 1024 * 1024 * 1024  # 10GB
        ]
        for size in invalid_sizes:
            assert not validators.validate_file_size(size, raise_exception=False)

    def test_custom_max_size(self):
        """Test with custom max size"""
        custom_max = 1024 * 1024  # 1MB
        assert validators.validate_file_size(custom_max - 1, custom_max, raise_exception=False)
        assert validators.validate_file_size(custom_max, custom_max, raise_exception=False)
        assert not validators.validate_file_size(custom_max + 1, custom_max, raise_exception=False)

    def test_raise_exception_on_invalid_size(self):
        """Test exception raised for invalid file size"""
        with pytest.raises(ValidationException) as exc_info:
            validators.validate_file_size(MAX_FILE_SIZE + 1)

        assert "file_size" in str(exc_info.value.details)


class TestValidateHash:
    """Test hash validation"""

    def test_valid_hashes(self):
        """Test valid hash formats"""
        valid_hashes = [
            "0x" + "a" * 64,
            "0x" + "0" * 64,
            "0x" + "f" * 64,
            "0x" + "ABC123def" * 7 + "abcd1234",  # Mixed case
            "a" * 64,  # Without 0x prefix
            "0" * 64
        ]
        for hash_value in valid_hashes:
            assert validators.validate_hash(hash_value, raise_exception=False)

    def test_invalid_hashes(self):
        """Test invalid hash formats"""
        invalid_hashes = [
            "",
            "0x",
            "0x" + "g" * 64,  # Invalid hex char
            "0x" + "a" * 63,  # Too short
            "0x" + "a" * 65,  # Too long
            "not-a-hash",
            "0xZZZ",
            " " + "a" * 64,  # Leading space
            "a" * 64 + " "   # Trailing space
        ]
        for hash_value in invalid_hashes:
            assert not validators.validate_hash(hash_value, raise_exception=False)

    def test_raise_exception_on_invalid_hash(self):
        """Test exception raised for invalid hash"""
        with pytest.raises(ValidationException) as exc_info:
            validators.validate_hash("invalid-hash")

        assert "hash" in str(exc_info.value.details)


class TestValidateEthereumAddress:
    """Test Ethereum address validation"""

    def test_valid_addresses(self):
        """Test valid Ethereum addresses"""
        valid_addresses = [
            "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
            "0x0000000000000000000000000000000000000000",
            "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
            "0x" + "a" * 40,
            "0x" + "1234567890abcdef" * 2 + "12345678"
        ]
        for address in valid_addresses:
            assert validators.validate_ethereum_address(address, raise_exception=False)

    def test_invalid_addresses(self):
        """Test invalid Ethereum addresses"""
        invalid_addresses = [
            "",
            "0x",
            "0x" + "g" * 40,  # Invalid hex
            "0x" + "a" * 39,  # Too short
            "0x" + "a" * 41,  # Too long
            "not-an-address",
            "742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",  # Missing 0x
            "0X" + "a" * 40,  # Capital X
            None
        ]
        for address in invalid_addresses:
            if address is not None:
                assert not validators.validate_ethereum_address(address, raise_exception=False)

    def test_case_insensitive(self):
        """Test that validation is case-insensitive"""
        address_lower = "0x" + "abcdef1234567890" * 2 + "12345678"
        address_upper = address_lower.upper()
        address_mixed = "0x" + "AbCdEf1234567890" * 2 + "12345678"

        assert validators.validate_ethereum_address(address_lower, raise_exception=False)
        assert validators.validate_ethereum_address(address_upper, raise_exception=False)
        assert validators.validate_ethereum_address(address_mixed, raise_exception=False)

    def test_raise_exception_on_invalid_address(self):
        """Test exception raised for invalid address"""
        with pytest.raises(ValidationException) as exc_info:
            validators.validate_ethereum_address("invalid")

        assert "ethereum_address" in str(exc_info.value.details)


class TestValidateUrl:
    """Test URL validation"""

    def test_valid_urls(self):
        """Test valid URLs"""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://subdomain.example.com",
            "https://example.com/path",
            "https://example.com/path/to/resource",
            "https://example.com?query=value",
            "https://example.com#anchor",
            "https://example.com:8080",
            "https://192.168.1.1",
            "https://example.co.uk"
        ]
        for url in valid_urls:
            assert validators.validate_url(url, raise_exception=False)

    def test_invalid_urls(self):
        """Test invalid URLs"""
        invalid_urls = [
            "",
            "not-a-url",
            "ftp://example.com",  # Not http/https
            "//example.com",  # Missing protocol
            "http://",
            "https://",
            "example.com",  # Missing protocol
            "http:/example.com",  # Single slash
            "https://example .com",  # Space
            None
        ]
        for url in invalid_urls:
            if url is not None:
                assert not validators.validate_url(url, raise_exception=False)

    def test_raise_exception_on_invalid_url(self):
        """Test exception raised for invalid URL"""
        with pytest.raises(ValidationException) as exc_info:
            validators.validate_url("not-a-url")

        assert "url" in str(exc_info.value.details)


class TestValidateTransactionHash:
    """Test transaction hash validation"""

    def test_valid_transaction_hashes(self):
        """Test valid transaction hashes"""
        # Transaction hashes are same format as regular hashes
        valid_hashes = [
            "0x" + "a" * 64,
            "0x" + "0" * 64,
            "0x" + "deadbeef" * 8
        ]
        for tx_hash in valid_hashes:
            assert validators.validate_transaction_hash(tx_hash, raise_exception=False)

    def test_invalid_transaction_hashes(self):
        """Test invalid transaction hashes"""
        invalid_hashes = [
            "",
            "0x",
            "0x" + "z" * 64,
            "0x" + "a" * 63,
            "not-a-hash"
        ]
        for tx_hash in invalid_hashes:
            assert not validators.validate_transaction_hash(tx_hash, raise_exception=False)

    def test_raise_exception_on_invalid_tx_hash(self):
        """Test exception raised for invalid transaction hash"""
        with pytest.raises(ValidationException) as exc_info:
            validators.validate_transaction_hash("invalid")

        assert "transaction_hash" in str(exc_info.value.details)


class TestValidateJson:
    """Test JSON validation"""

    def test_valid_json_strings(self):
        """Test valid JSON strings"""
        valid_json = [
            '{}',
            '[]',
            '{"key": "value"}',
            '[1, 2, 3]',
            '{"nested": {"key": "value"}}',
            'true',
            'false',
            'null',
            '123',
            '"string"'
        ]
        for json_str in valid_json:
            result = validators.validate_json(json_str, raise_exception=False)
            assert result is not None

    def test_invalid_json_strings(self):
        """Test invalid JSON strings"""
        invalid_json = [
            '',
            '{',
            '}',
            '{key: "value"}',  # Missing quotes
            "{'key': 'value'}",  # Single quotes
            '{,}',
            'undefined',
            'NaN'
        ]
        for json_str in invalid_json:
            result = validators.validate_json(json_str, raise_exception=False)
            assert result is None

    def test_return_parsed_json(self):
        """Test that parsed JSON is returned"""
        json_str = '{"key": "value", "number": 42}'
        result = validators.validate_json(json_str, raise_exception=False)
        assert result == {"key": "value", "number": 42}

    def test_raise_exception_on_invalid_json(self):
        """Test exception raised for invalid JSON"""
        with pytest.raises(ValidationException) as exc_info:
            validators.validate_json("{invalid}")

        assert "json" in str(exc_info.value.details)