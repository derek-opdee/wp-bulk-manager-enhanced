#!/usr/bin/env python3
"""
Direct page review using WordPress REST API
"""

import requests
import re
from html import unescape

class DirectPageReviewer:
    def __init__(self):
        self.base_url = "https://renowarriors.com.au/wp-json/wp/v2"
        self.api_key = "0ab365b5b83f46b65bf12466c404bfd3"
        self.headers = {"X-API-Key": self.api_key}
        self.page_ids = [7556, 7557, 7558, 7559, 7560]
        self.page_titles = {
            7556: "Bathroom Accessibility Renovation",
            7557: "Kitchen Accessibility Renovation", 
            7558: "Laundry Accessibility Renovation",
            7559: "Home Accessibility Design & Planning",
            7560: "European Accessible Hardware & Fixtures"
        }
    
    def get_page_data(self, page_id):
        """Get page data from WordPress API"""
        try:
            response = requests.get(f"{self.base_url}/pages/{page_id}", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get page {page_id}: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error fetching page {page_id}: {str(e)}")
            return None
    
    def analyze_heading_structure(self, content):
        """Analyze heading structure"""
        issues = []
        
        # Find all headings with proper regex
        h1_pattern = r'<h1[^>]*?class="wp-block-heading"[^>]*>(.*?)</h1>'
        h2_pattern = r'<h2[^>]*?class="wp-block-heading"[^>]*>(.*?)</h2>'
        h3_pattern = r'<h3[^>]*?class="wp-block-heading"[^>]*>(.*?)</h3>'
        
        h1_matches = re.findall(h1_pattern, content, re.DOTALL | re.IGNORECASE)
        h2_matches = re.findall(h2_pattern, content, re.DOTALL | re.IGNORECASE)
        h3_matches = re.findall(h3_pattern, content, re.DOTALL | re.IGNORECASE)
        
        # Clean heading text
        h1_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h1_matches]
        h2_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h2_matches]
        h3_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h3_matches]
        
        # Check H1 count
        if len(h1_clean) == 0:
            issues.append("❌ No H1 tag found")
        elif len(h1_clean) > 1:
            issues.append(f"❌ Multiple H1 tags ({len(h1_clean)})")
        else:
            issues.append(f"✅ Single H1: '{h1_clean[0][:50]}...'")
        
        # Check H2 structure
        if not h2_clean:
            issues.append("⚠️ No H2 headings found")
        else:
            issues.append(f"✅ {len(h2_clean)} H2 headings found")
        
        # Check hierarchy
        if h3_clean and not h2_clean:
            issues.append("❌ H3 without H2 - improper hierarchy")
        
        return {
            'h1': h1_clean,
            'h2': h2_clean,
            'h3': h3_clean,
            'issues': issues
        }
    
    def analyze_seo_elements(self, page_data):
        """Analyze SEO elements"""
        seo_issues = []
        
        title = page_data.get('title', {}).get('rendered', '') if isinstance(page_data.get('title'), dict) else str(page_data.get('title', ''))
        content = page_data.get('content', {}).get('rendered', '') if isinstance(page_data.get('content'), dict) else str(page_data.get('content', ''))
        
        # Title analysis
        title_length = len(title)
        if title_length < 30:
            seo_issues.append(f"⚠️ Title too short ({title_length} chars)")
        elif title_length > 60:
            seo_issues.append(f"⚠️ Title too long ({title_length} chars)")
        else:
            seo_issues.append(f"✅ Title length optimal ({title_length} chars)")
        
        # Content length
        content_text = re.sub(r'<[^>]+>', '', content)
        word_count = len(content_text.split())
        if word_count < 300:
            seo_issues.append(f"⚠️ Content short ({word_count} words)")
        else:
            seo_issues.append(f"✅ Content sufficient ({word_count} words)")
        
        # Keyword analysis
        if 'accessibility' in title.lower():
            seo_issues.append("✅ Target keyword in title")
        else:
            seo_issues.append("⚠️ Missing 'accessibility' in title")
        
        if 'australia' in title.lower() or 'australian' in title.lower():
            seo_issues.append("✅ Location targeting in title")
        else:
            seo_issues.append("⚠️ No location targeting in title")
        
        # Check for call-to-actions
        if 'consultation' in content.lower() or 'contact' in content.lower():
            seo_issues.append("✅ Call-to-action present")
        else:
            seo_issues.append("⚠️ No clear call-to-action")
        
        return {
            'title': title,
            'title_length': title_length,
            'word_count': word_count,
            'issues': seo_issues
        }
    
    def check_gutenberg_blocks(self, content):
        """Check Gutenberg block structure"""
        issues = []
        
        # Count blocks
        block_count = content.count('<!-- wp:')
        close_count = content.count('<!-- /wp:')
        
        if block_count == 0:
            issues.append("⚠️ No Gutenberg blocks detected")
        else:
            issues.append(f"✅ {block_count} Gutenberg blocks found")
        
        if block_count != close_count:
            issues.append(f"❌ Block mismatch: {block_count} open, {close_count} close")
        else:
            issues.append("✅ All blocks properly closed")
        
        # Check for specific blocks
        if '<!-- wp:heading' in content:
            issues.append("✅ Heading blocks present")
        else:
            issues.append("⚠️ No heading blocks found")
        
        if '<!-- wp:buttons' in content:
            issues.append("✅ Button blocks present")
        else:
            issues.append("⚠️ No button/CTA blocks")
        
        return {
            'block_count': block_count,
            'issues': issues
        }
    
    def review_page(self, page_id):
        """Review a single page"""
        print(f"\n📄 PAGE {page_id}: {self.page_titles.get(page_id, 'Unknown')}")
        print("-" * 60)
        
        page_data = self.get_page_data(page_id)
        if not page_data:
            return None
        
        content = page_data.get('content', {}).get('rendered', '') if isinstance(page_data.get('content'), dict) else str(page_data.get('content', ''))
        
        # Heading analysis
        print("🔤 HEADING STRUCTURE:")
        heading_analysis = self.analyze_heading_structure(content)
        for issue in heading_analysis['issues']:
            print(f"   {issue}")
        
        # SEO analysis
        print("\n🔍 SEO ANALYSIS:")
        seo_analysis = self.analyze_seo_elements(page_data)
        for issue in seo_analysis['issues']:
            print(f"   {issue}")
        
        # Gutenberg analysis
        print("\n🧱 GUTENBERG BLOCKS:")
        gutenberg_analysis = self.check_gutenberg_blocks(content)
        for issue in gutenberg_analysis['issues']:
            print(f"   {issue}")
        
        # Count issues
        issue_count = 0
        for analysis in [heading_analysis, seo_analysis, gutenberg_analysis]:
            issue_count += len([i for i in analysis['issues'] if i.startswith('❌') or i.startswith('⚠️')])
        
        if issue_count == 0:
            print("\n🎉 EXCELLENT - No issues!")
        elif issue_count <= 2:
            print(f"\n👍 GOOD - {issue_count} minor issues")
        else:
            print(f"\n⚠️ NEEDS WORK - {issue_count} issues")
        
        return {
            'page_id': page_id,
            'title': self.page_titles.get(page_id),
            'heading_analysis': heading_analysis,
            'seo_analysis': seo_analysis,
            'gutenberg_analysis': gutenberg_analysis,
            'issue_count': issue_count
        }
    
    def review_all_pages(self):
        """Review all accessibility pages"""
        print("🏠 RENO WARRIORS ACCESSIBILITY PAGES - STRUCTURE & SEO REVIEW")
        print("=" * 70)
        
        results = []
        
        for page_id in self.page_ids:
            result = self.review_page(page_id)
            if result:
                results.append(result)
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 SUMMARY REPORT")
        print("=" * 70)
        
        if not results:
            print("❌ No pages could be analyzed")
            return
        
        total_pages = len(results)
        excellent_pages = len([r for r in results if r['issue_count'] == 0])
        needs_work = len([r for r in results if r['issue_count'] > 2])
        
        print(f"\n📈 OVERVIEW:")
        print(f"   Total pages: {total_pages}")
        print(f"   Excellent: {excellent_pages}")
        print(f"   Good: {total_pages - excellent_pages - needs_work}")
        print(f"   Needs work: {needs_work}")
        
        # H1 analysis
        print(f"\n🔤 H1 STRUCTURE:")
        h1_issues = []
        for result in results:
            h1_count = len(result['heading_analysis']['h1'])
            if h1_count != 1:
                h1_issues.append(f"{result['title']}: {h1_count} H1s")
        
        if not h1_issues:
            print("   ✅ All pages have exactly one H1")
        else:
            print("   ❌ H1 issues found:")
            for issue in h1_issues:
                print(f"      - {issue}")
        
        # SEO summary
        print(f"\n🔍 SEO SUMMARY:")
        title_issues = []
        content_issues = []
        
        for result in results:
            if result['seo_analysis']['title_length'] < 30 or result['seo_analysis']['title_length'] > 60:
                title_issues.append(f"{result['title']}: {result['seo_analysis']['title_length']} chars")
            
            if result['seo_analysis']['word_count'] < 300:
                content_issues.append(f"{result['title']}: {result['seo_analysis']['word_count']} words")
        
        if not title_issues:
            print("   ✅ All titles optimal length")
        else:
            print("   ⚠️ Title length issues:")
            for issue in title_issues:
                print(f"      - {issue}")
        
        if not content_issues:
            print("   ✅ All content sufficient length")
        else:
            print("   ⚠️ Content length issues:")
            for issue in content_issues:
                print(f"      - {issue}")
        
        print(f"\n📋 RECOMMENDATIONS:")
        if excellent_pages == total_pages:
            print("   🎉 All pages excellent! Ready to publish!")
        else:
            print("   🔧 Improvements needed:")
            if h1_issues:
                print("      1. Fix H1 structure issues")
            if title_issues:
                print("      2. Optimize title lengths (50-60 chars)")
            if content_issues:
                print("      3. Expand content (aim for 500+ words)")
            print("      4. Add meta descriptions")
            print("      5. Include more internal links")
        
        return results

if __name__ == "__main__":
    reviewer = DirectPageReviewer()
    reviewer.review_all_pages()