#!/usr/bin/env python3
"""
Check page status and list all pages
"""

from wpbm_manager_mysql import WPBulkManagerMySQL

def check_page_status():
    manager = WPBulkManagerMySQL()
    
    print("🏠 CHECKING RENO WARRIORS PAGES STATUS")
    print("=" * 50)
    
    try:
        client = manager.get_client('renowarriors')
        if not client:
            print("❌ Could not connect to Reno Warriors")
            return
        
        print("✅ Connected to Reno Warriors")
        
        # First, let's list all pages to see what's available
        print("\n📋 Listing all pages:")
        try:
            all_pages = client.list_content('pages')
            print(f"   Found {len(all_pages)} pages total")
            
            # Look for our specific pages
            target_ids = [7556, 7557, 7558, 7559, 7560]
            found_pages = []
            
            for page in all_pages:
                page_id = page.get('id', 0)
                title = page.get('title', 'No title')
                status = page.get('status', 'unknown')
                
                if page_id in target_ids:
                    found_pages.append({
                        'id': page_id,
                        'title': title,
                        'status': status
                    })
                    print(f"   ✅ Found target page {page_id}: {title} (Status: {status})")
            
            print(f"\n📊 Target Pages Status:")
            print(f"   Looking for IDs: {target_ids}")
            print(f"   Found: {len(found_pages)} pages")
            
            if not found_pages:
                print("   ⚠️ None of our target pages found in the list")
                print("   📝 Showing first 10 pages for reference:")
                for i, page in enumerate(all_pages[:10]):
                    print(f"      {page.get('id', 'No ID')}: {page.get('title', 'No title')} ({page.get('status', 'unknown')})")
            
            # Try to get draft pages specifically
            print("\n📝 Checking for draft pages:")
            try:
                draft_pages = client.list_content('pages', status='draft')
                print(f"   Found {len(draft_pages)} draft pages")
                
                for page in draft_pages:
                    page_id = page.get('id', 0)
                    if page_id in target_ids:
                        title = page.get('title', 'No title')
                        print(f"   ✅ Draft page {page_id}: {title}")
                        
                        # Try to get full content for this page
                        try:
                            full_page = client.get_content(page_id, include_content=True)
                            if full_page:
                                print(f"      📄 Got full content for page {page_id}")
                                
                                # Analyze the content
                                if isinstance(full_page, list) and full_page:
                                    content = full_page[0].get('content', '')
                                elif isinstance(full_page, dict):
                                    content = full_page.get('content', '')
                                else:
                                    content = str(full_page)
                                
                                if content:
                                    # Quick structure analysis
                                    h1_count = content.count('<h1')
                                    h2_count = content.count('<h2')
                                    h3_count = content.count('<h3')
                                    gutenberg_blocks = content.count('<!-- wp:')
                                    word_count = len(content.split())
                                    
                                    print(f"      🔤 H1: {h1_count}, H2: {h2_count}, H3: {h3_count}")
                                    print(f"      🧱 Gutenberg blocks: {gutenberg_blocks}")
                                    print(f"      📝 Words: {word_count}")
                                    
                                    # Check for duplicate H1s
                                    if h1_count > 1:
                                        print(f"      ❌ DUPLICATE H1s detected!")
                                    elif h1_count == 1:
                                        print(f"      ✅ Perfect H1 structure")
                                    else:
                                        print(f"      ⚠️ No H1 found")
                                else:
                                    print(f"      ⚠️ No content found")
                        except Exception as e:
                            print(f"      ❌ Error getting full content: {str(e)}")
                
            except Exception as e:
                print(f"   ❌ Error getting draft pages: {str(e)}")
                
        except Exception as e:
            print(f"❌ Error listing pages: {str(e)}")
        
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")

if __name__ == "__main__":
    check_page_status()