#!/usr/bin/env python3
"""
Manual review using direct API calls
"""

import requests
import re
from html import unescape

def manual_review():
    print("🏠 RENO WARRIORS ACCESSIBILITY PAGES REVIEW")
    print("📊 Manual Semantic Structure & SEO Analysis")
    print("=" * 60)
    
    # Direct API access
    base_url = "https://renowarriors.com.au/wp-json/wpbm/v1"
    api_key = "0ab365b5b83f46b65bf12466c404bfd3"
    headers = {"X-API-Key": api_key}
    
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
        print("-" * 50)
        
        try:
            # Get page via our plugin API
            response = requests.get(f"{base_url}/content/{page_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and data.get('data'):
                    page_data = data['data']
                    
                    title = page_data.get('title', '')
                    content = page_data.get('content', '')
                    status = page_data.get('status', 'unknown')
                    
                    print(f"✅ Page found (Status: {status})")
                    print(f"📝 Title: {title}")
                    
                    # Analyze heading structure
                    print("\n🔤 HEADING STRUCTURE:")
                    
                    # Count headings
                    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
                    h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL | re.IGNORECASE)
                    h3_matches = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL | re.IGNORECASE)
                    
                    h1_count = len(h1_matches)
                    h2_count = len(h2_matches)
                    h3_count = len(h3_matches)
                    
                    print(f"   H1 tags: {h1_count}")
                    print(f"   H2 tags: {h2_count}")
                    print(f"   H3 tags: {h3_count}")
                    
                    # Check H1 compliance
                    if h1_count == 0:
                        print("   ❌ CRITICAL: No H1 tag found!")
                        h1_status = "MISSING"
                    elif h1_count > 1:
                        print(f"   ❌ CRITICAL: Multiple H1 tags ({h1_count}) - SEO issue!")
                        h1_status = "DUPLICATE"
                        
                        # Show the duplicate H1s
                        print("   📋 H1 tags found:")
                        for i, h1 in enumerate(h1_matches, 1):
                            clean_h1 = unescape(re.sub(r'<[^>]+>', '', h1)).strip()
                            print(f"      {i}. {clean_h1}")
                    else:
                        clean_h1 = unescape(re.sub(r'<[^>]+>', '', h1_matches[0])).strip()
                        print(f"   ✅ Perfect: Single H1 found")
                        print(f"   📋 H1: {clean_h1}")
                        h1_status = "PERFECT"
                    
                    # Check heading hierarchy
                    if h3_count > 0 and h2_count == 0:
                        print("   ❌ SEMANTIC ERROR: H3 without H2 - improper hierarchy")
                        hierarchy_status = "BROKEN"
                    else:
                        print("   ✅ Heading hierarchy is correct")
                        hierarchy_status = "CORRECT"
                    
                    # SEO Analysis
                    print("\n🔍 SEO ANALYSIS:")
                    
                    title_length = len(title)
                    if title_length < 30:
                        print(f"   ⚠️ Title too short ({title_length} chars) - aim for 50-60")
                        title_status = "TOO_SHORT"
                    elif title_length > 60:
                        print(f"   ⚠️ Title too long ({title_length} chars) - may be truncated")
                        title_status = "TOO_LONG"
                    else:
                        print(f"   ✅ Title length optimal ({title_length} chars)")
                        title_status = "OPTIMAL"
                    
                    # Content analysis
                    content_text = re.sub(r'<[^>]+>', '', content)
                    word_count = len(content_text.split())
                    
                    if word_count < 300:
                        print(f"   ❌ Content too thin ({word_count} words) - need 500+ for SEO")
                        content_status = "TOO_THIN"
                    elif word_count < 500:
                        print(f"   ⚠️ Content short ({word_count} words) - could be longer")
                        content_status = "SHORT"
                    else:
                        print(f"   ✅ Content length excellent ({word_count} words)")
                        content_status = "EXCELLENT"
                    
                    # Keyword analysis
                    keywords_in_title = []
                    if 'accessibility' in title.lower():
                        keywords_in_title.append('accessibility')
                    if 'renovation' in title.lower():
                        keywords_in_title.append('renovation')
                    if 'australia' in title.lower() or 'australian' in title.lower():
                        keywords_in_title.append('location')
                    
                    if keywords_in_title:
                        print(f"   ✅ Target keywords in title: {', '.join(keywords_in_title)}")
                        keyword_status = "GOOD"
                    else:
                        print("   ⚠️ Missing target keywords in title")
                        keyword_status = "MISSING"
                    
                    # Check for CTAs
                    cta_words = ['consultation', 'contact', 'call', 'phone', 'book', 'free']
                    ctas_found = [word for word in cta_words if word in content.lower()]
                    
                    if ctas_found:
                        print(f"   ✅ Call-to-actions present: {', '.join(ctas_found)}")
                        cta_status = "PRESENT"
                    else:
                        print("   ⚠️ No clear call-to-actions found")
                        cta_status = "MISSING"
                    
                    # Gutenberg blocks analysis
                    print("\n🧱 GUTENBERG STRUCTURE:")
                    block_count = content.count('<!-- wp:')
                    close_count = content.count('<!-- /wp:')
                    
                    if block_count == 0:
                        print("   ⚠️ No Gutenberg blocks detected")
                        gutenberg_status = "NO_BLOCKS"
                    elif block_count != close_count:
                        print(f"   ❌ Block structure broken: {block_count} open, {close_count} close")
                        gutenberg_status = "BROKEN"
                    else:
                        print(f"   ✅ {block_count} Gutenberg blocks properly structured")
                        gutenberg_status = "GOOD"
                    
                    # Overall assessment
                    print("\n📊 OVERALL ASSESSMENT:")
                    
                    critical_issues = 0
                    if h1_status in ["MISSING", "DUPLICATE"]:
                        critical_issues += 1
                    if hierarchy_status == "BROKEN":
                        critical_issues += 1
                    if content_status == "TOO_THIN":
                        critical_issues += 1
                    if gutenberg_status == "BROKEN":
                        critical_issues += 1
                    
                    warning_issues = 0
                    if title_status in ["TOO_SHORT", "TOO_LONG"]:
                        warning_issues += 1
                    if content_status == "SHORT":
                        warning_issues += 1
                    if keyword_status == "MISSING":
                        warning_issues += 1
                    if cta_status == "MISSING":
                        warning_issues += 1
                    
                    if critical_issues == 0 and warning_issues == 0:
                        print("   🎉 EXCELLENT - Ready to publish!")
                        overall_score = "EXCELLENT"
                    elif critical_issues == 0 and warning_issues <= 2:
                        print(f"   👍 GOOD - {warning_issues} minor improvements possible")
                        overall_score = "GOOD"
                    elif critical_issues == 0:
                        print(f"   ⚠️ NEEDS IMPROVEMENT - {warning_issues} issues to address")
                        overall_score = "NEEDS_IMPROVEMENT"
                    else:
                        print(f"   ❌ CRITICAL ISSUES - {critical_issues} critical, {warning_issues} warnings")
                        overall_score = "CRITICAL"
                    
                    results.append({
                        'page_id': page_id,
                        'title': title,
                        'h1_status': h1_status,
                        'hierarchy_status': hierarchy_status,
                        'title_status': title_status,
                        'content_status': content_status,
                        'keyword_status': keyword_status,
                        'cta_status': cta_status,
                        'gutenberg_status': gutenberg_status,
                        'overall_score': overall_score,
                        'critical_issues': critical_issues,
                        'warning_issues': warning_issues,
                        'word_count': word_count,
                        'title_length': title_length
                    })
                    
                else:
                    print(f"❌ No data returned for page {page_id}")
            
            elif response.status_code == 404:
                print(f"❌ Page {page_id} not found (404)")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error analyzing page {page_id}: {str(e)}")
    
    # Generate summary report
    if results:
        print("\n" + "=" * 60)
        print("📋 SUMMARY REPORT")
        print("=" * 60)
        
        total_pages = len(results)
        excellent = len([r for r in results if r['overall_score'] == 'EXCELLENT'])
        good = len([r for r in results if r['overall_score'] == 'GOOD'])
        needs_improvement = len([r for r in results if r['overall_score'] == 'NEEDS_IMPROVEMENT'])
        critical = len([r for r in results if r['overall_score'] == 'CRITICAL'])
        
        print(f"\n📊 OVERALL STATUS:")
        print(f"   Total pages: {total_pages}")
        print(f"   🎉 Excellent: {excellent}")
        print(f"   👍 Good: {good}")
        print(f"   ⚠️ Needs improvement: {needs_improvement}")
        print(f"   ❌ Critical issues: {critical}")
        
        # H1 issues summary
        duplicate_h1s = [r for r in results if r['h1_status'] == 'DUPLICATE']
        missing_h1s = [r for r in results if r['h1_status'] == 'MISSING']
        
        print(f"\n🔤 H1 STRUCTURE ISSUES:")
        if duplicate_h1s:
            print(f"   ❌ CRITICAL: {len(duplicate_h1s)} pages with duplicate H1s:")
            for r in duplicate_h1s:
                print(f"      - {r['title']}")
        
        if missing_h1s:
            print(f"   ❌ CRITICAL: {len(missing_h1s)} pages missing H1:")
            for r in missing_h1s:
                print(f"      - {r['title']}")
        
        if not duplicate_h1s and not missing_h1s:
            print("   ✅ All pages have perfect H1 structure")
        
        # SEO issues summary
        title_issues = [r for r in results if r['title_status'] in ['TOO_SHORT', 'TOO_LONG']]
        content_issues = [r for r in results if r['content_status'] in ['TOO_THIN', 'SHORT']]
        
        print(f"\n🔍 SEO ISSUES:")
        if title_issues:
            print(f"   ⚠️ {len(title_issues)} pages with title length issues:")
            for r in title_issues:
                print(f"      - {r['title']}: {r['title_length']} chars")
        
        if content_issues:
            print(f"   ⚠️ {len(content_issues)} pages with content length issues:")
            for r in content_issues:
                print(f"      - {r['title']}: {r['word_count']} words")
        
        if not title_issues and not content_issues:
            print("   ✅ All pages meet SEO requirements")
        
        # Final recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if excellent == total_pages:
            print("   🎉 ALL PAGES EXCELLENT! Ready to publish!")
        else:
            print("   🔧 Priority fixes needed:")
            if duplicate_h1s:
                print("      1. 🚨 URGENT: Fix duplicate H1s (critical SEO issue)")
            if missing_h1s:
                print("      2. 🚨 URGENT: Add missing H1s")
            if content_issues:
                print("      3. Expand content (aim for 500+ words)")
            if title_issues:
                print("      4. Optimize title lengths (50-60 chars)")
        
        print(f"\n✅ Review completed: {total_pages} pages analyzed")
    
    else:
        print("\n❌ No pages could be analyzed")

if __name__ == "__main__":
    manual_review()