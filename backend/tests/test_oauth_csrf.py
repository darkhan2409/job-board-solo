"""
Simple test to verify OAuth CSRF protection is working.
This is a manual verification script, not a full test suite.
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.services.oauth_service import create_oauth_state, validate_oauth_state
from app.utils.exceptions import ValidationException


async def test_oauth_csrf_protection():
    """Test OAuth CSRF protection flow."""
    print("Testing OAuth CSRF Protection...")
    
    async with AsyncSessionLocal() as db:
        # Test 1: Create state token
        print("\n1. Creating OAuth state token for Google...")
        state = await create_oauth_state(db=db, provider='google')
        print(f"   ✓ Created state token: {state[:16]}...")
        
        # Test 2: Validate valid state token
        print("\n2. Validating valid state token...")
        try:
            await validate_oauth_state(db=db, state=state, provider='google')
            print("   ✓ Valid state token accepted")
        except ValidationException as e:
            print(f"   ✗ Unexpected error: {e}")
            return False
        
        # Test 3: Try to reuse state token (should fail)
        print("\n3. Attempting to reuse state token (should fail)...")
        try:
            await validate_oauth_state(db=db, state=state, provider='google')
            print("   ✗ Reused state token was accepted (SECURITY ISSUE!)")
            return False
        except ValidationException as e:
            print(f"   ✓ Reused state token rejected: {e}")
        
        # Test 4: Try invalid state token
        print("\n4. Attempting to use invalid state token (should fail)...")
        try:
            await validate_oauth_state(db=db, state='invalid-state-token', provider='google')
            print("   ✗ Invalid state token was accepted (SECURITY ISSUE!)")
            return False
        except ValidationException as e:
            print(f"   ✓ Invalid state token rejected: {e}")
        
        # Test 5: Try wrong provider
        print("\n5. Creating GitHub state and validating with Google (should fail)...")
        github_state = await create_oauth_state(db=db, provider='github')
        try:
            await validate_oauth_state(db=db, state=github_state, provider='google')
            print("   ✗ Wrong provider was accepted (SECURITY ISSUE!)")
            return False
        except ValidationException as e:
            print(f"   ✓ Wrong provider rejected: {e}")
        
        # Test 6: Empty state
        print("\n6. Attempting to validate empty state (should fail)...")
        try:
            await validate_oauth_state(db=db, state='', provider='google')
            print("   ✗ Empty state was accepted (SECURITY ISSUE!)")
            return False
        except ValidationException as e:
            print(f"   ✓ Empty state rejected: {e}")
    
    print("\n" + "="*60)
    print("✓ All OAuth CSRF protection tests passed!")
    print("="*60)
    return True


if __name__ == "__main__":
    result = asyncio.run(test_oauth_csrf_protection())
    exit(0 if result else 1)
