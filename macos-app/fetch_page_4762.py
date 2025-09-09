#!/usr/bin/env python3
import requests
import json

# Direct connection to Opdee
base_url = "https://opdee.com"
api_key = "27013065aa24d225b5ea9db967d191f3"

# Set up API endpoint
api_url = f"{base_url}/wp-json/wpbm/v1/content/4762"
headers = {
    'X-API-Key': api_key
}

# Fetch the page
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    page = response.json()
    
    # Save full JSON first to see structure
    with open('page_4762_full.json', 'w') as f:
        json.dump(page, f, indent=2)
    
    print(f"Page ID: {page['id']}")
    print(f"Title: {page['title']}")
    print(f"Status: {page['status']}")
    if 'permalink' in page:
        print(f"URL: {page['permalink']}")
    print("\n--- Current Content ---\n")
    print(page['content'])
    
    # Save to file for reference
    with open('page_4762_content.html', 'w') as f:
        f.write(page['content'])
    
    # Also save full JSON for reference
    with open('page_4762_full.json', 'w') as f:
        json.dump(page, f, indent=2)
    
    print("\n--- Meta Data ---")
    print(f"SEO Title: {page.get('seo_title', 'N/A')}")
    print(f"SEO Description: {page.get('seo_description', 'N/A')}")
else:
    print(f"Error fetching page: {response.status_code}")
    print(response.text)