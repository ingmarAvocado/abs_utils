# abs_utils Examples

Comprehensive, runnable examples demonstrating all abs_utils features.

## 📋 Examples List

### 1. Basic Logging (`01_basic_logging.py`)
**What it shows:**
- Setting up logging with JSON and text formats
- Using different log levels (DEBUG, INFO, WARNING, ERROR)
- Adding context to logs with `extra` parameter
- Logging exceptions with stack traces

**Run it:**
```bash
poetry run python examples/01_basic_logging.py
```

**Key concepts:**
- Call `setup_logging()` once at startup
- Use `get_logger(__name__)` in each module
- JSON format for production, text for development
- Add structured data with `extra` parameter

---

### 2. Logging Context (`02_logging_context.py`)
**What it shows:**
- Setting global context for ALL logs
- Request ID tracking pattern
- Context cleanup after requests
- Practical use case for API servers

**Run it:**
```bash
poetry run python examples/02_logging_context.py
```

**Key concepts:**
- `set_log_context()` adds fields to all subsequent logs
- Perfect for request IDs, user sessions, correlation IDs
- Always `clear_log_context()` when done
- Use FastAPI middleware to auto-manage context

---

### 3. File Hashing (`03_file_hashing.py`)
**What it shows:**
- Synchronous file hashing
- Asynchronous file hashing (non-blocking)
- String and bytes hashing
- Hash verification
- Hash properties (deterministic, fixed-length, avalanche effect)

**Run it:**
```bash
poetry run python examples/03_file_hashing.py
```

**Key concepts:**
- Use `hash_file_async()` for large files to avoid blocking
- All hashes are SHA-256 (0x-prefixed, 66 characters)
- Same input always produces same hash
- Hashes are irreversible and cryptographically secure

---

### 4. API Key Management (`04_api_key_management.py`)
**What it shows:**
- Generating secure API keys
- Storing keys securely (hash only!)
- Validating API keys
- Key lifecycle (create, validate, revoke, list)
- Security best practices

**Run it:**
```bash
poetry run python examples/04_api_key_management.py
```

**Key concepts:**
- **NEVER** store full API keys in database
- Store only cryptographic hash
- Show full key to user ONCE at creation
- Users identify keys by prefix
- Keys are cryptographically random (64 hex characters)

---

### 5. Input Validation (`05_input_validation.py`)
**What it shows:**
- Email validation
- File type and size validation
- Hash format validation
- Ethereum address validation
- Required fields, positive integers, string length
- Error handling with ValidationException

**Run it:**
```bash
poetry run python examples/05_input_validation.py
```

**Key concepts:**
- All validators raise `ValidationException` on failure
- Use `raise_exception=False` to get boolean instead
- `ValidationException.to_dict()` perfect for API responses
- Validators check format, not actual validity
- Combine validators for complete input validation

---

### 6. Exception Handling (`06_exception_handling.py`)
**What it shows:**
- Using custom exceptions
- Converting exceptions to API responses
- Exception hierarchy and catching
- Blockchain-specific exceptions
- Authentication and authorization errors
- Complete error handling patterns

**Run it:**
```bash
poetry run python examples/06_exception_handling.py
```

**Key concepts:**
- All custom exceptions inherit from `NotaryException`
- Use `exc.to_dict()` for clean API error responses
- Exceptions include error codes and structured details
- Catch specific exceptions for different handling
- `BlockchainException` is base for all blockchain errors

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