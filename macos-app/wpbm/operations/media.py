"""
Media operations for WP Bulk Manager
"""
from typing import Dict, List, Optional, Callable
import os
import requests
from urllib.parse import urlparse

from ..api.client import WPBMClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MediaOperations:
    """Handle media/attachment operations"""
    
    def __init__(self, client: WPBMClient):
        self.client = client
        
    def list_media(self, media_type: Optional[str] = None, 
                   limit: int = 100) -> List[Dict]:
        """
        List media items
        
        Args:
            media_type: Filter by mime type (e.g., 'image', 'video')
            limit: Number of items to retrieve
            
        Returns:
            List of media items
        """
        params = {'limit': limit}
        
        if media_type:
            # Convert simple type to mime type pattern
            mime_patterns = {
                'image': 'image/',
                'video': 'video/',
                'audio': 'audio/',
                'pdf': 'application/pdf',
                'document': 'application/'
            }
            
            if media_type in mime_patterns:
                params['mime_type'] = mime_patterns[media_type]
            else:
                params['mime_type'] = media_type
                
        return self.client.get_media(**params)
        
    def bulk_download_media(self, media_ids: List[int] = None,
                           output_dir: str = './media_downloads',
                           progress_callback: Optional[Callable] = None) -> Dict:
        """
        Bulk download media files
        
        Args:
            media_ids: Specific media IDs to download (None for all)
            output_dir: Directory to save files
            progress_callback: Progress callback function
            
        Returns:
            Download results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        results = {
            'total': 0,
            'downloaded': 0,
            'failed': 0,
            'errors': []
        }
        
        # Get media items
        if media_ids:
            media_items = []
            for media_id in media_ids:
                try:
                    item = self.client.get(f'/media/{media_id}')
                    media_items.append(item)
                except Exception as e:
                    logger.error(f"Error fetching media {media_id}: {e}")
                    results['errors'].append({
                        'media_id': media_id,
                        'error': str(e)
                    })
        else:
            media_items = self.list_media()
            
        results['total'] = len(media_items)
        
        # Download each item
        for i, item in enumerate(media_items):
            if progress_callback:
                progress_callback(i + 1, len(media_items), 
                                f"Downloading {item.get('title', 'Untitled')}")
                
            try:
                # Get the media URL
                media_url = item.get('source_url') or item.get('guid', {}).get('rendered')
                
                if not media_url:
                    raise ValueError("No media URL found")
                    
                # Download file
                response = requests.get(media_url, stream=True)
                response.raise_for_status()
                
                # Determine filename
                filename = os.path.basename(urlparse(media_url).path)
                if not filename:
                    filename = f"media_{item['id']}"
                    
                filepath = os.path.join(output_dir, filename)
                
                # Write file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
                results['downloaded'] += 1
                logger.info(f"Downloaded: {filepath}")
                
            except Exception as e:
                logger.error(f"Error downloading media {item['id']}: {e}")
                results['failed'] += 1
                results['errors'].append({
                    'media_id': item['id'],
                    'title': item.get('title', 'Unknown'),
                    'error': str(e)
                })
                
        return results
        
    def bulk_update_media_metadata(self, updates: List[Dict]) -> Dict:
        """
        Bulk update media metadata
        
        Args:
            updates: List of dicts with 'id' and metadata fields
            
        Returns:
            Update results
        """
        results = {
            'total': len(updates),
            'updated': 0,
            'failed': 0,
            'errors': []
        }
        
        for update in updates:
            media_id = update.get('id')
            if not media_id:
                continue
                
            try:
                # Remove 'id' from update data
                update_data = {k: v for k, v in update.items() if k != 'id'}
                
                # Update media
                self.client.put(f'/media/{media_id}', update_data)
                results['updated'] += 1
                
            except Exception as e:
                logger.error(f"Error updating media {media_id}: {e}")
                results['failed'] += 1
                results['errors'].append({
                    'media_id': media_id,
                    'error': str(e)
                })
                
        return results
        
    def find_unused_media(self) -> List[Dict]:
        """
        Find media items that are not used in any posts/pages
        
        Returns:
            List of unused media items
        """
        # Get all media
        all_media = self.list_media(limit=1000)
        
        # Get all content
        all_content = []
        for post_type in ['post', 'page']:
            all_content.extend(self.client.get_content(content_type=post_type))
            
        # Build set of used media IDs
        used_media_ids = set()
        
        for post in all_content:
            content = post.get('content', '')
            
            # Look for wp:image blocks
            import re
            image_blocks = re.findall(r'wp:image[^}]+?"id":(\d+)', content)
            used_media_ids.update(int(id) for id in image_blocks)
            
            # Look for attachment URLs
            for media in all_media:
                if media.get('source_url') and media['source_url'] in content:
                    used_media_ids.add(media['id'])
                    
            # Check featured image
            if post.get('featured_media'):
                used_media_ids.add(post['featured_media'])
                
        # Find unused media
        unused = []
        for media in all_media:
            if media['id'] not in used_media_ids:
                unused.append({
                    'id': media['id'],
                    'title': media.get('title', {}).get('rendered', 'Untitled'),
                    'url': media.get('source_url'),
                    'mime_type': media.get('mime_type'),
                    'file_size': media.get('media_details', {}).get('filesize', 0)
                })
                
        logger.info(f"Found {len(unused)} unused media items out of {len(all_media)} total")
        return unused