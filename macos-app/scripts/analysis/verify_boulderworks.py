#!/usr/bin/env python3
"""Verify BoulderWorks connection after API key setup"""

from wpbm_manager import WPBulkManager
import requests

def verify_boulderworks():
    print("Verifying BoulderWorks connection...")
    print("="*50)
    
    manager = WPBulkManager()
    
    # Get BoulderWorks site
    sites = manager.get_sites('all')
    bw_site = None
    
    for site in sites:
        if 'boulderworks' in site['url'].lower():
            bw_site = site
            break
    
    if not bw_site:
        print("❌ BoulderWorks site not found in database")
        return
    
    print(f"✅ Found site: {bw_site['name']}")
    print(f"   URL: {bw_site['url']}")
    print(f"   Status: {bw_site['status']}")
    
    # Get API key
    api_key = manager.get_site_api_key(bw_site['id'])
    if not api_key:
        print("❌ API key not found in keychain")
        return
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test connection
    print("\nTesting connection...")
    if manager.test_connection(bw_site['url'], api_key):
        print("✅ Connection successful!")
        
        # Test listing content
        try:
            response = requests.get(
                f"{bw_site['url']}/wp-json/wpbm/v1/content",
                headers={'X-API-Key': api_key},
                params={'type': 'page', 'limit': 5},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ Successfully retrieved {len(data.get('posts', []))} pages")
                print("\nSample pages:")
                for post in data.get('posts', [])[:3]:
                    print(f"  - [{post['id']}] {post['title']}")
            else:
                print(f"❌ Failed to list content: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error listing content: {e}")
    else:
        print("❌ Connection failed!")
        print("\nPlease ensure:")
        print("1. The WP Bulk Manager plugin is activated on BoulderWorks")
        print("2. The API key is saved in WordPress admin (Settings → WP Bulk Manager)")
        print(f"3. The API key in WordPress matches: {api_key}")

if __name__ == "__main__":
    verify_boulderworks()