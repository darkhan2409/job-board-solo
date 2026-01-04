# 🔒 HTTPS Setup Guide

## Development HTTPS

### Quick Start

#### 1. Generate Self-Signed Certificates

**Windows:**
```bash
scripts\generate-certs.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/generate-certs.sh
./scripts/generate-certs.sh
```

This creates:
- `backend/localhost.pem` - SSL certificate
- `backend/localhost-key.pem` - Private key

#### 2. Start Backend with HTTPS

```bash
cd backend
python run_https.py
```

Backend will be available at: https://localhost:8000

#### 3. Start Frontend with HTTPS

```bash
cd frontend
npm run dev:https
```

Frontend will be available at: https://localhost:3000

### Browser Certificate Warning

When using self-signed certificates, browsers will show a security warning. This is normal for development.

**To proceed:**
- Chrome/Edge: Click "Advanced" → "Proceed to localhost (unsafe)"
- Firefox: Click "Advanced" → "Accept the Risk and Continue"

## Production HTTPS

### Option 1: Let's Encrypt (Free)

For production servers with a domain name:

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (runs twice daily)
sudo systemctl enable certbot.timer
```

### Option 2: Cloud Provider SSL

Most cloud providers offer free SSL certificates:

- **Vercel**: Automatic HTTPS for all deployments
- **Netlify**: Automatic HTTPS with Let's Encrypt
- **AWS**: Use AWS Certificate Manager (ACM)
- **Google Cloud**: Use Google-managed SSL certificates
- **Azure**: Use Azure App Service certificates

### Option 3: Nginx Reverse Proxy

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## Environment Configuration

### Backend (.env)

```bash
# Development
HTTPS_ENABLED=true
SSL_CERT_PATH=localhost.pem
SSL_KEY_PATH=localhost-key.pem

# Production
HTTPS_ENABLED=true
SSL_CERT_PATH=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/yourdomain.com/privkey.pem
```

### Frontend (.env.local)

```bash
# Development
NEXT_PUBLIC_API_URL=https://localhost:8000

# Production
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Troubleshooting

### Certificate Not Trusted

**Development:**
- This is expected with self-signed certificates
- Add exception in browser
- Or install certificate in system trust store

**Production:**
- Verify certificate is from trusted CA (Let's Encrypt, etc.)
- Check certificate chain is complete
- Verify domain name matches certificate

### Mixed Content Errors

Ensure all resources (API calls, images, scripts) use HTTPS:

```javascript
// ❌ Bad
const API_URL = 'http://api.example.com';

// ✅ Good
const API_URL = 'https://api.example.com';
```

### CORS Issues with HTTPS

Update CORS configuration in backend:

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://localhost:3000",  # Development
        "https://yourdomain.com",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Security Best Practices

### Development
- ✅ Use self-signed certificates for local testing
- ✅ Never commit private keys to git
- ✅ Add `*.pem` and `*.key` to `.gitignore`

### Production
- ✅ Use certificates from trusted CA (Let's Encrypt)
- ✅ Enable HSTS (HTTP Strict Transport Security)
- ✅ Use strong cipher suites
- ✅ Enable OCSP stapling
- ✅ Set up automatic certificate renewal
- ✅ Monitor certificate expiration

## Additional Resources

- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
- [FastAPI HTTPS Documentation](https://fastapi.tiangolo.com/deployment/https/)
- [Next.js Custom Server](https://nextjs.org/docs/advanced-features/custom-server)
