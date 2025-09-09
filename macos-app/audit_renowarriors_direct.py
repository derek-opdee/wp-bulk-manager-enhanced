#!/usr/bin/env python3
"""
Direct SEO Audit for renowarriors.com.au
"""

import requests
import json
import re
from datetime import datetime
import os

# Site configuration
SITE_URL = 'https://renowarriors.com.au'
API_KEY = '0ab365b5b83f46b65bf12466c404bfd3'
API_BASE = f'{SITE_URL}/wp-json'

# Headers for API requests
headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

def check_australian_spelling(text):
    """Check for common US/UK vs Australian spelling differences"""
    us_to_au = {
        'color': 'colour',
        'honor': 'honour',
        'favor': 'favour',
        'neighbor': 'neighbour',
        'favorite': 'favourite',
        'realize': 'realise',
        'organize': 'organise',
        'recognize': 'recognise',
        'analyze': 'analyse',
        'catalog': 'catalogue',
        'dialog': 'dialogue',
        'meter': 'metre',
        'center': 'centre',
        'theater': 'theatre',
        'fiber': 'fibre',
        'optimization': 'optimisation',
        'specialized': 'specialised',
        'minimize': 'minimise',
        'maximize': 'maximise'
    }
    
    issues = []
    if text:
        text_lower = text.lower()
        for us_word, au_word in us_to_au.items():
            pattern = r'\b' + us_word + r'\b'
            if re.search(pattern, text_lower):
                issues.append(f"Found US spelling '{us_word}' - should be '{au_word}'")
    
    return issues

def analyze_h1_structure(content):
    """Analyze H1 tag structure"""
    issues = []
    
    if not content:
        return ["No content found"]
    
    # Find all H1 tags
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    
    if len(h1_matches) == 0:
        issues.append("No H1 tag found")
    elif len(h1_matches) > 1:
        issues.append(f"Multiple H1 tags ({len(h1_matches)})")
    
    if h1_matches:
        h1_text = re.sub('<[^<]+?>', '', h1_matches[0]).strip()
        if not h1_text:
            issues.append("H1 tag is empty")
        elif len(h1_text) < 10:
            issues.append(f"H1 too short ({len(h1_text)} chars)")
    
    return issues

def get_pages():
    """Get all pages from WordPress"""
    print("📋 Fetching pages...")
    try:
        response = requests.get(
            f'{API_BASE}/wp/v2/pages',
            headers=headers,
            params={'per_page': 100}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching pages: {e}")
        return []

def get_posts():
    """Get all posts from WordPress"""
    print("📋 Fetching posts...")
    try:
        response = requests.get(
            f'{API_BASE}/wp/v2/posts',
            headers=headers,
            params={'per_page': 100}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching posts: {e}")
        return []

def get_yoast_data(post_id, post_type='pages'):
    """Get Yoast SEO data for a page/post"""
    try:
        response = requests.get(
            f'{API_BASE}/wp/v2/{post_type}/{post_id}',
            headers=headers,
            params={'_fields': 'yoast_head_json,title,content,link'}
        )
        response.raise_for_status()
        return response.json()
    except:
        return None

def perform_seo_audit():
    """Perform comprehensive SEO audit"""
    
    print(f"🚀 Starting SEO Audit for {SITE_URL}")
    print("="*80)
    
    # Get all content
    pages = get_pages()
    posts = get_posts()
    
    print(f"\n📊 Content Summary:")
    print(f"  • Total Pages: {len(pages)}")
    print(f"  • Total Posts: {len(posts)}")
    
    # Initialize issue tracking
    issues = {
        'missing_title': [],
        'title_issues': [],
        'missing_description': [],
        'description_issues': [],
        'h1_issues': [],
        'spelling_issues': [],
        'local_seo_issues': []
    }
    
    # Analyze pages
    print("\n🔍 Analyzing pages...")
    for page in pages:
        page_id = page['id']
        page_title = page['title']['rendered']
        page_url = page['link']
        content = page['content']['rendered']
        
        # Get Yoast data if available
        yoast_data = get_yoast_data(page_id, 'pages')
        
        # Default to basic meta if no Yoast
        seo_title = ''
        seo_description = ''
        
        if yoast_data and 'yoast_head_json' in yoast_data:
            yoast = yoast_data['yoast_head_json']
            seo_title = yoast.get('title', '')
            seo_description = yoast.get('og_description', '') or yoast.get('description', '')
        
        # Check SEO title
        if not seo_title or seo_title == page_title:
            issues['missing_title'].append({
                'title': page_title,
                'url': page_url
            })
        elif len(seo_title) > 60 or len(seo_title) < 30:
            issues['title_issues'].append({
                'title': page_title,
                'seo_title': seo_title,
                'length': len(seo_title),
                'url': page_url
            })
        
        # Check SEO description
        if not seo_description:
            issues['missing_description'].append({
                'title': page_title,
                'url': page_url
            })
        elif len(seo_description) > 160 or len(seo_description) < 120:
            issues['description_issues'].append({
                'title': page_title,
                'description': seo_description,
                'length': len(seo_description),
                'url': page_url
            })
        
        # Check H1 structure
        h1_problems = analyze_h1_structure(content)
        if h1_problems:
            issues['h1_issues'].append({
                'title': page_title,
                'url': page_url,
                'problems': h1_problems
            })
        
        # Check Australian spelling
        combined_text = f"{page_title} {seo_title} {seo_description} {content}"
        spelling_problems = check_australian_spelling(combined_text)
        if spelling_problems:
            issues['spelling_issues'].append({
                'title': page_title,
                'url': page_url,
                'problems': spelling_problems[:3]  # First 3 issues
            })
        
        # Check local SEO
        local_keywords = ['australia', 'melbourne', 'sydney', 'brisbane', 'perth', 'adelaide', 'renovation warriors']
        has_local = any(kw in combined_text.lower() for kw in local_keywords)
        if not has_local and 'contact' not in page_title.lower():
            issues['local_seo_issues'].append({
                'title': page_title,
                'url': page_url
            })
    
    # Generate Report
    print("\n" + "="*80)
    print("📊 SEO AUDIT RESULTS")
    print("="*80)
    
    total_issues = sum(len(v) for v in issues.values())
    print(f"\n🚨 Total Issues: {total_issues}")
    
    # Critical Issues
    if issues['missing_title']:
        print(f"\n❗ Missing SEO Titles: {len(issues['missing_title'])}")
        for item in issues['missing_title'][:3]:
            print(f"  • {item['title']}")
    
    if issues['missing_description']:
        print(f"\n❗ Missing Meta Descriptions: {len(issues['missing_description'])}")
        for item in issues['missing_description'][:3]:
            print(f"  • {item['title']}")
    
    if issues['h1_issues']:
        print(f"\n❗ H1 Tag Issues: {len(issues['h1_issues'])}")
        for item in issues['h1_issues'][:3]:
            print(f"  • {item['title']}: {', '.join(item['problems'])}")
    
    # Length Issues
    if issues['title_issues']:
        print(f"\n⚠️  Title Length Issues: {len(issues['title_issues'])}")
        for item in issues['title_issues'][:3]:
            print(f"  • {item['title']} ({item['length']} chars)")
    
    if issues['description_issues']:
        print(f"\n⚠️  Description Length Issues: {len(issues['description_issues'])}")
        for item in issues['description_issues'][:3]:
            print(f"  • {item['title']} ({item['length']} chars)")
    
    # Australian Compliance
    if issues['spelling_issues']:
        print(f"\n🇦🇺 US Spelling Found: {len(issues['spelling_issues'])} pages")
        for item in issues['spelling_issues'][:3]:
            print(f"  • {item['title']}")
            for problem in item['problems'][:2]:
                print(f"    - {problem}")
    
    if issues['local_seo_issues']:
        print(f"\n📍 Missing Local Keywords: {len(issues['local_seo_issues'])} pages")
        for item in issues['local_seo_issues'][:3]:
            print(f"  • {item['title']}")
    
    # Recommendations
    print("\n💡 KEY RECOMMENDATIONS:")
    print("\n1. CRITICAL FIXES:")
    print("   • Add unique SEO titles to all pages (50-60 chars)")
    print("   • Add meta descriptions to all pages (120-160 chars)")
    print("   • Ensure every page has exactly one H1 tag")
    
    print("\n2. CONTENT OPTIMIZATION:")
    print("   • Include 'renovation' keywords in titles")
    print("   • Add location modifiers (Melbourne, Australia)")
    print("   • Focus on 'Renovation Warriors' branding")
    
    print("\n3. AUSTRALIAN LOCALIZATION:")
    print("   • Convert US spelling to Australian")
    print("   • Add suburb/city names for local SEO")
    print("   • Include 'Australia' in key pages")
    
    print("\n4. TECHNICAL SEO:")
    print("   • Implement schema markup")
    print("   • Add XML sitemap")
    print("   • Optimize page load speed")
    
    # Save report
    os.makedirs('reports', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    report_data = {
        'site': SITE_URL,
        'audit_date': datetime.now().isoformat(),
        'summary': {
            'total_pages': len(pages),
            'total_posts': len(posts),
            'total_issues': total_issues
        },
        'issues': issues
    }
    
    report_file = f'reports/renowarriors_audit_{timestamp}.json'
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n✅ Report saved: {report_file}")
    
    return report_data


if __name__ == "__main__":
    os.system('clear')
    try:
        perform_seo_audit()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()