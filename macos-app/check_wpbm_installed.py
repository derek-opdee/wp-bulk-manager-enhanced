#!/usr/bin/env python3
import requests

# Check if WP Bulk Manager is installed
url = "https://renowarriors.com.au/wp-json/wp-bulk-manager/v1/test"
response = requests.get(url, timeout=5)

if response.status_code == 401:
    print("✅ WP Bulk Manager is installed (authentication required)")
elif response.status_code == 404:
    print("❌ WP Bulk Manager not installed yet")
else:
    print(f"Status: {response.status_code}")
