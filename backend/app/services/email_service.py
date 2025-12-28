# app/services/email_service.py
"""
Email service for sending transactional emails using async SMTP.
"""

import logging
from pathlib import Path
from typing import Optional

import aiosmtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader

from app.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Setup Jinja2 template environment
TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "emails"
jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


async def send_email(
    email_to: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
) -> bool:
    """
    Send an email using async SMTP.

    Args:
        email_to: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        text_content: Plain text content (optional fallback)

    Returns:
        True if email sent successfully, False otherwise
    """
    # Skip if SMTP not configured
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning(
            f"SMTP not configured. Email not sent to {email_to} with subject: {subject}"
        )
        return False

    try:
        message = EmailMessage()
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL or settings.SMTP_USER}>"
        message["To"] = email_to
        message["Subject"] = subject

        # Set HTML content
        message.add_alternative(html_content, subtype="html")

        # Set plain text fallback
        if text_content:
            message.set_content(text_content)

        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )

        logger.info(f"Email sent successfully to {email_to}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {email_to}: {str(e)}")
        return False


async def send_verification_email(
    email: str,
    full_name: str,
    verification_token: str
) -> bool:
    """
    Send email verification link to new user.

    Args:
        email: User's email address
        full_name: User's full name
        verification_token: Email verification token

    Returns:
        True if email sent successfully, False otherwise
    """
    verification_url = f"{settings.FRONTEND_URL}/auth/verify-email?token={verification_token}"

    # Render HTML template
    template = jinja_env.get_template("verification.html")
    html_content = template.render(
        full_name=full_name,
        verification_url=verification_url,
        expire_hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS
    )

    # Plain text fallback
    text_content = f"""
    Hi {full_name},

    Thank you for registering at {settings.PROJECT_NAME}!

    Please verify your email address by clicking the link below:
    {verification_url}

    This link will expire in {settings.EMAIL_VERIFICATION_EXPIRE_HOURS} hours.

    If you didn't create this account, you can safely ignore this email.

    Best regards,
    {settings.PROJECT_NAME} Team
    """

    return await send_email(
        email_to=email,
        subject="Verify Your Email Address",
        html_content=html_content,
        text_content=text_content
    )


async def send_password_reset_email(
    email: str,
    full_name: str,
    reset_token: str
) -> bool:
    """
    Send password reset link to user.

    Args:
        email: User's email address
        full_name: User's full name
        reset_token: Password reset token

    Returns:
        True if email sent successfully, False otherwise
    """
    reset_url = f"{settings.FRONTEND_URL}/auth/reset-password?token={reset_token}"

    # Render HTML template
    template = jinja_env.get_template("password_reset.html")
    html_content = template.render(
        full_name=full_name,
        reset_url=reset_url,
        expire_hours=settings.PASSWORD_RESET_EXPIRE_HOURS
    )

    # Plain text fallback
    text_content = f"""
    Hi {full_name},

    We received a request to reset your password for {settings.PROJECT_NAME}.

    Click the link below to reset your password:
    {reset_url}

    This link will expire in {settings.PASSWORD_RESET_EXPIRE_HOURS} hour(s).

    If you didn't request a password reset, you can safely ignore this email.
    Your password will not be changed.

    Best regards,
    {settings.PROJECT_NAME} Team
    """

    return await send_email(
        email_to=email,
        subject="Reset Your Password",
        html_content=html_content,
        text_content=text_content
    )


async def send_welcome_email(
    email: str,
    full_name: str
) -> bool:
    """
    Send welcome email to newly verified user.

    Args:
        email: User's email address
        full_name: User's full name

    Returns:
        True if email sent successfully, False otherwise
    """
    # Render HTML template
    template = jinja_env.get_template("welcome.html")
    html_content = template.render(
        full_name=full_name,
        frontend_url=settings.FRONTEND_URL
    )

    # Plain text fallback
    text_content = f"""
    Hi {full_name},

    Welcome to {settings.PROJECT_NAME}!

    Your email has been verified successfully. You can now start using all features.

    Visit our platform: {settings.FRONTEND_URL}

    We're excited to have you on board!

    Best regards,
    {settings.PROJECT_NAME} Team
    """

    return await send_email(
        email_to=email,
        subject=f"Welcome to {settings.PROJECT_NAME}!",
        html_content=html_content,
        text_content=text_content
    )
