#!/usr/bin/env python3
"""
Simple comprehensive test of derekzar.com using WordPress Bulk Manager
"""

import sys
import json
import requests
from datetime import datetime
from wpbm_manager_mysql import WPBulkManagerMySQL
from wpbm.api.client import WPBMClient
import time

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def test_derekzar():
    """Test derekzar.com functionality"""
    
    print("WordPress Bulk Manager - Testing derekzar.com")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize manager
    manager = WPBulkManagerMySQL()
    
    # Test results storage
    results = {
        "site": "derekzar.com",
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # 1. Find derekzar site
    print_section("1. Finding derekzar Site")
    
    site_info = None
    site_id = None
    
    try:
        sites = manager.list_sites()
        for site in sites:
            if 'derekzar' in site.get('name', '').lower() or 'derekzar' in site.get('url', '').lower():
                site_info = manager.get_site_info(site['name'])
                site_id = site['id']
                print(f"✅ Found derekzar site:")
                print(f"   - ID: {site_id}")
                print(f"   - Name: {site_info['name']}")
                print(f"   - URL: {site_info['url']}")
                print(f"   - API Key: {'*' * 20}{site_info['api_key'][-10:] if site_info.get('api_key') else 'NOT SET'}")
                results["tests"]["site_found"] = {"status": "passed", "site": site_info}
                break
        
        if not site_info:
            print("❌ derekzar site not found!")
            results["tests"]["site_found"] = {"status": "failed", "error": "Site not found"}
            return results
            
    except Exception as e:
        print(f"❌ Error finding site: {e}")
        results["tests"]["site_found"] = {"status": "failed", "error": str(e)}
        return results
    
    # Initialize API client
    api_client = WPBMClient(site_info['url'], site_info['api_key'])
    
    # 2. Test Basic Connection
    print_section("2. Testing API Connection")
    
    try:
        # Test WP Bulk Manager plugin status
        response = api_client.request('GET', '/wp-json/wp-bulk-manager/v1/status')
        if response.status_code == 200:
            print("✅ WP Bulk Manager plugin is active")
            results["tests"]["plugin_status"] = {"status": "passed", "data": response.json()}
        else:
            print(f"❌ WP Bulk Manager plugin issue - Status: {response.status_code}")
            results["tests"]["plugin_status"] = {"status": "failed", "code": response.status_code}
    except Exception as e:
        print(f"❌ Connection error: {e}")
        results["tests"]["plugin_status"] = {"status": "failed", "error": str(e)}
    
    # 3. List Content
    print_section("3. Content Overview")
    
    try:
        # Pages
        pages = manager.list_content(site_id, 'page', 100)
        print(f"\nPages: {len(pages)} total")
        results["tests"]["pages"] = {"count": len(pages), "items": []}
        
        if pages:
            print("Recent pages:")
            for page in pages[:5]:
                print(f"  - ID: {page['id']} | {page['title'][:50]}{'...' if len(page['title']) > 50 else ''}")
                results["tests"]["pages"]["items"].append({
                    "id": page['id'],
                    "title": page['title'],
                    "status": page['status']
                })
        
        # Posts
        posts = manager.list_content(site_id, 'post', 100)
        print(f"\nPosts: {len(posts)} total")
        results["tests"]["posts"] = {"count": len(posts), "items": []}
        
        if posts:
            print("Recent posts:")
            for post in posts[:5]:
                print(f"  - ID: {post['id']} | {post['title'][:50]}{'...' if len(post['title']) > 50 else ''}")
                results["tests"]["posts"]["items"].append({
                    "id": post['id'],
                    "title": post['title'],
                    "status": post['status']
                })
                
    except Exception as e:
        print(f"❌ Error listing content: {e}")
        results["tests"]["content_error"] = str(e)
    
    # 4. Check Plugins
    print_section("4. Plugin Status")
    
    try:
        plugins = manager.list_plugins(site_id)
        active_plugins = [p for p in plugins if p['status'] == 'active']
        
        print(f"Total plugins: {len(plugins)}")
        print(f"Active plugins: {len(active_plugins)}")
        
        results["tests"]["plugins"] = {
            "total": len(plugins),
            "active": len(active_plugins),
            "list": []
        }
        
        # Check for specific plugins
        important_plugins = {
            'wp-bulk-manager': 'WP Bulk Manager Client',
            'the-seo-framework': 'The SEO Framework',
            'wordpress-seo': 'Yoast SEO',
            'all-in-one-seo': 'All in One SEO',
            'rankmath': 'Rank Math'
        }
        
        print("\nImportant plugins:")
        for plugin in plugins:
            plugin_slug = plugin['plugin'].split('/')[0]
            if plugin_slug in important_plugins:
                status_icon = "✅" if plugin['status'] == 'active' else "⭕"
                print(f"  {status_icon} {plugin['name']} ({plugin['status']})")
                results["tests"]["plugins"]["list"].append({
                    "name": plugin['name'],
                    "status": plugin['status'],
                    "slug": plugin_slug
                })
                
    except Exception as e:
        print(f"❌ Error checking plugins: {e}")
        results["tests"]["plugins_error"] = str(e)
    
    # 5. Test CRUD Operations
    print_section("5. Testing Create/Update/Delete")
    
    try:
        # Create test page
        test_title = f"Test Page - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_content = "This is a test page created by WP Bulk Manager to verify functionality."
        
        print("Creating test page...")
        test_page_data = {
            "title": test_title,
            "content": test_content,
            "status": "draft"
        }
        
        response = api_client.request('POST', '/wp-json/wp/v2/pages', json=test_page_data)
        
        if response.status_code == 201:
            test_page = response.json()
            print(f"✅ Created page ID: {test_page['id']}")
            results["tests"]["create"] = {"status": "passed", "page_id": test_page['id']}
            
            # Update test
            print("Updating test page...")
            update_data = {"content": test_content + "\n\nUpdated!"}
            update_response = api_client.request('POST', f'/wp-json/wp/v2/pages/{test_page["id"]}', json=update_data)
            
            if update_response.status_code == 200:
                print("✅ Update successful")
                results["tests"]["update"] = {"status": "passed"}
            else:
                print(f"❌ Update failed: {update_response.status_code}")
                results["tests"]["update"] = {"status": "failed", "code": update_response.status_code}
            
            # Delete test
            print("Deleting test page...")
            delete_response = api_client.request('DELETE', f'/wp-json/wp/v2/pages/{test_page["id"]}')
            
            if delete_response.status_code == 200:
                print("✅ Delete successful")
                results["tests"]["delete"] = {"status": "passed"}
            else:
                print(f"⚠️  Delete issue: {delete_response.status_code}")
                results["tests"]["delete"] = {"status": "warning", "code": delete_response.status_code}
                
        else:
            print(f"❌ Create failed: {response.status_code}")
            results["tests"]["create"] = {"status": "failed", "code": response.status_code}
            
    except Exception as e:
        print(f"❌ CRUD test error: {e}")
        results["tests"]["crud_error"] = str(e)
    
    # 6. Check SEO
    print_section("6. SEO Functionality")
    
    try:
        # Get SEO data
        seo_data = manager.get_all_seo_data(site_id, 10)
        
        if seo_data:
            print(f"✅ SEO data available for {len(seo_data)} pages")
            
            seo_issues = 0
            for page in seo_data[:5]:
                issues = []
                if not page.get('seo_title'):
                    issues.append("no title")
                if not page.get('seo_description'):
                    issues.append("no description")
                
                if issues:
                    seo_issues += 1
                    print(f"  ⚠️  Page {page['id']}: {', '.join(issues)}")
            
            results["tests"]["seo"] = {
                "status": "passed",
                "pages_checked": len(seo_data),
                "issues_found": seo_issues
            }
        else:
            print("⚠️  No SEO data available")
            results["tests"]["seo"] = {"status": "warning", "message": "No SEO data"}
            
    except Exception as e:
        print(f"❌ SEO check error: {e}")
        results["tests"]["seo"] = {"status": "failed", "error": str(e)}
    
    # 7. API Endpoints Check
    print_section("7. API Endpoints Status")
    
    endpoints = [
        ("Pages", "/wp-json/wp/v2/pages?per_page=1"),
        ("Posts", "/wp-json/wp/v2/posts?per_page=1"),
        ("Media", "/wp-json/wp/v2/media?per_page=1"),
        ("Users", "/wp-json/wp/v2/users?per_page=1"),
        ("Categories", "/wp-json/wp/v2/categories?per_page=1"),
        ("Tags", "/wp-json/wp/v2/tags?per_page=1")
    ]
    
    results["tests"]["endpoints"] = {}
    
    for name, endpoint in endpoints:
        try:
            response = api_client.request('GET', endpoint)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
                results["tests"]["endpoints"][name] = "working"
            else:
                print(f"❌ {name}: Status {response.status_code}")
                results["tests"]["endpoints"][name] = f"error_{response.status_code}"
        except Exception as e:
            print(f"❌ {name}: Error")
            results["tests"]["endpoints"][name] = "error"
        time.sleep(0.3)  # Rate limiting
    
    # Summary
    print_section("Test Summary")
    
    # Count results
    passed = failed = warnings = 0
    for test_name, test_data in results["tests"].items():
        if isinstance(test_data, dict):
            status = test_data.get("status", "")
            if status == "passed":
                passed += 1
            elif status == "failed":
                failed += 1
            elif status == "warning":
                warnings += 1
    
    print(f"\n✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Warnings: {warnings}")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save results
    with open('derekzar_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: derekzar_test_results.json")
    
    return results

if __name__ == "__main__":
    try:
        results = test_derekzar()
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)