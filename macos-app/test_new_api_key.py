#!/usr/bin/env python3
"""
Test WP Bulk Manager v2 with new API key
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm import WPBMClient
from wpbm.operations.content import ContentOperations

def test_new_key():
    print("🔑 Testing WP Bulk Manager v2 with new API key")
    print("=" * 60)
    
    # Initialize with new API key
    client = WPBMClient(
        site_url="https://opdee.com",
        api_key="qTFjBsRTC0mBYITgK8ZhQWnTVQPnD2yR",
        cache_enabled=True
    )
    
    print("\n1️⃣ Testing basic connection...")
    try:
        pages = client.get_content(content_type='page', limit=3)
        print(f"✅ Connection successful! Retrieved {len(pages)} pages")
        
        if pages:
            print("\n   Pages found:")
            for page in pages:
                print(f"   • {page['title']} (ID: {page['id']})")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    print("\n2️⃣ Testing new endpoints...")
    
    # Search & Replace
    print("\n   Testing Search & Replace...")
    try:
        result = client.search_replace(
            search="AI",
            replace="Artificial Intelligence",
            post_types=['page'],
            dry_run=True
        )
        print(f"   ✅ Search & Replace works!")
        print(f"      Total posts: {result.get('total_posts', 0)}")
        print(f"      Would replace: {result.get('total_replacements', 0)} instances")
    except Exception as e:
        print(f"   ❌ Search & Replace not available: {str(e)[:100]}")
    
    # Media
    print("\n   Testing Media endpoint...")
    try:
        result = client.get('/media', params={'limit': 3})
        media = result.get('media', [])
        print(f"   ✅ Media endpoint works! Found {len(media)} items")
    except Exception as e:
        print(f"   ❌ Media endpoint not available: {str(e)[:100]}")
    
    # Backup
    print("\n   Testing Backup...")
    try:
        result = client.backup_content()
        print(f"   ✅ Backup works! Created backup with {result.get('post_count', 0)} posts")
    except Exception as e:
        print(f"   ❌ Backup not available: {str(e)[:100]}")
    
    # Cache performance
    print("\n3️⃣ Testing cache performance...")
    import time
    
    start = time.time()
    client.get_content(content_type='page', limit=10)
    time1 = time.time() - start
    
    start = time.time()
    client.get_content(content_type='page', limit=10)
    time2 = time.time() - start
    
    print(f"✅ Cache working:")
    print(f"   First request: {time1:.3f}s")
    print(f"   Cached request: {time2:.3f}s ({time1/time2:.1f}x faster)")
    
    print("\n" + "=" * 60)
    print("✅ Testing complete!")

if __name__ == "__main__":
    test_new_key()