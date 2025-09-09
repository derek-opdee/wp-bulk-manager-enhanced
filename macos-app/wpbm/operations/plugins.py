"""
Plugin management operations for WP Bulk Manager
"""
import os
import requests
from typing import Dict, List, Optional, BinaryIO
import zipfile
import tempfile

from ..api.client import WPBMClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


class PluginOperations:
    """Handle WordPress plugin operations"""
    
    def __init__(self, client: WPBMClient):
        self.client = client
        
    def list_plugins(self) -> List[Dict]:
        """
        List all plugins on the site
        
        Returns:
            List of plugin information
        """
        try:
            result = self.client.get('/plugins')
            # API returns {'plugins': [...], 'count': N}, we just want the plugins list
            if isinstance(result, dict) and 'plugins' in result:
                return result['plugins']
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error listing plugins: {e}")
            return []
            
    def upload_plugin(self, plugin_path: str, activate: bool = False) -> Dict:
        """
        Upload and install a plugin from local file
        
        Args:
            plugin_path: Path to plugin ZIP file
            activate: Whether to activate after installation
            
        Returns:
            Installation result
        """
        if not os.path.exists(plugin_path):
            raise FileNotFoundError(f"Plugin file not found: {plugin_path}")
            
        if not plugin_path.endswith('.zip'):
            raise ValueError("Plugin must be a ZIP file")
            
        # Verify it's a valid zip
        try:
            with zipfile.ZipFile(plugin_path, 'r') as zip_file:
                zip_file.testzip()
        except Exception as e:
            raise ValueError(f"Invalid ZIP file: {e}")
            
        logger.info(f"Uploading plugin: {os.path.basename(plugin_path)}")
        
        # Upload the plugin
        with open(plugin_path, 'rb') as f:
            files = {'plugin_file': (os.path.basename(plugin_path), f, 'application/zip')}
            
            # We need to use requests directly for multipart upload
            headers = {'X-API-Key': self.client.api_key}
            url = self.client._build_url('/plugins/upload')
            
            response = requests.post(url, files=files, headers=headers, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            
        if result.get('success') and activate:
            # Activate the plugin
            plugin_file = result.get('plugin_file')
            if plugin_file:
                activate_result = self.activate_plugin(plugin_file)
                result['activated'] = activate_result.get('activated', False)
                
        return result
        
    def install_from_url(self, plugin_url: str, activate: bool = False) -> Dict:
        """
        Install plugin from URL
        
        Args:
            plugin_url: URL to plugin ZIP file
            activate: Whether to activate after installation
            
        Returns:
            Installation result
        """
        logger.info(f"Installing plugin from URL: {plugin_url}")
        
        result = self.client.post('/plugins/install-url', {
            'url': plugin_url
        })
        
        if result.get('success') and activate:
            plugin_file = result.get('plugin_file')
            if plugin_file:
                activate_result = self.activate_plugin(plugin_file)
                result['activated'] = activate_result.get('activated', False)
                
        return result
        
    def activate_plugin(self, plugin_file: str) -> Dict:
        """
        Activate a plugin
        
        Args:
            plugin_file: Plugin file (e.g., 'plugin-name/plugin-name.php')
            
        Returns:
            Activation result
        """
        logger.info(f"Activating plugin: {plugin_file}")
        
        return self.client.post('/plugins/activate', {
            'plugin_file': plugin_file
        })
        
    def deactivate_plugin(self, plugin_file: str) -> Dict:
        """
        Deactivate a plugin
        
        Args:
            plugin_file: Plugin file
            
        Returns:
            Deactivation result
        """
        logger.info(f"Deactivating plugin: {plugin_file}")
        
        return self.client.post('/plugins/deactivate', {
            'plugin_file': plugin_file
        })
        
    def delete_plugin(self, plugin_file: str) -> Dict:
        """
        Delete a plugin
        
        Args:
            plugin_file: Plugin file
            
        Returns:
            Deletion result
        """
        logger.info(f"Deleting plugin: {plugin_file}")
        
        return self.client.post('/plugins/delete', {
            'plugin_file': plugin_file
        })
        
    def update_plugin(self, plugin_file: str) -> Dict:
        """
        Update a plugin to latest version
        
        Args:
            plugin_file: Plugin file
            
        Returns:
            Update result
        """
        logger.info(f"Updating plugin: {plugin_file}")
        
        return self.client.post('/plugins/update', {
            'plugin_file': plugin_file
        })
        
    def bulk_install_plugins(self, plugins: List[Dict], 
                           progress_callback: Optional[callable] = None) -> Dict:
        """
        Install multiple plugins
        
        Args:
            plugins: List of plugin dicts with 'path' or 'url' and optional 'activate'
            progress_callback: Callback for progress updates
            
        Returns:
            Results for each plugin
        """
        results = {
            'total': len(plugins),
            'success': 0,
            'failed': 0,
            'results': []
        }
        
        for i, plugin in enumerate(plugins):
            if progress_callback:
                progress_callback(i + 1, len(plugins), f"Installing plugin {i + 1}/{len(plugins)}")
                
            try:
                if 'path' in plugin:
                    # Local file
                    result = self.upload_plugin(
                        plugin['path'], 
                        activate=plugin.get('activate', False)
                    )
                elif 'url' in plugin:
                    # Remote URL
                    result = self.install_from_url(
                        plugin['url'],
                        activate=plugin.get('activate', False)
                    )
                else:
                    result = {'success': False, 'error': 'No path or URL provided'}
                    
                if result.get('success'):
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    
                results['results'].append({
                    'plugin': plugin,
                    'result': result
                })
                
            except Exception as e:
                logger.error(f"Error installing plugin: {e}")
                results['failed'] += 1
                results['results'].append({
                    'plugin': plugin,
                    'error': str(e)
                })
                
        return results
        
    def get_plugins_with_updates(self) -> List[Dict]:
        """
        Get list of plugins that have updates available
        
        Returns:
            List of plugins with updates
        """
        # Force update check to get accurate results
        try:
            result = self.client.get('/plugins', {'force_update_check': True})
            # API returns {'plugins': [...], 'count': N}, we just want the plugins list
            if isinstance(result, dict) and 'plugins' in result:
                all_plugins = result['plugins']
            else:
                all_plugins = result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error checking for plugin updates: {e}")
            # Fallback to regular list without forced check
            all_plugins = self.list_plugins()
        
        return [p for p in all_plugins if p.get('update_available', False)]
        
    def update_all_plugins(self, progress_callback: Optional[callable] = None) -> Dict:
        """
        Update all plugins that have updates available
        
        Args:
            progress_callback: Callback for progress updates
            
        Returns:
            Update results
        """
        plugins_to_update = self.get_plugins_with_updates()
        
        results = {
            'total': len(plugins_to_update),
            'success': 0,
            'failed': 0,
            'results': []
        }
        
        for i, plugin in enumerate(plugins_to_update):
            if progress_callback:
                plugin_name = plugin.get('name', 'Unknown')
                progress_callback(i + 1, len(plugins_to_update), f"Updating {plugin_name}")
                
            try:
                result = self.update_plugin(plugin['plugin_file'])
                
                if result.get('success'):
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    
                results['results'].append({
                    'plugin': plugin['name'],
                    'result': result
                })
                
            except Exception as e:
                logger.error(f"Error updating plugin {plugin['name']}: {e}")
                results['failed'] += 1
                results['results'].append({
                    'plugin': plugin['name'],
                    'error': str(e)
                })
                
        return results
        
    def export_plugin_list(self) -> Dict:
        """
        Export list of all plugins with their status
        
        Returns:
            Plugin list suitable for backup/migration
        """
        plugins = self.list_plugins()
        
        return {
            'site_url': self.client.site_url,
            'export_date': __import__('datetime').datetime.now().isoformat(),
            'total_plugins': len(plugins),
            'active_plugins': [p for p in plugins if p.get('active', False)],
            'inactive_plugins': [p for p in plugins if not p.get('active', False)],
            'plugins': plugins
        }