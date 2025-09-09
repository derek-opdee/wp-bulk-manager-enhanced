#!/usr/bin/env python3
"""
Setup derekzar.com in wpbm system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm.api.auth import APIKeyManager

# Site configuration
SITE_URL = "https://derekzar.com"
SITE_NAME = "derekzar"

print(f"Setting up {SITE_NAME} ({SITE_URL})")
print("Please provide the WordPress API key for derekzar.com")
print("You can get this from: WordPress Admin → WP Bulk Manager → API Keys")

api_key = input("Enter API key: ").strip()

if not api_key:
    print("❌ No API key provided")
    sys.exit(1)

# Initialize API key manager
auth_manager = APIKeyManager()

# Add the site
auth_manager.add_site(SITE_NAME, SITE_URL, api_key)

print(f"✅ {SITE_NAME} added successfully!")
print("You can now run the SEO fix script.")