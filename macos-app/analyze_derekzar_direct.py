#!/usr/bin/env python3
"""
Direct API content quality analysis for derekzar.com
Checks for:
- Lorem ipsum or placeholder text
- H1 semantic structure
- SEO titles and meta descriptions
"""

import requests
import base64
import json
import re
from datetime import datetime

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
        r'et\s+harum\s+quidem\s+rerum',  # From the post titles I saw
        r'at\s+vero\s+eos\s+et\s+accusamus',  # From the post titles
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
    
    # Get SEO data - check both Yoast and standard fields
    seo_title = ''
    seo_description = ''
    
    # Try Yoast first
    if page_data.get('yoast_head_json'):
        seo_title = page_data['yoast_head_json'].get('title', '')
        seo_description = page_data['yoast_head_json'].get('description', '')
    
    # Fall back to standard fields
    if not seo_title:
        seo_title = page_data.get('title', {}).get('rendered', '')
    
    if not seo_description and page_data.get('excerpt'):
        seo_description = page_data['excerpt'].get('rendered', '')
    
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
    
    # API setup
    api_key = '0b2d82ec91d2d876558ce460e57a7a1e'
    auth_string = base64.b64encode(api_key.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/json'
    }
    
    base_url = 'https://derekzar.com/wp-json/wp/v2'
    
    # Get all pages
    print("\n📄 Fetching all pages...")
    all_pages = []
    page = 1
    
    while True:
        resp = requests.get(f'{base_url}/pages', headers=headers, params={'per_page': 100, 'page': page})
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        all_pages.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    
    print(f"Found {len(all_pages)} pages")
    
    # Also analyze posts for placeholder content
    print("\n📰 Fetching posts...")
    posts = []
    resp = requests.get(f'{base_url}/posts', headers=headers, params={'per_page': 100})
    if resp.status_code == 200:
        posts = resp.json()
        print(f"Found {len(posts)} posts")
    
    # Analyze each page
    all_findings = []
    placeholder_count = 0
    h1_issue_count = 0
    seo_issue_count = 0
    
    print("\n🔍 Analyzing content quality...")
    print("-" * 60)
    
    # Analyze pages
    for page in all_pages:
        page_id = page.get('id')
        title = page.get('title', {}).get('rendered', 'Untitled')
        link = page.get('link', '')
        status = page.get('status', 'unknown')
        
        # Skip if not published
        if status != 'publish':
            continue
        
        # Get content
        content = page.get('content', {}).get('rendered', '')
        
        # Analyze placeholder text
        placeholder_findings = detect_placeholder_text(content)
        
        # Also check title for placeholder text
        title_placeholder = detect_placeholder_text(title)
        placeholder_findings.extend(title_placeholder)
        
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
            'type': 'page',
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
    
    # Also check posts for lorem ipsum content
    print("\n\n📰 Checking posts for placeholder content...")
    posts_with_lorem = 0
    for post in posts:
        post_title = post.get('title', {}).get('rendered', '')
        post_content = post.get('content', {}).get('rendered', '')
        
        # Check for placeholder text
        title_placeholder = detect_placeholder_text(post_title)
        content_placeholder = detect_placeholder_text(post_content)
        
        if title_placeholder or content_placeholder:
            posts_with_lorem += 1
            print(f"\n🚨 Post ID {post['id']}: {post_title}")
            print(f"   URL: {post.get('link', '')}")
            if title_placeholder:
                print("   ⚠️  Lorem ipsum in title")
            if content_placeholder:
                print(f"   ⚠️  Lorem ipsum in content: {len(content_placeholder)} instances")
    
    # Generate detailed report
    report = {
        'site': 'https://derekzar.com',
        'analysis_date': datetime.now().isoformat(),
        'summary': {
            'total_pages_analyzed': len([f for f in all_findings if f['status'] == 'publish']),
            'pages_with_issues': len([f for f in all_findings if f['has_issues']]),
            'placeholder_text_pages': placeholder_count,
            'h1_issue_pages': h1_issue_count,
            'seo_issue_pages': seo_issue_count,
            'posts_analyzed': len(posts),
            'posts_with_lorem': posts_with_lorem
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
    print(f"\nPosts analyzed: {report['summary']['posts_analyzed']}")
    print(f"Posts with lorem ipsum: {report['summary']['posts_with_lorem']}")
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
- **Posts Analyzed**: {report['summary']['posts_analyzed']}
- **Posts with Lorem Ipsum**: {report['summary']['posts_with_lorem']}

## Detailed Findings

### Pages with Issues
"""
    
    for finding in all_findings:
        if finding['has_issues']:
            md_report += f"\n#### Page ID {finding['id']}: {finding['title']}\n"
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
    
    # Add posts section if any have lorem ipsum
    if posts_with_lorem > 0:
        md_report += "\n### Posts with Lorem Ipsum Content\n"
        for post in posts:
            post_title = post.get('title', {}).get('rendered', '')
            title_placeholder = detect_placeholder_text(post_title)
            content_placeholder = detect_placeholder_text(post.get('content', {}).get('rendered', ''))
            
            if title_placeholder or content_placeholder:
                md_report += f"\n#### Post ID {post['id']}: {post_title}\n"
                md_report += f"**URL**: {post.get('link', '')}\n"
                if title_placeholder:
                    md_report += "- Lorem ipsum found in title\n"
                if content_placeholder:
                    md_report += f"- Lorem ipsum found in content ({len(content_placeholder)} instances)\n"
    
    md_filename = f"derekzar_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"📄 Markdown report saved to: {md_filename}")

if __name__ == "__main__":
    main()