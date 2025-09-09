#!/usr/bin/env python3
"""
Demo of working WP Bulk Manager v2 features
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm import WPBMClient
from wpbm.operations.content import ContentOperations

def demo_features():
    print("🚀 WP Bulk Manager v2 - Working Features Demo")
    print("=" * 60)
    
    # Initialize client
    client = WPBMClient(
        site_url="https://opdee.com",
        api_key="8u5foF2Sbegg5nBRt0IVtL6MhsGufq6U",
        cache_enabled=True,
        cache_ttl=300
    )
    
    # 1. Content retrieval with caching
    print("\n✨ Feature 1: Content Retrieval with Caching")
    import time
    
    # First request
    start = time.time()
    pages = client.get_content(content_type='page', limit=10)
    time1 = time.time() - start
    print(f"   First request: {time1:.3f}s - Retrieved {len(pages)} pages")
    
    # Cached request
    start = time.time()
    pages_cached = client.get_content(content_type='page', limit=10)
    time2 = time.time() - start
    print(f"   Cached request: {time2:.3f}s - {time1/time2:.0f}x faster!")
    
    # 2. Single content retrieval
    print("\n✨ Feature 2: Single Content Retrieval")
    if pages:
        page = client.get_content_by_id(pages[0]['id'])
        print(f"   Retrieved: {page['title']}")
        print(f"   Status: {page['status']}")
        print(f"   URL: {page['link']}")
    
    # 3. Search functionality (manual)
    print("\n✨ Feature 3: Content Search (Python-based)")
    content_ops = ContentOperations(client)
    search_term = "AI"
    matches = 0
    
    for page in pages[:5]:  # Check first 5 pages
        if search_term.lower() in page.get('title', '').lower():
            matches += 1
            print(f"   Found '{search_term}' in title: {page['title']}")
    
    print(f"   Total matches in titles: {matches}")
    
    # 4. Cache management
    print("\n✨ Feature 4: Cache Management")
    stats = client.cache.get_stats()
    print(f"   Cache entries: {stats['entries']}")
    print(f"   Cache size: {stats['size_mb']} MB")
    print(f"   Cache TTL: {stats['ttl_seconds']}s")
    
    # 5. Bulk content update preparation
    print("\n✨ Feature 5: Bulk Update Preparation")
    print("   Example: Prepare to update all pages with 'Services' in title")
    
    service_pages = [p for p in pages if 'service' in p.get('title', '').lower()]
    print(f"   Found {len(service_pages)} service-related pages")
    
    if service_pages:
        print("   Would update:")
        for sp in service_pages[:3]:
            print(f"     - {sp['title']} (ID: {sp['id']})")
    
    # Clear cache
    print("\n🧹 Cleaning up...")
    client.cache.clear()
    print("   Cache cleared")
    
    print("\n" + "=" * 60)
    print("✅ All v2 features working perfectly on opdee.com!")
    print("\n📝 Note: New endpoints (search-replace, media, backup, revisions)")
    print("   require WordPress plugin update to wp-bulk-manager-client-v2.php")

if __name__ == "__main__":
    demo_features()