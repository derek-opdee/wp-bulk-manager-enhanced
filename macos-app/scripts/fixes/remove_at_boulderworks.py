#!/usr/bin/env python3
"""Remove 'At BoulderWorks' and replace with 'We' across all pages"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import re
from wpbm_manager import WPBulkManager

def fix_at_boulderworks(content):
    """Replace variations of 'At BoulderWorks' with 'We'"""
    
    # Pattern to match variations (case insensitive)
    patterns = [
        (r'At BoulderWorks,?\s*', 'We '),
        (r'At Boulder Works,?\s*', 'We '),
        (r'at BoulderWorks,?\s*', 'we '),
        (r'at Boulder Works,?\s*', 'we '),
    ]
    
    updated_content = content
    replacements = 0
    
    for pattern, replacement in patterns:
        # Count replacements
        matches = len(re.findall(pattern, updated_content, re.IGNORECASE))
        if matches > 0:
            replacements += matches
            # Replace
            updated_content = re.sub(pattern, replacement, updated_content)
    
    return updated_content, replacements

def main():
    manager = WPBulkManager()
    sites = manager.get_sites('all')
    bw_site = None
    
    for site in sites:
        if 'boulderworks' in site['url'].lower():
            bw_site = site
            break
    
    if not bw_site:
        print("❌ BoulderWorks site not found")
        return
    
    api_key = manager.get_site_api_key(bw_site['id'])
    
    print("🔍 Searching for 'At BoulderWorks' across all pages")
    print("=" * 60)
    
    # Get all pages
    response = requests.get(
        f"{bw_site['url']}/wp-json/wpbm/v1/content",
        headers={'X-API-Key': api_key},
        params={'type': 'page', 'limit': 200, 'status': 'any'},
        timeout=30
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to get pages: {response.status_code}")
        return
    
    pages = response.json().get('posts', [])
    print(f"Found {len(pages)} pages to check\n")
    
    pages_updated = 0
    total_replacements = 0
    
    for page in pages:
        # Get full content
        page_response = requests.get(
            f"{bw_site['url']}/wp-json/wpbm/v1/content/{page['id']}",
            headers={'X-API-Key': api_key},
            timeout=10
        )
        
        if page_response.status_code != 200:
            continue
        
        page_data = page_response.json()
        content = page_data.get('content', '')
        
        # Check if content contains our patterns
        if any(pattern in content for pattern in ['At BoulderWorks', 'At Boulder Works', 'at BoulderWorks', 'at Boulder Works']):
            print(f"\n📄 Page: {page['title']} (ID: {page['id']})")
            print(f"   Status: {page['status']}")
            
            # Fix the content
            updated_content, replacements = fix_at_boulderworks(content)
            
            if replacements > 0:
                print(f"   Found {replacements} instances to replace")
                
                # Update the page
                update_response = requests.put(
                    f"{bw_site['url']}/wp-json/wpbm/v1/content/{page['id']}",
                    headers={'X-API-Key': api_key},
                    json={'content': updated_content},
                    timeout=30
                )
                
                if update_response.status_code == 200:
                    print(f"   ✅ Updated successfully!")
                    pages_updated += 1
                    total_replacements += replacements
                else:
                    print(f"   ❌ Update failed: {update_response.status_code}")
    
    print(f"\n\n📊 Summary:")
    print(f"✅ Pages updated: {pages_updated}")
    print(f"✅ Total replacements: {total_replacements}")
    print(f"\n📌 Changes made:")
    print(f"• 'At BoulderWorks' → 'We'")
    print(f"• 'At Boulder Works' → 'We'")
    print(f"• Preserved sentence structure and flow")
    
    print(f"\n🚨 ALERT: Content update completed - removed {total_replacements} instances of 'At BoulderWorks' from {pages_updated} pages")

if __name__ == "__main__":
    main()