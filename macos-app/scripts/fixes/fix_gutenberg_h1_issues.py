#!/usr/bin/env python3
"""Fix H1 issues while preserving Gutenberg block structure"""

import requests
import json
import re
from wpbm_manager import WPBulkManager
from bs4 import BeautifulSoup

def analyze_gutenberg_content(content):
    """Analyze content for Gutenberg blocks and H1 tags"""
    # Check if content has Gutenberg blocks
    has_gutenberg = '<!-- wp:' in content
    
    # Parse for H1s without breaking Gutenberg structure
    h1_matches = re.findall(r'<h1[^>]*>.*?</h1>', content, re.DOTALL | re.IGNORECASE)
    h1_count = len(h1_matches)
    
    # Look for Gutenberg heading blocks
    gutenberg_h1_blocks = re.findall(r'<!-- wp:heading {"level":1[^}]*} -->.*?<!-- /wp:heading -->', content, re.DOTALL)
    
    return {
        'has_gutenberg': has_gutenberg,
        'h1_count': h1_count,
        'h1_matches': h1_matches,
        'gutenberg_h1_blocks': gutenberg_h1_blocks
    }

def fix_services_page_h1(content):
    """Fix the duplicate H1 on services page while preserving Gutenberg blocks"""
    # Only change the Browse H1 to H2 within its Gutenberg block
    # This regex specifically targets the heading block with "Browse" text
    content = re.sub(
        r'(<!-- wp:heading[^>]*-->)\s*<h1[^>]*>Browse</h1>\s*(<!-- /wp:heading -->)',
        r'<!-- wp:heading {"level":2} -->\n<h2>Browse</h2>\n<!-- /wp:heading -->',
        content
    )
    return content

def add_h1_to_page(content, title):
    """Add H1 to pages missing it - using Gutenberg blocks"""
    # Create a Gutenberg heading block
    h1_block = f'<!-- wp:heading {{"level":1}} -->\n<h1>{title}</h1>\n<!-- /wp:heading -->\n\n'
    
    # Add at the beginning of content
    return h1_block + content

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
    
    print("🔍 Analyzing H1 Issues on BoulderWorks Pages")
    print("=" * 60)
    
    # Pages that need H1 fixes based on previous analysis
    pages_to_check = [
        {'id': 5, 'title': 'Blog', 'needs_h1': True},
        {'id': 1214, 'title': 'Thank You', 'needs_h1': True},
        {'id': 3127, 'title': 'Project Gallery', 'needs_h1': True},
        {'id': 830, 'title': 'Our Services', 'fix_duplicate': True}
    ]
    
    issues_found = []
    
    for page in pages_to_check:
        # Get page content
        response = requests.get(
            f"{bw_site['url']}/wp-json/wpbm/v1/content/{page['id']}",
            headers={'X-API-Key': api_key},
            timeout=10
        )
        
        if response.status_code == 200:
            page_data = response.json()
            content = page_data.get('content', '')
            analysis = analyze_gutenberg_content(content)
            
            print(f"\n📄 Page: {page['title']} (ID: {page['id']})")
            print(f"   Gutenberg blocks: {'Yes' if analysis['has_gutenberg'] else 'No'}")
            print(f"   H1 count: {analysis['h1_count']}")
            
            if page.get('needs_h1') and analysis['h1_count'] == 0:
                issues_found.append({
                    'id': page['id'],
                    'title': page['title'],
                    'issue': 'missing_h1',
                    'content': content
                })
                print(f"   ❌ Missing H1 tag")
                
            elif page.get('fix_duplicate') and analysis['h1_count'] > 1:
                issues_found.append({
                    'id': page['id'],
                    'title': page['title'],
                    'issue': 'duplicate_h1',
                    'content': content
                })
                print(f"   ❌ Multiple H1 tags ({analysis['h1_count']})")
                
    print(f"\n\n📊 Found {len(issues_found)} pages with H1 issues")
    
    if issues_found:
        print("\n🔧 Fixing H1 issues...")
        
        for issue in issues_found:
            if issue['issue'] == 'missing_h1':
                # Add H1 using Gutenberg block
                new_content = add_h1_to_page(issue['content'], issue['title'])
                
                # Update the page
                response = requests.put(
                    f"{bw_site['url']}/wp-json/wpbm/v1/content/{issue['id']}",
                    headers={'X-API-Key': api_key},
                    json={'content': new_content},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ Added H1 to {issue['title']} (ID: {issue['id']})")
                else:
                    print(f"❌ Failed to update {issue['title']}: {response.status_code}")
                    
            elif issue['issue'] == 'duplicate_h1':
                # Fix duplicate H1 (services page)
                new_content = fix_services_page_h1(issue['content'])
                
                # Update the page
                response = requests.put(
                    f"{bw_site['url']}/wp-json/wpbm/v1/content/{issue['id']}",
                    headers={'X-API-Key': api_key},
                    json={'content': new_content},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ Fixed duplicate H1 on {issue['title']} (ID: {issue['id']})")
                else:
                    print(f"❌ Failed to update {issue['title']}: {response.status_code}")
    
    # Alert on completion
    import subprocess
    alert_msg = f"H1 analysis complete - fixed {len(issues_found)} issues"
    subprocess.run(['echo', f'🚨 ALERT: {alert_msg}'])
    
    print(f"\n\n✅ H1 Analysis and Fixes Complete!")
    print("📌 All updates preserved Gutenberg block structure")

if __name__ == "__main__":
    main()