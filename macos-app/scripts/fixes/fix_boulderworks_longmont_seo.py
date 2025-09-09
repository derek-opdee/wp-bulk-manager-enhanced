#!/usr/bin/env python3
"""Fix SEO issues for BoulderWorks pages - Update to Longmont, CO location"""

import json
import requests
from wpbm_manager import WPBulkManager
from concurrent.futures import ThreadPoolExecutor, as_completed

# Updated with Longmont, CO location
LONGMONT_SEO_FIXES = {
    4: {  # Home page
        'seo_title': 'Laser Cutting & Engraving Services in Longmont, Colorado | BoulderWorks',
        'seo_description': 'Professional laser cutting, engraving, and fabrication services in Longmont, CO. Custom awards, signs, metal cutting, and more. Get a quote today!'
    },
    6: {  # Contact
        'seo_title': 'Contact BoulderWorks | Laser Cutting Services in Longmont, CO',
        'seo_description': 'Contact BoulderWorks for laser cutting, engraving, and custom fabrication in Longmont, Colorado. Get a free quote for your project today!'
    },
    352: {  # About
        'seo_title': 'About BoulderWorks | Laser Cutting Experts in Longmont, CO', 
        'seo_description': 'Learn about BoulderWorks, Longmont Colorado\'s premier laser cutting and engraving company. Over 20 years of precision fabrication experience.'
    },
    830: {  # Our Services
        'seo_title': 'Laser Cutting & Engraving Services | BoulderWorks - Longmont, CO',
        'seo_description': 'Professional laser cutting, engraving, wood burning, metal cutting, and custom fabrication services in Longmont, Colorado. Request a quote!'
    },
    952: {  # Laser Cutting
        'seo_title': 'Professional Laser Cutting Services in Longmont, CO | BoulderWorks',
        'seo_description': 'Expert laser cutting services in Longmont, Colorado. Precision cutting for metal, wood, acrylic, and more. Fast turnaround and competitive pricing.'
    },
    1246: {  # Commercial Laser Cutting
        'seo_title': 'Commercial Laser Cutting Services in Longmont, CO | BoulderWorks',
        'seo_description': 'Commercial-grade laser cutting services in Longmont, Colorado. High-volume production, precision cutting, and fast turnaround times.'
    },
    808: {  # Acrylic Cutting
        'seo_title': 'Precision Acrylic Cutting in Longmont, CO | BoulderWorks',
        'seo_description': 'Expert acrylic laser cutting services in Longmont, Colorado. Custom displays, signs, and precision parts. Fast quotes and turnaround.'
    },
    795: {  # Metal Cutting
        'seo_title': 'Industrial Metal Cutting Services in Longmont, CO | BoulderWorks',
        'seo_description': 'Professional metal cutting services in Longmont, Colorado. Laser cutting for steel, aluminum, and more. Precision cuts for any project.'
    },
    1751: {  # Signs & Signage
        'seo_title': 'Custom Signs & Signage in Longmont, CO | BoulderWorks',
        'seo_description': 'Custom business signs and signage in Longmont, Colorado. Laser cut and engraved signs for indoor and outdoor use. Get a free quote!'
    },
    1773: {  # Custom Awards
        'seo_title': 'Custom Awards & Recognition Plaques in Longmont, CO | BoulderWorks',
        'seo_description': 'Custom awards, trophies, and recognition plaques in Longmont, Colorado. Laser engraved awards for corporate, sports, and special events.'
    },
    786: {  # Gasket Cutting
        'seo_title': 'Custom Gasket Cutting Services in Longmont, CO | BoulderWorks',
        'seo_description': 'Precision gasket cutting services in Longmont, Colorado. Custom gaskets for industrial, automotive, and commercial applications.'
    },
    1987: {  # Large Format Laser Cutting
        'seo_title': 'Large Format Laser Cutting in Longmont, CO | BoulderWorks',
        'seo_description': 'Large format laser cutting services in Longmont, Colorado. Cut oversized materials up to 60"x120". Perfect for architectural and industrial projects.'
    },
    1972: {  # Large Format Laser Engraving
        'seo_title': 'Large Format Laser Engraving in Longmont, CO | BoulderWorks',
        'seo_description': 'Large format laser engraving services in Longmont, Colorado. Engrave oversized materials for signage, art, and industrial applications.'
    },
    3006: {  # Multi Media Murals
        'seo_title': 'Multi-Media Murals & Custom Displays in Longmont, CO | BoulderWorks',
        'seo_description': 'Custom multi-media murals and artistic displays in Longmont, Colorado. Combine laser cutting, engraving, and mixed materials for unique art.'
    },
    780: {  # Wood Burning
        'seo_title': 'Custom Wood Burning & Engraving in Longmont, CO | BoulderWorks',
        'seo_description': 'Professional wood burning and laser engraving services in Longmont, Colorado. Custom designs on wood for signs, art, and promotional items.'
    },
    797: {  # Rubber Cutting
        'seo_title': 'Industrial Rubber Cutting Services in Longmont, CO | BoulderWorks',
        'seo_description': 'Precision rubber cutting services in Longmont, Colorado. Custom rubber gaskets, seals, and parts for industrial applications.'
    },
    792: {  # Media Blasting
        'seo_title': 'Media Blasting Services (Sand/Garnet) in Longmont, CO | BoulderWorks',
        'seo_description': 'Professional media blasting services in Longmont, Colorado. Sand blasting, garnet blasting for surface preparation and finishing.'
    },
    788: {  # Laser Marking/Etching
        'seo_title': 'Laser Marking & Etching Services in Longmont, CO | BoulderWorks',
        'seo_description': 'Precision laser marking and etching services in Longmont, Colorado. Permanent marking on metal, plastic, and other materials.'
    },
    603: {  # FAQ
        'seo_title': 'Frequently Asked Questions | BoulderWorks - Longmont, CO',
        'seo_description': 'Common questions about laser cutting, engraving, and fabrication services at BoulderWorks in Longmont, Colorado. Get answers here!'
    },
    5: {  # Blog
        'seo_title': 'Laser Cutting & Fabrication Blog | BoulderWorks - Longmont, CO',
        'seo_description': 'Tips, news, and insights about laser cutting, engraving, and custom fabrication from BoulderWorks in Longmont, Colorado.'
    },
    1214: {  # Thank You
        'seo_title': 'Thank You | BoulderWorks - Longmont, CO',
        'seo_description': 'Thank you for contacting BoulderWorks in Longmont, Colorado. We\'ll respond to your laser cutting or engraving inquiry shortly.'
    },
    3127: {  # Project Gallery
        'seo_title': 'Project Gallery | BoulderWorks Laser Services - Longmont, CO',
        'seo_description': 'View our portfolio of laser cutting, engraving, and custom fabrication projects completed by BoulderWorks in Longmont, Colorado.'
    }
}

def update_page_seo(site_url, api_key, page_id, seo_data):
    """Update SEO data for a single page"""
    try:
        update_data = {
            'seo': {
                'title': seo_data['seo_title'],
                'description': seo_data['seo_description']
            }
        }
        
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
    
    print("🔧 BoulderWorks SEO Location Update - Longmont, CO")
    print("=" * 60)
    print(f"Site: {bw_site['url']}")
    print(f"Updating SEO for {len(LONGMONT_SEO_FIXES)} pages to Longmont, CO\n")
    
    # Update pages concurrently
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_page = {
            executor.submit(update_page_seo, bw_site['url'], api_key, page_id, seo_data): page_id 
            for page_id, seo_data in LONGMONT_SEO_FIXES.items()
        }
        
        for future in as_completed(future_to_page):
            page_id = future_to_page[future]
            try:
                result = future.result()
                results.append((page_id, result))
                
                if result['success']:
                    print(f"✅ Updated page {page_id}: {LONGMONT_SEO_FIXES[page_id]['seo_title'][:50]}...")
                else:
                    print(f"❌ Failed page {page_id}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Error updating page {page_id}: {e}")
    
    # Summary
    successful = sum(1 for _, r in results if r['success'])
    print(f"\n📊 Summary: {successful}/{len(LONGMONT_SEO_FIXES)} pages updated successfully")
    
    if successful == len(LONGMONT_SEO_FIXES):
        print("\n✅ All pages have been updated with Longmont, CO location!")
        print("\n📌 Location Update Complete:")
        print("• Changed from 'Boulder, CO' to 'Longmont, CO' in all titles")
        print("• Updated meta descriptions to reflect Longmont location")
        print("• Added SEO to previously missing pages (FAQ, Blog, Thank You, Gallery)")
        print("\n🎯 SEO Benefits:")
        print("• Better local search rankings for 'laser cutting Longmont'")
        print("• Accurate location for Google My Business alignment")
        print("• Serves nearby areas: Boulder, Fort Collins, Denver")

if __name__ == "__main__":
    main()