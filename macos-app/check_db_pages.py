#!/usr/bin/env python3
"""
Check pages directly in database for semantic analysis
"""

import subprocess
import re
from html import unescape

def analyze_heading_structure(content):
    """Analyze heading structure"""
    issues = []
    
    # Find all headings
    h1_pattern = r'<h1[^>]*class="wp-block-heading"[^>]*>(.*?)</h1>'
    h2_pattern = r'<h2[^>]*class="wp-block-heading"[^>]*>(.*?)</h2>'
    h3_pattern = r'<h3[^>]*class="wp-block-heading"[^>]*>(.*?)</h3>'
    
    h1_matches = re.findall(h1_pattern, content, re.DOTALL | re.IGNORECASE)
    h2_matches = re.findall(h2_pattern, content, re.DOTALL | re.IGNORECASE)
    h3_matches = re.findall(h3_pattern, content, re.DOTALL | re.IGNORECASE)
    
    # Clean heading text
    h1_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h1_matches]
    h2_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h2_matches]
    h3_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h3_matches]
    
    # Check H1 compliance
    if len(h1_clean) == 0:
        issues.append("❌ CRITICAL: No H1 tag found")
    elif len(h1_clean) > 1:
        issues.append(f"❌ CRITICAL: Multiple H1 tags ({len(h1_clean)}) - SEO violation!")
        issues.append(f"   Duplicate H1s: {h1_clean}")
    else:
        issues.append(f"✅ Perfect H1: '{h1_clean[0][:60]}...'")
    
    # Check H2 structure  
    if not h2_clean:
        issues.append("⚠️ No H2 headings - missing content structure")
    else:
        issues.append(f"✅ Good H2 structure: {len(h2_clean)} headings")
    
    # Check hierarchy
    if h3_clean and not h2_clean:
        issues.append("❌ SEMANTIC ERROR: H3 without H2 - improper hierarchy")
    
    return {
        'h1_count': len(h1_clean),
        'h2_count': len(h2_clean), 
        'h3_count': len(h3_clean),
        'h1_list': h1_clean,
        'h2_list': h2_clean,
        'issues': issues
    }

def analyze_seo_content(title, content):
    """Analyze SEO elements"""
    issues = []
    
    # Title analysis
    title_length = len(title)
    if title_length < 30:
        issues.append(f"⚠️ Title too short ({title_length} chars)")
    elif title_length > 60:
        issues.append(f"⚠️ Title too long ({title_length} chars)")
    else:
        issues.append(f"✅ Title length optimal ({title_length} chars)")
    
    # Content analysis
    content_text = re.sub(r'<[^>]+>', '', content)
    word_count = len(content_text.split())
    
    if word_count < 300:
        issues.append(f"❌ Content too thin ({word_count} words)")
    elif word_count < 500:
        issues.append(f"⚠️ Content short ({word_count} words)")
    else:
        issues.append(f"✅ Content sufficient ({word_count} words)")
    
    # Keyword analysis
    keywords = ['accessibility', 'renovation', 'australia', 'australian']
    found_keywords = [kw for kw in keywords if kw.lower() in title.lower()]
    
    if found_keywords:
        issues.append(f"✅ Keywords in title: {', '.join(found_keywords)}")
    else:
        issues.append("⚠️ No target keywords in title")
    
    return {
        'title_length': title_length,
        'word_count': word_count,
        'found_keywords': found_keywords,
        'issues': issues
    }

def check_gutenberg_structure(content):
    """Check Gutenberg blocks"""
    issues = []
    
    block_count = content.count('<!-- wp:')
    close_count = content.count('<!-- /wp:')
    
    if block_count == 0:
        issues.append("⚠️ No Gutenberg blocks")
    elif block_count != close_count:
        issues.append(f"❌ Block structure broken: {block_count} open, {close_count} close")
    else:
        issues.append(f"✅ {block_count} blocks properly structured")
    
    return {
        'block_count': block_count,
        'structure_valid': block_count == close_count,
        'issues': issues
    }

def execute_ssh_command(command):
    """Execute SSH command"""
    ssh_cmd = f'sshpass -p "56tbztc2cRZ8" ssh -o StrictHostKeyChecking=no master_ntuqvnephb@170.64.179.157 "{command}"'
    try:
        result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return "", str(e)

def check_database_pages():
    """Check pages directly in database"""
    print("🏠 RENO WARRIORS ACCESSIBILITY PAGES - DATABASE REVIEW")
    print("📊 Direct Database Semantic Structure & SEO Analysis")
    print("=" * 70)
    
    page_ids = [7556, 7557, 7558, 7559, 7560]
    page_names = {
        7556: "Bathroom Accessibility Renovation",
        7557: "Kitchen Accessibility Renovation", 
        7558: "Laundry Accessibility Renovation",
        7559: "Home Accessibility Design & Planning",
        7560: "European Accessible Hardware & Fixtures"
    }
    
    results = []
    
    for page_id in page_ids:
        print(f"\n📄 ANALYZING PAGE {page_id}: {page_names.get(page_id)}")
        print("-" * 60)
        
        # Get page from database
        query = f"SELECT ID, post_title, post_content, post_status FROM wpjk_posts WHERE ID = {page_id};"
        mysql_cmd = f"mysql -h localhost -P 3307 -u cfhbaxywhg -p7Sy28jzV25 cfhbaxywhg -e '{query}'"
        
        stdout, stderr = execute_ssh_command(mysql_cmd)
        
        if stderr and "Warning: Permanently added" not in stderr:
            print(f"❌ Database error: {stderr}")
            continue
        
        if not stdout or "Empty set" in stdout:
            print(f"❌ Page {page_id} not found in database")
            continue
        
        # Parse the output
        lines = stdout.split('\n')
        if len(lines) < 2:
            print(f"❌ No data returned for page {page_id}")
            continue
        
        # Skip header line, get data
        data_line = lines[1] if len(lines) > 1 else ""
        if not data_line:
            print(f"❌ No data in response for page {page_id}")
            continue
        
        # Split by tabs (MySQL output format)
        parts = data_line.split('\t')
        if len(parts) < 4:
            print(f"❌ Incomplete data for page {page_id}")
            continue
        
        page_id_db = parts[0]
        title = parts[1]
        content = parts[2]
        status = parts[3]
        
        print(f"✅ Page found in database")
        print(f"📝 Title: {title}")
        print(f"📊 Status: {status}")
        print(f"📄 Content length: {len(content)} characters")
        
        # Analyze heading structure
        print("\n🔤 HEADING STRUCTURE ANALYSIS:")
        heading_analysis = analyze_heading_structure(content)
        for issue in heading_analysis['issues']:
            print(f"   {issue}")
        
        if heading_analysis['h2_list']:
            print(f"\n   📋 H2 Headings ({len(heading_analysis['h2_list'])}):")
            for i, h2 in enumerate(heading_analysis['h2_list'][:5], 1):  # Show first 5
                print(f"      {i}. {h2[:60]}...")
        
        # SEO Analysis
        print("\n🔍 SEO ANALYSIS:")
        seo_analysis = analyze_seo_content(title, content)
        for issue in seo_analysis['issues']:
            print(f"   {issue}")
        
        # Gutenberg Analysis
        print("\n🧱 GUTENBERG STRUCTURE:")
        gutenberg_analysis = check_gutenberg_structure(content)
        for issue in gutenberg_analysis['issues']:
            print(f"   {issue}")
        
        # Overall Assessment
        critical_issues = len([i for i in heading_analysis['issues'] + seo_analysis['issues'] + gutenberg_analysis['issues'] if i.startswith('❌')])
        warning_issues = len([i for i in heading_analysis['issues'] + seo_analysis['issues'] + gutenberg_analysis['issues'] if i.startswith('⚠️')])
        
        if critical_issues == 0 and warning_issues == 0:
            overall = "🎉 EXCELLENT"
        elif critical_issues == 0 and warning_issues <= 2:
            overall = f"👍 GOOD ({warning_issues} minor issues)"
        elif critical_issues == 0:
            overall = f"⚠️ NEEDS IMPROVEMENT ({warning_issues} issues)"
        else:
            overall = f"❌ CRITICAL ISSUES ({critical_issues} critical, {warning_issues} warnings)"
        
        print(f"\n📊 OVERALL: {overall}")
        
        results.append({
            'page_id': page_id,
            'title': title,
            'status': status,
            'heading_analysis': heading_analysis,
            'seo_analysis': seo_analysis,
            'gutenberg_analysis': gutenberg_analysis,
            'critical_issues': critical_issues,
            'warning_issues': warning_issues,
            'overall': overall
        })
    
    # Generate Summary Report
    if results:
        print("\n" + "=" * 70)
        print("📋 COMPREHENSIVE SUMMARY REPORT")
        print("=" * 70)
        
        total_pages = len(results)
        excellent = len([r for r in results if "EXCELLENT" in r['overall']])
        good = len([r for r in results if "GOOD" in r['overall']])
        needs_improvement = len([r for r in results if "NEEDS IMPROVEMENT" in r['overall']])
        critical = len([r for r in results if "CRITICAL" in r['overall']])
        
        print(f"\n📊 OVERALL STATUS:")
        print(f"   Total pages analyzed: {total_pages}")
        print(f"   🎉 Excellent: {excellent}")
        print(f"   👍 Good: {good}")
        print(f"   ⚠️ Needs improvement: {needs_improvement}")
        print(f"   ❌ Critical issues: {critical}")
        
        # H1 Issues Summary
        duplicate_h1_pages = [r for r in results if r['heading_analysis']['h1_count'] > 1]
        missing_h1_pages = [r for r in results if r['heading_analysis']['h1_count'] == 0]
        
        print(f"\n🔤 H1 STRUCTURE ISSUES:")
        if duplicate_h1_pages:
            print(f"   ❌ CRITICAL: {len(duplicate_h1_pages)} pages with DUPLICATE H1s:")
            for r in duplicate_h1_pages:
                print(f"      - {r['title']}: {r['heading_analysis']['h1_count']} H1s")
        
        if missing_h1_pages:
            print(f"   ❌ CRITICAL: {len(missing_h1_pages)} pages MISSING H1:")
            for r in missing_h1_pages:
                print(f"      - {r['title']}")
        
        if not duplicate_h1_pages and not missing_h1_pages:
            print("   ✅ ALL PAGES: Perfect H1 structure!")
        
        # SEO Issues Summary
        title_issues = [r for r in results if r['seo_analysis']['title_length'] < 30 or r['seo_analysis']['title_length'] > 60]
        content_issues = [r for r in results if r['seo_analysis']['word_count'] < 300]
        
        print(f"\n🔍 SEO ISSUES:")
        if title_issues:
            print(f"   ⚠️ {len(title_issues)} pages with title length issues:")
            for r in title_issues:
                print(f"      - {r['title']}: {r['seo_analysis']['title_length']} chars")
        
        if content_issues:
            print(f"   ❌ {len(content_issues)} pages with thin content:")
            for r in content_issues:
                print(f"      - {r['title']}: {r['seo_analysis']['word_count']} words")
        
        if not title_issues and not content_issues:
            print("   ✅ ALL PAGES: Meet SEO requirements!")
        
        # Final Recommendations
        print(f"\n💡 FINAL RECOMMENDATIONS:")
        if excellent == total_pages:
            print("   🎉 ALL PAGES EXCELLENT! Ready to publish immediately!")
        else:
            print("   🔧 URGENT FIXES NEEDED:")
            if duplicate_h1_pages:
                print("      1. 🚨 Fix duplicate H1s (critical SEO issue)")
            if missing_h1_pages:
                print("      2. 🚨 Add missing H1 tags")
            if content_issues:
                print("      3. Expand thin content (aim for 500+ words)")
            if title_issues:
                print("      4. Optimize title lengths (50-60 chars)")
            
            print("\n   📈 SEO IMPROVEMENTS:")
            print("      - Add meta descriptions")
            print("      - Include more internal links")
            print("      - Add FAQ sections")
            print("      - Consider adding schema markup")
        
        print(f"\n✅ REVIEW COMPLETE: {total_pages} pages analyzed from database")
    
    else:
        print("\n❌ No pages found in database")

if __name__ == "__main__":
    check_database_pages()