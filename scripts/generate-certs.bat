@echo off
REM Certificate Generation Script for Job Board Solo (Windows)
REM This script generates SSL certificates for local HTTPS development

echo ==================================================
echo 🔒 SSL Certificate Generation for Local HTTPS
echo ==================================================
echo.

REM Check if mkcert is installed
where mkcert >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ mkcert is not installed!
    echo.
    echo Please install mkcert first:
    echo.
    echo With Chocolatey:
    echo   choco install mkcert
    echo.
    echo Or download from:
    echo   https://github.com/FiloSottile/mkcert/releases
    echo.
    echo After installation, restart your terminal and run this script again.
    pause
    exit /b 1
)

echo ✅ mkcert is installed
echo.

REM Install local CA
echo 📦 Installing local Certificate Authority...
mkcert -install
echo.

REM Create certs directory
if not exist "certs" (
    echo 📁 Creating certs directory...
    mkdir certs
) else (
    echo 📁 certs directory already exists
)

cd certs

REM Generate certificates
echo 🔑 Generating SSL certificates...
mkcert localhost 127.0.0.1 ::1

REM Rename files for consistency
echo 📝 Renaming certificate files...
if exist "localhost+2.pem" (
    move /Y localhost+2.pem localhost.pem >nul
)
if exist "localhost+2-key.pem" (
    move /Y localhost+2-key.pem localhost-key.pem >nul
)

cd ..

echo.
echo ==================================================
echo ✅ SSL Certificates Generated Successfully!
echo ==================================================
echo.
echo 📁 Certificate location: .\certs\
echo    - localhost.pem (certificate)
echo    - localhost-key.pem (private key)
echo.
echo 🚀 Next steps:
echo.
echo 1. Start backend with HTTPS:
echo    cd backend
echo    python run_https.py
echo.
echo 2. Start frontend with HTTPS:
echo    cd frontend
echo    npm run dev:https
echo.
echo 3. Access your application:
echo    Backend:  https://localhost:8000
echo    Frontend: https://localhost:3000
echo.
echo 💡 Your browser will trust these certificates automatically!
echo ==================================================
echo.
pause
