"""
Custom exceptions for abs_notary project
"""

from typing import Any


class NotaryException(Exception):
    """Base exception for all abs_notary errors"""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API responses"""
        return {
            "error": self.code,
            "message": self.message,
            "details": self.details,
        }


class DocumentNotFoundException(NotaryException):
    """Raised when a document is not found"""

    def __init__(self, document_id: int | str):
        super().__init__(
            message=f"Document not found: {document_id}",
            code="DOCUMENT_NOT_FOUND",
            details={"document_id": document_id},
        )


class DocumentAlreadyExistsException(NotaryException):
    """Raised when attempting to create a document that already exists"""

    def __init__(self, file_hash: str):
        super().__init__(
            message=f"Document with hash {file_hash} already exists",
            code="DOCUMENT_ALREADY_EXISTS",
            details={"file_hash": file_hash},
        )


class BlockchainException(NotaryException):
    """Base exception for blockchain-related errors"""

    pass


class InsufficientGasException(BlockchainException):
    """Raised when there's insufficient gas for a transaction"""

    def __init__(self, required_gas: int, available_gas: int):
        super().__init__(
            message=f"Insufficient gas: required {required_gas}, available {available_gas}",
            code="INSUFFICIENT_GAS",
            details={
                "required_gas": required_gas,
                "available_gas": available_gas,
            },
        )


class TransactionFailedException(BlockchainException):
    """Raised when a blockchain transaction fails"""

    def __init__(self, transaction_hash: str, reason: str | None = None):
        super().__init__(
            message=f"Transaction failed: {transaction_hash}",
            code="TRANSACTION_FAILED",
            details={
                "transaction_hash": transaction_hash,
                "reason": reason,
            },
        )


class InvalidNetworkException(BlockchainException):
    """Raised when an invalid blockchain network is specified"""

    def __init__(self, network: str, supported_networks: list[str]):
        super().__init__(
            message=f"Invalid network: {network}",
            code="INVALID_NETWORK",
            details={
                "network": network,
                "supported_networks": supported_networks,
            },
        )


class ArweaveUploadException(NotaryException):
    """Raised when Arweave upload fails"""

    def __init__(self, file_name: str, reason: str | None = None):
        super().__init__(
            message=f"Failed to upload {file_name} to Arweave",
            code="ARWEAVE_UPLOAD_FAILED",
            details={
                "file_name": file_name,
                "reason": reason,
            },
        )


class ValidationException(NotaryException):
    """Raised when input validation fails"""

    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Validation failed for {field}: {reason}",
            code="VALIDATION_ERROR",
            details={
                "field": field,
                "reason": reason,
            },
        )


class AuthenticationException(NotaryException):
    """Raised when authentication fails"""

    def __init__(self, reason: str = "Invalid credentials"):
        super().__init__(
            message=reason,
            code="AUTHENTICATION_FAILED",
        )


class AuthorizationException(NotaryException):
    """Raised when user lacks permission"""

    def __init__(self, action: str, resource: str | None = None):
        message = f"Not authorized to {action}"
        if resource:
            message += f" {resource}"
        super().__init__(
            message=message,
            code="AUTHORIZATION_FAILED",
            details={
                "action": action,
                "resource": resource,
            },
        )


class ApiKeyNotFoundException(NotaryException):
    """Raised when an API key is not found"""

    def __init__(self, key_prefix: str | None = None):
        message = "API key not found"
        if key_prefix:
            message += f": {key_prefix}"
        super().__init__(
            message=message,
            code="API_KEY_NOT_FOUND",
            details={"key_prefix": key_prefix},
        )


class RateLimitException(NotaryException):
    """Raised when rate limit is exceeded"""

    def __init__(self, retry_after: int | None = None):
        super().__init__(
            message="Rate limit exceeded",
            code="RATE_LIMIT_EXCEEDED",
            details={"retry_after_seconds": retry_after},
        )
