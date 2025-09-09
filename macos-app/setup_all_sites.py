#!/usr/bin/env python3
"""
Setup and test all WordPress sites
"""

from wpbm_manager_mysql import WPBulkManagerMySQL
from wpbm.api.client import WPBMClient
import time

# Site configurations
sites = [
    {
        'name': 'opdee',
        'url': 'https://opdee.com',
        'api_key': '27013065aa24d225b5ea9db967d191f3',
        'brand_voice': 'Professional and innovative, focusing on technology solutions and digital transformation'
    },
    {
        'name': 'boulderworks',
        'url': 'https://www.boulderworks.net',
        'api_key': 'HKq068Yl4ybRqhGjBfhF9siINYIl31G6',
        'brand_voice': 'Professional manufacturing tone, emphasizing precision, quality, and expertise in laser cutting and engraving'
    },
    {
        'name': 'dmbelectrical',
        'url': 'https://dmbelectrical.com.au',
        'api_key': '3bc76a99bd13cf7f7fc3c2bd5c7211ab',
        'brand_voice': 'Trustworthy and professional Australian electrical services, emphasizing safety, reliability, and local expertise'
    },
    {
        'name': 'renowarriors',
        'url': 'https://renowarriors.com.au',
        'api_key': '0ab365b5b83f46b65bf12466c404bfd3',
        'brand_voice': 'Energetic and confident Australian renovation specialists, focusing on transformation, quality craftsmanship, and customer satisfaction'
    },
    {
        'name': 'lawnenforcement',
        'url': 'https://lawnenforcement.com.au',
        'api_key': '17968bd29377e5def11aa1dbec45234a',
        'brand_voice': 'Friendly yet authoritative Australian lawn care experts, using clever wordplay while maintaining professionalism'
    },
    {
        'name': 'mavent',
        'url': 'https://mavent.com.au',
        'api_key': 'a1879934e2f9b0688de5fa140c27b966',
        'brand_voice': 'Modern and innovative Australian business solutions, professional yet approachable'
    }
]

def setup_and_test_sites():
    """Add all sites and test connections"""
    manager = WPBulkManagerMySQL()
    results = []
    
    print("🚀 Setting up WordPress sites...\n")
    
    for site in sites:
        print(f"📝 Processing {site['name']}...")
        
        # Check if site already exists
        existing = manager.db.get_site(site['name'])
        if existing:
            print(f"  ⚠️  Site already exists, skipping creation")
            site_id = existing['id']
        else:
            # Add site
            result = manager.add_site(
                name=site['name'],
                url=site['url'],
                api_key=site['api_key'],
                brand_voice=site['brand_voice']
            )
            
            if result['success']:
                print(f"  ✅ Site added successfully")
                print(f"  📁 Folder: {result['folder_path']}")
                site_id = result['site_id']
            else:
                print(f"  ❌ Failed to add: {result.get('error', 'Unknown error')}")
                results.append({
                    'site': site['name'],
                    'url': site['url'],
                    'status': 'Failed to add',
                    'error': result.get('error')
                })
                continue
        
        # Test connection
        print(f"  🔍 Testing connection...")
        try:
            client = WPBMClient(site['url'], site['api_key'])
            
            # Test health endpoint
            start_time = time.time()
            health = client.get('/health', use_cache=False)
            response_time = int((time.time() - start_time) * 1000)
            
            if health.get('status') in ['ok', 'healthy']:
                print(f"  ✅ Connection successful (Response time: {response_time}ms)")
                
                # Get some basic info
                try:
                    # Get content count
                    pages = client.get('/content', params={'type': 'page', 'per_page': 1})
                    posts = client.get('/content', params={'type': 'post', 'per_page': 1})
                    
                    # Get plugin count
                    try:
                        plugins = client.get('/plugins')
                        plugin_count = len(plugins) if isinstance(plugins, list) else 'N/A'
                    except:
                        plugin_count = 'N/A'
                    
                    # Log successful access
                    manager.track_api_access(
                        site['name'], '/health', 'GET', 
                        200, response_time
                    )
                    
                    results.append({
                        'site': site['name'],
                        'url': site['url'],
                        'status': 'Connected',
                        'response_time': f"{response_time}ms",
                        'pages': 'Yes' if pages else 'No',
                        'posts': 'Yes' if posts else 'No',
                        'plugins': plugin_count
                    })
                    
                except Exception as e:
                    results.append({
                        'site': site['name'],
                        'url': site['url'],
                        'status': 'Connected (Limited)',
                        'error': str(e)
                    })
            else:
                print(f"  ⚠️  Health check failed")
                results.append({
                    'site': site['name'],
                    'url': site['url'],
                    'status': 'Health check failed',
                    'error': health
                })
                
        except Exception as e:
            print(f"  ❌ Connection failed: {str(e)}")
            manager.track_api_access(
                site['name'], '/health', 'GET',
                500, 0, str(e)
            )
            results.append({
                'site': site['name'],
                'url': site['url'],
                'status': 'Connection failed',
                'error': str(e)
            })
        
        print()  # Empty line between sites
    
    # Update brand kits with Australian-specific content for AU sites
    au_sites = ['dmbelectrical', 'renowarriors', 'lawnenforcement', 'mavent']
    
    for site_name in au_sites:
        if any(r['site'] == site_name and r['status'] in ['Connected', 'Connected (Limited)'] for r in results):
            print(f"🇦🇺 Updating {site_name} with Australian brand kit...")
            
            au_brand_data = {
                'vocabulary_preferences': 'Australian spelling (colour, centre, organisation)',
                'local_keywords': ['australia', 'australian', 'aussie', 'local', 'melbourne', 'sydney', 'brisbane'],
                'compliance_requirements': 'Australian Consumer Law, Fair Trading',
                'currency': 'AUD',
                'measurement': 'metric'
            }
            
            manager.update_brand_voice(site_name, au_brand_data)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 SETUP SUMMARY")
    print("="*60)
    
    for result in results:
        status_icon = "✅" if result['status'] in ['Connected', 'Connected (Limited)'] else "❌"
        print(f"\n{status_icon} {result['site']} ({result['url']})")
        print(f"   Status: {result['status']}")
        
        if result.get('response_time'):
            print(f"   Response Time: {result['response_time']}")
        if result.get('pages'):
            print(f"   Content: Pages={result['pages']}, Posts={result['posts']}")
        if result.get('plugins') and result['plugins'] != 'N/A':
            print(f"   Plugins: {result['plugins']}")
        if result.get('error'):
            print(f"   Error: {result['error']}")
    
    # Show database summary
    print("\n" + "="*60)
    print("📊 DATABASE SUMMARY")
    print("="*60)
    
    all_sites = manager.list_sites()
    print(f"\nTotal sites in database: {len(all_sites)}")
    
    for site in all_sites:
        print(f"\n• {site['name']}:")
        print(f"  - Status: {site['status']}")
        print(f"  - Last accessed: {site.get('last_accessed', 'Never')}")
        print(f"  - API calls: {site.get('api_key_count', 0)}")
        print(f"  - Has templates: {'Yes' if site.get('has_templates') else 'No'}")
        print(f"  - Has brand kit: {'Yes' if site.get('has_brand_kit') else 'No'}")

if __name__ == "__main__":
    setup_and_test_sites()