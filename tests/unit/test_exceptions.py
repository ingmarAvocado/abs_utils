"""
Unit tests for exceptions module
"""
import pytest
from typing import Any
from abs_utils import exceptions


class TestNotaryException:
    """Test base NotaryException"""

    def test_create_with_message_only(self):
        """Test creating exception with just message"""
        exc = exceptions.NotaryException("Test error")
        assert exc.message == "Test error"
        assert exc.code == "NotaryException"
        assert exc.details == {}

    def test_create_with_code(self):
        """Test creating exception with custom code"""
        exc = exceptions.NotaryException("Test error", code="CUSTOM_ERROR")
        assert exc.message == "Test error"
        assert exc.code == "CUSTOM_ERROR"
        assert exc.details == {}

    def test_create_with_details(self):
        """Test creating exception with details"""
        details = {"key": "value", "count": 42}
        exc = exceptions.NotaryException("Test error", details=details)
        assert exc.message == "Test error"
        assert exc.details == details

    def test_to_dict(self):
        """Test converting exception to dictionary"""
        exc = exceptions.NotaryException(
            "Test error",
            code="TEST_CODE",
            details={"field": "value"}
        )
        result = exc.to_dict()
        assert result == {
            "error": "TEST_CODE",
            "message": "Test error",
            "details": {"field": "value"}
        }

    def test_str_representation(self):
        """Test string representation"""
        exc = exceptions.NotaryException("Test error")
        assert str(exc) == "Test error"


class TestDocumentNotFoundException:
    """Test DocumentNotFoundException"""

    def test_with_int_id(self):
        """Test with integer document ID"""
        exc = exceptions.DocumentNotFoundException(123)
        assert exc.message == "Document not found: 123"
        assert exc.code == "DOCUMENT_NOT_FOUND"
        assert exc.details == {"document_id": 123}

    def test_with_string_id(self):
        """Test with string document ID"""
        exc = exceptions.DocumentNotFoundException("abc-123")
        assert exc.message == "Document not found: abc-123"
        assert exc.code == "DOCUMENT_NOT_FOUND"
        assert exc.details == {"document_id": "abc-123"}

    def test_to_dict(self):
        """Test converting to dictionary"""
        exc = exceptions.DocumentNotFoundException(456)
        result = exc.to_dict()
        assert result == {
            "error": "DOCUMENT_NOT_FOUND",
            "message": "Document not found: 456",
            "details": {"document_id": 456}
        }


class TestDocumentAlreadyExistsException:
    """Test DocumentAlreadyExistsException"""

    def test_with_hash(self):
        """Test with file hash"""
        hash_value = "0x123abc"
        exc = exceptions.DocumentAlreadyExistsException(hash_value)
        assert exc.message == f"Document with hash {hash_value} already exists"
        assert exc.code == "DOCUMENT_ALREADY_EXISTS"
        assert exc.details == {"file_hash": hash_value}


class TestBlockchainException:
    """Test BlockchainException"""

    def test_basic(self):
        """Test basic blockchain exception"""
        exc = exceptions.BlockchainException("Transaction failed")
        assert exc.message == "Transaction failed"
        assert exc.code == "BLOCKCHAIN_ERROR"

    def test_with_transaction_details(self):
        """Test with transaction details"""
        exc = exceptions.BlockchainException(
            "Transaction failed",
            transaction_hash="0xabc123",
            network="polygon"
        )
        assert exc.details == {
            "transaction_hash": "0xabc123",
            "network": "polygon"
        }


class TestTransactionFailedException:
    """Test TransactionFailedException"""

    def test_with_tx_hash(self):
        """Test with transaction hash"""
        tx_hash = "0x789def"
        reason = "Out of gas"
        exc = exceptions.TransactionFailedException(tx_hash, reason)
        assert exc.message == f"Transaction {tx_hash} failed: {reason}"
        assert exc.code == "TRANSACTION_FAILED"
        assert exc.details == {"transaction_hash": tx_hash, "reason": reason}


class TestInvalidNetworkException:
    """Test InvalidNetworkException"""

    def test_with_supported_networks(self):
        """Test with list of supported networks"""
        supported = ["polygon", "ethereum"]
        exc = exceptions.InvalidNetworkException("bsc", supported)
        assert exc.message == "Invalid network: bsc"
        assert exc.code == "INVALID_NETWORK"
        assert exc.details == {
            "network": "bsc",
            "supported_networks": supported
        }


class TestValidationException:
    """Test ValidationException"""

    def test_basic(self):
        """Test basic validation exception"""
        exc = exceptions.ValidationException("email", "Invalid email format")
        assert exc.message == "Validation failed for field 'email': Invalid email format"
        assert exc.code == "VALIDATION_ERROR"
        assert exc.details == {
            "field": "email",
            "reason": "Invalid email format"
        }

    def test_with_none_field(self):
        """Test with None field"""
        exc = exceptions.ValidationException(None, "General validation error")
        assert exc.message == "Validation failed: General validation error"
        assert exc.details == {"field": None, "reason": "General validation error"}


class TestAuthenticationException:
    """Test AuthenticationException"""

    def test_basic(self):
        """Test basic authentication exception"""
        exc = exceptions.AuthenticationException("Invalid credentials")
        assert exc.message == "Invalid credentials"
        assert exc.code == "AUTHENTICATION_ERROR"

    def test_with_user_details(self):
        """Test with user details"""
        exc = exceptions.AuthenticationException(
            "Login failed",
            user_id="user123"
        )
        assert exc.details == {"user_id": "user123"}


class TestAuthorizationException:
    """Test AuthorizationException"""

    def test_basic(self):
        """Test basic authorization exception"""
        exc = exceptions.AuthorizationException("Access denied")
        assert exc.message == "Access denied"
        assert exc.code == "AUTHORIZATION_ERROR"

    def test_with_resource_details(self):
        """Test with resource details"""
        exc = exceptions.AuthorizationException(
            "Cannot access resource",
            resource="document",
            action="delete"
        )
        assert exc.details == {
            "resource": "document",
            "action": "delete"
        }


class TestRateLimitException:
    """Test RateLimitException"""

    def test_with_limit_details(self):
        """Test with rate limit details"""
        exc = exceptions.RateLimitException(60, 100)
        assert exc.message == "Rate limit exceeded. Retry after 60 seconds"
        assert exc.code == "RATE_LIMIT_EXCEEDED"
        assert exc.details == {
            "retry_after": 60,
            "limit": 100
        }

    def test_without_limit(self):
        """Test without limit parameter"""
        exc = exceptions.RateLimitException(30)
        assert exc.message == "Rate limit exceeded. Retry after 30 seconds"
        assert exc.details == {
            "retry_after": 30,
            "limit": None
        }


class TestAPIKeyException:
    """Test APIKeyException"""

    def test_basic(self):
        """Test basic API key exception"""
        exc = exceptions.APIKeyException("Invalid API key")
        assert exc.message == "Invalid API key"
        assert exc.code == "API_KEY_ERROR"

    def test_with_key_prefix(self):
        """Test with API key prefix details"""
        exc = exceptions.APIKeyException(
            "API key expired",
            key_prefix="sk_test_"
        )
        assert exc.details == {"key_prefix": "sk_test_"}


class TestStorageException:
    """Test StorageException"""

    def test_basic(self):
        """Test basic storage exception"""
        exc = exceptions.StorageException("File upload failed")
        assert exc.message == "File upload failed"
        assert exc.code == "STORAGE_ERROR"

    def test_with_file_details(self):
        """Test with file details"""
        exc = exceptions.StorageException(
            "Storage quota exceeded",
            file_name="document.pdf",
            size_mb=150
        )
        assert exc.details == {
            "file_name": "document.pdf",
            "size_mb": 150
        }


class TestExceptionInheritance:
    """Test that all exceptions inherit from NotaryException"""

    def test_all_inherit_from_base(self):
        """Test all custom exceptions inherit from NotaryException"""
        exception_classes = [
            exceptions.DocumentNotFoundException,
            exceptions.DocumentAlreadyExistsException,
            exceptions.BlockchainException,
            exceptions.TransactionFailedException,
            exceptions.InvalidNetworkException,
            exceptions.ValidationException,
            exceptions.AuthenticationException,
            exceptions.AuthorizationException,
            exceptions.RateLimitException,
            exceptions.APIKeyException,
            exceptions.StorageException
        ]

        for exc_class in exception_classes:
            assert issubclass(exc_class, exceptions.NotaryException)

    def test_can_catch_with_base(self):
        """Test that all exceptions can be caught with base exception"""
        try:
            raise exceptions.DocumentNotFoundException(123)
        except exceptions.NotaryException as e:
            assert e.code == "DOCUMENT_NOT_FOUND"

        try:
            raise exceptions.ValidationException("field", "error")
        except exceptions.NotaryException as e:
            assert e.code == "VALIDATION_ERROR"