"""
WP Bulk Manager - WordPress content management automation toolkit
"""

__version__ = "2.0.0"
__author__ = "Derek Zar"

from .api.client import WPBMClient
from .api.auth import APIKeyManager
from .utils.cache import CacheManager
from .utils.logger import get_logger
from .operations.content import ContentOperations
from .operations.media import MediaOperations
from .operations.plugins import PluginOperations

__all__ = [
    'WPBMClient', 
    'APIKeyManager', 
    'CacheManager', 
    'get_logger',
    'ContentOperations',
    'MediaOperations',
    'PluginOperations'
]