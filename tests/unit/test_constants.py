"""
Unit tests for constants module
"""
import pytest
from abs_utils import constants


class TestNetworkConstants:
    """Test network-related constants"""

    def test_supported_networks(self):
        """Test SUPPORTED_NETWORKS constant"""
        assert isinstance(constants.SUPPORTED_NETWORKS, list)
        assert len(constants.SUPPORTED_NETWORKS) > 0
        assert "polygon" in constants.SUPPORTED_NETWORKS
        assert "ethereum" in constants.SUPPORTED_NETWORKS
        assert all(isinstance(net, str) for net in constants.SUPPORTED_NETWORKS)

    def test_default_network(self):
        """Test DEFAULT_NETWORK constant"""
        assert constants.DEFAULT_NETWORK == "polygon"
        assert constants.DEFAULT_NETWORK in constants.SUPPORTED_NETWORKS

    def test_chain_ids(self):
        """Test CHAIN_IDS mapping"""
        assert isinstance(constants.CHAIN_IDS, dict)
        assert constants.CHAIN_IDS["polygon"] == 137
        assert constants.CHAIN_IDS["ethereum"] == 1
        assert constants.CHAIN_IDS["celo"] == 42220
        assert constants.CHAIN_IDS["sepolia"] == 11155111

        # All supported networks should have chain IDs
        for network in constants.SUPPORTED_NETWORKS:
            assert network in constants.CHAIN_IDS

    def test_rpc_endpoints(self):
        """Test RPC_ENDPOINTS mapping"""
        assert isinstance(constants.RPC_ENDPOINTS, dict)
        assert "polygon" in constants.RPC_ENDPOINTS
        assert "ethereum" in constants.RPC_ENDPOINTS

        # All endpoints should be valid URLs
        for network, endpoint in constants.RPC_ENDPOINTS.items():
            assert endpoint.startswith("https://")


class TestGasConstants:
    """Test gas-related constants"""

    def test_default_gas_limit(self):
        """Test DEFAULT_GAS_LIMIT constant"""
        assert constants.DEFAULT_GAS_LIMIT == 300000
        assert isinstance(constants.DEFAULT_GAS_LIMIT, int)
        assert constants.DEFAULT_GAS_LIMIT > 0

    def test_gas_price_multiplier(self):
        """Test GAS_PRICE_MULTIPLIER constant"""
        assert constants.GAS_PRICE_MULTIPLIER == 1.1
        assert isinstance(constants.GAS_PRICE_MULTIPLIER, float)
        assert constants.GAS_PRICE_MULTIPLIER > 1.0


class TestFileConstants:
    """Test file-related constants"""

    def test_max_file_size(self):
        """Test MAX_FILE_SIZE constant"""
        assert constants.MAX_FILE_SIZE == 100 * 1024 * 1024  # 100MB
        assert isinstance(constants.MAX_FILE_SIZE, int)
        assert constants.MAX_FILE_SIZE > 0

    def test_supported_file_types(self):
        """Test SUPPORTED_FILE_TYPES mapping"""
        assert isinstance(constants.SUPPORTED_FILE_TYPES, dict)
        assert "application/pdf" in constants.SUPPORTED_FILE_TYPES
        assert "image/jpeg" in constants.SUPPORTED_FILE_TYPES
        assert "image/png" in constants.SUPPORTED_FILE_TYPES
        assert "text/plain" in constants.SUPPORTED_FILE_TYPES

        # Check extensions mapping
        assert constants.SUPPORTED_FILE_TYPES["application/pdf"] == [".pdf"]
        assert ".jpg" in constants.SUPPORTED_FILE_TYPES["image/jpeg"]
        assert ".jpeg" in constants.SUPPORTED_FILE_TYPES["image/jpeg"]

    def test_allowed_extensions(self):
        """Test ALLOWED_EXTENSIONS list"""
        assert isinstance(constants.ALLOWED_EXTENSIONS, list)
        assert ".pdf" in constants.ALLOWED_EXTENSIONS
        assert ".jpg" in constants.ALLOWED_EXTENSIONS
        assert ".png" in constants.ALLOWED_EXTENSIONS
        assert ".txt" in constants.ALLOWED_EXTENSIONS

        # All extensions should start with dot
        for ext in constants.ALLOWED_EXTENSIONS:
            assert ext.startswith(".")


class TestContractConstants:
    """Test contract-related constants"""

    def test_contract_addresses(self):
        """Test CONTRACT_ADDRESSES mapping"""
        assert isinstance(constants.CONTRACT_ADDRESSES, dict)

        # Check polygon contracts
        assert "polygon" in constants.CONTRACT_ADDRESSES
        polygon_contracts = constants.CONTRACT_ADDRESSES["polygon"]
        assert "notary" in polygon_contracts
        assert "registry" in polygon_contracts

        # Check Ethereum contracts
        assert "ethereum" in constants.CONTRACT_ADDRESSES
        ethereum_contracts = constants.CONTRACT_ADDRESSES["ethereum"]
        assert "notary" in ethereum_contracts
        assert "registry" in ethereum_contracts

        # All addresses should be valid Ethereum addresses
        for network, contracts in constants.CONTRACT_ADDRESSES.items():
            for contract_name, address in contracts.items():
                assert address.startswith("0x")
                assert len(address) == 42  # 0x + 40 hex chars

    def test_contract_abi_paths(self):
        """Test CONTRACT_ABI_PATHS mapping"""
        assert isinstance(constants.CONTRACT_ABI_PATHS, dict)
        assert "notary" in constants.CONTRACT_ABI_PATHS
        assert "registry" in constants.CONTRACT_ABI_PATHS

        # Paths should end with .json
        for contract, path in constants.CONTRACT_ABI_PATHS.items():
            assert path.endswith(".json")


class TestTimeoutConstants:
    """Test timeout constants"""

    def test_request_timeout(self):
        """Test REQUEST_TIMEOUT constant"""
        assert constants.REQUEST_TIMEOUT == 30
        assert isinstance(constants.REQUEST_TIMEOUT, int)
        assert constants.REQUEST_TIMEOUT > 0

    def test_blockchain_timeout(self):
        """Test BLOCKCHAIN_TIMEOUT constant"""
        assert constants.BLOCKCHAIN_TIMEOUT == 60
        assert isinstance(constants.BLOCKCHAIN_TIMEOUT, int)
        assert constants.BLOCKCHAIN_TIMEOUT > constants.REQUEST_TIMEOUT

    def test_file_upload_timeout(self):
        """Test FILE_UPLOAD_TIMEOUT constant"""
        assert constants.FILE_UPLOAD_TIMEOUT == 120
        assert isinstance(constants.FILE_UPLOAD_TIMEOUT, int)
        assert constants.FILE_UPLOAD_TIMEOUT > constants.BLOCKCHAIN_TIMEOUT


class TestStatusConstants:
    """Test status constants"""

    def test_document_statuses(self):
        """Test DOCUMENT_STATUSES list"""
        assert isinstance(constants.DOCUMENT_STATUSES, list)
        expected_statuses = ["pending", "notarized", "failed", "expired"]
        for status in expected_statuses:
            assert status in constants.DOCUMENT_STATUSES

    def test_transaction_statuses(self):
        """Test TRANSACTION_STATUSES list"""
        assert isinstance(constants.TRANSACTION_STATUSES, list)
        expected_statuses = ["pending", "confirmed", "failed"]
        for status in expected_statuses:
            assert status in constants.TRANSACTION_STATUSES


class TestPaginationConstants:
    """Test pagination constants"""

    def test_default_page_size(self):
        """Test DEFAULT_PAGE_SIZE constant"""
        assert constants.DEFAULT_PAGE_SIZE == 20
        assert isinstance(constants.DEFAULT_PAGE_SIZE, int)
        assert constants.DEFAULT_PAGE_SIZE > 0

    def test_max_page_size(self):
        """Test MAX_PAGE_SIZE constant"""
        assert constants.MAX_PAGE_SIZE == 100
        assert isinstance(constants.MAX_PAGE_SIZE, int)
        assert constants.MAX_PAGE_SIZE > constants.DEFAULT_PAGE_SIZE


class TestCacheConstants:
    """Test cache constants"""

    def test_cache_ttl(self):
        """Test CACHE_TTL constant"""
        assert constants.CACHE_TTL == 300  # 5 minutes
        assert isinstance(constants.CACHE_TTL, int)
        assert constants.CACHE_TTL > 0

    def test_cache_key_prefix(self):
        """Test CACHE_KEY_PREFIX constant"""
        assert constants.CACHE_KEY_PREFIX == "abs_notary"
        assert isinstance(constants.CACHE_KEY_PREFIX, str)


class TestConstantsConsistency:
    """Test consistency between related constants"""

    def test_networks_consistency(self):
        """Test that network-related constants are consistent"""
        # All supported networks should have chain IDs
        for network in constants.SUPPORTED_NETWORKS:
            assert network in constants.CHAIN_IDS, f"Missing chain ID for {network}"

        # All supported networks should have RPC endpoints
        for network in constants.SUPPORTED_NETWORKS:
            assert network in constants.RPC_ENDPOINTS, f"Missing RPC endpoint for {network}"

        # All supported networks should have contract addresses
        for network in constants.SUPPORTED_NETWORKS:
            assert network in constants.CONTRACT_ADDRESSES, f"Missing contracts for {network}"

    def test_file_types_consistency(self):
        """Test that file type constants are consistent"""
        # All extensions in ALLOWED_EXTENSIONS should be in SUPPORTED_FILE_TYPES values
        all_supported_extensions = []
        for extensions in constants.SUPPORTED_FILE_TYPES.values():
            all_supported_extensions.extend(extensions)

        for ext in constants.ALLOWED_EXTENSIONS:
            assert ext in all_supported_extensions, f"{ext} not in SUPPORTED_FILE_TYPES"

    def test_timeout_ordering(self):
        """Test that timeouts are ordered sensibly"""
        assert constants.REQUEST_TIMEOUT < constants.BLOCKCHAIN_TIMEOUT
        assert constants.BLOCKCHAIN_TIMEOUT < constants.FILE_UPLOAD_TIMEOUT

    def test_pagination_ordering(self):
        """Test that pagination limits are ordered sensibly"""
        assert constants.DEFAULT_PAGE_SIZE < constants.MAX_PAGE_SIZE