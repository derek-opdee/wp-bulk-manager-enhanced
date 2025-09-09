#!/usr/bin/env python3
"""Upload signage service pages to WordPress as drafts"""

import sys
import os
# Add parent directory to path to import wpbm_manager
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from wpbm_manager import WPBulkManager

def upload_pages_to_wordpress():
    """Upload all signage pages as drafts"""
    
    # Define pages to upload
    pages = [
        {
            'title': 'Custom Business Signage',
            'file': 'business_signage_page.html',
            'slug': 'custom-business-signage'
        },
        {
            'title': 'Branded Environment Solutions',
            'file': 'branded_environments_page.html',
            'slug': 'branded-environment-solutions'
        },
        {
            'title': 'Indoor Signs',
            'file': 'indoor_signs_page.html',
            'slug': 'indoor-signs'
        },
        {
            'title': 'Outdoor Signs',
            'file': 'outdoor_signs_page.html',
            'slug': 'outdoor-signs'
        },
        {
            'title': 'Lobby Signs',
            'file': 'lobby_signs_page.html',
            'slug': 'lobby-signs'
        },
        {
            'title': 'Corporate Signs',
            'file': 'corporate_signs_page.html',
            'slug': 'corporate-signs'
        },
        {
            'title': 'Business Signs',
            'file': 'business_signs_page.html',
            'slug': 'business-signs'
        }
    ]
    
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
    
    print("📤 Uploading Signage Service Pages to WordPress")
    print("=" * 60)
    
    uploaded = 0
    
    for page in pages:
        print(f"\n📄 Uploading: {page['title']}")
        
        # Read the HTML content
        file_path = os.path.join('temp', page['file'])
        if not os.path.exists(file_path):
            print(f"   ❌ File not found: {file_path}")
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Create the page
        page_data = {
            'title': page['title'],
            'content': content,
            'status': 'draft',
            'type': 'page',
            'slug': page['slug'],
            'seo': {
                'title': f"{page['title']} | BoulderWorks - Longmont, CO",
                'description': f"Professional {page['title'].lower()} services in Longmont, Colorado. Precision laser cutting and fabrication for businesses. Get a free quote today!"
            }
        }
        
        response = requests.post(
            f"{bw_site['url']}/wp-json/wpbm/v1/content",
            headers={'X-API-Key': api_key},
            json=page_data,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"   ✅ Created successfully!")
            print(f"   ID: {result.get('post_id', 'Unknown')}")
            print(f"   URL: {result.get('permalink', 'Unknown')}")
            uploaded += 1
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
    
    print(f"\n\n📊 Summary:")
    print(f"✅ Successfully uploaded: {uploaded}/{len(pages)} pages")
    print(f"\n📌 Next Steps:")
    print(f"1. Review pages in WordPress admin")
    print(f"2. Add featured images for each service")
    print(f"3. Link pages from main Services page")
    print(f"4. Publish when ready")
    
    print(f"\n🚨 ALERT: Signage pages upload completed - {uploaded} draft pages created in WordPress")

if __name__ == "__main__":
    upload_pages_to_wordpress()