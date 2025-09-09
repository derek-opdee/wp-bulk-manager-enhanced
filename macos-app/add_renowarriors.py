#!/usr/bin/env python3
"""
Add RenoWarriors.com.au to WP Bulk Manager
"""

from wpbm_manager import WPBulkManager

def main():
    manager = WPBulkManager()
    
    print("Adding RenoWarriors.com.au to WP Bulk Manager...")
    
    # Use the stored API key
    api_key = '0ab365b5b83f46b65bf12466c404bfd3'
    print(f"Using stored API key: {api_key[:10]}...")
    
    # Add the site
    result = manager.add_site(
        name="RenoWarriors",
        url="https://renowarriors.com.au",
        api_key=api_key
    )
    
    if result:
        print(f"✅ Successfully added RenoWarriors!")
        print(f"   Site ID: {result}")
        
        # Verify connection
        sites = manager.get_sites('active')
        for site in sites:
            if site['name'] == 'RenoWarriors':
                print(f"   URL: {site['url']}")
                print(f"   Status: {site['status']}")
    else:
        print("❌ Failed to add RenoWarriors")

if __name__ == "__main__":
    main()