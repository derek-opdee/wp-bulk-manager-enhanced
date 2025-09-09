#!/usr/bin/env python3
"""
WP Bulk Manager CLI - Enhanced Version
"""

from wpbm_manager import WPBulkManager, ContentProcessor
import json
import requests
from datetime import datetime
from typing import Dict, List
import textwrap

class EnhancedWPBulkManager(WPBulkManager):
    """Enhanced manager with additional API methods"""
    
    def list_all_content(self, site_id: int, content_type: str = 'any', limit: int = 100, search: str = None) -> List[Dict]:
        """List all content from a site"""
        site = self.get_site(site_id)
        if not site:
            return []
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return []
        
        params = {
            'type': content_type if content_type != 'any' else ['post', 'page'],
            'limit': limit,
            'status': 'any'
        }
        
        if search:
            params['search'] = search
        
        try:
            response = requests.get(
                f"{site['url']}/wp-json/wpbm/v1/content",
                headers={'X-API-Key': api_key},
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('posts', [])
        except:
            pass
        
        return []
    
    def duplicate_content(self, site_id: int, post_id: int) -> Dict:
        """Duplicate a post/page"""
        site = self.get_site(site_id)
        if not site:
            return {'success': False, 'error': 'Site not found'}
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return {'success': False, 'error': 'API key not found'}
        
        try:
            response = requests.post(
                f"{site['url']}/wp-json/wpbm/v1/content/{post_id}/duplicate",
                headers={'X-API-Key': api_key},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_content(self, site_id: int, post_id: int, force: bool = False) -> bool:
        """Delete content"""
        site = self.get_site(site_id)
        if not site:
            return False
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return False
        
        try:
            response = requests.delete(
                f"{site['url']}/wp-json/wpbm/v1/content/{post_id}",
                headers={'X-API-Key': api_key},
                params={'force': 'true' if force else 'false'},
                timeout=30
            )
            return response.status_code == 200
        except:
            return False
    
    def get_all_seo_data(self, site_id: int, limit: int = 100) -> List[Dict]:
        """Get all SEO data"""
        site = self.get_site(site_id)
        if not site:
            return []
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return []
        
        try:
            response = requests.get(
                f"{site['url']}/wp-json/wpbm/v1/seo",
                headers={'X-API-Key': api_key},
                params={'limit': limit},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('posts', [])
        except:
            pass
        
        return []
    
    def get_content_details(self, site_id: int, post_id: int) -> Dict:
        """Get detailed content including full text"""
        site = self.get_site(site_id)
        if not site:
            return None
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return None
        
        try:
            response = requests.get(
                f"{site['url']}/wp-json/wpbm/v1/content/{post_id}",
                headers={'X-API-Key': api_key},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        return None
    
    def get_plugins(self, site_id: int) -> List[Dict]:
        """Get all plugins"""
        site = self.get_site(site_id)
        if not site:
            return []
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return []
        
        try:
            response = requests.get(
                f"{site['url']}/wp-json/wpbm/v1/plugins",
                headers={'X-API-Key': api_key},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('plugins', [])
        except:
            pass
        
        return []
    
    def get_themes(self, site_id: int) -> List[Dict]:
        """Get all themes"""
        site = self.get_site(site_id)
        if not site:
            return []
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return []
        
        try:
            response = requests.get(
                f"{site['url']}/wp-json/wpbm/v1/themes",
                headers={'X-API-Key': api_key},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('themes', [])
        except:
            pass
        
        return []
    
    def get_seo_generator_pages(self, site_id: int) -> List[Dict]:
        """Get all SEO Generator pages"""
        site = self.get_site(site_id)
        if not site:
            return []
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return []
        
        try:
            response = requests.get(
                f"{site['url']}/wp-json/wpbm/v1/seo-generator/pages",
                headers={'X-API-Key': api_key},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('pages', [])
        except:
            pass
        
        return []
    
    def get_seo_generator_page(self, site_id: int, page_id: int) -> Dict:
        """Get SEO Generator page details"""
        site = self.get_site(site_id)
        if not site:
            return None
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return None
        
        try:
            response = requests.get(
                f"{site['url']}/wp-json/wpbm/v1/seo-generator/page/{page_id}",
                headers={'X-API-Key': api_key},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        return None
    
    def update_seo_generator_page(self, site_id: int, page_id: int, data: Dict) -> bool:
        """Update SEO Generator page settings"""
        site = self.get_site(site_id)
        if not site:
            return False
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return False
        
        try:
            response = requests.put(
                f"{site['url']}/wp-json/wpbm/v1/seo-generator/page/{page_id}",
                headers={'X-API-Key': api_key},
                json=data,
                timeout=30
            )
            
            return response.status_code == 200
        except:
            return False


def show_enhanced_menu():
    print("\n" + "="*60)
    print("WP BULK MANAGER - ENHANCED CLI")
    print("="*60)
    print("CONTENT MANAGEMENT:")
    print("  1. List All Pages/Posts")
    print("  2. View/Edit Content")
    print("  3. Duplicate Page/Post")
    print("  4. Delete Content")
    print("  5. Create Single Page/Post")
    print("  6. Bulk Create with Variables")
    
    print("\nSEO MANAGEMENT:")
    print("  7. View All SEO Titles/Descriptions")
    print("  8. Update SEO Data")
    
    print("\nSEO GENERATOR:")
    print("  9. List SEO Generator Pages")
    print(" 10. Manage SEO Generator Page")
    
    print("\nSITE MANAGEMENT:")
    print(" 11. List Plugins")
    print(" 12. List Themes")
    print(" 13. Update Plugins/Themes")
    
    print("\nOTHER:")
    print(" 14. List Connected Sites")
    print(" 15. Search Content")
    print(" 16. Exit")
    print("="*60)


def list_all_content(manager, site_id=None):
    """List all pages and posts"""
    if not site_id:
        site = select_site(manager)
        if not site:
            return
        site_id = site['id']
    
    print("\nContent Type:")
    print("1. Pages only")
    print("2. Posts only")
    print("3. All content")
    
    choice = input("Select option [3]: ") or '3'
    
    content_type = 'any'
    if choice == '1':
        content_type = 'page'
    elif choice == '2':
        content_type = 'post'
    
    print("\nFetching content...")
    content = manager.list_all_content(site_id, content_type)
    
    if not content:
        print("No content found.")
        return
    
    print(f"\nFound {len(content)} items:")
    print("-" * 100)
    print(f"{'ID':<8} {'Type':<8} {'Status':<10} {'Title':<40} {'Modified':<20}")
    print("-" * 100)
    
    for item in content:
        title = item['title'][:37] + '...' if len(item['title']) > 40 else item['title']
        modified = datetime.fromisoformat(item['modified'].replace('T', ' ').split('+')[0]).strftime('%Y-%m-%d %H:%M')
        
        print(f"{item['id']:<8} {item['type']:<8} {item['status']:<10} {title:<40} {modified:<20}")
    
    return content


def view_edit_content(manager):
    """View and edit content"""
    site = select_site(manager)
    if not site:
        return
    
    # First list content
    content = list_all_content(manager, site['id'])
    if not content:
        return
    
    try:
        post_id = int(input("\nEnter content ID to view/edit: "))
    except ValueError:
        print("Invalid ID.")
        return
    
    # Get full content
    print("\nFetching content details...")
    details = manager.get_content_details(site['id'], post_id)
    
    if not details:
        print("Content not found.")
        return
    
    print("\n" + "="*60)
    print(f"Title: {details['title']}")
    print(f"Type: {details['type']}")
    print(f"Status: {details['status']}")
    print(f"URL: {details['permalink']}")
    print("="*60)
    
    print("\nCONTENT:")
    print("-" * 60)
    # Strip HTML tags for display
    import re
    clean_content = re.sub('<[^<]+?>', '', details['content'])
    wrapped = textwrap.fill(clean_content, width=60)
    print(wrapped[:500] + '...' if len(wrapped) > 500 else wrapped)
    
    print("\n" + "-" * 60)
    print("\nSEO DATA:")
    seo = details.get('seo', {})
    print(f"SEO Title: {seo.get('title', 'Not set')}")
    print(f"SEO Description: {seo.get('description', 'Not set')}")
    
    print("\nOptions:")
    print("1. Edit title")
    print("2. Edit content")
    print("3. Edit SEO")
    print("4. Change status")
    print("5. Duplicate this page")
    print("6. Delete this page")
    print("7. Back")
    
    choice = input("\nSelect option: ")
    
    if choice == '1':
        new_title = input("New title: ")
        if new_title:
            result = manager.update_content(site['id'], details['type'], post_id, {'title': new_title})
            print("✅ Title updated!" if result else "❌ Update failed")
    
    elif choice == '2':
        print("Enter new content (HTML). Type 'END' on a new line when done:")
        content_lines = []
        while True:
            line = input()
            if line == 'END':
                break
            content_lines.append(line)
        new_content = '\n'.join(content_lines)
        
        if new_content:
            result = manager.update_content(site['id'], details['type'], post_id, {'content': new_content})
            print("✅ Content updated!" if result else "❌ Update failed")
    
    elif choice == '3':
        seo_title = input(f"SEO Title [{seo.get('title', '')}]: ") or seo.get('title', '')
        seo_desc = input(f"SEO Description [{seo.get('description', '')}]: ") or seo.get('description', '')
        
        if manager.update_seo(site['id'], post_id, {'title': seo_title, 'description': seo_desc}):
            print("✅ SEO updated!")
        else:
            print("❌ SEO update failed")
    
    elif choice == '4':
        print("Status options: draft, publish, private, trash")
        new_status = input("New status: ")
        if new_status in ['draft', 'publish', 'private', 'trash']:
            result = manager.update_content(site['id'], details['type'], post_id, {'status': new_status})
            print(f"✅ Status changed to {new_status}!" if result else "❌ Update failed")
    
    elif choice == '5':
        duplicate_content(manager, site['id'], post_id)
    
    elif choice == '6':
        if input("Are you sure? (yes/no): ").lower() == 'yes':
            if manager.delete_content(site['id'], post_id):
                print("✅ Content deleted!")
            else:
                print("❌ Delete failed")


def duplicate_content(manager, site_id=None, post_id=None):
    """Duplicate a page or post"""
    if not site_id:
        site = select_site(manager)
        if not site:
            return
        site_id = site['id']
    
    if not post_id:
        content = list_all_content(manager, site_id)
        if not content:
            return
        
        try:
            post_id = int(input("\nEnter content ID to duplicate: "))
        except ValueError:
            print("Invalid ID.")
            return
    
    print("\nDuplicating content...")
    result = manager.duplicate_content(site_id, post_id)
    
    if result.get('success'):
        print(f"✅ Content duplicated successfully!")
        print(f"   New ID: {result['post_id']}")
        print(f"   Edit URL: {result['edit_link']}")
        print(f"   Status: Draft")
    else:
        print(f"❌ Duplication failed: {result.get('error', 'Unknown error')}")


def view_all_seo(manager):
    """View all SEO titles and descriptions"""
    site = select_site(manager)
    if not site:
        return
    
    print("\nFetching SEO data...")
    seo_data = manager.get_all_seo_data(site['id'])
    
    if not seo_data:
        print("No SEO data found.")
        return
    
    print(f"\nSEO Data for {len(seo_data)} pages:")
    print("-" * 120)
    
    for item in seo_data:
        print(f"\nPage: {item['title']}")
        print(f"URL: {item['url']}")
        print(f"SEO Title: {item['seo_title'] or '(not set - using default)'}")
        if item.get('generated_title') and not item['seo_title']:
            print(f"  Generated: {item['generated_title']}")
        print(f"SEO Description: {item['seo_description'] or '(not set - using default)'}")
        if item.get('generated_description') and not item['seo_description']:
            print(f"  Generated: {item['generated_description']}")
        print("-" * 120)


def manage_plugins(manager):
    """List and update plugins"""
    site = select_site(manager)
    if not site:
        return
    
    print("\nFetching plugins...")
    plugins = manager.get_plugins(site['id'])
    
    if not plugins:
        print("No plugins found.")
        return
    
    print(f"\nPlugins ({len(plugins)} total):")
    print("-" * 80)
    print(f"{'Active':<8} {'Plugin Name':<40} {'Version':<15}")
    print("-" * 80)
    
    for plugin in plugins:
        status = '✓' if plugin['active'] else ' '
        name = plugin['name'][:37] + '...' if len(plugin['name']) > 40 else plugin['name']
        print(f"{status:<8} {name:<40} {plugin['version']:<15}")


def select_site(manager) -> Dict:
    """Helper to select a site"""
    sites = manager.get_sites('active')
    if not sites:
        print("No active sites available.")
        return None
    
    if len(sites) == 1:
        return sites[0]
    
    print("\nSelect site:")
    for i, site in enumerate(sites, 1):
        print(f"{i}. {site['name']} ({site['domain']})")
    
    try:
        choice = int(input("Site number: ")) - 1
        if 0 <= choice < len(sites):
            return sites[choice]
    except ValueError:
        pass
    
    print("Invalid selection.")
    return None


def search_content(manager):
    """Search for content"""
    site = select_site(manager)
    if not site:
        return
    
    search_term = input("Enter search term: ")
    if not search_term:
        return
    
    print(f"\nSearching for '{search_term}'...")
    content = manager.list_all_content(site['id'], 'any', 100, search_term)
    
    if not content:
        print("No results found.")
        return
    
    print(f"\nFound {len(content)} results:")
    print("-" * 100)
    print(f"{'ID':<8} {'Type':<8} {'Title':<50} {'URL':<40}")
    print("-" * 100)
    
    for item in content:
        title = item['title'][:47] + '...' if len(item['title']) > 50 else item['title']
        url = item['permalink'].replace('https://', '').replace('http://', '')
        url = url[:37] + '...' if len(url) > 40 else url
        print(f"{item['id']:<8} {item['type']:<8} {title:<50} {url:<40}")


def list_seo_generator_pages(manager):
    """List all SEO Generator pages"""
    site = select_site(manager)
    if not site:
        return
    
    print("\nFetching SEO Generator pages...")
    pages = manager.get_seo_generator_pages(site['id'])
    
    if not pages:
        print("No SEO Generator pages found.")
        return
    
    print(f"\nSEO Generator Pages ({len(pages)} total):")
    print("-" * 120)
    print(f"{'ID':<8} {'Title':<40} {'Terms':<8} {'Locations':<10} {'Variations':<12} {'Status':<10}")
    print("-" * 120)
    
    for page in pages:
        title = page['title'][:37] + '...' if len(page['title']) > 40 else page['title']
        print(f"{page['id']:<8} {title:<40} {page['search_terms_count']:<8} {page['locations_count']:<10} {page['total_variations']:<12} {page['status']:<10}")
    
    return pages


def manage_seo_generator_page(manager):
    """Manage a specific SEO Generator page"""
    site = select_site(manager)
    if not site:
        return
    
    # First list pages
    pages = list_seo_generator_pages(manager)
    if not pages:
        return
    
    try:
        page_id = int(input("\nEnter page ID to manage: "))
    except ValueError:
        print("Invalid ID.")
        return
    
    # Get page details
    print("\nFetching page details...")
    details = manager.get_seo_generator_page(site['id'], page_id)
    
    if not details:
        print("Page not found or not a SEO Generator page.")
        return
    
    print("\n" + "="*80)
    print(f"Title: {details['title']}")
    print(f"URL Structure: {details['url_structure']}")
    print(f"Search Terms ({len(details['search_terms'])}): {', '.join(details['search_terms'][:5])}")
    if len(details['search_terms']) > 5:
        print(f"  ... and {len(details['search_terms']) - 5} more")
    print(f"Locations ({len(details['locations'])}): {', '.join(details['locations'][:5])}")
    if len(details['locations']) > 5:
        print(f"  ... and {len(details['locations']) - 5} more")
    print(f"Total Variations: {len(details['search_terms']) * len(details['locations'])}")
    print("\nDynamic Field Usage:")
    for field, count in details['dynamic_fields'].items():
        print(f"  {field}: {count} occurrences")
    print("="*80)
    
    print("\nOptions:")
    print("1. View/Edit Search Terms")
    print("2. View/Edit Locations")
    print("3. Update URL Structure")
    print("4. View Full Content")
    print("5. Add Dynamic Fields to Content")
    print("6. Back")
    
    choice = input("\nSelect option: ")
    
    if choice == '1':
        print(f"\nCurrent Search Terms ({len(details['search_terms'])}):")
        for i, term in enumerate(details['search_terms'], 1):
            print(f"{i}. {term}")
        
        print("\nOptions:")
        print("1. Replace all terms")
        print("2. Add terms")
        print("3. Remove terms")
        print("4. Cancel")
        
        sub_choice = input("\nSelect option: ")
        
        if sub_choice == '1':
            print(f"\nEnter new search terms (max {details['limits']['max_search_terms']}), one per line.")
            print("Type 'END' when done:")
            new_terms = []
            while len(new_terms) < details['limits']['max_search_terms']:
                term = input()
                if term == 'END':
                    break
                if term:
                    new_terms.append(term)
            
            if new_terms:
                if manager.update_seo_generator_page(site['id'], page_id, {'search_terms': new_terms}):
                    print(f"✅ Updated {len(new_terms)} search terms!")
                else:
                    print("❌ Update failed")
        
        elif sub_choice == '2':
            remaining = details['limits']['max_search_terms'] - len(details['search_terms'])
            print(f"\nYou can add up to {remaining} more terms.")
            print("Enter additional terms, one per line. Type 'END' when done:")
            
            current_terms = details['search_terms'][:]
            while len(current_terms) < details['limits']['max_search_terms']:
                term = input()
                if term == 'END':
                    break
                if term and term not in current_terms:
                    current_terms.append(term)
            
            if len(current_terms) > len(details['search_terms']):
                if manager.update_seo_generator_page(site['id'], page_id, {'search_terms': current_terms}):
                    print(f"✅ Added {len(current_terms) - len(details['search_terms'])} new terms!")
                else:
                    print("❌ Update failed")
    
    elif choice == '2':
        print(f"\nCurrent Locations ({len(details['locations'])}):")
        for i, loc in enumerate(details['locations'][:20], 1):
            print(f"{i}. {loc}")
        if len(details['locations']) > 20:
            print(f"... and {len(details['locations']) - 20} more")
        
        print("\nOptions:")
        print("1. Replace all locations")
        print("2. Add locations")
        print("3. Import from file")
        print("4. Cancel")
        
        sub_choice = input("\nSelect option: ")
        
        if sub_choice == '1':
            print(f"\nEnter new locations (max {details['limits']['max_locations']}), one per line.")
            print("Type 'END' when done:")
            new_locations = []
            while len(new_locations) < details['limits']['max_locations']:
                loc = input()
                if loc == 'END':
                    break
                if loc:
                    new_locations.append(loc)
            
            if new_locations:
                if manager.update_seo_generator_page(site['id'], page_id, {'locations': new_locations}):
                    print(f"✅ Updated {len(new_locations)} locations!")
                else:
                    print("❌ Update failed")
    
    elif choice == '3':
        current_structure = details['url_structure']
        print(f"\nCurrent URL structure: {current_structure}")
        print("Use [search_term] and [location] as placeholders")
        new_structure = input("New URL structure (or press Enter to keep current): ")
        
        if new_structure and new_structure != current_structure:
            if manager.update_seo_generator_page(site['id'], page_id, {'url_structure': new_structure}):
                print("✅ URL structure updated!")
            else:
                print("❌ Update failed")
    
    elif choice == '4':
        print("\nFull Content:")
        print("-" * 80)
        print(details['content'][:2000])
        if len(details['content']) > 2000:
            print("\n... (content truncated)")
        print("-" * 80)
    
    elif choice == '5':
        print("\nThis would open the content editor to add dynamic fields.")
        print("Dynamic fields available:")
        print("  [search_term] - Singular form of the search term")
        print("  [search_terms] - Plural form of the search term")
        print("  [location] - The location name")
        print("\nTo edit content with dynamic fields, use option 2 from the main content menu.")


def main():
    manager = EnhancedWPBulkManager()
    
    while True:
        show_enhanced_menu()
        choice = input("\nSelect option: ")
        
        if choice == '1':
            list_all_content(manager)
        elif choice == '2':
            view_edit_content(manager)
        elif choice == '3':
            duplicate_content(manager)
        elif choice == '4':
            site = select_site(manager)
            if site:
                content = list_all_content(manager, site['id'])
                if content:
                    try:
                        post_id = int(input("\nEnter content ID to delete: "))
                        if input("Move to trash (t) or permanently delete (d)? [t]: ").lower() == 'd':
                            if input("Are you SURE you want to permanently delete? (yes/no): ").lower() == 'yes':
                                if manager.delete_content(site['id'], post_id, force=True):
                                    print("✅ Content permanently deleted!")
                                else:
                                    print("❌ Delete failed")
                        else:
                            if manager.delete_content(site['id'], post_id, force=False):
                                print("✅ Content moved to trash!")
                            else:
                                print("❌ Delete failed")
                    except ValueError:
                        print("Invalid ID.")
        elif choice == '5':
            from wpbm_cli import create_single_content
            create_single_content(manager)
        elif choice == '6':
            from wpbm_cli import bulk_create_with_variables
            bulk_create_with_variables(manager)
        elif choice == '7':
            view_all_seo(manager)
        elif choice == '8':
            site = select_site(manager)
            if site:
                try:
                    post_id = int(input("Enter page/post ID to update SEO: "))
                    seo_title = input("SEO Title: ")
                    seo_desc = input("SEO Description: ")
                    
                    if manager.update_seo(site['id'], post_id, {'title': seo_title, 'description': seo_desc}):
                        print("✅ SEO updated!")
                    else:
                        print("❌ SEO update failed")
                except ValueError:
                    print("Invalid ID.")
        elif choice == '9':
            list_seo_generator_pages(manager)
        elif choice == '10':
            manage_seo_generator_page(manager)
        elif choice == '11':
            manage_plugins(manager)
        elif choice == '12':
            site = select_site(manager)
            if site:
                print("\nFetching themes...")
                themes = manager.get_themes(site['id'])
                if themes:
                    print(f"\nThemes ({len(themes)} total):")
                    print("-" * 60)
                    for theme in themes:
                        status = '✓ ACTIVE' if theme['active'] else ''
                        print(f"{theme['name']} (v{theme['version']}) {status}")
        elif choice == '13':
            print("Plugin/Theme updates not yet implemented in CLI")
        elif choice == '14':
            from wpbm_cli import list_sites
            list_sites(manager)
        elif choice == '15':
            search_content(manager)
        elif choice == '16':
            print("\nGoodbye!")
            break
        else:
            print("Invalid option.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    main()