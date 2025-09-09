#!/usr/bin/env python3
"""
Fix duplicate H1s and update SEO for derekzar.com
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm.api.client import WPBMClient
from wpbm.api.auth import APIKeyManager
from wpbm.utils.logger import get_logger
import json

logger = get_logger(__name__)

# Site configuration
SITE_URL = "https://derekzar.com"
SITE_NAME = "derekzar"

# Initialize API key manager
auth_manager = APIKeyManager()

# Try to get existing API key or prompt for new one
site_info = auth_manager.get_site(SITE_NAME)
if site_info and 'api_key' in site_info:
    api_key = site_info['api_key']
else:
    api_key = input(f"Enter API key for {SITE_URL}: ").strip()
    auth_manager.add_site(SITE_NAME, SITE_URL, api_key)

# Initialize client
client = WPBMClient(SITE_URL, api_key)

# Test connection
print(f"\nConnecting to {SITE_URL}...")
test_result = client.test_connection()
if test_result.get('success'):
    print("✅ Connection successful!")
else:
    print(f"❌ Connection failed: {test_result.get('message')}")
    sys.exit(1)

# Get all pages
print("\nFetching all pages...")
pages = client.get_pages(per_page=100)
print(f"Found {len(pages)} pages")

# Analyze pages for duplicate H1s
pages_with_issues = []
for page in pages:
    page_id = page['id']
    title = page.get('title', {}).get('rendered', '')
    
    # Get full page content
    full_page = client.get_page(page_id)
    content = full_page.get('content', {}).get('rendered', '')
    
    # Count H1 tags
    h1_count = content.lower().count('<h1')
    
    if h1_count > 1:
        # Extract H1 texts
        import re
        h1_pattern = r'<h1[^>]*>(.*?)</h1>'
        h1_matches = re.findall(h1_pattern, content, re.IGNORECASE | re.DOTALL)
        h1_texts = [re.sub(r'<[^>]+>', '', match).strip() for match in h1_matches]
        
        pages_with_issues.append({
            'id': page_id,
            'title': title,
            'url': page.get('link', ''),
            'h1_count': h1_count,
            'h1_texts': h1_texts,
            'content': content
        })

print(f"\nFound {len(pages_with_issues)} pages with duplicate H1s:")
for page in pages_with_issues:
    print(f"\n- Page {page['id']}: {page['title']}")
    print(f"  URL: {page['url']}")
    print(f"  H1 tags ({page['h1_count']}):")
    for i, h1 in enumerate(page['h1_texts'], 1):
        print(f"    {i}. {h1}")

# Fix duplicate H1s
if pages_with_issues:
    fix_h1s = input("\nFix duplicate H1s? (y/n): ").strip().lower()
    if fix_h1s == 'y':
        for page in pages_with_issues:
            print(f"\nFixing page {page['id']}: {page['title']}")
            
            # Show H1 options
            print("Choose which H1 to keep (others will become H2):")
            for i, h1 in enumerate(page['h1_texts'], 1):
                print(f"  {i}. {h1}")
            
            keep_index = int(input("Keep H1 number (1-{}): ".format(len(page['h1_texts']))).strip()) - 1
            
            # Update content
            content = page['content']
            h1_pattern = r'<h1([^>]*)>(.*?)</h1>'
            
            # Replace H1s with H2s except the one to keep
            h1_matches = list(re.finditer(h1_pattern, content, re.IGNORECASE | re.DOTALL))
            
            for i, match in enumerate(h1_matches):
                if i != keep_index:
                    # Replace this H1 with H2
                    old_tag = match.group(0)
                    new_tag = old_tag.replace('<h1', '<h2').replace('</h1>', '</h2>')
                    content = content.replace(old_tag, new_tag)
            
            # Update the page
            update_data = {
                'content': content
            }
            
            result = client.update_page(page['id'], update_data)
            if result:
                print(f"✅ Fixed H1s for page {page['id']}")
            else:
                print(f"❌ Failed to update page {page['id']}")

# Update SEO for all pages
print("\n\nUpdating SEO titles and descriptions for all pages...")

# SEO templates following brand guidelines
seo_templates = {
    'home': {
        'title': 'Derek Zar | AI Innovation Strategist Melbourne',
        'description': 'AI systems that work for your business. Expert guidance from experienced AI Innovation Strategist and Consultant specialising in practical implementation.'
    },
    'ai-consulting': {
        'title': 'AI Innovation Services | Derek Zar Melbourne',
        'description': 'Strategic AI innovation consulting for Melbourne businesses. From automation to machine learning, get expert guidance on implementing AI systems.'
    },
    'services': {
        'title': 'AI Innovation & Technology Services | Derek Zar',
        'description': 'Complete AI innovation and technology services for modern businesses. Strategy, implementation, and ongoing support from Melbourne experts.'
    },
    'about': {
        'title': 'About Derek Zar | AI Innovation Strategist Melbourne',
        'description': 'Meet Derek Zar, AI Innovation Strategist and Consultant helping Melbourne businesses implement practical AI systems. Experience in enterprise technology.'
    },
    'contact': {
        'title': 'Contact Derek Zar | AI Innovation Strategist',
        'description': 'Get in touch with Derek Zar for AI innovation consulting services in Melbourne. Book a consultation to discuss your business technology needs.'
    }
}

# Process all pages for SEO updates
for page in pages:
    page_id = page['id']
    title = page.get('title', {}).get('rendered', '')
    slug = page.get('slug', '')
    
    print(f"\nProcessing page {page_id}: {title}")
    print(f"  Slug: {slug}")
    
    # Get current SEO data
    yoast_meta = page.get('yoast_meta', {})
    current_title = yoast_meta.get('yoast_wpseo_title', '')
    current_desc = yoast_meta.get('yoast_wpseo_metadesc', '')
    
    print(f"  Current SEO Title: {current_title}")
    print(f"  Current SEO Desc: {current_desc}")
    
    # Get template or create custom
    if slug in seo_templates:
        new_title = seo_templates[slug]['title']
        new_desc = seo_templates[slug]['description']
        print(f"  Using template for '{slug}'")
    else:
        # Generate custom SEO based on page title
        page_title_clean = re.sub(r'<[^>]+>', '', title).strip()
        new_title = f"{page_title_clean} | Derek Zar Melbourne"
        new_desc = f"{page_title_clean} services from Derek Zar, AI Innovation Strategist and Consultant in Melbourne. Expert guidance for practical business implementation."
        
        # Ensure title is 30-60 chars
        if len(new_title) > 60:
            new_title = f"{page_title_clean[:40]}... | Derek Zar"
        
        # Ensure description is 120-160 chars
        if len(new_desc) > 160:
            new_desc = new_desc[:157] + "..."
    
    print(f"  New SEO Title ({len(new_title)} chars): {new_title}")
    print(f"  New SEO Desc ({len(new_desc)} chars): {new_desc}")
    
    # Update SEO meta
    update_data = {
        'meta': {
            'yoast_wpseo_title': new_title,
            'yoast_wpseo_metadesc': new_desc
        }
    }
    
    update_seo = input(f"Update SEO for this page? (y/n/skip all): ").strip().lower()
    if update_seo == 'skip all':
        break
    elif update_seo == 'y':
        result = client.update_page(page_id, update_data)
        if result:
            print(f"✅ Updated SEO for page {page_id}")
        else:
            print(f"❌ Failed to update SEO for page {page_id}")

print("\n\n✅ SEO update process complete!")