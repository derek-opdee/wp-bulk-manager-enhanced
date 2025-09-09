#!/usr/bin/env python3
"""
Check RenoWarriors connection and status
"""

from wpbm_manager import WPBulkManager
import sqlite3

def main():
    manager = WPBulkManager()
    
    # Check database directly
    print("Checking database for RenoWarriors...")
    conn = sqlite3.connect('wpbm_sites.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sites WHERE url LIKE '%renowarriors%'")
    sites = cursor.fetchall()
    
    if sites:
        print(f"Found {len(sites)} entries for RenoWarriors:")
        cursor.execute("PRAGMA table_info(sites)")
        columns = [col[1] for col in cursor.fetchall()]
        
        for site in sites:
            print("\nSite details:")
            for i, col in enumerate(columns):
                print(f"  {col}: {site[i]}")
    else:
        print("RenoWarriors not found in database")
        
        # Try to add it
        print("\nAttempting to add RenoWarriors...")
        try:
            result = manager.add_site(
                name="RenoWarriors",
                url="https://renowarriors.com.au",
                api_key="0ab365b5b83f46b65bf12466c404bfd3"
            )
            if result:
                print(f"✅ Successfully added! Site ID: {result}")
            else:
                print("❌ Failed to add - checking error")
                
                # Check if URL already exists with different name
                cursor.execute("SELECT name, url FROM sites WHERE status = 'active'")
                all_sites = cursor.fetchall()
                print("\nAll active sites:")
                for site in all_sites:
                    print(f"  {site[0]}: {site[1]}")
        except Exception as e:
            print(f"Error: {e}")
    
    conn.close()
    
    # Now test the connection
    print("\nTesting API connection...")
    sites = manager.get_sites('active')
    
    for site in sites:
        if 'reno' in site['name'].lower() or 'reno' in site['url'].lower():
            print(f"\nTesting {site['name']} ({site['url']})...")
            
            # Try to get content
            try:
                api_key = site.get('api_key', '0ab365b5b83f46b65bf12466c404bfd3')
                test_url = f"{site['url']}/wp-json/wp-bulk-manager/v1/test"
                
                import requests
                response = requests.get(
                    test_url,
                    headers={'X-API-Key': api_key},
                    timeout=10
                )
                
                if response.status_code == 200:
                    print("✅ API connection successful!")
                else:
                    print(f"❌ API returned status: {response.status_code}")
                    print(f"Response: {response.text[:200]}")
            except Exception as e:
                print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    main()