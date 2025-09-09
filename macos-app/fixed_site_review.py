#!/usr/bin/env python3
"""
Fixed comprehensive site review for Reno Warriors
"""

import subprocess
import re
from html import unescape
import json

class FixedSiteReview:
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
        
        self.critical_issues = []
        self.seo_issues = []
        self.semantic_issues = []
        
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
    
    def analyze_heading_structure(self, content, title):
        """Analyze heading structure"""
        issues = []
        
        # Count all heading levels
        h1_count = len(re.findall(r'<h1[^>]*>', content, re.IGNORECASE))
        h2_count = len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE))
        h3_count = len(re.findall(r'<h3[^>]*>', content, re.IGNORECASE))
        h4_count = len(re.findall(r'<h4[^>]*>', content, re.IGNORECASE))
        
        # H1 Analysis - CRITICAL
        if h1_count == 0:
            issues.append("❌ CRITICAL: No H1 tag")
            self.critical_issues.append(f"{title}: Missing H1")
        elif h1_count > 1:
            issues.append(f"❌ CRITICAL: {h1_count} H1 tags - SEO violation!")
            self.critical_issues.append(f"{title}: {h1_count} duplicate H1s")
        else:
            issues.append("✅ Perfect H1 structure")
        
        # Structure analysis
        if h2_count == 0:
            issues.append("⚠️ No H2 headings")
        else:
            issues.append(f"✅ {h2_count} H2 headings")
        
        # Hierarchy check
        if h3_count > 0 and h2_count == 0:
            issues.append("❌ H3 without H2 - improper hierarchy")
            self.semantic_issues.append(f"{title}: H3 without H2")
        
        return {
            'h1_count': h1_count,
            'h2_count': h2_count,
            'h3_count': h3_count,
            'h4_count': h4_count,
            'h1_valid': h1_count == 1,
            'hierarchy_valid': not (h3_count > 0 and h2_count == 0),
            'issues': issues
        }
    
    def analyze_seo_basics(self, title, content):
        """Basic SEO analysis"""
        issues = []
        
        # Title length
        title_length = len(title)
        if title_length < 30:
            issues.append(f"⚠️ Title short ({title_length} chars)")
            self.seo_issues.append(f"{title}: Short title")
        elif title_length > 60:
            issues.append(f"⚠️ Title long ({title_length} chars)")
            self.seo_issues.append(f"{title}: Long title")
        else:
            issues.append(f"✅ Title optimal ({title_length} chars)")
        
        # Content length
        content_text = re.sub(r'<[^>]+>', '', content)
        word_count = len(content_text.split())
        
        if word_count < 100:
            issues.append(f"❌ Extremely thin content ({word_count} words)")
            self.seo_issues.append(f"{title}: Extremely thin content")
        elif word_count < 300:
            issues.append(f"⚠️ Thin content ({word_count} words)")
            self.seo_issues.append(f"{title}: Thin content")
        else:
            issues.append(f"✅ Content sufficient ({word_count} words)")
        
        # Basic keyword check
        target_keywords = ['renovation', 'reno', 'warriors', 'australia', 'kitchen', 'bathroom']
        found_keywords = [kw for kw in target_keywords if kw.lower() in title.lower() or kw.lower() in content.lower()]
        
        if found_keywords:
            issues.append(f"✅ Keywords found: {len(found_keywords)}")
        else:
            issues.append("⚠️ No target keywords found")
        
        return {
            'title_length': title_length,
            'word_count': word_count,
            'found_keywords': len(found_keywords),
            'issues': issues
        }
    
    def get_pages_batch(self, limit=50, offset=0):
        """Get pages in batches to avoid memory issues"""
        query = f"""
        SELECT ID, post_title, SUBSTRING(post_content, 1, 5000) as content_preview, 
               post_status, post_type, LENGTH(post_content) as content_length
        FROM {self.wp_prefix}posts 
        WHERE post_type IN ('page', 'post') 
        AND post_status IN ('publish', 'draft', 'private')
        ORDER BY post_type, ID
        LIMIT {limit} OFFSET {offset};
        """
        
        stdout, stderr = self.execute_mysql_query(query)
        
        if stderr and "Warning: Permanently added" not in stderr:
            return []
        
        if not stdout or "Empty set" in stdout:
            return []
        
        lines = stdout.split('\n')
        if len(lines) < 2:
            return []
        
        pages = []
        for line in lines[1:]:  # Skip header
            if line.strip():
                # Handle tab-separated values more carefully
                parts = line.split('\t')
                if len(parts) >= 6:
                    try:
                        pages.append({
                            'id': parts[0],
                            'title': parts[1] if parts[1] != 'NULL' else 'Untitled',
                            'content': parts[2] if parts[2] != 'NULL' else '',
                            'status': parts[3] if parts[3] != 'NULL' else 'unknown',
                            'type': parts[4] if parts[4] != 'NULL' else 'unknown',
                            'content_length': int(parts[5]) if parts[5].isdigit() else 0
                        })
                    except (IndexError, ValueError) as e:
                        continue
        
        return pages
    
    def review_page_summary(self, page):
        """Quick page review for summary"""
        page_id = page['id']
        title = page['title']
        content = page['content']
        status = page['status']
        page_type = page['type']
        
        print(f"📄 {page_type.upper()} {page_id}: {title[:50]}... | Status: {status}")
        
        # Quick heading analysis
        heading_analysis = self.analyze_heading_structure(content, title)
        
        # Quick SEO analysis
        seo_analysis = self.analyze_seo_basics(title, content)
        
        # Show key issues
        critical_count = len([i for i in heading_analysis['issues'] + seo_analysis['issues'] if i.startswith('❌')])
        warning_count = len([i for i in heading_analysis['issues'] + seo_analysis['issues'] if i.startswith('⚠️')])
        
        if critical_count > 0:
            print(f"   ❌ {critical_count} critical issues")
            for issue in heading_analysis['issues'] + seo_analysis['issues']:
                if issue.startswith('❌'):
                    print(f"      {issue}")
        elif warning_count > 0:
            print(f"   ⚠️ {warning_count} warnings")
        else:
            print("   ✅ No major issues")
        
        return {
            'page_id': page_id,
            'title': title,
            'type': page_type,
            'status': status,
            'h1_valid': heading_analysis['h1_valid'],
            'hierarchy_valid': heading_analysis['hierarchy_valid'],
            'title_length': seo_analysis['title_length'],
            'word_count': seo_analysis['word_count'],
            'critical_issues': critical_count,
            'warning_issues': warning_count
        }
    
    def run_site_review(self):
        """Run comprehensive site review"""
        print("🏠 RENO WARRIORS COMPREHENSIVE SITE REVIEW")
        print("📊 SEO & Semantic HTML Structure Analysis")
        print("=" * 60)
        
        all_results = []
        offset = 0
        batch_size = 20
        
        while True:
            print(f"\n📋 Fetching pages {offset+1} to {offset+batch_size}...")
            pages = self.get_pages_batch(batch_size, offset)
            
            if not pages:
                break
            
            print(f"✅ Found {len(pages)} pages in this batch")
            
            for i, page in enumerate(pages, offset + 1):
                print(f"\n[{i}] ", end="")
                result = self.review_page_summary(page)
                all_results.append(result)
            
            offset += batch_size
            
            # Stop if we got fewer pages than requested (end of results)
            if len(pages) < batch_size:
                break
        
        # Generate comprehensive summary
        self.generate_final_summary(all_results)
        
        return all_results
    
    def generate_final_summary(self, results):
        """Generate final summary report"""
        print("\n" + "=" * 60)
        print("📊 RENO WARRIORS SITE-WIDE SUMMARY")
        print("=" * 60)
        
        if not results:
            print("❌ No pages analyzed")
            return
        
        total_pages = len(results)
        
        # Overall health
        excellent_pages = len([r for r in results if r['critical_issues'] == 0 and r['warning_issues'] == 0])
        good_pages = len([r for r in results if r['critical_issues'] == 0 and r['warning_issues'] > 0])
        critical_pages = len([r for r in results if r['critical_issues'] > 0])
        
        print(f"\n📈 SITE HEALTH OVERVIEW:")
        print(f"   Total pages: {total_pages}")
        print(f"   🎉 Excellent: {excellent_pages} ({excellent_pages/total_pages*100:.1f}%)")
        print(f"   👍 Good: {good_pages} ({good_pages/total_pages*100:.1f}%)")
        print(f"   ❌ Critical issues: {critical_pages} ({critical_pages/total_pages*100:.1f}%)")
        
        # H1 Structure Analysis
        h1_perfect = len([r for r in results if r['h1_valid']])
        h1_issues = total_pages - h1_perfect
        
        print(f"\n🔤 H1 STRUCTURE COMPLIANCE:")
        print(f"   ✅ Perfect H1 structure: {h1_perfect}/{total_pages} ({h1_perfect/total_pages*100:.1f}%)")
        if h1_issues > 0:
            print(f"   ❌ H1 issues: {h1_issues} pages need attention")
        
        # Content Quality
        thin_content = len([r for r in results if r['word_count'] < 300])
        very_thin = len([r for r in results if r['word_count'] < 100])
        
        print(f"\n📝 CONTENT QUALITY:")
        if very_thin > 0:
            print(f"   ❌ Extremely thin content: {very_thin} pages (<100 words)")
        if thin_content > 0:
            print(f"   ⚠️ Thin content: {thin_content} pages (<300 words)")
        
        good_content = total_pages - thin_content
        print(f"   ✅ Adequate content: {good_content}/{total_pages} ({good_content/total_pages*100:.1f}%)")
        
        # Page Type Breakdown
        print(f"\n📄 PAGE TYPE BREAKDOWN:")
        page_types = {}
        for result in results:
            page_type = result['type']
            if page_type not in page_types:
                page_types[page_type] = {'total': 0, 'issues': 0}
            page_types[page_type]['total'] += 1
            if result['critical_issues'] > 0:
                page_types[page_type]['issues'] += 1
        
        for page_type, stats in page_types.items():
            total = stats['total']
            issues = stats['issues']
            print(f"   {page_type.upper()}: {total} pages | {issues} with critical issues")
        
        # Critical Issues Summary
        print(f"\n🚨 CRITICAL ISSUES FOUND:")
        print(f"   Total unique critical issues: {len(self.critical_issues)}")
        print(f"   Total unique SEO issues: {len(self.seo_issues)}")
        print(f"   Total unique semantic issues: {len(self.semantic_issues)}")
        
        if self.critical_issues:
            print(f"\n   Top critical issues:")
            for issue in list(set(self.critical_issues))[:5]:
                print(f"      - {issue}")
        
        # Recommendations
        print(f"\n💡 PRIORITY RECOMMENDATIONS:")
        
        if h1_issues > 0:
            print(f"   1. 🚨 URGENT: Fix H1 structure on {h1_issues} pages")
        
        if very_thin > 0:
            print(f"   2. 🚨 URGENT: Expand extremely thin content on {very_thin} pages")
        
        if thin_content > 0:
            print(f"   3. ⚠️ Expand thin content on {thin_content} pages (aim for 500+ words)")
        
        print(f"\n📈 SEO OPTIMIZATION OPPORTUNITIES:")
        print("   - Add meta descriptions to all pages")
        print("   - Optimize page titles (50-60 characters)")
        print("   - Increase internal linking")
        print("   - Add schema markup for local business")
        print("   - Improve image alt text coverage")
        
        print(f"\n🏗️ SEMANTIC HTML IMPROVEMENTS:")
        print("   - Ensure proper heading hierarchy (H1→H2→H3)")
        print("   - Add HTML5 semantic elements (article, section)")
        print("   - Improve accessibility attributes")
        print("   - Validate Gutenberg block structure")
        
        # Health Score
        health_score = ((excellent_pages + good_pages) / total_pages) * 100
        
        print(f"\n📊 OVERALL SITE HEALTH SCORE: {health_score:.1f}%")
        
        if health_score >= 90:
            print("   🎉 EXCELLENT - Site is in great shape!")
        elif health_score >= 75:
            print("   👍 GOOD - Minor improvements needed")
        elif health_score >= 60:
            print("   ⚠️ NEEDS WORK - Several issues to address")
        else:
            print("   ❌ CRITICAL - Major improvements required")
        
        print(f"\n✅ COMPREHENSIVE REVIEW COMPLETE!")
        print(f"📄 Analyzed: {total_pages} pages")
        
        return {
            'total_pages': total_pages,
            'health_score': health_score,
            'excellent_pages': excellent_pages,
            'critical_pages': critical_pages,
            'h1_issues': h1_issues,
            'thin_content': thin_content
        }

if __name__ == "__main__":
    reviewer = FixedSiteReview()
    reviewer.run_site_review()