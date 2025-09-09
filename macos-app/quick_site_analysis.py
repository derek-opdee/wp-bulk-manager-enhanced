#!/usr/bin/env python3
"""
Quick site analysis for key Reno Warriors pages
"""

import subprocess
import re
from html import unescape

def execute_query(query):
    """Execute MySQL query"""
    ssh_cmd = f'sshpass -p "56tbztc2cRZ8" ssh -o StrictHostKeyChecking=no master_ntuqvnephb@170.64.179.157 "mysql -h localhost -P 3307 -u cfhbaxywhg -p7Sy28jzV25 cfhbaxywhg -e \\"{query}\\""'
    try:
        result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_h1_structure(content, title):
    """Analyze H1 structure"""
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    h1_count = len(h1_matches)
    
    if h1_count == 0:
        return "❌ CRITICAL: No H1 tag found"
    elif h1_count > 1:
        clean_h1s = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h1_matches]
        return f"❌ CRITICAL: {h1_count} H1 tags found - DUPLICATE H1s: {clean_h1s}"
    else:
        clean_h1 = unescape(re.sub(r'<[^>]+>', '', h1_matches[0])).strip()
        return f"✅ Perfect H1: '{clean_h1[:60]}...'"

def analyze_content_basics(title, content):
    """Basic content analysis"""
    issues = []
    
    # Title length
    title_length = len(title)
    if title_length < 30:
        issues.append(f"⚠️ Title short ({title_length} chars)")
    elif title_length > 60:
        issues.append(f"⚠️ Title long ({title_length} chars)")
    else:
        issues.append(f"✅ Title optimal ({title_length} chars)")
    
    # Content length
    content_text = re.sub(r'<[^>]+>', '', content)
    word_count = len(content_text.split())
    
    if word_count < 100:
        issues.append(f"❌ Extremely thin content ({word_count} words)")
    elif word_count < 300:
        issues.append(f"⚠️ Thin content ({word_count} words)")
    else:
        issues.append(f"✅ Content sufficient ({word_count} words)")
    
    # H2 structure
    h2_count = len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE))
    if h2_count == 0:
        issues.append("⚠️ No H2 headings")
    else:
        issues.append(f"✅ {h2_count} H2 headings")
    
    return issues

def quick_site_analysis():
    """Quick analysis of key Reno Warriors pages"""
    print("🏠 RENO WARRIORS QUICK SITE ANALYSIS")
    print("📊 SEO & Semantic Structure Review")
    print("=" * 60)
    
    # Get key pages
    print("📋 Fetching key pages...")
    
    pages_query = """SELECT ID, post_title, post_status, post_type, LENGTH(post_content) as content_length 
                    FROM wpjk_posts 
                    WHERE post_type IN ('page', 'post') 
                    AND post_status IN ('publish', 'draft') 
                    AND post_title NOT LIKE '%Auto Draft%' 
                    ORDER BY post_type, ID 
                    LIMIT 15;"""
    
    result = execute_query(pages_query)
    lines = result.split('\n')
    
    if len(lines) < 2:
        print("❌ No pages found")
        return
    
    pages = []
    for line in lines[1:]:  # Skip header
        if line.strip():
            parts = line.split('\t')
            if len(parts) >= 5:
                pages.append({
                    'id': parts[0],
                    'title': parts[1],
                    'status': parts[2],
                    'type': parts[3],
                    'content_length': parts[4]
                })
    
    print(f"✅ Found {len(pages)} pages to analyze")
    
    critical_h1_issues = []
    seo_issues = []
    
    # Analyze each page
    for i, page in enumerate(pages, 1):
        page_id = page['id']
        title = page['title']
        status = page['status']
        page_type = page['type']
        
        print(f"\n[{i}] 📄 {page_type.upper()} {page_id}: {title}")
        print(f"    Status: {status} | Content: {page['content_length']} chars")
        
        # Get content for this page
        content_query = f"SELECT post_content FROM wpjk_posts WHERE ID = {page_id};"
        content_result = execute_query(content_query)
        
        content_lines = content_result.split('\n')
        if len(content_lines) > 1:
            content = content_lines[1]
        else:
            content = ""
        
        if not content or content == 'NULL':
            print("    ⚠️ No content found")
            continue
        
        # H1 Analysis
        h1_analysis = analyze_h1_structure(content, title)
        print(f"    🔤 H1: {h1_analysis}")
        
        if "CRITICAL" in h1_analysis:
            critical_h1_issues.append(f"ID {page_id}: {title}")
        
        # Basic content analysis
        content_issues = analyze_content_basics(title, content)
        for issue in content_issues:
            print(f"    📊 {issue}")
            
            if "❌" in issue:
                seo_issues.append(f"ID {page_id}: {title} - {issue}")
    
    # Summary Report
    print("\n" + "=" * 60)
    print("📊 QUICK ANALYSIS SUMMARY")
    print("=" * 60)
    
    total_pages = len(pages)
    
    print(f"\n📈 OVERVIEW:")
    print(f"   Total pages analyzed: {total_pages}")
    print(f"   Critical H1 issues: {len(critical_h1_issues)}")
    print(f"   SEO issues: {len(seo_issues)}")
    
    # H1 Issues Detail
    if critical_h1_issues:
        print(f"\n❌ CRITICAL H1 ISSUES ({len(critical_h1_issues)} pages):")
        for issue in critical_h1_issues:
            print(f"   - {issue}")
    else:
        print(f"\n✅ H1 STRUCTURE: All analyzed pages have proper H1 structure!")
    
    # SEO Issues Detail
    if seo_issues:
        print(f"\n⚠️ SEO ISSUES FOUND ({len(seo_issues)}):")
        for issue in seo_issues[:10]:  # Show first 10
            print(f"   - {issue}")
        if len(seo_issues) > 10:
            print(f"   ... and {len(seo_issues) - 10} more issues")
    else:
        print(f"\n✅ SEO: No critical SEO issues found!")
    
    # Page Type Breakdown
    print(f"\n📄 PAGE TYPE BREAKDOWN:")
    page_types = {}
    for page in pages:
        page_type = page['type']
        if page_type not in page_types:
            page_types[page_type] = 0
        page_types[page_type] += 1
    
    for page_type, count in page_types.items():
        print(f"   {page_type.upper()}: {count} pages")
    
    # Recommendations
    print(f"\n💡 KEY RECOMMENDATIONS:")
    
    if critical_h1_issues:
        print("   🚨 URGENT: Fix H1 structure issues (critical for SEO)")
        print("      - Ensure each page has exactly one H1 tag")
        print("      - Remove duplicate H1s")
    
    if seo_issues:
        print("   📈 SEO Improvements needed:")
        print("      - Expand thin content (aim for 500+ words)")
        print("      - Optimize title lengths (50-60 characters)")
        print("      - Add H2 headings for better structure")
    
    if not critical_h1_issues and not seo_issues:
        print("   🎉 Excellent! No critical issues found in analyzed pages.")
        print("   📊 Consider adding:")
        print("      - Meta descriptions to all pages")
        print("      - More internal links between pages")
        print("      - Schema markup for local business")
    
    # Health Score
    issues_count = len(critical_h1_issues) + len(seo_issues)
    health_score = max(0, 100 - (issues_count / total_pages * 20))
    
    print(f"\n🏆 SITE HEALTH SCORE: {health_score:.1f}%")
    
    if health_score >= 90:
        print("   🎉 EXCELLENT - Site structure is in great shape!")
    elif health_score >= 75:
        print("   👍 GOOD - Minor improvements will help")
    elif health_score >= 60:
        print("   ⚠️ NEEDS WORK - Several issues to address")
    else:
        print("   ❌ CRITICAL - Major improvements needed")
    
    print(f"\n✅ Quick analysis complete!")
    print(f"📊 Analyzed {total_pages} key pages")

if __name__ == "__main__":
    quick_site_analysis()