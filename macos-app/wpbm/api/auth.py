"""
Authentication management for WP Bulk Manager
"""
import os
import json
import keyring
from typing import Dict, Optional
import logging

from ..utils.logger import get_logger

logger = get_logger(__name__)


class APIKeyManager:
    """Manage API keys securely using system keychain"""
    
    SERVICE_NAME = "WPBulkManager"
    
    def __init__(self, config_file: str = "~/.wpbm/sites.json"):
        self.config_file = os.path.expanduser(config_file)
        self._ensure_config_dir()
        
    def _ensure_config_dir(self):
        """Ensure config directory exists"""
        config_dir = os.path.dirname(self.config_file)
        os.makedirs(config_dir, exist_ok=True)
        
    def _load_sites(self) -> Dict:
        """Load sites configuration"""
        if not os.path.exists(self.config_file):
            return {}
            
        with open(self.config_file, 'r') as f:
            return json.load(f)
            
    def _save_sites(self, sites: Dict):
        """Save sites configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(sites, f, indent=2)
            
    def add_site(self, name: str, url: str, api_key: str):
        """Add a new site with secure API key storage"""
        sites = self._load_sites()
        
        # Store site info (without API key)
        sites[name] = {
            'url': url.rstrip('/'),
            'name': name
        }
        self._save_sites(sites)
        
        # Store API key in keychain
        keyring.set_password(self.SERVICE_NAME, name, api_key)
        logger.info(f"Added site: {name}")
        
    def get_site(self, name: str) -> Optional[Dict]:
        """Get site info with API key"""
        sites = self._load_sites()
        
        if name not in sites:
            return None
            
        site = sites[name].copy()
        
        # Retrieve API key from keychain
        api_key = keyring.get_password(self.SERVICE_NAME, name)
        if api_key:
            site['api_key'] = api_key
            
        return site
        
    def remove_site(self, name: str):
        """Remove site and API key"""
        sites = self._load_sites()
        
        if name in sites:
            del sites[name]
            self._save_sites(sites)
            
        # Remove from keychain
        try:
            keyring.delete_password(self.SERVICE_NAME, name)
        except keyring.errors.PasswordDeleteError:
            pass
            
        logger.info(f"Removed site: {name}")
        
    def list_sites(self) -> Dict:
        """List all configured sites"""
        return self._load_sites()