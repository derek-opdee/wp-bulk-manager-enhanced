#!/usr/bin/env python3
import sys
sys.path.append('.')
from wpbm.api.client import WPBMClient
import re
import time

def fix_h1_for_page(client, page_id):
    """Fix H1 duplicates for a specific page"""
    print(f'\nAttempting comprehensive H1 fix for page {page_id}...')
    
    try:
        page = client.get_content_by_id(page_id)
        content = page.get('content', '')
        title = page.get('title', '')
        print(f'Page: {title}')
        print(f'Content length: {len(content)}')
        
        original_content = content
        
        # Find all H1 tags
        h1_pattern = r'<h1([^>]*)>(.*?)</h1>'
        matches = list(re.finditer(h1_pattern, content, re.IGNORECASE | re.DOTALL))
        print(f'Found {len(matches)} H1 matches')
        
        # Show what we found
        for i, match in enumerate(matches):
            h1_text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
            print(f'  H1 #{i+1}: {h1_text}')
        
        if len(matches) > 1:
            # Convert all but the first H1 to H2
            for i, match in enumerate(matches[1:], 1):
                old_h1 = match.group(0)
                new_h2 = f'<h2{match.group(1)}>{match.group(2)}</h2>'
                content = content.replace(old_h1, new_h2, 1)
                print(f'  Converting H1 #{i+1} to H2')
        
        # Check if we made changes
        if content != original_content:
            print('Content was modified - applying update...')
            
            # Force update with status change to bypass caching
            update_data = {
                'content': content
            }
            
            response = client.update_content(page_id, update_data)
            print(f'Update response: {response}')
            
            # Wait for changes to propagate
            time.sleep(5)
            
            # Verify the fix
            updated_page = client.get_content_by_id(page_id)
            updated_content = updated_page.get('content', '')
            
            final_h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', updated_content, re.IGNORECASE | re.DOTALL)
            print(f'Final H1 count: {len(final_h1s)}')
            
            if len(final_h1s) == 1:
                print('✅ H1 fix successful!')
                return True
            else:
                print(f'⚠️  Still has {len(final_h1s)} H1 tags')
                for i, h1 in enumerate(final_h1s):
                    h1_text = re.sub(r'<[^>]+>', '', h1).strip()
                    print(f'  Remaining H1 #{i+1}: {h1_text}')
                return False
        else:
            print('No H1 changes needed')
            return True
            
    except Exception as e:
        print(f'Error: {e}')
        return False

def main():
    client = WPBMClient('https://derekzar.com', '0b2d82ec91d2d876558ce460e57a7a1e')
    
    # Pages that need H1 fixes
    pages_with_h1_issues = [2196, 2194, 2192, 2188, 2183, 2177]
    
    print("🔧 Aggressive H1 Fix for Derek Zar Pages")
    print("=" * 50)
    
    results = {}
    for page_id in pages_with_h1_issues:
        success = fix_h1_for_page(client, page_id)
        results[page_id] = success
        time.sleep(2)  # Rate limiting
    
    print("\n📊 RESULTS SUMMARY")
    print("=" * 30)
    for page_id, success in results.items():
        status = "✅ Fixed" if success else "❌ Still has issues"
        print(f"Page {page_id}: {status}")

if __name__ == "__main__":
    main()