#!/usr/bin/env python3
"""
Fetch content from WordPress page 3616
"""

import os
import sqlite3
import requests
import keyring
from wpbm_manager import WPBulkManager

def get_page_content(site_url, api_key, page_id):
    """Fetch page content from WordPress site"""
    try:
        # Try to get page content
        response = requests.get(
            f"{site_url}/wp-json/wpbm/v1/content/{page_id}",
            headers={'X-API-Key': api_key},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch page content. Status code: {response.status_code}")
            # Try WordPress REST API directly
            print("\nTrying standard WordPress REST API...")
            response = requests.get(
                f"{site_url}/wp-json/wp/v2/pages/{page_id}",
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'id': data.get('id'),
                    'title': data.get('title', {}).get('rendered', ''),
                    'content': data.get('content', {}).get('rendered', ''),
                    'link': data.get('link', ''),
                    'status': data.get('status', '')
                }
            else:
                print(f"Standard API also failed. Status code: {response.status_code}")
                return None
    except Exception as e:
        print(f"Error fetching page content: {e}")
        return None

def main():
    """Main function to fetch page 3616"""
    # Initialize manager
    manager = WPBulkManager()
    
    # Get all sites
    sites = manager.get_sites('all')
    
    if not sites:
        print("No sites found in the database.")
        return
    
    print("Available sites:")
    for i, site in enumerate(sites):
        print(f"{i+1}. {site['name']} - {site['url']}")
    
    # Get site selection
    # For now, just use the first site
    if len(sites) > 0:
        selected_site = sites[0]
        print(f"\nUsing site: {selected_site['name']} - {selected_site['url']}")
    else:
        print("No sites available.")
        return
    
    # Get API key
    api_key = manager.get_site_api_key(selected_site['id'])
    
    if not api_key:
        print(f"No API key found for site: {selected_site['name']}")
        return
    
    print(f"\nFetching page 3616 from {selected_site['name']}...")
    
    # Fetch page content
    page_content = get_page_content(selected_site['url'], api_key, 3616)
    
    if page_content:
        print("\n" + "="*80)
        print(f"PAGE TITLE: {page_content.get('title', 'No title')}")
        print("="*80)
        print("\nPAGE CONTENT:")
        print("-"*80)
        print(page_content.get('content', 'No content found'))
        print("-"*80)
        
        # Save to file for easier reading
        with open('page_3616_content.html', 'w', encoding='utf-8') as f:
            f.write(f"<h1>{page_content.get('title', '')}</h1>\n")
            f.write(page_content.get('content', ''))
        print("\nContent also saved to: page_3616_content.html")
    else:
        print("Failed to fetch page content.")

if __name__ == '__main__':
    main()