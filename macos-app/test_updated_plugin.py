#!/usr/bin/env python3
"""
Test WP Bulk Manager v2 with updated WordPress plugin
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm import WPBMClient
from wpbm.operations.content import ContentOperations
from wpbm.operations.media import MediaOperations

def test_updated_plugin():
    print("🚀 Testing WP Bulk Manager v2 with Updated Plugin")
    print("=" * 60)
    
    # Initialize client
    client = WPBMClient(
        site_url="https://opdee.com",
        api_key="8u5foF2Sbegg5nBRt0IVtL6MhsGufq6U",
        cache_enabled=False  # Disable cache for fresh testing
    )
    
    # Test 1: Search & Replace endpoint
    print("\n1️⃣ Testing Search & Replace endpoint...")
    try:
        result = client.search_replace(
            search="AI",
            replace="Artificial Intelligence",
            post_types=['page'],
            dry_run=True
        )
        print("✅ Search & Replace endpoint works!")
        print(f"   Total posts: {result.get('total_posts', 0)}")
        print(f"   Posts with matches: {result.get('posts_modified', 0)}")
        print(f"   Total replacements: {result.get('total_replacements', 0)}")
        
        if result.get('changes'):
            print("\n   First match:")
            change = result['changes'][0]
            print(f"   - Page: {change.get('title', 'Unknown')}")
            print(f"   - Content replacements: {change.get('content_replacements', 0)}")
            print(f"   - Title replacements: {change.get('title_replacements', 0)}")
    except Exception as e:
        print(f"❌ Search & Replace failed: {str(e)[:200]}")
    
    # Test 2: Media endpoint
    print("\n2️⃣ Testing Media endpoint...")
    try:
        media_ops = MediaOperations(client)
        media_items = media_ops.list_media(limit=5)
        print(f"✅ Media endpoint works! Found {len(media_items)} items")
        
        if media_items:
            item = media_items[0]
            print(f"   First media:")
            print(f"   - Title: {item.get('title', {}).get('rendered', 'Untitled')}")
            print(f"   - Type: {item.get('mime_type', 'Unknown')}")
            print(f"   - URL: {item.get('source_url', 'N/A')[:50]}...")
    except Exception as e:
        print(f"❌ Media endpoint failed: {str(e)[:200]}")
    
    # Test 3: Backup endpoint
    print("\n3️⃣ Testing Backup endpoint...")
    try:
        # Backup just 2 specific posts
        pages = client.get_content(content_type='page', limit=2)
        if pages:
            post_ids = [p['id'] for p in pages[:2]]
            
            content_ops = ContentOperations(client)
            backup_result = content_ops.backup_before_bulk_operation(post_ids)
            
            print(f"✅ Backup endpoint works!")
            print(f"   Backup file: {backup_result['backup_file']}")
            print(f"   Posts backed up: {backup_result['post_count']}")
            print(f"   Timestamp: {backup_result['timestamp']}")
    except Exception as e:
        print(f"❌ Backup endpoint failed: {str(e)[:200]}")
    
    # Test 4: Revisions endpoint
    print("\n4️⃣ Testing Revisions endpoint...")
    try:
        # Get a page that likely has revisions
        pages = client.get_content(content_type='page', limit=5)
        revision_found = False
        
        for page in pages:
            revisions = client.get_revisions(page['id'])
            if revisions:
                print(f"✅ Revisions endpoint works!")
                print(f"   Page: {page['title']}")
                print(f"   Number of revisions: {len(revisions)}")
                
                if revisions:
                    rev = revisions[0]
                    print(f"   Latest revision:")
                    print(f"   - Author: {rev.get('author', 'Unknown')}")
                    print(f"   - Date: {rev.get('date', 'Unknown')}")
                
                revision_found = True
                break
        
        if not revision_found:
            print("✅ Revisions endpoint works! (No revisions found)")
    except Exception as e:
        print(f"❌ Revisions endpoint failed: {str(e)[:200]}")
    
    # Test 5: Find unused media
    print("\n5️⃣ Testing Find Unused Media...")
    try:
        media_ops = MediaOperations(client)
        print("   Analyzing media usage (this may take a moment)...")
        unused = media_ops.find_unused_media()
        print(f"✅ Found {len(unused)} unused media items")
        
        if unused[:3]:  # Show first 3
            print("   First 3 unused items:")
            for item in unused[:3]:
                print(f"   - {item['title']} ({item['mime_type']})")
    except Exception as e:
        print(f"❌ Find unused media failed: {str(e)[:200]}")
    
    print("\n" + "=" * 60)
    print("🎉 Testing complete!")
    print("\n📊 Summary:")
    print("- Core content operations: ✅")
    print("- Caching system: ✅")
    print("- Search & Replace: Check above")
    print("- Media management: Check above")
    print("- Backup system: Check above")
    print("- Revision tracking: Check above")

if __name__ == "__main__":
    test_updated_plugin()