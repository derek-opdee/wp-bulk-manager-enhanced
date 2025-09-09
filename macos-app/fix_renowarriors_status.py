#!/usr/bin/env python3
"""
Fix RenoWarriors status and test connection
"""

import sqlite3
from wpbm_manager import WPBulkManager
import requests

def main():
    # First check database status
    conn = sqlite3.connect('wpbm_sites.db')
    cursor = conn.cursor()
    
    print("Checking RenoWarriors in database...")
    
    # Check if status column exists
    cursor.execute("PRAGMA table_info(sites)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Table columns: {columns}")
    
    # Get RenoWarriors data
    cursor.execute("SELECT * FROM sites WHERE name = 'RenoWarriors'")
    site_data = cursor.fetchone()
    
    if site_data:
        print("\nRenoWarriors found:")
        for i, col in enumerate(columns):
            print(f"  {col}: {site_data[i]}")
        
        # Check if we need to add status column
        if 'status' not in columns:
            print("\nAdding status column to sites table...")
            cursor.execute("ALTER TABLE sites ADD COLUMN status TEXT DEFAULT 'active'")
            conn.commit()
            print("✅ Status column added")
    
    conn.close()
    
    # Now test with manager
    print("\nTesting with WPBulkManager...")
    manager = WPBulkManager()
    
    # Get all sites (not just active)
    try:
        # Direct database query
        conn = sqlite3.connect('wpbm_sites.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, url FROM sites")
        all_sites = cursor.fetchall()
        
        print("\nAll sites in database:")
        for site in all_sites:
            print(f"  ID: {site[0]}, Name: {site[1]}, URL: {site[2]}")
        
        conn.close()
        
        # Test API connection
        print("\nTesting RenoWarriors API connection...")
        api_key = "0ab365b5b83f46b65bf12466c404bfd3"
        test_url = "https://renowarriors.com.au/wp-json/wp-bulk-manager/v1/test"
        
        response = requests.get(
            test_url,
            headers={'X-API-Key': api_key},
            timeout=10
        )
        
        print(f"API Response Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API connection successful!")
            print(f"Response: {response.json()}")
        else:
            print(f"Response: {response.text[:500]}")
            
            # Try the standard WordPress API
            print("\nTrying standard WordPress API...")
            wp_url = "https://renowarriors.com.au/wp-json/wp/v2/pages"
            wp_response = requests.get(wp_url, timeout=10)
            print(f"WordPress API Status: {wp_response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()