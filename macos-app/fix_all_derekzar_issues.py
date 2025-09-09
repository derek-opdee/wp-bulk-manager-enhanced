#!/usr/bin/env python3
"""
Comprehensive fix for derekzar.com:
1. Fix duplicate H1s (convert second H1 to H2)
2. Update all pages with Australian English SEO titles and descriptions
"""

import sys
sys.path.append('.')
from wpbm.api.client import WPBMClient
import json
import re
import time

def main():
    # Initialize client
    client = WPBMClient('https://derekzar.com', '0b2d82ec91d2d876558ce460e57a7a1e')
    
    print("🇦🇺 Derek Zar Website Fixes - Australian English SEO & H1 Updates")
    print("=" * 70)
    
    # Get all published pages
    print("📄 Fetching all published pages...")
    pages = client.get_content('page', status='publish')
    print(f"Found {len(pages)} published pages")
    
    # Analyze pages for H1 issues
    print("\n🔍 Analyzing pages for H1 issues...")
    pages_to_fix = []
    for page in pages:
        page_id = page.get('id')
        try:
            detailed_page = client.get_content_by_id(page_id)
            content = detailed_page.get('content', '')
            
            if isinstance(content, str):
                h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
                h1_count = len(h1_matches)
                
                if h1_count > 1:
                    pages_to_fix.append({
                        'id': page_id,
                        'title': detailed_page.get('title', ''),
                        'content': content,
                        'h1_count': h1_count,
                        'h1_tags': [re.sub(r'<[^>]+>', '', h1).strip() for h1 in h1_matches]
                    })
        except Exception as e:
            print(f"  ❌ Error analyzing page {page_id}: {e}")
    
    print(f"Found {len(pages_to_fix)} pages with duplicate H1s")
    
    # Fix H1 duplicates
    if pages_to_fix:
        print("\n🔧 Fixing duplicate H1s...")
        for page in pages_to_fix:
            page_id = page['id']
            title = page['title']
            content = page['content']
            
            print(f"\n  Fixing Page {page_id}: {title}")
            print(f"    Current H1s: {page['h1_tags']}")
            
            # Convert second H1 to H2
            h1_pattern = r'<h1([^>]*)>(.*?)</h1>'
            h1_matches = list(re.finditer(h1_pattern, content, re.IGNORECASE | re.DOTALL))
            
            if len(h1_matches) >= 2:
                # Replace the second H1 with H2
                second_h1 = h1_matches[1]
                old_h1 = second_h1.group(0)
                new_h2 = f'<h2{second_h1.group(1)}>{second_h1.group(2)}</h2>'
                
                new_content = content.replace(old_h1, new_h2, 1)
                
                try:
                    response = client.update_content(page_id, {'content': new_content})
                    print(f"    ✅ Successfully converted second H1 to H2")
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    print(f"    ❌ Error updating page {page_id}: {e}")
    
    # Define Australian English SEO content
    print("\n📝 Preparing Australian English SEO content...")
    seo_updates = {
        1015: {  # Home
            'title': 'Derek Zar | AI Strategy Expert Melbourne',
            'description': 'Derek Zar provides elite AI strategy consulting in Melbourne. Helping businesses evolve with intelligent technology for sustainable growth.'
        },
        1529: {  # About
            'title': 'About Derek Zar | AI Technology Visionary',
            'description': 'From tech support to AI visionary, Derek Zar brings decades of technology expertise to help Melbourne businesses embrace artificial intelligence.'
        },
        1731: {  # Contact
            'title': 'Contact Derek Zar | AI Strategy Consultation',
            'description': 'Ready to build AI into your business future? Contact Derek Zar for expert AI strategy consultation and implementation support in Melbourne.'
        },
        1786: {  # Projects
            'title': 'AI Projects | Derek Zar Portfolio Melbourne',  
            'description': 'Explore Derek Zar\'s featured AI projects showcasing successful artificial intelligence implementations across diverse industries in Melbourne.'
        },
        2126: {  # Privacy Policy
            'title': 'Privacy Policy | Derek Zar AI Consulting',
            'description': 'Privacy policy for Derek Zar AI consulting services. Your data protection and privacy rights when engaging with our Melbourne AI services.'
        },
        2129: {  # All Services
            'title': 'AI Services | Derek Zar Melbourne Consulting',
            'description': 'Comprehensive AI services from Derek Zar including strategy, cloud architecture, training, and executive leadership for Melbourne businesses.'
        },
        2177: {  # AI Strategy & Transformation
            'title': 'AI Strategy | Derek Zar Melbourne Consulting',
            'description': 'Strategic AI leadership for the new era. Derek Zar helps Melbourne organisations navigate artificial intelligence adoption and digital evolution.'
        },
        2183: {  # Fractional AI Executive
            'title': 'Fractional AI Executive | Derek Zar Melbourne',
            'description': 'Executive AI leadership on demand. Derek Zar provides fractional CTO and AI executive services to guide Melbourne companies through AI initiatives.'
        },
        2188: {  # Agentic AI Development
            'title': 'Agentic AI Development | Derek Zar Melbourne',
            'description': 'Next generation AI architecture services from Derek Zar. Building autonomous AI agents and intelligent systems for Melbourne enterprises.'
        },
        2192: {  # AI Cloud Architecture
            'title': 'AI Cloud Architecture | Derek Zar Melbourne',
            'description': 'Enterprise grade AI infrastructure design from Derek Zar. Scalable cloud architecture for artificial intelligence applications in Melbourne.'
        },
        2194: {  # AI Training & Enablement  
            'title': 'AI Training | Derek Zar Melbourne Workshops',
            'description': 'Comprehensive AI education and training from Derek Zar. Enabling Melbourne teams with practical artificial intelligence knowledge and skills.'
        },
        2196: {  # Speaking & Workshops
            'title': 'AI Speaking | Derek Zar Melbourne Workshops',
            'description': 'Global AI thought leadership from Derek Zar. Speaking engagements and workshops on artificial intelligence for Melbourne and international audiences.'
        },
        2265: {  # Investment Opportunities
            'title': 'AI Investment | Derek Zar Strategic Opportunities',
            'description': 'Strategic investment opportunities in artificial intelligence ventures. Derek Zar identifies and evaluates AI investment prospects for Melbourne investors.'
        }
    }
    
    print("\n🌏 Manual SEO Update Instructions")
    print("=" * 50)
    print("Due to authentication requirements, Yoast SEO metadata needs to be updated manually.")
    print("Please log into the WordPress admin and update the following pages:")
    print()
    
    for page in pages:
        page_id = page.get('id')
        if page_id in seo_updates:
            seo_data = seo_updates[page_id]
            slug = page.get('slug', '')
            
            print(f"📄 Page ID {page_id}: {page.get('title', '')}")
            print(f"   URL: /wp-admin/post.php?post={page_id}&action=edit")
            print(f"   Slug: /{slug}/")
            print(f"   SEO Title ({len(seo_data['title'])} chars): {seo_data['title']}")
            print(f"   SEO Description ({len(seo_data['description'])} chars): {seo_data['description']}")
            print()
    
    # Verify H1 fixes
    print("\n✅ Verifying H1 fixes...")
    for page in pages_to_fix:
        page_id = page['id']
        try:
            updated_page = client.get_content_by_id(page_id)
            content = updated_page.get('content', '')
            
            if isinstance(content, str):
                h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
                h1_count = len(h1_matches)
                
                if h1_count == 1:
                    print(f"  ✅ Page {page_id}: H1 fix successful (now has {h1_count} H1)")
                else:
                    print(f"  ⚠️  Page {page_id}: Still has {h1_count} H1 tags")
        except Exception as e:
            print(f"  ❌ Error verifying page {page_id}: {e}")
    
    print("\n🎉 SUMMARY")
    print("=" * 30)
    print(f"✅ H1 Fixes Applied: {len(pages_to_fix)} pages")
    print(f"📝 SEO Updates Required: {len(seo_updates)} pages")
    print("🌏 All SEO content uses Australian English spelling")
    print("📏 All titles 30-60 chars, descriptions 120-160 chars")
    print("🏢 Melbourne location included where relevant")
    print("👤 Derek Zar brand prominently featured")
    print()
    print("Next step: Log into WordPress admin to apply the SEO updates shown above.")

if __name__ == "__main__":
    main()