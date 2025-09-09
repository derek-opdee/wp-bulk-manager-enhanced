#!/usr/bin/env python3
"""
Working comprehensive test of derekzar.com using WordPress Bulk Manager
"""

import mysql.connector
import json
from datetime import datetime
from wpbm.api.client import WPBMClient
import time
import sys

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def test_derekzar():
    """Comprehensive test of derekzar.com"""
    
    print("🔍 WordPress Bulk Manager - Comprehensive Test for derekzar.com")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "site": "derekzar.com",
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Load database config
    with open('config/database.json', 'r') as f:
        db_config = json.load(f)['database']
    
    # Connect to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # 1. Get site information
    print_section("1. Site Connection & Configuration")
    
    cursor.execute("SELECT * FROM sites WHERE name = 'derekzar'")
    site = cursor.fetchone()
    
    if not site:
        print("❌ derekzar site not found in database!")
        results["tests"]["site_connection"] = {"status": "failed", "error": "Site not found"}
        return results
    
    print(f"✅ Found derekzar site:")
    print(f"   - ID: {site['id']}")
    print(f"   - Name: {site['name']}")
    print(f"   - URL: {site['url']}")
    print(f"   - Status: {site['status']}")
    print(f"   - Created: {site['created_at']}")
    
    # Get API key
    cursor.execute("SELECT * FROM api_keys WHERE site_id = %s AND is_active = 1", (site['id'],))
    api_key_record = cursor.fetchone()
    
    if not api_key_record:
        print("❌ No active API key found!")
        results["tests"]["api_key"] = {"status": "failed", "error": "No API key"}
        return results
    
    api_key = api_key_record['api_key']
    print(f"   - API Key: {'*' * 32}{api_key[-8:]}")
    
    results["tests"]["site_connection"] = {
        "status": "passed",
        "site_id": site['id'],
        "url": site['url']
    }
    
    # Initialize API client
    api_client = WPBMClient(site['url'], api_key)
    
    # 2. Test API endpoints
    print_section("2. API Endpoints Test")
    
    endpoints_tested = 0
    endpoints_working = 0
    
    # Test WordPress REST API
    try:
        data = api_client.get('/wp-json/wp/v2/')
        print("✅ WordPress REST API is accessible")
        endpoints_tested += 1
        endpoints_working += 1
    except Exception as e:
        print(f"❌ WordPress REST API error: {e}")
        endpoints_tested += 1
    
    # Test WP Bulk Manager plugin
    try:
        data = api_client.get('/wp-json/wp-bulk-manager/v1/status')
        print("✅ WP Bulk Manager plugin is active")
        if isinstance(data, dict):
            print(f"   - Version: {data.get('version', 'Unknown')}")
            print(f"   - Status: {data.get('status', 'Unknown')}")
        endpoints_tested += 1
        endpoints_working += 1
        results["tests"]["wpbm_plugin"] = {"status": "passed", "data": data}
    except Exception as e:
        print(f"❌ WP Bulk Manager plugin error: {e}")
        endpoints_tested += 1
        results["tests"]["wpbm_plugin"] = {"status": "failed", "error": str(e)}
    
    # Test other endpoints
    test_endpoints = [
        ("Pages", "/wp-json/wp/v2/pages?per_page=1"),
        ("Posts", "/wp-json/wp/v2/posts?per_page=1"),
        ("Media", "/wp-json/wp/v2/media?per_page=1"),
        ("Plugins", "/wp-json/wp-bulk-manager/v1/plugins"),
        ("SEO", "/wp-json/wp-bulk-manager/v1/seo/status")
    ]
    
    for name, endpoint in test_endpoints:
        try:
            data = api_client.get(endpoint)
            print(f"✅ {name} endpoint working")
            endpoints_tested += 1
            endpoints_working += 1
        except Exception as e:
            print(f"❌ {name} endpoint error: {str(e)[:50]}...")
            endpoints_tested += 1
        time.sleep(0.3)
    
    print(f"\n   Summary: {endpoints_working}/{endpoints_tested} endpoints working")
    results["tests"]["endpoints"] = {
        "total": endpoints_tested,
        "working": endpoints_working
    }
    
    # 3. Content Analysis
    print_section("3. Content Overview")
    
    try:
        # Get pages
        pages = api_client.get_content('page', limit=200)
        published_pages = [p for p in pages if p.get('status') == 'publish']
        draft_pages = [p for p in pages if p.get('status') == 'draft']
        
        print(f"\n📄 Pages:")
        print(f"   - Total: {len(pages)}")
        print(f"   - Published: {len(published_pages)}")
        print(f"   - Drafts: {len(draft_pages)}")
        
        if pages:
            print("\n   Recent pages:")
            for page in pages[:5]:
                title = page.get('title', {}).get('rendered', 'Untitled')
                print(f"     • ID {page['id']}: {title[:60]}{'...' if len(title) > 60 else ''}")
        
        results["tests"]["pages"] = {
            "total": len(pages),
            "published": len(published_pages),
            "drafts": len(draft_pages)
        }
        
    except Exception as e:
        print(f"❌ Error fetching pages: {e}")
        results["tests"]["pages"] = {"error": str(e)}
    
    try:
        # Get posts
        posts = api_client.get_content('post', limit=200)
        published_posts = [p for p in posts if p.get('status') == 'publish']
        draft_posts = [p for p in posts if p.get('status') == 'draft']
        
        print(f"\n📝 Posts:")
        print(f"   - Total: {len(posts)}")
        print(f"   - Published: {len(published_posts)}")
        print(f"   - Drafts: {len(draft_posts)}")
        
        if posts:
            print("\n   Recent posts:")
            for post in posts[:5]:
                title = post.get('title', {}).get('rendered', 'Untitled')
                print(f"     • ID {post['id']}: {title[:60]}{'...' if len(title) > 60 else ''}")
        
        results["tests"]["posts"] = {
            "total": len(posts),
            "published": len(published_posts),
            "drafts": len(draft_posts)
        }
        
    except Exception as e:
        print(f"❌ Error fetching posts: {e}")
        results["tests"]["posts"] = {"error": str(e)}
    
    # 4. Plugin Management
    print_section("4. Plugin Status")
    
    try:
        plugins_data = api_client.get('/wp-json/wp-bulk-manager/v1/plugins')
        
        if isinstance(plugins_data, list):
            plugins = plugins_data
        elif isinstance(plugins_data, dict) and 'plugins' in plugins_data:
            plugins = plugins_data['plugins']
        else:
            plugins = []
        
        active_plugins = [p for p in plugins if p.get('status') == 'active']
        
        print(f"\n🔌 Plugin Overview:")
        print(f"   - Total: {len(plugins)}")
        print(f"   - Active: {len(active_plugins)}")
        
        # Check for important plugins
        seo_plugins = ['seo', 'yoast', 'rankmath', 'all-in-one']
        security_plugins = ['wordfence', 'sucuri', 'ithemes', 'security']
        
        print("\n   Important plugins found:")
        
        for plugin in plugins:
            plugin_name = plugin.get('name', '').lower()
            plugin_file = plugin.get('plugin', '').lower()
            
            # Check for SEO plugins
            if any(seo in plugin_name or seo in plugin_file for seo in seo_plugins):
                status = "✅" if plugin.get('status') == 'active' else "⭕"
                print(f"     {status} SEO: {plugin['name']}")
            
            # Check for security plugins
            if any(sec in plugin_name or sec in plugin_file for sec in security_plugins):
                status = "✅" if plugin.get('status') == 'active' else "⭕"
                print(f"     {status} Security: {plugin['name']}")
            
            # Check for WP Bulk Manager
            if 'wp-bulk-manager' in plugin_file:
                status = "✅" if plugin.get('status') == 'active' else "⭕"
                print(f"     {status} WP Bulk Manager: {plugin['name']}")
        
        results["tests"]["plugins"] = {
            "total": len(plugins),
            "active": len(active_plugins)
        }
        
    except Exception as e:
        print(f"❌ Plugin check error: {e}")
        results["tests"]["plugins"] = {"error": str(e)}
    
    # 5. CRUD Operations Test
    print_section("5. Create/Read/Update/Delete Test")
    
    try:
        # Create test page
        test_title = f"WPBM Test - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_data = {
            "title": test_title,
            "content": "<p>This is a test page created by WP Bulk Manager.</p>",
            "status": "draft"
        }
        
        print(f"\n📝 Creating test page: '{test_title}'")
        created_page = api_client.create_content(test_data)
        
        if created_page and 'id' in created_page:
            test_id = created_page['id']
            print(f"✅ Created successfully - ID: {test_id}")
            results["tests"]["crud_create"] = {"status": "passed", "page_id": test_id}
            
            # Read test
            print("\n📖 Reading test page...")
            read_page = api_client.get_content_by_id(test_id)
            
            if read_page:
                print("✅ Read successful")
                results["tests"]["crud_read"] = {"status": "passed"}
            else:
                print("❌ Read failed")
                results["tests"]["crud_read"] = {"status": "failed"}
            
            # Update test
            print("\n✏️  Updating test page...")
            update_data = {
                "content": test_data["content"] + f"\n<p>Updated at: {datetime.now().isoformat()}</p>"
            }
            
            updated_page = api_client.update_content(test_id, update_data)
            
            if updated_page:
                print("✅ Update successful")
                results["tests"]["crud_update"] = {"status": "passed"}
            else:
                print("❌ Update failed")
                results["tests"]["crud_update"] = {"status": "failed"}
            
            # Delete test
            print("\n🗑️  Deleting test page...")
            delete_result = api_client.delete_content(test_id)
            
            if delete_result:
                print("✅ Delete successful")
                results["tests"]["crud_delete"] = {"status": "passed"}
            else:
                print("⚠️  Delete may have failed")
                results["tests"]["crud_delete"] = {"status": "warning"}
        else:
            print("❌ Create failed")
            results["tests"]["crud_create"] = {"status": "failed"}
            
    except Exception as e:
        print(f"❌ CRUD test error: {e}")
        results["tests"]["crud_error"] = str(e)
    
    # 6. SEO Functionality
    print_section("6. SEO Analysis")
    
    try:
        seo_status = api_client.get('/wp-json/wp-bulk-manager/v1/seo/status')
        
        if seo_status:
            print(f"✅ SEO functionality available")
            print(f"   - Plugin: {seo_status.get('plugin', 'Unknown')}")
            print(f"   - Active: {seo_status.get('active', False)}")
            
            # Try to get SEO data for some pages
            if pages[:5]:  # Use first 5 pages from earlier
                print("\n   SEO data for sample pages:")
                seo_issues = 0
                
                for page in pages[:5]:
                    try:
                        seo_data = api_client.get(f'/wp-json/wp-bulk-manager/v1/seo/{page["id"]}')
                        if seo_data:
                            has_title = bool(seo_data.get('title'))
                            has_desc = bool(seo_data.get('description'))
                            
                            if not has_title or not has_desc:
                                seo_issues += 1
                                issues = []
                                if not has_title:
                                    issues.append("no title")
                                if not has_desc:
                                    issues.append("no description")
                                print(f"     ⚠️  Page {page['id']}: {', '.join(issues)}")
                            else:
                                print(f"     ✅ Page {page['id']}: SEO data complete")
                    except:
                        pass
                
                if seo_issues > 0:
                    print(f"\n   Found {seo_issues} pages with SEO issues")
            
            results["tests"]["seo"] = {"status": "passed", "plugin": seo_status.get('plugin')}
        else:
            print("⚠️  SEO functionality not available")
            results["tests"]["seo"] = {"status": "warning", "message": "Not available"}
            
    except Exception as e:
        print(f"❌ SEO check error: {e}")
        results["tests"]["seo"] = {"status": "failed", "error": str(e)}
    
    # 7. Media Library
    print_section("7. Media Library Check")
    
    try:
        media_items = api_client.get_media(limit=10)
        
        print(f"✅ Media library accessible - {len(media_items)} items found")
        
        if media_items:
            print("\n   Recent media:")
            for item in media_items[:5]:
                title = item.get('title', {}).get('rendered', 'Untitled')
                media_type = item.get('media_type', 'unknown')
                print(f"     • {title} ({media_type})")
        
        results["tests"]["media"] = {
            "status": "passed",
            "count": len(media_items)
        }
        
    except Exception as e:
        print(f"❌ Media check error: {e}")
        results["tests"]["media"] = {"status": "failed", "error": str(e)}
    
    # Summary
    print_section("📊 Test Summary")
    
    # Count results
    passed = 0
    failed = 0
    warnings = 0
    
    for test_name, test_data in results["tests"].items():
        if isinstance(test_data, dict):
            if test_data.get("status") == "passed":
                passed += 1
            elif test_data.get("status") == "failed" or "error" in test_data:
                failed += 1
            elif test_data.get("status") == "warning":
                warnings += 1
    
    print(f"\n✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Warnings: {warnings}")
    
    # Key findings
    print("\n🔑 Key Findings:")
    
    # Connection status
    if results["tests"].get("site_connection", {}).get("status") == "passed":
        print("   • Site is properly connected with valid API key")
    
    # WP Bulk Manager status
    if results["tests"].get("wpbm_plugin", {}).get("status") == "passed":
        print("   • WP Bulk Manager plugin is active and responding")
    
    # Content summary
    pages_total = results["tests"].get("pages", {}).get("total", 0)
    posts_total = results["tests"].get("posts", {}).get("total", 0)
    if pages_total or posts_total:
        print(f"   • Content found: {pages_total} pages, {posts_total} posts")
    
    # Plugin summary
    plugins_data = results["tests"].get("plugins", {})
    if "total" in plugins_data:
        print(f"   • Plugins: {plugins_data['total']} total, {plugins_data['active']} active")
    
    # CRUD status
    crud_tests = ["crud_create", "crud_read", "crud_update", "crud_delete"]
    crud_passed = sum(1 for t in crud_tests if results["tests"].get(t, {}).get("status") == "passed")
    if crud_passed == 4:
        print("   • All CRUD operations working perfectly")
    elif crud_passed > 0:
        print(f"   • {crud_passed}/4 CRUD operations working")
    
    # SEO status
    if results["tests"].get("seo", {}).get("status") == "passed":
        seo_plugin = results["tests"]["seo"].get("plugin", "Unknown")
        print(f"   • SEO functionality available via {seo_plugin}")
    
    print(f"\n🏁 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save results
    with open('derekzar_comprehensive_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Detailed results saved to: derekzar_comprehensive_test_results.json")
    
    # Close database
    cursor.close()
    conn.close()
    
    return results

if __name__ == "__main__":
    try:
        results = test_derekzar()
        
        # Exit with appropriate code
        if any(test.get("status") == "failed" or "error" in test 
               for test in results["tests"].values() 
               if isinstance(test, dict)):
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)