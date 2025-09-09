#!/usr/bin/env python3
"""
Comprehensive test of derekzar.com using WordPress Bulk Manager
Tests all functionality and provides detailed report
"""

import sys
import json
import requests
from datetime import datetime
from wpbm_manager_mysql import WPBulkManagerMySQL
from wpbm.api.client import WPBMClient
from wpbm.utils.logger import get_logger

logger = get_logger(__name__)
import time

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def test_derekzar_site():
    """Comprehensive test of derekzar.com functionality"""
    
    print("WordPress Bulk Manager - Comprehensive Test for derekzar.com")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize manager
    manager = WPBulkManagerMySQL()
    site_id = 2  # derekzar site ID from database
    
    # Test results storage
    results = {
        "site": "derekzar.com",
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # 1. Test Site Connection
    print_section("1. Testing Site Connection")
    try:
        site = manager.get_site_by_id(site_id)
        if site:
            print(f"✅ Site found: {site['name']} ({site['url']})")
            print(f"   API Key: {'*' * 10}{site['api_key'][-10:] if site['api_key'] else 'NOT SET'}")
            results["tests"]["connection"] = {"status": "passed", "site": site}
        else:
            print("❌ Site not found in database")
            results["tests"]["connection"] = {"status": "failed", "error": "Site not found"}
            return results
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        results["tests"]["connection"] = {"status": "failed", "error": str(e)}
        return results
    
    # Initialize API client
    api_client = WPBMClient(site['url'], site['api_key'])
    
    # 2. Test API Endpoints
    print_section("2. Testing API Endpoints")
    endpoints_to_test = [
        ("Plugin Status", "/wp-json/wp-bulk-manager/v1/status"),
        ("SEO Status", "/wp-json/wp-bulk-manager/v1/seo/status"),
        ("Content Types", "/wp-json/wp/v2/types"),
        ("Pages", "/wp-json/wp/v2/pages?per_page=1"),
        ("Posts", "/wp-json/wp/v2/posts?per_page=1"),
        ("Media", "/wp-json/wp/v2/media?per_page=1"),
        ("Plugins", "/wp-json/wp-bulk-manager/v1/plugins"),
        ("Themes", "/wp-json/wp-bulk-manager/v1/themes")
    ]
    
    results["tests"]["endpoints"] = {}
    
    for name, endpoint in endpoints_to_test:
        try:
            response = api_client.request('GET', endpoint)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
                results["tests"]["endpoints"][name] = {"status": "passed", "code": 200}
            else:
                print(f"❌ {name}: Failed (Status: {response.status_code})")
                results["tests"]["endpoints"][name] = {"status": "failed", "code": response.status_code}
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
            results["tests"]["endpoints"][name] = {"status": "failed", "error": str(e)}
        time.sleep(0.5)  # Rate limiting
    
    # 3. List Content
    print_section("3. Listing Content (Pages and Posts)")
    results["tests"]["content"] = {}
    
    try:
        # List pages
        print("\nPages:")
        pages = manager.list_content(site_id, 'page', 10)
        results["tests"]["content"]["pages"] = {"count": len(pages), "items": []}
        
        if pages:
            for page in pages[:5]:  # Show first 5
                print(f"  - ID: {page['id']} | {page['title']} | Status: {page['status']}")
                results["tests"]["content"]["pages"]["items"].append({
                    "id": page['id'], 
                    "title": page['title'], 
                    "status": page['status']
                })
        else:
            print("  No pages found")
        
        # List posts
        print("\nPosts:")
        posts = manager.list_content(site_id, 'post', 10)
        results["tests"]["content"]["posts"] = {"count": len(posts), "items": []}
        
        if posts:
            for post in posts[:5]:  # Show first 5
                print(f"  - ID: {post['id']} | {post['title']} | Status: {post['status']}")
                results["tests"]["content"]["posts"]["items"].append({
                    "id": post['id'], 
                    "title": post['title'], 
                    "status": post['status']
                })
        else:
            print("  No posts found")
            
    except Exception as e:
        print(f"❌ Error listing content: {e}")
        results["tests"]["content"]["error"] = str(e)
    
    # 4. Test Plugin Management
    print_section("4. Testing Plugin Management")
    results["tests"]["plugins"] = {}
    
    try:
        plugins = manager.list_plugins(site_id)
        results["tests"]["plugins"]["count"] = len(plugins)
        results["tests"]["plugins"]["list"] = []
        
        print(f"Total plugins: {len(plugins)}")
        
        # Check for SEO plugins
        seo_plugins = ['the-seo-framework', 'wordpress-seo', 'all-in-one-seo-pack', 'rankmath']
        found_seo = False
        
        for plugin in plugins:
            plugin_info = {
                "name": plugin['name'],
                "status": plugin['status'],
                "slug": plugin['plugin']
            }
            results["tests"]["plugins"]["list"].append(plugin_info)
            
            if any(seo in plugin['plugin'].lower() for seo in seo_plugins):
                print(f"  📌 SEO Plugin Found: {plugin['name']} - Status: {plugin['status']}")
                found_seo = True
                results["tests"]["plugins"]["seo_plugin"] = plugin_info
        
        if not found_seo:
            print("  ⚠️  No SEO plugin detected")
            
        # Show first 5 plugins
        print("\nInstalled plugins (first 5):")
        for plugin in plugins[:5]:
            status_icon = "✅" if plugin['status'] == 'active' else "⭕"
            print(f"  {status_icon} {plugin['name']} ({plugin['status']})")
            
    except Exception as e:
        print(f"❌ Error listing plugins: {e}")
        results["tests"]["plugins"]["error"] = str(e)
    
    # 5. Test SEO Data
    print_section("5. Testing SEO Functionality")
    results["tests"]["seo"] = {}
    
    try:
        # Get SEO data for a few pages
        seo_data = manager.get_all_seo_data(site_id, 5)
        results["tests"]["seo"]["pages_checked"] = len(seo_data)
        results["tests"]["seo"]["issues"] = []
        
        if seo_data:
            print(f"SEO data retrieved for {len(seo_data)} pages")
            
            # Analyze SEO issues
            for page in seo_data:
                issues = []
                
                if not page['seo_title'] or len(page['seo_title']) < 30:
                    issues.append("Missing or short SEO title")
                if not page['seo_description'] or len(page['seo_description']) < 100:
                    issues.append("Missing or short meta description")
                    
                if issues:
                    results["tests"]["seo"]["issues"].append({
                        "page_id": page['id'],
                        "title": page['title'],
                        "issues": issues
                    })
                    print(f"  ⚠️  Page {page['id']} ({page['title']}): {', '.join(issues)}")
        else:
            print("  No SEO data available")
            
    except Exception as e:
        print(f"❌ Error checking SEO: {e}")
        results["tests"]["seo"]["error"] = str(e)
    
    # 6. Test Create/Update Capabilities
    print_section("6. Testing Create/Update Capabilities")
    results["tests"]["crud"] = {}
    
    try:
        # Test creating a draft page
        test_page_data = {
            "title": "WPBM Test Page - " + datetime.now().strftime("%Y%m%d_%H%M%S"),
            "content": "This is a test page created by WP Bulk Manager comprehensive test.",
            "status": "draft"
        }
        
        print("Creating test page...")
        response = api_client.request('POST', '/wp-json/wp/v2/pages', json=test_page_data)
        
        if response.status_code == 201:
            test_page = response.json()
            print(f"✅ Test page created successfully - ID: {test_page['id']}")
            results["tests"]["crud"]["create"] = {"status": "passed", "page_id": test_page['id']}
            
            # Try to update it
            print("Updating test page...")
            update_data = {
                "content": test_page_data["content"] + "\n\nUpdated at: " + datetime.now().isoformat()
            }
            
            update_response = api_client.request('POST', f'/wp-json/wp/v2/pages/{test_page["id"]}', json=update_data)
            
            if update_response.status_code == 200:
                print("✅ Test page updated successfully")
                results["tests"]["crud"]["update"] = {"status": "passed"}
            else:
                print(f"❌ Failed to update test page: {update_response.status_code}")
                results["tests"]["crud"]["update"] = {"status": "failed", "code": update_response.status_code}
            
            # Delete the test page
            print("Deleting test page...")
            delete_response = api_client.request('DELETE', f'/wp-json/wp/v2/pages/{test_page["id"]}')
            
            if delete_response.status_code == 200:
                print("✅ Test page deleted successfully")
                results["tests"]["crud"]["delete"] = {"status": "passed"}
            else:
                print(f"⚠️  Could not delete test page: {delete_response.status_code}")
                results["tests"]["crud"]["delete"] = {"status": "failed", "code": delete_response.status_code}
                
        else:
            print(f"❌ Failed to create test page: {response.status_code}")
            results["tests"]["crud"]["create"] = {"status": "failed", "code": response.status_code}
            
    except Exception as e:
        print(f"❌ Error testing CRUD operations: {e}")
        results["tests"]["crud"]["error"] = str(e)
    
    # 7. Test Media Upload
    print_section("7. Testing Media Capabilities")
    results["tests"]["media"] = {}
    
    try:
        # Just check if we can list media
        media_response = api_client.request('GET', '/wp-json/wp/v2/media?per_page=5')
        
        if media_response.status_code == 200:
            media_items = media_response.json()
            print(f"✅ Media endpoint working - Found {len(media_items)} media items")
            results["tests"]["media"]["status"] = "passed"
            results["tests"]["media"]["count"] = len(media_items)
            
            if media_items:
                print("Recent media:")
                for item in media_items[:3]:
                    print(f"  - {item.get('title', {}).get('rendered', 'Untitled')} ({item.get('media_type', 'unknown')})")
        else:
            print(f"❌ Media endpoint error: {media_response.status_code}")
            results["tests"]["media"]["status"] = "failed"
            results["tests"]["media"]["code"] = media_response.status_code
            
    except Exception as e:
        print(f"❌ Error checking media: {e}")
        results["tests"]["media"]["error"] = str(e)
    
    # Final Summary
    print_section("Test Summary")
    
    passed_tests = 0
    failed_tests = 0
    
    for test_name, test_result in results["tests"].items():
        if isinstance(test_result, dict):
            if test_result.get("status") == "passed":
                passed_tests += 1
            elif test_result.get("error") or test_result.get("status") == "failed":
                failed_tests += 1
    
    print(f"\n✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save results to file
    with open('test_derekzar_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to: test_derekzar_results.json")
    
    return results

if __name__ == "__main__":
    try:
        results = test_derekzar_site()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)