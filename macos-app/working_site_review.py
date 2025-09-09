#!/usr/bin/env python3
"""
Working comprehensive site review for Reno Warriors
"""

import subprocess
import re
from html import unescape

class WorkingSiteReview:
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
        
        self.critical_h1_issues = []
        self.seo_issues = []
        self.semantic_issues = []
        self.all_results = []
        
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
    
    def analyze_page_content(self, page_id, title, content, status, page_type):
        """Analyze individual page content"""
        issues = []
        
        # H1 Analysis - CRITICAL for SEO
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
        h1_count = len(h1_matches)
        
        h1_status = "UNKNOWN"
        if h1_count == 0:
            issues.append("❌ CRITICAL: No H1 tag found")
            h1_status = "MISSING"
            self.critical_h1_issues.append(f"ID {page_id}: {title} - Missing H1")
        elif h1_count > 1:
            issues.append(f"❌ CRITICAL: {h1_count} H1 tags - DUPLICATE H1s!")
            h1_status = "DUPLICATE"
            self.critical_h1_issues.append(f"ID {page_id}: {title} - {h1_count} H1s")
            # Show the duplicate H1s
            clean_h1s = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h1_matches]
            issues.append(f"   H1s found: {clean_h1s}")
        else:
            clean_h1 = unescape(re.sub(r'<[^>]+>', '', h1_matches[0])).strip()
            issues.append(f"✅ Perfect H1: '{clean_h1[:50]}...'")
            h1_status = "PERFECT"
        
        # H2-H6 Structure
        h2_count = len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE))
        h3_count = len(re.findall(r'<h3[^>]*>', content, re.IGNORECASE))
        h4_count = len(re.findall(r'<h4[^>]*>', content, re.IGNORECASE))
        
        if h2_count == 0:
            issues.append("⚠️ No H2 headings - lacks content structure")
        else:
            issues.append(f"✅ {h2_count} H2 headings")
        
        # Hierarchy check
        hierarchy_valid = True
        if h3_count > 0 and h2_count == 0:
            issues.append("❌ SEMANTIC ERROR: H3 without H2")
            hierarchy_valid = False
            self.semantic_issues.append(f"ID {page_id}: {title} - H3 without H2")
        
        # Title SEO Analysis
        title_length = len(title)
        title_status = "UNKNOWN"
        if title_length < 30:
            issues.append(f"⚠️ Title too short ({title_length} chars)")
            title_status = "TOO_SHORT"
            self.seo_issues.append(f"ID {page_id}: {title} - Title too short")
        elif title_length > 60:
            issues.append(f"⚠️ Title too long ({title_length} chars)")
            title_status = "TOO_LONG"
            self.seo_issues.append(f"ID {page_id}: {title} - Title too long")
        else:
            issues.append(f"✅ Title optimal ({title_length} chars)")
            title_status = "OPTIMAL"
        
        # Content Analysis
        content_text = re.sub(r'<[^>]+>', '', content)
        content_text = re.sub(r'\\s+', ' ', content_text).strip()
        word_count = len(content_text.split())
        
        content_status = "UNKNOWN"
        if word_count < 50:
            issues.append(f"❌ CRITICAL: Extremely thin content ({word_count} words)")
            content_status = "EXTREMELY_THIN"
            self.seo_issues.append(f"ID {page_id}: {title} - Extremely thin content")
        elif word_count < 200:
            issues.append(f"⚠️ Very thin content ({word_count} words)")
            content_status = "VERY_THIN"
            self.seo_issues.append(f"ID {page_id}: {title} - Very thin content")
        elif word_count < 300:
            issues.append(f"⚠️ Thin content ({word_count} words)")
            content_status = "THIN"
        else:
            issues.append(f"✅ Content sufficient ({word_count} words)")
            content_status = "SUFFICIENT"
        
        # Gutenberg Block Check
        gutenberg_blocks = content.count('<!-- wp:')
        gutenberg_closes = content.count('<!-- /wp:')
        
        gutenberg_status = "UNKNOWN"
        if gutenberg_blocks == 0:
            issues.append("⚠️ No Gutenberg blocks")
            gutenberg_status = "NO_BLOCKS"
        elif gutenberg_blocks != gutenberg_closes:
            issues.append(f"❌ Broken Gutenberg structure: {gutenberg_blocks} open, {gutenberg_closes} close")
            gutenberg_status = "BROKEN"
            self.semantic_issues.append(f"ID {page_id}: {title} - Broken Gutenberg structure")
        else:
            issues.append(f"✅ {gutenberg_blocks} Gutenberg blocks")
            gutenberg_status = "VALID"
        
        # Calculate severity
        critical_issues = len([i for i in issues if i.startswith('❌')])
        warning_issues = len([i for i in issues if i.startswith('⚠️')])
        
        # Overall assessment
        if critical_issues == 0 and warning_issues == 0:
            overall_score = "EXCELLENT"
        elif critical_issues == 0 and warning_issues <= 2:
            overall_score = "GOOD"
        elif critical_issues == 0:
            overall_score = "NEEDS_IMPROVEMENT"
        else:
            overall_score = "CRITICAL_ISSUES"
        
        return {
            'page_id': page_id,
            'title': title,
            'type': page_type,
            'status': status,
            'h1_status': h1_status,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'h3_count': h3_count,
            'hierarchy_valid': hierarchy_valid,
            'title_status': title_status,
            'title_length': title_length,
            'content_status': content_status,
            'word_count': word_count,
            'gutenberg_status': gutenberg_status,
            'gutenberg_blocks': gutenberg_blocks,
            'critical_issues': critical_issues,
            'warning_issues': warning_issues,
            'overall_score': overall_score,
            'issues': issues
        }
    
    def get_page_content(self, page_id):
        """Get full content for a specific page"""
        query = f"SELECT post_content FROM {self.wp_prefix}posts WHERE ID = {page_id};"
        stdout, stderr = self.execute_mysql_query(query)
        
        if stderr and "Warning: Permanently added" not in stderr:
            return ""
        
        lines = stdout.split('\\n')
        if len(lines) > 1:
            return lines[1] if lines[1] != 'NULL' else ""
        return ""
    
    def run_comprehensive_review(self):
        """Run comprehensive review of all pages"""
        print("🏠 RENO WARRIORS COMPREHENSIVE SITE REVIEW")
        print("🔍 SEO & Semantic HTML Structure Analysis")
        print("=" * 70)
        
        # First, get all pages summary
        print("📋 Fetching all pages...")
        
        query = f"""
        SELECT ID, post_title, post_status, post_type, LENGTH(post_content) as content_length
        FROM {self.wp_prefix}posts 
        WHERE post_type IN ('page', 'post') 
        AND post_status IN ('publish', 'draft', 'private')
        AND post_title NOT LIKE '%Auto Draft%'
        ORDER BY post_type, post_status, ID;
        """
        
        stdout, stderr = self.execute_mysql_query(query)
        
        if stderr and "Warning: Permanently added" not in stderr:
            print(f"❌ Database error: {stderr}")
            return
        
        if not stdout or "Empty set" in stdout:
            print("❌ No pages found")
            return
        
        lines = stdout.split('\\n')
        if len(lines) < 2:
            print("❌ No data returned")
            return
        
        # Parse page data
        pages = []
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.split('\\t')
                if len(parts) >= 5:
                    pages.append({
                        'id': parts[0],
                        'title': parts[1] if parts[1] != 'NULL' else 'Untitled',
                        'status': parts[2] if parts[2] != 'NULL' else 'unknown',
                        'type': parts[3] if parts[3] != 'NULL' else 'unknown',
                        'content_length': int(parts[4]) if parts[4].isdigit() else 0
                    })
        
        print(f"✅ Found {len(pages)} pages to analyze")
        
        # Show page breakdown
        page_types = {}
        for page in pages:
            page_type = page['type']
            if page_type not in page_types:
                page_types[page_type] = 0
            page_types[page_type] += 1
        
        print("📊 Page breakdown:")
        for page_type, count in page_types.items():
            print(f"   {page_type.upper()}: {count} pages")
        
        # Analyze each page
        print(f"\\n🔍 Analyzing each page...")
        
        for i, page in enumerate(pages, 1):
            page_id = page['id']
            title = page['title']
            status = page['status']
            page_type = page['type']
            
            print(f"\\n[{i}/{len(pages)}] 📄 {page_type.upper()} {page_id}: {title[:40]}...")
            print(f"    Status: {status} | Content Length: {page['content_length']} chars")
            
            # Get full content for this page
            content = self.get_page_content(page_id)
            
            if not content:
                print("    ⚠️ No content found - skipping detailed analysis")
                continue
            
            # Analyze this page
            result = self.analyze_page_content(page_id, title, content, status, page_type)
            self.all_results.append(result)
            
            # Show key findings
            for issue in result['issues']:
                print(f"    {issue}")
            
            print(f"    📊 Overall: {result['overall_score']}")
        
        # Generate comprehensive summary
        self.generate_comprehensive_summary()
    
    def generate_comprehensive_summary(self):
        """Generate final comprehensive summary"""
        print("\\n" + "=" * 70)
        print("📊 COMPREHENSIVE RENO WARRIORS SITE ANALYSIS")
        print("=" * 70)
        
        if not self.all_results:
            print("❌ No pages analyzed")
            return
        
        total_pages = len(self.all_results)
        
        # Overall Health Score
        excellent = len([p for p in self.all_results if p['overall_score'] == 'EXCELLENT'])
        good = len([p for p in self.all_results if p['overall_score'] == 'GOOD'])
        needs_improvement = len([p for p in self.all_results if p['overall_score'] == 'NEEDS_IMPROVEMENT'])
        critical = len([p for p in self.all_results if p['overall_score'] == 'CRITICAL_ISSUES'])
        
        health_score = ((excellent + good) / total_pages) * 100
        
        print(f"\\n📈 SITE HEALTH OVERVIEW:")
        print(f"   Total pages analyzed: {total_pages}")
        print(f"   🎉 Excellent: {excellent} ({excellent/total_pages*100:.1f}%)")
        print(f"   👍 Good: {good} ({good/total_pages*100:.1f}%)")
        print(f"   ⚠️ Needs improvement: {needs_improvement} ({needs_improvement/total_pages*100:.1f}%)")
        print(f"   ❌ Critical issues: {critical} ({critical/total_pages*100:.1f}%)")
        print(f"   🏆 Overall Health Score: {health_score:.1f}%")
        
        # H1 Structure Analysis - CRITICAL for SEO
        print(f"\\n🔤 H1 STRUCTURE COMPLIANCE (CRITICAL FOR SEO):")
        
        h1_perfect = len([p for p in self.all_results if p['h1_status'] == 'PERFECT'])
        h1_missing = len([p for p in self.all_results if p['h1_status'] == 'MISSING'])
        h1_duplicate = len([p for p in self.all_results if p['h1_status'] == 'DUPLICATE'])
        
        print(f"   ✅ Perfect H1 structure: {h1_perfect}/{total_pages} ({h1_perfect/total_pages*100:.1f}%)")
        
        if h1_missing > 0:
            print(f"   ❌ CRITICAL: {h1_missing} pages MISSING H1 tags:")
            missing_pages = [p for p in self.all_results if p['h1_status'] == 'MISSING']
            for page in missing_pages[:5]:  # Show first 5
                print(f"      - ID {page['page_id']}: {page['title']}")
            if len(missing_pages) > 5:
                print(f"      ... and {len(missing_pages) - 5} more")
        
        if h1_duplicate > 0:
            print(f"   ❌ CRITICAL: {h1_duplicate} pages with DUPLICATE H1s:")
            duplicate_pages = [p for p in self.all_results if p['h1_status'] == 'DUPLICATE']
            for page in duplicate_pages[:5]:  # Show first 5
                print(f"      - ID {page['page_id']}: {page['title']} ({page['h1_count']} H1s)")
            if len(duplicate_pages) > 5:
                print(f"      ... and {len(duplicate_pages) - 5} more")
        
        if h1_missing == 0 and h1_duplicate == 0:
            print("   🎉 ALL PAGES: Perfect H1 structure!")
        
        # Content Quality Analysis
        print(f"\\n📝 CONTENT QUALITY ANALYSIS:")
        
        extremely_thin = len([p for p in self.all_results if p['content_status'] == 'EXTREMELY_THIN'])
        very_thin = len([p for p in self.all_results if p['content_status'] == 'VERY_THIN'])
        thin = len([p for p in self.all_results if p['content_status'] == 'THIN'])
        sufficient = len([p for p in self.all_results if p['content_status'] == 'SUFFICIENT'])
        
        print(f"   ✅ Sufficient content: {sufficient}/{total_pages} ({sufficient/total_pages*100:.1f}%)")
        
        if extremely_thin > 0:
            print(f"   ❌ CRITICAL: {extremely_thin} pages with extremely thin content (<50 words)")
        if very_thin > 0:
            print(f"   ⚠️ {very_thin} pages with very thin content (<200 words)")
        if thin > 0:
            print(f"   ⚠️ {thin} pages with thin content (<300 words)")
        
        # SEO Title Analysis
        print(f"\\n🏷️ SEO TITLE ANALYSIS:")
        
        title_optimal = len([p for p in self.all_results if p['title_status'] == 'OPTIMAL'])
        title_short = len([p for p in self.all_results if p['title_status'] == 'TOO_SHORT'])
        title_long = len([p for p in self.all_results if p['title_status'] == 'TOO_LONG'])
        
        print(f"   ✅ Optimal title length: {title_optimal}/{total_pages} ({title_optimal/total_pages*100:.1f}%)")
        
        if title_short > 0:
            print(f"   ⚠️ {title_short} pages with titles too short (<30 chars)")
        if title_long > 0:
            print(f"   ⚠️ {title_long} pages with titles too long (>60 chars)")
        
        # Semantic HTML Structure
        print(f"\\n🏗️ SEMANTIC HTML STRUCTURE:")
        
        gutenberg_valid = len([p for p in self.all_results if p['gutenberg_status'] == 'VALID'])
        gutenberg_broken = len([p for p in self.all_results if p['gutenberg_status'] == 'BROKEN'])
        hierarchy_valid = len([p for p in self.all_results if p['hierarchy_valid']])
        
        print(f"   ✅ Valid Gutenberg structure: {gutenberg_valid}/{total_pages} ({gutenberg_valid/total_pages*100:.1f}%)")
        print(f"   ✅ Valid heading hierarchy: {hierarchy_valid}/{total_pages} ({hierarchy_valid/total_pages*100:.1f}%)")
        
        if gutenberg_broken > 0:
            print(f"   ❌ {gutenberg_broken} pages with broken Gutenberg structure")
        
        # Page Type Performance
        print(f"\\n📄 PAGE TYPE PERFORMANCE:")
        
        type_stats = {}
        for result in self.all_results:
            page_type = result['type']
            if page_type not in type_stats:
                type_stats[page_type] = {'total': 0, 'excellent': 0, 'critical': 0}
            
            type_stats[page_type]['total'] += 1
            if result['overall_score'] == 'EXCELLENT':
                type_stats[page_type]['excellent'] += 1
            elif result['overall_score'] == 'CRITICAL_ISSUES':
                type_stats[page_type]['critical'] += 1
        
        for page_type, stats in type_stats.items():
            total = stats['total']
            excellent = stats['excellent']
            critical = stats['critical']
            print(f"   {page_type.upper()}: {total} total | ✅{excellent} excellent | ❌{critical} critical")
        
        # Critical Action Items
        print(f"\\n🚨 CRITICAL ACTION ITEMS (URGENT):")
        
        action_count = 1
        if h1_missing > 0:
            print(f"   {action_count}. Add H1 tags to {h1_missing} pages (CRITICAL for SEO)")
            action_count += 1
        
        if h1_duplicate > 0:
            print(f"   {action_count}. Fix duplicate H1s on {h1_duplicate} pages (CRITICAL for SEO)")
            action_count += 1
        
        if extremely_thin > 0:
            print(f"   {action_count}. Expand extremely thin content on {extremely_thin} pages")
            action_count += 1
        
        if gutenberg_broken > 0:
            print(f"   {action_count}. Fix broken Gutenberg structure on {gutenberg_broken} pages")
            action_count += 1
        
        if action_count == 1:
            print("   🎉 NO CRITICAL ACTIONS NEEDED - Site structure is excellent!")
        
        # SEO Optimization Opportunities
        print(f"\\n📈 SEO OPTIMIZATION OPPORTUNITIES:")
        print("   - Add meta descriptions to all pages (150-160 characters)")
        print("   - Optimize page titles for target keywords")
        print("   - Increase internal linking between related pages")
        print("   - Add schema markup for local business")
        print("   - Optimize images with descriptive alt text")
        print("   - Create location-specific landing pages")
        print("   - Add FAQ sections to service pages")
        
        # Semantic HTML Improvements
        print(f"\\n🏗️ SEMANTIC HTML IMPROVEMENTS:")
        print("   - Ensure proper heading hierarchy (H1→H2→H3)")
        print("   - Add HTML5 semantic elements (article, section, aside)")
        print("   - Improve accessibility attributes (aria-labels, roles)")
        print("   - Validate all Gutenberg block structures")
        print("   - Add landmarks for screen readers")
        
        # Final Assessment
        print(f"\\n🏆 FINAL ASSESSMENT:")
        
        if health_score >= 90:
            print(f"   🎉 EXCELLENT SITE HEALTH ({health_score:.1f}%)")
            print("   Your site has excellent SEO and semantic structure!")
        elif health_score >= 75:
            print(f"   👍 GOOD SITE HEALTH ({health_score:.1f}%)")
            print("   Minor improvements will make your site even better.")
        elif health_score >= 60:
            print(f"   ⚠️ NEEDS IMPROVEMENT ({health_score:.1f}%)")
            print("   Several issues need attention for optimal SEO performance.")
        else:
            print(f"   ❌ CRITICAL IMPROVEMENTS NEEDED ({health_score:.1f}%)")
            print("   Major structural issues are impacting SEO performance.")
        
        print(f"\\n✅ COMPREHENSIVE REVIEW COMPLETE!")
        print(f"📊 Total Issues Found:")
        print(f"   - Critical H1 issues: {len(self.critical_h1_issues)}")
        print(f"   - SEO issues: {len(self.seo_issues)}")
        print(f"   - Semantic issues: {len(self.semantic_issues)}")
        
        return {
            'total_pages': total_pages,
            'health_score': health_score,
            'h1_issues': h1_missing + h1_duplicate,
            'content_issues': extremely_thin + very_thin + thin,
            'critical_actions': action_count - 1
        }

if __name__ == "__main__":
    reviewer = WorkingSiteReview()
    reviewer.run_comprehensive_review()