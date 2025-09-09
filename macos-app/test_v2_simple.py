#!/usr/bin/env python3
"""
Simple test of WP Bulk Manager v2 with opdee.com
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm import WPBMClient

def test_simple():
    print("Testing WP Bulk Manager v2 with opdee.com")
    print("-" * 40)
    
    # Test 1: Basic connection
    print("\n1. Testing basic connection...")
    try:
        client = WPBMClient(
            site_url="https://opdee.com",
            api_key="8u5foF2Sbegg5nBRt0IVtL6MhsGufq6U",
            cache_enabled=True
        )
        print("✅ Client created")
        
        # Get just 2 pages
        pages = client.get('/content', params={'type': 'page', 'limit': 2})
        print(f"✅ Got {len(pages.get('posts', []))} pages")
        
        if pages.get('posts'):
            print(f"   - {pages['posts'][0]['title']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()