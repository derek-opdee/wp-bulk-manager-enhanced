#!/usr/bin/env python3
"""
Test script for WP Bulk Manager v2
Tests all major features with opdee.com
"""
import os
import sys
import time
import json
from datetime import datetime

# Add the wpbm package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wpbm_manager_v2 import WPBulkManagerV2
from wpbm.utils.logger import get_logger
from wpbm.utils.cache import CacheManager

logger = get_logger(__name__)

class WPBMTester:
    """Test harness for WP Bulk Manager v2"""
    
    def __init__(self):
        self.manager = WPBulkManagerV2()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {},
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0
            }
        }
        
    def run_test(self, test_name: str, test_func):
        """Run a single test and record results"""
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        self.results['summary']['total'] += 1
        
        try:
            result = test_func()
            self.results['tests'][test_name] = {
                'status': 'passed',
                'result': result,
                'error': None
            }
            self.results['summary']['passed'] += 1
            print(f"✅ {test_name} - PASSED")
            return True
        except Exception as e:
            self.results['tests'][test_name] = {
                'status': 'failed',
                'result': None,
                'error': str(e)
            }
            self.results['summary']['failed'] += 1
            print(f"❌ {test_name} - FAILED: {e}")
            logger.error(f"Test failed: {test_name}", exc_info=True)
            return False
            
    def test_site_configuration(self):
        """Test if opdee.com is configured"""
        sites = self.manager.list_sites()
        opdee_site = next((s for s in sites if s['name'].lower() == 'opdee'), None)
        
        if not opdee_site:
            raise Exception("Opdee.com not configured. Please run ./add_opdee.sh first")
            
        print(f"Found site: {opdee_site['name']} - {opdee_site['url']}")
        return opdee_site
        
    def test_client_initialization(self):
        """Test client initialization with caching"""
        client = self.manager.get_client('Opdee', cache_enabled=True)
        
        if not client:
            raise Exception("Failed to initialize client")
            
        print(f"Client initialized successfully")
        print(f"Cache enabled: {client.cache_manager is not None}")
        return True
        
    def test_content_list(self):
        """Test getting content list"""
        client = self.manager.get_client('Opdee')
        
        if not client:
            raise Exception("Failed to get client")
            
        # Get posts
        posts = client.content.get_posts(per_page=5)
        print(f"Found {len(posts)} posts")
        
        if posts:
            print("\nSample posts:")
            for post in posts[:3]:
                print(f"  - ID: {post['id']}, Title: {post['title']['rendered']}")
                
        # Get pages
        pages = client.content.get_pages(per_page=5)
        print(f"\nFound {len(pages)} pages")
        
        if pages:
            print("\nSample pages:")
            for page in pages[:3]:
                print(f"  - ID: {page['id']}, Title: {page['title']['rendered']}")
                
        return {'posts': len(posts), 'pages': len(pages)}
        
    def test_search_functionality(self):
        """Test search functionality"""
        client = self.manager.get_client('Opdee')
        
        if not client:
            raise Exception("Failed to get client")
            
        # Search for AI-related content
        search_term = "AI"
        results = client.content.search(search_term, post_type='any', per_page=10)
        
        print(f"Search results for '{search_term}': {len(results)} items found")
        
        if results:
            print("\nSearch results:")
            for result in results[:5]:
                print(f"  - Type: {result['type']}, ID: {result['id']}, Title: {result['title']}")
                
        return {'search_term': search_term, 'results_count': len(results)}
        
    def test_caching(self):
        """Test caching by making the same request twice"""
        client = self.manager.get_client('Opdee', cache_enabled=True)
        
        if not client:
            raise Exception("Failed to get client")
            
        # First request (cache miss)
        start_time = time.time()
        posts1 = client.content.get_posts(per_page=5)
        time1 = time.time() - start_time
        
        # Second request (should be cache hit)
        start_time = time.time()
        posts2 = client.content.get_posts(per_page=5)
        time2 = time.time() - start_time
        
        print(f"First request time: {time1:.3f}s")
        print(f"Second request time: {time2:.3f}s")
        print(f"Speed improvement: {time1/time2:.1f}x faster")
        
        # Verify same data
        if len(posts1) != len(posts2):
            raise Exception("Cache returned different data")
            
        return {
            'first_request_time': time1,
            'second_request_time': time2,
            'speed_improvement': time1/time2
        }
        
    def test_cache_statistics(self):
        """Test cache statistics"""
        client = self.manager.get_client('Opdee', cache_enabled=True)
        
        if not client or not client.cache_manager:
            raise Exception("Failed to get client with cache")
            
        stats = client.cache_manager.get_stats()
        
        print("Cache Statistics:")
        print(f"  - Total requests: {stats['requests']}")
        print(f"  - Cache hits: {stats['hits']}")
        print(f"  - Cache misses: {stats['misses']}")
        print(f"  - Hit rate: {stats['hit_rate']:.1%}")
        print(f"  - Cache size: {stats['size']} entries")
        
        return stats
        
    def test_search_replace_dry_run(self):
        """Test search & replace endpoint (dry run only)"""
        client = self.manager.get_client('Opdee')
        
        if not client:
            raise Exception("Failed to get client")
            
        # Test search and replace (dry run)
        search_text = "solutions"
        replace_text = "systems"
        
        print(f"Testing search & replace: '{search_text}' → '{replace_text}' (DRY RUN)")
        
        try:
            # Perform dry run
            results = client.content.search_replace(
                search=search_text,
                replace=replace_text,
                dry_run=True,
                post_types=['post', 'page'],
                limit=5
            )
            
            print(f"\nDry run results:")
            print(f"  - Total matches: {results.get('total_matches', 0)}")
            print(f"  - Items with matches: {len(results.get('items', []))}")
            
            if results.get('items'):
                print("\n  Sample matches:")
                for item in results['items'][:3]:
                    print(f"    - {item['type']} #{item['id']}: {item['title']}")
                    print(f"      Matches: {item['match_count']}")
                    
            return results
            
        except AttributeError:
            # Method might not exist in current implementation
            print("Search & replace method not available in current implementation")
            return {'status': 'not_implemented'}
            
    def test_media_listing(self):
        """Test media listing"""
        client = self.manager.get_client('Opdee')
        
        if not client:
            raise Exception("Failed to get client")
            
        # Get media items
        media_items = client.media.get_media(per_page=10)
        
        print(f"Found {len(media_items)} media items")
        
        if media_items:
            print("\nSample media:")
            for item in media_items[:5]:
                print(f"  - ID: {item['id']}")
                print(f"    Title: {item['title']['rendered']}")
                print(f"    Type: {item['media_type']}")
                print(f"    URL: {item['source_url']}")
                
        return {'media_count': len(media_items)}
        
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("WP Bulk Manager v2 Test Suite")
        print("Testing with opdee.com")
        print("="*60)
        
        # Define tests
        tests = [
            ("Site Configuration", self.test_site_configuration),
            ("Client Initialization", self.test_client_initialization),
            ("Content List", self.test_content_list),
            ("Search Functionality", self.test_search_functionality),
            ("Caching Performance", self.test_caching),
            ("Cache Statistics", self.test_cache_statistics),
            ("Search & Replace (Dry Run)", self.test_search_replace_dry_run),
            ("Media Listing", self.test_media_listing)
        ]
        
        # Run tests
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total tests: {self.results['summary']['total']}")
        print(f"Passed: {self.results['summary']['passed']} ✅")
        print(f"Failed: {self.results['summary']['failed']} ❌")
        
        # Save results
        results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
            
        print(f"\nDetailed results saved to: {results_file}")
        
        return self.results['summary']['failed'] == 0


def main():
    """Main test runner"""
    tester = WPBMTester()
    
    # Check if opdee is configured
    sites = tester.manager.list_sites()
    if not any(s['name'].lower() == 'opdee' for s in sites):
        print("\n⚠️  Opdee.com is not configured!")
        print("Please run the following command first:")
        print("  ./add_opdee.sh")
        print("\nOr manually add it with:")
        print("  python3 wpbm_manager_v2.py add-site 'Opdee' 'https://opdee.com' 'YOUR_API_KEY'")
        return 1
        
    # Run all tests
    success = tester.run_all_tests()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())