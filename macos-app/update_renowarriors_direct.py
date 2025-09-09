#!/usr/bin/env python3
"""
Update RenoWarriors.com.au directly using WordPress REST API
"""

import requests
import json
import re
from typing import Dict, List
import base64

class RenoWarriorsUpdater:
    def __init__(self):
        self.base_url = "https://renowarriors.com.au/wp-json/wp/v2"
        # We'll need authentication - checking for application password
        self.session = requests.Session()
        
    def authenticate(self, username: str, app_password: str):
        """Setup authentication"""
        credentials = base64.b64encode(f"{username}:{app_password}".encode()).decode()
        self.session.headers.update({
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/json'
        })
    
    def check_plugins(self):
        """Check installed plugins via REST API"""
        print("\n1. Checking for SEO plugins...")
        
        # Try to access plugins endpoint (requires authentication)
        try:
            response = self.session.get(f"{self.base_url.replace('/wp/v2', '/wp/v2')}/plugins")
            if response.status_code == 200:
                plugins = response.json()
                for plugin in plugins:
                    if 'seo' in plugin['name'].lower():
                        print(f"  Found: {plugin['name']} (Status: {plugin['status']})")
            else:
                print("  Note: Cannot access plugins list without authentication")
                print("  Proceeding with SEO updates...")
        except:
            print("  Note: Plugins endpoint not accessible")
    
    def get_all_pages(self) -> List[Dict]:
        """Get all pages from the site"""
        print("\n2. Fetching all pages...")
        all_pages = []
        page = 1
        
        while True:
            response = self.session.get(
                f"{self.base_url}/pages",
                params={'per_page': 100, 'page': page, 'status': 'publish'}
            )
            
            if response.status_code != 200:
                break
                
            pages = response.json()
            if not pages:
                break
                
            all_pages.extend(pages)
            page += 1
        
        print(f"  Found {len(all_pages)} published pages")
        return all_pages
    
    def check_seo_framework(self, page_id: int) -> Dict:
        """Check if page has SEO Framework data"""
        try:
            # The SEO Framework stores data in post meta
            response = self.session.get(f"{self.base_url}/pages/{page_id}")
            if response.status_code == 200:
                page_data = response.json()
                
                # Check for SEO meta in the response
                meta = page_data.get('meta', {})
                
                # Common SEO Framework meta keys
                seo_title = meta.get('_genesis_title') or meta.get('_tsf_title_no_blogname')
                seo_desc = meta.get('_genesis_description') or meta.get('_tsf_description')
                
                return {
                    'has_seo': bool(seo_title or seo_desc),
                    'title': seo_title,
                    'description': seo_desc
                }
        except:
            pass
        
        return {'has_seo': False, 'title': None, 'description': None}
    
    def update_page_seo(self, page_id: int, title: str, description: str):
        """Update page SEO using Yoast or SEO Framework meta"""
        # Try updating via standard meta fields
        update_data = {
            'meta': {
                '_yoast_wpseo_title': title,
                '_yoast_wpseo_metadesc': description,
                # Also try SEO Framework fields
                '_tsf_title_no_blogname': title,
                '_tsf_description': description
            }
        }
        
        response = self.session.post(
            f"{self.base_url}/pages/{page_id}",
            json=update_data
        )
        
        return response.status_code == 200
    
    def fix_spelling_in_content(self, content: str) -> tuple[str, List[str]]:
        """Fix US to Australian spelling"""
        spelling_fixes = {
            'color': 'colour',
            'Color': 'Colour',
            'center': 'centre',
            'Center': 'Centre',
            'organize': 'organise',
            'Organize': 'Organise',
            'realize': 'realise',
            'Realize': 'Realise',
            'neighbor': 'neighbour',
            'Neighbor': 'Neighbour',
            'favor': 'favour',
            'Favor': 'Favour',
            'honor': 'honour',
            'Honor': 'Honour',
            'labor': 'labour',
            'Labor': 'Labour',
            'behavior': 'behaviour',
            'Behavior': 'Behaviour',
            'aluminum': 'aluminium',
            'Aluminum': 'Aluminium',
            'analyze': 'analyse',
            'Analyze': 'Analyse',
            'specialized': 'specialised',
            'Specialized': 'Specialised',
            'modernize': 'modernise',
            'Modernize': 'Modernise'
        }
        
        changes_made = []
        updated_content = content
        
        for us_spelling, au_spelling in spelling_fixes.items():
            if us_spelling in updated_content:
                # Use word boundary regex
                pattern = r'\b' + us_spelling + r'\b'
                updated_content = re.sub(pattern, au_spelling, updated_content)
                changes_made.append(f"{us_spelling} → {au_spelling}")
        
        return updated_content, changes_made
    
    def run_updates(self):
        """Run all updates"""
        # Southeast Melbourne suburbs
        se_melbourne_suburbs = [
            "Patterson Lakes", "Carrum", "Chelsea", "Bonbeach", "Frankston",
            "Seaford", "Carrum Downs", "Skye", "Sandhurst", "Cranbourne"
        ]
        
        # Check for plugins
        self.check_plugins()
        
        # Get all pages
        pages = self.get_all_pages()
        
        # Process pages for SEO
        print("\n3. Checking pages for missing SEO data...")
        pages_needing_seo = []
        
        for page in pages[:20]:  # Check first 20 pages
            seo_data = self.check_seo_framework(page['id'])
            if not seo_data['has_seo']:
                pages_needing_seo.append(page)
        
        print(f"  Found {len(pages_needing_seo)} pages potentially needing SEO data")
        
        # Update SEO for pages
        if pages_needing_seo:
            print("\n4. Updating SEO titles and descriptions...")
            
            for page in pages_needing_seo[:5]:  # Update first 5
                print(f"\n  Processing: {page['title']['rendered']}")
                
                # Generate SEO title
                page_title = page['title']['rendered']
                seo_title = f"{page_title} | Renovation Services Southeast Melbourne | RenoWarriors"
                
                # Generate SEO description
                # Extract text from content
                content_text = re.sub('<[^<]+?>', '', page['content']['rendered'])
                content_text = ' '.join(content_text.split())[:100]
                
                seo_description = f"Professional {page_title.lower()} services in Southeast Melbourne. "
                seo_description += f"Based in Patterson Lakes, VIC. Quality renovations for {', '.join(se_melbourne_suburbs[:3])} and surrounding suburbs."
                
                print(f"    SEO Title: {seo_title}")
                print(f"    SEO Description: {seo_description[:80]}...")
                
                # Note: Without authentication, we can't update
                print("    Note: Authentication required to update SEO data")
        
        # Check for US spelling
        print("\n5. Checking for US spelling to fix...")
        pages_with_us_spelling = []
        
        for page in pages[:10]:  # Check first 10 pages
            content = page['content']['rendered']
            _, changes = self.fix_spelling_in_content(content)
            if changes:
                pages_with_us_spelling.append({
                    'page': page,
                    'changes': changes
                })
        
        print(f"  Found {len(pages_with_us_spelling)} pages with US spelling")
        
        if pages_with_us_spelling:
            print("\n6. Pages with US spelling found:")
            for item in pages_with_us_spelling[:5]:
                page = item['page']
                changes = item['changes']
                print(f"\n  {page['title']['rendered']}:")
                print(f"    Changes needed: {', '.join(changes[:5])}")
                if len(changes) > 5:
                    print(f"    ... and {len(changes) - 5} more")
        
        # Summary
        print("\n" + "="*50)
        print("ANALYSIS COMPLETE")
        print("="*50)
        print(f"Site: RenoWarriors (https://renowarriors.com.au)")
        print(f"\nPages analyzed: {len(pages)}")
        print(f"Pages needing SEO: {len(pages_needing_seo)}")
        print(f"Pages with US spelling: {len(pages_with_us_spelling)}")
        print("\nNote: To complete the updates, authentication is required.")
        print("You'll need WordPress admin credentials or an application password.")

def main():
    updater = RenoWarriorsUpdater()
    
    print("RenoWarriors.com.au SEO and Spelling Update")
    print("="*50)
    
    # Check if we need authentication
    print("\nThis script can analyze the site without authentication,")
    print("but updates require WordPress admin access.")
    
    auth_choice = input("\nDo you have WordPress credentials? (y/n): ").lower()
    
    if auth_choice == 'y':
        username = input("WordPress username: ")
        app_password = input("Application password (or regular password): ")
        updater.authenticate(username, app_password)
        print("✅ Authentication configured")
    
    # Run the updates
    updater.run_updates()

if __name__ == "__main__":
    main()