"""
Site Manager - Handles folder structure and site setup
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from ..database.mysql_manager import MySQLManager
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SiteManager:
    """Manages site folders, templates, and branded agent kits"""
    
    def __init__(self, base_path: Optional[str] = None):
        """Initialize site manager"""
        self.base_path = Path(base_path or os.path.expanduser("~/Documents/WPBulkManager/sites"))
        self.db = MySQLManager()
        self._ensure_base_directory()
    
    def _ensure_base_directory(self):
        """Ensure base directory exists"""
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Site base directory: {self.base_path}")
    
    def setup_new_site(self, name: str, url: str, api_key: str,
                      brand_voice: Optional[str] = None,
                      ip_whitelist: Optional[str] = None) -> Dict:
        """Set up a new site with folder structure and database entry"""
        
        # Sanitize site name for folder
        folder_name = name.lower().replace(' ', '_').replace('/', '_')
        site_path = self.base_path / folder_name
        
        try:
            # Create folder structure
            folders = {
                'root': site_path,
                'templates': site_path / 'templates',
                'content': site_path / 'content',
                'backups': site_path / 'backups',
                'exports': site_path / 'exports',
                'branding': site_path / 'branding',
                'logs': site_path / 'logs'
            }
            
            for folder in folders.values():
                folder.mkdir(parents=True, exist_ok=True)
            
            # Create site info file
            site_info = {
                'name': name,
                'url': url,
                'created_at': datetime.now().isoformat(),
                'folder_structure': {k: str(v) for k, v in folders.items()}
            }
            
            with open(site_path / 'site_info.json', 'w') as f:
                json.dump(site_info, f, indent=2)
            
            # Create branded agent kit template
            brand_kit = {
                'brand_voice': brand_voice or 'Professional and informative',
                'tone_attributes': ['professional', 'helpful', 'clear'],
                'target_audience': {
                    'primary': 'Business professionals',
                    'age_range': '25-55',
                    'interests': []
                },
                'content_guidelines': {
                    'do': [
                        'Use clear, concise language',
                        'Focus on benefits',
                        'Include calls to action'
                    ],
                    'dont': [
                        'Use jargon without explanation',
                        'Make unsupported claims',
                        'Use offensive language'
                    ]
                },
                'keywords': {
                    'primary': [],
                    'secondary': [],
                    'local': []
                }
            }
            
            with open(site_path / 'branding' / 'brand_kit.json', 'w') as f:
                json.dump(brand_kit, f, indent=2)
            
            # Create README
            readme_content = f"""# {name} - WP Bulk Manager Site

## Site Information
- **URL**: {url}
- **Created**: {datetime.now().strftime('%Y-%m-%d')}
- **Folder**: {site_path}

## Folder Structure
- `/templates` - Content templates for pages, posts, etc.
- `/content` - Exported content and drafts
- `/backups` - Site backups
- `/exports` - Data exports (CSV, JSON)
- `/branding` - Brand guidelines and voice documentation
- `/logs` - Operation logs

## Brand Voice
{brand_voice or 'Not specified - update brand_kit.json'}

## Templates
Place your content templates in the `/templates` folder with descriptive names:
- `newsletter-signup.html` - Newsletter signup page template
- `product-page.html` - Product page template
- `blog-post.md` - Blog post template

## Usage
1. Update `branding/brand_kit.json` with your brand guidelines
2. Add templates to the `/templates` folder
3. Use the WP Bulk Manager to apply templates and manage content
"""
            
            with open(site_path / 'README.md', 'w') as f:
                f.write(readme_content)
            
            # Create sample template
            sample_template = """<!-- Template: Basic Page -->
<!-- Variables: {title}, {content}, {cta_text}, {cta_link} -->

<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">{title}</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{content}</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{cta_link}">{cta_text}</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->
"""
            
            with open(site_path / 'templates' / 'basic-page.html', 'w') as f:
                f.write(sample_template)
            
            # Add to database with folder path
            site_id = self.db.add_site(
                name=name,
                url=url,
                api_key=api_key,
                description=f"Site managed by WP Bulk Manager",
                ip_whitelist=ip_whitelist
            )
            
            if site_id:
                # Update with folder path
                self.db.update_site(site_id, 
                                   folder_path=str(site_path),
                                   brand_voice=brand_voice)
                
                # Add initial branded agent kit entry
                try:
                    conn = self.db.get_connection()
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO branded_agent_kit 
                            (site_id, brand_personality, tone_attributes)
                            VALUES (%s, %s, %s)
                        """, (site_id, brand_voice or 'Professional and informative',
                              json.dumps(['professional', 'helpful', 'clear'])))
                        conn.commit()
                except Exception as e:
                    logger.warning(f"Could not create branded agent kit: {e}")
                
                logger.info(f"✅ Successfully set up site '{name}' with ID {site_id}")
                
                return {
                    'success': True,
                    'site_id': site_id,
                    'folder_path': str(site_path),
                    'message': f"Site '{name}' created successfully!"
                }
            else:
                # Clean up folders if database entry failed
                import shutil
                shutil.rmtree(site_path)
                return {
                    'success': False,
                    'error': 'Failed to create database entry'
                }
                
        except Exception as e:
            logger.error(f"Error setting up site: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_site_folder(self, site_name: str) -> Optional[Path]:
        """Get folder path for a site"""
        site = self.db.get_site(site_name)
        if site and site.get('folder_path'):
            return Path(site['folder_path'])
        
        # Try to find by convention
        folder_name = site_name.lower().replace(' ', '_').replace('/', '_')
        site_path = self.base_path / folder_name
        if site_path.exists():
            return site_path
        
        return None
    
    def list_templates(self, site_name: str) -> Dict[str, list]:
        """List all templates for a site"""
        site_folder = self.get_site_folder(site_name)
        if not site_folder:
            return {'error': 'Site folder not found'}
        
        templates_dir = site_folder / 'templates'
        if not templates_dir.exists():
            return {'templates': []}
        
        templates = []
        for template_file in templates_dir.glob('*'):
            if template_file.is_file():
                templates.append({
                    'name': template_file.stem,
                    'file': template_file.name,
                    'path': str(template_file),
                    'size': template_file.stat().st_size,
                    'modified': datetime.fromtimestamp(
                        template_file.stat().st_mtime
                    ).isoformat()
                })
        
        return {'templates': templates}
    
    def get_brand_kit(self, site_name: str) -> Optional[Dict]:
        """Get brand kit for a site"""
        site_folder = self.get_site_folder(site_name)
        if not site_folder:
            return None
        
        brand_kit_path = site_folder / 'branding' / 'brand_kit.json'
        if brand_kit_path.exists():
            with open(brand_kit_path, 'r') as f:
                return json.load(f)
        
        return None
    
    def update_brand_kit(self, site_name: str, brand_data: Dict) -> bool:
        """Update brand kit for a site"""
        site_folder = self.get_site_folder(site_name)
        if not site_folder:
            return False
        
        brand_kit_path = site_folder / 'branding' / 'brand_kit.json'
        brand_kit_path.parent.mkdir(exist_ok=True)
        
        # Merge with existing data
        existing_data = {}
        if brand_kit_path.exists():
            with open(brand_kit_path, 'r') as f:
                existing_data = json.load(f)
        
        existing_data.update(brand_data)
        existing_data['updated_at'] = datetime.now().isoformat()
        
        with open(brand_kit_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        # Update database
        site = self.db.get_site(site_name)
        if site:
            try:
                conn = self.db.get_connection()
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE branded_agent_kit 
                        SET brand_personality = %s,
                            tone_attributes = %s,
                            primary_keywords = %s,
                            updated_at = NOW()
                        WHERE site_id = %s
                    """, (
                        brand_data.get('brand_voice'),
                        json.dumps(brand_data.get('tone_attributes', [])),
                        json.dumps(brand_data.get('keywords', {}).get('primary', [])),
                        site['id']
                    ))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error updating brand kit in database: {e}")
        
        return True
    
    def create_backup(self, site_name: str, backup_data: Dict, 
                     backup_type: str = 'content') -> Optional[str]:
        """Create a backup in the site's backup folder"""
        site_folder = self.get_site_folder(site_name)
        if not site_folder:
            return None
        
        backup_dir = site_folder / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f"{backup_type}_{timestamp}.json"
        
        with open(backup_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'type': backup_type,
                'data': backup_data
            }, f, indent=2)
        
        return str(backup_file)