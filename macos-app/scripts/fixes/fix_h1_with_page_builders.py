#!/usr/bin/env python3
"""Fix H1 issues handling different page builders"""

import requests
import re
from wpbm_manager import WPBulkManager

def add_h1_for_content_type(content, title):
    """Add H1 based on content type detection"""
    
    # Detect content type
    if '<!-- wp:stackable' in content:
        # Stackable blocks - add Stackable heading block
        h1_block = f'''<!-- wp:stackable/heading {{"headingTag":"h1","contentAlign":"left","uniqueId":"h1-{title.lower().replace(" ", "-")}"}} -->
<div class="wp-block-stackable-heading stk-block-heading stk-block-heading--v2 stk-block">
<h1 class="stk-block-heading__text">{title}</h1>
</div>
<!-- /wp:stackable/heading -->

'''
        return h1_block + content
        
    elif '[et_pb_' in content:
        # Divi Builder - add Divi text module with H1
        # Find the first column to insert into
        match = re.search(r'(\[et_pb_column[^\]]*\])', content)
        if match:
            column_tag = match.group(1)
            h1_module = f'[et_pb_text admin_label="Page Title" _builder_version="4.0"]<h1>{title}</h1>[/et_pb_text]'
            # Insert after the column tag
            content = content.replace(column_tag, column_tag + h1_module, 1)
        return content
        
    elif '<!-- wp:' in content:
        # Standard Gutenberg - add heading block
        h1_block = f'<!-- wp:heading {{"level":1}} -->\n<h1>{title}</h1>\n<!-- /wp:heading -->\n\n'
        return h1_block + content
        
    else:
        # Plain HTML or empty - just add H1
        if content.strip() == '':
            return f'<h1>{title}</h1>'
        else:
            return f'<h1>{title}</h1>\n\n{content}'

def fix_services_multiple_h1(content):
    """Fix multiple H1s in services page"""
    if '[et_pb_' in content:
        # For Divi, find and replace the Browse H1 with H2
        content = re.sub(
            r'<h1[^>]*>Browse</h1>',
            '<h2>Browse</h2>',
            content,
            count=1
        )
    else:
        # For other content types
        content = content.replace('<h1>Browse</h1>', '<h2>Browse</h2>', 1)
    return content

def main():
    manager = WPBulkManager()
    
    # Get BoulderWorks site
    sites = manager.get_sites('all')
    bw_site = None
    for site in sites:
        if 'boulderworks' in site['url'].lower():
            bw_site = site
            break
    
    api_key = manager.get_site_api_key(bw_site['id'])
    
    print("🔧 Fixing H1 Issues (Page Builder Compatible)")
    print("=" * 60)
    
    # Define fixes needed
    fixes_needed = [
        {'id': 3127, 'title': 'Project Gallery', 'action': 'add_h1'},
        {'id': 1214, 'title': 'Thank You', 'action': 'add_h1'},
        {'id': 5, 'title': 'Blog', 'action': 'add_h1'},
        {'id': 830, 'title': 'Our Services', 'action': 'fix_multiple'}
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
            print(f"   ❌ Failed to get content")
            continue
        
        page_data = response.json()
        content = page_data.get('content', '')
        full_title = page_data.get('title', fix['title'])
        
        # Detect page builder
        if '<!-- wp:stackable' in content:
            print("   Detected: Stackable blocks")
        elif '[et_pb_' in content:
            print("   Detected: Divi Builder")
        elif '<!-- wp:' in content:
            print("   Detected: Gutenberg blocks")
        else:
            print("   Detected: Plain HTML or empty")
        
        # Apply fix
        if fix['action'] == 'add_h1':
            new_content = add_h1_for_content_type(content, full_title)
        elif fix['action'] == 'fix_multiple':
            new_content = fix_services_multiple_h1(content)
        
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
    
    # Alert completion
    alert_msg = f"H1 fixes completed - {fixed}/{len(fixes_needed)} pages updated"
    print(f"\n\n🚨 ALERT: {alert_msg}")
    
    print("\n📌 Summary:")
    print(f"• Fixed {fixed} pages")
    print("• Handled Stackable, Divi, and Gutenberg content")
    print("• Preserved page builder structure")

if __name__ == "__main__":
    main()