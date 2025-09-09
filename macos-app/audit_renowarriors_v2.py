#!/usr/bin/env python3
"""
SEO Audit for renowarriors.com.au using WP Bulk Manager
"""

import json
import os
from datetime import datetime
from wpbm_manager_v2 import WPBulkManagerV2
from wpbm.operations.content import ContentOperations
from wpbm.operations.seo import SEOOperations
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
        'fiber': 'fibre',
        'optimization': 'optimisation',
        'specialized': 'specialised'
    }
    
    issues = []
    if text:
        text_lower = text.lower()
        for us_word, au_word in us_to_au.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + us_word + r'\b'
            if re.search(pattern, text_lower) and au_word not in text_lower:
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

def perform_seo_audit():
    """Perform comprehensive SEO audit for RenoWarriors"""
    
    # Initialize manager
    manager = WPBulkManagerV2()
    
    # Get client for RenoWarriors
    client = manager.get_client('RenoWarriors')
    if not client:
        # Try adding the site
        print("🔧 Site not found, adding RenoWarriors...")
        success = manager.add_site(
            name='RenoWarriors',
            url='https://renowarriors.com.au',
            api_key='0ab365b5b83f46b65bf12466c404bfd3'
        )
        if success:
            client = manager.get_client('RenoWarriors')
        else:
            print("❌ Failed to add site")
            return
    
    print(f"✅ Connected to RenoWarriors (https://renowarriors.com.au)")
    print("-" * 80)
    
    # Initialize operations
    content_ops = ContentOperations(client)
    seo_ops = SEOOperations(client)
    
    # Get all content
    print("\n📋 Fetching all content...")
    all_pages = content_ops.list_content(post_type='page', per_page=100)
    all_posts = content_ops.list_content(post_type='post', per_page=100)
    
    print(f"\n📊 Content Summary:")
    print(f"  • Total Pages: {len(all_pages)}")
    print(f"  • Total Posts: {len(all_posts)}")
    
    # Initialize issue tracking
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
    
    # Analyze pages
    print("\n🔍 Analyzing pages for SEO issues...")
    
    for page in all_pages:
        page_id = page['id']
        page_title = page['title']['rendered']
        page_url = page['link']
        
        # Get SEO data
        seo_data = seo_ops.get_seo_data(page_id)
        
        # Check SEO title
        seo_title = seo_data.get('title', '') if seo_data else ''
        if not seo_title:
            seo_issues['missing_title'].append({
                'id': page_id,
                'title': page_title,
                'url': page_url
            })
        else:
            if len(seo_title) > 60:
                seo_issues['title_too_long'].append({
                    'id': page_id,
                    'title': page_title,
                    'seo_title': seo_title,
                    'length': len(seo_title),
                    'url': page_url
                })
            elif len(seo_title) < 30:
                seo_issues['title_too_short'].append({
                    'id': page_id,
                    'title': page_title,
                    'seo_title': seo_title,
                    'length': len(seo_title),
                    'url': page_url
                })
        
        # Check SEO description
        seo_desc = seo_data.get('description', '') if seo_data else ''
        if not seo_desc:
            seo_issues['missing_description'].append({
                'id': page_id,
                'title': page_title,
                'url': page_url
            })
        else:
            if len(seo_desc) > 160:
                seo_issues['description_too_long'].append({
                    'id': page_id,
                    'title': page_title,
                    'seo_description': seo_desc,
                    'length': len(seo_desc),
                    'url': page_url
                })
            elif len(seo_desc) < 120:
                seo_issues['description_too_short'].append({
                    'id': page_id,
                    'title': page_title,
                    'seo_description': seo_desc,
                    'length': len(seo_desc),
                    'url': page_url
                })
        
        # Get full content
        page_content = page.get('content', {}).get('rendered', '')
        
        # Check H1 structure
        h1_issues = analyze_h1_structure(page_content)
        if h1_issues:
            seo_issues['h1_issues'].append({
                'id': page_id,
                'title': page_title,
                'url': page_url,
                'issues': h1_issues
            })
        
        # Check Australian spelling
        combined_text = f"{page_title} {seo_title} {seo_desc} {page_content}"
        spelling_issues = check_australian_spelling(combined_text)
        if spelling_issues:
            seo_issues['spelling_issues'].append({
                'id': page_id,
                'title': page_title,
                'url': page_url,
                'issues': spelling_issues
            })
        
        # Check for local SEO indicators
        local_keywords = ['australia', 'australian', 'melbourne', 'sydney', 'brisbane', 'perth', 'adelaide', 'hobart', 'darwin', 'canberra', 'queensland', 'nsw', 'victoria', 'tasmania']
        content_lower = combined_text.lower()
        has_local_keywords = any(keyword in content_lower for keyword in local_keywords)
        
        # Don't flag contact/about pages for local SEO
        if not has_local_keywords and not any(word in page_title.lower() for word in ['contact', 'about', 'privacy', 'terms']):
            seo_issues['local_seo_issues'].append({
                'id': page_id,
                'title': page_title,
                'url': page_url,
                'issue': 'No Australian location indicators found'
            })
    
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
        for issue in seo_issues['missing_title'][:5]:
            print(f"  • {issue['title']}")
            print(f"    URL: {issue['url']}")
    
    if seo_issues['missing_description']:
        print(f"\n📝 Missing SEO Descriptions ({len(seo_issues['missing_description'])} pages):")
        for issue in seo_issues['missing_description'][:5]:
            print(f"  • {issue['title']}")
            print(f"    URL: {issue['url']}")
    
    if seo_issues['h1_issues']:
        print(f"\n🏷️  H1 Tag Issues ({len(seo_issues['h1_issues'])} pages):")
        for issue in seo_issues['h1_issues'][:5]:
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
            for spelling in issue['issues'][:2]:
                print(f"    - {spelling}")
    else:
        print("\n✅ No US spelling issues found - good Australian spelling compliance!")
    
    if seo_issues['local_seo_issues']:
        print(f"\n📍 Local SEO Issues ({len(seo_issues['local_seo_issues'])} pages lacking local indicators):")
        for issue in seo_issues['local_seo_issues'][:5]:
            print(f"  • {issue['title']}")
            print(f"    - {issue['issue']}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    print("\n1. SEO Titles & Descriptions:")
    print("   • Add missing SEO titles and descriptions immediately")
    print("   • Optimize title length to 50-60 characters")
    print("   • Optimize description length to 120-160 characters")
    print("   • Include renovation/construction keywords")
    
    print("\n2. H1 Tags:")
    print("   • Ensure every page has exactly one H1 tag")
    print("   • H1 should contain primary keyword")
    print("   • H1 should be compelling and descriptive")
    
    print("\n3. Australian Localization:")
    print("   • Maintain Australian spelling throughout")
    print("   • Add location-specific keywords where relevant")
    print("   • Include city/state names in service pages")
    
    print("\n4. Local SEO:")
    print("   • Add location keywords to service pages")
    print("   • Create location-specific landing pages")
    print("   • Include \"Australia\" or city names in meta descriptions")
    print("   • Add schema markup for local business")
    
    print("\n5. Content Optimization:")
    print("   • Focus on renovation/construction keywords")
    print("   • Include terms like 'renovation warriors', 'home renovation', etc.")
    print("   • Create service-specific pages for different renovation types")
    
    # Save detailed report
    report_data = {
        'site': 'RenoWarriors',
        'url': 'https://renowarriors.com.au',
        'audit_date': datetime.now().isoformat(),
        'summary': {
            'total_pages': len(all_pages),
            'total_posts': len(all_posts),
            'total_issues': total_issues
        },
        'issues': seo_issues
    }
    
    os.makedirs('reports', exist_ok=True)
    report_filename = f"reports/renowarriors_seo_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_filename, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n✅ Detailed report saved to: {report_filename}")
    
    return report_data


if __name__ == "__main__":
    os.system('clear')
    print("🚀 Starting SEO Audit for renowarriors.com.au")
    print("="*80)
    
    try:
        perform_seo_audit()
    except Exception as e:
        print(f"\n❌ Error during audit: {str(e)}")
        import traceback
        traceback.print_exc()