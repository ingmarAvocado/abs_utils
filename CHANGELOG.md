# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security
- Removed insecure password hashing functions (hash_password and verify_password)
- These functions used simple SHA-256 without salting, which is cryptographically insecure for passwords
- Password hashing should be handled by a dedicated authentication service using bcrypt/passlib

### Fixed
- Fixed pyproject.toml Python version syntax from `^3.11` to `>=3.11` for proper dependency resolution
- Fixed MyPy type error in logger/core.py by adding explicit type annotation for formatter variable
- Removed incorrectly placed test directory from source code

### Added
- Comprehensive test suite with unit and integration tests
- Test coverage configuration targeting >90% coverage
- Examples directory with working code demonstrations:
  - Basic logging setup
  - FastAPI integration with logging middleware
  - Crypto hashing operations (sync and async)
  - API key generation and verification
  - Custom exception handling
  - Input validation examples
- CI/CD pipeline with GitHub Actions:
  - Multi-version testing (Python 3.11, 3.12, 3.13)
  - Linting with Black, Ruff, and MyPy
  - Security scanning with Trivy
  - Coverage reporting
- Development dependencies: pytest-cov, coverage, httpx
- Tool configurations for pytest, mypy, ruff, black, and coverage
- MIT LICENSE file
- This CHANGELOG

### Changed
- Updated development dependencies for better testing support
- Enhanced pyproject.toml with comprehensive tool configurations

## [0.1.0] - 2024-01-01

### Added
- Initial release with core utilities:
  - **logger**: Async-compatible JSON/plain logging with middleware support
  - **crypto**: File/string/bytes hashing (sync/async), API key generation, hash verification
  - **validators**: Email, file type/size, hash, Ethereum address, transaction hash validation
  - **exceptions**: Comprehensive exception hierarchy for abs_notary project
  - **config**: Pydantic-based settings management for files, network, and security
  - **constants**: Centralized constants for networks, gas, files, contracts, timeouts, etc.
- FastAPI middleware for structured request/response logging
- Async support for performance-critical operations
- Full type hints for better IDE support and type safety