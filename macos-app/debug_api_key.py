#!/usr/bin/env python3
"""
Debug API key issues with opdee.com
"""
import requests
import json

def debug_api():
    print("🔍 Debugging WP Bulk Manager API Connection")
    print("=" * 60)
    
    api_key = "U9RCZwoMPqxuEVbo6frJRGr50NVv3UIT"
    base_url = "https://opdee.com"
    
    print(f"API Key: {api_key[:8]}...{api_key[-8:]}")
    print(f"Site: {base_url}")
    print()
    
    # Test 1: Check if REST API is accessible
    print("1. Testing WordPress REST API availability...")
    try:
        response = requests.get(f"{base_url}/wp-json/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ REST API is accessible")
            print(f"   Site name: {data.get('name', 'Unknown')}")
            
            # Check for wpbm namespace
            namespaces = data.get('namespaces', [])
            if 'wpbm/v1' in namespaces:
                print(f"   ✅ WP Bulk Manager namespace found")
            else:
                print(f"   ❌ WP Bulk Manager namespace NOT found")
                print(f"   Available namespaces: {', '.join(namespaces)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Check the wpbm endpoint
    print("\n2. Testing WP Bulk Manager endpoint...")
    headers = {"X-API-Key": api_key}
    
    try:
        response = requests.get(f"{base_url}/wp-json/wpbm/v1/content?type=page&limit=1", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("\n   ❌ Authentication failed - API key not accepted")
            print("\n   Possible issues:")
            print("   1. The API key in WordPress doesn't match")
            print("   2. The plugin is not using the fixed version")
            print("   3. The API key wasn't saved properly")
            
            # Try without API key to see different error
            print("\n3. Testing without API key...")
            response2 = requests.get(f"{base_url}/wp-json/wpbm/v1/content?type=page&limit=1")
            print(f"   Status: {response2.status_code}")
            print(f"   Response: {response2.text[:200]}...")
            
            if response.status_code == response2.status_code:
                print("\n   🔍 Same error with and without key - key might not be checked properly")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Try to find the issue
    print("\n4. Troubleshooting steps:")
    print("   1. In WordPress admin, go to Settings → Bulk Manager")
    print("   2. Check if the API key shows: U9RCZwoMPqxuEVbo6frJRGr50NVv3UIT")
    print("   3. If not, click 'Generate API Key' button")
    print("   4. Make sure to click 'Save Changes' after key appears")
    print("   5. The key should persist after page reload")
    print("\n   If the key doesn't save:")
    print("   - Make sure you activated 'WP Bulk Manager Client (Fixed)'")
    print("   - Deactivate the old 'WP Bulk Manager Client' if still active")
    print("   - Check browser console for JavaScript errors")

if __name__ == "__main__":
    debug_api()