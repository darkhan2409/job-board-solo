#!/usr/bin/env python3
"""Test script to verify security fix is working correctly."""

from app.config import settings
from app.main import app
from app.utils.security import create_access_token, decode_token

print("Testing configuration and security...")
print(f"✅ Config loaded: SECRET_KEY length = {len(settings.SECRET_KEY)}")
print(f"✅ Config loaded: JWT_SECRET_KEY length = {len(settings.JWT_SECRET_KEY)}")

# Test JWT token creation and verification
test_data = {"sub": "test@example.com", "role": "regular_user"}
token = create_access_token(test_data)
print(f"✅ JWT token created: {len(token)} chars")

decoded = decode_token(token)
if decoded and decoded.get("sub") == "test@example.com":
    print(f"✅ JWT token verified: sub={decoded['sub']}")
else:
    print("❌ JWT token verification failed")
    exit(1)

print(f"✅ FastAPI app loaded successfully")
print("\n🎉 All security checks passed!")
