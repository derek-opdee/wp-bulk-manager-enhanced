#!/usr/bin/env python3
"""
WP Bulk Manager v2 - Refactored with shared utilities
"""
import os
import sys
import sqlite3
from typing import Dict, List, Optional

# Add the wpbm package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm.api.client import WPBMClient
from wpbm.api.auth import APIKeyManager
from wpbm.operations.content import ContentOperations
from wpbm.operations.media import MediaOperations
from wpbm.utils.logger import get_logger
from wpbm.utils.cache import CacheManager

logger = get_logger(__name__)


class WPBulkManagerV2:
    """Enhanced WP Bulk Manager with caching and better organization"""
    
    def __init__(self, db_path: str = 'wpbm_sites.db'):
        self.db_path = db_path
        self.auth_manager = APIKeyManager()
        self._init_db()
        
    def _init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                api_key_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def add_site(self, name: str, url: str, api_key: str) -> bool:
        """Add a new site"""
        try:
            # Store in auth manager (keychain)
            self.auth_manager.add_site(name, url, api_key)
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT OR REPLACE INTO sites (name, url, api_key_id) VALUES (?, ?, ?)',
                (name, url, name)  # Use name as key ID
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added site: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding site: {e}")
            return False
            
    def get_client(self, site_name: str, cache_enabled: bool = True) -> Optional[WPBMClient]:
        """Get API client for a site"""
        site = self.auth_manager.get_site(site_name)
        
        if not site or 'api_key' not in site:
            logger.error(f"Site not found or API key missing: {site_name}")
            return None
            
        return WPBMClient(
            site_url=site['url'],
            api_key=site['api_key'],
            cache_enabled=cache_enabled
        )
        
    def list_sites(self) -> List[Dict]:
        """List all configured sites"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM sites ORDER BY name')
        sites = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return sites
        
    def search_replace_across_site(self, site_name: str, search: str, 
                                  replace: str, dry_run: bool = True) -> Dict:
        """Search and replace across entire site"""
        client = self.get_client(site_name)
        if not client:
            return {'error': 'Site not found'}
            
        operations = ContentOperations(client)
        
        # Progress callback
        def progress(current, total, message):
            print(f"\r[{current}/{total}] {message}", end='', flush=True)
            
        results = operations.search_replace_content(
            search=search,
            replace=replace,
            dry_run=dry_run,
            progress_callback=progress
        )
        
        print()  # New line after progress
        return results
        
    def backup_site_content(self, site_name: str) -> Dict:
        """Create full backup of site content"""
        client = self.get_client(site_name, cache_enabled=False)
        if not client:
            return {'error': 'Site not found'}
            
        operations = ContentOperations(client)
        return operations.backup_before_bulk_operation()
        
    def manage_site_media(self, site_name: str) -> MediaOperations:
        """Get media operations for a site"""
        client = self.get_client(site_name)
        if not client:
            raise ValueError(f"Site not found: {site_name}")
            
        return MediaOperations(client)
        
    def clear_cache(self, site_name: str = None):
        """Clear cache for a site or all sites"""
        if site_name:
            cache = CacheManager()
            cache.clear()
            logger.info(f"Cleared cache for {site_name}")
        else:
            cache = CacheManager()
            cache.clear()
            logger.info("Cleared all cache")
            
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        cache = CacheManager()
        return cache.get_stats()


# Example usage
if __name__ == "__main__":
    manager = WPBulkManagerV2()
    
    # Example: Add a site
    # manager.add_site("example", "https://example.com", "your-api-key")
    
    # Example: Search and replace (dry run)
    # results = manager.search_replace_across_site(
    #     "example",
    #     search="old text",
    #     replace="new text",
    #     dry_run=True
    # )
    # print(f"Would update {len(results['changes'])} posts")
    
    # Example: Media management
    # media_ops = manager.manage_site_media("example")
    # unused = media_ops.find_unused_media()
    # print(f"Found {len(unused)} unused media items")