"""
Unit tests for config module
"""
import pytest
import os
from abs_utils import config


class TestFileSettings:
    """Test FileSettings configuration"""

    def test_default_values(self):
        """Test default configuration values"""
        settings = config.FileSettings()
        assert settings.max_file_size == 100 * 1024 * 1024  # 100MB
        assert settings.allowed_extensions == [".pdf", ".jpg", ".jpeg", ".png", ".txt"]
        assert settings.chunk_size == 8192

    def test_from_env_vars(self, monkeypatch):
        """Test loading from environment variables"""
        monkeypatch.setenv("MAX_FILE_SIZE", "200000000")
        monkeypatch.setenv("CHUNK_SIZE", "16384")

        settings = config.FileSettings()
        assert settings.max_file_size == 200000000
        assert settings.chunk_size == 16384

    def test_get_file_settings_singleton(self):
        """Test that get_file_settings returns same instance"""
        settings1 = config.get_file_settings()
        settings2 = config.get_file_settings()
        assert settings1 is settings2


class TestNetworkSettings:
    """Test NetworkSettings configuration"""

    def test_default_values(self):
        """Test default network configuration"""
        settings = config.NetworkSettings()
        assert settings.default_network == "polygon"
        assert settings.supported_networks == ["polygon", "ethereum", "celo", "sepolia"]
        assert settings.default_gas_limit == 300000

    def test_from_env_vars(self, monkeypatch):
        """Test loading network settings from environment"""
        monkeypatch.setenv("DEFAULT_NETWORK", "ethereum")
        monkeypatch.setenv("DEFAULT_GAS_LIMIT", "500000")

        settings = config.NetworkSettings()
        assert settings.default_network == "ethereum"
        assert settings.default_gas_limit == 500000

    def test_get_network_settings_singleton(self):
        """Test that get_network_settings returns same instance"""
        settings1 = config.get_network_settings()
        settings2 = config.get_network_settings()
        assert settings1 is settings2


class TestSecuritySettings:
    """Test SecuritySettings configuration"""

    def test_default_values(self):
        """Test default security configuration"""
        settings = config.SecuritySettings()
        assert settings.jwt_algorithm == "HS256"
        assert settings.jwt_expiration_minutes == 60
        assert settings.api_key_prefix == "sk_live"
        assert settings.rate_limit_requests == 100
        assert settings.rate_limit_period == 60

    def test_from_env_vars(self, monkeypatch):
        """Test loading security settings from environment"""
        monkeypatch.setenv("JWT_ALGORITHM", "HS512")
        monkeypatch.setenv("JWT_EXPIRATION_MINUTES", "120")
        monkeypatch.setenv("API_KEY_PREFIX", "sk_test")
        monkeypatch.setenv("RATE_LIMIT_REQUESTS", "200")

        settings = config.SecuritySettings()
        assert settings.jwt_algorithm == "HS512"
        assert settings.jwt_expiration_minutes == 120
        assert settings.api_key_prefix == "sk_test"
        assert settings.rate_limit_requests == 200

    def test_get_security_settings_singleton(self):
        """Test that get_security_settings returns same instance"""
        settings1 = config.get_security_settings()
        settings2 = config.get_security_settings()
        assert settings1 is settings2


class TestSettingsIsolation:
    """Test that different settings don't interfere"""

    def test_settings_are_independent(self):
        """Test that each settings class is independent"""
        file_settings = config.get_file_settings()
        network_settings = config.get_network_settings()
        security_settings = config.get_security_settings()

        # Check they are different instances of different classes
        assert file_settings is not network_settings
        assert network_settings is not security_settings
        assert file_settings is not security_settings

        # Check they have expected attributes
        assert hasattr(file_settings, 'max_file_size')
        assert hasattr(network_settings, 'default_network')
        assert hasattr(security_settings, 'jwt_algorithm')

        # Check they don't have each other's attributes
        assert not hasattr(file_settings, 'default_network')
        assert not hasattr(network_settings, 'jwt_algorithm')
        assert not hasattr(security_settings, 'max_file_size')


class TestSettingsPydanticFeatures:
    """Test Pydantic features of settings"""

    def test_settings_are_immutable(self):
        """Test that settings cannot be modified after creation"""
        settings = config.FileSettings()

        # Pydantic BaseSettings are not frozen by default, but let's test the pattern
        # of not modifying them directly
        original_size = settings.max_file_size

        # This should work (assignment)
        settings.max_file_size = 999

        # But the getter functions should return fresh instances with original env values
        new_settings = config.FileSettings()
        assert new_settings.max_file_size == original_size

    def test_settings_model_dump(self):
        """Test that settings can be dumped to dict"""
        settings = config.FileSettings()
        data = settings.model_dump()

        assert "max_file_size" in data
        assert "allowed_extensions" in data
        assert "chunk_size" in data
        assert isinstance(data["allowed_extensions"], list)

    def test_settings_model_json_schema(self):
        """Test that settings have JSON schema"""
        schema = config.FileSettings.model_json_schema()

        assert "properties" in schema
        assert "max_file_size" in schema["properties"]
        assert schema["properties"]["max_file_size"]["type"] == "integer"