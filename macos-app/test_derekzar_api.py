#!/usr/bin/env python3
"""Test derekzar.com API directly"""

import requests
import base64
import json

def test_api():
    # API credentials
    api_key = '0b2d82ec91d2d876558ce460e57a7a1e'
    auth_string = base64.b64encode(api_key.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/json'
    }
    
    # Test endpoints
    base_url = 'https://derekzar.com/wp-json/wp/v2'
    
    print("Testing derekzar.com API endpoints...")
    print("=" * 50)
    
    # Test pages
    print("\n📄 Testing Pages endpoint...")
    resp = requests.get(f'{base_url}/pages', headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        pages = resp.json()
        print(f"Found {len(pages)} pages")
        for page in pages:
            title = page.get('title', {}).get('rendered', 'Untitled')
            status = page.get('status')
            page_id = page.get('id')
            print(f"  - ID {page_id}: {title} (status: {status})")
    else:
        print(f"Error: {resp.text[:200]}")
    
    # Test posts
    print("\n📰 Testing Posts endpoint...")
    resp = requests.get(f'{base_url}/posts', headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        posts = resp.json()
        print(f"Found {len(posts)} posts")
        for post in posts[:3]:
            title = post.get('title', {}).get('rendered', 'Untitled')
            print(f"  - {title}")
    
    # Test WPBM endpoint
    print("\n🔌 Testing WPBM endpoint...")
    resp = requests.get(f'{base_url}/wpbm/v1/status', headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"WPBM plugin is active: {resp.json()}")
    else:
        print("WPBM plugin might not be installed or activated")

if __name__ == "__main__":
    test_api()