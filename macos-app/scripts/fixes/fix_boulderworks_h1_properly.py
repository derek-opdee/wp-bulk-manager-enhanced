#!/usr/bin/env python3
"""Fix H1 issues on BoulderWorks pages while preserving content structure"""

import requests
import re
from wpbm_manager import WPBulkManager

def fix_multiple_h1_services_page(content):
    """Fix the Browse/Our Services duplicate H1 issue"""
    # For non-Gutenberg content, just change the first H1 to H2
    if '<!-- wp:' not in content:
        # Replace first H1 (Browse) with H2
        content = content.replace('<h1>Browse</h1>', '<h2>Browse</h2>', 1)
    else:
        # For Gutenberg, change the heading level
        content = re.sub(
            r'<!-- wp:heading {"level":1} -->\s*<h1>Browse</h1>\s*<!-- /wp:heading -->',
            '<!-- wp:heading {"level":2} -->\n<h2>Browse</h2>\n<!-- /wp:heading -->',
            content
        )
    return content

def add_h1_to_page(content, title, has_gutenberg):
    """Add H1 to pages missing it"""
    if has_gutenberg:
        # Add Gutenberg heading block at the beginning
        h1_block = f'<!-- wp:heading {{"level":1}} -->\n<h1>{title}</h1>\n<!-- /wp:heading -->\n\n'
        return h1_block + content
    else:
        # For non-Gutenberg pages, add simple H1
        return f'<h1>{title}</h1>\n\n{content}'

def main():
    manager = WPBulkManager()
    
    # Get BoulderWorks site
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
    
    print("🔧 Fixing H1 Issues on BoulderWorks")
    print("=" * 60)
    
    # Define fixes needed based on our analysis
    fixes_needed = [
        {
            'id': 3127,
            'title': 'Project Gallery Page',
            'action': 'add_h1',
            'has_gutenberg': True
        },
        {
            'id': 1214,
            'title': 'Thank You For Contacting Us',
            'action': 'add_h1',
            'has_gutenberg': False
        },
        {
            'id': 5,
            'title': 'Blog',
            'action': 'add_h1',
            'has_gutenberg': False
        },
        {
            'id': 830,
            'title': 'Our Services',
            'action': 'fix_multiple',
            'has_gutenberg': False
        }
    ]
    
    fixed = 0
    
    for fix in fixes_needed:
        print(f"\n📄 Processing: {fix['title']} (ID: {fix['id']})")
        
        # Get current content
        response = requests.get(
            f"{bw_site['url']}/wp-json/wpbm/v1/content/{fix['id']}",
            headers={'X-API-Key': api_key},
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"   ❌ Failed to get content: {response.status_code}")
            continue
        
        page_data = response.json()
        content = page_data.get('content', '')
        
        # Apply fix based on action needed
        if fix['action'] == 'add_h1':
            print(f"   Adding H1 tag...")
            new_content = add_h1_to_page(content, fix['title'], fix['has_gutenberg'])
        elif fix['action'] == 'fix_multiple':
            print(f"   Fixing multiple H1 tags...")
            new_content = fix_multiple_h1_services_page(content)
        
        # Update the page
        update_response = requests.put(
            f"{bw_site['url']}/wp-json/wpbm/v1/content/{fix['id']}",
            headers={'X-API-Key': api_key},
            json={'content': new_content},
            timeout=30
        )
        
        if update_response.status_code == 200:
            print(f"   ✅ Successfully updated!")
            fixed += 1
        else:
            print(f"   ❌ Update failed: {update_response.status_code}")
            print(f"   Error: {update_response.text[:200]}")
    
    # Alert completion
    alert_msg = f"H1 fixes completed - {fixed}/{len(fixes_needed)} pages updated successfully"
    print(f"\n\n🚨 ALERT: {alert_msg}")
    
    print("\n📌 Summary:")
    print(f"• Fixed {fixed} pages out of {len(fixes_needed)}")
    print("• Preserved Gutenberg block structure where present")
    print("• Added H1 tags to pages missing them")
    print("• Fixed duplicate H1 on Services page")
    
    if fixed == len(fixes_needed):
        print("\n✅ All H1 issues have been resolved!")
    else:
        print("\n⚠️ Some pages couldn't be updated. Check errors above.")

if __name__ == "__main__":
    main()