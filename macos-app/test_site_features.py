#!/usr/bin/env python3
"""
Test site features for connected sites
"""

from wpbm_manager_mysql import WPBulkManagerMySQL
import json

def test_sites():
    """Test various features for connected sites"""
    manager = WPBulkManagerMySQL()
    
    # Test connected sites
    connected_sites = ['opdee', 'boulderworks', 'renowarriors', 'mavent']
    
    print("🧪 Testing Site Features\n")
    
    for site_name in connected_sites:
        print(f"\n{'='*60}")
        print(f"📍 Testing: {site_name}")
        print('='*60)
        
        # Get site info
        info = manager.get_site_info(site_name)
        
        if 'error' not in info:
            print(f"✅ Site URL: {info['site']['url']}")
            print(f"📁 Folder: {info['folder_path']}")
            print(f"📝 Templates: {len(info['templates'])}")
            
            # Show brand kit info
            if info['brand_kit']:
                print(f"\n🎨 Brand Kit:")
                print(f"  - Voice: {info['brand_kit'].get('brand_voice', 'Not set')}")
                print(f"  - Tone: {', '.join(info['brand_kit'].get('tone_attributes', []))}")
            
            # Test getting content
            try:
                client = manager.get_client(site_name)
                if client:
                    # Get recent pages
                    pages = client.get_content(content_type='page', limit=3)
                    print(f"\n📄 Recent Pages ({len(pages)}):")
                    for page in pages[:3]:
                        title = page.get('title', {}).get('rendered', 'Untitled')
                        print(f"  - {title}")
                    
                    # Get recent posts
                    posts = client.get_content(content_type='post', limit=3)
                    print(f"\n📝 Recent Posts ({len(posts)}):")
                    for post in posts[:3]:
                        title = post.get('title', {}).get('rendered', 'Untitled')
                        print(f"  - {title}")
            except Exception as e:
                print(f"⚠️  Could not fetch content: {str(e)}")
        else:
            print(f"❌ Error: {info['error']}")
    
    # Show database statistics
    print(f"\n\n{'='*60}")
    print("📊 DATABASE STATISTICS")
    print('='*60)
    
    # Get recent activity
    activity = manager.get_recent_activity()
    print(f"\n🔄 Recent Activity ({len(activity)} items):")
    for item in activity[:5]:
        print(f"  - {item['created_at']}: {item['action']} {item['content_type']} on {item['site_name']}")
    
    # Show sites with issues
    print(f"\n⚠️  Sites with Connection Issues:")
    print("  - dmbelectrical.com.au (403 Forbidden - Check IP whitelist)")
    print("  - lawnenforcement.com.au (401 Unauthorized - Check API key or plugin)")

if __name__ == "__main__":
    test_sites()