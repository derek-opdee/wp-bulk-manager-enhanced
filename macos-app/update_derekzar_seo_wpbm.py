#!/usr/bin/env python3
"""
Update SEO titles and descriptions for derekzar.com using WPBM API
Using The SEO Framework meta fields (_genesis_title and _genesis_description)
"""
import requests
import json
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
    
    def test_wpbm_connection(self) -> bool:
        """Test WPBM API connection"""
        try:
            print("Testing WPBM API connection...")
            
            # Test health endpoint
            response = requests.get(f'{self.base_url}/wp-json/wpbm/v1/health', headers=self.headers)
            print(f"WPBM health endpoint: {response.status_code}")
            
            if response.status_code == 200:
                status_data = response.json()
                print(f"✅ WPBM API connection successful")
                print(f"   Version: {status_data.get('version', 'Unknown')}")
                print(f"   Status: {status_data.get('status', 'Unknown')}")
                return True
            else:
                print(f"❌ WPBM API connection failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing WPBM connection: {e}")
            return False
    
    def get_all_pages_wpbm(self) -> List[Dict]:
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
            print(f"Error fetching pages via WPBM: {e}")
            return []
    
    def update_page_seo_wpbm(self, page_id: int, title: str, description: str) -> bool:
        """Update SEO meta fields using WPBM API"""
        try:
            url = f'{self.base_url}/wp-json/wpbm/v1/content/{page_id}'
            
            data = {
                'meta': {
                    '_genesis_title': title,
                    '_genesis_description': description
                }
            }
            
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"Error updating page {page_id} via WPBM: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return False
    
    def get_page_by_id_wpbm(self, page_id: int) -> Dict:
        """Get a specific page via WPBM API"""
        try:
            url = f'{self.base_url}/wp-json/wpbm/v1/content/{page_id}'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching page {page_id}: {e}")
            return {}
    
    def verify_page_seo_direct(self, page_id: int) -> Dict:
        """Verify SEO meta fields by checking WordPress REST API directly"""
        try:
            # Try to read from WordPress REST API directly to verify the meta was set
            # This is read-only so should work with the API key
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            url = f'{self.base_url}/wp-json/wp/v2/pages/{page_id}'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                page_data = response.json()
                meta = page_data.get('meta', {})
                return {
                    'genesis_title': meta.get('_genesis_title', ''),
                    'genesis_description': meta.get('_genesis_description', '')
                }
            else:
                print(f"Warning: Could not verify page {page_id} via WordPress API: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"Error verifying page {page_id}: {e}")
            return {}
    
    def update_all_seo(self, dry_run: bool = True) -> Dict:
        """Update SEO for all pages using WPBM API"""
        if not self.test_wpbm_connection():
            return {'error': 'WPBM API connection failed'}
        
        pages = self.get_all_pages_wpbm()
        results = {
            'total_pages': len(pages),
            'updated': 0,
            'skipped': 0,
            'errors': 0,
            'details': []
        }
        
        print(f"Found {len(pages)} pages via WPBM API")
        print(f"{'DRY RUN - ' if dry_run else ''}Updating SEO data...")
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
                
                if not dry_run:
                    success = self.update_page_seo_wpbm(page_id, seo_title, seo_description)
                    if success:
                        results['updated'] += 1
                        print("✅ Updated successfully")
                    else:
                        results['errors'] += 1
                        print("❌ Update failed")
                else:
                    print("✅ Ready to update (dry run)")
                    results['updated'] += 1
                
                results['details'].append({
                    'page_id': page_id,
                    'title': page_title,
                    'slug': slug,
                    'seo_title': seo_title,
                    'seo_description': seo_description,
                    'title_length': len(seo_title),
                    'description_length': len(seo_description)
                })
            else:
                print(f"Page: {page_title} (ID: {page_id})")
                print(f"Slug: {slug}")
                print("⚠️  No SEO data found for this slug")
                results['skipped'] += 1
            
            print("-" * 40)
        
        return results
    
    def verify_updates(self) -> Dict:
        """Verify that SEO updates were applied correctly"""
        if not self.test_wpbm_connection():
            return {'error': 'WPBM API connection failed'}
        
        pages = self.get_all_pages_wpbm()
        verification = {
            'total_checked': 0,
            'correctly_updated': 0,
            'missing_updates': 0,
            'details': []
        }
        
        print("Verifying SEO updates...")
        print("=" * 50)
        
        for page in pages:
            page_id = page['id']
            slug = page['slug']
            
            if slug in self.seo_data:
                verification['total_checked'] += 1
                expected_title = self.seo_data[slug]['title']
                expected_description = self.seo_data[slug]['description']
                
                # Get SEO meta data directly from WordPress API
                seo_meta = self.verify_page_seo_direct(page_id)
                current_title = seo_meta.get('genesis_title', '')
                current_description = seo_meta.get('genesis_description', '')
                
                title_match = current_title == expected_title
                description_match = current_description == expected_description
                
                if title_match and description_match:
                    verification['correctly_updated'] += 1
                    status = "✅ Correctly updated"
                else:
                    verification['missing_updates'] += 1
                    status = "❌ Missing or incorrect"
                
                print(f"Page: {page['title']} (ID: {page_id})")
                print(f"Status: {status}")
                print(f"Title match: {title_match}")
                print(f"Description match: {description_match}")
                
                verification['details'].append({
                    'page_id': page_id,
                    'slug': slug,
                    'title_match': title_match,
                    'description_match': description_match,
                    'current_title': current_title,
                    'current_description': current_description,
                    'expected_title': expected_title,
                    'expected_description': expected_description
                })
                
                print("-" * 40)
        
        return verification


def main():
    """Main execution function"""
    updater = DerekZarSEOUpdater('0b2d82ec91d2d876558ce460e57a7a1e')
    
    print("Derek Zar SEO Update Tool - WPBM API Version")
    print("=" * 50)
    
    # Run dry run first
    print("\n1. Running dry run...")
    dry_results = updater.update_all_seo(dry_run=True)
    
    if 'error' in dry_results:
        print(f"❌ Error: {dry_results['error']}")
        return
    
    print(f"\nDry Run Summary:")
    print(f"Total pages: {dry_results['total_pages']}")
    print(f"Ready to update: {dry_results['updated']}")
    print(f"Skipped: {dry_results['skipped']}")
    
    # Perform actual updates
    print("\n2. Performing actual updates...")
    live_results = updater.update_all_seo(dry_run=False)
    
    print(f"\nUpdate Results:")
    print(f"Total pages: {live_results['total_pages']}")
    print(f"Successfully updated: {live_results['updated']}")
    print(f"Skipped: {live_results['skipped']}")
    print(f"Errors: {live_results['errors']}")
    
    if live_results['errors'] > 0:
        print("\n⚠️  Some updates failed. Check the output above for details.")
    else:
        print("\n✅ All SEO updates completed successfully!")
    
    # Verify updates
    print("\n3. Verifying updates...")
    verification = updater.verify_updates()
    
    if 'error' not in verification:
        print(f"\nVerification Summary:")
        print(f"Total checked: {verification['total_checked']}")
        print(f"Correctly updated: {verification['correctly_updated']}")
        print(f"Missing updates: {verification['missing_updates']}")
        
        if verification['missing_updates'] == 0:
            print("\n🎉 All SEO updates verified successfully!")
        else:
            print(f"\n⚠️  {verification['missing_updates']} pages need attention")
    
    return live_results


if __name__ == "__main__":
    main()