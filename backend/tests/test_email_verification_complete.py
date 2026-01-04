#!/usr/bin/env python3
"""Comprehensive test for email verification functionality."""

import asyncio
import sys
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.user import User, UserRole
from app.models.email_verification_token import EmailVerificationToken
from app.services.auth_service import register_user, verify_email, login, resend_verification_email
from app.services.user_service import update_user_profile
from app.utils.exceptions import ValidationException

# Create async engine for testing
engine = create_async_engine(
    "sqlite+aiosqlite:///./test_complete_verification.db",
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def test_registration_verification_flow():
    """Test complete registration and verification flow."""
    
    print("\n🧪 Test 1: Registration and Verification Flow")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # Register a new user
        print("📝 Registering new user...")
        user = await register_user(
            db=db,
            email="newuser@example.com",
            password="TestPassword123",
            full_name="New User"
        )
        
        print(f"✅ User registered: {user.email}")
        print(f"   - is_verified: {user.is_verified}")
        print(f"   - is_active: {user.is_active}")
        
        if user.is_verified:
            print("❌ User should not be verified immediately after registration")
            return False
        
        # Try to login without verification
        print("\n🔐 Attempting login without verification...")
        try:
            await login(db=db, email=user.email, password="TestPassword123")
            print("❌ Login should fail for unverified user")
            return False
        except ValidationException as e:
            if "not verified" in str(e).lower():
                print(f"✅ Login correctly blocked: {e}")
            else:
                print(f"❌ Wrong error message: {e}")
                return False
        
        # Get verification token
        stmt = select(EmailVerificationToken).where(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.used == False
        )
        result = await db.execute(stmt)
        token = result.scalar_one_or_none()
        
        if not token:
            print("❌ No verification token found")
            return False
        
        print(f"✅ Verification token found: {token.token[:20]}...")
        
        # Verify email
        print("\n✉️ Verifying email...")
        verified_user = await verify_email(db=db, token=token.token)
        
        print(f"✅ Email verified: {verified_user.email}")
        print(f"   - is_verified: {verified_user.is_verified}")
        
        if not verified_user.is_verified:
            print("❌ User should be verified after verification")
            return False
        
        # Try to login after verification
        print("\n🔐 Attempting login after verification...")
        access_token, refresh_token, logged_in_user = await login(
            db=db,
            email=verified_user.email,
            password="TestPassword123"
        )
        
        print(f"✅ Login successful!")
        print(f"   - access_token: {access_token[:30]}...")
        print(f"   - refresh_token: {refresh_token[:30]}...")
        
        return True


async def test_email_change_verification():
    """Test email change requires re-verification."""
    
    print("\n🧪 Test 2: Email Change Verification")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # Get the verified user from previous test
        stmt = select(User).where(User.email == "newuser@example.com")
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            print("❌ User not found from previous test")
            return False
        
        print(f"👤 Current user: {user.email} (verified={user.is_verified})")
        
        # Change email
        new_email = "changed@example.com"
        print(f"\n📧 Changing email to: {new_email}")
        
        updated_user = await update_user_profile(
            db=db,
            user=user,
            email=new_email
        )
        
        print(f"✅ Email changed to: {updated_user.email}")
        print(f"   - is_verified: {updated_user.is_verified}")
        
        if updated_user.is_verified:
            print("❌ User should be unverified after email change")
            return False
        
        # Try to login with new email (should fail)
        print("\n🔐 Attempting login with new email (unverified)...")
        try:
            await login(db=db, email=new_email, password="TestPassword123")
            print("❌ Login should fail for unverified email")
            return False
        except ValidationException as e:
            if "not verified" in str(e).lower():
                print(f"✅ Login correctly blocked: {e}")
            else:
                print(f"❌ Wrong error message: {e}")
                return False
        
        # Check verification token was created
        stmt = select(EmailVerificationToken).where(
            EmailVerificationToken.user_id == updated_user.id,
            EmailVerificationToken.used == False
        ).order_by(EmailVerificationToken.created_at.desc())
        result = await db.execute(stmt)
        token = result.scalar_one_or_none()
        
        if not token:
            print("❌ No verification token found for new email")
            return False
        
        print(f"✅ New verification token created: {token.token[:20]}...")
        
        # Verify new email
        print("\n✉️ Verifying new email...")
        verified_user = await verify_email(db=db, token=token.token)
        
        print(f"✅ New email verified: {verified_user.email}")
        print(f"   - is_verified: {verified_user.is_verified}")
        
        if not verified_user.is_verified:
            print("❌ User should be verified after verification")
            return False
        
        # Try to login with new email (should succeed)
        print("\n🔐 Attempting login with new email (verified)...")
        access_token, refresh_token, logged_in_user = await login(
            db=db,
            email=new_email,
            password="TestPassword123"
        )
        
        print(f"✅ Login successful with new email!")
        
        return True


async def test_resend_verification():
    """Test resending verification email."""
    
    print("\n🧪 Test 3: Resend Verification Email")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # Register another user
        print("📝 Registering another user...")
        user = await register_user(
            db=db,
            email="resend@example.com",
            password="TestPassword123",
            full_name="Resend User"
        )
        
        print(f"✅ User registered: {user.email}")
        
        # Count initial tokens
        stmt = select(EmailVerificationToken).where(
            EmailVerificationToken.user_id == user.id
        )
        result = await db.execute(stmt)
        initial_tokens = len(result.scalars().all())
        
        print(f"   - Initial tokens: {initial_tokens}")
        
        # Resend verification email
        print("\n📧 Resending verification email...")
        await resend_verification_email(db=db, email=user.email)
        
        # Count tokens after resend
        stmt = select(EmailVerificationToken).where(
            EmailVerificationToken.user_id == user.id
        )
        result = await db.execute(stmt)
        final_tokens = len(result.scalars().all())
        
        print(f"✅ Verification email resent")
        print(f"   - Final tokens: {final_tokens}")
        
        if final_tokens <= initial_tokens:
            print("❌ New token should be created")
            return False
        
        # Try to resend for verified user (should fail)
        print("\n📧 Attempting to resend for verified user...")
        
        # First verify the user - get the latest unused token
        stmt = select(EmailVerificationToken).where(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.used == False
        ).order_by(EmailVerificationToken.created_at.desc()).limit(1)
        result = await db.execute(stmt)
        token = result.scalar_one_or_none()
        
        await verify_email(db=db, token=token.token)
        
        # Now try to resend
        try:
            await resend_verification_email(db=db, email=user.email)
            print("❌ Resend should fail for verified user")
            return False
        except ValidationException as e:
            if "already verified" in str(e).lower():
                print(f"✅ Resend correctly blocked: {e}")
            else:
                print(f"❌ Wrong error message: {e}")
                return False
        
        return True


async def main():
    """Run all tests."""
    
    print("🚀 Starting Email Verification Tests")
    print("=" * 60)
    
    # Create tables
    from app.database import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database initialized")
    
    try:
        # Run tests
        test1 = await test_registration_verification_flow()
        test2 = await test_email_change_verification()
        test3 = await test_resend_verification()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        print(f"Test 1 (Registration & Verification): {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"Test 2 (Email Change Verification): {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"Test 3 (Resend Verification): {'✅ PASS' if test3 else '❌ FAIL'}")
        
        if test1 and test2 and test3:
            print("\n🎉 All email verification tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
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
