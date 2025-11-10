#!/usr/bin/env python3
"""
Example 4: API Key Generation and Management

This example shows:
- How to generate secure API keys
- How to store them securely (hash only)
- How to validate API keys
- Complete API key lifecycle
"""

from abs_utils.crypto import generate_api_key, hash_string, verify_hash


# Simulated database
api_keys_db = {}


def create_api_key(user_id: int, description: str = ""):
    """Create a new API key for a user"""
    print(f"\n📝 Creating API key for user {user_id}...")

    # Generate API key
    full_key, key_hash, prefix = generate_api_key(prefix="sk_live")

    print(f"  Full key:    {full_key}")
    print(f"  Prefix:      {prefix}")
    print(f"  Hash (DB):   {key_hash[:20]}... (truncated)")

    # Store in "database" (only hash and prefix!)
    api_keys_db[key_hash] = {
        "user_id": user_id,
        "prefix": prefix,
        "description": description,
        "active": True,
    }

    print(f"\n✅ API key created!")
    print(f"⚠️  IMPORTANT: Show full key to user ONCE: {full_key}")
    print(f"   After this, user can only see prefix: {prefix}")

    return full_key, key_hash, prefix


def validate_api_key(api_key: str) -> dict | None:
    """Validate an API key and return user info"""
    print(f"\n🔍 Validating API key: {api_key[:20]}...")

    # Hash the provided key
    key_hash = hash_string(api_key)

    # Look up in database
    if key_hash in api_keys_db:
        key_info = api_keys_db[key_hash]
        if key_info["active"]:
            print(f"✅ Valid! User ID: {key_info['user_id']}")
            return key_info
        else:
            print(f"❌ Key is revoked")
            return None
    else:
        print(f"❌ Invalid API key")
        return None


def revoke_api_key(key_hash: str):
    """Revoke an API key"""
    print(f"\n🚫 Revoking API key...")
    if key_hash in api_keys_db:
        api_keys_db[key_hash]["active"] = False
        prefix = api_keys_db[key_hash]["prefix"]
        print(f"✅ API key {prefix} revoked")
    else:
        print(f"❌ API key not found")


def list_user_api_keys(user_id: int):
    """List all API keys for a user"""
    print(f"\n📋 API keys for user {user_id}:")

    keys = [
        (hash_val, info)
        for hash_val, info in api_keys_db.items()
        if info["user_id"] == user_id
    ]

    if not keys:
        print("  No API keys found")
        return

    for key_hash, info in keys:
        status = "🟢 Active" if info["active"] else "🔴 Revoked"
        print(f"  {status} - {info['prefix']} - {info['description']}")


def main():
    print("=" * 80)
    print("EXAMPLE 4: API KEY MANAGEMENT")
    print("=" * 80)

    # Scenario 1: User creates their first API key
    print("\n" + "=" * 80)
    print("SCENARIO 1: Creating First API Key")
    print("=" * 80)

    full_key_1, hash_1, prefix_1 = create_api_key(
        user_id=123, description="Production API key"
    )

    # Scenario 2: User creates a second API key
    print("\n" + "=" * 80)
    print("SCENARIO 2: Creating Second API Key")
    print("=" * 80)

    full_key_2, hash_2, prefix_2 = create_api_key(user_id=123, description="Dev/Test key")

    # Scenario 3: User makes API request with key
    print("\n" + "=" * 80)
    print("SCENARIO 3: Making API Request")
    print("=" * 80)

    print("\n📡 API Request with Authorization header...")
    user_info = validate_api_key(full_key_1)

    if user_info:
        print(f"\n✅ Request authorized for user {user_info['user_id']}")
        print("   Processing request...")

    # Scenario 4: Invalid key attempt
    print("\n" + "=" * 80)
    print("SCENARIO 4: Invalid API Key Attempt")
    print("=" * 80)

    fake_key = "sk_live_" + "a" * 64
    validate_api_key(fake_key)

    # Scenario 5: User lists their keys
    print("\n" + "=" * 80)
    print("SCENARIO 5: User Lists API Keys")
    print("=" * 80)

    list_user_api_keys(user_id=123)

    # Scenario 6: User revokes a key
    print("\n" + "=" * 80)
    print("SCENARIO 6: Revoking API Key")
    print("=" * 80)

    revoke_api_key(hash_2)
    list_user_api_keys(user_id=123)

    # Scenario 7: Trying to use revoked key
    print("\n" + "=" * 80)
    print("SCENARIO 7: Using Revoked Key")
    print("=" * 80)

    validate_api_key(full_key_2)

    # Security demonstration
    print("\n" + "=" * 80)
    print("SECURITY DEMONSTRATION")
    print("=" * 80)

    print("\n🔒 What's stored in the database:")
    for key_hash, info in list(api_keys_db.items())[:1]:  # Show first one
        print(f"\n  Key Hash: {key_hash}")
        print(f"  User ID:  {info['user_id']}")
        print(f"  Prefix:   {info['prefix']}")
        print(f"  Active:   {info['active']}")

    print("\n✅ Security Best Practices Followed:")
    print("  ✓ Never store full API key in database")
    print("  ✓ Only store cryptographic hash")
    print("  ✓ Show full key to user ONCE at creation")
    print("  ✓ Show only prefix for identification")
    print("  ✓ Keys are cryptographically random (64 hex chars)")

    print("\n" + "=" * 80)
    print("✅ Example complete!")
    print("\nKey Takeaways:")
    print("- generate_api_key() creates secure random keys")
    print("- Store ONLY the hash in your database")
    print("- Show full key to user ONCE (at creation)")
    print("- Users identify keys by prefix (first 12 chars)")
    print("- Hash incoming keys to validate them")
    print("=" * 80)


if __name__ == "__main__":
    main()
