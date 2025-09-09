#!/usr/bin/env python3
"""
Comprehensive test of derekzar.com using WordPress Bulk Manager
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
    """Comprehensive test of derekzar.com functionality"""
    
    print("🔍 WordPress Bulk Manager - Comprehensive Test for derekzar.com")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize manager
    manager = WPBulkManagerMySQL()
    
    # Test results storage
    results = {
        "site": "derekzar.com",
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # 1. Find and verify derekzar site
    print_section("1. Site Connection & Configuration")
    
    site_info = None
    site_id = None
    
    try:
        sites = manager.list_sites()
        for site in sites:
            if site['name'] == 'derekzar':
                site_id = site['id']
                # Get detailed site info
                site_info = manager.get_site_info('derekzar')
                
                print(f"✅ Found derekzar site:")
                print(f"   - ID: {site_id}")
                print(f"   - Name: {site_info['name']}")
                print(f"   - URL: {site_info['url']}")
                print(f"   - Status: {site['status']}")
                print(f"   - API Keys: {site['api_key_count']}")
                print(f"   - Created: {site['created_at']}")
                
                # Get API key
                if site_info.get('api_key'):
                    print(f"   - API Key: {'*' * 30}{site_info['api_key'][-10:]}")
                else:
                    print("   - API Key: NOT SET")
                
                results["tests"]["site_connection"] = {
                    "status": "passed",
                    "site_id": site_id,
                    "url": site_info['url'],
                    "api_keys": site['api_key_count']
                }
                break
        
        if not site_info:
            print("❌ derekzar site not found in database!")
            results["tests"]["site_connection"] = {"status": "failed", "error": "Site not found"}
            return results
            
    except Exception as e:
        print(f"❌ Error connecting to site: {e}")
        results["tests"]["site_connection"] = {"status": "failed", "error": str(e)}
        return results
    
    # Initialize API client
    if not site_info.get('api_key'):
        print("\n❌ No API key found for derekzar site!")
        results["tests"]["api_key"] = {"status": "failed", "error": "No API key"}
        return results
    
    api_client = WPBMClient(site_info['url'], site_info['api_key'])
    
    # 2. Test WP Bulk Manager Plugin
    print_section("2. WP Bulk Manager Plugin Status")
    
    try:
        response = api_client.request('GET', '/wp-json/wp-bulk-manager/v1/status')
        if response.status_code == 200:
            status_data = response.json()
            print("✅ WP Bulk Manager plugin is active")
            print(f"   - Version: {status_data.get('version', 'Unknown')}")
            print(f"   - Status: {status_data.get('status', 'Unknown')}")
            results["tests"]["wpbm_plugin"] = {"status": "passed", "data": status_data}
        else:
            print(f"❌ WP Bulk Manager plugin issue - Status: {response.status_code}")
            results["tests"]["wpbm_plugin"] = {"status": "failed", "code": response.status_code}
    except Exception as e:
        print(f"❌ Cannot reach WP Bulk Manager plugin: {e}")
        results["tests"]["wpbm_plugin"] = {"status": "failed", "error": str(e)}
    
    # 3. Content Overview
    print_section("3. Content Analysis")
    
    try:
        # Pages
        print("\n📄 Pages:")
        pages = manager.list_content(site_id, 'page', 200)
        published_pages = [p for p in pages if p['status'] == 'publish']
        draft_pages = [p for p in pages if p['status'] == 'draft']
        
        print(f"   - Total: {len(pages)}")
        print(f"   - Published: {len(published_pages)}")
        print(f"   - Drafts: {len(draft_pages)}")
        
        results["tests"]["pages"] = {
            "total": len(pages),
            "published": len(published_pages),
            "drafts": len(draft_pages),
            "samples": []
        }
        
        if pages:
            print("\n   Recent pages:")
            for page in pages[:5]:
                print(f"     • ID {page['id']}: {page['title'][:60]}{'...' if len(page['title']) > 60 else ''}")
                print(f"       Status: {page['status']} | Modified: {page['modified']}")
                results["tests"]["pages"]["samples"].append({
                    "id": page['id'],
                    "title": page['title'],
                    "status": page['status']
                })
        
        # Posts
        print("\n📝 Posts:")
        posts = manager.list_content(site_id, 'post', 200)
        published_posts = [p for p in posts if p['status'] == 'publish']
        draft_posts = [p for p in posts if p['status'] == 'draft']
        
        print(f"   - Total: {len(posts)}")
        print(f"   - Published: {len(published_posts)}")
        print(f"   - Drafts: {len(draft_posts)}")
        
        results["tests"]["posts"] = {
            "total": len(posts),
            "published": len(published_posts),
            "drafts": len(draft_posts),
            "samples": []
        }
        
        if posts:
            print("\n   Recent posts:")
            for post in posts[:5]:
                print(f"     • ID {post['id']}: {post['title'][:60]}{'...' if len(post['title']) > 60 else ''}")
                print(f"       Status: {post['status']} | Modified: {post['modified']}")
                results["tests"]["posts"]["samples"].append({
                    "id": post['id'],
                    "title": post['title'],
                    "status": post['status']
                })
                
    except Exception as e:
        print(f"❌ Error analyzing content: {e}")
        results["tests"]["content_error"] = str(e)
    
    # 4. Plugin Analysis
    print_section("4. Plugin Management")
    
    try:
        plugins = manager.list_plugins(site_id)
        active_plugins = [p for p in plugins if p['status'] == 'active']
        inactive_plugins = [p for p in plugins if p['status'] == 'inactive']
        
        print(f"\n🔌 Plugin Overview:")
        print(f"   - Total: {len(plugins)}")
        print(f"   - Active: {len(active_plugins)}")
        print(f"   - Inactive: {len(inactive_plugins)}")
        
        results["tests"]["plugins"] = {
            "total": len(plugins),
            "active": len(active_plugins),
            "inactive": len(inactive_plugins),
            "important": {}
        }
        
        # Check for important plugins
        important_checks = {
            'wp-bulk-manager-client': 'WP Bulk Manager Client',
            'the-seo-framework': 'The SEO Framework',
            'wordpress-seo': 'Yoast SEO',
            'all-in-one-seo-pack': 'All in One SEO',
            'seo-by-rank-math': 'Rank Math SEO'
        }
        
        print("\n   Important plugins:")
        seo_plugin_found = False
        
        for plugin in plugins:
            plugin_file = plugin['plugin']
            plugin_slug = plugin_file.split('/')[0] if '/' in plugin_file else plugin_file
            
            # Check if it's an important plugin
            for check_slug, friendly_name in important_checks.items():
                if check_slug in plugin_slug.lower():
                    status_icon = "✅" if plugin['status'] == 'active' else "⭕"
                    print(f"     {status_icon} {plugin['name']} ({plugin['status']})")
                    results["tests"]["plugins"]["important"][friendly_name] = {
                        "installed": True,
                        "active": plugin['status'] == 'active',
                        "name": plugin['name']
                    }
                    
                    if 'seo' in plugin_slug.lower() and plugin['status'] == 'active':
                        seo_plugin_found = True
        
        if not seo_plugin_found:
            print("     ⚠️  No active SEO plugin detected")
            results["tests"]["plugins"]["seo_warning"] = "No active SEO plugin found"
            
    except Exception as e:
        print(f"❌ Error checking plugins: {e}")
        results["tests"]["plugins_error"] = str(e)
    
    # 5. SEO Analysis
    print_section("5. SEO Configuration")
    
    try:
        print("\n🔍 Checking SEO data...")
        seo_data = manager.get_all_seo_data(site_id, 20)
        
        if seo_data:
            pages_with_seo = len([p for p in seo_data if p.get('seo_title') or p.get('seo_description')])
            pages_missing_title = len([p for p in seo_data if not p.get('seo_title')])
            pages_missing_desc = len([p for p in seo_data if not p.get('seo_description')])
            
            print(f"   - Pages analyzed: {len(seo_data)}")
            print(f"   - Pages with SEO data: {pages_with_seo}")
            print(f"   - Missing SEO titles: {pages_missing_title}")
            print(f"   - Missing meta descriptions: {pages_missing_desc}")
            
            results["tests"]["seo"] = {
                "status": "passed",
                "analyzed": len(seo_data),
                "with_seo": pages_with_seo,
                "missing_titles": pages_missing_title,
                "missing_descriptions": pages_missing_desc
            }
            
            if pages_missing_title > 0 or pages_missing_desc > 0:
                print("\n   Pages needing SEO attention:")
                count = 0
                for page in seo_data:
                    if not page.get('seo_title') or not page.get('seo_description'):
                        issues = []
                        if not page.get('seo_title'):
                            issues.append("no title")
                        if not page.get('seo_description'):
                            issues.append("no desc")
                        print(f"     ⚠️  Page {page['id']}: {page['title'][:40]}... - {', '.join(issues)}")
                        count += 1
                        if count >= 5:
                            print("     ... and more")
                            break
        else:
            print("   ⚠️  No SEO data available")
            results["tests"]["seo"] = {"status": "warning", "message": "No SEO data available"}
            
    except Exception as e:
        print(f"❌ SEO analysis error: {e}")
        results["tests"]["seo"] = {"status": "failed", "error": str(e)}
    
    # 6. CRUD Operations Test
    print_section("6. Create/Read/Update/Delete Test")
    
    try:
        # Create test page
        test_title = f"WPBM Test Page - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_content = "<p>This is a test page created by WP Bulk Manager to verify CRUD functionality.</p>"
        
        print(f"\n📝 Creating test page: '{test_title}'")
        test_page_data = {
            "title": test_title,
            "content": test_content,
            "status": "draft"
        }
        
        create_response = api_client.request('POST', '/wp-json/wp/v2/pages', json=test_page_data)
        
        if create_response.status_code == 201:
            test_page = create_response.json()
            test_page_id = test_page['id']
            print(f"✅ Created successfully - ID: {test_page_id}")
            results["tests"]["crud_create"] = {"status": "passed", "page_id": test_page_id}
            
            # Read test
            print(f"\n📖 Reading test page...")
            read_response = api_client.request('GET', f'/wp-json/wp/v2/pages/{test_page_id}')
            
            if read_response.status_code == 200:
                print("✅ Read successful")
                results["tests"]["crud_read"] = {"status": "passed"}
            else:
                print(f"❌ Read failed: {read_response.status_code}")
                results["tests"]["crud_read"] = {"status": "failed", "code": read_response.status_code}
            
            # Update test
            print(f"\n✏️  Updating test page...")
            update_data = {
                "content": test_content + f"\n<p>Updated at: {datetime.now().isoformat()}</p>"
            }
            update_response = api_client.request('POST', f'/wp-json/wp/v2/pages/{test_page_id}', json=update_data)
            
            if update_response.status_code == 200:
                print("✅ Update successful")
                results["tests"]["crud_update"] = {"status": "passed"}
            else:
                print(f"❌ Update failed: {update_response.status_code}")
                results["tests"]["crud_update"] = {"status": "failed", "code": update_response.status_code}
            
            # Delete test
            print(f"\n🗑️  Deleting test page...")
            delete_response = api_client.request('DELETE', f'/wp-json/wp/v2/pages/{test_page_id}?force=true')
            
            if delete_response.status_code == 200:
                print("✅ Delete successful")
                results["tests"]["crud_delete"] = {"status": "passed"}
            else:
                print(f"⚠️  Delete returned status: {delete_response.status_code}")
                results["tests"]["crud_delete"] = {"status": "warning", "code": delete_response.status_code}
                
        else:
            print(f"❌ Create failed: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            results["tests"]["crud_create"] = {"status": "failed", "code": create_response.status_code}
            
    except Exception as e:
        print(f"❌ CRUD test error: {e}")
        results["tests"]["crud_error"] = str(e)
    
    # 7. API Endpoints Health Check
    print_section("7. API Endpoints Health Check")
    
    endpoints = [
        ("WordPress Core", "/wp-json/wp/v2/", "✅"),
        ("Pages", "/wp-json/wp/v2/pages?per_page=1", "📄"),
        ("Posts", "/wp-json/wp/v2/posts?per_page=1", "📝"),
        ("Media", "/wp-json/wp/v2/media?per_page=1", "🖼️"),
        ("Categories", "/wp-json/wp/v2/categories?per_page=1", "📁"),
        ("Tags", "/wp-json/wp/v2/tags?per_page=1", "🏷️"),
        ("Users", "/wp-json/wp/v2/users?per_page=1", "👤"),
        ("Comments", "/wp-json/wp/v2/comments?per_page=1", "💬")
    ]
    
    results["tests"]["endpoints"] = {}
    working_endpoints = 0
    
    for name, endpoint, icon in endpoints:
        try:
            response = api_client.request('GET', endpoint)
            if response.status_code == 200:
                print(f"{icon} {name}: Working")
                results["tests"]["endpoints"][name] = "working"
                working_endpoints += 1
            elif response.status_code == 401:
                print(f"🔒 {name}: Requires authentication")
                results["tests"]["endpoints"][name] = "auth_required"
            else:
                print(f"❌ {name}: Status {response.status_code}")
                results["tests"]["endpoints"][name] = f"error_{response.status_code}"
        except Exception as e:
            print(f"❌ {name}: Connection error")
            results["tests"]["endpoints"][name] = "connection_error"
        time.sleep(0.2)  # Rate limiting
    
    print(f"\n   Summary: {working_endpoints}/{len(endpoints)} endpoints working")
    
    # 8. Media Test
    print_section("8. Media Library Check")
    
    try:
        media_response = api_client.request('GET', '/wp-json/wp/v2/media?per_page=10')
        
        if media_response.status_code == 200:
            media_items = media_response.json()
            print(f"✅ Media library accessible - {len(media_items)} items found")
            
            results["tests"]["media"] = {
                "status": "passed",
                "count": len(media_items),
                "samples": []
            }
            
            if media_items:
                print("\n   Recent media:")
                for item in media_items[:3]:
                    media_title = item.get('title', {}).get('rendered', 'Untitled')
                    media_type = item.get('media_type', 'unknown')
                    media_url = item.get('source_url', '')
                    print(f"     • {media_title} ({media_type})")
                    results["tests"]["media"]["samples"].append({
                        "title": media_title,
                        "type": media_type,
                        "url": media_url
                    })
        else:
            print(f"❌ Media library error: Status {media_response.status_code}")
            results["tests"]["media"] = {"status": "failed", "code": media_response.status_code}
            
    except Exception as e:
        print(f"❌ Media check error: {e}")
        results["tests"]["media"] = {"status": "failed", "error": str(e)}
    
    # Final Summary
    print_section("📊 Test Summary")
    
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
    
    # Key findings
    print("\n🔑 Key Findings:")
    
    # Site status
    if results["tests"].get("site_connection", {}).get("status") == "passed":
        print(f"   • Site is properly connected and configured")
    else:
        print(f"   • ⚠️  Site connection issues detected")
    
    # Plugin status
    if results["tests"].get("wpbm_plugin", {}).get("status") == "passed":
        print(f"   • WP Bulk Manager plugin is active and working")
    else:
        print(f"   • ❌ WP Bulk Manager plugin needs attention")
    
    # Content
    pages_total = results["tests"].get("pages", {}).get("total", 0)
    posts_total = results["tests"].get("posts", {}).get("total", 0)
    print(f"   • Content: {pages_total} pages, {posts_total} posts")
    
    # SEO
    if results["tests"].get("seo", {}).get("status") == "passed":
        missing_seo = results["tests"]["seo"].get("missing_titles", 0) + results["tests"]["seo"].get("missing_descriptions", 0)
        if missing_seo > 0:
            print(f"   • SEO: {missing_seo} items need optimization")
        else:
            print(f"   • SEO: All analyzed pages have SEO data")
    
    # CRUD
    crud_working = all([
        results["tests"].get("crud_create", {}).get("status") == "passed",
        results["tests"].get("crud_read", {}).get("status") == "passed",
        results["tests"].get("crud_update", {}).get("status") == "passed"
    ])
    if crud_working:
        print(f"   • All CRUD operations working properly")
    else:
        print(f"   • ⚠️  Some CRUD operations need attention")
    
    print(f"\n🏁 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save results
    with open('derekzar_test_report.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Detailed report saved to: derekzar_test_report.json")
    
    return results

if __name__ == "__main__":
    try:
        results = test_derekzar()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)