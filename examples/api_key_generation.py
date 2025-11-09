#!/usr/bin/env python3
"""
API key generation example for abs_utils
"""
from abs_utils import crypto


def main():
    print("=== API Key Generation Example ===\n")

    # Generate a production API key
    full_key, key_hash, display_prefix = crypto.generate_api_key("sk_live")

    print("Generated API Key:")
    print(f"  Full key (show user ONCE): {full_key}")
    print(f"  Key hash (store in DB): {key_hash}")
    print(f"  Display prefix (for UI): {display_prefix}\n")

    print("=== Key Verification Workflow ===\n")

    # Simulate storing in database
    stored_hash = key_hash
    print(f"1. Stored hash in database: {stored_hash[:20]}...\n")

    # Simulate user providing API key
    user_provided_key = full_key
    print(f"2. User provides key: {user_provided_key[:20]}...\n")

    # Verify the key
    computed_hash = crypto.hash_string(user_provided_key)
    is_valid = computed_hash == stored_hash
    print(f"3. Verification result: {'✓ Valid' if is_valid else '✗ Invalid'}\n")

    print("=== Multiple Environment Keys ===\n")

    # Generate keys for different environments
    environments = ["sk_test", "sk_dev", "sk_staging"]

    for env in environments:
        _, _, prefix = crypto.generate_api_key(env)
        print(f"  {env}: {prefix}...")

    print("\n=== Security Best Practices ===")
    print("1. Never log or store the full API key")
    print("2. Only show the full key once during generation")
    print("3. Store only the hash in your database")
    print("4. Use the display prefix for user identification")
    print("5. Implement rate limiting per API key")
    print("6. Rotate keys periodically")


if __name__ == "__main__":
    main()