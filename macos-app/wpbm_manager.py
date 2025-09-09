#!/usr/bin/env python3
"""
WP Bulk Manager - macOS Management Application
Manage multiple WordPress sites with bulk content and SEO updates
"""

import os
import json
import sqlite3
import requests
import keyring
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import hashlib
import hmac
from urllib.parse import urlparse


class WPBulkManager:
    def __init__(self, db_path: str = None):
        """Initialize the WP Bulk Manager"""
        if db_path is None:
            db_path = os.path.expanduser("~/Library/Application Support/WPBulkManager/sites.db")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sites table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                api_key_id TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                last_sync DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # Templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                variables TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Operations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_id INTEGER,
                type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                data TEXT,
                error TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                FOREIGN KEY (site_id) REFERENCES sites(id)
            )
        ''')
        
        # Variables table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS variables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                value_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Add default variables
        self._init_default_variables()
    
    def _init_default_variables(self):
        """Initialize default variables"""
        default_vars = [
            {
                'name': 'location',
                'type': 'location',
                'values': json.dumps([
                    'Brisbane', 'Sydney', 'Melbourne', 'Perth', 'Adelaide',
                    'Gold Coast', 'Newcastle', 'Canberra', 'Sunshine Coast'
                ])
            },
            {
                'name': 'service',
                'type': 'service',
                'values': json.dumps({
                    'painting': {'singular': 'painting service', 'plural': 'painting services'},
                    'plumbing': {'singular': 'plumbing service', 'plural': 'plumbing services'},
                    'electrical': {'singular': 'electrical service', 'plural': 'electrical services'},
                    'cleaning': {'singular': 'cleaning service', 'plural': 'cleaning services'}
                })
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for var in default_vars:
            cursor.execute('''
                INSERT OR IGNORE INTO variables (name, type, value_data)
                VALUES (?, ?, ?)
            ''', (var['name'], var['type'], var['values']))
        
        conn.commit()
        conn.close()
    
    def add_site(self, name: str, url: str, api_key: str) -> bool:
        """Add a new WordPress site"""
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Generate unique key ID for keychain storage
        key_id = f"wpbm_{hashlib.md5(url.encode()).hexdigest()}"
        
        # Store API key in macOS Keychain
        keyring.set_password("WPBulkManager", key_id, api_key)
        
        # Test connection
        if not self.test_connection(url, api_key):
            keyring.delete_password("WPBulkManager", key_id)
            return False
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO sites (name, url, api_key_id, last_sync)
                VALUES (?, ?, ?, ?)
            ''', (name, url, key_id, datetime.now()))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def test_connection(self, url: str, api_key: str) -> bool:
        """Test connection to WordPress site"""
        try:
            response = requests.post(
                f"{url}/wp-json/wpbm/v1/auth",
                headers={'X-API-Key': api_key},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def get_sites(self, status: str = 'active') -> List[Dict]:
        """Get all sites"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status == 'all':
            cursor.execute('SELECT * FROM sites ORDER BY name')
        else:
            cursor.execute('SELECT * FROM sites WHERE status = ? ORDER BY name', (status,))
        
        sites = []
        for row in cursor.fetchall():
            site = dict(row)
            # Parse URL to get domain
            parsed = urlparse(site['url'])
            site['domain'] = parsed.netloc
            sites.append(site)
        
        conn.close()
        return sites
    
    def get_site_api_key(self, site_id: int) -> Optional[str]:
        """Get API key for a site from keychain"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT api_key_id FROM sites WHERE id = ?', (site_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return keyring.get_password("WPBulkManager", result[0])
        return None
    
    def create_content(self, site_ids: List[int], content_data: Dict) -> List[Dict]:
        """Create content on multiple sites"""
        results = []
        
        for site_id in site_ids:
            site = self.get_site(site_id)
            if not site:
                results.append({
                    'site_id': site_id,
                    'success': False,
                    'error': 'Site not found'
                })
                continue
            
            api_key = self.get_site_api_key(site_id)
            if not api_key:
                results.append({
                    'site_id': site_id,
                    'success': False,
                    'error': 'API key not found'
                })
                continue
            
            try:
                response = requests.post(
                    f"{site['url']}/wp-json/wpbm/v1/content",
                    headers={'X-API-Key': api_key},
                    json=content_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        'site_id': site_id,
                        'site_name': site['name'],
                        'success': True,
                        'post_id': data.get('post_id'),
                        'permalink': data.get('permalink')
                    })
                else:
                    results.append({
                        'site_id': site_id,
                        'site_name': site['name'],
                        'success': False,
                        'error': f'HTTP {response.status_code}'
                    })
            except Exception as e:
                results.append({
                    'site_id': site_id,
                    'site_name': site['name'],
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def update_seo(self, site_id: int, post_id: int, seo_data: Dict) -> bool:
        """Update SEO data for a post"""
        site = self.get_site(site_id)
        if not site:
            return False
        
        api_key = self.get_site_api_key(site_id)
        if not api_key:
            return False
        
        try:
            response = requests.put(
                f"{site['url']}/wp-json/wpbm/v1/seo/{post_id}",
                headers={'X-API-Key': api_key},
                json=seo_data,
                timeout=30
            )
            return response.status_code == 200
        except:
            return False
    
    def bulk_create_with_variables(self, site_ids: List[int], template: str, 
                                 variable_values: Dict[str, List[str]]) -> List[Dict]:
        """Create content with variable replacement across multiple sites"""
        results = []
        
        # Generate content variations
        content_processor = ContentProcessor()
        
        for site_id in site_ids:
            # Generate unique content for each site
            for location in variable_values.get('location', ['']):
                for service_key, service_data in variable_values.get('service', {}).items():
                    replacements = {
                        'location': location,
                        'service': service_data['singular'],
                        'service_plural': service_data['plural']
                    }
                    
                    # Process template with variables
                    processed_content = content_processor.process(template, replacements)
                    
                    # Extract title from content (assuming first H1)
                    import re
                    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', processed_content, re.IGNORECASE)
                    title = title_match.group(1) if title_match else f"{service_data['singular']} in {location}"
                    
                    # Create content
                    content_data = {
                        'title': re.sub(r'<[^>]+>', '', title),  # Strip HTML from title
                        'content': processed_content,
                        'type': 'page',
                        'status': 'draft',
                        'seo': {
                            'title': f"{service_data['singular'].title()} in {location} - Professional Services",
                            'description': f"Looking for {service_data['singular']} in {location}? We provide professional {service_data['plural']} with experienced technicians."
                        }
                    }
                    
                    result = self.create_content([site_id], content_data)
                    results.extend(result)
        
        return results
    
    def get_site(self, site_id: int) -> Optional[Dict]:
        """Get site by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM sites WHERE id = ?', (site_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def save_template(self, name: str, type: str, content: str, variables: List[str]) -> bool:
        """Save a content template"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO templates (name, type, content, variables)
            VALUES (?, ?, ?, ?)
        ''', (name, type, content, json.dumps(variables)))
        
        conn.commit()
        conn.close()
        return True
    
    def get_templates(self) -> List[Dict]:
        """Get all templates"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM templates ORDER BY name')
        templates = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return templates


class ContentProcessor:
    """Process content with variables and spintax"""
    
    def process(self, content: str, replacements: Dict[str, str]) -> str:
        """Process content with variable replacements"""
        # Replace variables
        for key, value in replacements.items():
            content = content.replace(f'{{{key}}}', value)
            content = content.replace(f'{{{key}|upper}}', value.upper())
            content = content.replace(f'{{{key}|lower}}', value.lower())
            content = content.replace(f'{{{key}|capitalize}}', value.title())
        
        # Process spintax
        import random
        import re
        
        def replace_spintax(match):
            options = match.group(1).split('|')
            return random.choice(options).strip()
        
        # Process nested spintax
        while '{' in content and '}' in content:
            new_content = re.sub(r'\{([^{}]+)\}', replace_spintax, content)
            if new_content == content:
                break
            content = new_content
        
        return content


def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='WP Bulk Manager - Manage multiple WordPress sites')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add site command
    add_parser = subparsers.add_parser('add-site', help='Add a new WordPress site')
    add_parser.add_argument('name', help='Site name')
    add_parser.add_argument('url', help='Site URL')
    add_parser.add_argument('api_key', help='API key from WP Bulk Manager Client plugin')
    
    # List sites command
    list_parser = subparsers.add_parser('list-sites', help='List all sites')
    list_parser.add_argument('--status', default='active', choices=['active', 'inactive', 'all'])
    
    # Create content command
    create_parser = subparsers.add_parser('create-content', help='Create content on sites')
    create_parser.add_argument('--sites', nargs='+', type=int, help='Site IDs')
    create_parser.add_argument('--title', required=True, help='Content title')
    create_parser.add_argument('--content', required=True, help='Content body')
    create_parser.add_argument('--type', default='page', choices=['post', 'page'])
    create_parser.add_argument('--status', default='draft', choices=['draft', 'publish', 'private'])
    
    args = parser.parse_args()
    
    manager = WPBulkManager()
    
    if args.command == 'add-site':
        success = manager.add_site(args.name, args.url, args.api_key)
        if success:
            print(f"✅ Successfully added site: {args.name}")
        else:
            print(f"❌ Failed to add site. Check URL and API key.")
    
    elif args.command == 'list-sites':
        sites = manager.get_sites(args.status)
        if sites:
            print("\nConnected WordPress Sites:")
            print("-" * 60)
            for site in sites:
                print(f"[{site['id']}] {site['name']:<20} {site['domain']:<30} {site['status']}")
        else:
            print("No sites found.")
    
    elif args.command == 'create-content':
        if not args.sites:
            print("Please specify site IDs with --sites")
            return
        
        content_data = {
            'title': args.title,
            'content': args.content,
            'type': args.type,
            'status': args.status
        }
        
        results = manager.create_content(args.sites, content_data)
        
        print("\nContent Creation Results:")
        print("-" * 60)
        for result in results:
            if result['success']:
                print(f"✅ {result['site_name']}: Created post ID {result['post_id']}")
                print(f"   URL: {result['permalink']}")
            else:
                print(f"❌ {result['site_name']}: {result['error']}")


if __name__ == '__main__':
    main()