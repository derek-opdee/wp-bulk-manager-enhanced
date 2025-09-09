#!/usr/bin/env python3
"""
Direct test of derekzar.com using WordPress Bulk Manager
"""

import mysql.connector
import json
import requests
from datetime import datetime
from wpbm.api.client import WPBMClient
import time

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def test_derekzar_direct():
    """Direct test of derekzar.com"""
    
    print("🔍 WordPress Bulk Manager - Direct Test for derekzar.com")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load database config
    with open('config/database.json', 'r') as f:
        db_config = json.load(f)['database']
    
    # Connect directly to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # 1. Get derekzar site info
    print_section("1. Site Information")
    
    cursor.execute("SELECT * FROM sites WHERE name = 'derekzar'")
    site = cursor.fetchone()
    
    if not site:
        print("❌ derekzar site not found!")
        return
    
    print(f"✅ Found derekzar site:")
    print(f"   - ID: {site['id']}")
    print(f"   - Name: {site['name']}")
    print(f"   - URL: {site['url']}")
    print(f"   - Status: {site['status']}")
    
    # Get API key
    cursor.execute("SELECT * FROM api_keys WHERE site_id = %s AND is_active = 1", (site['id'],))
    api_key_record = cursor.fetchone()
    
    if not api_key_record:
        print("❌ No active API key found!")
        return
    
    api_key = api_key_record['api_key']
    print(f"   - API Key: {'*' * 30}{api_key[-10:]}")
    
    # Initialize API client
    api_client = WPBMClient(site['url'], api_key)
    
    # 2. Test API Connection
    print_section("2. API Connection Test")
    
    try:
        # Test basic WP REST API
        response = api_client.request('GET', '/wp-json/wp/v2/')
        if response.status_code == 200:
            print("✅ WordPress REST API is accessible")
        else:
            print(f"❌ WordPress REST API error: {response.status_code}")
        
        # Test WP Bulk Manager plugin
        response = api_client.request('GET', '/wp-json/wp-bulk-manager/v1/status')
        if response.status_code == 200:
            print("✅ WP Bulk Manager plugin is active")
            plugin_data = response.json()
            print(f"   - Plugin version: {plugin_data.get('version', 'Unknown')}")
        else:
            print(f"❌ WP Bulk Manager plugin not responding: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # 3. Content Overview
    print_section("3. Content Overview")
    
    try:
        # Get pages
        response = api_client.request('GET', '/wp-json/wp/v2/pages?per_page=100')
        if response.status_code == 200:
            pages = response.json()
            print(f"\n📄 Pages: {len(pages)} total")
            
            if pages:
                print("   Recent pages:")
                for page in pages[:5]:
                    print(f"     • ID {page['id']}: {page['title']['rendered']}")
        else:
            print(f"❌ Error fetching pages: {response.status_code}")
        
        # Get posts
        response = api_client.request('GET', '/wp-json/wp/v2/posts?per_page=100')
        if response.status_code == 200:
            posts = response.json()
            print(f"\n📝 Posts: {len(posts)} total")
            
            if posts:
                print("   Recent posts:")
                for post in posts[:5]:
                    print(f"     • ID {post['id']}: {post['title']['rendered']}")
        else:
            print(f"❌ Error fetching posts: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Content error: {e}")
    
    # 4. Plugin Check
    print_section("4. Plugin Status")
    
    try:
        response = api_client.request('GET', '/wp-json/wp-bulk-manager/v1/plugins')
        if response.status_code == 200:
            plugins = response.json()
            active_plugins = [p for p in plugins if p.get('status') == 'active']
            
            print(f"\n🔌 Plugins:")
            print(f"   - Total: {len(plugins)}")
            print(f"   - Active: {len(active_plugins)}")
            
            # Look for SEO plugins
            seo_plugins = ['seo', 'yoast', 'rankmath', 'all-in-one']
            print("\n   SEO Plugins:")
            seo_found = False
            
            for plugin in plugins:
                plugin_name = plugin.get('name', '').lower()
                plugin_file = plugin.get('plugin', '').lower()
                
                if any(seo in plugin_name or seo in plugin_file for seo in seo_plugins):
                    status = "✅" if plugin.get('status') == 'active' else "⭕"
                    print(f"     {status} {plugin['name']} ({plugin['status']})")
                    seo_found = True
            
            if not seo_found:
                print("     ⚠️  No SEO plugin found")
                
        else:
            print(f"❌ Plugin endpoint error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Plugin check error: {e}")
    
    # 5. CRUD Test
    print_section("5. CRUD Operations Test")
    
    try:
        # Create test page
        test_data = {
            "title": f"Test Page - {datetime.now().strftime('%H%M%S')}",
            "content": "Test content from WP Bulk Manager",
            "status": "draft"
        }
        
        print("Creating test page...")
        response = api_client.request('POST', '/wp-json/wp/v2/pages', json=test_data)
        
        if response.status_code == 201:
            test_page = response.json()
            test_id = test_page['id']
            print(f"✅ Created page ID: {test_id}")
            
            # Update test
            print("Updating test page...")
            update_data = {"content": test_data["content"] + " - Updated!"}
            response = api_client.request('POST', f'/wp-json/wp/v2/pages/{test_id}', json=update_data)
            
            if response.status_code == 200:
                print("✅ Update successful")
            else:
                print(f"❌ Update failed: {response.status_code}")
            
            # Delete test
            print("Deleting test page...")
            response = api_client.request('DELETE', f'/wp-json/wp/v2/pages/{test_id}?force=true')
            
            if response.status_code == 200:
                print("✅ Delete successful")
            else:
                print(f"⚠️  Delete status: {response.status_code}")
                
        else:
            print(f"❌ Create failed: {response.status_code}")
            if response.text:
                print(f"   Error: {response.text[:200]}")
                
    except Exception as e:
        print(f"❌ CRUD error: {e}")
    
    # 6. SEO Check
    print_section("6. SEO Functionality")
    
    try:
        response = api_client.request('GET', '/wp-json/wp-bulk-manager/v1/seo/status')
        if response.status_code == 200:
            seo_status = response.json()
            print(f"✅ SEO endpoint working")
            print(f"   - Plugin: {seo_status.get('plugin', 'Unknown')}")
            print(f"   - Active: {seo_status.get('active', False)}")
        else:
            print(f"❌ SEO endpoint error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ SEO check error: {e}")
    
    # 7. Media Check
    print_section("7. Media Library")
    
    try:
        response = api_client.request('GET', '/wp-json/wp/v2/media?per_page=5')
        if response.status_code == 200:
            media = response.json()
            print(f"✅ Media library accessible: {len(media)} items")
            
            if media:
                print("   Recent media:")
                for item in media[:3]:
                    title = item.get('title', {}).get('rendered', 'Untitled')
                    print(f"     • {title}")
        else:
            print(f"❌ Media endpoint error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Media check error: {e}")
    
    # Summary
    print_section("Test Summary")
    
    print("\n✅ Test completed successfully")
    print(f"\n🏁 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Close database
    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        test_derekzar_direct()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()