"""
Caching utilities for WP Bulk Manager
"""
import os
import json
import time
import hashlib
from typing import Any, Optional, Dict
import logging
import tempfile
import shutil

from .logger import get_logger

logger = get_logger(__name__)


class CacheManager:
    """Simple file-based cache with TTL support"""
    
    def __init__(self, cache_dir: str = None, ttl: int = 300):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory for cache files (default: system temp)
            ttl: Time to live in seconds (default: 5 minutes)
        """
        if cache_dir is None:
            cache_dir = os.path.join(tempfile.gettempdir(), 'wpbm_cache')
            
        self.cache_dir = os.path.expanduser(cache_dir)
        self.ttl = ttl
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = {
            'args': args,
            'kwargs': kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
        
    def _get_cache_path(self, key: str) -> str:
        """Get full path for cache file"""
        return os.path.join(self.cache_dir, f"{key}.json")
        
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
            
        try:
            # Check if expired
            mtime = os.path.getmtime(cache_path)
            if time.time() - mtime > self.ttl:
                logger.debug(f"Cache expired for key: {key}")
                os.remove(cache_path)
                return None
                
            # Load cached data
            with open(cache_path, 'r') as f:
                data = json.load(f)
                logger.debug(f"Cache hit for key: {key}")
                return data
                
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Error reading cache for key {key}: {e}")
            # Remove corrupted cache file
            try:
                os.remove(cache_path)
            except OSError:
                pass
            return None
            
    def set(self, key: str, value: Any):
        """Set value in cache"""
        cache_path = self._get_cache_path(key)
        
        try:
            # Write to temp file first for atomicity
            temp_fd, temp_path = tempfile.mkstemp(dir=self.cache_dir)
            with os.fdopen(temp_fd, 'w') as f:
                json.dump(value, f)
                
            # Move temp file to final location
            shutil.move(temp_path, cache_path)
            logger.debug(f"Cached value for key: {key}")
            
        except (OSError, json.JSONDecodeError) as e:
            logger.warning(f"Error caching value for key {key}: {e}")
            
    def delete(self, key: str):
        """Delete specific cache entry"""
        cache_path = self._get_cache_path(key)
        
        try:
            os.remove(cache_path)
            logger.debug(f"Deleted cache for key: {key}")
        except OSError:
            pass
            
    def clear(self):
        """Clear all cache entries"""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
            logger.info("Cleared all cache")
        except OSError as e:
            logger.warning(f"Error clearing cache: {e}")
            
    def cleanup_expired(self):
        """Remove expired cache entries"""
        current_time = time.time()
        cleaned = 0
        
        try:
            for filename in os.listdir(self.cache_dir):
                if not filename.endswith('.json'):
                    continue
                    
                filepath = os.path.join(self.cache_dir, filename)
                mtime = os.path.getmtime(filepath)
                
                if current_time - mtime > self.ttl:
                    os.remove(filepath)
                    cleaned += 1
                    
            if cleaned > 0:
                logger.info(f"Cleaned up {cleaned} expired cache entries")
                
        except OSError as e:
            logger.warning(f"Error cleaning up cache: {e}")
            
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
            total_size = sum(
                os.path.getsize(os.path.join(self.cache_dir, f)) 
                for f in files
            )
            
            return {
                'entries': len(files),
                'size_bytes': total_size,
                'size_mb': round(total_size / 1024 / 1024, 2),
                'cache_dir': self.cache_dir,
                'ttl_seconds': self.ttl
            }
        except OSError:
            return {
                'entries': 0,
                'size_bytes': 0,
                'size_mb': 0,
                'cache_dir': self.cache_dir,
                'ttl_seconds': self.ttl
            }