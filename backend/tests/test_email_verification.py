#!/usr/bin/env python3
"""Test script to verify email verification on email change works correctly."""

import asyncio
import sys
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.user import User, UserRole
from app.models.email_verification_token import EmailVerificationToken
from app.services.user_service import update_user_profile
from app.utils.security import hash_password
from app.config import settings

# Create async engine for testing
engine = create_async_engine(
    "sqlite+aiosqlite:///./test_email_verification.db",
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def test_email_change_verification():
    """Test that changing email triggers verification email."""
    
    print("🧪 Testing email verification on email change...")
    
    # Create tables
    from app.database import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as db:
        # Create a test user
        test_user = User(
            email="original@example.com",
            hashed_password=hash_password("TestPassword123"),
            full_name="Test User",
            role=UserRole.REGULAR_USER,
            is_active=True,
            is_verified=True,  # Start as verified
        )
        
        db.add(test_user)
        await db.commit()
        await db.refresh(test_user)
        
        print(f"✅ Created test user: {test_user.email} (verified={test_user.is_verified})")
        
        # Change email
        new_email = "newemail@example.com"
        print(f"📧 Changing email to: {new_email}")
        
        updated_user = await update_user_profile(
            db=db,
            user=test_user,
            email=new_email
        )
        
        # Verify email was changed
        if updated_user.email != new_email:
            print(f"❌ Email was not updated. Expected: {new_email}, Got: {updated_user.email}")
            return False
        
        print(f"✅ Email updated to: {updated_user.email}")
        
        # Verify user is now unverified
        if updated_user.is_verified:
            print(f"❌ User is still verified after email change")
            return False
        
        print(f"✅ User is now unverified (is_verified={updated_user.is_verified})")
        
        # Check that verification token was created
        stmt = select(EmailVerificationToken).where(
            EmailVerificationToken.user_id == updated_user.id
        )
        result = await db.execute(stmt)
        tokens = result.scalars().all()
        
        if not tokens:
            print(f"❌ No verification token was created")
            return False
        
        # Get the most recent token
        latest_token = max(tokens, key=lambda t: t.created_at)
        
        print(f"✅ Verification token created: {latest_token.token[:20]}...")
        print(f"✅ Token expires at: {latest_token.expires_at}")
        print(f"✅ Token used: {latest_token.used}")
        
        # Verify token is not expired
        if latest_token.expires_at < datetime.utcnow():
            print(f"❌ Token is already expired")
            return False
        
        print(f"✅ Token is valid (not expired)")
        
        # Verify token is not used
        if latest_token.used:
            print(f"❌ Token is already marked as used")
            return False
        
        print(f"✅ Token is not used")
        
        return True


async def main():
    """Run the test."""
    try:
        success = await test_email_change_verification()
        
        if success:
            print("\n🎉 All email verification tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Email verification tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
