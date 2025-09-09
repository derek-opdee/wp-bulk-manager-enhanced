#!/usr/bin/env python3
"""
SEO Audit for renowarriors.com.au
"""

import json
from datetime import datetime
from wpbm_manager_v2 import WPBulkManagerV2
from wpbm_cli_enhanced import EnhancedWPBulkManager
import re

def check_australian_spelling(text):
    """Check for common US/UK vs Australian spelling differences"""
    us_to_au = {
        'color': 'colour',
        'honor': 'honour',
        'flavor': 'flavour',
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
        'fiber': 'fibre'
    }
    
    issues = []
    if text:
        text_lower = text.lower()
        for us_word, au_word in us_to_au.items():
            if us_word in text_lower and au_word not in text_lower:
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
        issues.append("No H1 tag found - critical for SEO")
    elif len(h1_matches) > 1:
        issues.append(f"Multiple H1 tags found ({len(h1_matches)}) - should only have one")
    
    # Check if H1 is empty or too short
    if h1_matches:
        h1_text = re.sub('<[^<]+?>', '', h1_matches[0]).strip()
        if not h1_text:
            issues.append("H1 tag is empty")
        elif len(h1_text) < 10:
            issues.append(f"H1 tag too short ({len(h1_text)} chars)")
    
    return issues

def perform_seo_audit(site_name='RenoWarriors'):
    """Perform comprehensive SEO audit"""
    
    # Initialize managers
    manager_v2 = WPBulkManagerV2()
    
    # Add site to manager
    print(f"🔧 Adding {site_name} to WP Bulk Manager...")
    manager_v2.add_site(
        name=site_name,
        url='https://renowarriors.com.au',
        api_key='0ab365b5b83f46b65bf12466c404bfd3'
    )
    
    # Create enhanced manager and select site
    manager = EnhancedWPBulkManager()
    sites = manager.get_sites('active')
    
    # Find our site
    site = next((s for s in sites if s['name'] == site_name), None)
    if not site:
        print("❌ Could not find site in manager")
        return
    
    site_id = site['id']
    print(f"✅ Connected to {site['name']} ({site['url']})")
    print("-" * 80)
    
    # Get all content
    print("\n📋 Fetching all content...")
    all_content = manager.list_all_content(site_id, 'any', 200)
    
    # Separate pages and posts
    pages = [c for c in all_content if c['type'] == 'page']
    posts = [c for c in all_content if c['type'] == 'post']
    
    print(f"\n📊 Content Summary:")
    print(f"  • Total Pages: {len(pages)}")
    print(f"  • Total Posts: {len(posts)}")
    print(f"  • Published: {len([c for c in all_content if c['status'] == 'publish'])}")
    print(f"  • Drafts: {len([c for c in all_content if c['status'] == 'draft'])}")
    
    # Get SEO data
    print("\n🔍 Analyzing SEO...")
    seo_data = manager.get_all_seo_data(site_id, 200)
    
    # Initialize issue counters
    seo_issues = {
        'missing_title': [],
        'title_too_long': [],
        'title_too_short': [],
        'missing_description': [],
        'description_too_long': [],
        'description_too_short': [],
        'h1_issues': [],
        'spelling_issues': [],
        'local_seo_issues': []
    }
    
    # Analyze each page
    print("\n📄 Analyzing individual pages...")
    for page in seo_data:
        page_issues = []
        
        # Check SEO title
        seo_title = page.get('seo_title', '')
        if not seo_title:
            seo_issues['missing_title'].append({
                'id': page['id'],
                'title': page['title'],
                'url': page['url']
            })
        else:
            if len(seo_title) > 60:
                seo_issues['title_too_long'].append({
                    'id': page['id'],
                    'title': page['title'],
                    'seo_title': seo_title,
                    'length': len(seo_title),
                    'url': page['url']
                })
            elif len(seo_title) < 30:
                seo_issues['title_too_short'].append({
                    'id': page['id'],
                    'title': page['title'],
                    'seo_title': seo_title,
                    'length': len(seo_title),
                    'url': page['url']
                })
        
        # Check SEO description
        seo_desc = page.get('seo_description', '')
        if not seo_desc:
            seo_issues['missing_description'].append({
                'id': page['id'],
                'title': page['title'],
                'url': page['url']
            })
        else:
            if len(seo_desc) > 160:
                seo_issues['description_too_long'].append({
                    'id': page['id'],
                    'title': page['title'],
                    'seo_description': seo_desc,
                    'length': len(seo_desc),
                    'url': page['url']
                })
            elif len(seo_desc) < 120:
                seo_issues['description_too_short'].append({
                    'id': page['id'],
                    'title': page['title'],
                    'seo_description': seo_desc,
                    'length': len(seo_desc),
                    'url': page['url']
                })
        
        # Get full page content for H1 and spelling analysis
        try:
            full_content = manager.get_content_details(site_id, page['id'])
            
            # Check H1 structure
            h1_issues = analyze_h1_structure(full_content.get('content', ''))
            if h1_issues:
                seo_issues['h1_issues'].append({
                    'id': page['id'],
                    'title': page['title'],
                    'url': page['url'],
                    'issues': h1_issues
                })
            
            # Check Australian spelling
            combined_text = f"{page['title']} {seo_title} {seo_desc} {full_content.get('content', '')}"
            spelling_issues = check_australian_spelling(combined_text)
            if spelling_issues:
                seo_issues['spelling_issues'].append({
                    'id': page['id'],
                    'title': page['title'],
                    'url': page['url'],
                    'issues': spelling_issues
                })
            
            # Check for local SEO indicators
            local_keywords = ['australia', 'australian', 'melbourne', 'sydney', 'brisbane', 'perth', 'adelaide', 'au']
            content_lower = combined_text.lower()
            has_local_keywords = any(keyword in content_lower for keyword in local_keywords)
            
            if not has_local_keywords and 'contact' not in page['title'].lower() and 'about' not in page['title'].lower():
                seo_issues['local_seo_issues'].append({
                    'id': page['id'],
                    'title': page['title'],
                    'url': page['url'],
                    'issue': 'No Australian location indicators found'
                })
                
        except Exception as e:
            print(f"  ⚠️  Error analyzing page {page['id']}: {str(e)}")
    
    # Generate report
    print("\n" + "="*80)
    print("📊 SEO AUDIT REPORT - renowarriors.com.au")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Summary of issues
    total_issues = sum(len(issues) for issues in seo_issues.values())
    print(f"\n🚨 Total Issues Found: {total_issues}")
    
    # Critical issues
    print("\n❗ CRITICAL ISSUES:")
    
    if seo_issues['missing_title']:
        print(f"\n📌 Missing SEO Titles ({len(seo_issues['missing_title'])} pages):")
        for issue in seo_issues['missing_title'][:5]:  # First 5
            print(f"  • {issue['title']}")
            print(f"    URL: {issue['url']}")
    
    if seo_issues['missing_description']:
        print(f"\n📝 Missing SEO Descriptions ({len(seo_issues['missing_description'])} pages):")
        for issue in seo_issues['missing_description'][:5]:  # First 5
            print(f"  • {issue['title']}")
            print(f"    URL: {issue['url']}")
    
    if seo_issues['h1_issues']:
        print(f"\n🏷️  H1 Tag Issues ({len(seo_issues['h1_issues'])} pages):")
        for issue in seo_issues['h1_issues'][:5]:  # First 5
            print(f"  • {issue['title']}")
            for h1_issue in issue['issues']:
                print(f"    - {h1_issue}")
    
    # Medium priority issues
    print("\n⚠️  MEDIUM PRIORITY ISSUES:")
    
    if seo_issues['title_too_long'] or seo_issues['title_too_short']:
        print(f"\n📏 Title Length Issues:")
        if seo_issues['title_too_long']:
            print(f"  Too long ({len(seo_issues['title_too_long'])} pages):")
            for issue in seo_issues['title_too_long'][:3]:
                print(f"    • {issue['title']} ({issue['length']} chars)")
        if seo_issues['title_too_short']:
            print(f"  Too short ({len(seo_issues['title_too_short'])} pages):")
            for issue in seo_issues['title_too_short'][:3]:
                print(f"    • {issue['title']} ({issue['length']} chars)")
    
    if seo_issues['description_too_long'] or seo_issues['description_too_short']:
        print(f"\n📏 Description Length Issues:")
        if seo_issues['description_too_long']:
            print(f"  Too long ({len(seo_issues['description_too_long'])} pages):")
            for issue in seo_issues['description_too_long'][:3]:
                print(f"    • {issue['title']} ({issue['length']} chars)")
        if seo_issues['description_too_short']:
            print(f"  Too short ({len(seo_issues['description_too_short'])} pages):")
            for issue in seo_issues['description_too_short'][:3]:
                print(f"    • {issue['title']} ({issue['length']} chars)")
    
    # Australian compliance
    print("\n🇦🇺 AUSTRALIAN COMPLIANCE:")
    
    if seo_issues['spelling_issues']:
        print(f"\n🔤 Spelling Issues ({len(seo_issues['spelling_issues'])} pages with US spelling):")
        for issue in seo_issues['spelling_issues'][:5]:
            print(f"  • {issue['title']}")
            for spelling in issue['issues'][:2]:  # First 2 issues per page
                print(f"    - {spelling}")
    
    if seo_issues['local_seo_issues']:
        print(f"\n📍 Local SEO Issues ({len(seo_issues['local_seo_issues'])} pages):")
        for issue in seo_issues['local_seo_issues'][:5]:
            print(f"  • {issue['title']}")
            print(f"    - {issue['issue']}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    print("\n1. SEO Titles & Descriptions:")
    print("   • Add missing SEO titles and descriptions immediately")
    print("   • Optimize title length to 50-60 characters")
    print("   • Optimize description length to 120-160 characters")
    print("   • Include primary keywords and location (Australia/city)")
    
    print("\n2. H1 Tags:")
    print("   • Ensure every page has exactly one H1 tag")
    print("   • H1 should contain primary keyword")
    print("   • H1 should be descriptive and compelling")
    
    print("\n3. Australian Localization:")
    print("   • Convert all US spelling to Australian spelling")
    print("   • Add location-specific keywords where relevant")
    print("   • Include 'Australia' or city names in titles/descriptions")
    
    print("\n4. Local SEO:")
    print("   • Add schema markup for local business")
    print("   • Include NAP (Name, Address, Phone) consistently")
    print("   • Create location-specific landing pages if serving multiple areas")
    
    # Save detailed report
    report_data = {
        'site': site_name,
        'url': 'https://renowarriors.com.au',
        'audit_date': datetime.now().isoformat(),
        'summary': {
            'total_pages': len(pages),
            'total_posts': len(posts),
            'total_issues': total_issues
        },
        'issues': seo_issues
    }
    
    report_filename = f"reports/renowarriors_seo_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs('reports', exist_ok=True)
    
    with open(report_filename, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n✅ Detailed report saved to: {report_filename}")
    
    return report_data


if __name__ == "__main__":
    import os
    os.system('clear')
    print("🚀 Starting SEO Audit for renowarriors.com.au")
    print("="*80)
    
    try:
        perform_seo_audit()
    except Exception as e:
        print(f"\n❌ Error during audit: {str(e)}")
        import traceback
        traceback.print_exc()