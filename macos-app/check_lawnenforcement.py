#!/usr/bin/env python3
"""
Check lawnenforcement.com.au connection status
"""

from wpbm.api.client import WPBMClient
import requests

def check_lawnenforcement():
    """Check connection to lawnenforcement.com.au"""
    
    site_url = "https://lawnenforcement.com.au"
    api_key = "17968bd29377e5def11aa1dbec45234a"
    
    print("🔍 Checking lawnenforcement.com.au connection...")
    print(f"URL: {site_url}")
    print(f"API Key: {api_key[:8]}...")
    
    # First check if the site is accessible
    try:
        response = requests.get(site_url, timeout=10)
        print(f"✅ Site accessible (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Site not accessible: {e}")
        return
    
    # Check if WordPress REST API is accessible
    try:
        wp_api_url = f"{site_url}/wp-json/wp/v2/"
        response = requests.get(wp_api_url, timeout=10)
        print(f"✅ WordPress REST API accessible (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ WordPress REST API not accessible: {e}")
    
    # Check if our plugin endpoint exists
    try:
        plugin_health_url = f"{site_url}/wp-json/wpbm/v1/health"
        response = requests.get(plugin_health_url, timeout=10)
        print(f"⚠️  Plugin endpoint status: {response.status_code}")
        if response.status_code == 401:
            print("   → 401 Unauthorized: Plugin installed but needs API key")
        elif response.status_code == 404:
            print("   → 404 Not Found: Plugin not installed or not activated")
        elif response.status_code == 403:
            print("   → 403 Forbidden: IP not whitelisted")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Plugin endpoint error: {e}")
    
    # Try with API key
    try:
        client = WPBMClient(site_url, api_key)
        health = client.get('/health', use_cache=False)
        print(f"✅ API connection successful!")
        print(f"   Health response: {health}")
    except requests.exceptions.HTTPError as e:
        print(f"❌ API connection failed: {e}")
        if "401" in str(e):
            print("   → Check API key is correct")
        elif "403" in str(e):
            print("   → Check IP whitelisting")
        elif "404" in str(e):
            print("   → Check plugin is installed and activated")
    except Exception as e:
        print(f"❌ API connection error: {e}")

if __name__ == "__main__":
    check_lawnenforcement()