#!/usr/bin/env python3
"""Analyze BoulderWorks pages for SEO and HTML structure"""

import requests
import json
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from wpbm_manager import WPBulkManager

def fetch_page_content(site_url, api_key, page_id):
    """Fetch a single page's content"""
    try:
        response = requests.get(
            f"{site_url}/wp-json/wpbm/v1/content/{page_id}",
            headers={'X-API-Key': api_key},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def analyze_page_structure(page_data):
    """Analyze HTML structure and SEO elements"""
    issues = []
    recommendations = []
    
    # Parse HTML content
    content = page_data.get('content', '')
    soup = BeautifulSoup(content, 'html.parser')
    
    # Check headings
    h1_tags = soup.find_all('h1')
    h2_tags = soup.find_all('h2')
    h3_tags = soup.find_all('h3')
    
    # H1 checks
    if len(h1_tags) == 0:
        issues.append("❌ No H1 tag found")
        recommendations.append("Add one H1 tag as the main page heading")
    elif len(h1_tags) > 1:
        issues.append(f"❌ Multiple H1 tags found ({len(h1_tags)})")
        recommendations.append("Use only one H1 tag per page")
    
    # Check heading hierarchy
    all_headings = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        all_headings.append((tag.name, tag.get_text().strip()))
    
    # SEO checks
    seo = page_data.get('seo', {})
    title = seo.get('title', '').strip()
    description = seo.get('description', '').strip()
    
    if not title:
        issues.append("❌ No SEO title set")
        recommendations.append(f"Add SEO title with location (Colorado) and service keywords")
    elif len(title) > 60:
        issues.append(f"⚠️ SEO title too long ({len(title)} chars)")
        recommendations.append("Keep SEO title under 60 characters")
    elif 'Colorado' not in title and 'Boulder' not in title and 'CO' not in title:
        issues.append("⚠️ SEO title missing location")
        recommendations.append("Include 'Colorado' or 'Boulder, CO' in title")
    
    if not description:
        issues.append("❌ No SEO description set")
        recommendations.append("Add compelling meta description with location and services")
    elif len(description) < 120:
        issues.append(f"⚠️ SEO description too short ({len(description)} chars)")
        recommendations.append("Expand description to 120-160 characters")
    elif len(description) > 160:
        issues.append(f"⚠️ SEO description too long ({len(description)} chars)")
        recommendations.append("Keep description under 160 characters")
    
    # Check for British spellings
    british_spellings = {
        'colour': 'color',
        'centre': 'center',
        'realise': 'realize',
        'organise': 'organize',
        'optimise': 'optimize',
        'specialise': 'specialize',
        'aluminium': 'aluminum',
        'honour': 'honor',
        'favour': 'favor',
        'behaviour': 'behavior'
    }
    
    text_content = soup.get_text().lower()
    for brit, amer in british_spellings.items():
        if brit in text_content:
            issues.append(f"⚠️ British spelling found: '{brit}'")
            recommendations.append(f"Change '{brit}' to '{amer}' (US spelling)")
    
    return {
        'headings': all_headings,
        'h1_count': len(h1_tags),
        'h2_count': len(h2_tags),
        'h3_count': len(h3_tags),
        'issues': issues,
        'recommendations': recommendations,
        'seo_title': title,
        'seo_description': description
    }

def generate_seo_suggestions(page_title, page_type):
    """Generate SEO title and description suggestions"""
    
    # Common BoulderWorks services
    services_map = {
        'laser cutting': 'Professional Laser Cutting Services',
        'laser engraving': 'Custom Laser Engraving Services',
        'acrylic cutting': 'Precision Acrylic Cutting',
        'metal cutting': 'Industrial Metal Cutting',
        'wood burning': 'Custom Wood Burning & Engraving',
        'gasket cutting': 'Custom Gasket Cutting Services',
        'media blasting': 'Media Blasting Services',
        'rubber cutting': 'Industrial Rubber Cutting',
        'signs': 'Custom Signs & Signage',
        'awards': 'Custom Awards & Recognition',
        'murals': 'Multi-Media Murals & Displays'
    }
    
    # Find matching service
    title_lower = page_title.lower()
    service_found = None
    for service, full_name in services_map.items():
        if service in title_lower:
            service_found = full_name
            break
    
    if page_type == 'home':
        return {
            'title': 'Laser Cutting & Engraving Services in Boulder, Colorado | BoulderWorks',
            'description': 'Professional laser cutting, engraving, and fabrication services in Boulder, CO. Custom awards, signs, metal cutting, and more. Get a quote today!'
        }
    elif page_type == 'about':
        return {
            'title': 'About BoulderWorks | Laser Cutting Experts in Boulder, CO',
            'description': 'Learn about BoulderWorks, Boulder Colorado\'s premier laser cutting and engraving company. Over 20 years of precision fabrication experience.'
        }
    elif page_type == 'contact':
        return {
            'title': 'Contact BoulderWorks | Laser Cutting Services in Boulder, CO',
            'description': 'Contact BoulderWorks for laser cutting, engraving, and custom fabrication in Boulder, Colorado. Get a free quote for your project today!'
        }
    elif service_found:
        return {
            'title': f'{service_found} in Boulder, CO | BoulderWorks',
            'description': f'Expert {service_found.lower()} in Boulder, Colorado. Fast turnaround, competitive pricing, and exceptional quality. Contact BoulderWorks today!'
        }
    else:
        return {
            'title': f'{page_title} | BoulderWorks - Boulder, CO',
            'description': f'{page_title} services by BoulderWorks in Boulder, Colorado. Professional laser cutting and fabrication services. Request a quote today!'
        }

def main():
    # Load page data
    with open('boulderworks_pages.json', 'r') as f:
        data = json.load(f)
    
    site = data['site']
    page_ids = data['page_ids']
    
    manager = WPBulkManager()
    api_key = manager.get_site_api_key(site['id'])
    
    print("BoulderWorks SEO & HTML Structure Analysis")
    print("=" * 80)
    print(f"Site: {site['url']}")
    print(f"Analyzing {len(page_ids)} pages...\n")
    
    # Fetch all pages concurrently
    pages_data = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(fetch_page_content, site['url'], api_key, pid): pid for pid in page_ids}
        
        for future in as_completed(future_to_id):
            page_id = future_to_id[future]
            try:
                result = future.result()
                if result:
                    pages_data[page_id] = result
            except Exception as e:
                print(f"Error fetching page {page_id}: {e}")
    
    # Analyze each page
    report = []
    for page_id, page_data in pages_data.items():
        analysis = analyze_page_structure(page_data)
        
        # Determine page type
        page_type = 'service'
        title_lower = page_data['title'].lower()
        if 'boulder works' in title_lower and page_id == 4:
            page_type = 'home'
        elif 'about' in title_lower:
            page_type = 'about'
        elif 'contact' in title_lower:
            page_type = 'contact'
        
        # Generate suggestions
        suggestions = generate_seo_suggestions(page_data['title'], page_type)
        
        report.append({
            'id': page_id,
            'title': page_data['title'],
            'status': page_data['status'],
            'analysis': analysis,
            'suggestions': suggestions
        })
    
    # Print report
    critical_pages = []
    for page in report:
        if page['status'] == 'publish' and len(page['analysis']['issues']) > 0:
            critical_pages.append(page)
    
    print(f"\n📊 SUMMARY: Found {len(critical_pages)} published pages with issues\n")
    
    # Detailed report for critical pages
    for page in sorted(critical_pages, key=lambda x: x['id']):
        print(f"\n{'='*80}")
        print(f"📄 PAGE: {page['title']} (ID: {page['id']})")
        print(f"Status: {page['status']}")
        print(f"\nCurrent SEO:")
        print(f"  Title: {page['analysis']['seo_title'] or 'Not set'}")
        print(f"  Desc: {page['analysis']['seo_description'] or 'Not set'}")
        
        if page['analysis']['issues']:
            print(f"\n🚨 Issues Found ({len(page['analysis']['issues'])}):")
            for issue in page['analysis']['issues']:
                print(f"  {issue}")
        
        print(f"\n💡 Recommendations:")
        for rec in page['analysis']['recommendations']:
            print(f"  • {rec}")
        
        print(f"\n✨ Suggested SEO:")
        print(f"  Title: {page['suggestions']['title']}")
        print(f"  Desc: {page['suggestions']['description']}")
        
        # Show heading structure
        if page['analysis']['headings']:
            print(f"\n📋 Heading Structure:")
            for tag, text in page['analysis']['headings'][:5]:
                indent = "  " * (int(tag[1]) - 1)
                print(f"  {indent}{tag.upper()}: {text[:50]}...")
    
    # Save full report
    with open('boulderworks_seo_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n\n✅ Full report saved to: boulderworks_seo_report.json")
    print(f"📌 Focus on fixing the {len(critical_pages)} published pages first!")

if __name__ == "__main__":
    main()