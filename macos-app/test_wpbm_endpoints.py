#!/usr/bin/env python3
"""
Test the actual WPBM v1 endpoints found on derekzar.com
"""

import requests
import json
import base64

# Configuration
SITE_URL = "https://derekzar.com"
API_KEY = "0b2d82ec91d2d876558ce460e57a7a1e"
USERNAME = "derek@derekzar.com"

print("=" * 80)
print("Testing WPBM v1 endpoints on derekzar.com")
print("=" * 80)

# Test different authentication methods
def test_endpoint(endpoint, method="GET", data=None):
    """Test an endpoint with different authentication methods"""
    print(f"\nTesting {method} {endpoint}")
    print("-" * 50)
    
    # Method 1: X-API-Key header
    print("1. Using X-API-Key header:")
    headers = {
        "X-API-Key": API_KEY,
        "User-Agent": "WP-Bulk-Manager/2.0",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(f"{SITE_URL}{endpoint}", headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(f"{SITE_URL}{endpoint}", headers=headers, json=data, timeout=30)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Success!")
            return response.json()
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Method 2: Basic Auth with username:api_key
    print("\n2. Using Basic Auth (username:api_key):")
    auth_string = f"{USERNAME}:{API_KEY}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "User-Agent": "WP-Bulk-Manager/2.0",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(f"{SITE_URL}{endpoint}", headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(f"{SITE_URL}{endpoint}", headers=headers, json=data, timeout=30)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Success!")
            return response.json()
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Method 3: X-WP-API-Key header
    print("\n3. Using X-WP-API-Key header:")
    headers = {
        "X-WP-API-Key": API_KEY,
        "User-Agent": "WP-Bulk-Manager/2.0",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(f"{SITE_URL}{endpoint}", headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(f"{SITE_URL}{endpoint}", headers=headers, json=data, timeout=30)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Success!")
            return response.json()
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Method 4: API key as query parameter
    print("\n4. Using API key as query parameter:")
    headers = {
        "User-Agent": "WP-Bulk-Manager/2.0",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"{SITE_URL}{endpoint}?api_key={API_KEY}"
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Success!")
            return response.json()
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    return None

# Test 1: Health check endpoint
result = test_endpoint("/wp-json/wpbm/v1/health")
if result:
    print(f"\nHealth check response: {json.dumps(result, indent=2)}")

# Test 2: Content endpoint
result = test_endpoint("/wp-json/wpbm/v1/content")
if result:
    print(f"\nContent endpoint response: {json.dumps(result, indent=2)[:500]}...")

# Test 3: Plugins endpoint
result = test_endpoint("/wp-json/wpbm/v1/plugins")
if result:
    print(f"\nPlugins endpoint response: {json.dumps(result, indent=2)[:500]}...")

# Test 4: Check if we need to use wpbm/v1 without wp-json prefix
print("\n" + "=" * 80)
print("Testing alternative URL formats")
print("=" * 80)

# Try without wp-json prefix
alt_endpoints = [
    "/wpbm/v1/health",
    "/wp-json/wpbm/v1",
    "/wp-json/wpbm/v1/"
]

for endpoint in alt_endpoints:
    print(f"\nTrying: {SITE_URL}{endpoint}")
    try:
        response = requests.get(
            f"{SITE_URL}{endpoint}",
            headers={
                "X-API-Key": API_KEY,
                "User-Agent": "WP-Bulk-Manager/2.0"
            },
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {str(e)}")

print("\n" + "=" * 80)
print("Test complete")
print("=" * 80)