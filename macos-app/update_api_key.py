#!/usr/bin/env python3
"""
Update API key for a WordPress site in WP Bulk Manager
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm_manager import WPBulkManager
import keyring
import argparse


def update_api_key(site_name: str, new_api_key: str):
    """Update API key for an existing site"""
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
        return False
    
    # Test new API key
    print(f"🔄 Testing connection to {site['url']}...")
    if not manager.test_connection(site['url'], new_api_key):
        print(f"❌ Failed to connect with new API key. Please verify the key is correct.")
        return False
    
    # Update API key in keychain
    keyring.set_password("WPBulkManager", site['api_key_id'], new_api_key)
    print(f"✅ Successfully updated API key for {site['name']}")
    
    # Verify the update
    stored_key = manager.get_site_api_key(site['id'])
    if stored_key == new_api_key:
        print(f"✅ Verified: API key is correctly stored")
        print(f"   Site: {site['name']} ({site['url']})")
        print(f"   Key: {new_api_key[:8]}{'•' * (len(new_api_key) - 8)}")
    else:
        print(f"⚠️  Warning: Stored key verification failed")
    
    return True


def show_current_key(site_name: str):
    """Show current API key for a site"""
    manager = WPBulkManager()
    sites = manager.get_sites('all')
    
    site = None
    for s in sites:
        if s['name'].lower() == site_name.lower() or site_name.lower() in s['url'].lower():
            site = s
            break
    
    if not site:
        print(f"❌ Site '{site_name}' not found")
        return
    
    api_key = manager.get_site_api_key(site['id'])
    if api_key:
        print(f"Site: {site['name']} ({site['url']})")
        print(f"Current API Key: {api_key[:8]}{'•' * (len(api_key) - 8)}")
        print(f"Full key: {api_key}")
    else:
        print(f"No API key found for {site['name']}")


def main():
    parser = argparse.ArgumentParser(description='Update API key for WordPress site')
    parser.add_argument('site', help='Site name or URL')
    parser.add_argument('--key', help='New API key')
    parser.add_argument('--show', action='store_true', help='Show current API key')
    
    args = parser.parse_args()
    
    if args.show:
        show_current_key(args.site)
    elif args.key:
        update_api_key(args.site, args.key)
    else:
        print("Please provide either --key to update or --show to display current key")


if __name__ == '__main__':
    main()