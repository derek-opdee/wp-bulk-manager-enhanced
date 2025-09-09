#!/usr/bin/env python3
"""
Comprehensive content quality analysis for derekzar.com using MySQL manager
Checks for:
- Lorem ipsum or placeholder text
- H1 semantic structure
- SEO titles and meta descriptions
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path

# Add the wpbm package to path
sys.path.insert(0, str(Path(__file__).parent))

from wpbm_manager_mysql import WPBulkManagerMySQL
from wpbm.utils.logger import get_logger

logger = get_logger(__name__)

def detect_placeholder_text(content):
    """Detect lorem ipsum or placeholder text"""
    if not content:
        return []
    
    # Convert to lowercase for case-insensitive matching
    content_lower = content.lower()
    
    # Patterns to look for
    placeholder_patterns = [
        r'lorem\s+ipsum',
        r'placeholder',
        r'dummy\s+text',
        r'sample\s+text',
        r'example\s+content',
        r'test\s+content',
        r'your\s+content\s+here',
        r'insert\s+text\s+here',
        r'coming\s+soon',
        r'under\s+construction',
        r'dolor\s+sit\s+amet',  # Common lorem ipsum phrase
        r'consectetur\s+adipiscing',  # Another lorem ipsum phrase
    ]
    
    findings = []
    for pattern in placeholder_patterns:
        matches = re.finditer(pattern, content_lower)
        for match in matches:
            # Find the actual text in original content to preserve case
            start = match.start()
            end = match.end()
            actual_text = content[start:end]
            
            # Get context (50 chars before and after)
            context_start = max(0, start - 50)
            context_end = min(len(content), end + 50)
            context = content[context_start:context_end].replace('\n', ' ').strip()
            
            findings.append({
                'text': actual_text,
                'context': context,
                'position': start
            })
    
    return findings

def analyze_h1_structure(content):
    """Analyze H1 tag structure"""
    if not content:
        return {'count': 0, 'h1_tags': [], 'issues': ['No content to analyze']}
    
    # Find all H1 tags (both HTML and Gutenberg blocks)
    h1_patterns = [
        r'<h1[^>]*>(.*?)</h1>',  # HTML H1 tags
        r'<!-- wp:heading {"level":1[^}]*} -->\s*<h1[^>]*>(.*?)</h1>',  # Gutenberg H1
    ]
    
    h1_tags = []
    for pattern in h1_patterns:
        matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
        for match in matches:
            # Clean the H1 content
            h1_content = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            if h1_content:
                h1_tags.append(h1_content)
    
    issues = []
    if len(h1_tags) == 0:
        issues.append('Missing H1 tag')
    elif len(h1_tags) > 1:
        issues.append(f'Multiple H1 tags found ({len(h1_tags)})')
    
    # Check for empty or too short H1s
    for h1 in h1_tags:
        if len(h1) < 10:
            issues.append(f'H1 too short: "{h1}"')
        if len(h1) > 70:
            issues.append(f'H1 too long: "{h1[:70]}..."')
    
    return {
        'count': len(h1_tags),
        'h1_tags': h1_tags,
        'issues': issues
    }

def analyze_seo_meta(page_data):
    """Analyze SEO title and meta description"""
    issues = []
    
    # Get SEO data
    seo_title = page_data.get('yoast_head_json', {}).get('title', '') if page_data.get('yoast_head_json') else ''
    if not seo_title:
        seo_title = page_data.get('title', {}).get('rendered', '') if isinstance(page_data.get('title'), dict) else ''
    
    seo_description = page_data.get('yoast_head_json', {}).get('description', '') if page_data.get('yoast_head_json') else ''
    if not seo_description:
        seo_description = page_data.get('excerpt', {}).get('rendered', '') if isinstance(page_data.get('excerpt'), dict) else ''
    
    # Clean up the values
    if seo_title:
        seo_title = re.sub(r'<[^>]+>', '', seo_title).strip()
    if seo_description:
        seo_description = re.sub(r'<[^>]+>', '', seo_description).strip()
    
    # Check title
    if not seo_title:
        issues.append('Missing SEO title')
    else:
        if len(seo_title) < 30:
            issues.append(f'SEO title too short ({len(seo_title)} chars): "{seo_title}"')
        elif len(seo_title) > 60:
            issues.append(f'SEO title too long ({len(seo_title)} chars): "{seo_title[:60]}..."')
    
    # Check description
    if not seo_description:
        issues.append('Missing meta description')
    else:
        if len(seo_description) < 120:
            issues.append(f'Meta description too short ({len(seo_description)} chars)')
        elif len(seo_description) > 160:
            issues.append(f'Meta description too long ({len(seo_description)} chars)')
    
    return {
        'title': seo_title,
        'title_length': len(seo_title) if seo_title else 0,
        'description': seo_description,
        'description_length': len(seo_description) if seo_description else 0,
        'issues': issues
    }

def main():
    print("🔍 Derek's Content Quality Analysis for derekzar.com")
    print("=" * 60)
    
    # Initialize manager
    manager = WPBulkManagerMySQL()
    
    # Get site info
    site_info = manager.get_site_info('derekzar')
    
    if not site_info or site_info.get('error'):
        print("❌ derekzar.com not found in sites.")
        print("\nPlease run 'python add_derekzar.py' to add the site")
        return
    
    # Get client for API access
    client = manager.get_client('derekzar')
    
    if not client:
        print("❌ Failed to create client for derekzar.com")
        return
    
    # Get the site URL from site details
    site_url = site_info.get('site_url', 'https://derekzar.com')
    print(f"\n📡 Connecting to {site_url}...")
    print("✅ Connected successfully!")
    
    # Get all pages
    print("\n📄 Fetching all pages...")
    try:
        # Try to get all pages, not just published ones
        all_pages = []
        page = 1
        while True:
            batch = client.get_content('pages', params={'per_page': 100, 'page': page, 'status': 'any'})
            if not batch:
                break
            all_pages.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        
        # Filter for published pages
        pages = [p for p in all_pages if p.get('status') == 'publish']
        print(f"Found {len(all_pages)} total pages, {len(pages)} published")
        
        # If no pages, try without status filter
        if not pages:
            pages = client.get_content('pages', params={'per_page': 100})
            print(f"Retrying: Found {len(pages)} pages")
            
    except Exception as e:
        print(f"❌ Error fetching pages: {str(e)}")
        return
    
    # Analyze each page
    all_findings = []
    placeholder_count = 0
    h1_issue_count = 0
    seo_issue_count = 0
    
    print("\n🔍 Analyzing content quality...")
    print("-" * 60)
    
    for page in pages:
        page_id = page.get('id')
        title = page.get('title', {}).get('rendered', 'Untitled') if isinstance(page.get('title'), dict) else str(page.get('title', 'Untitled'))
        link = page.get('link', '')
        status = page.get('status', 'unknown')
        
        # Get content
        content = page.get('content', {}).get('rendered', '') if isinstance(page.get('content'), dict) else str(page.get('content', ''))
        
        # Analyze placeholder text
        placeholder_findings = detect_placeholder_text(content)
        
        # Analyze H1 structure
        h1_analysis = analyze_h1_structure(content)
        
        # Analyze SEO meta
        seo_analysis = analyze_seo_meta(page)
        
        # Compile findings for this page
        page_findings = {
            'id': page_id,
            'title': title,
            'link': link,
            'status': status,
            'placeholder_text': placeholder_findings,
            'h1_analysis': h1_analysis,
            'seo_analysis': seo_analysis,
            'has_issues': bool(placeholder_findings or h1_analysis['issues'] or seo_analysis['issues'])
        }
        
        all_findings.append(page_findings)
        
        # Count issues
        if placeholder_findings:
            placeholder_count += 1
        if h1_analysis['issues']:
            h1_issue_count += 1
        if seo_analysis['issues']:
            seo_issue_count += 1
        
        # Print summary for pages with issues
        if page_findings['has_issues']:
            print(f"\n🚨 Page ID {page_id}: {title}")
            print(f"   URL: {link}")
            
            if placeholder_findings:
                print(f"   ⚠️  Placeholder text found: {len(placeholder_findings)} instance(s)")
                for finding in placeholder_findings[:3]:  # Show first 3
                    print(f"      - \"{finding['text']}\" in: ...{finding['context']}...")
            
            if h1_analysis['issues']:
                print(f"   ⚠️  H1 issues: {', '.join(h1_analysis['issues'])}")
                if h1_analysis['h1_tags']:
                    print(f"      H1 tags: {h1_analysis['h1_tags']}")
            
            if seo_analysis['issues']:
                print(f"   ⚠️  SEO issues: {', '.join(seo_analysis['issues'])}")
                if seo_analysis['title']:
                    print(f"      Title ({seo_analysis['title_length']} chars): {seo_analysis['title']}")
                if seo_analysis['description']:
                    print(f"      Description ({seo_analysis['description_length']} chars): {seo_analysis['description'][:100]}...")
    
    # Generate detailed report
    report = {
        'site': site_url,
        'analysis_date': datetime.now().isoformat(),
        'summary': {
            'total_pages_analyzed': len(pages),
            'pages_with_issues': len([f for f in all_findings if f['has_issues']]),
            'placeholder_text_pages': placeholder_count,
            'h1_issue_pages': h1_issue_count,
            'seo_issue_pages': seo_issue_count
        },
        'findings': all_findings
    }
    
    # Save detailed report
    report_filename = f"derekzar_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 CONTENT QUALITY SUMMARY")
    print("=" * 60)
    print(f"Total pages analyzed: {report['summary']['total_pages_analyzed']}")
    print(f"Pages with issues: {report['summary']['pages_with_issues']}")
    print(f"Pages with placeholder text: {placeholder_count}")
    print(f"Pages with H1 issues: {h1_issue_count}")
    print(f"Pages with SEO issues: {seo_issue_count}")
    print(f"\n📁 Detailed report saved to: {report_filename}")
    
    # Also create a markdown summary
    md_report = f"""# Content Quality Analysis Report - derekzar.com
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Pages Analyzed**: {report['summary']['total_pages_analyzed']}
- **Pages with Issues**: {report['summary']['pages_with_issues']}
- **Pages with Placeholder Text**: {placeholder_count}
- **Pages with H1 Issues**: {h1_issue_count}
- **Pages with SEO Issues**: {seo_issue_count}

## Detailed Findings

"""
    
    for finding in all_findings:
        if finding['has_issues']:
            md_report += f"\n### Page ID {finding['id']}: {finding['title']}\n"
            md_report += f"**URL**: {finding['link']}\n\n"
            
            if finding['placeholder_text']:
                md_report += "**Placeholder Text Found:**\n"
                for ph in finding['placeholder_text'][:5]:
                    md_report += f"- \"{ph['text']}\" in context: ...{ph['context']}...\n"
                md_report += "\n"
            
            if finding['h1_analysis']['issues']:
                md_report += "**H1 Issues:**\n"
                for issue in finding['h1_analysis']['issues']:
                    md_report += f"- {issue}\n"
                if finding['h1_analysis']['h1_tags']:
                    md_report += f"- Found H1 tags: {finding['h1_analysis']['h1_tags']}\n"
                md_report += "\n"
            
            if finding['seo_analysis']['issues']:
                md_report += "**SEO Issues:**\n"
                for issue in finding['seo_analysis']['issues']:
                    md_report += f"- {issue}\n"
                md_report += "\n"
    
    md_filename = f"derekzar_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"📄 Markdown report saved to: {md_filename}")

if __name__ == "__main__":
    main()