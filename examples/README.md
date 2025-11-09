# abs_utils Examples

This directory contains working examples demonstrating how to use the abs_utils library.

## Available Examples

### 1. Basic Logging (`basic_logging.py`)
Demonstrates basic logging setup and usage:
- Setting up JSON/plain logging
- Logging at different levels
- Adding extra context to logs
- Exception logging

```bash
python basic_logging.py
```

### 2. FastAPI with Logging Middleware (`fastapi_logging.py`)
Shows integration with FastAPI:
- Adding logging middleware
- Exception handlers for custom exceptions
- Request/response logging
- Automatic request ID generation

```bash
# Install FastAPI first: pip install fastapi uvicorn
python fastapi_logging.py
# Then visit http://localhost:8000/docs
```

### 3. Crypto Hashing (`crypto_hashing.py`)
Demonstrates cryptographic hashing functions:
- File hashing (sync and async)
- String hashing with different encodings
- Bytes hashing
- Hash verification

```bash
python crypto_hashing.py
```

### 4. API Key Generation (`api_key_generation.py`)
Shows secure API key generation and verification:
- Generating API keys with prefixes
- Storing key hashes securely
- Verifying API keys
- Best practices for key management

```bash
python api_key_generation.py
```

### 5. Custom Exceptions (`custom_exceptions.py`)
Demonstrates using custom exception classes:
- Document-related exceptions
- Validation exceptions
- Authentication/authorization exceptions
- Blockchain exceptions
- Converting exceptions to API responses

```bash
python custom_exceptions.py
```

### 6. Input Validators (`validators_usage.py`)
Shows input validation functions:
- Email validation
- File type and size validation
- Hash validation (file hashes, transaction hashes)
- Ethereum address validation
- Combined validation example

```bash
python validators_usage.py
```

## Running Examples

1. Make sure abs_utils is installed:
```bash
cd /path/to/abs_utils
pip install -e .
```

2. Run any example:
```bash
cd examples
python <example_name>.py
```

## Key Patterns

### Async Operations
Many crypto functions have async versions for better performance:
```python
import asyncio
from abs_utils import crypto

async def main():
    hash_result = await crypto.hash_file_async("file.pdf")
    print(hash_result)

asyncio.run(main())
```

### Exception Handling
All custom exceptions inherit from `NotaryException`:
```python
from abs_utils.exceptions import NotaryException

try:
    # Your code here
    pass
except NotaryException as e:
    # Handle any abs_utils exception
    error_dict = e.to_dict()
```

### Logging Best Practices
Setup logging once at application startup:
```python
from abs_utils.logger import setup_logging, get_logger

# At startup
setup_logging(level="INFO", log_format="json", service_name="my-service")

# In modules
logger = get_logger(__name__)
logger.info("Message", extra={"key": "value"})
```

## Integration with abs_notary

These utilities are designed to work seamlessly with the abs_notary project:
- Use the same logging setup across all services
- Consistent exception handling
- Shared validation rules
- Unified crypto operations

## Need Help?

Check the main README and CLAUDE.md for more detailed documentation.