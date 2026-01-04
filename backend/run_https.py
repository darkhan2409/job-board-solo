"""
HTTPS development server for FastAPI backend.
Uses SSL certificates from the certs directory.

Usage:
    python run_https.py

Requirements:
    - SSL certificates in ../certs/ directory
    - localhost.pem (certificate)
    - localhost-key.pem (private key)

See HTTPS_SETUP.md for certificate generation instructions.
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """Start the HTTPS development server."""
    # Get the project root directory (parent of backend)
    backend_dir = Path(__file__).parent
    project_root = backend_dir.parent
    cert_dir = project_root / "certs"
    
    # Check if certificates exist
    cert_file = cert_dir / "localhost.pem"
    key_file = cert_dir / "localhost-key.pem"
    
    if not cert_file.exists() or not key_file.exists():
        print("❌ SSL certificates not found!")
        print(f"\nExpected files:")
        print(f"  - {cert_file}")
        print(f"  - {key_file}")
        print("\n📚 Please generate certificates first:")
        print("  1. Install mkcert: https://github.com/FiloSottile/mkcert")
        print("  2. Run: mkcert -install")
        print("  3. Create certs directory: mkdir certs")
        print("  4. Generate certificates: cd certs && mkcert localhost 127.0.0.1 ::1")
        print("  5. Rename files:")
        print("     - mv localhost+2.pem localhost.pem")
        print("     - mv localhost+2-key.pem localhost-key.pem")
        print("\nSee HTTPS_SETUP.md for detailed instructions.")
        sys.exit(1)
    
    print("=" * 60)
    print("🔒 Starting HTTPS Development Server")
    print("=" * 60)
    print(f"📁 Certificate directory: {cert_dir}")
    print(f"🔑 Private key: {key_file.name}")
    print(f"📜 Certificate: {cert_file.name}")
    print("-" * 60)
    print(f"🌐 Backend URL: https://localhost:8000")
    print(f"📚 API Documentation: https://localhost:8000/docs")
    print(f"🔍 Health Check: https://localhost:8000/health")
    print("-" * 60)
    print("💡 Tips:")
    print("  - First time? Your browser may show a security warning")
    print("  - With mkcert: No warnings, certificate is trusted")
    print("  - Self-signed: Click 'Advanced' → 'Proceed to localhost'")
    print("  - Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            ssl_keyfile=str(key_file),
            ssl_certfile=str(cert_file),
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
