"""
Test CORS configuration for the Job Board API.

This test verifies that CORS is properly configured to:
1. Allow requests from configured origins
2. Block requests from unauthorized origins
3. Support preflight OPTIONS requests
4. Include proper CORS headers in responses
5. Support credentials (cookies, auth headers)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings


client = TestClient(app)


class TestCORSConfiguration:
    """Test suite for CORS configuration."""

    def test_cors_allowed_origin_http(self):
        """Test that requests from allowed HTTP origin are accepted."""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_cors_allowed_origin_https(self):
        """Test that requests from allowed HTTPS origin are accepted."""
        response = client.get(
            "/health",
            headers={"Origin": "https://localhost:3000"}
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "https://localhost:3000"
        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_cors_disallowed_origin(self):
        """Test that requests from unauthorized origins are blocked."""
        response = client.get(
            "/health",
            headers={"Origin": "http://malicious-site.com"}
        )
        
        # Request succeeds but CORS headers should not include the malicious origin
        assert response.status_code == 200
        # FastAPI's CORSMiddleware doesn't include access-control-allow-origin
        # for disallowed origins
        assert response.headers.get("access-control-allow-origin") != "http://malicious-site.com"

    def test_cors_preflight_request(self):
        """Test CORS preflight OPTIONS request."""
        response = client.options(
            "/api/jobs",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type,Authorization"
            }
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
        assert "access-control-allow-methods" in response.headers
        assert "POST" in response.headers["access-control-allow-methods"]
        assert "access-control-allow-headers" in response.headers
        assert "content-type" in response.headers["access-control-allow-headers"].lower()
        assert "authorization" in response.headers["access-control-allow-headers"].lower()
        assert "access-control-max-age" in response.headers

    def test_cors_allowed_methods(self):
        """Test that all required HTTP methods are allowed."""
        allowed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
        
        for method in allowed_methods:
            response = client.options(
                "/api/jobs",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": method
                }
            )
            
            assert response.status_code == 200
            assert "access-control-allow-methods" in response.headers
            assert method in response.headers["access-control-allow-methods"]

    def test_cors_allowed_headers(self):
        """Test that required headers are allowed."""
        required_headers = [
            "Content-Type",
            "Authorization",
            "Accept",
            "Origin",
            "X-Requested-With"
        ]
        
        response = client.options(
            "/api/jobs",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": ",".join(required_headers)
            }
        )
        
        assert response.status_code == 200
        assert "access-control-allow-headers" in response.headers
        
        allowed_headers_lower = response.headers["access-control-allow-headers"].lower()
        for header in required_headers:
            assert header.lower() in allowed_headers_lower, f"Header {header} not allowed"

    def test_cors_credentials_support(self):
        """Test that credentials (cookies, auth headers) are supported."""
        response = client.get(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Cookie": "session=test"
            }
        )
        
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_cors_exposed_headers(self):
        """Test that response headers are properly exposed to the browser."""
        response = client.options(
            "/api/jobs",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        assert response.status_code == 200
        # Check if expose headers is present (may vary by endpoint)
        if "access-control-expose-headers" in response.headers:
            exposed_headers = response.headers["access-control-expose-headers"].lower()
            # Verify common exposed headers
            assert any(h in exposed_headers for h in ["content-type", "content-length"])

    def test_cors_max_age_cache(self):
        """Test that preflight responses are cached appropriately."""
        response = client.options(
            "/api/jobs",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        assert response.status_code == 200
        assert "access-control-max-age" in response.headers
        # Verify max-age is set to configured value (3600 seconds = 1 hour)
        assert int(response.headers["access-control-max-age"]) == settings.CORS_MAX_AGE

    def test_cors_with_authentication_header(self):
        """Test CORS with Authorization header."""
        response = client.get(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Authorization": "Bearer fake-token"
            }
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_cors_multiple_origins_configured(self):
        """Test that multiple origins are properly configured."""
        # Verify both HTTP and HTTPS localhost are in the allowed origins
        assert "http://localhost:3000" in settings.cors_origins_list
        assert "https://localhost:3000" in settings.cors_origins_list

    def test_cors_origin_validation(self):
        """Test that CORS origin validation works correctly."""
        # Test with valid origins
        for origin in settings.cors_origins_list:
            response = client.get(
                "/health",
                headers={"Origin": origin}
            )
            assert response.status_code == 200
            assert response.headers.get("access-control-allow-origin") == origin

    def test_cors_no_origin_header(self):
        """Test that requests without Origin header work normally."""
        response = client.get("/health")
        
        assert response.status_code == 200
        # No CORS headers should be present when Origin header is missing
        # (this is normal for same-origin requests)


class TestCORSSecurityHeaders:
    """Test security headers work alongside CORS."""

    def test_security_headers_with_cors(self):
        """Test that security headers are present with CORS requests."""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # Verify CORS headers
        assert "access-control-allow-origin" in response.headers
        # Verify security headers are also present
        assert "x-content-type-options" in response.headers
        assert response.headers["x-content-type-options"] == "nosniff"
        assert "x-frame-options" in response.headers
        assert response.headers["x-frame-options"] == "DENY"


class TestCORSConfiguration_EdgeCases:
    """Test edge cases and error scenarios."""

    def test_cors_with_port_variation(self):
        """Test that port numbers are properly validated."""
        # Different port should be rejected
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:8080"}
        )
        
        assert response.status_code == 200
        # Should not match allowed origin
        assert response.headers.get("access-control-allow-origin") != "http://localhost:8080"

    def test_cors_with_subdomain(self):
        """Test that subdomains are properly validated."""
        response = client.get(
            "/health",
            headers={"Origin": "http://api.localhost:3000"}
        )
        
        assert response.status_code == 200
        # Should not match allowed origin (subdomain is different)
        assert response.headers.get("access-control-allow-origin") != "http://api.localhost:3000"

    def test_cors_case_sensitivity(self):
        """Test that origin matching is case-sensitive for security."""
        response = client.get(
            "/health",
            headers={"Origin": "HTTP://LOCALHOST:3000"}
        )
        
        assert response.status_code == 200
        # Case-sensitive matching - uppercase should not match
        assert response.headers.get("access-control-allow-origin") != "HTTP://LOCALHOST:3000"


def test_cors_settings_validation():
    """Test that CORS settings are properly validated."""
    # Verify settings are loaded correctly
    assert hasattr(settings, 'CORS_ORIGINS')
    assert hasattr(settings, 'CORS_ALLOW_CREDENTIALS')
    assert hasattr(settings, 'CORS_MAX_AGE')
    
    # Verify origins list is properly parsed
    assert isinstance(settings.cors_origins_list, list)
    assert len(settings.cors_origins_list) > 0
    
    # Verify all origins start with http:// or https://
    for origin in settings.cors_origins_list:
        if origin != "*":
            assert origin.startswith("http://") or origin.startswith("https://"), \
                f"Invalid origin format: {origin}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
