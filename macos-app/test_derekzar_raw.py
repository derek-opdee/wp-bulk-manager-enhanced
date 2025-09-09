#!/usr/bin/env python3
"""
Raw test of derekzar.com WordPress site using direct API calls
"""

import requests
import json
import mysql.connector
from datetime import datetime

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def test_derekzar_raw():
    """Direct API test of derekzar.com"""
    
    print("🔍 WordPress Bulk Manager - Raw API Test for derekzar.com")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get API key from database
    with open('config/database.json', 'r') as f:
        db_config = json.load(f)['database']
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT s.*, ak.api_key 
        FROM sites s 
        JOIN api_keys ak ON s.id = ak.site_id 
        WHERE s.name = 'derekzar' AND ak.is_active = 1
    """)
    site = cursor.fetchone()
    
    if not site:
        print("❌ Site or API key not found!")
        return
    
    api_key = site['api_key']
    site_url = site['url'].rstrip('/')
    
    print(f"✅ Site: {site_url}")
    print(f"✅ API Key: {'*' * 32}{api_key[-8:]}")
    
    # Set up headers
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Test results
    results = {
        "working": [],
        "failed": [],
        "issues": []
    }
    
    # 1. Test WordPress REST API
    print_section("1. WordPress REST API Test")
    
    test_endpoints = [
        ("API Index", f"{site_url}/wp-json/"),
        ("WP v2 Index", f"{site_url}/wp-json/wp/v2/"),
        ("Pages", f"{site_url}/wp-json/wp/v2/pages?per_page=1"),
        ("Posts", f"{site_url}/wp-json/wp/v2/posts?per_page=1"),
        ("Media", f"{site_url}/wp-json/wp/v2/media?per_page=1"),
        ("Users", f"{site_url}/wp-json/wp/v2/users?per_page=1"),
        ("Categories", f"{site_url}/wp-json/wp/v2/categories?per_page=1")
    ]
    
    for name, url in test_endpoints:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
                results["working"].append(name)
            elif response.status_code == 401:
                print(f"🔒 {name}: Authentication required")
                results["issues"].append(f"{name}: Auth required")
            else:
                print(f"❌ {name}: Status {response.status_code}")
                results["failed"].append(f"{name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)[:50]}")
            results["failed"].append(f"{name}: Connection error")
    
    # 2. Test WP Bulk Manager Plugin
    print_section("2. WP Bulk Manager Plugin Test")
    
    wpbm_endpoints = [
        ("Plugin Status", f"{site_url}/wp-json/wp-bulk-manager/v1/status"),
        ("Plugins List", f"{site_url}/wp-json/wp-bulk-manager/v1/plugins"),
        ("Themes List", f"{site_url}/wp-json/wp-bulk-manager/v1/themes"),
        ("SEO Status", f"{site_url}/wp-json/wp-bulk-manager/v1/seo/status"),
        ("SEO Data", f"{site_url}/wp-json/wp-bulk-manager/v1/seo"),
        ("Backup", f"{site_url}/wp-json/wp-bulk-manager/v1/backup"),
        ("Search Replace", f"{site_url}/wp-json/wp-bulk-manager/v1/search-replace")
    ]
    
    wpbm_working = False
    
    for name, url in wpbm_endpoints:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
                results["working"].append(f"WPBM: {name}")
                wpbm_working = True
                
                # Show details for some endpoints
                if "status" in name.lower():
                    data = response.json()
                    if isinstance(data, dict):
                        print(f"   Details: {json.dumps(data, indent=2)[:200]}")
                        
            elif response.status_code == 404:
                print(f"⚠️  {name}: Not found (404)")
                results["issues"].append(f"WPBM: {name} not found")
            else:
                print(f"❌ {name}: Status {response.status_code}")
                results["failed"].append(f"WPBM: {name} - {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)[:50]}")
            results["failed"].append(f"WPBM: {name} error")
    
    if not wpbm_working:
        print("\n⚠️  WP Bulk Manager plugin may not be installed or active!")
        results["issues"].append("WP Bulk Manager plugin not detected")
    
    # 3. Test Content Access
    print_section("3. Content Access Test")
    
    try:
        # Get pages
        response = requests.get(f"{site_url}/wp-json/wp/v2/pages?per_page=5", headers=headers)
        if response.status_code == 200:
            pages = response.json()
            print(f"✅ Can access pages: {len(pages)} found")
            
            if pages:
                print("\n   Sample pages:")
                for page in pages[:3]:
                    title = page.get('title', {}).get('rendered', 'Untitled')
                    status = page.get('status', 'unknown')
                    print(f"     • ID {page['id']}: {title} ({status})")
        else:
            print(f"❌ Cannot access pages: {response.status_code}")
            
        # Get posts
        response = requests.get(f"{site_url}/wp-json/wp/v2/posts?per_page=5", headers=headers)
        if response.status_code == 200:
            posts = response.json()
            print(f"\n✅ Can access posts: {len(posts)} found")
            
            if posts:
                print("\n   Sample posts:")
                for post in posts[:3]:
                    title = post.get('title', {}).get('rendered', 'Untitled')
                    status = post.get('status', 'unknown')
                    print(f"     • ID {post['id']}: {title} ({status})")
        else:
            print(f"❌ Cannot access posts: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Content access error: {e}")
    
    # 4. Test CRUD Operations
    print_section("4. CRUD Operations Test")
    
    try:
        # Create test page
        test_data = {
            "title": f"API Test - {datetime.now().strftime('%H%M%S')}",
            "content": "This is a test page created via direct API call",
            "status": "draft"
        }
        
        print("📝 Creating test page...")
        response = requests.post(
            f"{site_url}/wp-json/wp/v2/pages",
            headers=headers,
            json=test_data
        )
        
        if response.status_code == 201:
            created_page = response.json()
            test_id = created_page['id']
            print(f"✅ Created page ID: {test_id}")
            
            # Read it back
            print("📖 Reading test page...")
            response = requests.get(f"{site_url}/wp-json/wp/v2/pages/{test_id}", headers=headers)
            
            if response.status_code == 200:
                print("✅ Read successful")
                
                # Update it
                print("✏️  Updating test page...")
                update_data = {"content": test_data["content"] + "\n\nUpdated!"}
                response = requests.post(
                    f"{site_url}/wp-json/wp/v2/pages/{test_id}",
                    headers=headers,
                    json=update_data
                )
                
                if response.status_code == 200:
                    print("✅ Update successful")
                    
                    # Delete it
                    print("🗑️  Deleting test page...")
                    response = requests.delete(
                        f"{site_url}/wp-json/wp/v2/pages/{test_id}?force=true",
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        print("✅ Delete successful")
                        print("\n✅ All CRUD operations working!")
                        results["working"].append("CRUD operations")
                    else:
                        print(f"⚠️  Delete returned: {response.status_code}")
                else:
                    print(f"❌ Update failed: {response.status_code}")
            else:
                print(f"❌ Read failed: {response.status_code}")
        else:
            print(f"❌ Create failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            results["failed"].append("CRUD operations")
            
    except Exception as e:
        print(f"❌ CRUD test error: {e}")
        results["failed"].append("CRUD operations")
    
    # Summary
    print_section("📊 Test Summary")
    
    print(f"\n✅ Working features: {len(results['working'])}")
    for feature in results['working']:
        print(f"   • {feature}")
    
    if results['failed']:
        print(f"\n❌ Failed features: {len(results['failed'])}")
        for feature in results['failed']:
            print(f"   • {feature}")
    
    if results['issues']:
        print(f"\n⚠️  Issues found: {len(results['issues'])}")
        for issue in results['issues']:
            print(f"   • {issue}")
    
    # Key findings
    print("\n🔑 Key Findings:")
    
    if "CRUD operations" in results["working"]:
        print("   • WordPress REST API is fully functional")
        print("   • Can create, read, update, and delete content")
    
    if any("WPBM:" in w for w in results["working"]):
        print("   • WP Bulk Manager plugin is installed and partially working")
    elif "WP Bulk Manager plugin not detected" in results["issues"]:
        print("   • ⚠️  WP Bulk Manager plugin needs to be installed or activated")
    
    if len(results["working"]) > len(results["failed"]):
        print("   • Overall system is functioning well")
    else:
        print("   • ⚠️  Several features need attention")
    
    print(f"\n🏁 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Close database
    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        test_derekzar_raw()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()