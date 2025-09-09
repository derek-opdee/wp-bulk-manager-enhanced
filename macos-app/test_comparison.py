#!/usr/bin/env python3
"""
Compare old vs new WP Bulk Manager
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
from wpbm_manager import WPBulkManager
from wpbm import WPBMClient
from wpbm.operations.content import ContentOperations

def test_comparison():
    print("Comparing Old vs New WP Bulk Manager")
    print("=" * 50)
    
    # Test OLD manager
    print("\n🔵 Testing OLD WPBulkManager...")
    try:
        old_manager = WPBulkManager()
        sites = old_manager.get_sites('all')
        opdee_site = None
        
        for site in sites:
            if 'opdee' in site['url'].lower():
                opdee_site = site
                break
                
        if opdee_site:
            print(f"✅ Found opdee.com in database")
            api_key = old_manager.get_site_api_key(opdee_site['id'])
            print(f"✅ Retrieved API key: {api_key[:8]}...")
        else:
            print("❌ Opdee not found in old system")
            
    except Exception as e:
        print(f"❌ Old system error: {e}")
    
    # Test NEW system
    print("\n🟢 Testing NEW WPBMClient v2...")
    try:
        # Use the API key provided
        new_client = WPBMClient(
            site_url="https://opdee.com",
            api_key="8u5foF2Sbegg5nBRt0IVtL6MhsGufq6U",
            cache_enabled=True
        )
        
        # Test 1: Get content with caching
        start = time.time()
        result1 = new_client.get('/content', params={'type': 'page', 'limit': 5})
        time1 = time.time() - start
        
        start = time.time()
        result2 = new_client.get('/content', params={'type': 'page', 'limit': 5})
        time2 = time.time() - start
        
        print(f"✅ First request: {time1:.3f}s")
        print(f"✅ Cached request: {time2:.3f}s (speedup: {time1/time2:.1f}x)")
        
        # Test 2: Content operations
        content_ops = ContentOperations(new_client)
        print("\n🔍 Testing search functionality...")
        
        # Simple search for "AI" in pages
        pages = result1.get('posts', [])
        ai_count = 0
        for page in pages[:3]:  # Check first 3 pages
            full_page = new_client.get(f'/content/{page["id"]}')
            content = full_page.get('content', '')
            if 'AI' in content or 'artificial intelligence' in content.lower():
                ai_count += 1
                
        print(f"✅ Found 'AI' mentioned in {ai_count} of {min(3, len(pages))} pages checked")
        
        # Test 3: Cache stats
        cache_stats = new_client.cache.get_stats()
        print(f"\n📊 Cache statistics:")
        print(f"   - Entries: {cache_stats['entries']}")
        print(f"   - Size: {cache_stats['size_mb']} MB")
        
    except Exception as e:
        print(f"❌ New system error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")

if __name__ == "__main__":
    test_comparison()