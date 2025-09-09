#!/usr/bin/env python3
"""
Test WP Bulk Manager v2 with opdee.com
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm import WPBMClient
from wpbm.operations.content import ContentOperations
from wpbm.operations.media import MediaOperations
from wpbm.utils.cache import CacheManager

def test_opdee():
    """Test all v2 features with opdee.com"""
    
    print("🧪 Testing WP Bulk Manager v2 with opdee.com")
    print("=" * 60)
    
    # Initialize client with caching
    print("\n1️⃣ Initializing client with caching...")
    try:
        client = WPBMClient(
            site_url="https://opdee.com",
            api_key="8u5foF2Sbegg5nBRt0IVtL6MhsGufq6U",
            cache_enabled=True,
            cache_ttl=300
        )
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return
    
    # Test getting content
    print("\n2️⃣ Testing content retrieval...")
    try:
        pages = client.get_content(content_type='page', limit=5)
        print(f"✅ Retrieved {len(pages)} pages")
        if pages:
            print(f"   First page: {pages[0]['title']}")
    except Exception as e:
        print(f"❌ Failed to get content: {e}")
    
    # Test caching by making same request
    print("\n3️⃣ Testing cache (making same request)...")
    try:
        import time
        start = time.time()
        pages1 = client.get_content(content_type='page', limit=5)
        time1 = time.time() - start
        
        start = time.time()
        pages2 = client.get_content(content_type='page', limit=5)
        time2 = time.time() - start
        
        print(f"✅ First request: {time1:.3f}s")
        print(f"✅ Second request (cached): {time2:.3f}s")
        print(f"   Cache speedup: {time1/time2:.1f}x faster")
    except Exception as e:
        print(f"❌ Cache test failed: {e}")
    
    # Get cache statistics
    print("\n4️⃣ Cache statistics...")
    try:
        cache_stats = client.cache.get_stats()
        print(f"✅ Cache stats:")
        print(f"   Entries: {cache_stats['entries']}")
        print(f"   Size: {cache_stats['size_mb']} MB")
        print(f"   TTL: {cache_stats['ttl_seconds']}s")
    except Exception as e:
        print(f"❌ Failed to get cache stats: {e}")
    
    # Test search & replace (dry run)
    print("\n5️⃣ Testing search & replace (dry run)...")
    try:
        content_ops = ContentOperations(client)
        results = content_ops.search_replace_content(
            search="AI",
            replace="artificial intelligence",
            post_types=['page'],
            dry_run=True
        )
        print(f"✅ Search & replace results:")
        print(f"   Total posts scanned: {results['total_posts']}")
        print(f"   Posts with matches: {len(results['changes'])}")
        print(f"   Total replacements: {results['total_replacements']}")
        
        if results['changes']:
            print(f"\n   First match:")
            change = results['changes'][0]
            print(f"   - Page: {change['title']}")
            print(f"   - Content replacements: {change['content_replacements']}")
            print(f"   - Title replacements: {change['title_replacements']}")
    except Exception as e:
        print(f"❌ Search & replace failed: {e}")
    
    # Test media operations
    print("\n6️⃣ Testing media operations...")
    try:
        media_ops = MediaOperations(client)
        media_items = media_ops.list_media(limit=5)
        print(f"✅ Retrieved {len(media_items)} media items")
        
        if media_items:
            print(f"   First media: {media_items[0].get('title', 'Untitled')}")
            print(f"   Type: {media_items[0].get('mime_type', 'Unknown')}")
    except Exception as e:
        print(f"❌ Media operations failed: {e}")
    
    # Test getting single content item
    print("\n7️⃣ Testing single content retrieval...")
    try:
        if pages:
            page_id = pages[0]['id']
            single_page = client.get_content_by_id(page_id)
            print(f"✅ Retrieved page ID {page_id}: {single_page['title']}")
            print(f"   Status: {single_page['status']}")
            print(f"   Modified: {single_page['modified']}")
    except Exception as e:
        print(f"❌ Single content retrieval failed: {e}")
    
    # Test the search-replace endpoint directly
    print("\n8️⃣ Testing search-replace API endpoint...")
    try:
        # This will fail if the endpoint doesn't exist on the WordPress side
        sr_results = client.search_replace(
            search="Opdee",
            replace="Opdee AI",
            post_types=['page'],
            dry_run=True
        )
        print(f"✅ Search-replace endpoint works!")
        print(f"   Would modify {sr_results.get('posts_modified', 0)} posts")
    except Exception as e:
        print(f"⚠️  Search-replace endpoint not available (needs plugin update): {e}")
    
    # Clear cache at the end
    print("\n9️⃣ Clearing cache...")
    try:
        client.cache.clear()
        print("✅ Cache cleared successfully")
    except Exception as e:
        print(f"❌ Failed to clear cache: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Testing complete!")

if __name__ == "__main__":
    test_opdee()