"""
Shared constants for abs_notary project
"""

# ============================================================================
# Blockchain Networks
# ============================================================================

SUPPORTED_NETWORKS = ["polygon", "ethereum", "celo", "sepolia", "localhost"]

# Network IDs (Chain IDs)
NETWORK_IDS = {
    "polygon": 137,
    "ethereum": 1,
    "celo": 42220,
    "sepolia": 11155111,  # Ethereum testnet
    "localhost": 1337,
}

# RPC URLs (can be overridden via environment variables)
DEFAULT_RPC_URLS = {
    "polygon": "https://polygon-rpc.com",
    "ethereum": "https://eth.llamarpc.com",
    "celo": "https://forno.celo.org",
    "sepolia": "https://rpc.sepolia.org",
    "localhost": "http://localhost:8545",
}

# ============================================================================
# Gas Settings
# ============================================================================

# Default gas limit for transactions
DEFAULT_GAS_LIMIT = 300000

# Maximum gas price in Gwei (to prevent overpaying)
MAX_GAS_PRICE_GWEI = 100

# Gas buffer multiplier (add 10% to estimated gas)
GAS_BUFFER_MULTIPLIER = 1.1

# ============================================================================
# File Handling
# ============================================================================

# Maximum file size (100 MB)
MAX_FILE_SIZE = 100 * 1024 * 1024

# Supported MIME types
SUPPORTED_FILE_TYPES = [
    "application/pdf",
    "image/png",
    "image/jpeg",
    "application/json",
    "text/plain",
    "text/csv",
    "application/zip",
]

# File extension to MIME type mapping
EXTENSION_TO_MIME = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".json": "application/json",
    ".txt": "text/plain",
    ".csv": "text/csv",
    ".zip": "application/zip",
}

# ============================================================================
# Document Status
# ============================================================================

DOC_STATUS_PENDING = "pending"
DOC_STATUS_PROCESSING = "processing"
DOC_STATUS_ON_CHAIN = "on_chain"
DOC_STATUS_ERROR = "error"

ALL_DOC_STATUSES = [
    DOC_STATUS_PENDING,
    DOC_STATUS_PROCESSING,
    DOC_STATUS_ON_CHAIN,
    DOC_STATUS_ERROR,
]

# ============================================================================
# Document Types
# ============================================================================

DOC_TYPE_HASH = "hash"
DOC_TYPE_NFT = "nft"

ALL_DOC_TYPES = [DOC_TYPE_HASH, DOC_TYPE_NFT]

# ============================================================================
# API Settings
# ============================================================================

# API key prefix
API_KEY_PREFIX = "sk_live"
API_KEY_TEST_PREFIX = "sk_test"

# API key length (in hex characters)
API_KEY_LENGTH = 64

# ============================================================================
# Authentication
# ============================================================================

# JWT settings
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 30
JWT_REFRESH_EXPIRE_DAYS = 7

# Password requirements
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

# ============================================================================
# Rate Limiting
# ============================================================================

# Requests per minute for authenticated users
RATE_LIMIT_AUTHENTICATED = 60

# Requests per minute for API keys
RATE_LIMIT_API_KEY = 100

# Requests per minute for unauthenticated users
RATE_LIMIT_UNAUTHENTICATED = 10

# ============================================================================
# Arweave Settings
# ============================================================================

# Arweave gateway URL
ARWEAVE_GATEWAY = "https://arweave.net"

# Arweave transaction confirmation time (minutes)
ARWEAVE_CONFIRMATION_TIME = 2

# ============================================================================
# Database
# ============================================================================

# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# ============================================================================
# Error Codes
# ============================================================================

ERROR_CODES = {
    "DOCUMENT_NOT_FOUND": "Document not found",
    "DOCUMENT_ALREADY_EXISTS": "Document already exists",
    "INSUFFICIENT_GAS": "Insufficient gas for transaction",
    "TRANSACTION_FAILED": "Blockchain transaction failed",
    "INVALID_NETWORK": "Invalid blockchain network",
    "ARWEAVE_UPLOAD_FAILED": "Failed to upload to Arweave",
    "VALIDATION_ERROR": "Input validation failed",
    "AUTHENTICATION_FAILED": "Authentication failed",
    "AUTHORIZATION_FAILED": "Not authorized",
    "API_KEY_NOT_FOUND": "API key not found",
    "RATE_LIMIT_EXCEEDED": "Rate limit exceeded",
}

# ============================================================================
# HTTP Status Codes (for consistency)
# ============================================================================

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_TOO_MANY_REQUESTS = 429
HTTP_INTERNAL_ERROR = 500
HTTP_BAD_GATEWAY = 502
HTTP_SERVICE_UNAVAILABLE = 503
