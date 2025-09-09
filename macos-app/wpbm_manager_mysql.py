#!/usr/bin/env python3
"""
WP Bulk Manager with MySQL Database Support
"""

import os
import sys
from typing import Dict, List, Optional
from pathlib import Path

# Add the wpbm package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm.api.client import WPBMClient
from wpbm.database.mysql_manager import MySQLManager
from wpbm.utils.site_manager import SiteManager
from wpbm.operations.content import ContentOperations
from wpbm.operations.media import MediaOperations
from wpbm.utils.logger import get_logger

logger = get_logger(__name__)


class WPBulkManagerMySQL:
    """Enhanced WP Bulk Manager with MySQL database and site management"""
    
    def __init__(self):
        """Initialize manager with MySQL database"""
        self.db = MySQLManager()
        self.site_manager = SiteManager()
        
    def add_site(self, name: str, url: str, api_key: str,
                 brand_voice: Optional[str] = None,
                 ip_whitelist: Optional[str] = None) -> Dict:
        """Add a new site with folder structure and branding"""
        
        # Check if site already exists
        existing = self.db.get_site(name)
        if existing:
            return {
                'success': False,
                'error': f"Site '{name}' already exists"
            }
        
        # Set up site with folders and database entry
        result = self.site_manager.setup_new_site(
            name=name,
            url=url,
            api_key=api_key,
            brand_voice=brand_voice,
            ip_whitelist=ip_whitelist
        )
        
        if result['success']:
            # Log the site creation
            self.db.log_change(
                site_id=result['site_id'],
                content_type='site',
                content_id=result['site_id'],
                action='create',
                summary=f"Site '{name}' created with folder structure"
            )
        
        return result
    
    def get_client(self, site_name: str, cache_enabled: bool = True) -> Optional[WPBMClient]:
        """Get API client for a site"""
        site = self.db.get_site(site_name)
        if not site:
            logger.error(f"Site not found: {site_name}")
            return None
            
        return WPBMClient(
            site_url=site['url'],
            api_key=site['api_key'],
            cache_enabled=cache_enabled
        )
    
    def list_sites(self, status: Optional[str] = None) -> List[Dict]:
        """List all sites with statistics"""
        sites = self.db.list_sites(status)
        
        # Add folder info
        for site in sites:
            folder = self.site_manager.get_site_folder(site['name'])
            if folder:
                site['folder_path'] = str(folder)
                site['has_templates'] = (folder / 'templates').exists()
                site['has_brand_kit'] = (folder / 'branding' / 'brand_kit.json').exists()
        
        return sites
    
    def get_site_info(self, site_name: str) -> Dict:
        """Get comprehensive site information"""
        site = self.db.get_site(site_name)
        if not site:
            return {'error': 'Site not found'}
        
        # Get statistics
        stats = self.db.get_site_statistics(site['id'])
        
        # Get folder info
        folder = self.site_manager.get_site_folder(site_name)
        
        # Get brand kit
        brand_kit = self.site_manager.get_brand_kit(site_name)
        
        # Get templates
        templates = self.site_manager.list_templates(site_name)
        
        return {
            'site': site,
            'statistics': stats,
            'folder_path': str(folder) if folder else None,
            'brand_kit': brand_kit,
            'templates': templates.get('templates', [])
        }
    
    def update_brand_voice(self, site_name: str, brand_data: Dict) -> bool:
        """Update brand voice and guidelines for a site"""
        # Update in file system
        if not self.site_manager.update_brand_kit(site_name, brand_data):
            return False
        
        # Update in database
        site = self.db.get_site(site_name)
        if site:
            self.db.update_site(
                site['id'],
                brand_voice=brand_data.get('brand_voice'),
                brand_guidelines=brand_data
            )
            
            # Log the change
            self.db.log_change(
                site_id=site['id'],
                content_type='branding',
                content_id=site['id'],
                action='update',
                field_name='brand_kit',
                summary='Updated brand voice and guidelines'
            )
        
        return True
    
    def create_content_from_template(self, site_name: str, template_name: str,
                                   variables: Dict, content_type: str = 'page') -> Dict:
        """Create content using a template"""
        client = self.get_client(site_name)
        if not client:
            return {'error': 'Could not get client'}
        
        site = self.db.get_site(site_name)
        folder = self.site_manager.get_site_folder(site_name)
        
        if not folder:
            return {'error': 'Site folder not found'}
        
        # Load template
        template_path = folder / 'templates' / f"{template_name}.html"
        if not template_path.exists():
            template_path = folder / 'templates' / f"{template_name}.md"
        
        if not template_path.exists():
            return {'error': f'Template not found: {template_name}'}
        
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Replace variables
        content = template_content
        for key, value in variables.items():
            content = content.replace(f'{{{key}}}', str(value))
        
        # Create content
        data = {
            'type': content_type,
            'title': variables.get('title', 'New Page'),
            'content': content,
            'status': 'draft'
        }
        
        try:
            result = client.create_content(data)
            
            # Log to database
            self.db.log_change(
                site_id=site['id'],
                content_type=content_type,
                content_id=result.get('id'),
                action='create',
                summary=f"Created from template: {template_name}"
            )
            
            # Track template usage
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE templates 
                    SET usage_count = usage_count + 1,
                        last_used_at = NOW()
                    WHERE site_id = %s AND template_name = %s
                """, (site['id'], template_name))
                conn.commit()
            
            return {
                'success': True,
                'data': result,
                'message': f"Created {content_type} from template '{template_name}'"
            }
            
        except Exception as e:
            logger.error(f"Error creating content from template: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def track_api_access(self, site_name: str, endpoint: str, method: str,
                        response_code: int, response_time_ms: int,
                        error_message: Optional[str] = None) -> None:
        """Track API access for monitoring"""
        site = self.db.get_site(site_name)
        if site:
            self.db.log_access(
                site_id=site['id'],
                api_key=site['api_key'],
                endpoint=endpoint,
                method=method,
                response_code=response_code,
                response_time_ms=response_time_ms,
                error_message=error_message
            )
    
    def get_recent_activity(self, site_name: Optional[str] = None) -> List[Dict]:
        """Get recent activity for a site or all sites"""
        if site_name:
            site = self.db.get_site(site_name)
            if site:
                return self.db.get_changes(site['id'])
        return self.db.get_recent_activity()
    
    def backup_site_content(self, site_name: str) -> Dict:
        """Create full backup of site content"""
        client = self.get_client(site_name, cache_enabled=False)
        if not client:
            return {'error': 'Site not found'}
        
        site = self.db.get_site(site_name)
        operations = ContentOperations(client)
        
        # Create backup
        backup_result = operations.backup_before_bulk_operation()
        
        # Save to site folder
        backup_path = self.site_manager.create_backup(
            site_name,
            backup_result,
            'full_content'
        )
        
        # Record in database
        if backup_path:
            backup_id = self.db.create_backup_record(
                site_id=site['id'],
                backup_type='full_content',
                backup_location=backup_path,
                backup_size=os.path.getsize(backup_path),
                items_count=backup_result.get('post_count', 0)
            )
            
            self.db.update_backup_status(backup_id, 'completed')
        
        return {
            'success': True,
            'backup_file': backup_path,
            'post_count': backup_result.get('post_count', 0)
        }


# Example usage
if __name__ == "__main__":
    manager = WPBulkManagerMySQL()
    
    # Example: Add a new site
    # result = manager.add_site(
    #     name="example",
    #     url="https://example.com",
    #     api_key="your-api-key",
    #     brand_voice="Professional and friendly tone focusing on innovation"
    # )
    # print(result)
    
    # Example: List all sites
    sites = manager.list_sites()
    print(f"\n📊 Managed Sites ({len(sites)}):")
    for site in sites:
        print(f"  - {site['name']}: {site['url']}")
        if site.get('has_brand_kit'):
            print(f"    ✓ Brand kit configured")
        if site.get('has_templates'):
            print(f"    ✓ Has templates")