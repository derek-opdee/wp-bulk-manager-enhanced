#!/usr/bin/env python3
"""
Manual fix instructions for derekzar.com
Since the H1 changes aren't persisting through the API (likely due to page builder interference),
this provides comprehensive manual instructions.
"""

import sys
sys.path.append('.')
from wpbm.api.client import WPBMClient

def main():
    client = WPBMClient('https://derekzar.com', '0b2d82ec91d2d876558ce460e57a7a1e')
    
    print("🇦🇺 DEREK ZAR WEBSITE - MANUAL FIXES REQUIRED")
    print("=" * 60)
    print("The API updates aren't persisting, likely due to page builder cache.")
    print("Please make these changes manually in WordPress admin:\n")
    
    # Get all pages for complete instructions
    pages = client.get_content('page', status='publish')
    
    # H1 fixes needed
    h1_fixes = {
        2196: {
            'title': 'Speaking & Workshops',
            'h1_change': 'Change "Global AI Thought Leadership" from H1 to H2'
        },
        2194: {
            'title': 'AI Training & Enablement', 
            'h1_change': 'Change "Comprehensive AI Education" from H1 to H2'
        },
        2192: {
            'title': 'AI Cloud Architecture',
            'h1_change': 'Change "Enterprise-Grade AI Infrastructure" from H1 to H2'
        },
        2188: {
            'title': 'Agentic AI Development',
            'h1_change': 'Change "Next-Generation AI Architecture" from H1 to H2'
        },
        2183: {
            'title': 'Fractional AI Executive',
            'h1_change': 'Change "Executive AI Leadership" from H1 to H2'
        },
        2177: {
            'title': 'AI Strategy & Transformation',
            'h1_change': 'Change "Strategic Leadership for the AI Era" from H1 to H2'
        }
    }
    
    # SEO updates for all pages
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
    
    print("🔧 STEP 1: FIX DUPLICATE H1 TAGS")
    print("=" * 40)
    print("These pages have duplicate H1 tags. Keep the first H1, change the second to H2:\n")
    
    for page_id, fix_info in h1_fixes.items():
        print(f"📄 Page ID {page_id}: {fix_info['title']}")
        print(f"   Edit URL: https://derekzar.com/wp-admin/post.php?post={page_id}&action=edit")
        print(f"   Action: {fix_info['h1_change']}")
        print(f"   Note: Look for heading blocks in the page builder and change the second H1 to H2")
        print()
    
    print("\n📝 STEP 2: UPDATE SEO TITLES & DESCRIPTIONS")
    print("=" * 50)
    print("Update these SEO fields using Yoast SEO or your SEO plugin:\n")
    
    # Get page data for slugs
    page_lookup = {p.get('id'): p for p in pages}
    
    for page_id, seo_data in seo_updates.items():
        if page_id in page_lookup:
            page = page_lookup[page_id]
            slug = page.get('slug', '')
            title = page.get('title', '')
            
            print(f"📄 Page ID {page_id}: {title}")
            print(f"   Edit URL: https://derekzar.com/wp-admin/post.php?post={page_id}&action=edit")
            print(f"   Live URL: https://derekzar.com/{slug}/")
            print(f"   SEO Title ({len(seo_data['title'])} chars): {seo_data['title']}")
            print(f"   SEO Description ({len(seo_data['description'])} chars): {seo_data['description']}")
            print()
    
    print("✅ VERIFICATION CHECKLIST")
    print("=" * 30)
    print("After making changes, verify:")
    print("• Each page has only ONE H1 tag")
    print("• All SEO titles are 30-60 characters")
    print("• All SEO descriptions are 120-160 characters") 
    print("• Australian English spelling is used throughout")
    print("• 'Derek Zar' brand appears in all SEO titles")
    print("• Melbourne location mentioned where relevant")
    print("• No 'transform', 'elevate', or 'solutions' words used")
    print("• Professional, friendly tone maintained")
    
    print("\n🔍 QUICK ACCESS LINKS")
    print("=" * 25)
    print("WordPress Admin: https://derekzar.com/wp-admin/")
    print("Pages List: https://derekzar.com/wp-admin/edit.php?post_type=page")
    print("SEO Overview: https://derekzar.com/wp-admin/admin.php?page=wpseo_dashboard")
    
    print(f"\n🎯 SUMMARY: {len(h1_fixes)} pages need H1 fixes, {len(seo_updates)} pages need SEO updates")

if __name__ == "__main__":
    main()