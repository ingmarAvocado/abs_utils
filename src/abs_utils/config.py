"""
Shared configuration helpers and common settings
"""

from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingSettings(BaseSettings):
    """Logging configuration"""

    model_config = SettingsConfigDict(env_prefix="LOG_", env_file=".env", extra="ignore")

    level: str = "INFO"
    format: str = "json"  # 'json' or 'text'
    service_name: str | None = None


class SecuritySettings(BaseSettings):
    """Security configuration"""

    model_config = SettingsConfigDict(env_prefix="SECURITY_", env_file=".env", extra="ignore")

    # JWT settings
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    # API key settings
    api_key_prefix: str = "sk_live"


class FileSettings(BaseSettings):
    """File handling configuration"""

    model_config = SettingsConfigDict(env_prefix="FILE_", env_file=".env", extra="ignore")

    # File size limits (in bytes)
    max_size: int = 100 * 1024 * 1024  # 100 MB
    storage_path: str = "./storage/files"
    certificate_path: str = "./storage/certificates"

    # Supported MIME types
    supported_types: list[str] = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "application/json",
        "text/plain",
    ]


class NetworkSettings(BaseSettings):
    """Blockchain network configuration"""

    model_config = SettingsConfigDict(env_prefix="NETWORK_", env_file=".env", extra="ignore")

    # Default network
    default_network: str = "polygon"

    # Supported networks
    supported_networks: list[str] = ["polygon", "ethereum", "celo", "sepolia"]

    # Gas settings
    default_gas_limit: int = 300000
    max_gas_price_gwei: int = 100


@lru_cache
def get_logging_settings() -> LoggingSettings:
    """Get cached logging settings"""
    return LoggingSettings()


@lru_cache
def get_security_settings() -> SecuritySettings:
    """Get cached security settings"""
    return SecuritySettings()


@lru_cache
def get_file_settings() -> FileSettings:
    """Get cached file settings"""
    return FileSettings()


@lru_cache
def get_network_settings() -> NetworkSettings:
    """Get cached network settings"""
    return NetworkSettings()


def get_env_var(key: str, default: Any = None) -> Any:
    """
    Get environment variable with optional default

    Args:
        key: Environment variable name
        default: Default value if not found

    Returns:
        Environment variable value or default
    """
    import os

    return os.getenv(key, default)


def get_secret(secret_name: str, default: Any = None) -> Any:
    """
    Get secret from environment or secrets manager

    Args:
        secret_name: Name of the secret
        default: Default value if not found

    Returns:
        Secret value or default

    Note:
        This is a placeholder. In production, integrate with
        AWS Secrets Manager, HashiCorp Vault, etc.
    """
    # For now, just use environment variables
    # TODO: Integrate with proper secrets manager
    return get_env_var(secret_name, default)
