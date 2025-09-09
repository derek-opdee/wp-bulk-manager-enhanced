#!/usr/bin/env python3
"""
Automated fix for duplicate H1s and SEO updates on derekzar.com
"""
import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm.api.client import WPBMClient
from wpbm.api.auth import APIKeyManager
from wpbm.utils.logger import get_logger

logger = get_logger(__name__)

# Site configuration
SITE_URL = "https://derekzar.com"
SITE_NAME = "derekzar"

# Initialize API key manager
auth_manager = APIKeyManager()

# Try to get existing API key
site_info = auth_manager.get_site(SITE_NAME)
if not site_info or 'api_key' not in site_info:
    print(f"No API key found for {SITE_NAME}. Please add it first.")
    api_key = input(f"Enter API key for {SITE_URL}: ").strip()
    auth_manager.add_site(SITE_NAME, SITE_URL, api_key)
    site_info = auth_manager.get_site(SITE_NAME)

api_key = site_info['api_key']

# Initialize client
client = WPBMClient(SITE_URL, api_key)

# Test connection
print(f"\nConnecting to {SITE_URL}...")
test_result = client.test_connection()
if not test_result.get('success'):
    print(f"❌ Connection failed: {test_result.get('message')}")
    sys.exit(1)

print("✅ Connection successful!")

# Get all pages
print("\nFetching all pages...")
pages = client.get_pages(per_page=100)
print(f"Found {len(pages)} pages")

# SEO templates following brand guidelines (Australian English, no dashes, lean style)
seo_data = {
    # Home page
    'home': {
        'title': 'Derek Zar | AI Strategy Consultant Melbourne',
        'description': 'AI systems that work for your business. Expert guidance from experienced consultants specialising in practical AI implementation.'
    },
    # About page
    'about': {
        'title': 'About Derek Zar | AI Consultant Melbourne',
        'description': 'Meet Derek Zar, AI strategy consultant helping Melbourne businesses implement practical AI systems. Experience in enterprise technology.'
    },
    'about-derek-zar': {
        'title': 'About Derek Zar | AI Consultant Melbourne',
        'description': 'Meet Derek Zar, AI strategy consultant helping Melbourne businesses implement practical AI systems. Experience in enterprise technology.'
    },
    # Services pages
    'services': {
        'title': 'AI & Technology Services | Derek Zar',
        'description': 'Complete AI and technology services for modern businesses. Strategy, implementation, and ongoing support from Melbourne experts.'
    },
    'ai-consulting': {
        'title': 'AI Consulting Services | Derek Zar Melbourne',
        'description': 'Strategic AI consulting for Melbourne businesses. From automation to machine learning, get expert guidance on implementing AI systems.'
    },
    'ai-strategy': {
        'title': 'AI Strategy Consulting | Derek Zar Melbourne',
        'description': 'Develop your AI strategy with expert consultants. Practical roadmaps for implementing artificial intelligence in Melbourne businesses.'
    },
    'automation': {
        'title': 'Business Automation Services | Derek Zar',
        'description': 'Automate your business processes with AI and modern technology. Melbourne consultants specialising in workflow optimisation.'
    },
    'data-analytics': {
        'title': 'Data Analytics Services | Derek Zar Melbourne',
        'description': 'Turn your data into insights with expert analytics services. Melbourne consultants helping businesses make data driven decisions.'
    },
    # Contact
    'contact': {
        'title': 'Contact Derek Zar | AI Consultant Melbourne',
        'description': 'Get in touch with Derek Zar for AI consulting services in Melbourne. Book a consultation to discuss your business technology needs.'
    },
    # Blog/Insights
    'blog': {
        'title': 'AI Insights & Articles | Derek Zar',
        'description': 'Latest insights on AI, automation, and business technology. Expert perspectives from Melbourne AI consultant Derek Zar.'
    },
    'insights': {
        'title': 'Technology Insights | Derek Zar Melbourne',
        'description': 'Expert insights on AI and technology for business. Stay informed with articles from Melbourne consultant Derek Zar.'
    },
    # Case studies
    'case-studies': {
        'title': 'AI Implementation Case Studies | Derek Zar',
        'description': 'Real world AI implementation success stories. See how Melbourne businesses have benefited from strategic AI consulting.'
    },
    'portfolio': {
        'title': 'AI Project Portfolio | Derek Zar Melbourne',
        'description': 'Successful AI projects and implementations. See how Derek Zar helps Melbourne businesses leverage artificial intelligence.'
    }
}

# Process each page
duplicate_h1_pages = []
seo_updates = []

for page in pages:
    page_id = page['id']
    title = page.get('title', {}).get('rendered', '')
    slug = page.get('slug', '')
    link = page.get('link', '')
    
    print(f"\n{'='*60}")
    print(f"Processing page {page_id}: {title}")
    print(f"Slug: {slug}")
    print(f"URL: {link}")
    
    # Get full page content
    full_page = client.get_page(page_id)
    content = full_page.get('content', {}).get('rendered', '')
    
    # Check for duplicate H1s
    h1_pattern = r'<h1[^>]*>(.*?)</h1>'
    h1_matches = re.findall(h1_pattern, content, re.IGNORECASE | re.DOTALL)
    h1_texts = [re.sub(r'<[^>]+>', '', match).strip() for match in h1_matches]
    
    if len(h1_texts) > 1:
        print(f"⚠️  Found {len(h1_texts)} H1 tags:")
        for i, h1 in enumerate(h1_texts, 1):
            print(f"   {i}. {h1}")
        
        # Determine which H1 to keep (usually the more descriptive one)
        # Keep the longer, more descriptive H1
        keep_index = 0
        max_length = 0
        for i, h1 in enumerate(h1_texts):
            # Prefer H1s without generic terms
            if len(h1) > max_length and not any(word in h1.lower() for word in ['welcome', 'hello']):
                max_length = len(h1)
                keep_index = i
        
        print(f"   → Keeping H1 #{keep_index + 1}: {h1_texts[keep_index]}")
        
        # Fix the content
        new_content = content
        h1_full_pattern = r'<h1([^>]*)>(.*?)</h1>'
        h1_full_matches = list(re.finditer(h1_full_pattern, content, re.IGNORECASE | re.DOTALL))
        
        for i, match in enumerate(h1_full_matches):
            if i != keep_index:
                old_tag = match.group(0)
                new_tag = old_tag.replace('<h1', '<h2').replace('</h1>', '</h2>')
                new_content = new_content.replace(old_tag, new_tag)
                print(f"   → Converting to H2: {h1_texts[i]}")
        
        duplicate_h1_pages.append({
            'id': page_id,
            'title': title,
            'new_content': new_content
        })
    
    # Prepare SEO updates
    yoast_meta = page.get('yoast_meta', {})
    current_seo_title = yoast_meta.get('yoast_wpseo_title', '')
    current_seo_desc = yoast_meta.get('yoast_wpseo_metadesc', '')
    
    print(f"\nCurrent SEO:")
    print(f"  Title: {current_seo_title}")
    print(f"  Desc: {current_seo_desc}")
    
    # Get new SEO data
    if slug in seo_data:
        new_seo_title = seo_data[slug]['title']
        new_seo_desc = seo_data[slug]['description']
    else:
        # Generate based on page title
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        
        # Remove common suffixes
        clean_title = re.sub(r'\s*[-–—]\s*Derek Zar.*$', '', clean_title)
        clean_title = re.sub(r'\s*\|.*$', '', clean_title)
        
        new_seo_title = f"{clean_title} | Derek Zar Melbourne"
        new_seo_desc = f"{clean_title} services from Derek Zar, AI consultant in Melbourne. Expert guidance for practical business implementation."
        
        # Ensure proper length
        if len(new_seo_title) > 60:
            new_seo_title = f"{clean_title[:45]} | Derek Zar"
        
        if len(new_seo_desc) > 160:
            new_seo_desc = f"{clean_title} from Derek Zar, Melbourne AI consultant. Practical implementation and expert guidance for your business."
            if len(new_seo_desc) > 160:
                new_seo_desc = new_seo_desc[:157] + "..."
    
    print(f"\nNew SEO:")
    print(f"  Title ({len(new_seo_title)} chars): {new_seo_title}")
    print(f"  Desc ({len(new_seo_desc)} chars): {new_seo_desc}")
    
    # Check if update needed
    if current_seo_title != new_seo_title or current_seo_desc != new_seo_desc:
        seo_updates.append({
            'id': page_id,
            'title': title,
            'seo_title': new_seo_title,
            'seo_desc': new_seo_desc
        })

# Apply fixes
print(f"\n\n{'='*60}")
print("SUMMARY:")
print(f"- Pages with duplicate H1s: {len(duplicate_h1_pages)}")
print(f"- Pages needing SEO updates: {len(seo_updates)}")

if duplicate_h1_pages or seo_updates:
    print("\nApplying fixes...")
    
    # Fix duplicate H1s
    for page_data in duplicate_h1_pages:
        print(f"\nFixing H1s on page {page_data['id']}: {page_data['title']}")
        update_data = {
            'content': page_data['new_content']
        }
        result = client.update_page(page_data['id'], update_data)
        if result:
            print("✅ H1s fixed")
        else:
            print("❌ Failed to fix H1s")
    
    # Update SEO
    for seo_data in seo_updates:
        print(f"\nUpdating SEO for page {seo_data['id']}: {seo_data['title']}")
        update_data = {
            'meta': {
                'yoast_wpseo_title': seo_data['seo_title'],
                'yoast_wpseo_metadesc': seo_data['seo_desc']
            }
        }
        result = client.update_page(seo_data['id'], update_data)
        if result:
            print("✅ SEO updated")
        else:
            print("❌ Failed to update SEO")

print(f"\n\n{'='*60}")
print("✅ All updates complete!")
print(f"- Fixed {len(duplicate_h1_pages)} pages with duplicate H1s")
print(f"- Updated SEO on {len(seo_updates)} pages")
print("\nBrand guidelines applied:")
print("- Australian English spelling (organise, specialise, optimise)")
print("- No em dashes or en dashes")
print("- Lean, professional tone without excessive adjectives")
print("- Location: Melbourne")
print("- Avoided words: transform, elevate, solutions")