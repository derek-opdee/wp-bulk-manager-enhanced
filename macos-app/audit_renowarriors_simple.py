#!/usr/bin/env python3
"""
SEO Audit for renowarriors.com.au using WP Bulk Manager Assistant
"""

import json
import os
from datetime import datetime
from wpbm_assistant import WPBulkAssistant
from wpbm_manager_v2 import WPBulkManagerV2
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

def perform_audit():
    """Perform SEO audit using the assistant"""
    
    # First add the site using manager v2
    manager = WPBulkManagerV2()
    print("🔧 Adding RenoWarriors site...")
    manager.add_site(
        name='RenoWarriors',
        url='https://renowarriors.com.au',
        api_key='0ab365b5b83f46b65bf12466c404bfd3'
    )
    
    # Initialize assistant
    assistant = WPBulkAssistant()
    
    # Select the site
    if not assistant.select_site('RenoWarriors'):
        print("❌ Could not select RenoWarriors site")
        return
    
    print(f"✅ Connected to {assistant.current_site['name']} ({assistant.current_site['url']})")
    print("-" * 80)
    
    # Get content summary
    print("\n📋 Getting content summary...")
    summary = assistant.get_content_summary()
    
    print(f"\n📊 Content Summary:")
    print(f"  • Total Content: {summary['total']}")
    print(f"  • Pages: {summary['pages']}")
    print(f"  • Posts: {summary['posts']}")
    print(f"  • Published: {summary['published']}")
    print(f"  • Drafts: {summary['drafts']}")
    
    # Analyze SEO issues
    print("\n🔍 Analyzing SEO issues...")
    seo_issues = assistant.analyze_seo_issues()
    
    # Get additional details for each page with issues
    enhanced_issues = []
    for issue_page in seo_issues[:20]:  # Analyze first 20 pages with issues
        page_id = issue_page['page_id']
        
        try:
            # Get full page content
            page_content = assistant.get_page_content(page_id)
            
            # Analyze H1 tags
            h1_issues = analyze_h1_structure(page_content.get('content', ''))
            
            # Check Australian spelling
            combined_text = f"{page_content['title']} {page_content.get('content', '')}"
            if page_content.get('seo'):
                combined_text += f" {page_content['seo'].get('title', '')} {page_content['seo'].get('description', '')}"
            
            spelling_issues = check_australian_spelling(combined_text)
            
            # Check local SEO
            local_keywords = ['australia', 'australian', 'melbourne', 'sydney', 'brisbane', 'perth', 'adelaide']
            has_local = any(kw in combined_text.lower() for kw in local_keywords)
            
            enhanced_issue = {
                **issue_page,
                'h1_issues': h1_issues,
                'spelling_issues': spelling_issues,
                'has_local_keywords': has_local
            }
            enhanced_issues.append(enhanced_issue)
            
        except Exception as e:
            print(f"  ⚠️  Error analyzing page {page_id}: {str(e)}")
    
    # Generate comprehensive report
    print("\n" + "="*80)
    print("📊 SEO AUDIT REPORT - renowarriors.com.au")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Count different issue types
    missing_titles = sum(1 for p in enhanced_issues for i in p['issues'] if i['type'] == 'missing_title')
    missing_descriptions = sum(1 for p in enhanced_issues for i in p['issues'] if i['type'] == 'missing_description')
    title_length_issues = sum(1 for p in enhanced_issues for i in p['issues'] if 'title_too' in i['type'])
    desc_length_issues = sum(1 for p in enhanced_issues for i in p['issues'] if 'description_too' in i['type'])
    h1_issue_count = sum(1 for p in enhanced_issues if p.get('h1_issues'))
    spelling_issue_count = sum(1 for p in enhanced_issues if p.get('spelling_issues'))
    no_local_count = sum(1 for p in enhanced_issues if not p.get('has_local_keywords'))
    
    print(f"\n🚨 Issues Summary:")
    print(f"  • Pages with issues: {len(seo_issues)}")
    print(f"  • Missing titles: {missing_titles}")
    print(f"  • Missing descriptions: {missing_descriptions}")
    print(f"  • Title length issues: {title_length_issues}")
    print(f"  • Description length issues: {desc_length_issues}")
    print(f"  • H1 tag issues: {h1_issue_count}")
    print(f"  • Spelling issues: {spelling_issue_count}")
    print(f"  • Missing local keywords: {no_local_count}")
    
    # Show critical issues
    print("\n❗ CRITICAL ISSUES:")
    
    # Missing titles
    pages_missing_title = [p for p in enhanced_issues if any(i['type'] == 'missing_title' for i in p['issues'])]
    if pages_missing_title:
        print(f"\n📌 Missing SEO Titles ({len(pages_missing_title)} pages):")
        for page in pages_missing_title[:5]:
            print(f"  • {page['page_title']}")
            print(f"    URL: {page['url']}")
    
    # Missing descriptions
    pages_missing_desc = [p for p in enhanced_issues if any(i['type'] == 'missing_description' for i in p['issues'])]
    if pages_missing_desc:
        print(f"\n📝 Missing SEO Descriptions ({len(pages_missing_desc)} pages):")
        for page in pages_missing_desc[:5]:
            print(f"  • {page['page_title']}")
            print(f"    URL: {page['url']}")
    
    # H1 issues
    pages_h1_issues = [p for p in enhanced_issues if p.get('h1_issues')]
    if pages_h1_issues:
        print(f"\n🏷️  H1 Tag Issues ({len(pages_h1_issues)} pages):")
        for page in pages_h1_issues[:5]:
            print(f"  • {page['page_title']}")
            for issue in page['h1_issues']:
                print(f"    - {issue}")
    
    # Australian spelling issues
    print("\n🇦🇺 AUSTRALIAN COMPLIANCE:")
    pages_spelling_issues = [p for p in enhanced_issues if p.get('spelling_issues')]
    if pages_spelling_issues:
        print(f"\n🔤 US Spelling Found ({len(pages_spelling_issues)} pages):")
        for page in pages_spelling_issues[:5]:
            print(f"  • {page['page_title']}")
            for issue in page['spelling_issues'][:2]:
                print(f"    - {issue}")
    else:
        print("\n✅ No US spelling issues found!")
    
    # Local SEO
    pages_no_local = [p for p in enhanced_issues if not p.get('has_local_keywords')]
    if pages_no_local:
        print(f"\n📍 Pages Missing Local Keywords ({len(pages_no_local)} pages):")
        for page in pages_no_local[:5]:
            print(f"  • {page['page_title']}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    
    print("\n1. IMMEDIATE ACTIONS:")
    print("   • Add missing SEO titles and descriptions")
    print("   • Fix pages with no H1 tags")
    print("   • Ensure single H1 per page")
    
    print("\n2. SEO OPTIMIZATION:")
    print("   • Titles: 50-60 characters")
    print("   • Descriptions: 120-160 characters")
    print("   • Include 'renovation' keywords")
    print("   • Add location modifiers (Australia, city names)")
    
    print("\n3. AUSTRALIAN LOCALIZATION:")
    print("   • Convert any US spelling to Australian")
    print("   • Add Australian location keywords")
    print("   • Include local area names for service pages")
    
    print("\n4. CONTENT STRATEGY:")
    print("   • Create location-specific service pages")
    print("   • Focus on 'renovation warriors' branding")
    print("   • Include renovation types (kitchen, bathroom, etc.)")
    print("   • Add customer testimonials with locations")
    
    # Generate full report
    print("\n📄 Generating full report...")
    full_report = assistant.generate_report()
    
    # Save reports
    os.makedirs('reports', exist_ok=True)
    
    # Save text report
    text_report_file = f"reports/renowarriors_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(text_report_file, 'w') as f:
        f.write(full_report)
    
    # Save JSON data
    json_data = {
        'site': 'RenoWarriors',
        'url': 'https://renowarriors.com.au',
        'audit_date': datetime.now().isoformat(),
        'summary': summary,
        'seo_issues': enhanced_issues,
        'statistics': {
            'total_issues': len(seo_issues),
            'missing_titles': missing_titles,
            'missing_descriptions': missing_descriptions,
            'h1_issues': h1_issue_count,
            'spelling_issues': spelling_issue_count,
            'no_local_keywords': no_local_count
        }
    }
    
    json_report_file = f"reports/renowarriors_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_report_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    print(f"\n✅ Reports saved:")
    print(f"   • Text report: {text_report_file}")
    print(f"   • JSON data: {json_report_file}")
    
    return json_data


if __name__ == "__main__":
    os.system('clear')
    print("🚀 Starting SEO Audit for renowarriors.com.au")
    print("="*80)
    
    try:
        perform_audit()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()