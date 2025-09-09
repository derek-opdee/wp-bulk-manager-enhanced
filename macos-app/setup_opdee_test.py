#!/usr/bin/env python3
"""
Setup opdee.com for testing if API key is available
"""
import os
import sys

# Add the wpbm package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm_manager_v2 import WPBulkManagerV2

# Try to get API key from environment
api_key = (os.environ.get('OPDEE_API_KEY') or 
           os.environ.get('WPBM_OPDEE_API_KEY') or
           os.environ.get('API_KEY'))  # Try generic API_KEY

if not api_key:
    print("❌ No API key found in environment variables")
    print("Please set one of the following:")
    print("  - OPDEE_API_KEY")
    print("  - WPBM_OPDEE_API_KEY")
    print("  - API_KEY (generic)")
    print("\nOr run ./add_opdee.sh to add manually")
    sys.exit(1)

# Add opdee.com
manager = WPBulkManagerV2()

print("Adding opdee.com to WP Bulk Manager...")
success = manager.add_site("Opdee", "https://opdee.com", api_key)

if success:
    print("✅ Successfully added opdee.com")
    print("\nConfigured sites:")
    for site in manager.list_sites():
        print(f"  - {site['name']}: {site['url']}")
else:
    print("❌ Failed to add opdee.com")
    sys.exit(1)