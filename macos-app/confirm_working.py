#!/usr/bin/env python3
"""
Confirm WP Bulk Manager v2 is working with current API key
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm import WPBMClient

# Test with current API key
client = WPBMClient(
    site_url="https://opdee.com",
    api_key="TJtdmqCA0VoNS4BkmjzIJN1kVbXyWddi",
    cache_enabled=True
)

print("✅ Testing opdee.com with API key: TJtdmqCA0VoNS4BkmjzIJN1kVbXyWddi")
print()

# Get some pages
pages = client.get_content(content_type='page', limit=5)
print(f"✅ SUCCESS! Found {len(pages)} pages:")
for page in pages:
    print(f"   • {page['title']} (ID: {page['id']}, Status: {page['status']})")

# Update local keychain
try:
    from wpbm_manager import WPBulkManager
    import keyring
    
    manager = WPBulkManager()
    sites = manager.get_sites('all')
    
    for site in sites:
        if 'opdee' in site['url'].lower():
            keyring.set_password("WPBulkManager", f"site_{site['id']}", "TJtdmqCA0VoNS4BkmjzIJN1kVbXyWddi")
            print(f"\n✅ Updated opdee.com API key in local keychain")
            break
except:
    pass

print("\n💡 To fix the clearing issue permanently:")
print("   Upload 'wp-bulk-manager-client-separated.php' which keeps")
print("   API key management completely separate from other settings.")