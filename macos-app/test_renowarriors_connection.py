#!/usr/bin/env python3
"""
Test connection to RenoWarriors site
"""

from wpbm_manager_v2 import WPBulkManagerV2
from wpbm_cli_enhanced import EnhancedWPBulkManager

# First ensure site is added
manager_v2 = WPBulkManagerV2()
print("Adding RenoWarriors to manager...")
success = manager_v2.add_site(
    name='RenoWarriors',
    url='https://renowarriors.com.au',
    api_key='0ab365b5b83f46b65bf12466c404bfd3'
)
print(f"Add site result: {success}")

# List all sites
print("\nAll sites in database:")
sites = manager_v2.list_sites()
for site in sites:
    print(f"  - {site['name']}: {site['url']}")

# Test with enhanced manager
print("\nTesting with enhanced manager...")
enhanced = EnhancedWPBulkManager()
active_sites = enhanced.get_sites('active')
print(f"Active sites: {len(active_sites)}")
for site in active_sites:
    print(f"  - ID: {site['id']}, Name: {site['name']}, URL: {site['url']}")

# Test API connection
print("\nTesting API connection...")
client = manager_v2.get_client('RenoWarriors')
if client:
    print("✅ Client created successfully")
    # Test a simple API call
    try:
        response = client.get('/wp-bulk-manager/v1/test')
        print(f"API test response: {response}")
    except Exception as e:
        print(f"API test error: {e}")
else:
    print("❌ Failed to create client")