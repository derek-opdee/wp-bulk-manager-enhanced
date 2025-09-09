#!/usr/bin/env python3
"""
Update SEO titles and descriptions for derekzar.com (Auto version)
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
            'Authorization': f'Bearer {api_key}',
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
        """Fetch all pages from WordPress"""
        url = f'{self.base_url}/wp-json/wp/v2/pages'
        params = {'per_page': 100}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching pages: {e}")
            return []
    
    def update_page_seo(self, page_id: int, title: str, description: str) -> bool:
        """Update SEO meta fields for a specific page"""
        url = f'{self.base_url}/wp-json/wp/v2/pages/{page_id}'
        
        data = {
            'meta': {
                '_genesis_title': title,
                '_genesis_description': description
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error updating page {page_id}: {e}")
            print(f"Response: {response.text if 'response' in locals() else 'No response'}")
            return False
    
    def update_all_seo(self, dry_run: bool = True) -> Dict:
        """Update SEO for all pages"""
        pages = self.get_all_pages()
        results = {
            'total_pages': len(pages),
            'updated': 0,
            'skipped': 0,
            'errors': 0,
            'details': []
        }
        
        print(f"Found {len(pages)} pages")
        print(f"{'DRY RUN - ' if dry_run else ''}Updating SEO data...")
        print("=" * 80)
        
        for page in pages:
            page_id = page['id']
            page_title = page['title']['rendered']
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
                    success = self.update_page_seo(page_id, seo_title, seo_description)
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
    
    def validate_seo_lengths(self) -> Dict:
        """Validate SEO title and description lengths"""
        validation = {
            'valid_titles': 0,
            'valid_descriptions': 0,
            'invalid_titles': [],
            'invalid_descriptions': []
        }
        
        for slug, seo in self.seo_data.items():
            title_len = len(seo['title'])
            desc_len = len(seo['description'])
            
            # Titles should be 30-60 characters
            if 30 <= title_len <= 60:
                validation['valid_titles'] += 1
            else:
                validation['invalid_titles'].append({
                    'slug': slug, 
                    'title': seo['title'], 
                    'length': title_len
                })
            
            # Descriptions should be 120-160 characters
            if 120 <= desc_len <= 160:
                validation['valid_descriptions'] += 1
            else:
                validation['invalid_descriptions'].append({
                    'slug': slug, 
                    'description': seo['description'], 
                    'length': desc_len
                })
        
        return validation


def main():
    """Main execution function"""
    updater = DerekZarSEOUpdater('0b2d82ec91d2d876558ce460e57a7a1e')
    
    print("Derek Zar SEO Update Tool - Auto Version")
    print("=" * 50)
    
    # First, validate SEO lengths
    print("\n1. Validating SEO data lengths...")
    validation = updater.validate_seo_lengths()
    
    print(f"Valid titles (30-60 chars): {validation['valid_titles']}")
    print(f"Valid descriptions (120-160 chars): {validation['valid_descriptions']}")
    
    if validation['invalid_titles']:
        print("\n⚠️  Invalid title lengths:")
        for item in validation['invalid_titles']:
            print(f"  {item['slug']}: {item['length']} chars - {item['title']}")
    
    if validation['invalid_descriptions']:
        print("\n⚠️  Invalid description lengths:")
        for item in validation['invalid_descriptions']:
            print(f"  {item['slug']}: {item['length']} chars")
    
    # Run dry run first
    print("\n2. Running dry run...")
    dry_results = updater.update_all_seo(dry_run=True)
    
    print(f"\nDry Run Summary:")
    print(f"Total pages: {dry_results['total_pages']}")
    print(f"Ready to update: {dry_results['updated']}")
    print(f"Skipped: {dry_results['skipped']}")
    
    # Proceed with actual updates automatically
    print("\n3. Performing actual updates...")
    live_results = updater.update_all_seo(dry_run=False)
    
    print(f"\nFinal Results:")
    print(f"Total pages: {live_results['total_pages']}")
    print(f"Successfully updated: {live_results['updated']}")
    print(f"Skipped: {live_results['skipped']}")
    print(f"Errors: {live_results['errors']}")
    
    if live_results['errors'] > 0:
        print("\n⚠️  Some updates failed. Check the output above for details.")
    else:
        print("\n✅ All SEO updates completed successfully!")
    
    return live_results


if __name__ == "__main__":
    main()