#!/usr/bin/env python3
"""
Comprehensive test script for derekzar.com WP Bulk Manager API connection
"""

import requests
import json
from urllib.parse import urljoin
import base64

# Configuration
SITE_URL = "https://derekzar.com"
API_KEY = "0b2d82ec91d2d876558ce460e57a7a1e"
USERNAME = "derek@derekzar.com"

print("=" * 80)
print("Testing connection to derekzar.com")
print("=" * 80)

# Test 1: Basic WordPress REST API connection
print("\n1. Testing basic WordPress REST API connection...")
try:
    response = requests.get(
        f"{SITE_URL}/wp-json/wp/v2/posts",
        headers={"User-Agent": "WP-Bulk-Manager/2.0"},
        timeout=30
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ Basic WordPress API is accessible")
    else:
        print(f"   ✗ Response: {response.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

# Test 2: Test with API key authentication
print("\n2. Testing with API key authentication...")
try:
    headers = {
        "X-API-Key": API_KEY,
        "User-Agent": "WP-Bulk-Manager/2.0",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{SITE_URL}/wp-json/wp-bulk-manager/v2/test",
        headers=headers,
        timeout=30
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ API key authentication successful")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ✗ Response: {response.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

# Test 3: Test with Basic Authentication
print("\n3. Testing with Basic Authentication...")
try:
    auth_string = f"{USERNAME}:{API_KEY}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "User-Agent": "WP-Bulk-Manager/2.0",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{SITE_URL}/wp-json/wp-bulk-manager/v2/test",
        headers=headers,
        timeout=30
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ Basic authentication successful")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ✗ Response: {response.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

# Test 4: Check plugin status endpoint
print("\n4. Checking WP Bulk Manager plugin status...")
endpoints_to_test = [
    "/wp-json/wp-bulk-manager/v2/status",
    "/wp-json/wp-bulk-manager/v2/info",
    "/wp-json/wp-bulk-manager/v1/status",
    "/wp-json/wpbm/v1/status"
]

for endpoint in endpoints_to_test:
    try:
        print(f"\n   Testing endpoint: {endpoint}")
        
        # Try with API key
        response = requests.get(
            f"{SITE_URL}{endpoint}",
            headers={
                "X-API-Key": API_KEY,
                "User-Agent": "WP-Bulk-Manager/2.0"
            },
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✓ Endpoint accessible")
            print(f"   Response: {response.json()}")
            break
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)}")

# Test 5: Check available REST routes
print("\n5. Checking available REST API routes...")
try:
    response = requests.get(
        f"{SITE_URL}/wp-json",
        headers={"User-Agent": "WP-Bulk-Manager/2.0"},
        timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        routes = data.get("routes", {})
        
        # Look for WP Bulk Manager routes
        wpbm_routes = [route for route in routes.keys() if "bulk" in route.lower() or "wpbm" in route.lower()]
        
        if wpbm_routes:
            print("   ✓ Found WP Bulk Manager routes:")
            for route in wpbm_routes:
                print(f"     - {route}")
        else:
            print("   ✗ No WP Bulk Manager routes found")
            print("   Available namespaces:")
            namespaces = data.get("namespaces", [])
            for ns in namespaces:
                if "wp/" not in ns and "oembed" not in ns:
                    print(f"     - {ns}")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

# Test 6: Direct plugin file check
print("\n6. Testing direct plugin file access...")
plugin_paths = [
    "/wp-content/plugins/wp-bulk-manager-client/wp-bulk-manager-client.php",
    "/wp-content/plugins/wp-bulk-manager/wp-bulk-manager.php",
    "/wp-content/plugins/wpbm-client/wpbm-client.php"
]

for path in plugin_paths:
    try:
        response = requests.head(
            f"{SITE_URL}{path}",
            headers={"User-Agent": "WP-Bulk-Manager/2.0"},
            timeout=10,
            allow_redirects=True
        )
        if response.status_code == 200:
            print(f"   ✓ Plugin file found at: {path}")
            break
        else:
            print(f"   {path}: {response.status_code}")
    except Exception as e:
        print(f"   {path}: Error - {str(e)}")

# Test 7: Test content management endpoints
print("\n7. Testing content management endpoints...")
content_endpoints = [
    ("/wp-json/wp-bulk-manager/v2/content", "GET"),
    ("/wp-json/wp-bulk-manager/v2/pages", "GET"),
    ("/wp-json/wp-bulk-manager/v2/posts", "GET")
]

for endpoint, method in content_endpoints:
    try:
        print(f"\n   Testing {method} {endpoint}")
        
        headers = {
            "X-API-Key": API_KEY,
            "User-Agent": "WP-Bulk-Manager/2.0",
            "Content-Type": "application/json"
        }
        
        if method == "GET":
            response = requests.get(f"{SITE_URL}{endpoint}", headers=headers, timeout=30)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✓ Endpoint accessible")
            data = response.json()
            if isinstance(data, list):
                print(f"   Found {len(data)} items")
            else:
                print(f"   Response type: {type(data)}")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)}")

# Test 8: WordPress Application Password (if needed)
print("\n8. Testing WordPress Application Password authentication...")
try:
    # Try with application password format
    auth_string = f"{USERNAME}:{API_KEY}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    response = requests.get(
        f"{SITE_URL}/wp-json/wp/v2/users/me",
        headers={
            "Authorization": f"Basic {encoded_auth}",
            "User-Agent": "WP-Bulk-Manager/2.0"
        },
        timeout=30
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"   ✓ Authenticated as: {user_data.get('name', 'Unknown')}")
        print(f"   User ID: {user_data.get('id', 'Unknown')}")
    else:
        print(f"   ✗ Authentication failed: {response.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

print("\n" + "=" * 80)
print("Connection test complete")
print("=" * 80)