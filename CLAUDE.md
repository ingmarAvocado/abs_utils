# CLAUDE.md - Quick Start Guide for LLMs

## What This Is

`abs_utils` is a shared utility library for the abs_notary project. It provides logging, exceptions, crypto, validation, and configuration utilities used by all services.

## Key Concepts

**All utilities are async-compatible** - Use `await` where needed (crypto functions especially).

**Six main modules:**
1. **logger** - JSON logging with context
2. **exceptions** - Custom errors with codes
3. **crypto** - File hashing, API key generation
4. **validators** - Input validation
5. **constants** - Shared constants
6. **config** - Settings management

## Quick Examples

### Setup Logging (Do This First!)

```python
from abs_utils.logger import setup_logging, get_logger

# Call once at app startup
setup_logging(level="INFO", log_format="json", service_name="abs_api_server")

# Get logger anywhere
logger = get_logger(__name__)
logger.info("Server started")
```

### Hash a File (Async)

```python
from abs_utils.crypto import hash_file_async

# Returns "0x1234abcd..." (66 chars)
file_hash = await hash_file_async("/path/to/file.pdf")
```

### Generate API Key

```python
from abs_utils.crypto import generate_api_key

full_key, key_hash, prefix = generate_api_key("sk_live")
# full_key: "sk_live_abc123..." - show user ONCE
# key_hash: "0x..." - store in database
# prefix: "sk_live_abc1" - show user for identification
```

### Validate Input

```python
from abs_utils.validators import validate_email, validate_hash
from abs_utils.exceptions import ValidationException

try:
    validate_email("user@example.com")
    validate_hash(file_hash)
except ValidationException as e:
    print(e.to_dict())
```

### Use Constants

```python
from abs_utils.constants import SUPPORTED_NETWORKS, MAX_FILE_SIZE

if network not in SUPPORTED_NETWORKS:
    raise InvalidNetworkException(network, SUPPORTED_NETWORKS)

if file_size > MAX_FILE_SIZE:
    raise ValidationException("file_size", "File too large")
```

### Raise Custom Exceptions

```python
from abs_utils.exceptions import DocumentNotFoundException

if not document:
    raise DocumentNotFoundException(doc_id=123)
```

## Common Patterns

### FastAPI with Logging Middleware

```python
from fastapi import FastAPI
from abs_utils.logger import LoggingMiddleware, setup_logging

setup_logging(level="INFO", log_format="json", service_name="api")
app = FastAPI()
app.add_middleware(LoggingMiddleware)
# All requests auto-logged with request_id
```

### Exception Handling in FastAPI

```python
from fastapi import HTTPException
from abs_utils.exceptions import NotaryException

@app.exception_handler(NotaryException)
async def handle_notary_exception(request, exc: NotaryException):
    return JSONResponse(
        status_code=400,
        content=exc.to_dict()
    )
```

### Hash File on Upload

```python
from abs_utils.crypto import hash_file_async
from abs_utils.validators import validate_file_type, validate_file_size

# Validate
validate_file_type(file.filename, file.content_type)
validate_file_size(file.size)

# Save file
file_path = save_file(file)

# Hash file
file_hash = await hash_file_async(file_path)
```

## Module Reference

### logger
- `setup_logging()` - Configure logging
- `get_logger(name)` - Get logger
- `LoggingMiddleware` - FastAPI middleware

### exceptions
All inherit from `NotaryException`:
- `DocumentNotFoundException`
- `BlockchainException`
- `ValidationException`
- `AuthenticationException`
- More in exceptions.py

### crypto
- `hash_file_async()` - Async file hash
- `hash_file()` - Sync file hash
- `hash_string()` - String hash
- `generate_api_key()` - API key generation
- `verify_hash()` - Verify hash

### validators
- `validate_email()`
- `validate_file_type()`
- `validate_file_size()`
- `validate_hash()`
- `validate_ethereum_address()`

### constants
- `SUPPORTED_NETWORKS` = ["polygon", "ethereum", "celo", "sepolia"]
- `MAX_FILE_SIZE` = 100 MB
- `DEFAULT_GAS_LIMIT` = 300000
- Many more in constants.py

### config
Settings classes:
- `get_file_settings()` - File config
- `get_network_settings()` - Network config
- `get_security_settings()` - Security config

## Important Notes

- **Async crypto**: Use `hash_file_async()` in async code
- **Exceptions have `.to_dict()`**: Perfect for API responses
- **All validators raise `ValidationException`**: Catch and handle
- **Setup logging once**: At app startup
- **Constants are uppercase**: `SUPPORTED_NETWORKS`, not `supported_networks`

## Next Steps

This library is used by:
- `abs_orm` - For validation
- `abs_blockchain` - For hashing, validation
- `abs_api_server` - For logging, exceptions, validation
- `abs_worker` - For logging

Import what you need:
```python
from abs_utils.logger import get_logger
from abs_utils.crypto import hash_file_async
from abs_utils.exceptions import DocumentNotFoundException
```
