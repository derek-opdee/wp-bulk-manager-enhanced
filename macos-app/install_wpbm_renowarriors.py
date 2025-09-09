#!/usr/bin/env python3
"""
Guide to install WP Bulk Manager on RenoWarriors.com.au
"""

print("""
========================================
WP BULK MANAGER INSTALLATION GUIDE
For: renowarriors.com.au
========================================

To complete the SEO and spelling updates, the WP Bulk Manager plugin needs to be installed on RenoWarriors.

STEP 1: Install the Plugin
--------------------------
1. Log in to WordPress admin at: https://renowarriors.com.au/wp-admin
2. Go to Plugins > Add New > Upload Plugin
3. Upload the plugin file from:
   /Users/derekzar/Documents/Projects/wp-bulk-manager/wordpress-plugin/

   Use the file: wp-bulk-manager-client-robust.php
   (You may need to zip it first with includes folder)

4. Activate the plugin

STEP 2: Configure the Plugin
----------------------------
1. After activation, go to Tools > WP Bulk Manager
2. Click "Generate New API Key"
3. Save the generated API key
4. Add your IP address to the allowed IPs list (optional but recommended)

STEP 3: Update the Local Database
---------------------------------
Once installed, update the API key in the local database:

Run: python update_api_key.py

Enter:
- Site: RenoWarriors
- New API Key: [the key generated in step 2]

STEP 4: Run the Updates
----------------------
After setup, run: python wpbm_assistant.py

Then execute these commands:
- assistant = wpbm_connect()
- assistant.select_site('RenoWarriors')
- wpbm_generate_report(assistant)

CURRENT FINDINGS:
----------------
✅ 16 published pages found
❌ All 16 pages are missing SEO titles/descriptions
❌ 10 pages contain US spelling that needs to be changed to Australian English

The updates will:
1. Add SEO titles focusing on "Southeast Melbourne" and "Patterson Lakes, VIC"
2. Fix US spellings: color→colour, center→centre, organize→organise, etc.
3. Only update SEO metadata and spelling (not adding location keywords to content)

========================================
""")

# Also create a quick check script
with open('check_wpbm_installed.py', 'w') as f:
    f.write("""#!/usr/bin/env python3
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
""")

print("\nCreated: check_wpbm_installed.py")
print("Run this to check if the plugin is installed: python check_wpbm_installed.py")