#!/usr/bin/env python3
"""
Quick summary of all site statuses
"""

from wpbm_manager_mysql import WPBulkManagerMySQL

def show_summary():
    """Show site status summary"""
    manager = WPBulkManagerMySQL()
    
    print("🏢 WordPress Bulk Manager - Site Status Summary")
    print("=" * 60)
    
    sites = manager.list_sites()
    
    connected = 0
    total = len(sites)
    
    for site in sites:
        status_icon = "✅" if site['status'] == 'active' else "❌"
        has_folder = "📁" if site.get('folder_path') else "❌"
        has_templates = "📝" if site.get('has_templates') else "❌"
        has_brand = "🎨" if site.get('has_brand_kit') else "❌"
        
        print(f"\n{status_icon} {site['name']}")
        print(f"   URL: {site['url']}")
        print(f"   Folder: {has_folder}  Templates: {has_templates}  Brand Kit: {has_brand}")
        print(f"   Last Access: {site.get('last_accessed', 'Never')}")
        
        if site['status'] == 'active':
            connected += 1
    
    print(f"\n📊 Summary: {connected}/{total} sites successfully configured")
    print(f"💾 Database: opdee-bulk-manager (MySQL)")
    print(f"📂 Folders: ~/Documents/WPBulkManager/sites/")
    
    print(f"\n✅ Working Sites:")
    working = ['opdee', 'boulderworks', 'renowarriors', 'mavent']
    for site in working:
        print(f"   - {site}")
    
    print(f"\n⚠️  Sites Needing Attention:")
    print(f"   - dmbelectrical (403 Forbidden - Check IP whitelist)")
    print(f"   - lawnenforcement (401 Unauthorized - Check plugin/API key)")

if __name__ == "__main__":
    show_summary()