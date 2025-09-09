"""
Content operations for WP Bulk Manager
"""
from typing import Dict, List, Optional, Callable
import re
import time
from datetime import datetime

from ..api.client import WPBMClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ContentOperations:
    """High-level content operations"""
    
    def __init__(self, client: WPBMClient):
        self.client = client
        
    def search_replace_content(self, search: str, replace: str, 
                              post_types: List[str] = None,
                              dry_run: bool = True,
                              progress_callback: Optional[Callable] = None) -> Dict:
        """
        Search and replace across content
        
        Args:
            search: Text to search for
            replace: Replacement text
            post_types: Post types to search (default: post, page)
            dry_run: Preview changes without applying
            progress_callback: Callback for progress updates
            
        Returns:
            Dictionary with results
        """
        post_types = post_types or ['post', 'page']
        results = {
            'total_posts': 0,
            'posts_modified': 0,
            'total_replacements': 0,
            'changes': [],
            'errors': []
        }
        
        # Get all content
        for post_type in post_types:
            posts = self.client.get_content(content_type=post_type)
            results['total_posts'] += len(posts)
            
            for i, post in enumerate(posts):
                if progress_callback:
                    progress_callback(i + 1, len(posts), f"Processing {post['title']}")
                    
                try:
                    # Check content for matches
                    content = post.get('content', '')
                    title = post.get('title', '')
                    
                    # Count replacements
                    content_matches = len(re.findall(re.escape(search), content))
                    title_matches = len(re.findall(re.escape(search), title))
                    
                    if content_matches > 0 or title_matches > 0:
                        # Prepare replacement
                        new_content = content.replace(search, replace)
                        new_title = title.replace(search, replace)
                        
                        change = {
                            'id': post['id'],
                            'title': post['title'],
                            'url': post.get('link', ''),
                            'content_replacements': content_matches,
                            'title_replacements': title_matches,
                            'preview': {
                                'before': content[:200] + '...' if len(content) > 200 else content,
                                'after': new_content[:200] + '...' if len(new_content) > 200 else new_content
                            }
                        }
                        
                        results['changes'].append(change)
                        results['total_replacements'] += content_matches + title_matches
                        
                        # Apply changes if not dry run
                        if not dry_run:
                            update_data = {}
                            if content_matches > 0:
                                update_data['content'] = new_content
                            if title_matches > 0:
                                update_data['title'] = new_title
                                
                            self.client.update_content(post['id'], update_data)
                            results['posts_modified'] += 1
                            
                except Exception as e:
                    logger.error(f"Error processing post {post['id']}: {e}")
                    results['errors'].append({
                        'post_id': post['id'],
                        'error': str(e)
                    })
                    
        return results
        
    def backup_before_bulk_operation(self, post_ids: List[int] = None) -> Dict:
        """
        Create backup before bulk operations
        
        Args:
            post_ids: Specific post IDs to backup (None for all)
            
        Returns:
            Backup information
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_data = {
            'timestamp': timestamp,
            'posts': []
        }
        
        if post_ids:
            # Backup specific posts
            for post_id in post_ids:
                try:
                    post = self.client.get_content_by_id(post_id)
                    backup_data['posts'].append(post)
                except Exception as e:
                    logger.error(f"Error backing up post {post_id}: {e}")
        else:
            # Backup all content
            for post_type in ['post', 'page']:
                posts = self.client.get_content(content_type=post_type)
                backup_data['posts'].extend(posts)
                
        # Save backup locally
        import json
        backup_file = f"backup_{timestamp}.json"
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
            
        logger.info(f"Created backup with {len(backup_data['posts'])} posts: {backup_file}")
        
        return {
            'backup_file': backup_file,
            'post_count': len(backup_data['posts']),
            'timestamp': timestamp
        }
        
    def get_revision_history(self, post_id: int) -> List[Dict]:
        """Get revision history for a post"""
        try:
            return self.client.get_revisions(post_id)
        except Exception as e:
            logger.error(f"Error getting revisions for post {post_id}: {e}")
            return []
            
    def restore_from_revision(self, post_id: int, revision_id: int) -> bool:
        """Restore post from a specific revision"""
        try:
            result = self.client.restore_revision(post_id, revision_id)
            return result.get('success', False)
        except Exception as e:
            logger.error(f"Error restoring revision {revision_id} for post {post_id}: {e}")
            return False