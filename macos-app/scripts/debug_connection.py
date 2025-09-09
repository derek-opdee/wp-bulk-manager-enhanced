#!/usr/bin/env python3
import requests
import sys

# Test connection without storing anything
api_key = input("Enter API key: ")
url = "https://opdee.com"

print(f"\nTesting connection to {url}...")

try:
    response = requests.post(
        f"{url}/wp-json/wpbm/v1/auth",
        headers={'X-API-Key': api_key},
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Success!")
    else:
        print("❌ Failed")
        
except Exception as e:
    print(f"Error: {e}")