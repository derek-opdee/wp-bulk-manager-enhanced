#!/usr/bin/env python3
"""Fix SEO issues for BoulderWorks pages"""

import json
import requests
from wpbm_manager import WPBulkManager
from concurrent.futures import ThreadPoolExecutor, as_completed

# Priority pages to fix
PRIORITY_FIXES = {
    4: {  # Home page
        'seo_title': 'Laser Cutting & Engraving Services in Boulder, Colorado | BoulderWorks',
        'seo_description': 'Professional laser cutting, engraving, and fabrication services in Boulder, CO. Custom awards, signs, metal cutting, and more. Get a quote today!',
        'add_h1': False  # Already has H1
    },
    6: {  # Contact
        'seo_title': 'Contact BoulderWorks | Laser Cutting Services in Boulder, CO',
        'seo_description': 'Contact BoulderWorks for laser cutting, engraving, and custom fabrication in Boulder, Colorado. Get a free quote for your project today!',
        'add_h1': False
    },
    352: {  # About
        'seo_title': 'About BoulderWorks | Laser Cutting Experts in Boulder, CO', 
        'seo_description': 'Learn about BoulderWorks, Boulder Colorado\'s premier laser cutting and engraving company. Over 20 years of precision fabrication experience.',
        'add_h1': False
    },
    830: {  # Our Services
        'seo_title': 'Laser Cutting & Engraving Services | BoulderWorks - Boulder, CO',
        'seo_description': 'Professional laser cutting, engraving, wood burning, metal cutting, and custom fabrication services in Boulder, Colorado. Request a quote!',
        'add_h1': False,
        'fix_multiple_h1': True
    },
    952: {  # Laser Cutting
        'seo_title': 'Professional Laser Cutting Services in Boulder, CO | BoulderWorks',
        'seo_description': 'Expert laser cutting services in Boulder, Colorado. Precision cutting for metal, wood, acrylic, and more. Fast turnaround and competitive pricing.',
        'add_h1': False
    },
    1246: {  # Commercial Laser Cutting
        'seo_title': 'Commercial Laser Cutting Services in Boulder, CO | BoulderWorks',
        'seo_description': 'Commercial-grade laser cutting services in Boulder, Colorado. High-volume production, precision cutting, and fast turnaround times.',
        'add_h1': False
    },
    808: {  # Acrylic Cutting
        'seo_title': 'Precision Acrylic Cutting in Boulder, CO | BoulderWorks',
        'seo_description': 'Expert acrylic laser cutting services in Boulder, Colorado. Custom displays, signs, and precision parts. Fast quotes and turnaround.',
        'add_h1': False
    },
    795: {  # Metal Cutting
        'seo_title': 'Industrial Metal Cutting Services in Boulder, CO | BoulderWorks',
        'seo_description': 'Professional metal cutting services in Boulder, Colorado. Laser cutting for steel, aluminum, and more. Precision cuts for any project.',
        'add_h1': False
    },
    1751: {  # Signs & Signage
        'seo_title': 'Custom Signs & Signage in Boulder, CO | BoulderWorks',
        'seo_description': 'Custom business signs and signage in Boulder, Colorado. Laser cut and engraved signs for indoor and outdoor use. Get a free quote!',
        'add_h1': False
    },
    1773: {  # Custom Awards
        'seo_title': 'Custom Awards & Recognition Plaques in Boulder, CO | BoulderWorks',
        'seo_description': 'Custom awards, trophies, and recognition plaques in Boulder, Colorado. Laser engraved awards for corporate, sports, and special events.',
        'add_h1': False
    },
    786: {  # Gasket Cutting
        'seo_title': 'Custom Gasket Cutting Services in Boulder, CO | BoulderWorks',
        'seo_description': 'Precision gasket cutting services in Boulder, Colorado. Custom gaskets for industrial, automotive, and commercial applications.',
        'add_h1': False
    },
    1987: {  # Large Format Laser Cutting
        'seo_title': 'Large Format Laser Cutting in Boulder, CO | BoulderWorks',
        'seo_description': 'Large format laser cutting services in Boulder, Colorado. Cut oversized materials up to 60"x120". Perfect for architectural and industrial projects.',
        'add_h1': False
    },
    1972: {  # Large Format Laser Engraving
        'seo_title': 'Large Format Laser Engraving in Boulder, CO | BoulderWorks',
        'seo_description': 'Large format laser engraving services in Boulder, Colorado. Engrave oversized materials for signage, art, and industrial applications.',
        'add_h1': False
    },
    3006: {  # Multi Media Murals
        'seo_title': 'Multi-Media Murals & Custom Displays in Boulder, CO | BoulderWorks',
        'seo_description': 'Custom multi-media murals and artistic displays in Boulder, Colorado. Combine laser cutting, engraving, and mixed materials for unique art.',
        'add_h1': False
    },
    780: {  # Wood Burning
        'seo_title': 'Custom Wood Burning & Engraving in Boulder, CO | BoulderWorks',
        'seo_description': 'Professional wood burning and laser engraving services in Boulder, Colorado. Custom designs on wood for signs, art, and promotional items.',
        'add_h1': False
    },
    797: {  # Rubber Cutting
        'seo_title': 'Industrial Rubber Cutting Services in Boulder, CO | BoulderWorks',
        'seo_description': 'Precision rubber cutting services in Boulder, Colorado. Custom rubber gaskets, seals, and parts for industrial applications.',
        'add_h1': False
    },
    792: {  # Media Blasting
        'seo_title': 'Media Blasting Services (Sand/Garnet) in Boulder, CO | BoulderWorks',
        'seo_description': 'Professional media blasting services in Boulder, Colorado. Sand blasting, garnet blasting for surface preparation and finishing.',
        'add_h1': False
    },
    788: {  # Laser Marking/Etching
        'seo_title': 'Laser Marking & Etching Services in Boulder, CO | BoulderWorks',
        'seo_description': 'Precision laser marking and etching services in Boulder, Colorado. Permanent marking on metal, plastic, and other materials.',
        'add_h1': False
    }
}

def update_page_seo(site_url, api_key, page_id, seo_data):
    """Update SEO data for a single page"""
    try:
        # First get the current content
        response = requests.get(
            f"{site_url}/wp-json/wpbm/v1/content/{page_id}",
            headers={'X-API-Key': api_key},
            timeout=10
        )
        
        if response.status_code != 200:
            return {'success': False, 'error': f'Failed to get page: {response.status_code}'}
        
        page_data = response.json()
        content = page_data.get('content', '')
        
        # Handle multiple H1 tags if needed
        if seo_data.get('fix_multiple_h1'):
            # For the services page, keep only the second H1 "Our Services"
            content = content.replace('<h1>Browse</h1>', '<h2>Browse</h2>')
        
        # Update the page with new SEO data
        update_data = {
            'seo': {
                'title': seo_data['seo_title'],
                'description': seo_data['seo_description']
            }
        }
        
        # If content was modified, include it
        if seo_data.get('fix_multiple_h1'):
            update_data['content'] = content
        
        response = requests.put(
            f"{site_url}/wp-json/wpbm/v1/content/{page_id}",
            headers={'X-API-Key': api_key},
            json=update_data,
            timeout=30
        )
        
        if response.status_code == 200:
            return {'success': True, 'page_id': page_id}
        else:
            return {'success': False, 'error': f'Update failed: {response.status_code}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

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
    
    print("🔧 BoulderWorks SEO Fix Script")
    print("=" * 60)
    print(f"Site: {bw_site['url']}")
    print(f"Fixing SEO for {len(PRIORITY_FIXES)} priority pages\n")
    
    # Update pages concurrently
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_page = {
            executor.submit(update_page_seo, bw_site['url'], api_key, page_id, seo_data): page_id 
            for page_id, seo_data in PRIORITY_FIXES.items()
        }
        
        for future in as_completed(future_to_page):
            page_id = future_to_page[future]
            try:
                result = future.result()
                results.append((page_id, result))
                
                if result['success']:
                    print(f"✅ Updated page {page_id}: {PRIORITY_FIXES[page_id]['seo_title'][:50]}...")
                else:
                    print(f"❌ Failed page {page_id}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Error updating page {page_id}: {e}")
    
    # Summary
    successful = sum(1 for _, r in results if r['success'])
    print(f"\n📊 Summary: {successful}/{len(PRIORITY_FIXES)} pages updated successfully")
    
    if successful < len(PRIORITY_FIXES):
        print("\n⚠️ Some pages failed to update. Please check the errors above.")
    else:
        print("\n✅ All priority pages have been updated with proper SEO titles and descriptions!")
        print("\n📌 Next steps:")
        print("1. Review the updated pages on the live site")
        print("2. Submit updated sitemap to Google Search Console")
        print("3. Monitor search rankings for 'laser cutting Boulder CO' keywords")

if __name__ == "__main__":
    main()