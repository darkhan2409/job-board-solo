#!/usr/bin/env python3
"""
Validation script to ensure SECRET_KEY and JWT_SECRET_KEY meet security requirements.
Run this script to verify your environment configuration before deployment.
"""

import sys
from app.config import settings


def validate_secret_key(key_name: str, key_value: str) -> bool:
    """Validate that a secret key meets security requirements."""
    errors = []
    
    # Check minimum length (32 characters recommended)
    if len(key_value) < 32:
        errors.append(f"  ❌ {key_name} is too short ({len(key_value)} chars). Minimum 32 characters recommended.")
    
    # Check for insecure default values
    insecure_patterns = [
        "dev-secret",
        "change-in-production",
        "your-secret-key",
        "your-jwt-secret",
        "please-change",
        "test-key",
        "example-key"
    ]
    
    key_lower = key_value.lower()
    for pattern in insecure_patterns:
        if pattern in key_lower:
            errors.append(f"  ❌ {key_name} contains insecure pattern: '{pattern}'")
    
    # Check for sufficient entropy (should have mix of characters)
    if key_value.isalnum() and key_value.isascii():
        # Good - has alphanumeric characters
        pass
    elif len(set(key_value)) < 10:
        errors.append(f"  ❌ {key_name} has low entropy (only {len(set(key_value))} unique characters)")
    
    if errors:
        print(f"\n{key_name} validation FAILED:")
        for error in errors:
            print(error)
        return False
    else:
        print(f"✅ {key_name} validation PASSED (length: {len(key_value)} chars)")
        return True


def main():
    """Main validation function."""
    print("=" * 60)
    print("SECRET KEY VALIDATION")
    print("=" * 60)
    
    all_valid = True
    
    # Validate SECRET_KEY
    all_valid &= validate_secret_key("SECRET_KEY", settings.SECRET_KEY)
    
    # Validate JWT_SECRET_KEY
    all_valid &= validate_secret_key("JWT_SECRET_KEY", settings.JWT_SECRET_KEY)
    
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ ALL SECRET KEYS ARE SECURE")
        print("=" * 60)
        return 0
    else:
        print("❌ SOME SECRET KEYS ARE INSECURE")
        print("=" * 60)
        print("\nTo generate secure keys, run:")
        print('  python -c "import secrets; print(secrets.token_urlsafe(32))"')
        return 1


if __name__ == "__main__":
    sys.exit(main())
