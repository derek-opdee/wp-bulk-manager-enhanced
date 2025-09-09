#!/usr/bin/env python3
"""
Comprehensive site-wide SEO and semantic structure review for Reno Warriors
Using WP Bulk Manager to analyze ALL pages
"""

import subprocess
import re
from html import unescape
import json
from datetime import datetime

class ComprehensiveSiteReview:
    def __init__(self):
        self.ssh_host = "170.64.179.157"
        self.ssh_user = "master_ntuqvnephb"
        self.ssh_pass = "56tbztc2cRZ8"
        self.db_host = "localhost"
        self.db_port = "3307"
        self.db_name = "cfhbaxywhg"
        self.db_user = "cfhbaxywhg"
        self.db_pass = "7Sy28jzV25"
        self.wp_prefix = "wpjk_"
        
        self.seo_issues = []
        self.semantic_issues = []
        self.page_results = []
    
    def execute_ssh_command(self, command):
        """Execute command via SSH"""
        full_command = f'sshpass -p "{self.ssh_pass}" ssh -o StrictHostKeyChecking=no {self.ssh_user}@{self.ssh_host} "{command}"'
        try:
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            return result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return "", str(e)
    
    def execute_mysql_query(self, query):
        """Execute MySQL query via SSH tunnel"""
        mysql_cmd = f"mysql -h {self.db_host} -P {self.db_port} -u {self.db_user} -p{self.db_pass} {self.db_name} -e '{query}'"
        return self.execute_ssh_command(mysql_cmd)
    
    def analyze_heading_structure(self, content, page_title):
        """Analyze heading structure and semantic HTML"""
        issues = []
        
        # Find all headings with various patterns
        heading_patterns = {
            'h1': [
                r'<h1[^>]*class="wp-block-heading"[^>]*>(.*?)</h1>',
                r'<h1[^>]*>(.*?)</h1>'
            ],
            'h2': [
                r'<h2[^>]*class="wp-block-heading"[^>]*>(.*?)</h2>',
                r'<h2[^>]*>(.*?)</h2>'
            ],
            'h3': [
                r'<h3[^>]*class="wp-block-heading"[^>]*>(.*?)</h3>',
                r'<h3[^>]*>(.*?)</h3>'
            ],
            'h4': [
                r'<h4[^>]*class="wp-block-heading"[^>]*>(.*?)</h4>',
                r'<h4[^>]*>(.*?)</h4>'
            ],
            'h5': [
                r'<h5[^>]*class="wp-block-heading"[^>]*>(.*?)</h5>',
                r'<h5[^>]*>(.*?)</h5>'
            ],
            'h6': [
                r'<h6[^>]*class="wp-block-heading"[^>]*>(.*?)</h6>',
                r'<h6[^>]*>(.*?)</h6>'
            ]
        }
        
        heading_counts = {}
        all_headings = {}
        
        for level, patterns in heading_patterns.items():
            matches = []
            for pattern in patterns:
                matches.extend(re.findall(pattern, content, re.DOTALL | re.IGNORECASE))
            
            # Clean heading text
            clean_headings = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in matches]
            clean_headings = [h for h in clean_headings if h]  # Remove empty headings
            
            heading_counts[level] = len(clean_headings)
            all_headings[level] = clean_headings
        
        # H1 Analysis - CRITICAL for SEO
        h1_count = heading_counts['h1']
        if h1_count == 0:
            issues.append("❌ CRITICAL: No H1 tag found - major SEO issue")
            self.seo_issues.append(f"{page_title}: Missing H1")
        elif h1_count > 1:
            issues.append(f"❌ CRITICAL: {h1_count} H1 tags found - SEO violation!")
            issues.append(f"   Duplicate H1s: {all_headings['h1']}")
            self.seo_issues.append(f"{page_title}: {h1_count} duplicate H1s")
        else:
            h1_text = all_headings['h1'][0]
            issues.append(f"✅ Perfect H1: '{h1_text[:60]}...'")
        
        # H2-H6 Structure Analysis
        h2_count = heading_counts['h2']
        h3_count = heading_counts['h3']
        h4_count = heading_counts['h4']
        h5_count = heading_counts['h5']
        h6_count = heading_counts['h6']
        
        if h2_count == 0:
            issues.append("⚠️ No H2 headings - content lacks structure")
        else:
            issues.append(f"✅ Good structure: {h2_count} H2 headings")
        
        # Check proper hierarchy
        hierarchy_issues = []
        if h3_count > 0 and h2_count == 0:
            hierarchy_issues.append("H3 without H2")
        if h4_count > 0 and h3_count == 0:
            hierarchy_issues.append("H4 without H3")
        if h5_count > 0 and h4_count == 0:
            hierarchy_issues.append("H5 without H4")
        if h6_count > 0 and h5_count == 0:
            hierarchy_issues.append("H6 without H5")
        
        if hierarchy_issues:
            issues.append(f"❌ SEMANTIC ERROR: Improper hierarchy - {', '.join(hierarchy_issues)}")
            self.semantic_issues.append(f"{page_title}: {', '.join(hierarchy_issues)}")
        else:
            issues.append("✅ Perfect heading hierarchy")
        
        return {
            'heading_counts': heading_counts,
            'all_headings': all_headings,
            'hierarchy_valid': len(hierarchy_issues) == 0,
            'h1_valid': h1_count == 1,
            'issues': issues
        }
    
    def analyze_seo_elements(self, page_id, title, content, status):
        """Comprehensive SEO analysis"""
        issues = []
        
        # Title SEO Analysis
        title_length = len(title)
        if title_length < 30:
            issues.append(f"❌ Title too short ({title_length} chars) - Google may ignore")
            self.seo_issues.append(f"{title}: Title too short ({title_length} chars)")
        elif title_length > 60:
            issues.append(f"⚠️ Title too long ({title_length} chars) - will be truncated")
            self.seo_issues.append(f"{title}: Title too long ({title_length} chars)")
        else:
            issues.append(f"✅ Title length perfect ({title_length} chars)")
        
        # Content Analysis
        content_text = re.sub(r'<[^>]+>', '', content)
        content_text = re.sub(r'\s+', ' ', content_text).strip()
        word_count = len(content_text.split())
        
        if word_count < 200:
            issues.append(f"❌ Content extremely thin ({word_count} words) - critical SEO issue")
            self.seo_issues.append(f"{title}: Thin content ({word_count} words)")
        elif word_count < 300:
            issues.append(f"⚠️ Content thin ({word_count} words) - aim for 500+")
            self.seo_issues.append(f"{title}: Short content ({word_count} words)")
        elif word_count < 500:
            issues.append(f"⚠️ Content short ({word_count} words) - could expand")
        else:
            issues.append(f"✅ Content sufficient ({word_count} words)")
        
        # Keyword Analysis for Reno Warriors
        target_keywords = {
            'primary': ['renovation', 'reno', 'warriors'],
            'location': ['australia', 'australian', 'melbourne', 'victoria', 'patterson lakes'],
            'service': ['kitchen', 'bathroom', 'home', 'accessibility', 'design'],
            'quality': ['professional', 'expert', 'quality', 'premium']
        }
        
        found_categories = []
        missing_categories = []
        
        title_lower = title.lower()
        content_lower = content.lower()
        
        for category, keywords in target_keywords.items():
            found_in_title = any(kw in title_lower for kw in keywords)
            found_in_content = any(kw in content_lower for kw in keywords)
            
            if found_in_title or found_in_content:
                found_categories.append(category)
            else:
                missing_categories.append(category)
        
        if found_categories:
            issues.append(f"✅ Target keywords found: {', '.join(found_categories)}")
        
        if missing_categories:
            issues.append(f"⚠️ Missing keyword categories: {', '.join(missing_categories)}")
        
        # Meta elements check (would need meta query)
        # For now, check if content has good structure for meta generation
        
        # Check for CTAs
        cta_patterns = [
            'contact', 'call', 'phone', 'consultation', 'quote', 'free',
            'book', 'schedule', 'get in touch', 'speak with', 'discuss'
        ]
        
        ctas_found = [cta for cta in cta_patterns if cta in content_lower]
        if ctas_found:
            issues.append(f"✅ Call-to-actions present: {len(ctas_found)} found")
        else:
            issues.append("⚠️ No clear call-to-actions - missing conversion opportunities")
        
        # Internal linking check
        internal_links = len(re.findall(r'<a[^>]*href="[^"]*renowarriors\.com\.au[^"]*"', content))
        if internal_links > 0:
            issues.append(f"✅ Internal links: {internal_links} found")
        else:
            issues.append("⚠️ No internal links - missing SEO opportunity")
        
        # Image alt text check
        images = re.findall(r'<img[^>]*>', content)
        images_with_alt = re.findall(r'<img[^>]*alt="[^"]*"[^>]*>', content)
        
        if images:
            alt_ratio = len(images_with_alt) / len(images) * 100
            if alt_ratio == 100:
                issues.append(f"✅ All {len(images)} images have alt text")
            elif alt_ratio >= 80:
                issues.append(f"⚠️ {alt_ratio:.0f}% images have alt text ({len(images_with_alt)}/{len(images)})")
            else:
                issues.append(f"❌ Poor alt text coverage: {alt_ratio:.0f}% ({len(images_with_alt)}/{len(images)})")
                self.seo_issues.append(f"{title}: Missing alt text on images")
        
        return {
            'title_length': title_length,
            'word_count': word_count,
            'found_keywords': found_categories,
            'missing_keywords': missing_categories,
            'ctas_found': len(ctas_found),
            'internal_links': internal_links,
            'images_total': len(images) if images else 0,
            'images_with_alt': len(images_with_alt) if images else 0,
            'issues': issues
        }
    
    def check_semantic_html(self, content, page_title):
        """Check semantic HTML structure"""
        issues = []
        
        # Check for semantic HTML5 elements
        semantic_elements = {
            'header': r'<header[^>]*>',
            'nav': r'<nav[^>]*>',
            'main': r'<main[^>]*>',
            'article': r'<article[^>]*>',
            'section': r'<section[^>]*>',
            'aside': r'<aside[^>]*>',
            'footer': r'<footer[^>]*>'
        }
        
        found_elements = []
        for element, pattern in semantic_elements.items():
            if re.search(pattern, content, re.IGNORECASE):
                found_elements.append(element)
        
        if found_elements:
            issues.append(f"✅ Semantic HTML5: {', '.join(found_elements)}")
        else:
            issues.append("⚠️ No HTML5 semantic elements found")
        
        # Check Gutenberg block structure
        gutenberg_blocks = content.count('<!-- wp:')
        gutenberg_closes = content.count('<!-- /wp:')
        
        if gutenberg_blocks == 0:
            issues.append("⚠️ No Gutenberg blocks - using classic editor?")
        elif gutenberg_blocks != gutenberg_closes:
            issues.append(f"❌ Gutenberg structure broken: {gutenberg_blocks} open, {gutenberg_closes} close")
            self.semantic_issues.append(f"{page_title}: Broken Gutenberg structure")
        else:
            issues.append(f"✅ {gutenberg_blocks} Gutenberg blocks properly structured")
        
        # Check for accessibility attributes
        accessibility_patterns = {
            'aria-label': r'aria-label="[^"]*"',
            'aria-describedby': r'aria-describedby="[^"]*"',
            'role': r'role="[^"]*"',
            'tabindex': r'tabindex="[^"]*"'
        }
        
        accessibility_found = []
        for attr, pattern in accessibility_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                accessibility_found.append(attr)
        
        if accessibility_found:
            issues.append(f"✅ Accessibility attributes: {', '.join(accessibility_found)}")
        else:
            issues.append("⚠️ No accessibility attributes found")
        
        return {
            'semantic_elements': found_elements,
            'gutenberg_blocks': gutenberg_blocks,
            'gutenberg_valid': gutenberg_blocks == gutenberg_closes,
            'accessibility_attrs': accessibility_found,
            'issues': issues
        }
    
    def get_all_pages(self):
        """Get all pages from the database"""
        query = f"""
        SELECT ID, post_title, post_content, post_status, post_type, post_date 
        FROM {self.wp_prefix}posts 
        WHERE post_type IN ('page', 'post') 
        AND post_status IN ('publish', 'draft', 'private')
        ORDER BY post_type, post_status, ID;
        """
        
        stdout, stderr = self.execute_mysql_query(query)
        
        if stderr and "Warning: Permanently added" not in stderr:
            print(f"❌ Database error: {stderr}")
            return []
        
        if not stdout or "Empty set" in stdout:
            print("❌ No pages found in database")
            return []
        
        lines = stdout.split('\n')
        if len(lines) < 2:
            return []
        
        pages = []
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 6:
                    pages.append({
                        'id': parts[0],
                        'title': parts[1],
                        'content': parts[2],
                        'status': parts[3],
                        'type': parts[4],
                        'date': parts[5]
                    })
        
        return pages
    
    def review_single_page(self, page_data):
        """Review a single page comprehensively"""
        page_id = page_data['id']
        title = page_data['title']
        content = page_data['content']
        status = page_data['status']
        page_type = page_data['type']
        
        print(f"\n📄 REVIEWING {page_type.upper()} {page_id}: {title}")
        print(f"    Status: {status} | Content: {len(content)} chars")
        print("-" * 80)
        
        # Analyze heading structure
        print("🔤 HEADING STRUCTURE & SEMANTIC HTML:")
        heading_analysis = self.analyze_heading_structure(content, title)
        for issue in heading_analysis['issues']:
            print(f"   {issue}")
        
        # Show heading summary
        if any(count > 0 for count in heading_analysis['heading_counts'].values()):
            print("   📊 Heading Summary:", end="")
            for level, count in heading_analysis['heading_counts'].items():
                if count > 0:
                    print(f" {level.upper()}:{count}", end="")
            print()
        
        # SEO Analysis
        print("\n🔍 SEO ANALYSIS:")
        seo_analysis = self.analyze_seo_elements(page_id, title, content, status)
        for issue in seo_analysis['issues']:
            print(f"   {issue}")
        
        # Semantic HTML Analysis
        print("\n🏗️ SEMANTIC HTML STRUCTURE:")
        semantic_analysis = self.check_semantic_html(content, title)
        for issue in semantic_analysis['issues']:
            print(f"   {issue}")
        
        # Calculate overall score
        critical_issues = 0
        warning_issues = 0
        
        all_issues = (heading_analysis['issues'] + 
                     seo_analysis['issues'] + 
                     semantic_analysis['issues'])
        
        for issue in all_issues:
            if issue.startswith('❌'):
                critical_issues += 1
            elif issue.startswith('⚠️'):
                warning_issues += 1
        
        # Overall assessment
        if critical_issues == 0 and warning_issues == 0:
            overall_score = "EXCELLENT"
            print("\n🎉 OVERALL: EXCELLENT - Perfect structure and SEO!")
        elif critical_issues == 0 and warning_issues <= 2:
            overall_score = "GOOD"
            print(f"\n👍 OVERALL: GOOD - {warning_issues} minor improvements possible")
        elif critical_issues == 0:
            overall_score = "NEEDS_IMPROVEMENT"
            print(f"\n⚠️ OVERALL: NEEDS IMPROVEMENT - {warning_issues} issues to address")
        else:
            overall_score = "CRITICAL_ISSUES"
            print(f"\n❌ OVERALL: CRITICAL ISSUES - {critical_issues} critical, {warning_issues} warnings")
        
        result = {
            'page_id': page_id,
            'title': title,
            'type': page_type,
            'status': status,
            'heading_analysis': heading_analysis,
            'seo_analysis': seo_analysis,
            'semantic_analysis': semantic_analysis,
            'critical_issues': critical_issues,
            'warning_issues': warning_issues,
            'overall_score': overall_score
        }
        
        self.page_results.append(result)
        return result
    
    def generate_comprehensive_report(self):
        """Generate final comprehensive report"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE RENO WARRIORS SITE REVIEW")
        print("📋 SEO & SEMANTIC HTML STRUCTURE ANALYSIS")
        print("=" * 80)
        
        if not self.page_results:
            print("❌ No pages analyzed")
            return
        
        total_pages = len(self.page_results)
        
        # Overall scores
        excellent = len([p for p in self.page_results if p['overall_score'] == 'EXCELLENT'])
        good = len([p for p in self.page_results if p['overall_score'] == 'GOOD'])
        needs_improvement = len([p for p in self.page_results if p['overall_score'] == 'NEEDS_IMPROVEMENT'])
        critical = len([p for p in self.page_results if p['overall_score'] == 'CRITICAL_ISSUES'])
        
        print(f"\n📊 SITE-WIDE OVERVIEW:")
        print(f"   Total pages analyzed: {total_pages}")
        print(f"   🎉 Excellent: {excellent} ({excellent/total_pages*100:.1f}%)")
        print(f"   👍 Good: {good} ({good/total_pages*100:.1f}%)")
        print(f"   ⚠️ Needs improvement: {needs_improvement} ({needs_improvement/total_pages*100:.1f}%)")
        print(f"   ❌ Critical issues: {critical} ({critical/total_pages*100:.1f}%)")
        
        # H1 Structure Analysis
        print(f"\n🔤 H1 STRUCTURE COMPLIANCE:")
        h1_perfect = len([p for p in self.page_results if p['heading_analysis']['h1_valid']])
        duplicate_h1s = [p for p in self.page_results if p['heading_analysis']['heading_counts']['h1'] > 1]
        missing_h1s = [p for p in self.page_results if p['heading_analysis']['heading_counts']['h1'] == 0]
        
        print(f"   ✅ Perfect H1 structure: {h1_perfect}/{total_pages} pages ({h1_perfect/total_pages*100:.1f}%)")
        
        if duplicate_h1s:
            print(f"   ❌ Pages with DUPLICATE H1s ({len(duplicate_h1s)}):")
            for page in duplicate_h1s[:5]:  # Show first 5
                h1_count = page['heading_analysis']['heading_counts']['h1']
                print(f"      - {page['title']}: {h1_count} H1s")
            if len(duplicate_h1s) > 5:
                print(f"      ... and {len(duplicate_h1s) - 5} more")
        
        if missing_h1s:
            print(f"   ❌ Pages MISSING H1s ({len(missing_h1s)}):")
            for page in missing_h1s[:5]:
                print(f"      - {page['title']}")
            if len(missing_h1s) > 5:
                print(f"      ... and {len(missing_h1s) - 5} more")
        
        # SEO Issues Summary
        print(f"\n🔍 SEO ISSUES SUMMARY:")
        thin_content = [p for p in self.page_results if p['seo_analysis']['word_count'] < 300]
        title_issues = [p for p in self.page_results if p['seo_analysis']['title_length'] < 30 or p['seo_analysis']['title_length'] > 60]
        
        print(f"   Total unique SEO issues found: {len(set(self.seo_issues))}")
        
        if thin_content:
            print(f"   ❌ Thin content ({len(thin_content)} pages):")
            for page in thin_content[:3]:
                print(f"      - {page['title']}: {page['seo_analysis']['word_count']} words")
            if len(thin_content) > 3:
                print(f"      ... and {len(thin_content) - 3} more")
        
        if title_issues:
            print(f"   ⚠️ Title length issues ({len(title_issues)} pages):")
            for page in title_issues[:3]:
                print(f"      - {page['title']}: {page['seo_analysis']['title_length']} chars")
            if len(title_issues) > 3:
                print(f"      ... and {len(title_issues) - 3} more")
        
        # Semantic HTML Summary
        print(f"\n🏗️ SEMANTIC HTML COMPLIANCE:")
        semantic_valid = len([p for p in self.page_results if p['semantic_analysis']['gutenberg_valid']])
        print(f"   ✅ Valid Gutenberg structure: {semantic_valid}/{total_pages} pages ({semantic_valid/total_pages*100:.1f}%)")
        
        semantic_elements_found = 0
        for page in self.page_results:
            if page['semantic_analysis']['semantic_elements']:
                semantic_elements_found += 1
        
        print(f"   ✅ HTML5 semantic elements: {semantic_elements_found}/{total_pages} pages ({semantic_elements_found/total_pages*100:.1f}%)")
        
        # Page Type Breakdown
        print(f"\n📄 PAGE TYPE BREAKDOWN:")
        page_types = {}
        for page in self.page_results:
            page_type = page['type']
            if page_type not in page_types:
                page_types[page_type] = {'total': 0, 'excellent': 0, 'good': 0, 'issues': 0}
            
            page_types[page_type]['total'] += 1
            if page['overall_score'] == 'EXCELLENT':
                page_types[page_type]['excellent'] += 1
            elif page['overall_score'] == 'GOOD':
                page_types[page_type]['good'] += 1
            else:
                page_types[page_type]['issues'] += 1
        
        for page_type, stats in page_types.items():
            total = stats['total']
            excellent = stats['excellent']
            good = stats['good']
            issues = stats['issues']
            print(f"   {page_type.upper()}: {total} total | ✅{excellent} excellent | 👍{good} good | ⚠️{issues} issues")
        
        # Critical Actions Needed
        print(f"\n🚨 CRITICAL ACTIONS NEEDED:")
        if duplicate_h1s:
            print(f"   1. Fix {len(duplicate_h1s)} pages with duplicate H1s (URGENT - SEO critical)")
        if missing_h1s:
            print(f"   2. Add H1 tags to {len(missing_h1s)} pages (URGENT - SEO critical)")
        if thin_content:
            print(f"   3. Expand content on {len(thin_content)} pages (aim for 500+ words)")
        if title_issues:
            print(f"   4. Optimize {len(title_issues)} page titles (50-60 chars ideal)")
        
        if not (duplicate_h1s or missing_h1s or thin_content or title_issues):
            print("   🎉 NO CRITICAL ACTIONS NEEDED - Site structure is excellent!")
        
        # Recommendations
        print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
        print("   📈 SEO Improvements:")
        print("      - Add meta descriptions to all pages")
        print("      - Increase internal linking between pages")
        print("      - Add schema markup for local business")
        print("      - Optimize images with descriptive alt text")
        
        print("   🏗️ Semantic HTML Improvements:")
        print("      - Add more HTML5 semantic elements (article, section)")
        print("      - Improve accessibility attributes (aria-labels)")
        print("      - Ensure proper heading hierarchy on all pages")
        
        print("   📊 Content Strategy:")
        print("      - Expand thin content with relevant information")
        print("      - Add FAQ sections to service pages")
        print("      - Include customer testimonials and reviews")
        print("      - Create location-specific landing pages")
        
        # Export summary data
        summary_data = {
            'review_date': datetime.now().isoformat(),
            'total_pages': total_pages,
            'scores': {
                'excellent': excellent,
                'good': good,
                'needs_improvement': needs_improvement,
                'critical_issues': critical
            },
            'h1_issues': {
                'duplicate_h1s': len(duplicate_h1s),
                'missing_h1s': len(missing_h1s)
            },
            'seo_issues': {
                'thin_content': len(thin_content),
                'title_issues': len(title_issues),
                'total_unique_issues': len(set(self.seo_issues))
            },
            'semantic_compliance': {
                'valid_gutenberg': semantic_valid,
                'semantic_elements': semantic_elements_found
            }
        }
        
        with open('reno_warriors_site_review.json', 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"\n✅ COMPREHENSIVE REVIEW COMPLETE!")
        print(f"📄 Analyzed: {total_pages} pages")
        print(f"📊 Report saved: reno_warriors_site_review.json")
        
        return summary_data
    
    def run_full_site_review(self):
        """Run complete site review"""
        print("🏠 RENO WARRIORS COMPREHENSIVE SITE REVIEW")
        print("🔍 Analyzing ALL pages for SEO & Semantic HTML Structure")
        print("=" * 80)
        
        # Get all pages
        print("📋 Fetching all pages from database...")
        pages = self.get_all_pages()
        
        if not pages:
            print("❌ No pages found to analyze")
            return
        
        print(f"✅ Found {len(pages)} pages to analyze")
        
        # Group by type
        pages_by_type = {}
        for page in pages:
            page_type = page['type']
            if page_type not in pages_by_type:
                pages_by_type[page_type] = []
            pages_by_type[page_type].append(page)
        
        print("📊 Page breakdown:")
        for page_type, type_pages in pages_by_type.items():
            print(f"   {page_type.upper()}: {len(type_pages)} pages")
        
        # Review each page
        for i, page in enumerate(pages, 1):
            print(f"\n[{i}/{len(pages)}]", end="")
            self.review_single_page(page)
        
        # Generate comprehensive report
        return self.generate_comprehensive_report()

if __name__ == "__main__":
    reviewer = ComprehensiveSiteReview()
    reviewer.run_full_site_review()