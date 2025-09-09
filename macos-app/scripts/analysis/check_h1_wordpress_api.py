#!/usr/bin/env python3
"""Check H1 issues using standard WordPress REST API"""

import requests
import re
from bs4 import BeautifulSoup

def main():
    site_url = "https://www.boulderworks.net"
    
    print("🔍 H1 Analysis for BoulderWorks Pages (Using WordPress API)")
    print("=" * 80)
    
    # Get all pages using standard WordPress API
    response = requests.get(
        f"{site_url}/wp-json/wp/v2/pages",
        params={'per_page': 100, 'status': 'publish'},
        timeout=30
    )
    
    if response.status_code != 200:
        print(f"Failed to get pages: {response.status_code}")
        return
        
    pages = response.json()
    print(f"Found {len(pages)} published pages\n")
    
    missing_h1 = []
    multiple_h1 = []
    has_proper_h1 = []
    
    for page in pages:
        # Get rendered content
        content = page.get('content', {}).get('rendered', '')
        title = page.get('title', {}).get('rendered', '')
        
        # Parse HTML
        soup = BeautifulSoup(content, 'html.parser')
        h1_tags = soup.find_all('h1')
        h1_count = len(h1_tags)
        
        # Check for Gutenberg blocks in raw content
        raw_content = page.get('content', {}).get('raw', '')
        has_gutenberg = '<!-- wp:' in raw_content if raw_content else False
        
        if h1_count == 0:
            missing_h1.append({
                'id': page['id'],
                'title': title,
                'slug': page['slug'],
                'has_gutenberg': has_gutenberg
            })
        elif h1_count > 1:
            multiple_h1.append({
                'id': page['id'],
                'title': title,
                'slug': page['slug'],
                'count': h1_count,
                'has_gutenberg': has_gutenberg,
                'h1_texts': [h1.get_text().strip() for h1 in h1_tags]
            })
        else:
            has_proper_h1.append({
                'title': title,
                'h1_text': h1_tags[0].get_text().strip() if h1_tags else ''
            })
    
    # Print results
    print(f"📊 Summary:")
    print(f"✅ Pages with proper H1: {len(has_proper_h1)}")
    print(f"❌ Pages missing H1: {len(missing_h1)}")
    print(f"⚠️  Pages with multiple H1: {len(multiple_h1)}")
    
    if missing_h1:
        print(f"\n🚨 Pages MISSING H1 tags ({len(missing_h1)}):")
        for page in missing_h1:
            print(f"  - [{page['id']}] {page['title']} (/{page['slug']})")
    
    if multiple_h1:
        print(f"\n⚠️  Pages with MULTIPLE H1 tags ({len(multiple_h1)}):")
        for page in multiple_h1:
            print(f"  - [{page['id']}] {page['title']} - {page['count']} H1s")
            print(f"    H1 texts: {', '.join(page['h1_texts'][:3])}")
    
    # Alert completion
    total_issues = len(missing_h1) + len(multiple_h1)
    alert_msg = f"H1 analysis completed - {total_issues} issues found ({len(missing_h1)} missing, {len(multiple_h1)} multiple)"
    print(f"\n🚨 ALERT: {alert_msg}")
    
    print("\n📌 Note: The WP Bulk Manager plugin appears to be inactive.")
    print("To fix H1 issues, you'll need to:")
    print("1. Re-activate the WP Bulk Manager plugin on BoulderWorks")
    print("2. Or edit pages directly in WordPress admin")

if __name__ == "__main__":
    main()