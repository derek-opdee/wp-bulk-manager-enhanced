#!/usr/bin/env python3
"""
WP Bulk Manager Assistant Mode
Designed for Claude to help manage WordPress sites
"""

from wpbm_cli_enhanced import EnhancedWPBulkManager
import requests
import json
from datetime import datetime
import re
from typing import Dict, List, Tuple

class WPBulkAssistant:
    """Assistant class for Claude to manage WordPress sites"""
    
    def __init__(self):
        self.manager = EnhancedWPBulkManager()
        self.current_site = None
        self.current_site_id = None
    
    def get_site_status(self) -> Dict:
        """Get comprehensive status of the current site"""
        if not self.current_site:
            return {"error": "No site selected"}
        
        status = {
            "site": self.current_site,
            "content_summary": self.get_content_summary(),
            "seo_issues": self.analyze_seo_issues(),
            "plugin_updates": self.check_plugin_updates(),
            "theme_updates": self.check_theme_updates()
        }
        
        return status
    
    def get_content_summary(self) -> Dict:
        """Get summary of all content"""
        content = self.manager.list_all_content(self.current_site_id, 'any', 500)
        
        summary = {
            "total": len(content),
            "pages": len([c for c in content if c['type'] == 'page']),
            "posts": len([c for c in content if c['type'] == 'post']),
            "published": len([c for c in content if c['status'] == 'publish']),
            "drafts": len([c for c in content if c['status'] == 'draft']),
            "recent_updates": []
        }
        
        # Sort by modified date
        sorted_content = sorted(content, key=lambda x: x['modified'], reverse=True)
        
        # Get 10 most recent
        for item in sorted_content[:10]:
            summary["recent_updates"].append({
                "id": item['id'],
                "title": item['title'],
                "type": item['type'],
                "modified": item['modified'],
                "url": item['permalink']
            })
        
        return summary
    
    def analyze_seo_issues(self) -> List[Dict]:
        """Analyze SEO and return recommendations"""
        seo_data = self.manager.get_all_seo_data(self.current_site_id, 200)
        issues = []
        
        for page in seo_data:
            page_issues = []
            
            # Check title
            if not page['seo_title']:
                page_issues.append({
                    "type": "missing_title",
                    "severity": "high",
                    "message": "No custom SEO title set"
                })
            elif len(page['seo_title']) > 60:
                page_issues.append({
                    "type": "title_too_long",
                    "severity": "medium",
                    "message": f"Title is {len(page['seo_title'])} chars (recommended: 50-60)"
                })
            elif len(page['seo_title']) < 30:
                page_issues.append({
                    "type": "title_too_short",
                    "severity": "medium",
                    "message": f"Title is {len(page['seo_title'])} chars (recommended: 30-60)"
                })
            
            # Check description
            if not page['seo_description']:
                page_issues.append({
                    "type": "missing_description",
                    "severity": "high",
                    "message": "No custom SEO description set"
                })
            elif len(page['seo_description']) > 160:
                page_issues.append({
                    "type": "description_too_long",
                    "severity": "medium",
                    "message": f"Description is {len(page['seo_description'])} chars (recommended: 120-160)"
                })
            elif len(page['seo_description']) < 120:
                page_issues.append({
                    "type": "description_too_short",
                    "severity": "medium",
                    "message": f"Description is {len(page['seo_description'])} chars (recommended: 120-160)"
                })
            
            if page_issues:
                issues.append({
                    "page_id": page['id'],
                    "page_title": page['title'],
                    "url": page['url'],
                    "issues": page_issues
                })
        
        return issues
    
    def check_plugin_updates(self) -> Dict:
        """Check for available plugin updates"""
        plugins = self.manager.get_plugins(self.current_site_id)
        
        # In real implementation, would check for updates
        # For now, return plugin list
        return {
            "total_plugins": len(plugins),
            "active_plugins": len([p for p in plugins if p['active']]),
            "plugins": plugins
        }
    
    def check_theme_updates(self) -> Dict:
        """Check for available theme updates"""
        themes = self.manager.get_themes(self.current_site_id)
        
        return {
            "total_themes": len(themes),
            "active_theme": next((t for t in themes if t['active']), None),
            "themes": themes
        }
    
    def get_page_content(self, page_id: int) -> Dict:
        """Get detailed page content for review"""
        return self.manager.get_content_details(self.current_site_id, page_id)
    
    def recommend_seo_improvements(self, page_id: int) -> Dict:
        """Generate SEO recommendations for a specific page"""
        content = self.get_page_content(page_id)
        if not content:
            return {"error": "Page not found"}
        
        recommendations = []
        
        # Analyze title
        title = content['title']
        seo_title = content['seo'].get('title', '')
        
        if not seo_title:
            # Generate recommendation
            if len(title) > 60:
                rec_title = title[:57] + "..."
            else:
                rec_title = title
            recommendations.append({
                "field": "seo_title",
                "current": "",
                "recommended": rec_title,
                "reason": "No SEO title set, using page title"
            })
        
        # Analyze content for keywords
        text_content = re.sub('<[^<]+?>', '', content['content'])
        words = text_content.lower().split()
        
        # Find most common meaningful words (simple keyword extraction)
        common_words = ['the', 'and', 'a', 'an', 'is', 'it', 'to', 'of', 'in', 'for', 'on', 'with']
        word_freq = {}
        for word in words:
            if len(word) > 3 and word not in common_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Generate description recommendation
        if not content['seo'].get('description'):
            # Extract first paragraph
            paragraphs = re.findall(r'<p>(.*?)</p>', content['content'])
            if paragraphs:
                first_para = re.sub('<[^<]+?>', '', paragraphs[0])
                if len(first_para) > 160:
                    rec_desc = first_para[:157] + "..."
                else:
                    rec_desc = first_para
                
                recommendations.append({
                    "field": "seo_description",
                    "current": "",
                    "recommended": rec_desc,
                    "reason": "Generated from first paragraph"
                })
        
        return {
            "page_id": page_id,
            "title": title,
            "url": content['permalink'],
            "top_keywords": [kw[0] for kw in top_keywords],
            "recommendations": recommendations
        }
    
    def update_page_seo(self, page_id: int, seo_data: Dict) -> bool:
        """Update SEO data for a page"""
        return self.manager.update_seo(self.current_site_id, page_id, seo_data)
    
    def update_page_content(self, page_id: int, updates: Dict) -> bool:
        """Update page content"""
        page = self.get_page_content(page_id)
        if not page:
            return False
        
        return self.manager.update_content(
            self.current_site_id,
            page['type'],
            page_id,
            updates
        )
    
    def bulk_seo_update(self, updates: List[Dict]) -> List[Dict]:
        """Perform bulk SEO updates"""
        results = []
        
        for update in updates:
            success = self.update_page_seo(update['page_id'], update['seo_data'])
            results.append({
                "page_id": update['page_id'],
                "success": success
            })
        
        return results
    
    def select_site(self, site_name: str = None) -> bool:
        """Select a site to work with"""
        sites = self.manager.get_sites('active')
        
        if site_name:
            # Find site by name
            site = next((s for s in sites if s['name'].lower() == site_name.lower()), None)
            if site:
                self.current_site = site
                self.current_site_id = site['id']
                return True
        elif len(sites) == 1:
            # Auto-select if only one site
            self.current_site = sites[0]
            self.current_site_id = sites[0]['id']
            return True
        
        return False
    
    def generate_report(self) -> str:
        """Generate a comprehensive report"""
        if not self.current_site:
            return "No site selected"
        
        report = f"# WP Bulk Manager Report for {self.current_site['name']}\n"
        report += f"URL: {self.current_site['url']}\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Content Summary
        summary = self.get_content_summary()
        report += "## Content Summary\n"
        report += f"- Total Pages/Posts: {summary['total']}\n"
        report += f"- Pages: {summary['pages']}\n"
        report += f"- Posts: {summary['posts']}\n"
        report += f"- Published: {summary['published']}\n"
        report += f"- Drafts: {summary['drafts']}\n\n"
        
        # SEO Issues
        seo_issues = self.analyze_seo_issues()
        report += "## SEO Issues Found\n"
        if seo_issues:
            report += f"Total pages with issues: {len(seo_issues)}\n\n"
            for issue in seo_issues[:10]:  # First 10
                report += f"### {issue['page_title']}\n"
                report += f"URL: {issue['url']}\n"
                for i in issue['issues']:
                    report += f"- {i['severity'].upper()}: {i['message']}\n"
                report += "\n"
        else:
            report += "No major SEO issues found!\n\n"
        
        # Plugin Status
        plugins = self.check_plugin_updates()
        report += "## Plugin Status\n"
        report += f"- Total Plugins: {plugins['total_plugins']}\n"
        report += f"- Active Plugins: {plugins['active_plugins']}\n\n"
        
        return report


# Helper functions for Claude to use

def wpbm_connect() -> WPBulkAssistant:
    """Initialize and connect to WP Bulk Manager"""
    assistant = WPBulkAssistant()
    if assistant.select_site("Opdee"):  # Auto-select Opdee if available
        print(f"Connected to {assistant.current_site['name']} ({assistant.current_site['url']})")
    return assistant

def wpbm_status(assistant: WPBulkAssistant) -> None:
    """Get current site status"""
    status = assistant.get_site_status()
    print(json.dumps(status, indent=2))

def wpbm_analyze_page(assistant: WPBulkAssistant, page_id: int) -> None:
    """Analyze a specific page"""
    content = assistant.get_page_content(page_id)
    recommendations = assistant.recommend_seo_improvements(page_id)
    
    print(f"Page: {content['title']}")
    print(f"URL: {content['permalink']}")
    print(f"Status: {content['status']}")
    print("\nSEO Recommendations:")
    print(json.dumps(recommendations, indent=2))

def wpbm_update_seo(assistant: WPBulkAssistant, page_id: int, title: str = None, description: str = None) -> None:
    """Update SEO for a page"""
    seo_data = {}
    if title:
        seo_data['title'] = title
    if description:
        seo_data['description'] = description
    
    if assistant.update_page_seo(page_id, seo_data):
        print(f"✅ SEO updated for page {page_id}")
    else:
        print(f"❌ Failed to update SEO for page {page_id}")

def wpbm_list_pages(assistant: WPBulkAssistant, limit: int = 20) -> None:
    """List all pages with SEO status"""
    content = assistant.manager.list_all_content(assistant.current_site_id, 'page', limit)
    
    print(f"Pages on {assistant.current_site['name']}:")
    print("-" * 80)
    for page in content:
        seo = page.get('seo', {})
        seo_status = "✓" if seo.get('title') and seo.get('description') else "✗"
        print(f"ID: {page['id']:<6} SEO: {seo_status} | {page['title']}")

def wpbm_generate_report(assistant: WPBulkAssistant) -> None:
    """Generate and display a site report"""
    report = assistant.generate_report()
    print(report)


if __name__ == "__main__":
    # Example usage for Claude
    print("WP Bulk Manager Assistant Mode")
    print("="*50)
    print("This mode is designed for Claude to help manage WordPress sites.")
    print("\nExample commands:")
    print("  assistant = wpbm_connect()")
    print("  wpbm_status(assistant)")
    print("  wpbm_list_pages(assistant)")
    print("  wpbm_analyze_page(assistant, 123)")
    print("  wpbm_update_seo(assistant, 123, title='New Title', description='New description')")
    print("  wpbm_generate_report(assistant)")
    
    # Auto-connect for testing
    assistant = wpbm_connect()
    if assistant.current_site:
        print(f"\n✅ Ready to manage {assistant.current_site['name']}")
        wpbm_generate_report(assistant)