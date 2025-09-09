#!/usr/bin/env python3
"""
Review Reno Warriors pages using WP Bulk Manager
"""

from wpbm_manager_mysql import WPBulkManagerMySQL
import re
from html import unescape

class WPBMPageReviewer:
    def __init__(self):
        self.manager = WPBulkManagerMySQL()
        self.page_ids = [7556, 7557, 7558, 7559, 7560]
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
        
        # Find all headings in Gutenberg format
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
        
        # Check H1 count - CRITICAL for SEO
        if len(h1_clean) == 0:
            issues.append("❌ CRITICAL: No H1 tag found")
        elif len(h1_clean) > 1:
            issues.append(f"❌ CRITICAL: Multiple H1 tags ({len(h1_clean)}) - Duplicate H1s detected!")
            issues.append(f"   H1s found: {h1_clean}")
        else:
            issues.append(f"✅ Perfect H1: '{h1_clean[0]}'")
        
        # Check H2 structure
        if not h2_clean:
            issues.append("⚠️ No H2 headings - missing content structure")
        else:
            issues.append(f"✅ Good H2 structure: {len(h2_clean)} H2 headings")
        
        # Check H3 structure
        if h3_clean:
            issues.append(f"✅ H3 headings present: {len(h3_clean)} H3s")
        
        # Check hierarchy - H3 should not appear without H2
        if h3_clean and not h2_clean:
            issues.append("❌ SEMANTIC ERROR: H3 found without H2 - improper hierarchy")
        
        return {
            'h1': h1_clean,
            'h2': h2_clean,
            'h3': h3_clean,
            'issues': issues,
            'hierarchy_valid': len(h1_clean) == 1 and (not h3_clean or h2_clean)
        }
    
    def analyze_seo_elements(self, page_data, content):
        """Comprehensive SEO analysis"""
        seo_issues = []
        
        title = page_data.get('title', {}).get('rendered', '') if isinstance(page_data.get('title'), dict) else str(page_data.get('title', ''))
        
        # Title SEO analysis
        title_length = len(title)
        if title_length < 30:
            seo_issues.append(f"❌ Title too short ({title_length} chars) - Google may truncate")
        elif title_length > 60:
            seo_issues.append(f"❌ Title too long ({title_length} chars) - will be truncated in SERPs")
        else:
            seo_issues.append(f"✅ Title length perfect ({title_length} chars)")
        
        # Content analysis
        content_text = re.sub(r'<[^>]+>', '', content)
        word_count = len(content_text.split())
        
        if word_count < 300:
            seo_issues.append(f"❌ Content too thin ({word_count} words) - aim for 500+ for SEO")
        elif word_count < 500:
            seo_issues.append(f"⚠️ Content short ({word_count} words) - could be longer for better SEO")
        else:
            seo_issues.append(f"✅ Content length excellent ({word_count} words)")
        
        # Keyword analysis
        target_keywords = ['accessibility', 'renovation', 'australia', 'australian']
        found_keywords = []
        missing_keywords = []
        
        for keyword in target_keywords:
            if keyword.lower() in title.lower():
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        if found_keywords:
            seo_issues.append(f"✅ Target keywords in title: {', '.join(found_keywords)}")
        
        if missing_keywords:
            seo_issues.append(f"⚠️ Missing keywords in title: {', '.join(missing_keywords)}")
        
        # Check for call-to-action
        cta_patterns = ['consultation', 'contact', 'call', 'phone', 'book', 'free']
        cta_found = any(pattern in content.lower() for pattern in cta_patterns)
        
        if cta_found:
            seo_issues.append("✅ Call-to-action present")
        else:
            seo_issues.append("❌ No clear call-to-action found")
        
        # Check for internal links
        internal_links = len(re.findall(r'<a[^>]*href="[^"]*renowarriors\.com\.au[^"]*"', content))
        external_links = len(re.findall(r'<a[^>]*href="http[^"]*"', content)) - internal_links
        
        if internal_links > 0:
            seo_issues.append(f"✅ Internal links: {internal_links}")
        else:
            seo_issues.append("⚠️ No internal links - missing SEO opportunity")
        
        # Check for location mentions
        if 'patterson lakes' in content.lower() or 'victoria' in content.lower() or 'melbourne' in content.lower():
            seo_issues.append("✅ Local SEO - location mentioned")
        else:
            seo_issues.append("⚠️ Local SEO - consider mentioning location")
        
        return {
            'title': title,
            'title_length': title_length,
            'word_count': word_count,
            'found_keywords': found_keywords,
            'missing_keywords': missing_keywords,
            'internal_links': internal_links,
            'issues': seo_issues
        }
    
    def check_gutenberg_structure(self, content):
        """Check Gutenberg block structure and compliance"""
        issues = []
        
        # Count blocks
        block_opens = content.count('<!-- wp:')
        block_closes = content.count('<!-- /wp:')
        
        if block_opens == 0:
            issues.append("❌ No Gutenberg blocks - using classic editor?")
            return {'block_count': 0, 'issues': issues}
        
        issues.append(f"✅ Gutenberg structure: {block_opens} blocks")
        
        # Check block integrity
        if block_opens != block_closes:
            issues.append(f"❌ CRITICAL: Block structure broken - {block_opens} opens, {block_closes} closes")
        else:
            issues.append("✅ All blocks properly structured")
        
        # Check for essential blocks
        essential_blocks = {
            'heading': '<!-- wp:heading',
            'paragraph': '<!-- wp:paragraph',
            'buttons': '<!-- wp:buttons',
            'columns': '<!-- wp:columns',
            'list': '<!-- wp:list'
        }
        
        for block_name, pattern in essential_blocks.items():
            if pattern in content:
                issues.append(f"✅ {block_name.title()} blocks present")
            else:
                if block_name in ['heading', 'paragraph']:
                    issues.append(f"❌ Missing {block_name} blocks")
                else:
                    issues.append(f"⚠️ No {block_name} blocks (consider adding)")
        
        return {
            'block_count': block_opens,
            'issues': issues,
            'structure_valid': block_opens == block_closes
        }
    
    def review_single_page(self, page_id):
        """Review a single page comprehensively"""
        print(f"\n📄 REVIEWING PAGE {page_id}: {self.page_titles.get(page_id, 'Unknown')}")
        print("=" * 70)
        
        try:
            # Get client for Reno Warriors
            client = self.manager.get_client('renowarriors')
            if not client:
                print("❌ Could not connect to Reno Warriors")
                return None
            
            # Get page content
            result = client.get_content(page_id)
            
            if not result or result.get('error'):
                print(f"❌ Could not retrieve page {page_id}: {result.get('error', 'Unknown error')}")
                return None
            
            content = result.get('content', '')
            
            # Analyze heading structure
            print("\n🔤 HEADING STRUCTURE & SEMANTIC ANALYSIS:")
            heading_analysis = self.analyze_heading_structure(content)
            for issue in heading_analysis['issues']:
                print(f"   {issue}")
            
            if heading_analysis['h2']:
                print(f"\n   📋 H2 Structure ({len(heading_analysis['h2'])}):")
                for i, h2 in enumerate(heading_analysis['h2'], 1):
                    print(f"      {i}. {h2}")
            
            if heading_analysis['h3']:
                print(f"\n   📋 H3 Structure ({len(heading_analysis['h3'])}):")
                for i, h3 in enumerate(heading_analysis['h3'], 1):
                    print(f"      {i}. {h3}")
            
            # SEO analysis
            print("\n🔍 SEO ANALYSIS:")
            seo_analysis = self.analyze_seo_elements(result, content)
            for issue in seo_analysis['issues']:
                print(f"   {issue}")
            
            print(f"\n   📊 Page Title: '{seo_analysis['title']}'")
            
            # Gutenberg structure
            print("\n🧱 GUTENBERG BLOCK STRUCTURE:")
            gutenberg_analysis = self.check_gutenberg_structure(content)
            for issue in gutenberg_analysis['issues']:
                print(f"   {issue}")
            
            # Calculate overall score
            critical_issues = len([i for i in heading_analysis['issues'] + seo_analysis['issues'] + gutenberg_analysis['issues'] if i.startswith('❌')])
            warning_issues = len([i for i in heading_analysis['issues'] + seo_analysis['issues'] + gutenberg_analysis['issues'] if i.startswith('⚠️')])
            
            print(f"\n📊 OVERALL ASSESSMENT:")
            if critical_issues == 0 and warning_issues == 0:
                print("   🎉 EXCELLENT - Ready to publish!")
                overall_score = "EXCELLENT"
            elif critical_issues == 0 and warning_issues <= 2:
                print(f"   👍 GOOD - {warning_issues} minor improvements possible")
                overall_score = "GOOD"
            elif critical_issues == 0:
                print(f"   ⚠️ NEEDS IMPROVEMENT - {warning_issues} issues to address")
                overall_score = "NEEDS IMPROVEMENT"
            else:
                print(f"   ❌ CRITICAL ISSUES - {critical_issues} critical, {warning_issues} warnings")
                overall_score = "CRITICAL ISSUES"
            
            return {
                'page_id': page_id,
                'title': self.page_titles.get(page_id),
                'heading_analysis': heading_analysis,
                'seo_analysis': seo_analysis,
                'gutenberg_analysis': gutenberg_analysis,
                'critical_issues': critical_issues,
                'warning_issues': warning_issues,
                'overall_score': overall_score
            }
            
        except Exception as e:
            print(f"❌ Error reviewing page {page_id}: {str(e)}")
            return None
    
    def generate_summary_report(self, results):
        """Generate comprehensive summary report"""
        print("\n" + "=" * 70)
        print("📋 COMPREHENSIVE SUMMARY REPORT")
        print("=" * 70)
        
        if not results:
            print("❌ No pages could be analyzed")
            return
        
        total_pages = len(results)
        excellent = len([r for r in results if r['overall_score'] == 'EXCELLENT'])
        good = len([r for r in results if r['overall_score'] == 'GOOD'])
        needs_improvement = len([r for r in results if r['overall_score'] == 'NEEDS IMPROVEMENT'])
        critical = len([r for r in results if r['overall_score'] == 'CRITICAL ISSUES'])
        
        print(f"\n📊 OVERALL STATUS:")
        print(f"   Total pages reviewed: {total_pages}")
        print(f"   🎉 Excellent: {excellent}")
        print(f"   👍 Good: {good}")
        print(f"   ⚠️ Needs improvement: {needs_improvement}")
        print(f"   ❌ Critical issues: {critical}")
        
        # H1 Analysis
        print(f"\n🔤 H1 STRUCTURE COMPLIANCE:")
        h1_issues = []
        duplicate_h1s = []
        
        for result in results:
            h1_count = len(result['heading_analysis']['h1'])
            if h1_count == 0:
                h1_issues.append(f"{result['title']}: No H1")
            elif h1_count > 1:
                duplicate_h1s.append(f"{result['title']}: {h1_count} H1s")
        
        if not h1_issues and not duplicate_h1s:
            print("   ✅ ALL PAGES: Perfect H1 structure")
        else:
            if h1_issues:
                print("   ❌ Missing H1:")
                for issue in h1_issues:
                    print(f"      - {issue}")
            if duplicate_h1s:
                print("   ❌ DUPLICATE H1s (CRITICAL SEO ISSUE):")
                for issue in duplicate_h1s:
                    print(f"      - {issue}")
        
        # SEO Compliance
        print(f"\n🔍 SEO COMPLIANCE:")
        title_issues = []
        content_issues = []
        keyword_issues = []
        
        for result in results:
            # Title length issues
            title_len = result['seo_analysis']['title_length']
            if title_len < 30 or title_len > 60:
                title_issues.append(f"{result['title']}: {title_len} chars")
            
            # Content length issues
            word_count = result['seo_analysis']['word_count']
            if word_count < 300:
                content_issues.append(f"{result['title']}: {word_count} words")
            
            # Keyword issues
            if not result['seo_analysis']['found_keywords']:
                keyword_issues.append(f"{result['title']}: No target keywords")
        
        if not title_issues:
            print("   ✅ All titles optimal length (30-60 chars)")
        else:
            print("   ⚠️ Title length issues:")
            for issue in title_issues:
                print(f"      - {issue}")
        
        if not content_issues:
            print("   ✅ All content sufficient length")
        else:
            print("   ❌ Content length issues:")
            for issue in content_issues:
                print(f"      - {issue}")
        
        # Gutenberg Compliance
        print(f"\n🧱 GUTENBERG STRUCTURE:")
        gutenberg_issues = []
        
        for result in results:
            if not result['gutenberg_analysis']['structure_valid']:
                gutenberg_issues.append(f"{result['title']}: Block structure broken")
        
        if not gutenberg_issues:
            print("   ✅ All pages have valid Gutenberg structure")
        else:
            print("   ❌ Gutenberg structure issues:")
            for issue in gutenberg_issues:
                print(f"      - {issue}")
        
        # Recommendations
        print(f"\n💡 ACTIONABLE RECOMMENDATIONS:")
        
        if excellent == total_pages:
            print("   🎉 PERFECT! All pages ready to publish!")
            print("   📈 Next steps:")
            print("      1. Publish all pages")
            print("      2. Add to main navigation")
            print("      3. Submit sitemap to Google")
        else:
            print("   🔧 PRIORITY FIXES:")
            
            if duplicate_h1s:
                print("      1. 🚨 URGENT: Fix duplicate H1s (critical SEO issue)")
            if h1_issues:
                print("      2. 🚨 URGENT: Add missing H1s")
            if content_issues:
                print("      3. 📝 Expand thin content (aim for 500+ words)")
            if title_issues:
                print("      4. 🏷️ Optimize title lengths (50-60 chars ideal)")
            if gutenberg_issues:
                print("      5. 🧱 Fix Gutenberg block structure")
            
            print("   📈 SEO ENHANCEMENTS:")
            print("      - Add meta descriptions (150-160 chars)")
            print("      - Include more internal links")
            print("      - Add FAQ sections")
            print("      - Include customer testimonials")
            print("      - Add local business schema markup")
        
        return {
            'total_pages': total_pages,
            'scores': {'excellent': excellent, 'good': good, 'needs_improvement': needs_improvement, 'critical': critical},
            'h1_issues': len(h1_issues) + len(duplicate_h1s),
            'seo_issues': len(title_issues) + len(content_issues),
            'recommendations_count': len([r for r in results if r['overall_score'] != 'EXCELLENT'])
        }
    
    def review_all_pages(self):
        """Review all accessibility pages"""
        print("🏠 RENO WARRIORS ACCESSIBILITY PAGES")
        print("📊 COMPREHENSIVE SEMANTIC STRUCTURE & SEO REVIEW")
        print("=" * 70)
        
        results = []
        
        for page_id in self.page_ids:
            result = self.review_single_page(page_id)
            if result:
                results.append(result)
        
        # Generate summary
        summary = self.generate_summary_report(results)
        
        print(f"\n✅ Review completed successfully!")
        print(f"📄 Pages analyzed: {len(results)}/{len(self.page_ids)}")
        
        return results, summary

if __name__ == "__main__":
    reviewer = WPBMPageReviewer()
    reviewer.review_all_pages()