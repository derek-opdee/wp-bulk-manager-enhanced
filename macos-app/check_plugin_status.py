#!/usr/bin/env python3
"""
Check WP Bulk Manager plugin status
"""
import requests

def check_plugin():
    print("Checking WP Bulk Manager plugin status on opdee.com")
    print("=" * 50)
    
    # Test basic endpoint that should exist
    url = "https://opdee.com/wp-json/wpbm/v1/content?limit=1"
    headers = {"X-API-Key": "8u5foF2Sbegg5nBRt0IVtL6MhsGufq6U"}
    
    print("\n1. Testing existing endpoint (/content)...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Basic endpoint works - plugin is active")
            print(f"   Version: {response.headers.get('X-WPBM-Version', 'Unknown')}")
        else:
            print(f"❌ Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Check new endpoints
    new_endpoints = [
        "/search-replace",
        "/media", 
        "/backup",
        "/content/3040/revisions"
    ]
    
    print("\n2. Checking new endpoints...")
    for endpoint in new_endpoints:
        url = f"https://opdee.com/wp-json/wpbm/v1{endpoint}"
        try:
            # Use OPTIONS to check if endpoint exists
            response = requests.options(url, headers=headers, timeout=5)
            if response.status_code < 400:
                print(f"✅ {endpoint} - Available")
            else:
                print(f"❌ {endpoint} - Not found ({response.status_code})")
        except:
            print(f"❌ {endpoint} - Error")
    
    print("\n3. Plugin file check...")
    print("   The plugin needs to be updated with one of these files:")
    print("   - wp-bulk-manager-client-v2.php (new refactored version)")
    print("   - Or update existing wp-bulk-manager-client.php with new endpoints")
    
    print("\n💡 To activate the v2 plugin:")
    print("   1. Upload wp-bulk-manager-client-v2.php to the plugin folder")
    print("   2. Deactivate the old plugin")
    print("   3. Activate 'WP Bulk Manager Client v2'")
    print("   4. Copy the API key to the new plugin settings")

if __name__ == "__main__":
    check_plugin()