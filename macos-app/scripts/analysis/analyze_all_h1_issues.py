#!/usr/bin/env python3
"""Comprehensive H1 analysis for all BoulderWorks pages"""

import requests
import json
import re
from wpbm_manager import WPBulkManager

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
    
    # Get all pages
    response = requests.get(
        f"{bw_site['url']}/wp-json/wpbm/v1/content",
        headers={'X-API-Key': api_key},
        params={'type': 'page', 'limit': 100, 'status': 'publish'},
        timeout=30
    )
    
    if response.status_code != 200:
        print(f"Failed to get pages: {response.status_code}")
        return
        
    pages = response.json().get('posts', [])
    
    print("🔍 H1 Analysis for All Published BoulderWorks Pages")
    print("=" * 80)
    print(f"Analyzing {len(pages)} published pages...\n")
    
    missing_h1 = []
    multiple_h1 = []
    has_proper_h1 = []
    
    for page in pages:
        # Get full content
        resp = requests.get(
            f"{bw_site['url']}/wp-json/wpbm/v1/content/{page['id']}",
            headers={'X-API-Key': api_key},
            timeout=10
        )
        
        if resp.status_code == 200:
            content = resp.json().get('content', '')
            
            # Count H1 tags
            h1_count = len(re.findall(r'<h1[^>]*>.*?</h1>', content, re.DOTALL | re.IGNORECASE))
            
            # Check for Gutenberg blocks
            has_gutenberg = '<!-- wp:' in content
            
            if h1_count == 0:
                missing_h1.append({
                    'id': page['id'],
                    'title': page['title'],
                    'has_gutenberg': has_gutenberg
                })
            elif h1_count > 1:
                multiple_h1.append({
                    'id': page['id'],
                    'title': page['title'],
                    'count': h1_count,
                    'has_gutenberg': has_gutenberg
                })
            else:
                has_proper_h1.append(page['title'])
    
    # Print results
    print(f"📊 Summary:")
    print(f"✅ Pages with proper H1: {len(has_proper_h1)}")
    print(f"❌ Pages missing H1: {len(missing_h1)}")
    print(f"⚠️  Pages with multiple H1: {len(multiple_h1)}")
    
    if missing_h1:
        print(f"\n🚨 Pages MISSING H1 tags ({len(missing_h1)}):")
        for page in missing_h1:
            gutenberg = "✓ Gutenberg" if page['has_gutenberg'] else "✗ No Gutenberg"
            print(f"  - [{page['id']}] {page['title']} ({gutenberg})")
    
    if multiple_h1:
        print(f"\n⚠️  Pages with MULTIPLE H1 tags ({len(multiple_h1)}):")
        for page in multiple_h1:
            gutenberg = "✓ Gutenberg" if page['has_gutenberg'] else "✗ No Gutenberg"
            print(f"  - [{page['id']}] {page['title']} - {page['count']} H1s ({gutenberg})")
    
    # Alert completion
    total_issues = len(missing_h1) + len(multiple_h1)
    alert_msg = f"H1 analysis completed - {total_issues} issues found ({len(missing_h1)} missing, {len(multiple_h1)} multiple)"
    print(f"\n🚨 ALERT: {alert_msg}")
    
    # Save report
    report = {
        'site': bw_site['url'],
        'total_pages': len(pages),
        'proper_h1': len(has_proper_h1),
        'missing_h1': missing_h1,
        'multiple_h1': multiple_h1,
        'pages_with_proper_h1': has_proper_h1
    }
    
    with open('boulderworks_h1_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Full report saved to: boulderworks_h1_report.json")
    
    # Gutenberg rules reminder
    print("\n📌 IMPORTANT: When fixing H1 issues:")
    print("• ALWAYS preserve Gutenberg block structure")
    print("• Use <!-- wp:heading {\"level\":1} --> blocks")
    print("• Never inject raw HTML outside of blocks")
    print("• Test in WordPress editor after changes")

if __name__ == "__main__":
    main()