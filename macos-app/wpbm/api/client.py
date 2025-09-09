"""
Base API client for WordPress Bulk Manager
"""
import requests
import json
import time
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urljoin
import logging

from ..utils.cache import CacheManager
from ..utils.logger import get_logger
from .auth import APIKeyManager

logger = get_logger(__name__)


class WPBMClient:
    """Base API client with caching, retries, and error handling"""
    
    def __init__(self, site_url: str, api_key: str, cache_enabled: bool = True, 
                 cache_ttl: int = 300, max_retries: int = 3):
        self.site_url = site_url.rstrip('/')
        self.api_key = api_key
        self.cache_enabled = cache_enabled
        self.cache = CacheManager(ttl=cache_ttl) if cache_enabled else None
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })
        
    def _build_url(self, endpoint: str) -> str:
        """Build full API URL"""
        base = f"{self.site_url}/wp-json/wpbm/v1"
        return urljoin(base + '/', endpoint.lstrip('/'))
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with retries"""
        url = self._build_url(endpoint)
        
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"{method} {url} (attempt {attempt + 1}/{self.max_retries})")
                response = self.session.request(method, url, timeout=30, **kwargs)
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
                    
    def get(self, endpoint: str, params: Optional[Dict] = None, 
            use_cache: bool = True) -> Dict[str, Any]:
        """GET request with optional caching"""
        cache_key = None
        
        if self.cache and use_cache:
            cache_key = self.cache.generate_key(endpoint, params)
            cached = self.cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit for {endpoint}")
                return cached
                
        response = self._make_request('GET', endpoint, params=params)
        data = response.json()
        
        if cache_key and self.cache:
            self.cache.set(cache_key, data)
            
        return data
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST request"""
        response = self._make_request('POST', endpoint, json=data)
        return response.json()
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT request"""
        response = self._make_request('PUT', endpoint, json=data)
        return response.json()
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE request"""
        response = self._make_request('DELETE', endpoint)
        return response.json()
    
    def get_content(self, content_type: str = 'page', limit: int = 100, 
                    status: str = 'any', **kwargs) -> List[Dict]:
        """Get content with pagination support"""
        all_content = []
        page = 1
        
        while True:
            params = {
                'type': content_type,
                'limit': limit,
                'page': page,
                'status': status,
                **kwargs
            }
            
            response = self.get('/content', params=params)
            posts = response.get('posts', [])
            
            if not posts:
                break
                
            all_content.extend(posts)
            
            if len(posts) < limit:
                break
                
            page += 1
            
        return all_content
    
    def get_content_by_id(self, content_id: int) -> Dict[str, Any]:
        """Get single content item"""
        return self.get(f'/content/{content_id}')
    
    def update_content(self, content_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update content"""
        return self.put(f'/content/{content_id}', data)
    
    def create_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new content"""
        return self.post('/content', data)
    
    def delete_content(self, content_id: int) -> Dict[str, Any]:
        """Delete content"""
        return self.delete(f'/content/{content_id}')
    
    def search_replace(self, search: str, replace: str, post_types: List[str] = None,
                      dry_run: bool = True) -> Dict[str, Any]:
        """Search and replace across content"""
        data = {
            'search': search,
            'replace': replace,
            'post_types': post_types or ['post', 'page'],
            'dry_run': dry_run
        }
        return self.post('/search-replace', data)
    
    def get_media(self, limit: int = 100, **kwargs) -> List[Dict]:
        """Get media items"""
        return self.get('/media', params={'limit': limit, **kwargs})
    
    def backup_content(self, post_ids: List[int] = None) -> Dict[str, Any]:
        """Create backup before bulk operations"""
        data = {'post_ids': post_ids} if post_ids else {}
        return self.post('/backup', data)
    
    def get_revisions(self, content_id: int) -> List[Dict]:
        """Get content revisions"""
        return self.get(f'/content/{content_id}/revisions')
    
    def restore_revision(self, content_id: int, revision_id: int) -> Dict[str, Any]:
        """Restore content to specific revision"""
        return self.post(f'/content/{content_id}/revisions/{revision_id}/restore', {})