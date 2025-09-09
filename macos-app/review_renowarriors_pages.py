#!/usr/bin/env python3
"""
Review Reno Warriors accessibility pages for semantic structure and SEO
"""

from wpbm_manager_mysql import WPBulkManagerMySQL
import re
from html import unescape

class PageSemanticReviewer:
    def __init__(self):
        self.manager = WPBulkManagerMySQL()
        self.accessibility_page_ids = [7556, 7557, 7558, 7559, 7560]
        self.page_titles = {
            7556: "Bathroom Accessibility Renovation Services",
            7557: "Kitchen Accessibility Renovation Services", 
            7558: "Laundry Accessibility Renovation Services",
            7559: "Home Accessibility Design & Planning Services",
            7560: "European Accessible Hardware & Fixtures"
        }
        
    def analyze_heading_structure(self, content):
        """Analyze heading structure and hierarchy"""
        issues = []
        
        # Find all headings
        h1_pattern = r'<h1[^>]*>(.*?)</h1>'
        h2_pattern = r'<h2[^>]*>(.*?)</h2>'
        h3_pattern = r'<h3[^>]*>(.*?)</h3>'
        h4_pattern = r'<h4[^>]*>(.*?)</h4>'
        
        h1_matches = re.findall(h1_pattern, content, re.DOTALL | re.IGNORECASE)
        h2_matches = re.findall(h2_pattern, content, re.DOTALL | re.IGNORECASE)
        h3_matches = re.findall(h3_pattern, content, re.DOTALL | re.IGNORECASE)
        h4_matches = re.findall(h4_pattern, content, re.DOTALL | re.IGNORECASE)
        
        # Clean heading text
        h1_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h1_matches]
        h2_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h2_matches]
        h3_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h3_matches]
        h4_clean = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h4_matches]
        
        # Check H1 count
        if len(h1_clean) == 0:
            issues.append("❌ No H1 tag found")
        elif len(h1_clean) > 1:
            issues.append(f"⚠️ Multiple H1 tags found ({len(h1_clean)}): {h1_clean}")
        else:
            issues.append(f"✅ Single H1 found: '{h1_clean[0]}'")
        
        # Check hierarchy
        if h3_clean and not h2_clean:
            issues.append("⚠️ H3 found without H2 - improper hierarchy")
        
        if h4_clean and not h3_clean:
            issues.append("⚠️ H4 found without H3 - improper hierarchy")
        
        return {
            'h1': h1_clean,
            'h2': h2_clean,
            'h3': h3_clean,
            'h4': h4_clean,
            'issues': issues,
            'hierarchy_valid': len(issues) <= 1  # Only H1 success message is acceptable
        }
    
    def analyze_seo_elements(self, page_data):
        """Analyze SEO elements"""
        seo_issues = []
        content = page_data.get('content', {}).get('rendered', '')
        title = page_data.get('title', {}).get('rendered', '')
        excerpt = page_data.get('excerpt', {}).get('rendered', '')
        
        # Check title length
        title_length = len(title)
        if title_length < 30:
            seo_issues.append(f"⚠️ Title too short ({title_length} chars) - aim for 50-60")
        elif title_length > 60:
            seo_issues.append(f"⚠️ Title too long ({title_length} chars) - aim for 50-60")
        else:
            seo_issues.append(f"✅ Title length good ({title_length} chars)")
        
        # Check for meta description (would be in SEO data)
        if not excerpt or len(excerpt.strip()) < 10:
            seo_issues.append("⚠️ No meta description detected")
        else:
            excerpt_length = len(re.sub(r'<[^>]+>', '', excerpt).strip())
            if excerpt_length < 120:
                seo_issues.append(f"⚠️ Meta description too short ({excerpt_length} chars)")
            elif excerpt_length > 160:
                seo_issues.append(f"⚠️ Meta description too long ({excerpt_length} chars)")
            else:
                seo_issues.append(f"✅ Meta description length good ({excerpt_length} chars)")
        
        # Check content length
        content_text = re.sub(r'<[^>]+>', '', content)
        content_words = len(content_text.split())
        if content_words < 300:
            seo_issues.append(f"⚠️ Content too short ({content_words} words) - aim for 500+")
        else:
            seo_issues.append(f"✅ Content length good ({content_words} words)")
        
        # Check for target keywords in title
        if 'accessibility' not in title.lower():
            seo_issues.append("⚠️ Target keyword 'accessibility' not in title")
        else:
            seo_issues.append("✅ Target keyword 'accessibility' found in title")
        
        # Check for location targeting
        if 'australia' not in title.lower() and 'australian' not in title.lower():
            seo_issues.append("⚠️ Location targeting (Australia) not in title")
        else:
            seo_issues.append("✅ Location targeting found in title")
        
        return {
            'title': title,
            'title_length': title_length,
            'content_words': content_words,
            'issues': seo_issues
        }
    
    def check_gutenberg_structure(self, content):
        """Check Gutenberg block structure"""
        issues = []
        
        # Check for proper Gutenberg blocks
        block_pattern = r'<!-- wp:(\w+)'
        blocks = re.findall(block_pattern, content)
        
        if not blocks:
            issues.append("⚠️ No Gutenberg blocks detected - may be classic editor content")
        else:
            issues.append(f"✅ Gutenberg blocks found: {len(blocks)} blocks")
            
            # Check for common block types
            if 'heading' not in blocks:
                issues.append("⚠️ No heading blocks found")
            if 'paragraph' not in blocks:
                issues.append("⚠️ No paragraph blocks found")
            if 'buttons' in blocks:
                issues.append("✅ Call-to-action buttons present")
        
        # Check for proper block closure
        open_blocks = content.count('<!-- wp:')
        close_blocks = content.count('<!-- /wp:')
        if open_blocks != close_blocks:
            issues.append(f"⚠️ Block mismatch: {open_blocks} opening, {close_blocks} closing")
        else:
            issues.append("✅ All Gutenberg blocks properly closed")
        
        return {
            'blocks': blocks,
            'block_count': len(blocks),
            'issues': issues
        }
    
    def review_single_page(self, page_id):
        """Review a single page"""
        print(f"\n📄 REVIEWING PAGE {page_id}: {self.page_titles.get(page_id, 'Unknown')}")
        print("=" * 70)
        
        try:
            client = self.manager.get_client('renowarriors')
            if not client:
                print("❌ Could not connect to Reno Warriors")
                return None
            
            # Get page data
            page_data = client.api_client.get(f"posts/{page_id}")
            if not page_data:
                print(f"❌ Could not retrieve page {page_id}")
                return None
            
            content = page_data.get('content', {}).get('rendered', '')
            
            # Analyze heading structure
            print("\n🔤 HEADING STRUCTURE ANALYSIS:")
            heading_analysis = self.analyze_heading_structure(content)
            for issue in heading_analysis['issues']:
                print(f"   {issue}")
            
            if heading_analysis['h2']:
                print(f"\n   H2 Headings ({len(heading_analysis['h2'])}):")
                for i, h2 in enumerate(heading_analysis['h2'], 1):
                    print(f"      {i}. {h2}")
            
            if heading_analysis['h3']:
                print(f"\n   H3 Headings ({len(heading_analysis['h3'])}):")
                for i, h3 in enumerate(heading_analysis['h3'], 1):
                    print(f"      {i}. {h3}")
            
            # Analyze SEO elements
            print("\n🔍 SEO ANALYSIS:")
            seo_analysis = self.analyze_seo_elements(page_data)
            for issue in seo_analysis['issues']:
                print(f"   {issue}")
            
            print(f"\n   Page Title: '{seo_analysis['title']}'")
            
            # Check Gutenberg structure
            print("\n🧱 GUTENBERG STRUCTURE:")
            gutenberg_analysis = self.check_gutenberg_structure(content)
            for issue in gutenberg_analysis['issues']:
                print(f"   {issue}")
            
            # Overall score
            total_issues = len([i for i in heading_analysis['issues'] if i.startswith('❌') or i.startswith('⚠️')])
            total_issues += len([i for i in seo_analysis['issues'] if i.startswith('❌') or i.startswith('⚠️')])
            total_issues += len([i for i in gutenberg_analysis['issues'] if i.startswith('❌') or i.startswith('⚠️')])
            
            if total_issues == 0:
                print("\n🎉 OVERALL: EXCELLENT - No issues found!")
            elif total_issues <= 2:
                print(f"\n👍 OVERALL: GOOD - {total_issues} minor issues to address")
            elif total_issues <= 4:
                print(f"\n⚠️ OVERALL: NEEDS IMPROVEMENT - {total_issues} issues found")
            else:
                print(f"\n❌ OVERALL: MAJOR ISSUES - {total_issues} problems need fixing")
            
            return {
                'page_id': page_id,
                'title': self.page_titles.get(page_id),
                'heading_analysis': heading_analysis,
                'seo_analysis': seo_analysis,
                'gutenberg_analysis': gutenberg_analysis,
                'total_issues': total_issues
            }
            
        except Exception as e:
            print(f"❌ Error reviewing page {page_id}: {str(e)}")
            return None
    
    def review_all_pages(self):
        """Review all accessibility pages"""
        print("🏠 RENO WARRIORS ACCESSIBILITY PAGES REVIEW")
        print("📊 Semantic Structure & SEO Analysis")
        print("=" * 70)
        
        results = []
        
        for page_id in self.accessibility_page_ids:
            result = self.review_single_page(page_id)
            if result:
                results.append(result)
        
        # Generate summary report
        print("\n" + "=" * 70)
        print("📋 SUMMARY REPORT")
        print("=" * 70)
        
        total_pages = len(results)
        pages_with_issues = len([r for r in results if r['total_issues'] > 0])
        pages_excellent = len([r for r in results if r['total_issues'] == 0])
        
        print(f"\n📊 OVERVIEW:")
        print(f"   Total pages reviewed: {total_pages}")
        print(f"   Pages with no issues: {pages_excellent}")
        print(f"   Pages needing attention: {pages_with_issues}")
        
        # Heading structure summary
        print(f"\n🔤 HEADING STRUCTURE SUMMARY:")
        h1_issues = []
        hierarchy_issues = []
        
        for result in results:
            h1_count = len(result['heading_analysis']['h1'])
            if h1_count == 0:
                h1_issues.append(f"{result['title']}: No H1")
            elif h1_count > 1:
                h1_issues.append(f"{result['title']}: {h1_count} H1s")
            
            if not result['heading_analysis']['hierarchy_valid']:
                hierarchy_issues.append(result['title'])
        
        if not h1_issues:
            print("   ✅ All pages have proper H1 structure")
        else:
            print("   ⚠️ H1 Issues:")
            for issue in h1_issues:
                print(f"      - {issue}")
        
        if not hierarchy_issues:
            print("   ✅ All pages have proper heading hierarchy")
        else:
            print("   ⚠️ Hierarchy Issues:")
            for page in hierarchy_issues:
                print(f"      - {page}")
        
        # SEO summary
        print(f"\n🔍 SEO SUMMARY:")
        title_issues = []
        content_issues = []
        
        for result in results:
            title_len = result['seo_analysis']['title_length']
            if title_len < 30 or title_len > 60:
                title_issues.append(f"{result['title']}: {title_len} chars")
            
            word_count = result['seo_analysis']['content_words']
            if word_count < 300:
                content_issues.append(f"{result['title']}: {word_count} words")
        
        if not title_issues:
            print("   ✅ All page titles are optimal length")
        else:
            print("   ⚠️ Title Length Issues:")
            for issue in title_issues:
                print(f"      - {issue}")
        
        if not content_issues:
            print("   ✅ All pages have sufficient content")
        else:
            print("   ⚠️ Content Length Issues:")
            for issue in content_issues:
                print(f"      - {issue}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if pages_excellent == total_pages:
            print("   🎉 All pages are excellent! Ready to publish.")
        else:
            print("   🔧 Priority fixes needed:")
            
            if h1_issues:
                print("      1. Fix H1 structure issues")
            if hierarchy_issues:
                print("      2. Correct heading hierarchy")
            if title_issues:
                print("      3. Optimize page title lengths")
            if content_issues:
                print("      4. Expand thin content")
            
            print("   📈 SEO improvements:")
            print("      - Add meta descriptions if missing")
            print("      - Include target keywords naturally")
            print("      - Add internal links between pages")
            print("      - Consider adding FAQ sections")
        
        print(f"\n✅ Review complete! Pages analyzed: {total_pages}")
        return results

if __name__ == "__main__":
    reviewer = PageSemanticReviewer()
    reviewer.review_all_pages()