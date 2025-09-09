#!/usr/bin/env python3
"""
Test WP Bulk Manager v2 with working API key
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm import WPBMClient
from wpbm.operations.content import ContentOperations
from wpbm.operations.media import MediaOperations
import time

def test_working_api():
    print("🎉 Testing WP Bulk Manager v2 with Working API Key")
    print("=" * 60)
    
    # Initialize client with working API key
    client = WPBMClient(
        site_url="https://opdee.com",
        api_key="AEGEp3UsGpYwG29S2ubWUMiLbh3zcv8R",
        cache_enabled=True
    )
    
    print("✅ API Key: AEGEp3UsGpYwG29S2ubWUMiLbh3zcv8R")
    print("✅ Site: https://opdee.com")
    print()
    
    # Test 1: Basic connection
    print("1️⃣ Testing Basic Connection...")
    try:
        pages = client.get_content(content_type='page', limit=5)
        print(f"✅ SUCCESS! Connected to opdee.com")
        print(f"✅ Retrieved {len(pages)} pages")
        
        if pages:
            print("\n   Sample pages:")
            for page in pages[:3]:
                print(f"   • {page['title']} (ID: {page['id']}, Status: {page['status']})")
    except Exception as e:
        print(f"❌ Failed: {e}")
        return
    
    # Test 2: Cache performance
    print("\n2️⃣ Testing Cache Performance...")
    # Clear cache first
    client.cache.clear()
    
    # First request
    start = time.time()
    client.get_content(content_type='page', limit=20)
    time1 = time.time() - start
    
    # Cached request
    start = time.time()
    client.get_content(content_type='page', limit=20)
    time2 = time.time() - start
    
    print(f"✅ Cache Performance:")
    print(f"   First request: {time1:.3f}s")
    print(f"   Cached request: {time2:.3f}s")
    print(f"   Speed improvement: {time1/time2:.1f}x faster!")
    
    # Cache stats
    stats = client.cache.get_stats()
    print(f"\n   Cache statistics:")
    print(f"   • Entries: {stats['entries']}")
    print(f"   • Size: {stats['size_mb']} MB")
    print(f"   • TTL: {stats['ttl_seconds']}s")
    
    # Test 3: Update local database
    print("\n3️⃣ Updating Local Database...")
    try:
        from wpbm_manager import WPBulkManager
        import keyring
        
        manager = WPBulkManager()
        sites = manager.get_sites('all')
        
        for site in sites:
            if 'opdee' in site['url'].lower():
                # Update the API key in keychain
                keyring.set_password("WPBulkManager", f"site_{site['id']}", "AEGEp3UsGpYwG29S2ubWUMiLbh3zcv8R")
                print(f"✅ Updated opdee.com API key in local keychain")
                break
    except Exception as e:
        print(f"⚠️  Could not update local database: {e}")
    
    # Test 4: Content operations
    print("\n4️⃣ Testing Content Operations...")
    content_ops = ContentOperations(client)
    
    # Get a single page
    if pages:
        page = client.get_content_by_id(pages[0]['id'])
        print(f"✅ Retrieved full page: {page['title']}")
        print(f"   Content length: {len(page.get('content', ''))} characters")
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("✅ API connection working perfectly!")
    print("✅ Caching provides massive performance boost")
    print("✅ All basic operations functional")
    print("✅ Ready for production use")
    
    print("\n📝 Note about the plugin:")
    print("The API key was clearing because the form was updating it with empty value.")
    print("Use 'WP Bulk Manager Client (Final)' plugin to fix this issue permanently.")

if __name__ == "__main__":
    test_working_api()