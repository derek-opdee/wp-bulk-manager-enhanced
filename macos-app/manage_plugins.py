#!/usr/bin/env python3
"""
WordPress Plugin Manager via WP Bulk Manager
"""
import sys
import os
import argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm import WPBMClient
from wpbm.operations.plugins import PluginOperations
from wpbm_manager import WPBulkManager
import json


def list_plugins(site_name: str):
    """List all plugins on a site"""
    client = get_client(site_name)
    plugin_ops = PluginOperations(client)
    
    plugins = plugin_ops.list_plugins()
    
    if not plugins:
        print("No plugins found or unable to retrieve plugins.")
        return
    
    print(f"\n📋 Plugins on {site_name}:")
    print("=" * 80)
    
    # Active plugins
    active = [p for p in plugins if p.get('active')]
    if active:
        print("\n✅ Active Plugins:")
        for p in active:
            update_marker = " 🔄" if p.get('update_available') else ""
            print(f"  • {p['name']} (v{p['version']}){update_marker}")
    
    # Inactive plugins
    inactive = [p for p in plugins if not p.get('active')]
    if inactive:
        print("\n⏸️  Inactive Plugins:")
        for p in inactive:
            update_marker = " 🔄" if p.get('update_available') else ""
            print(f"  • {p['name']} (v{p['version']}){update_marker}")
    
    # Updates available
    updates = [p for p in plugins if p.get('update_available')]
    if updates:
        print(f"\n🔄 Updates Available: {len(updates)} plugins")
        for p in updates:
            print(f"  • {p['name']}: v{p['version']} → v{p.get('update_version', 'latest')}")
    
    print(f"\n📊 Total: {len(plugins)} plugins ({len(active)} active, {len(inactive)} inactive)")


def upload_plugin(site_name: str, plugin_path: str, activate: bool = False):
    """Upload and install a plugin"""
    if not os.path.exists(plugin_path):
        print(f"❌ Error: Plugin file not found: {plugin_path}")
        return
    
    client = get_client(site_name)
    plugin_ops = PluginOperations(client)
    
    print(f"📤 Uploading plugin: {os.path.basename(plugin_path)}")
    print(f"   To site: {site_name}")
    print(f"   Activate: {'Yes' if activate else 'No'}")
    
    try:
        result = plugin_ops.upload_plugin(plugin_path, activate=activate)
        
        if result.get('success'):
            print("\n✅ Plugin installed successfully!")
            plugin_data = result.get('plugin_data', {})
            print(f"   Name: {plugin_data.get('name', 'Unknown')}")
            print(f"   Version: {plugin_data.get('version', 'Unknown')}")
            
            if result.get('activated'):
                print("   Status: Activated")
            else:
                print("   Status: Installed (not activated)")
                
            # Show installation messages
            messages = result.get('messages', [])
            if messages:
                print("\n📝 Installation log:")
                for msg in messages:
                    print(f"   {msg}")
        else:
            print(f"❌ Installation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def install_from_url(site_name: str, plugin_url: str, activate: bool = False):
    """Install plugin from URL"""
    client = get_client(site_name)
    plugin_ops = PluginOperations(client)
    
    print(f"🌐 Installing plugin from URL: {plugin_url}")
    print(f"   To site: {site_name}")
    print(f"   Activate: {'Yes' if activate else 'No'}")
    
    try:
        result = plugin_ops.install_from_url(plugin_url, activate=activate)
        
        if result.get('success'):
            print("\n✅ Plugin installed successfully!")
            plugin_data = result.get('plugin_data', {})
            print(f"   Name: {plugin_data.get('name', 'Unknown')}")
            print(f"   Version: {plugin_data.get('version', 'Unknown')}")
            
            if result.get('activated'):
                print("   Status: Activated")
        else:
            print(f"❌ Installation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def activate_plugin(site_name: str, plugin_file: str):
    """Activate a plugin"""
    client = get_client(site_name)
    plugin_ops = PluginOperations(client)
    
    print(f"🔌 Activating plugin: {plugin_file}")
    
    try:
        result = plugin_ops.activate_plugin(plugin_file)
        
        if result.get('success'):
            print("✅ Plugin activated successfully!")
        else:
            print(f"❌ Activation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def update_all_plugins(site_name: str):
    """Update all plugins with available updates"""
    client = get_client(site_name)
    plugin_ops = PluginOperations(client)
    
    print(f"🔄 Checking for plugin updates on {site_name}...")
    
    plugins_to_update = plugin_ops.get_plugins_with_updates()
    
    if not plugins_to_update:
        print("✅ All plugins are up to date!")
        return
    
    print(f"\nFound {len(plugins_to_update)} plugins with updates:")
    for p in plugins_to_update:
        print(f"  • {p['name']}: v{p['version']} → v{p.get('update_version', 'latest')}")
    
    confirm = input("\nUpdate all plugins? (y/N): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return
    
    print("\nUpdating plugins...")
    
    def progress(current, total, message):
        print(f"[{current}/{total}] {message}")
    
    results = plugin_ops.update_all_plugins(progress_callback=progress)
    
    print(f"\n📊 Update Summary:")
    print(f"   Successful: {results['success']}")
    print(f"   Failed: {results['failed']}")
    
    if results['failed'] > 0:
        print("\n❌ Failed updates:")
        for r in results['results']:
            if 'error' in r:
                print(f"   • {r['plugin']}: {r['error']}")


def bulk_install_from_config(site_name: str, config_file: str):
    """Install multiple plugins from a config file"""
    if not os.path.exists(config_file):
        print(f"❌ Error: Config file not found: {config_file}")
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    plugins = config.get('plugins', [])
    if not plugins:
        print("❌ No plugins found in config file")
        return
    
    client = get_client(site_name)
    plugin_ops = PluginOperations(client)
    
    print(f"📦 Installing {len(plugins)} plugins from config...")
    
    def progress(current, total, message):
        print(f"[{current}/{total}] {message}")
    
    results = plugin_ops.bulk_install_plugins(plugins, progress_callback=progress)
    
    print(f"\n📊 Installation Summary:")
    print(f"   Successful: {results['success']}")
    print(f"   Failed: {results['failed']}")
    
    if results['failed'] > 0:
        print("\n❌ Failed installations:")
        for r in results['results']:
            if 'error' in r:
                plugin_info = r['plugin'].get('path') or r['plugin'].get('url')
                print(f"   • {plugin_info}: {r['error']}")


def export_plugin_list(site_name: str, output_file: str = None):
    """Export plugin list for backup/migration"""
    client = get_client(site_name)
    plugin_ops = PluginOperations(client)
    
    print(f"📋 Exporting plugin list from {site_name}...")
    
    export_data = plugin_ops.export_plugin_list()
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        print(f"✅ Plugin list exported to: {output_file}")
    else:
        # Print to console
        print(json.dumps(export_data, indent=2))


def get_client(site_name: str) -> WPBMClient:
    """Get API client for a site"""
    manager = WPBulkManager()
    sites = manager.get_sites('all')
    
    site = None
    for s in sites:
        if s['name'].lower() == site_name.lower() or site_name.lower() in s['url'].lower():
            site = s
            break
    
    if not site:
        print(f"❌ Site '{site_name}' not found in WP Bulk Manager")
        print("\nAvailable sites:")
        for s in sites:
            print(f"  • {s['name']} ({s['url']})")
        sys.exit(1)
    
    api_key = manager.get_site_api_key(site['id'])
    
    if not api_key:
        print(f"❌ No API key found for {site['name']}")
        sys.exit(1)
    
    return WPBMClient(site['url'], api_key, cache_enabled=False)


def main():
    parser = argparse.ArgumentParser(description='WordPress Plugin Manager')
    parser.add_argument('site', help='Site name or URL')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List plugins
    list_parser = subparsers.add_parser('list', help='List all plugins')
    
    # Upload plugin
    upload_parser = subparsers.add_parser('upload', help='Upload and install plugin')
    upload_parser.add_argument('plugin_file', help='Path to plugin ZIP file')
    upload_parser.add_argument('--activate', action='store_true', help='Activate after installation')
    
    # Install from URL
    url_parser = subparsers.add_parser('install-url', help='Install plugin from URL')
    url_parser.add_argument('url', help='Plugin ZIP URL')
    url_parser.add_argument('--activate', action='store_true', help='Activate after installation')
    
    # Activate plugin
    activate_parser = subparsers.add_parser('activate', help='Activate a plugin')
    activate_parser.add_argument('plugin_file', help='Plugin file (e.g., plugin-name/plugin-name.php)')
    
    # Update all
    update_parser = subparsers.add_parser('update-all', help='Update all plugins')
    
    # Bulk install
    bulk_parser = subparsers.add_parser('bulk-install', help='Install multiple plugins from config')
    bulk_parser.add_argument('config_file', help='JSON config file with plugin list')
    
    # Export
    export_parser = subparsers.add_parser('export', help='Export plugin list')
    export_parser.add_argument('--output', '-o', help='Output file (default: print to console)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == 'list':
        list_plugins(args.site)
    elif args.command == 'upload':
        upload_plugin(args.site, args.plugin_file, args.activate)
    elif args.command == 'install-url':
        install_from_url(args.site, args.url, args.activate)
    elif args.command == 'activate':
        activate_plugin(args.site, args.plugin_file)
    elif args.command == 'update-all':
        update_all_plugins(args.site)
    elif args.command == 'bulk-install':
        bulk_install_from_config(args.site, args.config_file)
    elif args.command == 'export':
        export_plugin_list(args.site, args.output)


if __name__ == "__main__":
    main()

# Example usage:
# python manage_plugins.py opdee list
# python manage_plugins.py opdee upload /path/to/plugin.zip --activate
# python manage_plugins.py opdee install-url https://downloads.wordpress.org/plugin/akismet.latest.zip
# python manage_plugins.py opdee update-all
# python manage_plugins.py opdee export --output opdee-plugins.json