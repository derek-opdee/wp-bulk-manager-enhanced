#!/usr/bin/env python3
"""
Final SEO Update for derekzar.com 
Using correct The SEO Framework meta fields and clearing cache
"""
import requests
import json
import time
from typing import Dict, List

class DerekZarSEOUpdater:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://derekzar.com'
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
        
        # SEO data for each page - Australian English, lean communicator voice, Melbourne-focused
        self.seo_data = {
            'home': {
                'title': 'AI Innovation Strategist & Consultant Melbourne | Derek Zar',
                'description': 'Transform your business with AI. Melbourne-based strategist Derek Zar delivers practical AI solutions, executive training, and innovation consulting.'
            },
            'about': {
                'title': 'About Derek Zar | AI Innovation Strategist Melbourne',
                'description': 'Meet Derek Zar, Melbourne\'s trusted AI strategist. Specialising in practical AI transformation, cloud architecture, and executive enablement.'
            },
            'contact': {
                'title': 'Contact Derek Zar | AI Consultant Melbourne',
                'description': 'Ready to transform with AI? Contact Melbourne-based AI strategist Derek Zar for consulting, training, and innovation solutions.'
            },
            'projects': {
                'title': 'AI Projects & Case Studies | Derek Zar Melbourne',
                'description': 'Explore Derek Zar\'s AI transformation projects. Real-world case studies from Melbourne businesses implementing practical AI solutions.'
            },
            'all-services': {
                'title': 'AI Services & Solutions | Derek Zar Melbourne',
                'description': 'Complete AI services from Melbourne\'s leading strategist. Strategy, architecture, training, and agentic AI development solutions.'
            },
            'ai-strategy-transformation': {
                'title': 'AI Strategy & Transformation | Derek Zar Melbourne',
                'description': 'Strategic AI transformation for Melbourne businesses. Practical roadmaps, implementation planning, and organisational change management.'
            },
            'fractional-ai-executive': {
                'title': 'Fractional AI Executive | Derek Zar Melbourne',
                'description': 'Part-time AI leadership for Melbourne companies. Executive guidance, strategic planning, and AI governance without full-time commitment.'
            },
            'agentic-ai-development': {
                'title': 'Agentic AI Development | Derek Zar Melbourne',
                'description': 'Build autonomous AI agents for your Melbourne business. Custom development, integration, and deployment of intelligent automation systems.'
            },
            'ai-cloud-architecture': {
                'title': 'AI Cloud Architecture | Derek Zar Melbourne',
                'description': 'Scalable AI infrastructure for Melbourne enterprises. Cloud-native architectures, deployment strategies, and platform optimisation.'
            },
            'ai-training-enablement': {
                'title': 'AI Training & Enablement | Derek Zar Melbourne',
                'description': 'Empower your Melbourne team with AI skills. Executive workshops, technical training, and organisational enablement programmes.'
            },
            'speaking-workshops': {
                'title': 'AI Speaking & Workshops | Derek Zar Melbourne',
                'description': 'Engage your Melbourne audience with AI insights. Expert keynote speaking, executive workshops, and comprehensive team training sessions.'
            },
            'investment-opportunities': {
                'title': 'AI Investment Opportunities | Derek Zar Melbourne',
                'description': 'Strategic AI investment advice for Melbourne investors. Comprehensive market analysis, technology evaluation, and portfolio guidance strategies.'
            },
            'privacy-policy': {
                'title': 'Privacy Policy | Derek Zar AI Consultant Melbourne',
                'description': 'Privacy policy for Derek Zar AI consulting services. How we protect your data and respect your privacy in Melbourne and beyond.'
            }
        }
    
    def get_all_pages(self) -> List[Dict]:
        """Fetch all pages using WPBM API"""
        try:
            url = f'{self.base_url}/wp-json/wpbm/v1/content'
            params = {
                'type': 'page',
                'limit': 100,
                'status': 'publish'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get('posts', [])
            
        except Exception as e:
            print(f"Error fetching pages: {e}")
            return []
    
    def update_page_seo_comprehensive(self, page_id: int, title: str, description: str) -> bool:
        """Update SEO with all possible TSF meta field combinations"""
        
        # The SEO Framework meta fields - comprehensive approach
        meta_data = {
            # Standard TSF meta fields
            '_tsf_title_no_blogname': title,
            '_tsf_description_no_additions': description,
            
            # Alternative TSF fields
            '_open_graph_title': title,
            '_open_graph_description': description,
            '_twitter_title': title,
            '_twitter_description': description,
            
            # Backup standard fields (in case TSF falls back to these)
            '_genesis_title': title,
            '_genesis_description': description,
            
            # Yoast compatibility (in case there's dual support)
            '_yoast_wpseo_title': title,
            '_yoast_wpseo_metadesc': description,
            
            # Generic SEO fields
            '_seo_title': title,
            '_seo_description': description
        }
        
        try:
            url = f'{self.base_url}/wp-json/wpbm/v1/content/{page_id}'
            data = {'meta': meta_data}
            
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"Error updating page {page_id}: {e}")
            return False
    
    def clear_cache_attempt(self) -> bool:
        """Attempt to clear any caching that might prevent SEO updates from showing"""
        try:
            # Try to clear object cache if available
            cache_url = f'{self.base_url}/wp-json/objectcache/v1/flush'
            cache_response = requests.post(cache_url, headers=self.headers)
            
            if cache_response.status_code == 200:
                print("✅ Object cache cleared")
                return True
            else:
                print(f"Cache clear failed: {cache_response.status_code}")
                return False
                
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False
    
    def update_all_seo_final(self) -> Dict:
        """Final comprehensive SEO update"""
        pages = self.get_all_pages()
        results = {
            'total_pages': len(pages),
            'updated': 0,
            'skipped': 0,
            'errors': 0,
            'details': []
        }
        
        print(f"Found {len(pages)} pages")
        print("Performing comprehensive SEO updates...")
        print("=" * 80)
        
        for page in pages:
            page_id = page['id']
            page_title = page['title']
            slug = page['slug']
            
            if slug in self.seo_data:
                seo_info = self.seo_data[slug]
                seo_title = seo_info['title']
                seo_description = seo_info['description']
                
                print(f"Page: {page_title} (ID: {page_id})")
                print(f"Slug: {slug}")
                print(f"SEO Title: {seo_title} ({len(seo_title)} chars)")
                print(f"SEO Description: {seo_description} ({len(seo_description)} chars)")
                
                success = self.update_page_seo_comprehensive(page_id, seo_title, seo_description)
                if success:
                    results['updated'] += 1
                    print("✅ Updated successfully")
                else:
                    results['errors'] += 1
                    print("❌ Update failed")
                
                results['details'].append({
                    'page_id': page_id,
                    'title': page_title,
                    'slug': slug,
                    'seo_title': seo_title,
                    'seo_description': seo_description,
                    'success': success
                })
            else:
                print(f"Page: {page_title} (ID: {page_id})")
                print(f"Slug: {slug}")
                print("⚠️  No SEO data found for this slug")
                results['skipped'] += 1
            
            print("-" * 40)
        
        # Try to clear cache after all updates
        print("\\nAttempting to clear cache...")
        self.clear_cache_attempt()
        
        return results
    
    def verify_html_output(self, wait_time: int = 5) -> Dict:
        """Verify SEO updates in actual HTML output"""
        import re
        
        print(f"\\nWaiting {wait_time} seconds for updates to propagate...")
        time.sleep(wait_time)
        
        verification = {
            'pages_checked': 0,
            'titles_updated': 0,
            'descriptions_updated': 0,
            'details': []
        }
        
        # Check a few key pages
        test_pages = [
            ('home', 'https://derekzar.com/'),
            ('about', 'https://derekzar.com/about/'),
            ('contact', 'https://derekzar.com/contact/'),
            ('investment-opportunities', 'https://derekzar.com/investment-opportunities/')
        ]
        
        for slug, url in test_pages:
            if slug in self.seo_data:
                verification['pages_checked'] += 1
                expected_title = self.seo_data[slug]['title']
                expected_desc = self.seo_data[slug]['description']
                
                try:
                    response = requests.get(url)
                    html = response.text
                    
                    # Extract title
                    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                    current_title = title_match.group(1).strip() if title_match else ''
                    
                    # Extract description
                    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
                    current_desc = desc_match.group(1) if desc_match else ''
                    
                    # Check if our SEO data appears
                    title_updated = expected_title.split('|')[0].strip() in current_title
                    desc_updated = expected_desc[:50] in current_desc  # Check first 50 chars
                    
                    if title_updated:
                        verification['titles_updated'] += 1
                    if desc_updated:
                        verification['descriptions_updated'] += 1
                    
                    verification['details'].append({
                        'slug': slug,
                        'url': url,
                        'expected_title': expected_title,
                        'current_title': current_title,
                        'expected_desc': expected_desc,
                        'current_desc': current_desc,
                        'title_updated': title_updated,
                        'desc_updated': desc_updated
                    })
                    
                    print(f"Page: {slug}")
                    print(f"  Title updated: {'✅' if title_updated else '❌'}")
                    print(f"  Description updated: {'✅' if desc_updated else '❌'}")
                    print(f"  Current title: {current_title[:60]}...")
                    print(f"  Current desc: {current_desc[:80]}...")
                    print()
                    
                except Exception as e:
                    print(f"Error checking {slug}: {e}")
        
        return verification


def main():
    """Main execution function"""
    updater = DerekZarSEOUpdater('0b2d82ec91d2d876558ce460e57a7a1e')
    
    print("Derek Zar Final SEO Update")
    print("=" * 50)
    
    # Perform comprehensive updates
    print("\\n1. Performing comprehensive SEO updates...")
    update_results = updater.update_all_seo_final()
    
    print(f"\\nUpdate Results:")
    print(f"Total pages: {update_results['total_pages']}")
    print(f"Successfully updated: {update_results['updated']}")
    print(f"Skipped: {update_results['skipped']}")
    print(f"Errors: {update_results['errors']}")
    
    if update_results['errors'] == 0:
        print("\\n✅ All SEO updates completed successfully!")
    else:
        print(f"\\n⚠️  {update_results['errors']} updates failed")
    
    # Verify HTML output
    print("\\n2. Verifying HTML output...")
    verification = updater.verify_html_output()
    
    print(f"\\nVerification Summary:")
    print(f"Pages checked: {verification['pages_checked']}")
    print(f"Titles updated: {verification['titles_updated']}")
    print(f"Descriptions updated: {verification['descriptions_updated']}")
    
    if verification['titles_updated'] > 0 or verification['descriptions_updated'] > 0:
        print("\\n🎉 SEO updates are live and working!")
    else:
        print("\\n⚠️  SEO updates may need manual verification or cache clearing")
    
    return update_results


if __name__ == "__main__":
    main()