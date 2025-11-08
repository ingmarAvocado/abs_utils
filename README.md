# abs_utils

**Shared async-compatible utilities for abs_notary project**

## Overview

`abs_utils` provides reusable utilities used across all abs_notary services:
- **Logger**: Structured JSON logging with context injection
- **Exceptions**: Custom exception hierarchy with error codes
- **Crypto**: Async file hashing, API key generation
- **Config**: Shared configuration helpers
- **Validators**: Input validation utilities
- **Constants**: Shared constants (networks, file types, limits)

## Installation

```bash
poetry add git+https://github.com/ingmarAvocado/abs_utils.git
```

## Quick Start

### Logging

```python
from abs_utils.logger import setup_logging, get_logger

# Setup logging (call once at startup)
setup_logging(level="INFO", log_format="json", service_name="abs_api_server")

# Get logger
logger = get_logger(__name__)

# Log with context
logger.info("Processing document", extra={"doc_id": 123})
```

### Exceptions

```python
from abs_utils.exceptions import DocumentNotFoundException, ValidationException

# Raise custom exception
if not document:
    raise DocumentNotFoundException(doc_id=123)

# Handle exception
try:
    validate_something()
except ValidationException as e:
    print(e.to_dict())  # {"error": "VALIDATION_ERROR", "message": "...", "details": {...}}
```

### Crypto (Async)

```python
from abs_utils.crypto import hash_file_async, generate_api_key

# Hash file asynchronously
file_hash = await hash_file_async("/path/to/file.pdf")
# Returns: "0x1234abcd..."

# Generate API key
full_key, key_hash, prefix = generate_api_key("sk_live")
# full_key: "sk_live_abc123..." (give to user once)
# key_hash: "0x..." (store in database)
# prefix: "sk_live_abc1" (show to user for identification)
```

### Validators

```python
from abs_utils.validators import validate_email, validate_file_type, validate_hash

# Validate email
validate_email("user@example.com")  # Raises ValidationException if invalid

# Validate file type
validate_file_type("document.pdf", mime_type="application/pdf")

# Validate hash format
validate_hash("0x" + "a" * 64)  # Valid hash
```

### Constants

```python
from abs_utils.constants import SUPPORTED_NETWORKS, MAX_FILE_SIZE, DEFAULT_GAS_LIMIT

print(SUPPORTED_NETWORKS)  # ["polygon", "ethereum", "celo", "sepolia"]
print(MAX_FILE_SIZE)       # 104857600 (100 MB)
print(DEFAULT_GAS_LIMIT)   # 300000
```

### Config

```python
from abs_utils.config import get_file_settings, get_network_settings

# Get file settings
file_settings = get_file_settings()
print(file_settings.max_size)  # 104857600
print(file_settings.storage_path)  # "./storage/files"

# Get network settings
network_settings = get_network_settings()
print(network_settings.default_network)  # "polygon"
```

## Modules

### 1. `abs_utils.logger`

**Functions:**
- `setup_logging(level, log_format, service_name)` - Configure logging
- `get_logger(name)` - Get logger instance
- `set_log_context(**kwargs)` - Add context to all logs
- `clear_log_context()` - Clear context

**Classes:**
- `LoggingMiddleware` - FastAPI middleware for request logging

### 2. `abs_utils.exceptions`

**Exception Hierarchy:**
```
NotaryException (base)
├── DocumentNotFoundException
├── DocumentAlreadyExistsException
├── BlockchainException
│   ├── InsufficientGasException
│   ├── TransactionFailedException
│   └── InvalidNetworkException
├── ArweaveUploadException
├── ValidationException
├── AuthenticationException
├── AuthorizationException
├── ApiKeyNotFoundException
└── RateLimitException
```

### 3. `abs_utils.crypto`

**Functions:**
- `hash_file_async(file_path)` - Async file hashing
- `hash_file(file_path)` - Sync file hashing
- `hash_string(data)` - String hashing
- `hash_bytes(data)` - Bytes hashing
- `verify_hash(data, expected_hash)` - Verify hash
- `generate_api_key(prefix)` - Generate API key

### 4. `abs_utils.validators`

**Functions:**
- `validate_email(email)` - Email validation
- `validate_file_type(file_name, mime_type)` - File type validation
- `validate_file_size(file_size)` - File size validation
- `validate_hash(hash_string)` - Hash format validation
- `validate_ethereum_address(address)` - Ethereum address validation
- `validate_transaction_hash(tx_hash)` - Transaction hash validation
- `validate_required_fields(data, required)` - Required fields validation
- `validate_positive_integer(value, field_name)` - Positive integer validation
- `validate_string_length(value, field_name, min_length, max_length)` - String length validation

### 5. `abs_utils.constants`

**Categories:**
- Blockchain Networks: `SUPPORTED_NETWORKS`, `NETWORK_IDS`, `DEFAULT_RPC_URLS`
- Gas Settings: `DEFAULT_GAS_LIMIT`, `MAX_GAS_PRICE_GWEI`
- File Handling: `MAX_FILE_SIZE`, `SUPPORTED_FILE_TYPES`
- Document Status: `DOC_STATUS_*`
- API Settings: `API_KEY_PREFIX`, `API_KEY_LENGTH`
- Rate Limiting: `RATE_LIMIT_*`
- HTTP Status: `HTTP_*`

### 6. `abs_utils.config`

**Settings Classes:**
- `LoggingSettings` - Logging configuration
- `SecuritySettings` - Security configuration
- `FileSettings` - File handling configuration
- `NetworkSettings` - Blockchain network configuration

**Functions:**
- `get_logging_settings()` - Get logging settings
- `get_security_settings()` - Get security settings
- `get_file_settings()` - Get file settings
- `get_network_settings()` - Get network settings
- `get_env_var(key, default)` - Get environment variable
- `get_secret(secret_name, default)` - Get secret (placeholder)

## FastAPI Middleware Example

```python
from fastapi import FastAPI
from abs_utils.logger import LoggingMiddleware, setup_logging

# Setup logging
setup_logging(level="INFO", log_format="json", service_name="abs_api_server")

# Create app
app = FastAPI()

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# All requests will now be automatically logged with request_id
```

## Environment Variables

```bash
# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_SERVICE_NAME=abs_api_server

# Security
SECURITY_JWT_SECRET_KEY=your-secret-key
SECURITY_JWT_EXPIRE_MINUTES=30

# Files
FILE_MAX_SIZE=104857600
FILE_STORAGE_PATH=./storage/files
FILE_CERTIFICATE_PATH=./storage/certificates

# Network
NETWORK_DEFAULT_NETWORK=polygon
NETWORK_DEFAULT_GAS_LIMIT=300000
```

## Development

```bash
# Install dependencies
make dev-install

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Clean build artifacts
make clean
```

## License

MIT

## Links

- **Repository**: https://github.com/ingmarAvocado/abs_utils
- **Issues**: https://github.com/ingmarAvocado/abs_utils/issues
- **abs_notary Project**: Part of the abs_notary ecosystem
