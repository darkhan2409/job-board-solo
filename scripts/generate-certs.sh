#!/bin/bash

# Certificate Generation Script for Job Board Solo
# This script generates SSL certificates for local HTTPS development

set -e

echo "=================================================="
echo "🔒 SSL Certificate Generation for Local HTTPS"
echo "=================================================="
echo ""

# Check if mkcert is installed
if ! command -v mkcert &> /dev/null; then
    echo "❌ mkcert is not installed!"
    echo ""
    echo "Please install mkcert first:"
    echo ""
    echo "macOS:"
    echo "  brew install mkcert"
    echo "  brew install nss  # for Firefox"
    echo ""
    echo "Linux (Ubuntu/Debian):"
    echo "  sudo apt install libnss3-tools"
    echo "  wget -O mkcert https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64"
    echo "  chmod +x mkcert"
    echo "  sudo mv mkcert /usr/local/bin/"
    echo ""
    echo "Windows (with Chocolatey):"
    echo "  choco install mkcert"
    echo ""
    echo "For more info: https://github.com/FiloSottile/mkcert"
    exit 1
fi

echo "✅ mkcert is installed"
echo ""

# Install local CA
echo "📦 Installing local Certificate Authority..."
mkcert -install
echo ""

# Create certs directory
if [ ! -d "certs" ]; then
    echo "📁 Creating certs directory..."
    mkdir certs
else
    echo "📁 certs directory already exists"
fi

cd certs

# Generate certificates
echo "🔑 Generating SSL certificates..."
mkcert localhost 127.0.0.1 ::1

# Rename files for consistency
echo "📝 Renaming certificate files..."
if [ -f "localhost+2.pem" ]; then
    mv localhost+2.pem localhost.pem
fi
if [ -f "localhost+2-key.pem" ]; then
    mv localhost+2-key.pem localhost-key.pem
fi

cd ..

echo ""
echo "=================================================="
echo "✅ SSL Certificates Generated Successfully!"
echo "=================================================="
echo ""
echo "📁 Certificate location: ./certs/"
echo "   - localhost.pem (certificate)"
echo "   - localhost-key.pem (private key)"
echo ""
echo "🚀 Next steps:"
echo ""
echo "1. Start backend with HTTPS:"
echo "   cd backend"
echo "   python run_https.py"
echo ""
echo "2. Start frontend with HTTPS:"
echo "   cd frontend"
echo "   npm run dev:https"
echo ""
echo "3. Access your application:"
echo "   Backend:  https://localhost:8000"
echo "   Frontend: https://localhost:3000"
echo ""
echo "💡 Your browser will trust these certificates automatically!"
echo "=================================================="
