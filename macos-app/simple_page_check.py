#!/usr/bin/env python3
"""
Simple check of Reno Warriors pages
"""

from wpbm_manager_mysql import WPBulkManagerMySQL

def simple_page_check():
    manager = WPBulkManagerMySQL()
    
    print("🏠 RENO WARRIORS PAGE STRUCTURE CHECK")
    print("=" * 50)
    
    try:
        # Get client
        client = manager.get_client('renowarriors')
        if not client:
            print("❌ Could not connect to Reno Warriors")
            return
        
        print("✅ Connected to Reno Warriors")
        
        page_ids = [7556, 7557, 7558, 7559, 7560]
        
        for page_id in page_ids:
            print(f"\n📄 Checking Page {page_id}:")
            
            try:
                # Get page content
                result = client.get_content(page_id)
                print(f"   API Response type: {type(result)}")
                
                if isinstance(result, list):
                    print(f"   Response is list with {len(result)} items")
                    if result:
                        first_item = result[0]
                        print(f"   First item type: {type(first_item)}")
                        if isinstance(first_item, dict):
                            print(f"   Keys: {list(first_item.keys())}")
                            title = first_item.get('title', 'No title')
                            print(f"   Title: {title}")
                            
                            # Check content structure
                            content = first_item.get('content', '')
                            if content:
                                h1_count = content.count('<h1')
                                h2_count = content.count('<h2')
                                h3_count = content.count('<h3')
                                word_count = len(content.split())
                                
                                print(f"   H1 tags: {h1_count}")
                                print(f"   H2 tags: {h2_count}")
                                print(f"   H3 tags: {h3_count}")
                                print(f"   Word count: {word_count}")
                                
                                # Check for duplicate H1s
                                if h1_count > 1:
                                    print(f"   ❌ DUPLICATE H1s FOUND!")
                                elif h1_count == 1:
                                    print(f"   ✅ Single H1 found")
                                else:
                                    print(f"   ⚠️ No H1 found")
                            else:
                                print(f"   ⚠️ No content found")
                
                elif isinstance(result, dict):
                    print(f"   Response is dict")
                    print(f"   Keys: {list(result.keys())}")
                    
                    title = result.get('title', 'No title')
                    print(f"   Title: {title}")
                    
                    content = result.get('content', '')
                    if content:
                        h1_count = content.count('<h1')
                        h2_count = content.count('<h2')
                        h3_count = content.count('<h3')
                        word_count = len(content.split())
                        
                        print(f"   H1 tags: {h1_count}")
                        print(f"   H2 tags: {h2_count}")
                        print(f"   H3 tags: {h3_count}")
                        print(f"   Word count: {word_count}")
                        
                        # Check for duplicate H1s
                        if h1_count > 1:
                            print(f"   ❌ DUPLICATE H1s FOUND!")
                        elif h1_count == 1:
                            print(f"   ✅ Single H1 found")
                        else:
                            print(f"   ⚠️ No H1 found")
                else:
                    print(f"   Unexpected response type: {type(result)}")
                    print(f"   Response: {result}")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        print(f"\n📊 Quick Summary:")
        print(f"   All 5 pages checked")
        print(f"   Check for H1 structure and content length")
        
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")

if __name__ == "__main__":
    simple_page_check()