"""
Test script to verify rate limiting is working correctly.
"""
import requests
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"


def test_rate_limit(endpoint: str, method: str = "GET", data: Dict[str, Any] = None, expected_limit: int = 5):
    """
    Test rate limiting for a specific endpoint.
    
    Args:
        endpoint: API endpoint to test
        method: HTTP method (GET, POST, etc.)
        data: Request data for POST requests
        expected_limit: Expected number of requests before rate limit
    """
    print(f"\n{'='*60}")
    print(f"Testing: {method} {endpoint}")
    print(f"Expected limit: {expected_limit} requests")
    print(f"{'='*60}")
    
    success_count = 0
    rate_limited = False
    
    for i in range(expected_limit + 2):
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            elif method == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=5)
            
            print(f"Request {i+1}: Status {response.status_code}", end="")
            
            # Check for rate limit headers
            if "X-RateLimit-Limit" in response.headers:
                print(f" | Limit: {response.headers['X-RateLimit-Limit']}", end="")
                print(f" | Remaining: {response.headers['X-RateLimit-Remaining']}", end="")
            
            if response.status_code == 429:
                print(" | ⚠️  RATE LIMITED")
                rate_limited = True
                break
            elif response.status_code < 400:
                print(" | ✅ Success")
                success_count += 1
            else:
                print(f" | ❌ Error: {response.json().get('detail', 'Unknown error')}")
            
            time.sleep(0.1)  # Small delay between requests
            
        except requests.exceptions.RequestException as e:
            print(f"Request {i+1}: ❌ Connection error: {e}")
            break
    
    print(f"\nResults:")
    print(f"  Successful requests: {success_count}")
    print(f"  Rate limited: {'Yes ✅' if rate_limited else 'No ❌'}")
    
    return rate_limited


def main():
    """Run rate limiting tests."""
    print("\n" + "="*60)
    print("RATE LIMITING TEST SUITE")
    print("="*60)
    print("\nMake sure the backend server is running on http://localhost:8000")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Test 1: Health check (no rate limit)
        print("\n📋 Test 1: Health Check (should not be rate limited)")
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Status: {response.status_code} | Response: {response.json()}")
        
        # Test 2: Login endpoint (5/minute)
        print("\n📋 Test 2: Login Endpoint (5/minute)")
        test_rate_limit(
            "/auth/login",
            method="POST",
            data={"email": "test@example.com", "password": "wrongpassword"},
            expected_limit=5
        )
        
        # Wait for rate limit to reset
        print("\n⏳ Waiting 60 seconds for rate limit to reset...")
        time.sleep(60)
        
        # Test 3: Job search endpoint (30/minute)
        print("\n📋 Test 3: Job Search Endpoint (30/minute)")
        test_rate_limit("/jobs?limit=10", method="GET", expected_limit=30)
        
        print("\n" + "="*60)
        print("✅ Rate limiting tests completed!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except requests.exceptions.ConnectionError:
        print("\n\n❌ Error: Could not connect to backend server")
        print("Make sure the server is running on http://localhost:8000")


if __name__ == "__main__":
    main()
